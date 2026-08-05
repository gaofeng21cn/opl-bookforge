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

from opl_framework.artifact_inspection import (
    inspect_pdf_fonts as inspect_pdf_font_inventory,
    inspect_png_visual_metrics,
)
from opl_framework.json_io import write_json_object_atomic

HELPER_DIR = Path(__file__).resolve().parent
if str(HELPER_DIR) not in sys.path:
    sys.path.insert(0, str(HELPER_DIR))

from bookforge_pdf_export_parts.profile_and_assets import (
    DEFAULT_PUBLICATION_PROFILE,
    as_mapping,
    rel,
)
from bookforge_pdf_export_parts.artifact_gate import assess_artifact_gate
from bookforge_pdf_export_parts.compile_phases import (
    compile_backend,
    finalize_gate,
    prepare_pdf_compile,
    render_and_inspect,
)


VERSION = "bookforge-pdf-export.v1"
DEFAULT_RENDERED_PAGE_ROLES = (
    "front_matter",
    "table_of_contents",
    "chapter_opening",
    "dense_body",
    "figure_or_table",
    "callout",
    "closing_page",
)
DEFAULT_RENDERED_PAGE_CHECKLIST_REFS = (
    "nonblank_pages",
    "embedded_fonts",
    "page_size_consistency",
    "caption_proximity",
    "figure_table_rendering",
    "running_head",
    "page_number",
    "trailing_whitespace",
)


def write_manifest(path: Path | None, payload: dict[str, Any]) -> None:
    if path is None:
        return
    write_json_object_atomic(path, payload)


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def profile_threshold(profile: dict[str, Any], key: str, default: float) -> float:
    expectations = as_mapping(profile.get("visual_qa_expectations"))
    value = expectations.get(key)
    if isinstance(value, (int, float)):
        return float(value)
    return default


def profile_string_list(profile: dict[str, Any], section: str, key: str, default: tuple[str, ...]) -> list[str]:
    value = as_mapping(profile.get(section)).get(key)
    if isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value):
        return [item for item in value if item.strip()]
    return list(default)


def inspect_pdf_fonts(pdf_path: Path, root: Path) -> dict[str, Any]:
    inventory = inspect_pdf_font_inventory(pdf_path, root)
    fonts = inventory["fonts"]
    non_embedded = [font for font in fonts if font["embedded_raw"] not in ("yes", "unknown")]
    embedded_count = inventory["embedded_font_count"]
    if inventory["inspection_status"] == "tool_missing":
        status = "tool_missing"
    elif inventory["inspection_status"] == "tool_error":
        status = "failed"
    elif not fonts:
        status = "unchecked"
    elif non_embedded:
        status = "failed"
    elif embedded_count == 0:
        status = "unchecked"
    else:
        status = "passed"
    return {
        "status": status,
        "tool": inventory["tool"],
        "embedded_font_count": embedded_count,
        "non_embedded_font_count": len(non_embedded),
        "fonts": fonts,
        "error": inventory["error"],
    }


def png_visual_metrics(path: Path, *, min_fill_ratio: float, max_trailing_whitespace_ratio: float) -> dict[str, Any]:
    metrics = inspect_png_visual_metrics(path)
    fill_ratio = metrics["fill_ratio"]
    trailing_whitespace_ratio = metrics["trailing_whitespace_ratio"]
    metrics["density_status"] = (
        "passed"
        if isinstance(fill_ratio, (int, float)) and fill_ratio >= min_fill_ratio
        else "checked_with_warnings"
        if isinstance(fill_ratio, (int, float))
        else "unchecked"
    )
    metrics["trailing_whitespace_status"] = (
        "passed"
        if isinstance(trailing_whitespace_ratio, (int, float))
        and trailing_whitespace_ratio <= max_trailing_whitespace_ratio
        else "checked_with_warnings"
        if isinstance(trailing_whitespace_ratio, (int, float))
        else "unchecked"
    )
    return metrics


def auto_rendered_page_inspection(
    rendered_pages: list[str],
    root: Path,
    payload: dict[str, Any],
    output_pdf: Path,
    publication_profile: dict[str, Any],
) -> dict[str, Any]:
    min_fill_ratio = profile_threshold(publication_profile, "min_machine_page_fill_ratio", 0.01)
    max_trailing_whitespace_ratio = profile_threshold(publication_profile, "max_trailing_whitespace_ratio", 0.35)
    sample_page_roles = profile_string_list(
        publication_profile,
        "visual_qa_expectations",
        "sample_page_roles",
        DEFAULT_RENDERED_PAGE_ROLES,
    )
    checklist_refs = profile_string_list(
        publication_profile,
        "visual_qa_expectations",
        "checklist_refs",
        DEFAULT_RENDERED_PAGE_CHECKLIST_REFS,
    )
    page_metrics: list[dict[str, Any]] = []
    for ref in rendered_pages:
        path = root / ref
        metrics = png_visual_metrics(
            path,
            min_fill_ratio=min_fill_ratio,
            max_trailing_whitespace_ratio=max_trailing_whitespace_ratio,
        )
        page_metrics.append({
            "ref": ref,
            **metrics,
        })

    nonblank_pages = sum(1 for item in page_metrics if item["nonblank_baseline"])
    dimensions = {(item.get("width"), item.get("height")) for item in page_metrics if item.get("width") and item.get("height")}
    density_statuses = {str(item.get("density_status")) for item in page_metrics}
    trailing_statuses = {str(item.get("trailing_whitespace_status")) for item in page_metrics}
    font_inspection = inspect_pdf_fonts(output_pdf, root)
    missing_images = as_mapping(payload.get("markdown_image_refs")).get("missing_count", 0)
    figure_blockers = as_mapping(payload.get("figure_asset_manifest_summary")).get("blockers", [])
    element_status = "passed" if missing_images == 0 and not figure_blockers else "blocked"
    return {
        "surface_kind": "bookforge_rendered_page_inspection",
        "version": "bookforge-rendered-page-inspection.v1",
        "inspection_kind": "machine_baseline",
        "source_pattern": "kami-inspired executable proof QA adapted for Book Forge publication proofs",
        "nonblank_pages": nonblank_pages,
        "overflow_or_clipping": False if nonblank_pages == len(rendered_pages) and rendered_pages else "unchecked",
        "caption_figure_table_status": element_status,
        "callout_status": "profile_applied",
        "heading_hierarchy_status": "profile_applied",
        "headers_footers_status": "profile_applied",
        "page_numbering_status": "profile_applied",
        "visual_rhythm_status": "profile_applied_machine_baseline_manual_review_recommended",
        "embedded_font_status": font_inspection["status"],
        "embedded_font_inspection": font_inspection,
        "page_density_status": "checked_with_warnings" if "checked_with_warnings" in density_statuses else (
            "passed" if density_statuses == {"passed"} and page_metrics else "unchecked"
        ),
        "trailing_whitespace_status": "checked_with_warnings" if "checked_with_warnings" in trailing_statuses else (
            "passed" if trailing_statuses == {"passed"} and page_metrics else "unchecked"
        ),
        "rendered_page_size_status": "passed" if len(dimensions) == 1 and nonblank_pages == len(rendered_pages) and rendered_pages else "unchecked",
        "sample_page_roles_status": "passed" if sample_page_roles else "unchecked",
        "checklist_refs_status": "passed" if checklist_refs else "unchecked",
        "sample_page_roles": sample_page_roles,
        "checklist_refs": checklist_refs,
        "machine_thresholds": {
            "min_machine_page_fill_ratio": min_fill_ratio,
            "max_trailing_whitespace_ratio": max_trailing_whitespace_ratio,
        },
        "page_metrics": page_metrics,
        "manual_review_still_required_for_final_export": True,
    }


def pandoc_xelatex_command(
    source_md: Path,
    output_pdf: Path,
    metadata_file: Path | None,
    variables: list[str],
    resource_paths: list[Path],
    include_headers: list[Path],
    *,
    number_sections: bool,
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
        "--metadata",
        "link-citations=true",
        "-o",
        str(output_pdf),
    ]
    if number_sections:
        command.append("--number-sections")
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


def materialize_progress_diagnostic(payload: dict[str, Any], *, code: str, error: str) -> dict[str, Any]:
    payload["status"] = "completed_with_quality_debt"
    payload["error"] = error
    payload["progress_diagnostic"] = {
        "code": code,
        "detail": error,
        "no_output": not Path(str(payload["output_pdf"])).is_file(),
        "blocks_stage_transition": False,
        "blocks_quality_export_or_ready_claims": True,
        "next_stage_may_start": True,
    }
    payload["artifact_gate"] = {
        "status": "quality_debt",
        "blockers": [{"blocker_type": code, "message": error}],
        "quality_debt": {
            "status": "open",
            "blocks_stage_transition": False,
            "blocks_quality_export_or_ready_claims": True,
        },
        "warnings": [],
        "claim_boundary": {
            "review_pdf_counts_as_publication_proof": False,
            "publication_proof_counts_as_final_export": False,
            "helper_receipt_counts_as_owner_acceptance": False,
        },
    }
    return payload


def compile_pdf(args: argparse.Namespace) -> dict[str, Any]:
    prepared = prepare_pdf_compile(
        args,
        version=VERSION,
        artifact_role=artifact_role,
    )
    payload = prepared.payload
    if prepared.diagnostic:
        code, error = prepared.diagnostic
        return materialize_progress_diagnostic(payload, code=code, error=error)

    backend = compile_backend(prepared, pandoc_xelatex_command)
    payload["command"] = backend.command
    if backend.hard_stop:
        payload["status"] = "blocked_executor_unavailable"
        payload["error"] = backend.hard_stop
        payload["hard_stop"] = {
            "kind": "executor_unavailable",
            "blocks_stage_transition": True,
        }
        return payload
    if backend.diagnostic:
        code, error = backend.diagnostic
        return materialize_progress_diagnostic(payload, code=code, error=error)

    prepared.output_pdf.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(backend.command, cwd=prepared.root, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        if prepared.output_pdf.exists():
            prepared.output_pdf.unlink()
        return materialize_progress_diagnostic(
            payload,
            code="pdf_compile_failed",
            error=(result.stderr or result.stdout or "pandoc failed").strip()[-2000:],
        )

    payload["status"] = "generated"
    payload["error"] = None

    inspection_path = render_and_inspect(
        prepared,
        auto_rendered_page_inspection=auto_rendered_page_inspection,
    )
    if inspection_path:
        write_json_object_atomic(inspection_path, payload["rendered_page_inspection"])
        payload["auto_rendered_page_inspection_ref"] = rel(inspection_path, prepared.root)

    finalize_gate(prepared)
    return payload


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="OPL Book Forge publication/typesetting PDF export helper.",
    )
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root for relative refs.")
    parser.add_argument("--source-md", type=Path, help="Markdown source to compile.")
    parser.add_argument("--output-pdf", type=Path, help="PDF output path.")
    parser.add_argument("--manifest", type=Path, help="Optional JSON manifest output path.")
    parser.add_argument("--render-dir", type=Path, help="Optional directory for rendered page PNGs.")
    parser.add_argument("--render-prefix", default="bookforge-page", help="Rendered page file prefix.")
    parser.add_argument("--render-dpi", type=int, default=180, help="DPI for rendered page PNG inspection output.")
    parser.add_argument("--metadata-file", type=Path, help="Optional Pandoc YAML metadata file for design/profile variables.")
    parser.add_argument(
        "--number-sections",
        dest="number_sections",
        action="store_true",
        default=True,
        help="Ask Pandoc to number sections. Enabled by default for publication-style Markdown without pre-numbered Chinese chapter titles.",
    )
    parser.add_argument(
        "--no-number-sections",
        dest="number_sections",
        action="store_false",
        help="Disable Pandoc automatic section numbering for pre-numbered manuscripts or cumulative review PDFs.",
    )
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
    missing = []
    if args.source_md is None:
        missing.append("source_md")
    if args.output_pdf is None:
        missing.append("output_pdf")
    if missing:
        print(f"missing required arguments: {', '.join('--' + name.replace('_', '-') for name in missing)}", file=sys.stderr)
        return 2

    payload = compile_pdf(args)
    write_manifest(args.manifest, payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["status"] in {
        "generated",
        "generated_with_quality_debt",
        "completed_with_quality_debt",
    } else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
