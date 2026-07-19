#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_AUTHORITY_FLAGS = {
    "can_write_domain_truth": False,
    "can_sign_owner_receipt": False,
    "can_create_domain_typed_blocker": False,
    "can_authorize_quality_export_publication_or_review_verdict": False,
}

def load_json(ref: str) -> dict[str, Any]:
    return json.loads((REPO_ROOT / ref).read_text(encoding="utf-8"))


def assert_has(actual: list[str], expected: set[str], label: str) -> None:
    missing = expected - set(actual)
    assert not missing, f"{label} missing: {sorted(missing)}"


def main() -> int:
    manifest = load_json("contracts/foundry-agent-os-domain-kernel-manifest.json")
    descriptor = load_json("contracts/domain_descriptor.json")
    pack_compiler_input = load_json("contracts/pack_compiler_input.json")
    package_manifest = load_json("contracts/opl_agent_package_manifest.json")
    plugin_manifest = load_json("plugins/opl-bookforge/.codex-plugin/plugin.json")
    package_metadata = load_json("package.json")
    temporal_policy = load_json("contracts/temporal_stage_run_consumption_policy.json")
    generated_handoff = load_json("contracts/generated_surface_handoff.json")
    functional_audit = load_json("contracts/functional_privatization_audit.json")
    ledger_contract = load_json("contracts/opl_ledger_artifact_registration.json")
    principles = load_json("contracts/standard-agent-principles-adoption.json")
    capability_map = load_json("contracts/capability_map.json")

    assert manifest["surface_kind"] == "foundry_agent_os_domain_kernel_manifest"
    assert manifest["version"] == "foundry-agent-os-domain-kernel-manifest.v1"
    assert manifest["domain_id"] == "opl-bookforge"
    assert manifest["domain_agent_id"] == "obf"
    assert manifest["owner"] == "OPL Book Forge"
    assert manifest["role"] == "w4_domain_kernel_manifest"

    assert pack_compiler_input["canonical_agent_id"] == "obf"
    assert pack_compiler_input["domain_id"] == "opl-bookforge"
    assert package_manifest["agent_id"] == pack_compiler_input["canonical_agent_id"]
    assert package_manifest["package_id"] == pack_compiler_input["canonical_agent_id"]
    assert package_manifest["codex_surface"]["plugin_id"] == "opl-bookforge"
    assert plugin_manifest["name"] == "opl-bookforge"
    assert package_metadata["name"] == "opl-bookforge"
    assert package_metadata["version"] == "0.3.5"
    assert plugin_manifest["version"] == package_metadata["version"]
    assert package_manifest["version"] == package_metadata["version"]
    dependency_profile = descriptor["dependency_profiles"][0]
    package_dependency_profile = package_manifest["dependency_profiles"][0]
    profile_bytes = json.dumps(
        dependency_profile,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    assert "dependencies" not in package_dependency_profile
    assert package_dependency_profile["source_descriptor_ref"] == (
        "contracts/domain_descriptor.json#/dependency_profiles/0"
    )
    assert package_dependency_profile["source_profile_sha256"] == (
        f"sha256:{hashlib.sha256(profile_bytes).hexdigest()}"
    )
    dependency_ids = {
        dependency["dependency_id"] for dependency in dependency_profile["dependencies"]
    }
    assert {
        "FandolSong-Regular.otf",
        "FandolHei-Regular.otf",
        "FandolFang-Regular.otf",
    } <= dependency_ids
    assert functional_audit["retired_default_surface_ids"] == [
        "cli",
        "mcp",
        "skill",
        "product_entry",
        "product_status",
        "product_session",
        "domain_handler",
        "workbench",
    ]
    assert functional_audit["default_surface_boundary"] == {
        "state": "physically_absent",
        "owner": "one-person-lab",
        "domain_repo_can_own_default_surface": False,
        "no_resurrection_policy": (
            "generated_or_hosted_by_opl_only_do_not_restore_repo_local_default_surfaces"
        ),
    }
    assert generated_handoff["surface_kind"] == "opl_generated_surface_handoff_delta"
    assert (
        generated_handoff["defaults_profile"]
        == "opl.standard-generated-surface-handoff.v1"
    )
    assert "generated_surfaces" not in generated_handoff
    assert "handoff_surfaces" not in generated_handoff
    assert (
        functional_audit["defaults_profile"]
        == "opl.standard-functional-privatization-audit.v1"
    )
    assert "classification_policy" not in functional_audit
    assert "forbidden_generic_owner_roles" not in functional_audit
    assert "private_functional_surface_admission_policy_ref" not in functional_audit
    assert "private_functional_surface_admission_policy" not in functional_audit
    morphology = functional_audit["physical_source_morphology_policy"]
    assert morphology["policy_id"] == "opl-bookforge.physical-source-morphology.v1"
    assert morphology["authority_boundary"] == {
        "domain_can_claim_generic_runtime_owner": False,
        "domain_repo_can_own_generated_surface": False,
    }
    assert not (REPO_ROOT / "contracts/private_functional_surface_policy.json").exists()
    assert "contracts/private_functional_surface_policy.json" not in json.dumps(manifest)
    assert "contracts/private_functional_surface_policy.json" not in json.dumps(principles)
    assert "contracts/functional_privatization_audit.json" in manifest["source_of_truth_refs"]
    assert "contracts/functional_privatization_audit.json" in manifest["verification"]["source_contract_refs"]
    assert manifest["verification"]["validator_refs"] == [
        "python3 -m json.tool contracts/foundry-agent-os-domain-kernel-manifest.json",
        "opl agents check --repo <repo-dir> --json",
    ]
    for capability in capability_map["capabilities"]:
        assert "opl agents check --repo <repo-dir> --json" in capability["verification_refs"]
        assert all("agents scaffold --validate" not in ref for ref in capability["verification_refs"])
    assert all("bridge_exit_gate" not in module for module in functional_audit["modules"])
    assert "distribution_payload" not in package_manifest
    implementation_profile = pack_compiler_input["implementation_profile"]
    assert implementation_profile == {
        "profile_id": "opl.standard_domain_agent.v1",
        "agent_identity": "declarative_standard_agent_pack",
        "pack_formats": ["markdown", "json"],
        "helpers": {
            "optional": True,
            "entries": [
                {
                    "language": "python",
                    "role": "native_helper",
                    "source_roots": ["runtime/native_helpers/"],
                },
            ],
            "language_is_identity": False,
            "rust_policy": "framework_hot_path_only",
        },
        "generated_surfaces_owner": "one-person-lab",
    }
    assert pack_compiler_input["reference_implementation"] == {
        "role": "golden_fixture_reference",
        "is_standard_owner": False,
        "standard_owner": "one-person-lab",
        "can_define_standard_agent_identity": False,
        "can_define_framework_contract": False,
        "default_runtime_caller": False,
        "golden_fixture_refs": ["tests/", "docs/evidence/"],
        "golden_fixture_is_second_standard_source": False,
    }
    for helper in implementation_profile["helpers"]["entries"]:
        assert helper["language"] == "python"
        assert helper["role"] == "native_helper"
        assert helper["source_roots"] == ["runtime/native_helpers/"]
        assert all((REPO_ROOT / ref).is_dir() for ref in helper["source_roots"])
    assert descriptor["authority_boundary"]["domain_owns_truth_quality_artifact_memory_and_receipts"] is True
    standard_interface = descriptor["standard_agent_interface"]
    assert standard_interface["version"] == "opl_standard_agent_interface.v1"
    assert standard_interface["workspace_binding"] == {
        "locator_surface_kind": "opl_bookforge_workspace",
        "default_profile_id": "one_off",
        "workspace_kind": "book_authoring_workspace",
        "project_kind": "book_project",
        "project_collection_label": "books",
        "default_workspace_id": "bookforge-workspace",
        "default_project_id": "book-001",
        "required_locator_fields": ["workspace_root"],
        "optional_locator_fields": [],
    }
    assert standard_interface["stage_catalog"] == {
        "source_kind": "agent_repo_relative_json",
        "relative_path": "agent/stages/manifest.json",
        "items_pointer": "/stages",
        "field_map": {
            "stage_id": "stage_id",
            "display_name": "title",
            "display_names": "display_names",
        },
    }
    assert set(standard_interface["runtime"]) == {"runtime_domain_id", "registration_ref"}
    assert standard_interface["progress"]["deliverable_delta_aliases"] == [
        "book_manuscript_progress_delta"
    ]
    assert temporal_policy["stage_run_owner"] == "one-person-lab"
    assert generated_handoff["temporal_stage_run_projection"]["owner"] == "one-person-lab"
    assert ledger_contract["refs_only"] is True

    default_read_root = manifest["default_read_root"]
    assert default_read_root["surface"] == "current_owner_delta"
    assert default_read_root["ordinary_operator_root"] is True
    assert default_read_root["provider_completion_role"] == "transport_evidence_only"
    assert default_read_root["ledger_registration_role"] == "refs_only_visibility_not_owner_answer"
    assert default_read_root["projection_can_be_owner_answer"] is False

    kernel = manifest["domain_authority_kernel"]
    assert_has(
        kernel["retained_surfaces"],
        {
            "book_truth",
            "manuscript_truth",
            "source_reference_judgment",
            "style_policy_and_memory_accept_reject_or_blocker",
            "publication_proof_verdict",
            "final_export_authority",
            "owner_receipt_signer",
            "typed_blocker_materializer",
        },
        "retained_surfaces",
    )
    assert kernel["retained_surface_owner"] == "opl-bookforge"
    assert kernel["owner_receipt_signer"] == "opl-bookforge_authority_kernel"
    assert kernel["typed_blocker_signer"] == "opl-bookforge_authority_kernel"
    assert_has(
        kernel["quality_export_publication_review_verdict_signers"],
        {
            "source_reference_judgment",
            "manuscript_quality_verdict",
            "publication_proof_verdict",
            "final_export_authority",
        },
        "quality/export verdict signers",
    )
    assert_has(
        kernel["accepted_answer_shapes"],
        {
            "obf_owner_receipt_ref",
            "obf_typed_blocker_ref",
            "source_reference_verdict_ref",
            "publication_proof_ref",
            "final_export_handoff_ref",
            "human_gate_ref",
            "route_back_ref",
        },
        "accepted_answer_shapes",
    )

    assert_has(
        manifest["opl_upcollect_surfaces"],
        {
            "stage_run_kernel",
            "pack_compiler",
            "workspace_locator_shell",
            "opl_ledger_artifact_registration_shell",
            "generated_cli_mcp_skill_product_workbench_surfaces",
            "session_transport",
            "workbench_status_session_transport",
            "console_current_owner_delta_projection",
        },
        "opl_upcollect_surfaces",
    )

    for surface, flags in manifest["forbidden_authority_flags"].items():
        assert flags == FORBIDDEN_AUTHORITY_FLAGS, surface

    assert manifest["non_claims"] == {
        "domain_ready": False,
        "runtime_ready": False,
        "book_ready": False,
        "manuscript_ready": False,
        "review_pdf_ready": False,
        "publication_ready": False,
        "publication_proof_ready": False,
        "final_export_ready": False,
        "owner_acceptance": False,
        "production_ready": False,
        "app_release_ready": False,
        "physical_delete_authorized": False,
    }

    print(json.dumps({
        "status": "passed",
        "test": "foundry_agent_os_domain_kernel_manifest_contract",
        "contract": "contracts/foundry-agent-os-domain-kernel-manifest.json",
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
