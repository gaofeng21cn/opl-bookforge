from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from temporal_stage_run_consumption_policy_cases.policy_assertions import load_json


PRIVATE_PLATFORM_RETIREMENT_SURFACES = {
    "publication_and_export_helper",
    "image_asset_helper",
    "runtime_session_update_absence",
}

PRIVATE_PLATFORM_NATIVE_HELPER_MODULES = {
    "opl-bookforge.publication-and-export-helper",
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
        "source_closure_effects": {
            ("image_refs_from_pandoc_ast", "process_spawn"),
            ("compile_pdf", "process_spawn"),
            ("render_pdf_pages", "process_spawn"),
            ("compile_pdf", "filesystem_write"),
            ("render_pdf_pages", "filesystem_write"),
        },
    },
    "runtime/native_helpers/bookforge_imagegen_asset.native-helper-probe.json": {
        "helper_id": "opl-bookforge.imagegen-asset",
        "entrypoint_ref": "bookforge_imagegen_asset.py",
        "required_commands": [],
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


def assert_opl_default_hygiene_and_probe_consumption(repo: Path) -> None:
    workspace_policy = load_json(repo, "contracts/workspace_lifecycle_policy.json")
    guard = workspace_policy["byproduct_policy"]["repo_source_byproduct_guard"]
    assert guard["guard_surface"] == "opl_repo_source_byproduct_guard"
    assert guard["guard_owner"] == "one-person-lab"
    assert guard["guard_command"] == "opl workspace source-hygiene --source-root <repo> --json"

    verify_script = (repo / "scripts/verify.sh").read_text(encoding="utf-8")
    assert verify_script.count('workspace source-hygiene --source-root "${repo_dir}" --json') == 1
    assert 'case "${lane}" in' in verify_script
    assert "default|fast)" in verify_script
    assert "structural)" in verify_script
    assert "helpers)" in verify_script
    assert "pdf-smoke|pdf)" in verify_script
    assert "full-local)" in verify_script
    assert "full)" in verify_script
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
        if "source_closure_effects" in expected:
            effect_slots = descriptor["source_closure"]["effect_slots"]
            assert {(slot["symbol"], slot["effect_kind"]) for slot in effect_slots} == expected[
                "source_closure_effects"
            ], descriptor_ref
            source_path = (repo / descriptor_ref).parent / descriptor["entrypoint_ref"]
            source_digest = f"sha256:{hashlib.sha256(source_path.read_bytes()).hexdigest()}"
            assert {slot["source_digest"] for slot in effect_slots} == {source_digest}, descriptor_ref
            for slot in effect_slots:
                if slot["effect_kind"] == "process_spawn":
                    assert slot["target_policy"] == "declared_command_set", slot
                    assert slot["allowed_targets"], slot
                    assert set(slot["allowed_targets"]) <= set(descriptor["required_commands"]), slot
                    assert not {"codex", "opl"} & set(slot["allowed_targets"]), slot
                else:
                    assert slot["effect_kind"] == "filesystem_write", slot
                    assert slot["target_policy"] == "declared_artifact_write_slot", slot
                    assert slot["allowed_targets"] == [], slot
        else:
            assert "source_closure" not in descriptor, descriptor_ref
        command = f'pack native-helper probe --descriptor "${{repo_dir}}/{descriptor_ref}" --json'
        assert command in verify_script, descriptor_ref


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
    assert image["replacement_opl_primitive"] == "opl_hosted_image_generation_output_injection"
    assert image["retirement_action"] == "retain_as_read_only_figure_authority_handler"
    assert image["physical_delete_authorized"] is False
    assert "api_key_or_base_url_owner" in image["forbidden_domain_repo_roles"]
    assert "runtime_queue_owner" in image["forbidden_domain_repo_roles"]
    assert "executor_request_builder" in image["forbidden_domain_repo_roles"]
    assert "artifact_manifest_persistence_owner" in image["forbidden_domain_repo_roles"]

    absent = by_surface["runtime_session_update_absence"]
    assert absent["current_paths"] == []
    assert absent["retirement_action"] == "keep_absent_and_fail_closed_if_reintroduced"
    assert absent["active_caller_boundary"] == "no_repo_local_runtime_session_update_or_workbench_default_caller"
    assert "package_update_manager" in absent["forbidden_domain_repo_roles"]

    modules = {module["module_id"]: module for module in functional_audit["modules"]}
    assert "opl-bookforge.generated-wrapper-handler-targets" not in modules
    assert "opl-bookforge.domain-handler-target" not in modules
    stage_bindings = modules["opl-bookforge.declarative-stage-action-bindings"]
    assert stage_bindings["classification"] == "declarative_pack"
    assert stage_bindings["migration_class"] == "declarative_pack"
    assert stage_bindings["code_paths"] == ["contracts/action_catalog.json", "agent/stages/manifest.json"]
    authority_policy = modules["opl-bookforge.authority-function-policy"]
    assert authority_policy["classification"] == "declarative_pack"
    assert authority_policy["active_caller_status"] == "declarative_authority_policy_only_no_runtime_entry"
    assert PRIVATE_PLATFORM_NATIVE_HELPER_MODULES <= set(modules)
    for module_id in PRIVATE_PLATFORM_NATIVE_HELPER_MODULES:
        module = modules[module_id]
        assert module["classification"] == "native_helper_implementation", module_id
        assert module["semantic_equivalence_status"] == "cleared_by_boundary", module_id
        assert module["audit_visibility"] == "hidden_by_default", module_id
        assert module["no_forbidden_write_evidence_ref"], module_id
    image_module = modules["opl-bookforge.image-asset-helper"]
    assert image_module["classification"] == "minimal_authority_function"
    assert image_module["migration_class"] == "minimal_authority_function"
    assert image_module["receipt_schema_ref"] == "contracts/image_asset_host_handoff.json"
    assert image_module["active_caller_status"] == "read_only_domain_handler_registered"
    assert image_module["active_callers"] == [
        "OPL hosted image output handler_ref invocation",
        "OPL pack native-helper diagnostic probe",
    ]
    assert image_module["no_forbidden_write_evidence_ref"] == "contracts/image_asset_host_handoff.json#/forbidden_domain_effects"

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
