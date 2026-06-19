#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


VERSION = "bookforge-pdf-export.v1"
ARTIFACT_ROLES = ("review_pdf", "publication_proof", "final_export")
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


def render_pdf_pages(pdf_path: Path, render_dir: Path, root: Path, prefix: str) -> tuple[str, str | None, list[str]]:
    if not command_exists("pdftoppm"):
        return "skipped_missing_pdftoppm", "pdftoppm not found", []

    render_dir.mkdir(parents=True, exist_ok=True)
    for old_page in render_dir.glob(f"{prefix}-*.png"):
        old_page.unlink()

    page_prefix = render_dir / prefix
    result = subprocess.run(
        ["pdftoppm", "-png", str(pdf_path), str(page_prefix)],
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
    elif role in {"publication_proof", "final_export"}:
        if not args.publication_design_profile:
            blockers.append({
                "blocker_type": "publication_design_profile_missing",
                "message": "publication proof requires --publication-design-profile",
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

        if not args.rendered_page_inspection:
            blockers.append({
                "blocker_type": "rendered_page_inspection_missing",
                "message": "publication proof requires --rendered-page-inspection",
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
            "rendered_page_inspection": rel(args.rendered_page_inspection.resolve(), root) if args.rendered_page_inspection else None,
            "owner_acceptance_receipt": rel(args.owner_acceptance_receipt.resolve(), root) if args.owner_acceptance_receipt else None,
            "figure_asset_manifest": rel(args.figure_asset_manifest.resolve(), root) if args.figure_asset_manifest else None,
        },
    }


def compile_pdf(args: argparse.Namespace) -> dict[str, Any]:
    root = args.root.resolve()
    source_md = args.source_md.resolve()
    output_pdf = args.output_pdf.resolve()
    render_dir = args.render_dir.resolve() if args.render_dir else None
    publication_design_profile = args.publication_design_profile.resolve() if args.publication_design_profile else None
    rendered_page_inspection = args.rendered_page_inspection.resolve() if args.rendered_page_inspection else None
    owner_acceptance_receipt = args.owner_acceptance_receipt.resolve() if args.owner_acceptance_receipt else None
    figure_asset_manifest = args.figure_asset_manifest.resolve() if args.figure_asset_manifest else None
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
        "quality_boundary": {
            "source_is_markdown": True,
            "uses_publication_typesetting_backend": True,
            "hand_rolled_raster_renderer": False,
            "owner_acceptance_required_for_publication_claim": True,
        },
    }
    args.publication_design_profile = publication_design_profile
    args.rendered_page_inspection = rendered_page_inspection
    args.owner_acceptance_receipt = owner_acceptance_receipt
    args.figure_asset_manifest = figure_asset_manifest

    publication_design, design_error = read_json_object(publication_design_profile)
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
    payload["publication_design_profile"] = publication_design
    payload["rendered_page_inspection"] = rendered_inspection
    payload["owner_acceptance_receipt"] = owner_acceptance
    payload["figure_asset_manifest_summary"] = {
        "record_count": len(as_list(figure_manifest.get("figures")) or as_list(figure_manifest.get("assets"))),
    }

    if not source_md.exists():
        payload["status"] = "blocked_missing_source_md"
        payload["error"] = f"source Markdown not found: {source_md}"
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

    command, blocker = pandoc_xelatex_command(source_md, output_pdf, metadata_file, args.variable, resource_paths)
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
        )
        payload["render_status"] = render_status
        payload["render_error"] = render_error
        payload["rendered_pages"] = rendered_pages
        payload["pdf_page_count"] = len(rendered_pages)

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
    parser.add_argument("--metadata-file", type=Path, help="Optional Pandoc YAML metadata file for design/profile variables.")
    parser.add_argument(
        "--resource-path",
        type=Path,
        action="append",
        default=[],
        help="Pandoc resource path for relative figures/assets. Repeatable; defaults to source Markdown directory plus root.",
    )
    parser.add_argument("--publication-design-profile", type=Path, help="JSON publication design profile for publication proof or final export gates.")
    parser.add_argument("--rendered-page-inspection", type=Path, help="JSON rendered-page inspection report for publication proof or final export gates.")
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
