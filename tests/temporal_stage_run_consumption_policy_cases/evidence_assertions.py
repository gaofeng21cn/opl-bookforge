from __future__ import annotations

from typing import Any


LIVE_STAGE_RUN_PROGRESS_ACCEPTED_STATUSES = {
    "owner_evidence_required",
}

LIVE_STAGE_RUN_PROGRESS_REF_FIELDS = {
    "typed_blocker_refs",
    "quality_or_export_receipt_refs",
    "superseded_topology_provenance_refs",
    "topology_guard_refs",
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

def assert_ref_fields(fields: list[str] | tuple[str, ...], expected: set[str], label: str) -> None:
    actual = set(fields)
    assert expected <= actual, f"{label} missing required refs: {expected - actual}"


def assert_live_stage_run_progress_evidence(payload: dict[str, Any]) -> None:
    assert payload["surface_kind"] == "domain_live_stage_run_progress_evidence"
    assert payload["domain_id"] == "opl-bookforge"
    assert payload["owner"] == "OPL Book Forge"
    assert payload["status"] in LIVE_STAGE_RUN_PROGRESS_ACCEPTED_STATUSES
    assert payload["status"] == "owner_evidence_required"
    assert payload["evidence_contract_status"] == "standard_contract_resolved_without_accepted_refs"
    assert payload["topology_state"] == "historical_two_stage_evidence_superseded_by_current_five_stage_topology"
    assert payload["active_stage_sequence"] == [
        "storyline-architecture",
        "chapter-production-planning",
        "chapter-materialization",
        "source-style-integrity-review",
        "publication-proof-handoff",
    ]
    assert payload["evidence_gap_kind"] == "current_topology_live_evidence_required"
    assert "typed_blocker_kind" not in payload

    refs = payload["refs"]
    assert LIVE_STAGE_RUN_PROGRESS_REF_FIELDS <= set(refs), "live StageRun progress evidence missing ref groups"
    assert refs["typed_blocker_refs"] == []
    assert refs["quality_or_export_receipt_refs"] == []
    assert_ref_fields(
        refs["superseded_topology_provenance_refs"],
        {
            "docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/README.md",
            "docs/evidence/oma-agent-lab/provenance/baseline_delivery_receipt.json",
            "docs/evidence/oma-agent-lab/provenance/stage_decomposition_attempt_receipt.json",
        },
        "superseded topology provenance refs",
    )
    assert_ref_fields(
        refs["topology_guard_refs"],
        {
            "contracts/temporal_stage_run_consumption_policy.json#completion_boundary",
            "contracts/temporal_stage_run_consumption_policy.json#completion_audit.acceptance_tail",
        },
        "live StageRun topology guard refs",
    )
    assert_ref_fields(
        refs["next_verification_command_refs"],
        {
            "python3 tests/test_stage_topology.py",
            "python3 tests/test_temporal_stage_run_consumption_policy.py",
            "./scripts/verify.sh",
        },
        "live StageRun verification refs",
    )

    evidence_items = payload["deferred_stage_evidence_items"]
    assert len(evidence_items) == 5, evidence_items
    assert [item["stage_id"] for item in evidence_items] == payload["active_stage_sequence"]
    assert {item["result_shape"] for item in evidence_items} == {"live_evidence_deferred"}
    assert {item["status"] for item in evidence_items} == {
        "deferred_topology_superseded_no_current_live_evidence"
    }

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
