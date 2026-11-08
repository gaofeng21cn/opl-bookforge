from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from bookforge_pdf_export_parts.profile_and_assets import (
    as_list,
    as_mapping,
    file_refs_exist,
    rel,
)


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
    "embedded_font_status",
    "page_density_status",
    "trailing_whitespace_status",
    "rendered_page_size_status",
    "sample_page_roles_status",
    "checklist_refs_status",
)
BLOCKING_PROOF_QA_STATUSES = {
    "blocked",
    "error",
    "failed",
    "missing",
    "tool_missing",
    "unavailable",
    "unchecked",
}


def missing_fields(section: dict[str, Any], fields: tuple[str, ...]) -> list[str]:
    return [field for field in fields if section.get(field) in (None, "", [], {})]


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
                "message": "publication proof requires a publication design profile or Book Forge publication profile",
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
            for field in (
                "embedded_font_status",
                "page_density_status",
                "trailing_whitespace_status",
                "rendered_page_size_status",
                "sample_page_roles_status",
                "checklist_refs_status",
            ):
                status = str(rendered_inspection.get(field) or "missing")
                if status in BLOCKING_PROOF_QA_STATUSES:
                    blockers.append({
                        "blocker_type": f"rendered_page_{field}_not_passed",
                        "message": f"publication proof requires {field}; got {status}",
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
        "status": "passed" if not blockers else "quality_debt",
        "blockers": blockers,
        "quality_debt": {
            "status": "none" if not blockers else "open",
            "blocks_stage_transition": False,
            "blocks_quality_export_or_ready_claims": bool(blockers),
        },
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
