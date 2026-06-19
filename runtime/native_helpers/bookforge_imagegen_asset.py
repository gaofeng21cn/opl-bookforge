#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zlib
from pathlib import Path
from typing import Any


VERSION = "bookforge-imagegen-asset.v1"
IMAGE_EXTENSIONS = (".png", ".webp", ".jpg", ".jpeg")


def safe_text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text if text else default


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def project_path(root: Path, path: Path | None) -> Path | None:
    if path is None:
        return None
    expanded = path.expanduser()
    if expanded.is_absolute():
        return expanded.resolve()
    return (root / expanded).resolve()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path | None, payload: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt_file:
        return args.prompt_file.read_text(encoding="utf-8").strip()
    return safe_text(args.prompt)


def png_chunk(kind: bytes, data: bytes) -> bytes:
    payload = kind + data
    return len(data).to_bytes(4, "big") + kind + data + (zlib.crc32(payload) & 0xFFFFFFFF).to_bytes(4, "big")


def mock_png(width: int, height: int, seed: str) -> bytes:
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    bg = (248, 246, 238, 255)
    accent = tuple(80 + (value % 120) for value in digest[:3]) + (255,)
    raw_rows: list[bytes] = []
    for y in range(height):
        row = bytearray([0])
        for x in range(width):
            band = ((x + int(y * 1.3)) % 173) < 4
            marker = (
                width * 0.08 < x < width * 0.92
                and height * 0.16 < y < height * 0.84
                and ((x // 53 + y // 41) % 13 == 0)
            )
            row.extend(accent if band or marker else bg)
        raw_rows.append(bytes(row))
    ihdr = width.to_bytes(4, "big") + height.to_bytes(4, "big") + bytes([8, 6, 0, 0, 0])
    return (
        b"\x89PNG\r\n\x1a\n"
        + png_chunk(b"IHDR", ihdr)
        + png_chunk(b"IDAT", zlib.compress(b"".join(raw_rows), 6))
        + png_chunk(b"IEND", b"")
    )


def image_info(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    if len(data) >= 24 and data[:8] == b"\x89PNG\r\n\x1a\n":
        return {
            "kind": "png",
            "width": int.from_bytes(data[16:20], "big"),
            "height": int.from_bytes(data[20:24], "big"),
            "sha256": sha256_bytes(data),
            "bytes": len(data),
        }
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return {
            "kind": "webp",
            "width": None,
            "height": None,
            "sha256": sha256_bytes(data),
            "bytes": len(data),
        }
    if len(data) >= 4 and data[:2] == b"\xff\xd8":
        return {
            "kind": "jpeg",
            "width": None,
            "height": None,
            "sha256": sha256_bytes(data),
            "bytes": len(data),
        }
    raise ValueError(f"not a supported bitmap image: {path}")


def parse_codex_command(raw: str | None) -> list[str]:
    value = safe_text(raw)
    if value:
        if value.startswith("["):
            parsed = json.loads(value)
            if not isinstance(parsed, list):
                raise ValueError("Codex command JSON must be an array")
            command = [safe_text(item) for item in parsed if safe_text(item)]
            if not command:
                raise ValueError("Codex command JSON array is empty")
            return command
        return [value]

    canonical = Path.home() / "bin" / "codex-canonical"
    if canonical.is_file() and os.access(canonical, os.X_OK):
        return [str(canonical)]
    return ["codex"]


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex").expanduser()


def generated_images_dir() -> Path:
    return codex_home() / "generated_images"


def parse_jsonl(stdout: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            events.append(parsed)
    return events


def collect_strings(value: Any, out: list[str], limit: int = 200) -> None:
    if len(out) >= limit:
        return
    if isinstance(value, str):
        if value.strip():
            out.append(value)
        return
    if isinstance(value, dict):
        for item in value.values():
            collect_strings(item, out, limit)
        return
    if isinstance(value, list):
        for item in value:
            collect_strings(item, out, limit)


def event_strings(events: list[dict[str, Any]]) -> list[str]:
    strings: list[str] = []
    for event in events:
        collect_strings(event, strings)
    return strings


def used_native_imagegen(events: list[dict[str, Any]], output_file: Path) -> bool:
    strings = event_strings(events)
    for text in strings:
        lowered = text.lower()
        if any(token in lowered for token in ("image_gen", "image_generation", "image_generation_call")):
            return True
    joined = "\n".join(strings)
    if ".codex/generated_images/" in joined and str(output_file) in joined:
        return True
    return ".codex/generated_images/" in joined and re.search(r"\b(cp|mv|rsync|install)\b", joined) is not None


def generated_paths_from_events(events: list[dict[str, Any]]) -> list[Path]:
    paths: list[Path] = []
    seen: set[str] = set()
    pattern = re.compile(r"(/[^\s\"']*\.codex/generated_images/[^\s\"']+\.(?:png|webp|jpe?g))", re.IGNORECASE)
    for text in event_strings(events):
        for match in pattern.findall(text):
            path = Path(match)
            key = str(path)
            if key not in seen:
                seen.add(key)
                paths.append(path)
    return paths


def recent_generated_images(since: float) -> list[Path]:
    root = generated_images_dir()
    if not root.is_dir():
        return []
    candidates: list[Path] = []
    for path in root.glob("*/*"):
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        try:
            if path.stat().st_mtime >= since:
                candidates.append(path)
        except OSError:
            continue
    return sorted(candidates, key=lambda item: item.stat().st_mtime, reverse=True)


def parse_last_message(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return None
    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        return None
    try:
        parsed = json.loads(match.group(0))
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        return None


def build_task_prompt(args: argparse.Namespace, output_file: Path, prompt: str) -> str:
    tool_options = {
        "type": "image_generation",
        "size": args.size,
        "quality": args.quality,
        "format": output_file.suffix.lower().lstrip(".") or "png",
        "background": "opaque",
    }
    return "\n".join([
        "你是 OPL BookForge 的 Codex executor，负责执行书稿插图资产生成任务。",
        "必须显式使用 $imagegen 或 Codex 原生 image_generation 能力生成 raster bitmap。不要使用脚本绘图、SVG、HTML 截图、占位图、外部 curl/fetch、显式 Base URL、显式 API key 或 OPENAI_API_KEY。",
        "使用内置 imagegen 默认路径生成后，把最终图片复制或移动到指定 output_file。不要把 book/project-bound asset 只留在 $CODEX_HOME/generated_images。",
        "如果可以看到内置 imagegen 的原始生成路径，请在 generated_image_file 字段返回它。",
        "如果无法生成或无法落盘，返回 JSON blocker，不要伪造图片。",
        f"bookforge_helper_version: {VERSION}",
        f"figure_id: {args.figure_id}",
        f"title: {args.title}",
        f"output_file: {output_file}",
        f"style_reference: {args.style_reference or ''}",
        f"image_tool_options: {json.dumps(tool_options, ensure_ascii=False)}",
        "",
        "Image prompt:",
        prompt,
        "",
        "完成后只回复一行 JSON，不要附加说明：",
        json.dumps({
            "ok": True,
            "mode": "codex_native_imagegen",
            "image_file": str(output_file),
            "generated_image_file": "",
        }, ensure_ascii=False),
    ])


def build_codex_args(args: argparse.Namespace, root: Path, last_message_file: Path) -> tuple[list[str], list[str]]:
    command = parse_codex_command(args.codex_command or os.environ.get("OBF_CODEX_COMMAND"))
    exec_args = [
        "exec",
        "--json",
        "--ephemeral",
        "--cd",
        str(root),
        "--skip-git-repo-check",
        "-s",
        args.sandbox,
        "-c",
        'approval_policy="never"',
    ]
    if args.model:
        exec_args.extend(["--model", args.model])
    if args.reasoning_effort:
        exec_args.extend(["-c", f'model_reasoning_effort="{args.reasoning_effort}"'])
    exec_args.extend([
        "--enable",
        "image_generation",
        "--output-last-message",
        str(last_message_file),
        "-",
    ])
    return command, exec_args


def base_payload(args: argparse.Namespace, root: Path, output_file: Path, prompt: str) -> dict[str, Any]:
    return {
        "surface_kind": "bookforge_imagegen_asset",
        "version": VERSION,
        "artifact_role": args.artifact_role,
        "figure_id": args.figure_id,
        "title": args.title,
        "root": str(root),
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "output_file": rel(output_file, root),
        "status": "blocked",
        "blocker_kind": None,
        "error": None,
        "asset": None,
        "generation_runtime": None,
        "quality_boundary": {
            "uses_codex_native_imagegen": True,
            "project_local_bitmap_required": True,
            "chat_preview_only_is_not_asset": True,
            "script_drawn_or_svg_final_figure_allowed": False,
            "explicit_provider_token_required": False,
            "provider_token_persisted": False,
        },
    }


def update_asset_manifest(asset_manifest: Path | None, receipt_path: Path | None, receipt: dict[str, Any], root: Path) -> None:
    if asset_manifest is None:
        return
    if not asset_manifest.exists():
        raise FileNotFoundError(f"asset manifest does not exist: {asset_manifest}")

    payload = read_json(asset_manifest)
    figures = payload.get("figures")
    if not isinstance(figures, list):
        raise ValueError(f"asset manifest has no figures list: {asset_manifest}")

    figure_id = safe_text(receipt.get("figure_id"))
    if not figure_id:
        raise ValueError("receipt has no figure_id")

    target = None
    for item in figures:
        if isinstance(item, dict) and item.get("id") == figure_id:
            target = item
            break
    if target is None:
        raise ValueError(f"figure id not found in asset manifest: {figure_id}")

    status = safe_text(receipt.get("status"), "blocked")
    target["asset_status"] = status
    target["receipt_ref"] = rel(receipt_path, root) if receipt_path else None
    target["blocker_kind"] = receipt.get("blocker_kind")
    target.pop("preview_note", None)
    target["prompt_sha256"] = receipt.get("prompt_sha256")
    if receipt.get("error"):
        target["error"] = receipt.get("error")
    else:
        target.pop("error", None)

    if status == "asset_ready":
        asset = receipt.get("asset") or {}
        runtime = receipt.get("generation_runtime") or {}
        target["project_local_path"] = asset.get("path") or receipt.get("output_file")
        target["asset"] = {
            key: asset.get(key)
            for key in ("kind", "width", "height", "bytes", "sha256")
            if key in asset
        }
        target["generation_runtime"] = {
            key: runtime.get(key)
            for key in (
                "provider",
                "task_surface",
                "imagegen_mode",
                "codex_generated_image_file",
                "materialized_from_codex_generated_images",
                "provider_token_source",
            )
            if key in runtime
        }
        target["review_result"] = "Generated through BookForge native imagegen helper; visual review still required before publication proof."
    else:
        target.pop("asset", None)
        target.pop("generation_runtime", None)
        target.pop("review_result", None)

    write_json(asset_manifest, payload)


def generate_mock(args: argparse.Namespace, root: Path, output_file: Path, prompt: str) -> dict[str, Any]:
    payload = base_payload(args, root, output_file, prompt)
    width, height = parse_size(args.size)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_bytes(mock_png(width, height, f"{args.figure_id}:{prompt}"))
    info = image_info(output_file)
    payload["status"] = "asset_ready"
    payload["asset"] = {
        "path": rel(output_file, root),
        **info,
    }
    payload["generation_runtime"] = {
        "provider": "mock",
        "task_surface": "bookforge_imagegen_asset_mock",
        "imagegen_mode": "mock_no_provider_call",
        "token_persisted": False,
    }
    return payload


def parse_size(value: str) -> tuple[int, int]:
    match = re.match(r"^(\d+)x(\d+)$", safe_text(value))
    if not match:
        return 1536, 1024
    return int(match.group(1)), int(match.group(2))


def generate_live(args: argparse.Namespace, root: Path, output_file: Path, prompt: str) -> dict[str, Any]:
    payload = base_payload(args, root, output_file, prompt)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    since = time.time() - 5
    with tempfile.TemporaryDirectory(prefix="bookforge-imagegen-") as tmp:
        last_message_file = Path(tmp) / "last-message.json"
        command, exec_args = build_codex_args(args, root, last_message_file)
        task_prompt = build_task_prompt(args, output_file, prompt)
        result = subprocess.run(
            [command[0], *command[1:], *exec_args],
            input=task_prompt,
            cwd=root,
            text=True,
            capture_output=True,
            timeout=args.timeout,
            check=False,
        )
        events = parse_jsonl(result.stdout)
        last_message = parse_last_message(last_message_file) or {}
        if result.returncode != 0:
            payload["status"] = "blocked_codex_exec_failed"
            payload["blocker_kind"] = "codex_native_imagegen_exec_failed"
            payload["error"] = (result.stderr or result.stdout or "Codex native imagegen task failed").strip()[-4000:]
            return payload

        generated_from_result = safe_text(last_message.get("generated_image_file"))
        candidates = []
        if generated_from_result:
            candidates.append(Path(generated_from_result).expanduser())
        candidates.extend(generated_paths_from_events(events))
        candidates.extend(recent_generated_images(since))

        if not output_file.exists():
            copied = False
            for candidate in candidates:
                if candidate.resolve() == output_file.resolve():
                    continue
                if not candidate.is_file():
                    continue
                try:
                    image_info(candidate)
                except ValueError:
                    continue
                shutil.copyfile(candidate, output_file)
                copied = True
                break
            if not copied:
                payload["status"] = "blocked_missing_project_bitmap"
                payload["blocker_kind"] = "codex_native_imagegen_did_not_materialize_project_asset"
                payload["error"] = f"output file was not created: {output_file}"
                return payload

        if not used_native_imagegen(events, output_file):
            payload["status"] = "blocked_missing_native_imagegen_provenance"
            payload["blocker_kind"] = "no_codex_native_imagegen_event_or_generated_images_ref"
            payload["error"] = "Codex task completed, but JSONL events did not prove imagegen/generated_images use."
            return payload

        info = image_info(output_file)
        payload["status"] = "asset_ready"
        payload["asset"] = {
            "path": rel(output_file, root),
            **info,
        }
        payload["generation_runtime"] = {
            "provider": "codex_native_imagegen",
            "task_surface": "codex_native_imagegen_skill",
            "imagegen_mode": "built_in_tool",
            "run_id": next((safe_text(event.get("run_id")) for event in reversed(events) if safe_text(event.get("run_id"))), ""),
            "codex_generated_image_file": rel(candidates[0], root) if candidates else None,
            "materialized_from_codex_generated_images": bool(candidates),
            "model_selection": args.model or "inherit_local_codex_default",
            "sandbox": args.sandbox,
            "tool_options": {
                "type": "image_generation",
                "size": args.size,
                "quality": args.quality,
                "format": output_file.suffix.lower().lstrip(".") or "png",
            },
            "token_persisted": False,
            "explicit_provider_token_required": False,
            "provider_token_source": "codex_executor_native_tool",
        }
        return payload


def doctor(args: argparse.Namespace) -> dict[str, Any]:
    command = parse_codex_command(args.codex_command or os.environ.get("OBF_CODEX_COMMAND"))
    help_has_image_generation = False
    help_error = None
    try:
        result = subprocess.run(
            [command[0], *command[1:], "exec", "--help"],
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
        help_has_image_generation = "--enable" in result.stdout and "FEATURE" in result.stdout
        if result.returncode != 0:
            help_error = (result.stderr or result.stdout).strip()[-1000:]
    except Exception as exc:  # pragma: no cover - diagnostic path
        help_error = str(exc)
    root = generated_images_dir()
    newest = None
    if root.is_dir():
        files = sorted((path for path in root.glob("*/*") if path.is_file()), key=lambda item: item.stat().st_mtime, reverse=True)
        if files:
            newest = str(files[0])
    return {
        "surface_kind": "bookforge_imagegen_asset_doctor",
        "version": VERSION,
        "codex_command": command,
        "codex_exec_help_has_enable_feature": help_has_image_generation,
        "codex_exec_help_error": help_error,
        "codex_home": str(codex_home()),
        "generated_images_dir": str(root),
        "generated_images_dir_exists": root.is_dir(),
        "newest_generated_image": newest,
        "default_route": "codex_native_imagegen_child_executor",
        "api_fallback_boundary": "explicit owner/operator choice for large batches or unavailable built-in imagegen; not the default BookForge route",
        "token_policy": {
            "helper_reads_openai_api_key": False,
            "helper_reads_base_url": False,
            "provider_token_source": "codex_executor_native_tool",
        },
    }


def run_self_test(args: argparse.Namespace) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="bookforge-imagegen-selftest-") as tmp:
        root = Path(tmp)
        manifest = root / "manifest.json"
        output = root / "figures" / "self-test.png"
        test_args = argparse.Namespace(**vars(args))
        test_args.mock = True
        test_args.root = root
        test_args.output_file = output
        test_args.manifest = manifest
        test_args.prompt = "Draw a simple BookForge imagegen helper self-test bitmap."
        test_args.prompt_file = None
        test_args.figure_id = "self-test"
        test_args.title = "BookForge imagegen helper self-test"
        payload = generate_mock(test_args, root, output, test_args.prompt)
        write_json(manifest, payload)
        return {
            "surface_kind": "bookforge_imagegen_asset_self_test",
            "version": VERSION,
            "status": "passed" if payload["status"] == "asset_ready" and output.exists() and manifest.exists() else "failed",
            "manifest_status": payload["status"],
            "asset_kind": payload.get("asset", {}).get("kind"),
            "asset_bytes": payload.get("asset", {}).get("bytes"),
        }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate OPL BookForge project-local bitmap figure assets through Codex native imagegen.")
    parser.add_argument("--doctor", action="store_true", help="Print local capability diagnostics without generating an image.")
    parser.add_argument("--self-test", action="store_true", help="Run a mock helper self-test without provider calls.")
    parser.add_argument("--update-asset-manifest", action="store_true", help="Update --asset-manifest from an existing --receipt-file without generating.")
    parser.add_argument("--mock", action="store_true", help="Write a deterministic mock PNG. For verification only; not a final book figure.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Book project root for relative refs.")
    parser.add_argument("--prompt", default="", help="Image prompt text.")
    parser.add_argument("--prompt-file", type=Path, help="File containing the image prompt.")
    parser.add_argument("--output-file", type=Path, help="Project-local bitmap output path.")
    parser.add_argument("--manifest", type=Path, help="Optional generation manifest path.")
    parser.add_argument("--receipt-file", type=Path, help="Existing helper receipt for --update-asset-manifest.")
    parser.add_argument("--asset-manifest", type=Path, help="Optional figure asset manifest to update by figure id after generation.")
    parser.add_argument("--figure-id", default="", help="Figure id for provenance.")
    parser.add_argument("--title", default="", help="Figure title for provenance.")
    parser.add_argument("--style-reference", default="", help="Optional style reference path recorded in the child prompt.")
    parser.add_argument("--size", default="1536x1024", help="Requested image size, e.g. 1536x1024.")
    parser.add_argument("--quality", default="high", help="Requested image quality.")
    parser.add_argument("--artifact-role", default="book_manuscript_figure", help="Artifact role recorded in the manifest.")
    parser.add_argument("--codex-command", default="", help="Codex command or JSON array. Defaults to ~/bin/codex-canonical when available, then codex.")
    parser.add_argument("--sandbox", default=os.environ.get("OBF_CODEX_SANDBOX", "workspace-write"), help="Child Codex sandbox.")
    parser.add_argument("--model", default=os.environ.get("OBF_CODEX_MODEL", ""), help="Optional child Codex model override.")
    parser.add_argument("--reasoning-effort", default=os.environ.get("OBF_CODEX_REASONING_EFFORT", ""), help="Optional child Codex reasoning override.")
    parser.add_argument("--timeout", type=int, default=900, help="Child Codex timeout in seconds.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.doctor:
        print(json.dumps(doctor(args), ensure_ascii=False, indent=2))
        return 0
    if args.self_test:
        payload = run_self_test(args)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if payload["status"] == "passed" else 1

    root = args.root.resolve()
    if args.update_asset_manifest:
        receipt_file = project_path(root, args.receipt_file)
        asset_manifest = project_path(root, args.asset_manifest)
        if receipt_file is None or asset_manifest is None:
            print("--update-asset-manifest requires --receipt-file and --asset-manifest", file=sys.stderr)
            return 2
        payload = read_json(receipt_file)
        update_asset_manifest(asset_manifest, receipt_file, payload, root)
        print(json.dumps({
            "surface_kind": "bookforge_imagegen_asset_manifest_update",
            "version": VERSION,
            "status": "updated",
            "figure_id": payload.get("figure_id"),
            "asset_manifest": rel(asset_manifest, root),
            "receipt_file": rel(receipt_file, root),
            "asset_status": payload.get("status"),
        }, ensure_ascii=False, indent=2))
        return 0

    args.prompt_file = project_path(root, args.prompt_file)
    prompt = read_prompt(args)
    if not prompt:
        print("missing required prompt or prompt-file", file=sys.stderr)
        return 2
    if args.output_file is None:
        print("missing required --output-file", file=sys.stderr)
        return 2

    output_file = project_path(root, args.output_file)
    manifest = project_path(root, args.manifest)
    asset_manifest = project_path(root, args.asset_manifest)
    try:
        payload = generate_mock(args, root, output_file, prompt) if args.mock else generate_live(args, root, output_file, prompt)
    except Exception as exc:
        payload = base_payload(args, root, output_file, prompt)
        payload["status"] = "blocked_helper_exception"
        payload["blocker_kind"] = "bookforge_imagegen_helper_exception"
        payload["error"] = str(exc)
    write_json(manifest, payload)
    if asset_manifest:
        update_asset_manifest(asset_manifest, manifest, payload, root)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["status"] == "asset_ready" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
