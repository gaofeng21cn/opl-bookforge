from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def chapter_statuses(root: Path) -> dict[str, Any]:
    metrics_path = root / "artifacts/stage_outputs/chapter-materialization/manuscript-metrics.json"
    if not metrics_path.exists():
        return {"status": "missing_metrics", "path": rel(metrics_path, root)}
    try:
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"status": "invalid_metrics", "path": rel(metrics_path, root), "error": str(exc)}
    chapters = metrics.get("chapters")
    return {
        "status": "loaded" if isinstance(chapters, list) else "missing_chapters",
        "assembly_status": metrics.get("assembly_status"),
        "extent_status": metrics.get("extent_status"),
        "total_chars": metrics.get("total_chars"),
        "estimated_pages_at_600_chars": metrics.get("estimated_pages_at_600_chars"),
        "target_chars_min": metrics.get("target_chars_min"),
        "missing_chars_min": metrics.get("missing_chars_min"),
        "review_pdf": metrics.get("completed_chapters_review", {}),
        "chapters": chapters if isinstance(chapters, list) else [],
    }


def review_pdf_export_summary(root: Path) -> dict[str, Any]:
    export_path = root / "artifacts/review/completed-chapters.review-pdf-export.json"
    if not export_path.exists():
        return {}
    try:
        export = json.loads(export_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {
        "nonblank_pages": export.get("rendered_page_inspection", {}).get("nonblank_pages"),
        "markdown_image_refs_present": export.get("markdown_image_refs", {}).get("present_count"),
        "markdown_image_refs_total": export.get("markdown_image_refs", {}).get("total"),
        "markdown_image_refs_missing": export.get("markdown_image_refs", {}).get("missing_count"),
    }


def figure_asset_summary(root: Path) -> dict[str, Any]:
    manifest_path = root / "artifacts/stage_outputs/chapter-materialization/figure-asset-manifest.json"
    if not manifest_path.exists():
        return {}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    figures = manifest.get("figures") if isinstance(manifest.get("figures"), list) else []
    asset_ready = 0
    preview_only = 0
    planned = 0
    project_local_paths = 0
    for item in figures:
        status = item.get("asset_status")
        if status == "asset_ready":
            asset_ready += 1
        elif status == "preview_only":
            preview_only += 1
        elif status == "planned":
            planned += 1
        asset = item.get("project_local_path")
        if asset and (root / asset).exists():
            project_local_paths += 1
    figure_dir = root / "artifacts/figures"
    figure_files = [
        path for path in figure_dir.glob("*")
        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    ] if figure_dir.exists() else []
    return {
        "asset_ready": asset_ready,
        "preview_only": preview_only,
        "planned": planned,
        "project_local_paths": project_local_paths,
        "figure_files": len(figure_files),
    }
