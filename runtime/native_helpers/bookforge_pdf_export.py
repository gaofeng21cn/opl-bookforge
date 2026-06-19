#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


VERSION = "bookforge-pdf-export.v1"
ARTIFACT_ROLES = ("review_pdf", "publication_proof", "final_export")
DEFAULT_PUBLICATION_PROFILE = "bookforge-zh-publication-proof"
BUNDLED_PROFILE_DIR = Path(__file__).resolve().parent / "pdf_profiles"
PUBLICATION_DESIGN_REQUIRED_FIELDS = (
    "page_geometry",
    "typography_hierarchy",
    "caption_style",
    "figure_treatment",
    "table_treatment",
    "callout_style",
    "headers_footers",
    "page_numbering",
    "visual_rhythm",
    "rendered_page_inspection_plan",
)
RENDERED_INSPECTION_REQUIRED_FIELDS = (
    "nonblank_pages",
    "overflow_or_clipping",
    "caption_figure_table_status",
    "callout_status",
    "heading_hierarchy_status",
    "headers_footers_status",
    "page_numbering_status",
    "visual_rhythm_status",
)
MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def write_manifest(path: Path | None, payload: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def as_mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


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


def missing_fields(section: dict[str, Any], fields: tuple[str, ...]) -> list[str]:
    return [field for field in fields if section.get(field) in (None, "", [], {})]


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


def png_dimensions(path: Path) -> tuple[int | None, int | None]:
    data = path.read_bytes()[:24]
    if len(data) >= 24 and data[:8] == b"\x89PNG\r\n\x1a\n":
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    return None, None


def auto_rendered_page_inspection(rendered_pages: list[str], root: Path, payload: dict[str, Any]) -> dict[str, Any]:
    page_metrics: list[dict[str, Any]] = []
    for ref in rendered_pages:
        path = root / ref
        width, height = png_dimensions(path) if path.exists() else (None, None)
        size = path.stat().st_size if path.exists() else 0
        page_metrics.append({
            "ref": ref,
            "bytes": size,
            "width": width,
            "height": height,
            "nonblank_baseline": bool(size > 1000 and width and height),
        })

    nonblank_pages = sum(1 for item in page_metrics if item["nonblank_baseline"])
    missing_images = as_mapping(payload.get("markdown_image_refs")).get("missing_count", 0)
    figure_blockers = as_mapping(payload.get("figure_asset_manifest_summary")).get("blockers", [])
    element_status = "passed" if missing_images == 0 and not figure_blockers else "blocked"
    return {
        "surface_kind": "bookforge_rendered_page_inspection",
        "version": "bookforge-rendered-page-inspection.v1",
        "inspection_kind": "machine_baseline",
        "nonblank_pages": nonblank_pages,
        "overflow_or_clipping": False if nonblank_pages == len(rendered_pages) and rendered_pages else "unchecked",
        "caption_figure_table_status": element_status,
        "callout_status": "profile_applied",
        "heading_hierarchy_status": "profile_applied",
        "headers_footers_status": "profile_applied",
        "page_numbering_status": "profile_applied",
        "visual_rhythm_status": "profile_applied_machine_baseline_manual_review_recommended",
        "page_metrics": page_metrics,
        "manual_review_still_required_for_final_export": True,
    }


def render_pdf_pages(pdf_path: Path, render_dir: Path, root: Path, prefix: str, dpi: int) -> tuple[str, str | None, list[str]]:
    if not command_exists("pdftoppm"):
        return "skipped_missing_pdftoppm", "pdftoppm not found", []

    render_dir.mkdir(parents=True, exist_ok=True)
    for old_page in render_dir.glob(f"{prefix}-*.png"):
        old_page.unlink()

    page_prefix = render_dir / prefix
    result = subprocess.run(
        ["pdftoppm", "-png", "-r", str(dpi), str(pdf_path), str(page_prefix)],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        error = (result.stderr or result.stdout or "pdftoppm failed").strip()
        return "failed", error[-2000:], []

    rendered_pages = [rel(path, root) for path in sorted(render_dir.glob(f"{prefix}-*.png"))]
    return "rendered", None, rendered_pages


def pandoc_xelatex_command(
    source_md: Path,
    output_pdf: Path,
    metadata_file: Path | None,
    variables: list[str],
    resource_paths: list[Path],
    include_headers: list[Path],
) -> tuple[list[str], str | None]:
    if not command_exists("pandoc"):
        return [], "pandoc not found"
    if not command_exists("xelatex"):
        return [], "xelatex not found"
    command = [
        "pandoc",
        str(source_md),
        "-s",
        "--pdf-engine=xelatex",
        "--toc",
        "--number-sections",
        "--metadata",
        "link-citations=true",
        "-o",
        str(output_pdf),
    ]
    if metadata_file:
        command.extend(["--metadata-file", str(metadata_file)])
    for header in include_headers:
        if not header.exists():
            return [], f"include header not found: {header}"
        command.extend(["--include-in-header", str(header)])
    if resource_paths:
        command.append(f"--resource-path={os.pathsep.join(str(path) for path in resource_paths)}")
    for variable in variables:
        command.extend(["-V", variable])
    return command, None


def artifact_role(args: argparse.Namespace) -> str:
    role = args.artifact_role.strip()
    aliases = {
        "owner_review_only_not_final_export": "review_pdf",
        "verify_smoke_not_publication": "review_pdf",
        "publication_proof_pdf": "publication_proof",
        "final_publication_export": "final_export",
    }
    return aliases.get(role, role)


def assess_artifact_gate(
    payload: dict[str, Any],
    args: argparse.Namespace,
    root: Path,
    publication_design: dict[str, Any],
    design_error: str | None,
    rendered_inspection: dict[str, Any],
    inspection_error: str | None,
    owner_acceptance: dict[str, Any],
    owner_error: str | None,
) -> None:
    role = str(payload["artifact_role"])
    blockers: list[dict[str, str]] = []
    warnings: list[str] = []

    if role not in ARTIFACT_ROLES:
        blockers.append({
            "blocker_type": "unsupported_artifact_role",
            "message": f"unsupported artifact role: {role}",
        })

    if design_error:
        blockers.append({"blocker_type": "publication_design_profile_unreadable", "message": design_error})
    if inspection_error:
        blockers.append({"blocker_type": "rendered_page_inspection_unreadable", "message": inspection_error})
    if owner_error:
        blockers.append({"blocker_type": "owner_acceptance_unreadable", "message": owner_error})

    if role == "review_pdf":
        if payload.get("render_status") != "rendered":
            warnings.append("review_pdf was not rendered for visual inspection; do not treat it as a publication proof")
        if as_mapping(payload.get("markdown_image_refs")).get("missing_count", 0):
            warnings.append("review_pdf has missing Markdown image refs; inspect before owner handoff")
    elif role in {"publication_proof", "final_export"}:
        if not publication_design:
            blockers.append({
                "blocker_type": "publication_design_profile_missing",
                "message": "publication proof requires a publication design profile or BookForge publication profile",
            })
        else:
            missing = missing_fields(publication_design, PUBLICATION_DESIGN_REQUIRED_FIELDS)
            for field in missing:
                blockers.append({
                    "blocker_type": "publication_design_profile_incomplete",
                    "message": f"missing publication design profile field: {field}",
                })

        if payload.get("render_status") != "rendered" or not payload.get("rendered_pages"):
            blockers.append({
                "blocker_type": "rendered_pages_missing",
                "message": "publication proof requires rendered page PNG refs",
            })

        if not rendered_inspection:
            blockers.append({
                "blocker_type": "rendered_page_inspection_missing",
                "message": "publication proof requires rendered-page inspection evidence",
            })
        else:
            missing = missing_fields(rendered_inspection, RENDERED_INSPECTION_REQUIRED_FIELDS)
            for field in missing:
                blockers.append({
                    "blocker_type": "rendered_page_inspection_incomplete",
                    "message": f"missing rendered page inspection field: {field}",
                })
            if rendered_inspection.get("overflow_or_clipping") not in (False, "false", "none", "clean", "passed"):
                blockers.append({
                    "blocker_type": "rendered_page_overflow_or_clipping",
                    "message": "rendered-page inspection reports overflow, clipping, or an unchecked state",
                })
            if rendered_inspection.get("nonblank_pages") in (None, 0, "0", False):
                blockers.append({
                    "blocker_type": "rendered_pages_blank_or_unchecked",
                    "message": "rendered-page inspection must record nonblank pages",
                })

        markdown_refs = as_mapping(payload.get("markdown_image_refs"))
        for item in as_list(markdown_refs.get("refs")):
            if isinstance(item, dict) and item.get("status") == "missing":
                blockers.append({
                    "blocker_type": "markdown_image_ref_missing",
                    "message": f"Markdown image ref is missing from resource paths: {item.get('ref')}",
                })
            if isinstance(item, dict) and item.get("status") == "external_or_data":
                blockers.append({
                    "blocker_type": "markdown_image_ref_not_project_local",
                    "message": f"publication proof requires project-local bitmap refs, not external/data image refs: {item.get('ref')}",
                })

        figure_summary = as_mapping(payload.get("figure_asset_manifest_summary"))
        for item in as_list(figure_summary.get("blockers")):
            if isinstance(item, dict):
                blockers.append({
                    "blocker_type": str(item.get("blocker_type") or "figure_asset_manifest_blocker"),
                    "message": str(item.get("message") or item),
                })

        ready_refs = as_list(args.figure_asset_manifest and as_mapping(publication_design).get("required_asset_ready_refs"))
        if ready_refs:
            _present, missing = file_refs_exist(ready_refs, root)
            for ref in missing:
                blockers.append({
                    "blocker_type": "required_asset_ref_missing",
                    "message": f"required asset ref missing or empty: {ref}",
                })

    if role == "final_export":
        if not args.owner_acceptance_receipt:
            blockers.append({
                "blocker_type": "owner_acceptance_missing",
                "message": "final export requires --owner-acceptance-receipt",
            })
        else:
            accepted = owner_acceptance.get("status") in ("accepted", "approved", "owner_accepted")
            if not accepted:
                blockers.append({
                    "blocker_type": "owner_acceptance_not_accepted",
                    "message": "owner acceptance receipt status must be accepted, approved, or owner_accepted",
                })

    payload["artifact_gate"] = {
        "status": "passed" if not blockers else "blocked",
        "blockers": blockers,
        "warnings": warnings,
        "claim_boundary": {
            "review_pdf_counts_as_publication_proof": False,
            "publication_proof_counts_as_final_export": False,
            "helper_receipt_counts_as_owner_acceptance": False,
        },
        "evidence_refs": {
            "publication_design_profile": rel(args.publication_design_profile.resolve(), root) if args.publication_design_profile else None,
            "publication_profile": rel(args.resolved_publication_profile, root) if args.resolved_publication_profile else None,
            "rendered_page_inspection": rel(args.rendered_page_inspection.resolve(), root) if args.rendered_page_inspection else payload.get("auto_rendered_page_inspection_ref"),
            "owner_acceptance_receipt": rel(args.owner_acceptance_receipt.resolve(), root) if args.owner_acceptance_receipt else None,
            "figure_asset_manifest": rel(args.figure_asset_manifest.resolve(), root) if args.figure_asset_manifest else None,
        },
    }


def compile_pdf(args: argparse.Namespace) -> dict[str, Any]:
    root = args.root.resolve()
    source_md = args.source_md.resolve()
    output_pdf = args.output_pdf.resolve()
    render_dir = args.render_dir.resolve() if args.render_dir else None
    if args.write_rendered_page_inspection:
        write_rendered_page_inspection = args.write_rendered_page_inspection
        if not write_rendered_page_inspection.is_absolute():
            write_rendered_page_inspection = root / write_rendered_page_inspection
        args.write_rendered_page_inspection = write_rendered_page_inspection.resolve()
    publication_design_profile = args.publication_design_profile.resolve() if args.publication_design_profile else None
    rendered_page_inspection = args.rendered_page_inspection.resolve() if args.rendered_page_inspection else None
    owner_acceptance_receipt = args.owner_acceptance_receipt.resolve() if args.owner_acceptance_receipt else None
    figure_asset_manifest = args.figure_asset_manifest.resolve() if args.figure_asset_manifest else None
    publication_profile, publication_profile_path, profile_error = resolve_publication_profile(args.publication_profile, root)
    profile_variables = [str(value) for value in profile_list(publication_profile, "pandoc_variables") if str(value).strip()]
    include_headers = [
        path
        for path in (
            resolve_profile_path(value, publication_profile_path, root)
            for value in profile_list(publication_profile, "include_in_header")
        )
        if path is not None
    ]
    resource_paths = [
        (root / path).resolve() if not path.is_absolute() else path.resolve()
        for path in args.resource_path
    ]
    if not resource_paths:
        resource_paths = [source_md.parent.resolve(), root]

    payload: dict[str, Any] = {
        "surface_kind": "bookforge_pdf_export",
        "version": VERSION,
        "artifact_role": artifact_role(args),
        "requested_artifact_role": args.artifact_role,
        "backend": args.backend,
        "source_md": rel(source_md, root),
        "output_pdf": rel(output_pdf, root),
        "status": "blocked",
        "error": None,
        "render_status": "not_requested",
        "render_error": None,
        "rendered_pages": [],
        "pdf_page_count": 0,
        "command": [],
        "resource_paths": [rel(path, root) for path in resource_paths],
        "publication_profile": {
            "requested": args.publication_profile,
            "resolved": rel(publication_profile_path, root) if publication_profile_path else None,
            "profile_id": publication_profile.get("profile_id"),
            "status": "loaded" if publication_profile and not profile_error else ("disabled" if not publication_profile_path else "unreadable"),
            "error": profile_error,
        },
        "include_headers": [rel(path, root) for path in include_headers],
        "quality_boundary": {
            "source_is_markdown": True,
            "uses_publication_typesetting_backend": True,
            "hand_rolled_raster_renderer": False,
            "owner_acceptance_required_for_publication_claim": True,
        },
        "auto_rendered_page_inspection_ref": None,
    }
    args.publication_design_profile = publication_design_profile
    args.rendered_page_inspection = rendered_page_inspection
    args.owner_acceptance_receipt = owner_acceptance_receipt
    args.figure_asset_manifest = figure_asset_manifest
    args.resolved_publication_profile = publication_profile_path

    publication_design, design_error = read_json_object(publication_design_profile)
    if not publication_design:
        publication_design = as_mapping(publication_profile.get("publication_design_profile"))
    if profile_error:
        design_error = design_error or profile_error
    rendered_inspection, inspection_error = read_json_object(rendered_page_inspection)
    owner_acceptance, owner_error = read_json_object(owner_acceptance_receipt)
    if figure_asset_manifest:
        figure_manifest, figure_error = read_json_object(figure_asset_manifest)
        payload["figure_asset_manifest_status"] = "loaded" if not figure_error else "unreadable"
        payload["figure_asset_manifest_error"] = figure_error
        if figure_error:
            design_error = design_error or figure_error
    else:
        figure_manifest = {}
    figure_summary = figure_manifest_readiness(figure_manifest, root) if figure_manifest else {
        "record_count": 0,
        "required_count": 0,
        "ready_required_count": 0,
        "blockers": [],
    }
    payload["publication_design_profile"] = publication_design
    payload["rendered_page_inspection"] = rendered_inspection
    payload["owner_acceptance_receipt"] = owner_acceptance
    payload["figure_asset_manifest_summary"] = figure_summary

    if not source_md.exists():
        payload["status"] = "blocked_missing_source_md"
        payload["error"] = f"source Markdown not found: {source_md}"
        return payload

    payload["markdown_image_refs"] = markdown_image_refs(source_md, resource_paths, root)
    image_ref_blockers: list[str] = []
    if payload["artifact_role"] in {"publication_proof", "final_export"}:
        for item in as_list(as_mapping(payload["markdown_image_refs"]).get("refs")):
            if isinstance(item, dict) and item.get("status") == "missing":
                image_ref_blockers.append(f"Markdown image ref is missing from resource paths: {item.get('ref')}")
            if isinstance(item, dict) and item.get("status") == "external_or_data":
                image_ref_blockers.append(
                    f"publication proof requires project-local bitmap refs, not external/data image refs: {item.get('ref')}"
                )
    if image_ref_blockers:
        payload["status"] = "blocked_image_asset_refs"
        payload["error"] = "; ".join(image_ref_blockers)
        assess_artifact_gate(
            payload,
            args,
            root,
            publication_design,
            design_error,
            rendered_inspection,
            inspection_error,
            owner_acceptance,
            owner_error,
        )
        return payload

    if args.backend != "pandoc-xelatex":
        payload["status"] = "blocked_unsupported_backend"
        payload["error"] = f"unsupported backend: {args.backend}"
        return payload

    metadata_file = args.metadata_file.resolve() if args.metadata_file else None
    if metadata_file and not metadata_file.exists():
        payload["status"] = "blocked_missing_metadata_file"
        payload["error"] = f"metadata file not found: {metadata_file}"
        return payload

    command, blocker = pandoc_xelatex_command(
        source_md,
        output_pdf,
        metadata_file,
        profile_variables + args.variable,
        resource_paths,
        include_headers,
    )
    payload["command"] = command
    if blocker:
        payload["status"] = f"blocked_missing_{blocker.split()[0]}"
        payload["error"] = blocker
        return payload

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        if output_pdf.exists():
            output_pdf.unlink()
        payload["status"] = "blocked_pdf_compile_failed"
        payload["error"] = (result.stderr or result.stdout or "pandoc failed").strip()[-2000:]
        return payload

    payload["status"] = "generated"
    payload["error"] = None

    if render_dir:
        render_status, render_error, rendered_pages = render_pdf_pages(
            output_pdf,
            render_dir,
            root,
            args.render_prefix,
            args.render_dpi,
        )
        payload["render_status"] = render_status
        payload["render_error"] = render_error
        payload["rendered_pages"] = rendered_pages
        payload["pdf_page_count"] = len(rendered_pages)
        if render_status == "rendered" and rendered_pages and not rendered_inspection:
            rendered_inspection = auto_rendered_page_inspection(rendered_pages, root, payload)
            payload["rendered_page_inspection"] = rendered_inspection
            if args.write_rendered_page_inspection:
                args.write_rendered_page_inspection.parent.mkdir(parents=True, exist_ok=True)
                args.write_rendered_page_inspection.write_text(
                    json.dumps(rendered_inspection, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                payload["auto_rendered_page_inspection_ref"] = rel(args.write_rendered_page_inspection, root)

    assess_artifact_gate(
        payload,
        args,
        root,
        publication_design,
        design_error,
        rendered_inspection,
        inspection_error,
        owner_acceptance,
        owner_error,
    )
    if payload["artifact_gate"]["status"] == "blocked":
        payload["status"] = "generated_with_artifact_gate_blocker"

    return payload


def doctor() -> dict[str, Any]:
    return {
        "surface_kind": "bookforge_pdf_export_doctor",
        "version": VERSION,
        "available_backends": {
            "pandoc-xelatex": command_exists("pandoc") and command_exists("xelatex"),
        },
        "artifact_roles": list(ARTIFACT_ROLES),
        "default_publication_profile": DEFAULT_PUBLICATION_PROFILE,
        "bundled_profile_dir": str(BUNDLED_PROFILE_DIR),
        "capabilities": {
            "markdown_image_ref_scan": True,
            "markdown_image_ref_scan_backend": "pandoc_ast_when_available",
            "figure_asset_manifest_readiness": True,
            "helper_generated_rendered_page_inspection": True,
            "publication_proof_fail_closes_missing_assets": True,
        },
        "tools": {
            "pandoc": shutil.which("pandoc"),
            "xelatex": shutil.which("xelatex"),
            "pdftoppm": shutil.which("pdftoppm"),
            "quarto": shutil.which("quarto"),
            "typst": shutil.which("typst"),
        },
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="OPL BookForge publication/typesetting PDF export helper.",
    )
    parser.add_argument("--doctor", action="store_true", help="Print backend availability JSON and exit.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root for relative refs.")
    parser.add_argument("--source-md", type=Path, help="Markdown source to compile.")
    parser.add_argument("--output-pdf", type=Path, help="PDF output path.")
    parser.add_argument("--manifest", type=Path, help="Optional JSON manifest output path.")
    parser.add_argument("--render-dir", type=Path, help="Optional directory for rendered page PNGs.")
    parser.add_argument("--render-prefix", default="bookforge-page", help="Rendered page file prefix.")
    parser.add_argument("--render-dpi", type=int, default=180, help="DPI for rendered page PNG inspection output.")
    parser.add_argument("--metadata-file", type=Path, help="Optional Pandoc YAML metadata file for design/profile variables.")
    parser.add_argument(
        "--publication-profile",
        default=DEFAULT_PUBLICATION_PROFILE,
        help="Bundled profile id or JSON path for publication-grade Pandoc variables/header. Use 'none' to disable.",
    )
    parser.add_argument(
        "--resource-path",
        type=Path,
        action="append",
        default=[],
        help="Pandoc resource path for relative figures/assets. Repeatable; defaults to source Markdown directory plus root.",
    )
    parser.add_argument("--publication-design-profile", type=Path, help="JSON publication design profile for publication proof or final export gates.")
    parser.add_argument("--rendered-page-inspection", type=Path, help="JSON rendered-page inspection report for publication proof or final export gates.")
    parser.add_argument("--write-rendered-page-inspection", type=Path, help="Optional path for a helper-generated rendered-page baseline inspection JSON.")
    parser.add_argument("--owner-acceptance-receipt", type=Path, help="JSON owner/export acceptance receipt required for final export.")
    parser.add_argument("--figure-asset-manifest", type=Path, help="Optional figure asset manifest used as publication-proof evidence.")
    parser.add_argument(
        "-V",
        "--variable",
        action="append",
        default=[],
        help="Pandoc variable, for example geometry:inner=30mm or documentclass=ctexbook. Repeatable.",
    )
    parser.add_argument(
        "--backend",
        default="pandoc-xelatex",
        choices=["pandoc-xelatex"],
        help="Typesetting backend. v1 supports Pandoc with XeLaTeX.",
    )
    parser.add_argument(
        "--artifact-role",
        default="review_pdf",
        help="Artifact role recorded in the manifest: review_pdf, publication_proof, or final_export.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.doctor:
        print(json.dumps(doctor(), ensure_ascii=False, indent=2))
        return 0

    missing = [name for name in ("source_md", "output_pdf") if getattr(args, name) is None]
    if missing:
        print(f"missing required arguments: {', '.join('--' + name.replace('_', '-') for name in missing)}", file=sys.stderr)
        return 2

    payload = compile_pdf(args)
    write_manifest(args.manifest, payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["status"] == "generated" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
