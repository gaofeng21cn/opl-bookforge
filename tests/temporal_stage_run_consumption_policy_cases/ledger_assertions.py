from __future__ import annotations

from typing import Any

from temporal_stage_run_consumption_policy_cases.evidence_assertions import assert_ref_fields


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


def assert_no_forbidden_keys(payload: Any, forbidden: set[str], label: str) -> None:
    if isinstance(payload, dict):
        present = forbidden & set(payload)
        assert not present, f"{label} includes forbidden keys: {present}"
        for value in payload.values():
            assert_no_forbidden_keys(value, forbidden, label)
    elif isinstance(payload, list):
        for value in payload:
            assert_no_forbidden_keys(value, forbidden, label)


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
    assert generated_handoff["surface_kind"] == "opl_generated_surface_handoff_delta"
    assert generated_handoff["defaults_profile"] == "opl.standard-generated-surface-handoff.v1"
    assert generated_handoff["generated_surface_owner"] == "one-person-lab"
    assert generated_handoff["domain_repo_can_own_generated_surface"] is False
    assert "generated_surfaces" not in generated_handoff
    assert "handoff_surfaces" not in generated_handoff
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

    generated_surface_ids = {item["surface_id"] for item in generated_handoff["generated_surface_overrides"]}
    handoff_surface_ids = {item["surface_id"] for item in generated_handoff["handoff_surface_overrides"]}
    assert "opl_ledger_artifact_registration" not in generated_surface_ids
    assert "opl_ledger_artifact_registration" not in handoff_surface_ids
