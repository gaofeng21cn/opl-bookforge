from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from bookforge_pdf_export_parts.artifact_gate import assess_artifact_gate
from bookforge_pdf_export_parts.profile_and_assets import (
    as_mapping,
    figure_manifest_readiness,
    image_refs_from_pandoc_document,
    markdown_image_refs,
    profile_list,
    read_json_object,
    rel,
    resolve_profile_path,
    resolve_publication_profile,
)


@dataclass
class PdfCompilePreparation:
    args: argparse.Namespace
    root: Path
    source_md: Path
    output_pdf: Path
    render_dir: Path | None
    publication_profile: dict[str, Any]
    profile_variables: list[str]
    include_headers: list[Path]
    resource_paths: list[Path]
    publication_design: dict[str, Any]
    design_error: str | None
    rendered_inspection: dict[str, Any]
    inspection_error: str | None
    owner_acceptance: dict[str, Any]
    owner_error: str | None
    payload: dict[str, Any]
    diagnostic: tuple[str, str] | None = None


@dataclass
class BackendCompile:
    command: list[str]
    blocker: str | None = None
    diagnostic: tuple[str, str] | None = None
    hard_stop: str | None = None


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


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
        document = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
    return image_refs_from_pandoc_document(document)


def prepare_pdf_compile(
    args: argparse.Namespace,
    *,
    version: str,
    artifact_role: Callable[[argparse.Namespace], str],
) -> PdfCompilePreparation:
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
        "version": version,
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

    diagnostic = None
    if not source_md.exists():
        diagnostic = (
            "source_markdown_missing",
            f"source Markdown not found: {source_md}",
        )
    else:
        pandoc_image_refs = image_refs_from_pandoc_ast(source_md, root)
        payload["markdown_image_refs"] = markdown_image_refs(
            source_md,
            resource_paths,
            root,
            extracted_refs=pandoc_image_refs,
            extraction_method="pandoc_ast" if pandoc_image_refs is not None else None,
        )
        if args.backend != "pandoc-xelatex":
            diagnostic = (
                "unsupported_backend",
                f"unsupported backend: {args.backend}",
            )

    return PdfCompilePreparation(
        args=args,
        root=root,
        source_md=source_md,
        output_pdf=output_pdf,
        render_dir=render_dir,
        publication_profile=publication_profile,
        profile_variables=profile_variables,
        include_headers=include_headers,
        resource_paths=resource_paths,
        publication_design=publication_design,
        design_error=design_error,
        rendered_inspection=rendered_inspection,
        inspection_error=inspection_error,
        owner_acceptance=owner_acceptance,
        owner_error=owner_error,
        payload=payload,
        diagnostic=diagnostic,
    )


def compile_backend(
    prepared: PdfCompilePreparation,
    command_builder: Callable[..., tuple[list[str], str | None]],
) -> BackendCompile:
    args = prepared.args
    metadata_file = args.metadata_file.resolve() if args.metadata_file else None
    if metadata_file and not metadata_file.exists():
        return BackendCompile(
            command=[],
            diagnostic=(
                "metadata_file_missing",
                f"metadata file not found: {metadata_file}",
            ),
        )

    command, blocker = command_builder(
        prepared.source_md,
        prepared.output_pdf,
        metadata_file,
        prepared.profile_variables + args.variable,
        prepared.resource_paths,
        prepared.include_headers,
        number_sections=args.number_sections,
    )
    if blocker:
        if blocker in {"pandoc not found", "xelatex not found"}:
            return BackendCompile(command=command, blocker=blocker, hard_stop=blocker)
        return BackendCompile(
            command=command,
            blocker=blocker,
            diagnostic=("publication_backend_input_missing", blocker),
        )
    return BackendCompile(command=command)


def render_and_inspect(
    prepared: PdfCompilePreparation,
    *,
    auto_rendered_page_inspection: Callable[..., dict[str, Any]],
) -> Path | None:
    if not prepared.render_dir:
        return None

    payload = prepared.payload
    args = prepared.args
    render_status, render_error, rendered_pages = render_pdf_pages(
        prepared.output_pdf,
        prepared.render_dir,
        prepared.root,
        args.render_prefix,
        args.render_dpi,
    )
    payload["render_status"] = render_status
    payload["render_error"] = render_error
    payload["rendered_pages"] = rendered_pages
    payload["pdf_page_count"] = len(rendered_pages)
    if render_status == "rendered" and rendered_pages and not prepared.rendered_inspection:
        rendered_inspection = auto_rendered_page_inspection(
            rendered_pages,
            prepared.root,
            payload,
            prepared.output_pdf,
            prepared.publication_profile,
        )
        prepared.rendered_inspection = rendered_inspection
        payload["rendered_page_inspection"] = rendered_inspection
        if args.write_rendered_page_inspection:
            return args.write_rendered_page_inspection
    return None


def render_pdf_pages(
    pdf_path: Path,
    render_dir: Path,
    root: Path,
    prefix: str,
    dpi: int,
) -> tuple[str, str | None, list[str]]:
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

    rendered_pages = [
        rel(path, root)
        for path in sorted(render_dir.glob(f"{prefix}-*.png"))
    ]
    return "rendered", None, rendered_pages


def finalize_gate(prepared: PdfCompilePreparation) -> None:
    assess_artifact_gate(
        prepared.payload,
        prepared.args,
        prepared.root,
        prepared.publication_design,
        prepared.design_error,
        prepared.rendered_inspection,
        prepared.inspection_error,
        prepared.owner_acceptance,
        prepared.owner_error,
    )
    if prepared.payload["artifact_gate"]["status"] == "quality_debt":
        prepared.payload["status"] = "generated_with_quality_debt"
