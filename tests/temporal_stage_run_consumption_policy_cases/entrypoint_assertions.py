from __future__ import annotations

from pathlib import Path
from typing import Any

from temporal_stage_run_consumption_policy_cases.policy_assertions import (
    assert_closeout_refs,
    assert_surface_export_boundary,
)


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


def assert_handoff_current_paths_exist(repo: Path, generated_handoff: dict[str, Any]) -> None:
    for surface in generated_handoff["handoff_surface_overrides"]:
        for current_path in surface.get("current_paths", []):
            assert (repo / current_path).exists(), f"{surface['surface_id']} points at missing {current_path}"


def assert_generated_handoff_temporal_projection(generated_handoff: dict[str, Any]) -> None:
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


def assert_stage_run_profile(stage_run_profile: dict[str, Any]) -> None:
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
