#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path
from typing import Any


VERSION = "bookforge-imagegen-asset.v2"


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


def build_task_prompt(args: argparse.Namespace, output_file: Path, prompt: str) -> str:
    tool_options = {
        "type": "image_generation",
        "size": args.size,
        "quality": args.quality,
        "format": output_file.suffix.lower().lstrip(".") or "png",
        "background": "opaque",
    }
    return "\n".join([
        "你是 OPL Book Forge 的 Codex executor，负责执行书稿插图资产生成任务。",
        "必须显式使用 $imagegen 或 Codex 原生 image_generation 能力生成 raster bitmap。不要使用脚本绘图、SVG、HTML 截图、占位图、外部 curl/fetch、显式 Base URL、显式 API key 或 OPENAI_API_KEY。",
        "最终 bitmap 必须由本次 OPL executor task 直接物化到指定 output_file；其他位置的预览或临时图片不计为书稿资产。",
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
        }, ensure_ascii=False),
    ])


def build_opl_executor_request(
    args: argparse.Namespace,
    root: Path,
    output_file: Path,
    prompt: str,
) -> dict[str, Any]:
    request: dict[str, Any] = {
        "executor_kind": "codex_cli",
        "mode": "bookforge_project_image_asset",
        "prompt": build_task_prompt(args, output_file, prompt),
        "cwd": str(root),
        "timeout_ms": args.timeout * 1000,
        "json": True,
        "required_capabilities": ["image_generation"],
        "domain_payload": {
            "domain_id": "opl-bookforge",
            "artifact_role": args.artifact_role,
            "figure_id": args.figure_id,
            "output_ref": rel(output_file, root),
        },
    }
    if args.model:
        request["model"] = args.model
    if args.reasoning_effort:
        request["reasoning_effort"] = args.reasoning_effort
    return request


def read_opl_executor_receipt(stdout: str) -> dict[str, Any]:
    response = json.loads(stdout)
    if not isinstance(response, dict):
        raise ValueError("OPL executor response must be a JSON object")
    receipt = response.get("agent_execution_receipt")
    if not isinstance(receipt, dict):
        raise ValueError("OPL executor response has no agent_execution_receipt")
    return receipt


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


def materialize_progress_diagnostic(
    payload: dict[str, Any],
    *,
    code: str,
    error: str,
) -> dict[str, Any]:
    payload["status"] = "completed_with_quality_debt"
    payload["blocker_kind"] = None
    payload["error"] = error
    payload["progress_diagnostic"] = {
        "code": code,
        "detail": error,
        "no_output": payload.get("asset") is None,
        "blocks_stage_transition": False,
        "blocks_quality_export_or_ready_claims": True,
        "next_stage_may_start": True,
        "route_selection_owner": "codex_cli",
    }
    return payload


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
                "session_id",
                "requested_capabilities",
                "activated_capabilities",
                "materialized_by",
                "provider_token_source",
            )
            if key in runtime
        }
        target["review_result"] = "Generated through Book Forge native imagegen helper; visual review still required before publication proof."
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
    with tempfile.TemporaryDirectory(prefix="bookforge-opl-executor-") as tmp:
        request_file = Path(tmp) / "agent-execution-request.json"
        write_json(request_file, build_opl_executor_request(args, root, output_file, prompt))
        try:
            result = subprocess.run(
                [args.opl_bin, "executor", "run", "--request", str(request_file), "--json"],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )
        except OSError as exc:
            payload["status"] = "blocked_opl_executor_unavailable"
            payload["blocker_kind"] = "opl_executor_command_unavailable"
            payload["error"] = str(exc)
            return payload
        if result.returncode != 0:
            return materialize_progress_diagnostic(
                payload,
                code="image_generation_attempt_failed",
                error=(result.stderr or result.stdout or "OPL image-generation executor task failed").strip()[-4000:],
            )

        try:
            receipt = read_opl_executor_receipt(result.stdout)
        except (json.JSONDecodeError, ValueError) as exc:
            payload["status"] = "blocked_invalid_opl_executor_receipt"
            payload["blocker_kind"] = "opl_executor_receipt_invalid"
            payload["error"] = str(exc)
            return payload
        requested = receipt.get("requested_capabilities")
        activated = receipt.get("activated_capabilities")
        if requested != ["image_generation"] or activated != ["image_generation"]:
            payload["status"] = "blocked_opl_capability_not_activated"
            payload["blocker_kind"] = "opl_executor_image_generation_capability_not_activated"
            payload["error"] = "OPL executor receipt did not prove activation of the requested image_generation capability."
            return payload

        if receipt.get("exit_code") != 0:
            return materialize_progress_diagnostic(
                payload,
                code="image_generation_attempt_failed",
                error=safe_text(receipt.get("stderr_preview"), "OPL executor returned a non-zero exit code.")[-4000:],
            )

        if not output_file.is_file():
            return materialize_progress_diagnostic(
                payload,
                code="project_bitmap_not_materialized",
                error=f"OPL executor completed without creating output_file: {output_file}",
            )

        info = image_info(output_file)
        payload["status"] = "asset_ready"
        payload["asset"] = {
            "path": rel(output_file, root),
            **info,
        }
        payload["generation_runtime"] = {
            "provider": safe_text(receipt.get("executor_kind"), "codex_cli"),
            "task_surface": safe_text(receipt.get("surface_kind"), "opl_agent_execution_receipt"),
            "imagegen_mode": "opl_executor_required_capability",
            "session_id": receipt.get("session_id"),
            "requested_capabilities": requested,
            "activated_capabilities": activated,
            "materialized_by": "opl_executor_task_to_domain_owned_output_ref",
            "model_selection": args.model or "inherit_local_codex_default",
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
        test_args.prompt = "Draw a simple Book Forge imagegen helper self-test bitmap."
        test_args.prompt_file = None
        test_args.figure_id = "self-test"
        test_args.title = "Book Forge imagegen helper self-test"
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
    parser = argparse.ArgumentParser(description="Generate OPL Book Forge project-local bitmap figure assets through Codex native imagegen.")
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
    parser.add_argument("--opl-bin", default=os.environ.get("OPL_BIN", "opl"), help="Canonical OPL CLI used for executor transport.")
    parser.add_argument("--model", default=os.environ.get("OBF_CODEX_MODEL", ""), help="Optional model override passed through OPL executor request.")
    parser.add_argument("--reasoning-effort", default=os.environ.get("OBF_CODEX_REASONING_EFFORT", ""), help="Optional reasoning override passed through OPL executor request.")
    parser.add_argument("--timeout", type=int, default=900, help="OPL executor request timeout in seconds.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
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
    if args.output_file is None:
        print("missing required --output-file", file=sys.stderr)
        return 2

    output_file = project_path(root, args.output_file)
    manifest = project_path(root, args.manifest)
    asset_manifest = project_path(root, args.asset_manifest)
    prompt = read_prompt(args)
    if not prompt:
        payload = materialize_progress_diagnostic(
            base_payload(args, root, output_file, prompt),
            code="image_prompt_missing",
            error="missing required prompt or prompt-file",
        )
        write_json(manifest, payload)
        try:
            update_asset_manifest(asset_manifest, manifest, payload, root)
        except Exception as exc:
            payload["progress_diagnostic"]["asset_manifest_update_error"] = str(exc)
            write_json(manifest, payload)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    try:
        payload = generate_mock(args, root, output_file, prompt) if args.mock else generate_live(args, root, output_file, prompt)
    except Exception as exc:
        payload = base_payload(args, root, output_file, prompt)
        payload = materialize_progress_diagnostic(
            payload,
            code=(
                "corrupt_or_unreadable_output"
                if output_file.exists()
                else "image_helper_attempt_failed"
            ),
            error=str(exc),
        )
    write_json(manifest, payload)
    if asset_manifest:
        try:
            update_asset_manifest(asset_manifest, manifest, payload, root)
        except Exception as exc:
            if payload["status"] == "asset_ready":
                payload = materialize_progress_diagnostic(
                    payload,
                    code="asset_manifest_update_failed",
                    error=str(exc),
                )
            else:
                payload.setdefault("progress_diagnostic", {})["asset_manifest_update_error"] = str(exc)
            write_json(manifest, payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["status"] in {"asset_ready", "completed_with_quality_debt"} else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
