#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_CLOSEOUT_REFS = {
    "owner_receipt_ref",
    "typed_blocker_ref",
    "human_gate_ref",
    "route_back_ref",
}

COMPLETION_ACCOUNTS = {
    "review_pdf",
    "publication_proof",
    "final_export",
    "owner_acceptance",
}

FALSE_COMPLETION_ACCOUNTS = {
    "provider_attempt_completion",
    "generated_surface_ready",
    "stage_run_status_ready",
}

FUNCTIONAL_CLOSURE_GATES = {
    "standard_scaffold_interface",
    "golden_path_default_route",
    "revision_entrypoint_route",
    "pdf_proof_helper_plumbing",
    "artifact_lifecycle_handoff",
    "default_caller_structural_gate",
    "private_platform_retirement_matrix",
    "evidence_package_navigation",
}

FUNCTIONAL_CLOSURE_LATER_EVIDENCE_LANES = {
    "real_long_book_run_evidence",
    "publication_proof_visual_acceptance",
    "final_export_owner_acceptance",
    "direct_runtime_cli_or_hosted_artifact_handoff_parity",
    "workspace_artifact_lifecycle_apply_receipt",
    "physical_delete_authorization",
}

BOOKFORGE_EXPOSED_DOMAIN_SURFACES = {
    "book_domain_action_contract_ref",
    "chapter_task_card_ref",
    "manuscript_authority_ref",
    "style_authority_ref",
    "artifact_authority_ref",
    "owner_gated_publication_decision_ref",
    "owner_gated_export_decision_ref",
    "typed_blocker_ref",
    "owner_receipt_ref",
}

FORBIDDEN_RUNTIME_SURFACE_EXPORTS = {
    "private_temporal_wrapper",
    "private_stage_run_wrapper",
    "private_scheduler",
    "private_queue",
    "private_session_store",
    "private_provider_completion_store",
    "private_attempt_ledger",
    "runtime_status_read_model",
}

LIVE_STAGE_RUN_PROGRESS_ACCEPTED_STATUSES = {
    "owner_evidence_recorded_not_ready_claim",
    "owner_typed_blocker_recorded_not_ready_claim",
    "owner_evidence_required",
}

LIVE_STAGE_RUN_PROGRESS_REF_FIELDS = {
    "typed_blocker_refs",
    "quality_or_export_receipt_refs",
    "no_regression_refs",
    "doc_refs",
    "next_verification_command_refs",
}

LIVE_STAGE_RUN_PROGRESS_FORBIDDEN_CLAIMS = {
    "live_domain_progress_complete",
    "domain_ready",
    "production_ready",
    "quality_or_export_ready",
    "final_export_ready",
    "owner_acceptance",
    "owner_receipt_signed_by_opl",
    "typed_blocker_created_by_opl",
}

PRODUCTION_ACCEPTANCE_FORBIDDEN_CLAIMS = {
    "domain_ready",
    "production_ready",
    "quality_or_export_ready",
    "final_export_ready",
    "owner_acceptance",
    "owner_receipt_signed_by_opl",
    "typed_blocker_created_by_opl",
}

DEFAULT_ENTRY_ACCEPTED_RETURN_SHAPES = {
    "owner_receipt_ref",
    "typed_blocker_ref",
    "human_gate_ref",
    "route_back_ref",
}

REVISION_ENTRY_ACCEPTED_RETURN_SHAPES = {
    "route_back_ref",
    "repair_plan_ref",
    "typed_blocker_ref",
    "owner_decision_ref",
}

LEDGER_REGISTERED_FIELD_KINDS = {
    "ref",
    "hash",
    "index_ref",
    "review_ref",
    "receipt_ref",
}

LEDGER_REGISTRATION_ARTIFACT_CLASSES = {
    "storyline_package",
    "chapter_task_card",
    "manuscript_package",
    "figure_table_asset_index",
    "review_pdf",
    "publication_proof",
    "final_export_handoff",
}

LEDGER_FORBIDDEN_REGISTRATION_FIELDS = {
    "manuscript_body",
    "artifact_body",
    "body_text",
    "chapter_body",
    "memory_body",
    "owner_receipt_body",
    "typed_blocker_body",
    "runtime_queue_ref",
    "provider_attempt_ref",
    "publication_verdict",
    "quality_verdict",
    "owner_authority_verdict",
    "final_export_authority_verdict",
}

PRIVATE_PLATFORM_RETIREMENT_SURFACES = {
    "publication_and_export_helper",
    "image_asset_helper",
    "project_hygiene_helper",
    "runtime_session_update_absence",
}

PRIVATE_PLATFORM_NATIVE_HELPER_MODULES = {
    "opl-bookforge.publication-and-export-helper",
    "opl-bookforge.image-asset-helper",
    "opl-bookforge.project-hygiene-helper",
}

PRIVATE_PLATFORM_FORBIDDEN_READY_CLAIMS = {
    "counts_as_owner_acceptance",
    "counts_as_domain_ready",
    "counts_as_publication_ready",
    "counts_as_final_export_ready",
    "authorizes_physical_delete",
}

NATIVE_HELPER_PROBE_DESCRIPTORS = {
    "runtime/native_helpers/bookforge_pdf_export.native-helper-probe.json": {
        "helper_id": "opl-bookforge.pdf-export",
        "entrypoint_ref": "bookforge_pdf_export.py",
        "required_commands": ["pandoc", "xelatex", "pdftoppm", "pdffonts"],
    },
    "runtime/native_helpers/bookforge_imagegen_asset.native-helper-probe.json": {
        "helper_id": "opl-bookforge.imagegen-asset",
        "entrypoint_ref": "bookforge_imagegen_asset.py",
        "required_commands": ["codex-canonical"],
    },
}

NATIVE_HELPER_PROBE_AUTHORITY_FIELDS = {
    "can_write_domain_truth",
    "can_mutate_artifact_body",
    "can_sign_owner_receipt",
    "can_create_typed_blocker",
    "can_authorize_quality_verdict",
    "can_authorize_export_readiness",
    "can_claim_domain_ready",
    "can_claim_production_ready",
}

STANDARD_CAPABILITY_KINDS = {
    "stage_prompt",
    "stage_projection",
    "runtime_projection",
    "primary_skill",
    "professional_skill",
    "tool_connector",
    "reference_pack",
    "contract_module",
}

LEGACY_PROFESSIONAL_SKILL_REDIRECTS = {
    "legacy-professional-skill:bookforge-story-architect": (
        "agent/professional_skills/bookforge-story-style-architect/SKILL.md"
    ),
    "legacy-professional-skill:bookforge-reader-style-designer": (
        "agent/professional_skills/bookforge-story-style-architect/SKILL.md"
    ),
    "legacy-professional-skill:bookforge-style-editor": (
        "agent/professional_skills/bookforge-story-style-architect/SKILL.md"
    ),
    "legacy-professional-skill:bookforge-reference-absorber": (
        "agent/professional_skills/bookforge-source-reference-reviewer/SKILL.md"
    ),
    "legacy-professional-skill:bookforge-source-claim-reviewer": (
        "agent/professional_skills/bookforge-source-reference-reviewer/SKILL.md"
    ),
    "legacy-professional-skill:bookforge-book-memory-curator": (
        "agent/professional_skills/bookforge-publication-memory-curator/SKILL.md"
    ),
    "legacy-professional-skill:bookforge-publication-designer": (
        "agent/professional_skills/bookforge-publication-memory-curator/SKILL.md"
    ),
}


def load_json(repo: Path, ref: str) -> dict[str, Any]:
    return json.loads((repo / ref).read_text(encoding="utf-8"))


def assert_false(payload: dict[str, Any], path: str) -> None:
    current: Any = payload
    for part in path.split("."):
        current = current[part]
    assert current is False, f"{path} expected false, got {current!r}"


def assert_true(payload: dict[str, Any], path: str) -> None:
    current: Any = payload
    for part in path.split("."):
        current = current[part]
    assert current is True, f"{path} expected true, got {current!r}"


def assert_closeout_refs(fields: list[str] | tuple[str, ...], label: str) -> None:
    actual = set(fields)
    assert REQUIRED_CLOSEOUT_REFS <= actual, f"{label} missing closeout refs: {REQUIRED_CLOSEOUT_REFS - actual}"
    forbidden = {"provider_completion_ref", "temporal_workflow_completion_ref", "generated_surface_ready_ref"}
    assert not (actual & forbidden), f"{label} includes false-ready closeout refs: {actual & forbidden}"


def assert_ref_fields(fields: list[str] | tuple[str, ...], expected: set[str], label: str) -> None:
    actual = set(fields)
    assert expected <= actual, f"{label} missing required refs: {expected - actual}"


def assert_false_completion_account(account: dict[str, Any], label: str) -> None:
    for field in (
        "counts_as_bookforge_domain_completion",
        "counts_as_review_pdf_ready",
        "counts_as_publication_proof_ready",
        "counts_as_final_export_ready",
        "counts_as_owner_acceptance",
    ):
        assert account[field] is False, f"{label}.{field} expected false"


def assert_surface_export_boundary(payload: dict[str, Any], label: str) -> None:
    assert set(payload["bookforge_exposed_domain_surfaces"]) == BOOKFORGE_EXPOSED_DOMAIN_SURFACES, label
    assert set(payload["forbidden_runtime_surface_exports"]) == FORBIDDEN_RUNTIME_SURFACE_EXPORTS, label


def assert_functional_closure_gate(payload: dict[str, Any]) -> None:
    assert payload["gate_id"] == "bookforge_non_live_functional_closure_gate"
    assert payload["gate_role"] == "non_live_structural_closure_for_standard_default_path"
    assert payload["state"] == "functional_structure_gate_landed_not_publication_or_owner_acceptance"
    gate_refs = payload["required_non_live_gate_refs"]
    assert {entry["gate"] for entry in gate_refs} == FUNCTIONAL_CLOSURE_GATES
    refs_by_gate = {entry["gate"]: entry for entry in gate_refs}
    assert refs_by_gate["standard_scaffold_interface"]["contract_ref"] == "contracts/domain_descriptor.json"
    assert_ref_fields(
        refs_by_gate["standard_scaffold_interface"]["validator_refs"],
        {
            "opl agents scaffold --validate <repo-dir> --json",
            "opl agents interfaces --repo-dir <repo-dir> --json",
        },
        "standard scaffold/interface validator refs",
    )
    assert refs_by_gate["golden_path_default_route"]["contract_ref"] == "contracts/golden_path_profile.json"
    assert refs_by_gate["revision_entrypoint_route"]["contract_ref"] == "agent/skills/revision-entrypoint-router.md"
    assert refs_by_gate["revision_entrypoint_route"]["support_ref"] == "docs/references/opl-base-revision-routing-handoff.md"
    assert refs_by_gate["pdf_proof_helper_plumbing"]["contract_ref"] == "runtime/native_helpers/bookforge_pdf_export.py"
    assert (
        "opl pack native-helper probe --descriptor runtime/native_helpers/bookforge_pdf_export.native-helper-probe.json --json"
        in refs_by_gate["pdf_proof_helper_plumbing"]["validator_refs"]
    )
    assert refs_by_gate["artifact_lifecycle_handoff"]["contract_ref"] == "contracts/artifact_lifecycle_handoff.json"
    assert refs_by_gate["default_caller_structural_gate"]["contract_ref"] == "contracts/functional_privatization_audit.json"
    assert (
        refs_by_gate["private_platform_retirement_matrix"]["contract_ref"]
        == "contracts/functional_privatization_audit.json#bookforge_private_platform_retirement_matrix"
    )
    assert (
        refs_by_gate["private_platform_retirement_matrix"]["support_ref"]
        == "contracts/generated_surface_handoff.json#private_platform_retirement_projection"
    )
    assert refs_by_gate["evidence_package_navigation"]["contract_ref"] == "docs/evidence/README.md"
    assert refs_by_gate["evidence_package_navigation"]["claim_boundary"] == "historical_evidence_index_only_not_active_truth"

    assertions = payload["default_path_assertions"]
    assert assertions["default_cli_app_skill_path_must_route_via_opl_generated_or_hosted_surfaces"] is True
    assert assertions["stage_run_and_generated_surface_status_are_transport_or_projection_only"] is True
    assert assertions["bookforge_owner_answer_shape_required_for_domain_completion"] is True
    assert_closeout_refs(assertions["owner_answer_shapes"], "functional closure owner answer shapes")
    assert assertions["no_private_runtime_wrapper_or_default_caller_second_truth"] is True

    assert set(payload["later_evidence_lanes"]) == FUNCTIONAL_CLOSURE_LATER_EVIDENCE_LANES
    for field, value in payload["forbidden_claims"].items():
        assert value is False, f"functional_closure_gate.forbidden_claims.{field} expected false"


def assert_default_entry_routing(payload: dict[str, Any]) -> None:
    assert payload["routing_id"] == "bookforge_stage_run_owner_boundary_default_entry"
    assert payload["entry_owner"] == "one-person-lab"
    assert payload["stage_run_account_owner"] == "one-person-lab"
    assert payload["domain_owner"] == "OPL Book Forge"
    assert payload["default_entry_surface_kind"] == "opl_stage_run_attempt_request"
    assert payload["default_read_surface"] == "stage_run_current_owner_delta"
    assert payload["domain_closeout_surface"] == "owner_receipt_or_typed_blocker_or_human_gate_or_route_back_ref"

    entries = payload["revision_export_and_acceptance_entries"]
    revision_entry = entries["revision_entrypoint"]
    assert revision_entry["domain_ref"] == "agent/skills/revision-entrypoint-router.md"
    assert set(revision_entry["accepted_return_shapes"]) == REVISION_ENTRY_ACCEPTED_RETURN_SHAPES
    assert revision_entry["evidence_package_role"] == "output_refs_only_not_route_bypass"

    export_entry = entries["publication_or_final_export"]
    assert export_entry["domain_ref"] == "runtime/native_helpers/bookforge_pdf_export.py"
    assert set(export_entry["accepted_return_shapes"]) == DEFAULT_ENTRY_ACCEPTED_RETURN_SHAPES
    assert export_entry["evidence_package_role"] == "output_refs_only_not_route_bypass"

    production_entry = entries["production_acceptance"]
    assert production_entry["domain_ref"] == "contracts/production_acceptance/bookforge-production-acceptance.json"
    assert set(production_entry["accepted_return_shapes"]) == DEFAULT_ENTRY_ACCEPTED_RETURN_SHAPES
    assert production_entry["evidence_package_role"] == "output_refs_only_not_route_bypass"

    evidence_policy = payload["evidence_package_policy"]
    assert evidence_policy["index_ref"] == "docs/evidence/README.md"
    assert evidence_policy["role"] == "historical_or_output_refs_only"
    for field in (
        "can_be_default_entry",
        "can_explain_around_owner_boundary",
        "can_claim_acceptance",
        "can_claim_production_ready",
    ):
        assert evidence_policy[field] is False, f"default_entry.evidence_package_policy.{field} expected false"

    assert {
        "repo_local_stage_run_runner",
        "private_stage_run_wrapper",
        "private_temporal_wrapper",
        "direct_opl_bookforge_runtime_cli_as_default_entry",
        "evidence_package_as_acceptance_bypass",
    } <= set(payload["forbidden_default_entries"])
    for field, value in payload["forbidden_claims"].items():
        assert value is False, f"default_entry.forbidden_claims.{field} expected false"


def assert_private_platform_retirement_matrix(
    functional_audit: dict[str, Any],
    generated_handoff: dict[str, Any],
) -> None:
    matrix = functional_audit["bookforge_private_platform_retirement_matrix"]
    assert {entry["surface_id"] for entry in matrix} == PRIVATE_PLATFORM_RETIREMENT_SURFACES
    by_surface = {entry["surface_id"]: entry for entry in matrix}

    publication = by_surface["publication_and_export_helper"]
    assert publication["replacement_opl_primitive"] == "opl_pack_native_helper_probe"
    assert publication["retirement_action"] == "retain_as_domain_specific_native_helper_only"
    assert publication["physical_delete_authorized"] is False
    assert "system_package_manager" in publication["forbidden_domain_repo_roles"]
    assert "publication_ready_authority" in publication["forbidden_domain_repo_roles"]

    image = by_surface["image_asset_helper"]
    assert image["replacement_opl_primitive"] == "codex_native_image_generation_surface_plus_opl_generated_artifact_refs"
    assert image["retirement_action"] == "retain_as_domain_specific_asset_materialization_helper_only"
    assert image["physical_delete_authorized"] is False
    assert "api_key_or_base_url_owner" in image["forbidden_domain_repo_roles"]
    assert "runtime_queue_owner" in image["forbidden_domain_repo_roles"]

    hygiene = by_surface["project_hygiene_helper"]
    assert hygiene["replacement_opl_primitive"] == "opl_workspace_source_hygiene_and_artifact_lifecycle_projection"
    assert hygiene["retirement_action"] == "retain_as_deterministic_diagnostic_helper_only"
    assert hygiene["physical_delete_authorized"] is False
    assert "session_store" in hygiene["forbidden_domain_repo_roles"]
    assert "status_workbench" in hygiene["forbidden_domain_repo_roles"]
    assert hygiene["active_caller_boundary"] == "no_default_or_generated_caller_for_retained_domain_diagnostic"

    absent = by_surface["runtime_session_update_absence"]
    assert absent["current_paths"] == []
    assert absent["retirement_action"] == "keep_absent_and_fail_closed_if_reintroduced"
    assert absent["active_caller_boundary"] == "no_repo_local_runtime_session_update_or_workbench_default_caller"
    assert "package_update_manager" in absent["forbidden_domain_repo_roles"]

    modules = {module["module_id"]: module for module in functional_audit["modules"]}
    assert PRIVATE_PLATFORM_NATIVE_HELPER_MODULES <= set(modules)
    for module_id in PRIVATE_PLATFORM_NATIVE_HELPER_MODULES:
        module = modules[module_id]
        assert module["classification"] == "native_helper_implementation", module_id
        assert module["semantic_equivalence_status"] == "cleared_by_boundary", module_id
        assert module["audit_visibility"] == "hidden_by_default", module_id
        assert module["no_forbidden_write_evidence_ref"], module_id
    hygiene_module = modules["opl-bookforge.project-hygiene-helper"]
    assert hygiene_module["active_caller_allowed"] is False
    assert hygiene_module["active_default_caller_allowed"] is False
    assert hygiene_module["active_callers"] == []
    assert hygiene_module["active_caller_status"] == "no_active_caller_retained_domain_diagnostic"

    projection = generated_handoff["private_platform_retirement_projection"]
    assert projection["owner"] == "one-person-lab"
    assert projection["source_contract_ref"] == "contracts/functional_privatization_audit.json#bookforge_private_platform_retirement_matrix"
    assert {entry["surface_id"] for entry in projection["surfaces"]} == PRIVATE_PLATFORM_RETIREMENT_SURFACES
    for surface in projection["surfaces"]:
        assert surface["generated_or_hosted_owner"] == "one-person-lab", surface["surface_id"]
        assert surface["default_runtime_surface"] is False, surface["surface_id"]
        assert surface["ready_claim_authorized"] is False, surface["surface_id"]
    assert set(projection["forbidden_projection_claims"]) == PRIVATE_PLATFORM_FORBIDDEN_READY_CLAIMS
    for field, value in projection["forbidden_projection_claims"].items():
        assert value is False, f"private_platform_retirement_projection.{field} expected false"


def assert_opl_default_hygiene_and_probe_consumption(repo: Path) -> None:
    workspace_policy = load_json(repo, "contracts/workspace_lifecycle_policy.json")
    guard = workspace_policy["byproduct_policy"]["repo_source_byproduct_guard"]
    assert guard["guard_surface"] == "opl_repo_source_byproduct_guard"
    assert guard["guard_owner"] == "one-person-lab"
    assert guard["guard_command"] == "opl workspace source-hygiene --source-root <repo> --json"

    verify_script = (repo / "scripts/verify.sh").read_text(encoding="utf-8")
    assert verify_script.count('workspace source-hygiene --source-root "${repo_dir}" --json') == 2
    assert "bookforge_project_hygiene.py" not in verify_script
    assert "--doctor" not in verify_script
    for helper_ref in (
        "runtime/native_helpers/bookforge_pdf_export.py",
        "runtime/native_helpers/bookforge_imagegen_asset.py",
    ):
        assert "--doctor" not in (repo / helper_ref).read_text(encoding="utf-8"), helper_ref

    for descriptor_ref, expected in NATIVE_HELPER_PROBE_DESCRIPTORS.items():
        descriptor = load_json(repo, descriptor_ref)
        assert descriptor["surface_kind"] == "opl_pack_native_helper_probe_descriptor", descriptor_ref
        assert descriptor["schema_version"] == 1, descriptor_ref
        assert descriptor["helper_id"] == expected["helper_id"], descriptor_ref
        assert descriptor["owner"] == "opl-bookforge", descriptor_ref
        assert descriptor["entrypoint_ref"] == expected["entrypoint_ref"], descriptor_ref
        assert descriptor["runtime_command"] == "python3", descriptor_ref
        assert descriptor["required_commands"] == expected["required_commands"], descriptor_ref
        assert set(descriptor["authority_boundary"]) == NATIVE_HELPER_PROBE_AUTHORITY_FIELDS, descriptor_ref
        assert all(value is False for value in descriptor["authority_boundary"].values()), descriptor_ref
        assert (repo / descriptor_ref).parent.joinpath(descriptor["entrypoint_ref"]).is_file(), descriptor_ref
        command = f'pack native-helper probe --descriptor "${{repo_dir}}/{descriptor_ref}" --json'
        assert command in verify_script, descriptor_ref

    assert not (repo / "runtime/native_helpers/bookforge_project_hygiene_parts/byproducts.py").exists()
    hygiene_helper = (repo / "runtime/native_helpers/bookforge_project_hygiene.py").read_text(encoding="utf-8")
    assert "bookforge_project_hygiene_parts.opl_lifecycle" not in hygiene_helper
    assert "--require-opl-lifecycle" not in hygiene_helper
    assert "--source-root" not in hygiene_helper
    assert "workspace artifact-lifecycle" not in hygiene_helper
    assert not (repo / "runtime/native_helpers/bookforge_project_hygiene_parts/opl_lifecycle.py").exists()
    assert "bookforge_project_hygiene.py" not in (
        repo / "agent/skills/book-production.md"
    ).read_text(encoding="utf-8")


def assert_live_stage_run_progress_evidence(payload: dict[str, Any]) -> None:
    assert payload["surface_kind"] == "domain_live_stage_run_progress_evidence"
    assert payload["domain_id"] == "opl-bookforge"
    assert payload["owner"] == "OPL Book Forge"
    assert payload["status"] in LIVE_STAGE_RUN_PROGRESS_ACCEPTED_STATUSES
    assert payload["status"] == "owner_typed_blocker_recorded_not_ready_claim"
    assert payload["typed_blocker_kind"] == "owner_acceptance_final_export_and_live_stage_run_evidence_tail_open"

    refs = payload["refs"]
    assert LIVE_STAGE_RUN_PROGRESS_REF_FIELDS <= set(refs), "live StageRun progress evidence missing ref groups"
    assert_ref_fields(
        refs["typed_blocker_refs"],
        {
            "docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/receipts/storyline-owner-blocker.json",
            "docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/receipts/book-owner-blocker.json",
        },
        "live StageRun typed blockers",
    )
    assert_ref_fields(
        refs["quality_or_export_receipt_refs"],
        {
            "docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/receipts/storyline-independent-gate-receipt.json",
            "docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/receipts/book-materialization-independent-gate-receipt.json",
        },
        "live StageRun quality/export refs",
    )
    assert_ref_fields(
        refs["no_regression_refs"],
        {
            "contracts/temporal_stage_run_consumption_policy.json#completion_boundary",
            "contracts/temporal_stage_run_consumption_policy.json#completion_audit.acceptance_tail",
        },
        "live StageRun no-regression refs",
    )
    assert_ref_fields(
        refs["next_verification_command_refs"],
        {"python3 tests/test_temporal_stage_run_consumption_policy.py", "./scripts/verify.sh"},
        "live StageRun verification refs",
    )

    evidence_items = payload["evidence_items"]
    assert len(evidence_items) == 2, evidence_items
    assert {item["result_shape"] for item in evidence_items} == {"typed_blocker_ref"}
    assert {item["status"] for item in evidence_items} == {"blocked_owner_acceptance_missing"}

    open_tail = payload["open_tail"]
    for field in (
        "owner_acceptance_open",
        "final_export_acceptance_open",
        "live_stage_run_evidence_tail_open",
        "real_long_book_run_evidence_open",
        "direct_runtime_cli_or_hosted_parity_evidence_open",
    ):
        assert open_tail[field] is True, f"open_tail.{field} expected true"

    authority_boundary = payload["authority_boundary"]
    assert authority_boundary["refs_only"] is True
    for field in (
        "domain_ready_claimed",
        "production_ready_claimed",
        "quality_or_export_ready_claimed",
        "owner_acceptance_claimed",
        "final_export_acceptance_claimed",
        "live_stage_run_progress_complete_claimed",
        "opl_can_sign_owner_receipt",
        "opl_can_create_typed_blocker",
        "opl_can_claim_domain_ready",
        "opl_can_claim_production_ready",
        "bookforge_contract_can_synthesize_owner_receipt_body",
        "bookforge_contract_can_write_runtime_queue_or_provider_attempt",
    ):
        assert authority_boundary[field] is False, f"authority_boundary.{field} expected false"
    assert LIVE_STAGE_RUN_PROGRESS_FORBIDDEN_CLAIMS <= set(payload["forbidden_claims"])


def assert_production_acceptance_tail(payload: dict[str, Any]) -> None:
    assert payload["surface_kind"] == "bookforge_domain_owned_production_acceptance_evidence"
    assert payload["domain_id"] == "opl-bookforge"
    assert payload["owner"] == "OPL Book Forge"
    assert payload["evidence_tail_status"] == "domain_owned_typed_blocker_with_next_verification_ref"
    assert payload["acceptance_status"] == "domain_owned_typed_blocker_with_next_verification_ref"

    default_entry = payload["default_entry_boundary"]
    assert default_entry["default_entry_routing_ref"] == "contracts/temporal_stage_run_consumption_policy.json#default_entry_routing"
    assert default_entry["default_entry_surface_kind"] == "opl_stage_run_attempt_request"
    assert default_entry["default_read_surface"] == "stage_run_current_owner_delta"
    assert default_entry["accepted_return_shape"] == "owner_receipt_or_typed_blocker_or_human_gate_or_route_back_ref"
    assert default_entry["evidence_package_role"] == "output_refs_only_not_route_bypass"
    assert default_entry["direct_domain_cli_is_default_entry"] is False
    assert default_entry["evidence_package_can_be_default_entry"] is False
    assert default_entry["production_acceptance_can_be_explained_around_owner_boundary"] is False

    closure_evidence = payload["closure_evidence"]
    assert closure_evidence["accepted_return_shape"] == "typed_blocker"
    assert closure_evidence["typed_blocker_kind"] == "owner_acceptance_final_export_and_production_evidence_tail_open"
    assert closure_evidence["next_verification_ref"] == "./scripts/verify.sh"

    refs = payload["refs"]
    assert_ref_fields(
        refs["typed_blocker_refs"],
        {
            "docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/receipts/storyline-owner-blocker.json",
            "docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/receipts/book-owner-blocker.json",
        },
        "production acceptance typed blockers",
    )
    assert_ref_fields(
        refs["artifact_receipt_refs"],
        {
            "docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/receipts/production-readiness-closeout.json",
            "docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/quality/local-verification-receipt.json",
        },
        "production acceptance artifact receipts",
    )
    assert_ref_fields(
        refs["doc_refs"],
        {
            "docs/status.md#claim-boundary",
            "docs/active/bookforge-ideal-state-gap-plan.md#current-completion-progress",
        },
        "production acceptance docs",
    )
    assert_ref_fields(
        refs["next_verification_command_refs"],
        {
            "./scripts/verify.sh",
            "/Users/gaofeng/workspace/one-person-lab/bin/opl agents conformance --agent opl-bookforge=<repo> --json",
        },
        "production acceptance verification refs",
    )

    typed_blocker = payload["typed_blocker"]
    assert typed_blocker["owner"] == "OPL Book Forge"
    assert typed_blocker["blocker_kind"] == "owner_acceptance_final_export_and_production_evidence_tail_open"
    assert_ref_fields(
        typed_blocker["blocker_refs"],
        set(refs["typed_blocker_refs"]),
        "production acceptance typed blocker body",
    )

    open_tail = payload["open_tail"]
    for field in (
        "owner_acceptance_open",
        "final_export_acceptance_open",
        "production_ready_claim_open",
        "real_long_book_run_evidence_open",
        "direct_runtime_cli_or_hosted_parity_evidence_open",
    ):
        assert open_tail[field] is True, f"open_tail.{field} expected true"

    authority_boundary = payload["authority_boundary"]
    assert authority_boundary["refs_only"] is True
    for field in (
        "domain_ready_claimed",
        "production_ready_claimed",
        "quality_or_export_ready_claimed",
        "owner_acceptance_claimed",
        "final_export_acceptance_claimed",
        "live_stage_run_progress_complete_claimed",
        "provider_completion_is_domain_completion",
        "generated_surface_ready_counts_as_domain_ready",
        "stage_run_status_ready_counts_as_domain_ready",
        "opl_can_write_domain_truth",
        "opl_can_sign_owner_receipt",
        "opl_can_create_typed_blocker",
        "opl_can_authorize_quality_or_export",
        "opl_can_authorize_domain_ready",
        "opl_can_claim_domain_ready",
        "opl_can_claim_production_ready",
        "bookforge_contract_can_synthesize_owner_receipt_body",
        "bookforge_contract_can_write_runtime_queue_or_provider_attempt",
        "conformance_report_can_claim_domain_ready",
        "domain_ready_claimed_by_conformance",
    ):
        assert authority_boundary[field] is False, f"authority_boundary.{field} expected false"
    assert PRODUCTION_ACCEPTANCE_FORBIDDEN_CLAIMS <= set(payload["forbidden_claims"])


def assert_no_forbidden_keys(payload: Any, forbidden: set[str], label: str) -> None:
    if isinstance(payload, dict):
        present = forbidden & set(payload)
        assert not present, f"{label} includes forbidden keys: {present}"
        for value in payload.values():
            assert_no_forbidden_keys(value, forbidden, label)
    elif isinstance(payload, list):
        for value in payload:
            assert_no_forbidden_keys(value, forbidden, label)


def assert_handoff_current_paths_exist(repo: Path, generated_handoff: dict[str, Any]) -> None:
    for surface in generated_handoff["handoff_surfaces"]:
        for current_path in surface.get("current_paths", []):
            assert (repo / current_path).exists(), f"{surface['surface_id']} points at missing {current_path}"


def assert_opl_ledger_artifact_registration(payload: dict[str, Any]) -> None:
    assert payload["surface_kind"] == "bookforge_opl_ledger_artifact_registration_contract"
    assert payload["version"] == "bookforge-opl-ledger-artifact-registration.v1"
    assert payload["contract_owner"] == "opl-bookforge"
    assert payload["domain_id"] == "opl-bookforge"
    assert payload["ledger_owner"] == "one-person-lab"
    assert payload["refs_only"] is True
    assert payload["structural_gate_only"] is True

    shape = payload["registration_record_shape"]
    assert_ref_fields(shape["required_metadata_fields"], {"domain_id", "project_id", "artifact_class"}, "ledger metadata")
    assert_ref_fields(shape["required_ref_fields"], {"artifact_ref", "artifact_index_ref", "review_ref"}, "ledger refs")
    assert_ref_fields(shape["required_hash_fields"], {"artifact_hash"}, "ledger hash")
    assert_ref_fields(
        shape["optional_ref_fields"],
        {"source_index_ref", "quality_receipt_ref", "export_receipt_ref", "owner_receipt_ref", "route_back_ref"},
        "ledger optional refs",
    )
    assert set(shape["forbidden_registration_fields"]) == LEDGER_FORBIDDEN_REGISTRATION_FIELDS
    allowed_shape_fields = (
        set(shape["required_metadata_fields"])
        | set(shape["required_ref_fields"])
        | set(shape["required_hash_fields"])
        | set(shape["optional_ref_fields"])
        | set(shape["ledger_written_fields"])
    )
    assert not (allowed_shape_fields & LEDGER_FORBIDDEN_REGISTRATION_FIELDS)

    hash_policy = payload["hash_policy"]
    assert hash_policy["hash_algorithm"] == "sha256"
    assert hash_policy["hash_required_for_every_registration"] is True
    assert hash_policy["hash_can_replace_artifact_ref"] is False
    assert hash_policy["hash_can_claim_artifact_ready"] is False

    artifact_classes = payload["artifact_classes"]
    assert {item["artifact_class"] for item in artifact_classes} == LEDGER_REGISTRATION_ARTIFACT_CLASSES
    for item in artifact_classes:
        assert item["owner"] == "OPL Book Forge", item["artifact_class"]
        class_fields = set(item["required_ref_fields"]) | set(item["required_hash_fields"]) | set(item["receipt_ref_fields"])
        assert not (class_fields & LEDGER_FORBIDDEN_REGISTRATION_FIELDS), item["artifact_class"]
        assert "artifact_hash" in item["required_hash_fields"], item["artifact_class"]
        assert "review_ref" in item["required_ref_fields"], item["artifact_class"]
        assert any(field.endswith("_ref") for field in item["receipt_ref_fields"]), item["artifact_class"]

    command_refs = {item["command_id"]: item for item in payload["opl_ledger_command_refs"]}
    assert set(command_refs) == {"opl-ledger.bundle-record", "opl-ledger.bundle-inspect"}
    for item in command_refs.values():
        assert item["owner"] == "one-person-lab", item["command_id"]
        assert item["bookforge_default_entry"] is False, item["command_id"]
        assert "opl ledger bundle" in item["command_ref"], item["command_id"]

    readback = payload["readback_surface"]
    assert readback["owner"] == "one-person-lab"
    assert readback["contract_ref"] == "contracts/opl_ledger_artifact_registration.json"
    assert readback["payload_root"] == "opl_ledger_artifact_registration"
    assert readback["readback_counts_as_registration_visibility"] is True
    assert readback["readback_counts_as_book_delivery_ready"] is False
    assert readback["readback_counts_as_owner_acceptance"] is False
    assert readback["readback_counts_as_publication_or_final_export_verdict"] is False

    boundary = payload["owner_boundary"]
    assert boundary["bookforge_owner"] == "OPL Book Forge"
    assert boundary["opl_ledger_owner"] == "one-person-lab"
    assert boundary["bookforge_supplies_artifact_refs_hashes_indexes_reviews_and_receipt_refs"] is True
    for field in (
        "bookforge_contract_can_write_ledger_entries",
        "bookforge_contract_can_mutate_artifact_body",
        "bookforge_contract_can_generate_owner_receipt",
        "bookforge_contract_can_create_typed_blocker",
        "bookforge_contract_can_write_runtime_queue",
        "bookforge_contract_can_write_provider_attempt",
        "opl_ledger_can_mutate_bookforge_artifact_body",
        "opl_ledger_can_authorize_quality_publication_or_final_export",
        "opl_ledger_can_sign_owner_receipt",
        "opl_ledger_can_create_typed_blocker",
    ):
        assert boundary[field] is False, f"owner_boundary.{field} expected false"

    for field, value in payload["false_ready_guard"].items():
        assert value is False, f"false_ready_guard.{field} expected false"

    assert_no_forbidden_keys(payload, LEDGER_FORBIDDEN_REGISTRATION_FIELDS, "ledger registration contract")


def assert_generated_handoff_ledger_projection(generated_handoff: dict[str, Any]) -> None:
    assert generated_handoff["opl_ledger_artifact_registration_contract_ref"] == "contracts/opl_ledger_artifact_registration.json"
    projection = generated_handoff["opl_ledger_artifact_registration_projection"]
    assert projection["owner"] == "one-person-lab"
    assert projection["ledger_owner"] == "one-person-lab"
    assert projection["domain_owner"] == "OPL Book Forge"
    assert projection["domain_id"] == "opl-bookforge"
    assert projection["contract_ref"] == "contracts/opl_ledger_artifact_registration.json"
    assert projection["payload_root"] == "opl_ledger_artifact_registration"
    assert set(projection["registered_field_kinds"]) == LEDGER_REGISTERED_FIELD_KINDS
    assert projection["refs_only"] is True
    for field in (
        "bookforge_can_write_ledger_entries",
        "bookforge_can_mutate_artifact_body",
        "ledger_entry_counts_as_domain_ready",
        "ledger_entry_counts_as_owner_acceptance",
        "ledger_entry_counts_as_publication_or_final_export_verdict",
        "ledger_entry_counts_as_runtime_queue_or_provider_attempt",
    ):
        assert projection[field] is False, f"ledger projection.{field} expected false"

    generated_surface_ids = {item["surface_id"] for item in generated_handoff["generated_surfaces"]}
    handoff_surface_ids = {item["surface_id"] for item in generated_handoff["handoff_surfaces"]}
    assert "opl_ledger_artifact_registration" not in generated_surface_ids
    assert "opl_ledger_artifact_registration" not in handoff_surface_ids


def assert_capability_map_standard_kinds(repo: Path, capability_map: dict[str, Any]) -> None:
    capabilities = capability_map["capabilities"]
    for capability in capabilities:
        assert capability["capability_kind"] in STANDARD_CAPABILITY_KINDS, capability["capability_id"]

    primary = next(capability for capability in capabilities if capability["surface_role"] == "primary_skill")
    assert primary["capability_kind"] == "primary_skill"
    assert primary["physical_source_ref"]["ref"] == "agent/primary_skill/SKILL.md"
    assert primary["carrier_projection_contract"]["carrier_skill_ref"] == "plugins/opl-bookforge/skills/opl-bookforge/SKILL.md"
    assert primary["carrier_projection_contract"]["carrier_materialization"] == "materialized_full_skill_copy"
    plugin_manifest = json.loads((repo / "plugins/opl-bookforge/.codex-plugin/plugin.json").read_text())
    assert plugin_manifest["name"] == "opl-bookforge"
    assert plugin_manifest["skills"] == "./skills/"
    assert (
        (repo / "plugins/opl-bookforge/skills/opl-bookforge/SKILL.md").read_text()
        == (repo / "agent/primary_skill/SKILL.md").read_text()
    )


def assert_legacy_professional_skill_redirects(repo: Path, capability_map: dict[str, Any]) -> None:
    professional_capabilities = {
        capability["capability_id"]: capability
        for capability in capability_map["capabilities"]
        if capability["surface_role"] == "professional_skill"
    }
    skill_paths = {
        str(path.relative_to(repo))
        for path in (repo / "agent/professional_skills").glob("*/SKILL.md")
    }
    redirects = capability_map["legacy_professional_skill_redirects"]

    assert {
        entry["legacy_ref"]: entry["covered_by_skill_ref"]
        for entry in redirects
    } == LEGACY_PROFESSIONAL_SKILL_REDIRECTS

    for entry in redirects:
        legacy_skill_id = entry["legacy_ref"].removeprefix("legacy-professional-skill:")
        legacy_root = repo / "agent/professional_skills" / legacy_skill_id
        assert entry["state"] == "legacy_redirect", entry["legacy_ref"]
        assert entry["capability_kind"] == "legacy_professional_skill_redirect", entry["legacy_ref"]
        assert entry["capability_preserved"] is True, entry["legacy_ref"]
        assert entry["default_codex_exposure"] is False, entry["legacy_ref"]
        assert entry["covered_by_skill_ref"] in skill_paths, entry["legacy_ref"]
        assert entry["covered_by_capability_id"] in professional_capabilities, entry["legacy_ref"]
        assert (
            professional_capabilities[entry["covered_by_capability_id"]]["physical_source_ref"]["ref"]
            == entry["covered_by_skill_ref"]
        ), entry["legacy_ref"]
        assert not (legacy_root / "SKILL.md").exists(), entry["legacy_ref"]
        assert not (legacy_root / "TOMBSTONE.md").exists(), entry["legacy_ref"]
        if legacy_root.exists():
            assert not any(legacy_root.iterdir()), entry["legacy_ref"]


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    capability_map = load_json(repo, "contracts/capability_map.json")
    policy = load_json(repo, "contracts/temporal_stage_run_consumption_policy.json")
    action_catalog = load_json(repo, "contracts/action_catalog.json")
    foundry_series = load_json(repo, "contracts/foundry_agent_series.json")
    generated_handoff = load_json(repo, "contracts/generated_surface_handoff.json")
    functional_audit = load_json(repo, "contracts/functional_privatization_audit.json")
    agent_lab_handoff = load_json(repo, "contracts/agent_lab_handoff.json")
    stage_run_profile = load_json(repo, "contracts/stage_run_kernel_profile.json")
    live_stage_run_progress = load_json(repo, "contracts/live_stage_run_progress_evidence.json")
    production_acceptance = load_json(repo, "contracts/production_acceptance/bookforge-production-acceptance.json")
    opl_ledger_artifact_registration = load_json(repo, "contracts/opl_ledger_artifact_registration.json")

    assert policy["surface_kind"] == "opl_temporal_stage_run_consumption_policy"
    assert policy["temporal_attempt_ledger_owner"] == "one-person-lab"
    assert policy["temporal_runtime_owner"] == "one-person-lab"
    assert policy["stage_run_owner"] == "one-person-lab"

    assert_false(policy, "completion_boundary.provider_completion_is_domain_completion")
    assert_false(policy, "completion_boundary.provider_completion_is_closeout")
    assert_false(policy, "completion_boundary.generated_surface_ready_counts_as_domain_ready")
    assert_false(policy, "completion_boundary.stage_run_status_ready_counts_as_domain_ready")
    assert_false(policy, "completion_boundary.temporal_workflow_completion_counts_as_domain_ready")
    assert_false(policy, "forbidden_domain_repo_ownership.domain_repo_can_own_temporal_runtime")
    assert_false(policy, "forbidden_domain_repo_ownership.domain_repo_can_own_temporal_wrapper")
    assert_false(policy, "forbidden_domain_repo_ownership.domain_repo_can_own_stage_run_wrapper")
    assert_false(policy, "forbidden_domain_repo_ownership.domain_repo_can_own_attempt_ledger")
    assert_false(policy, "write_boundary.bookforge_can_write_opl_stage_attempts")
    assert_false(policy, "write_boundary.bookforge_can_write_temporal_attempt_ledger")
    assert_false(policy, "write_boundary.bookforge_can_write_private_scheduler")
    assert_false(policy, "write_boundary.bookforge_can_write_private_session_store")
    assert_true(policy, "projection_policy.projection_must_not_create_second_runtime")
    assert_true(policy, "projection_policy.projection_must_not_create_attempt_ledger")
    assert_true(policy, "projection_policy.projection_must_not_wrap_temporal_or_stage_run")
    assert_closeout_refs(policy["completion_boundary"]["domain_completion_ref_fields"], "policy completion_boundary")
    assert_surface_export_boundary(policy, "policy surface export boundary")
    assert_functional_closure_gate(policy["functional_closure_gate"])
    assert_default_entry_routing(policy["default_entry_routing"])
    assert_opl_default_hygiene_and_probe_consumption(repo)
    assert foundry_series["surface_kind"] == "opl_foundry_agent_series_consumer"
    assert foundry_series["canonical_policy_export"] == "opl-framework/foundry-agent-series-policy"
    assert (
        foundry_series["canonical_series_contract_ref"]
        == "contracts/opl-framework/foundry-agent-series-contract.json"
    )
    assert "standard_feedback_self_evolution_trigger_policy" not in foundry_series
    assert_handoff_current_paths_exist(repo, generated_handoff)
    trigger = agent_lab_handoff["feedback_self_evolution_trigger"]
    assert trigger["surface_kind"] == "opl_foundry_agent_feedback_self_evolution_trigger"
    assert (
        trigger["policy_ref"]
        == "contracts/opl-framework/foundry-agent-series-contract.json#/standard_feedback_self_evolution_trigger_policy"
    )
    assert trigger["target_agent_id"] == "opl-bookforge"
    assert trigger["external_suite_ref"] == "contracts/agent_lab_handoff.json"
    assert trigger["developer_mode_execution_gate_refs"] == [
        "opl-developer-mode:repo-fix-execution",
        "opl-developer-mode:direct-fix-or-fork-pr-route",
    ]

    audit = policy["completion_audit"]
    assert audit["audit_role"] == "separate_opl_transport_generated_status_from_bookforge_domain_completion"
    assert audit["acceptance_tail"]["real_book_pilot_evidence_role"] == "historical_evidence_only"
    assert audit["acceptance_tail"]["real_book_pilot_counts_as_final_export_acceptance"] is False
    assert audit["acceptance_tail"]["owner_receipt_body_must_not_be_synthesized_by_contract"] is True
    assert audit["acceptance_tail"]["live_stage_run_evidence_required_for_runtime_claims"] is True
    assert audit["acceptance_tail"]["owner_export_acceptance_required_for_final_export_claims"] is True

    opl_accounts = audit["opl_provider_generated_and_stage_run_accounts"]
    assert set(opl_accounts) == FALSE_COMPLETION_ACCOUNTS
    for account_name, account in opl_accounts.items():
        assert account["owner"] == "one-person-lab", account_name
        assert_false_completion_account(account, account_name)

    completion_accounts = audit["bookforge_completion_accounts"]
    assert set(completion_accounts) == COMPLETION_ACCOUNTS
    review_pdf = completion_accounts["review_pdf"]
    assert review_pdf["owner"] == "OPL Book Forge"
    assert_ref_fields(
        review_pdf["minimum_ref_fields"],
        {"review_pdf_ref", "review_pdf_receipt_ref"},
        "review_pdf",
    )
    assert review_pdf["counts_as_publication_proof_ready"] is False
    assert review_pdf["counts_as_final_export_ready"] is False
    assert review_pdf["counts_as_owner_acceptance"] is False

    publication_proof = completion_accounts["publication_proof"]
    assert publication_proof["owner"] == "OPL Book Forge"
    assert_ref_fields(
        publication_proof["minimum_ref_fields"],
        {
            "publication_proof_ref",
            "publication_design_profile_ref",
            "rendered_page_inspection_ref",
            "asset_resolution_receipt_ref",
        },
        "publication_proof",
    )
    assert publication_proof["counts_as_final_export_ready"] is False
    assert publication_proof["counts_as_owner_acceptance"] is False

    final_export = completion_accounts["final_export"]
    assert final_export["owner"] == "OPL Book Forge"
    assert final_export["requires_owner_export_acceptance"] is True
    assert_ref_fields(
        final_export["minimum_ref_fields"],
        {"final_export_ref", "publication_proof_ref", "owner_export_acceptance_ref"},
        "final_export",
    )
    assert final_export["counts_as_owner_acceptance"] is False

    owner_acceptance = completion_accounts["owner_acceptance"]
    assert owner_acceptance["owner"] == "owner_or_human_gate"
    assert_ref_fields(owner_acceptance["minimum_ref_fields"], {"owner_receipt_ref"}, "owner_acceptance")
    assert owner_acceptance["can_be_written_by_opl_provider"] is False
    assert owner_acceptance["can_be_written_by_generated_surface"] is False
    assert owner_acceptance["can_be_inferred_from_stage_run_status"] is False

    assert action_catalog["temporal_stage_run_consumption_policy_ref"] == "contracts/temporal_stage_run_consumption_policy.json"
    assert action_catalog["completion_audit_policy_ref"] == "contracts/temporal_stage_run_consumption_policy.json#completion_audit"
    default_entry_policy = action_catalog["default_entry_policy"]
    assert default_entry_policy["default_entry_surface_kind"] == "opl_stage_run_attempt_request"
    assert default_entry_policy["entry_owner"] == "one-person-lab"
    assert default_entry_policy["stage_run_account_owner"] == "one-person-lab"
    assert default_entry_policy["domain_owner"] == "OPL Book Forge"
    assert default_entry_policy["stage_run_policy_ref"] == "contracts/temporal_stage_run_consumption_policy.json#default_entry_routing"
    assert default_entry_policy["direct_domain_cli_is_default_entry"] is False
    assert default_entry_policy["evidence_package_can_be_default_entry"] is False
    assert default_entry_policy["production_acceptance_routes_through_owner_answer_ref"] is True
    catalog_audit = action_catalog["completion_audit_summary"]
    assert catalog_audit["review_pdf_publication_proof_final_export_are_distinct"] is True
    assert catalog_audit["provider_completion_counts_as_any_bookforge_completion_account"] is False
    assert catalog_audit["generated_surface_ready_counts_as_any_bookforge_completion_account"] is False
    assert catalog_audit["stage_run_status_ready_counts_as_any_bookforge_completion_account"] is False
    assert catalog_audit["final_export_requires_owner_export_acceptance_ref"] is True
    assert catalog_audit["owner_acceptance_cannot_be_inferred_from_generated_or_stage_run_status"] is True
    assert catalog_audit["real_book_pilot_evidence_is_acceptance_tail_not_completion"] is True
    assert_false(action_catalog, "authority_boundary.provider_completion_is_domain_completion")
    assert_false(action_catalog, "authority_boundary.domain_repo_can_own_temporal_runtime")
    assert_false(action_catalog, "authority_boundary.generated_surface_ready_counts_as_domain_ready")
    assert_false(action_catalog, "authority_boundary.bookforge_can_write_opl_stage_attempts")
    assert action_catalog["authority_boundary"]["temporal_attempt_ledger_owner"] == "one-person-lab"
    assert_surface_export_boundary(action_catalog, "action catalog surface export boundary")

    assert "standard_public_projection_policy" not in foundry_series
    assert all(value is False for value in foundry_series["authority_boundary"].values())
    for action in action_catalog["actions"]:
        stage_name = "storyline-architecture" if action["action_id"] == "shape-storyline" else "chapter-production-planning"
        expected_command_prefix = (
            f"opl family-runtime attempt create --domain opl-bookforge --stage {stage_name} --provider temporal "
        )
        assert action["source_command"]["surface_kind"] == "opl_stage_run_attempt_request", action["action_id"]
        assert action["source_command"]["command"].startswith(expected_command_prefix), action["action_id"]
        assert action["supported_surfaces"]["cli"]["surface_kind"] == "opl_stage_run_attempt_request", action["action_id"]
        assert action["supported_surfaces"]["cli"]["command"] == action["source_command"]["command"], action["action_id"]
        assert action["supported_surfaces"]["product_entry"]["surface_kind"] == "opl_stage_run_attempt_request", action["action_id"]
        assert action["supported_surfaces"]["product_entry"]["command"] == action["source_command"]["command"], action["action_id"]
        boundary = action["authority_boundary"]
        assert boundary["provider_completion_is_domain_completion"] is False, action["action_id"]
        assert boundary["domain_repo_can_own_temporal_runtime"] is False, action["action_id"]
        assert boundary["bookforge_can_write_opl_stage_attempts"] is False, action["action_id"]
        assert boundary["default_entry_surface_kind"] == "opl_stage_run_attempt_request", action["action_id"]
        assert boundary["default_entry_routes_via_stage_run_account"] is True, action["action_id"]
        assert boundary["direct_domain_cli_is_default_entry"] is False, action["action_id"]
        assert boundary["evidence_package_can_bypass_owner_boundary"] is False, action["action_id"]
        assert boundary["temporal_attempt_ledger_owner"] == "one-person-lab", action["action_id"]
        assert_closeout_refs(boundary["domain_completion_ref_fields"], f"action {action['action_id']}")
        assert boundary["completion_audit_policy_ref"] == "contracts/temporal_stage_run_consumption_policy.json#completion_audit", action["action_id"]
        assert set(boundary["completion_accounts"]) == COMPLETION_ACCOUNTS, action["action_id"]
        assert set(boundary["false_completion_accounts"]) == FALSE_COMPLETION_ACCOUNTS, action["action_id"]

    assert generated_handoff["temporal_stage_run_consumption_policy_ref"] == "contracts/temporal_stage_run_consumption_policy.json"
    projection = generated_handoff["temporal_stage_run_projection"]
    assert projection["owner"] == "one-person-lab"
    assert projection["default_entry_routing_ref"] == "contracts/temporal_stage_run_consumption_policy.json#default_entry_routing"
    assert projection["default_entry_surface_kind"] == "opl_stage_run_attempt_request"
    assert projection["direct_domain_cli_is_default_entry"] is False
    assert projection["evidence_package_can_be_default_entry"] is False
    assert projection["provider_completion_is_domain_completion"] is False
    assert projection["generated_surface_ready_counts_as_domain_ready"] is False
    assert projection["domain_repo_can_own_temporal_runtime"] is False
    assert projection["bookforge_can_write_opl_stage_attempts"] is False
    assert projection["temporal_attempt_ledger_owner"] == "one-person-lab"
    assert_closeout_refs(projection["domain_completion_ref_fields"], "generated handoff projection")
    assert_surface_export_boundary(projection, "generated handoff projection")
    assert_generated_handoff_ledger_projection(generated_handoff)
    assert_private_platform_retirement_matrix(functional_audit, generated_handoff)
    assert_capability_map_standard_kinds(repo, capability_map)
    assert_legacy_professional_skill_redirects(repo, capability_map)

    assert stage_run_profile["temporal_stage_run_consumption_policy_ref"] == "contracts/temporal_stage_run_consumption_policy.json"
    embedded_policy = stage_run_profile["temporal_stage_run_consumption_policy"]
    assert embedded_policy["temporal_attempt_ledger_owner"] == "one-person-lab"
    assert embedded_policy["default_entry_routing_ref"] == "contracts/temporal_stage_run_consumption_policy.json#default_entry_routing"
    assert embedded_policy["default_entry_surface_kind"] == "opl_stage_run_attempt_request"
    assert embedded_policy["direct_domain_cli_is_default_entry"] is False
    assert embedded_policy["evidence_package_can_be_default_entry"] is False
    assert embedded_policy["domain_repo_can_own_temporal_runtime"] is False
    assert embedded_policy["bookforge_can_write_opl_stage_attempts"] is False
    assert embedded_policy["provider_completion_is_domain_completion"] is False
    assert_closeout_refs(embedded_policy["domain_completion_ref_fields"], "stage run embedded policy")
    assert_surface_export_boundary(embedded_policy, "stage run embedded policy")
    assert stage_run_profile["stage_run_state_machine"]["provider_completion_is_domain_completion"] is False
    assert stage_run_profile["authority_boundary"]["domain_repo_can_own_temporal_runtime"] is False
    assert stage_run_profile["authority_boundary"]["bookforge_can_write_opl_stage_attempts"] is False
    assert stage_run_profile["authority_boundary"]["generated_surface_ready_counts_as_domain_ready"] is False
    assert stage_run_profile["authority_boundary"]["domain_repo_can_export_private_temporal_wrapper"] is False
    assert stage_run_profile["authority_boundary"]["domain_repo_can_export_private_stage_run_wrapper"] is False
    assert stage_run_profile["default_read_surface"]["root"] == "stage_run_current_owner_delta"
    assert stage_run_profile["default_read_surface"]["evidence_package_default"] is False
    assert_live_stage_run_progress_evidence(live_stage_run_progress)
    assert_production_acceptance_tail(production_acceptance)
    assert_opl_ledger_artifact_registration(opl_ledger_artifact_registration)

    print(json.dumps({
        "status": "passed",
        "test": "temporal_stage_run_consumption_policy",
        "contract": "contracts/temporal_stage_run_consumption_policy.json",
        "live_stage_run_progress_evidence_contract": "contracts/live_stage_run_progress_evidence.json",
        "production_acceptance_contract": "contracts/production_acceptance/bookforge-production-acceptance.json",
        "private_platform_retirement_contract": "contracts/functional_privatization_audit.json",
        "opl_ledger_artifact_registration_contract": "contracts/opl_ledger_artifact_registration.json",
        "capability_map_contract": "contracts/capability_map.json"
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
