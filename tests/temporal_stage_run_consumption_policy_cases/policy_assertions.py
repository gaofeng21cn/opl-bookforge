from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from temporal_stage_run_consumption_policy_cases.evidence_assertions import assert_ref_fields


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
            "opl agents check --repo <repo-dir> --json",
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


def assert_policy_header(policy: dict[str, Any]) -> None:
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


def assert_foundry_series(foundry_series: dict[str, Any]) -> None:
    assert foundry_series["surface_kind"] == "opl_foundry_agent_series_consumer"
    assert foundry_series["canonical_policy_export"] == "opl-framework/foundry-agent-series-policy"
    assert (
        foundry_series["canonical_series_contract_ref"]
        == "contracts/opl-framework/foundry-agent-series-contract.json"
    )
    assert "standard_feedback_self_evolution_trigger_policy" not in foundry_series


def assert_feedback_self_evolution_trigger(trigger: dict[str, Any]) -> None:
    assert trigger["surface_kind"] == "opl_foundry_agent_feedback_self_evolution_trigger"
    assert trigger["schema_version"] == 2
    assert (
        trigger["policy_ref"]
        == "contracts/opl-framework/foundry-agent-series-contract.json#/standard_feedback_self_evolution_trigger_policy"
    )
    assert trigger["target_agent_id"] == "opl-bookforge"
    assert trigger["external_suite_ref"] == "contracts/agent_lab_handoff.json"
    assert trigger["policy_id"] == "standard_agent_feedback_self_evolution_trigger.v2"
    assert trigger["agent_evolution_skill_ref"] == "opl-meta-agent:oma-agent-evolution"
    assert "agent_evolution_skill_ref" in trigger["required_trigger_fields"]
    assert "oma_evolution_skill_ref" not in trigger
    assert "default_oma_skill_ref" not in trigger
    assert trigger["developer_mode_execution_gate_refs"] == [
        "opl-developer-mode:repo-fix-execution",
        "opl-developer-mode:direct-fix-or-fork-pr-route",
    ]


def assert_completion_audit(policy: dict[str, Any]) -> None:
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


def assert_action_catalog(action_catalog: dict[str, Any], foundry_series: dict[str, Any]) -> None:
    assert action_catalog["version"] == "family-action-catalog.v2"
    assert set(action_catalog) == {
        "surface_kind",
        "version",
        "catalog_id",
        "target_domain_id",
        "owner",
        "authority_boundary",
        "actions",
    }
    assert action_catalog["authority_boundary"]["opl_role"] == "projection_consumer_only"
    assert action_catalog["authority_boundary"]["write_policy"] == "no_domain_truth_writes"
    assert_false(action_catalog, "authority_boundary.provider_completion_is_domain_completion")

    assert "standard_public_projection_policy" not in foundry_series
    assert all(value is False for value in foundry_series["authority_boundary"].values())
    for action in action_catalog["actions"]:
        stage_name = "storyline-architecture" if action["action_id"] == "shape-storyline" else "chapter-production-planning"
        assert action["execution_binding"] == {
            "kind": "stage_binding",
            "stage_manifest_ref": "agent/stages/manifest.json",
        }, action["action_id"]
        assert action["stage_route"]["entry_stage_ref"] == stage_name, action["action_id"]
        assert "source_command" not in action, action["action_id"]
        assert "natural_language_intent" not in action, action["action_id"]
        assert "stage_route_exempt" not in action, action["action_id"]
        assert "handler_binding" not in action, action["action_id"]
        for surface in action["supported_surfaces"].values():
            assert "command" not in surface, action["action_id"]
            assert "surface_kind" not in surface, action["action_id"]
        assert action["authority_boundary"] == {
            "domain_truth_owner": "OPL Book Forge",
            "opl_role": "projection_consumer_only",
            "write_policy": "no_domain_truth_writes",
            "opl_can_write_domain_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_mutate_domain_artifact_body": False,
            "opl_can_authorize_quality_or_export": False,
            "provider_completion_is_domain_completion": False,
        }, action["action_id"]
