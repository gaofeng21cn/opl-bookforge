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


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    policy = load_json(repo, "contracts/temporal_stage_run_consumption_policy.json")
    action_catalog = load_json(repo, "contracts/action_catalog.json")
    foundry_series = load_json(repo, "contracts/foundry_agent_series.json")
    generated_handoff = load_json(repo, "contracts/generated_surface_handoff.json")
    stage_run_profile = load_json(repo, "contracts/stage_run_kernel_profile.json")

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

    public_projection = foundry_series["standard_public_projection_policy"]
    assert public_projection["standard_public_foundry_surface"] == "opl_generated_hosted_series"
    assert public_projection["active_public_projection_allows_non_opl_foundry_cli"] is False
    assert public_projection["active_public_projection_allows_domain_owned_cli_as_standard_surface"] is False
    assert public_projection["active_public_projection_allows_forbidden_surface_roles"] is False
    assert public_projection["active_public_projection_allows_compatibility_aliases"] is False
    assert public_projection["active_public_projection_allows_legacy_json_aliases"] is False
    for action in action_catalog["actions"]:
        boundary = action["authority_boundary"]
        assert boundary["provider_completion_is_domain_completion"] is False, action["action_id"]
        assert boundary["domain_repo_can_own_temporal_runtime"] is False, action["action_id"]
        assert boundary["bookforge_can_write_opl_stage_attempts"] is False, action["action_id"]
        assert boundary["temporal_attempt_ledger_owner"] == "one-person-lab", action["action_id"]
        assert_closeout_refs(boundary["domain_completion_ref_fields"], f"action {action['action_id']}")
        assert boundary["completion_audit_policy_ref"] == "contracts/temporal_stage_run_consumption_policy.json#completion_audit", action["action_id"]
        assert set(boundary["completion_accounts"]) == COMPLETION_ACCOUNTS, action["action_id"]
        assert set(boundary["false_completion_accounts"]) == FALSE_COMPLETION_ACCOUNTS, action["action_id"]

    assert generated_handoff["temporal_stage_run_consumption_policy_ref"] == "contracts/temporal_stage_run_consumption_policy.json"
    projection = generated_handoff["temporal_stage_run_projection"]
    assert projection["owner"] == "one-person-lab"
    assert projection["provider_completion_is_domain_completion"] is False
    assert projection["generated_surface_ready_counts_as_domain_ready"] is False
    assert projection["domain_repo_can_own_temporal_runtime"] is False
    assert projection["bookforge_can_write_opl_stage_attempts"] is False
    assert projection["temporal_attempt_ledger_owner"] == "one-person-lab"
    assert_closeout_refs(projection["domain_completion_ref_fields"], "generated handoff projection")
    assert_surface_export_boundary(projection, "generated handoff projection")

    assert stage_run_profile["temporal_stage_run_consumption_policy_ref"] == "contracts/temporal_stage_run_consumption_policy.json"
    embedded_policy = stage_run_profile["temporal_stage_run_consumption_policy"]
    assert embedded_policy["temporal_attempt_ledger_owner"] == "one-person-lab"
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

    print(json.dumps({
        "status": "passed",
        "test": "temporal_stage_run_consumption_policy",
        "contract": "contracts/temporal_stage_run_consumption_policy.json"
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
