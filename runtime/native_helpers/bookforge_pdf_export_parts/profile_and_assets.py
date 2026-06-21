from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


DEFAULT_PUBLICATION_PROFILE = "bookforge-zh-publication-proof"
BUNDLED_PROFILE_DIR = Path(__file__).resolve().parents[1] / "pdf_profiles"
MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def read_json_object(path: Path | None) -> tuple[dict[str, Any], str | None]:
    if path is None:
        return {}, None
    if not path.exists():
        return {}, f"JSON evidence file not found: {path}"
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {}, f"invalid JSON evidence file {path}: {exc}"
    if not isinstance(parsed, dict):
        return {}, f"JSON evidence root must be an object: {path}"
    return parsed, None


def resolve_publication_profile(ref: str, root: Path) -> tuple[dict[str, Any], Path | None, str | None]:
    if ref in ("", "none", "None", "NONE"):
        return {}, None, None

    profile_ref = ref or DEFAULT_PUBLICATION_PROFILE
    candidate = Path(profile_ref)
    if candidate.suffix:
        path = candidate if candidate.is_absolute() else (root / candidate)
    else:
        path = BUNDLED_PROFILE_DIR / f"{profile_ref}.json"

    path = path.resolve()
    profile, error = read_json_object(path)
    if error:
        return {}, path, error
    return profile, path, None


def profile_list(profile: dict[str, Any], key: str) -> list[Any]:
    value = profile.get(key)
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        nested = value.get("items")
        return nested if isinstance(nested, list) else []
    return []


def resolve_profile_path(ref: Any, profile_path: Path | None, root: Path) -> Path | None:
    if not isinstance(ref, str) or not ref.strip():
        return None
    path = Path(ref)
    if path.is_absolute():
        return path.resolve()
    base = profile_path.parent if profile_path else root
    return (base / path).resolve()


def file_refs_exist(refs: list[Any], root: Path) -> tuple[list[str], list[str]]:
    present: list[str] = []
    missing: list[str] = []
    for item in refs:
        if not isinstance(item, str) or not item.strip():
            missing.append(str(item))
            continue
        path = Path(item)
        candidate = path if path.is_absolute() else root / path
        if candidate.exists() and (not candidate.is_file() or candidate.stat().st_size > 0):
            present.append(item)
        else:
            missing.append(item)
    return present, missing


def is_remote_or_data_ref(ref: str) -> bool:
    parsed = urlparse(ref)
    return parsed.scheme in {"http", "https", "data", "mailto"}


def image_refs_from_pandoc_ast(source_md: Path, root: Path) -> list[str] | None:
    if not command_exists("pandoc"):
        return None
    result = subprocess.run(
        ["pandoc", str(source_md), "-t", "json"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    try:
        ast = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None

    refs: list[str] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            if value.get("t") == "Image":
                content = value.get("c")
                if isinstance(content, list) and content:
                    target = content[-1]
                    if isinstance(target, list) and target:
                        ref = target[0]
                        if isinstance(ref, str):
                            refs.append(ref)
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(ast)
    return refs


def image_refs_from_markdown_text(source_md: Path) -> list[str]:
    try:
        source = source_md.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        source = source_md.read_text(encoding="utf-8", errors="replace")
    return [match.group(1).strip("<>") for match in MARKDOWN_IMAGE_RE.finditer(source)]


def markdown_image_refs(source_md: Path, resource_paths: list[Path], root: Path) -> dict[str, Any]:
    refs: list[dict[str, Any]] = []
    extracted_refs = image_refs_from_pandoc_ast(source_md, root)
    extraction_method = "pandoc_ast" if extracted_refs is not None else "markdown_text_scan"
    if extracted_refs is None:
        extracted_refs = image_refs_from_markdown_text(source_md)

    for raw in extracted_refs:
        raw_ref = unquote(raw.strip("<>"))
        if not raw_ref or is_remote_or_data_ref(raw_ref):
            refs.append({"ref": raw_ref, "status": "external_or_data"})
            continue

        raw_without_fragment = raw_ref.split("#", 1)[0]
        candidate = Path(raw_without_fragment)
        candidates = [candidate] if candidate.is_absolute() else [path / candidate for path in resource_paths]
        resolved = next((path for path in candidates if path.exists() and path.is_file() and path.stat().st_size > 0), None)
        refs.append({
            "ref": raw_ref,
            "status": "present" if resolved else "missing",
            "resolved": rel(resolved, root) if resolved else None,
        })

    return {
        "total": len(refs),
        "present_count": sum(1 for item in refs if item["status"] == "present"),
        "missing_count": sum(1 for item in refs if item["status"] == "missing"),
        "external_or_data_count": sum(1 for item in refs if item["status"] == "external_or_data"),
        "extraction_method": extraction_method,
        "refs": refs,
    }


def figure_manifest_readiness(figure_manifest: dict[str, Any], root: Path) -> dict[str, Any]:
    records = as_list(figure_manifest.get("figures")) or as_list(figure_manifest.get("assets"))
    required_count = 0
    ready_count = 0
    blockers: list[dict[str, str]] = []

    for item in records:
        if not isinstance(item, dict):
            continue
        required = item.get("required", True) is not False
        if not required:
            continue
        required_count += 1
        figure_id = str(item.get("id") or item.get("figure_id") or "unknown_figure")
        asset_status = str(item.get("asset_status") or item.get("status") or "")
        path_ref = item.get("project_local_path") or item.get("output_file") or item.get("asset_path")
        if not isinstance(path_ref, str) or not path_ref.strip():
            blockers.append({
                "figure_id": figure_id,
                "blocker_type": "required_figure_missing_project_local_path",
                "message": "required figure has no project-local bitmap path",
            })
            continue
        path = Path(path_ref)
        candidate = path if path.is_absolute() else root / path
        if asset_status != "asset_ready":
            blockers.append({
                "figure_id": figure_id,
                "blocker_type": "required_figure_not_asset_ready",
                "message": f"required figure asset_status is {asset_status or 'missing'}",
            })
            continue
        if not candidate.exists() or not candidate.is_file() or candidate.stat().st_size <= 0:
            blockers.append({
                "figure_id": figure_id,
                "blocker_type": "required_figure_file_missing",
                "message": f"required figure bitmap is missing or empty: {path_ref}",
            })
            continue
        ready_count += 1

    return {
        "record_count": len(records),
        "required_count": required_count,
        "ready_required_count": ready_count,
        "blockers": blockers,
    }
