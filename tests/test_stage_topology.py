#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


STAGE_SEQUENCE = [
    "storyline-architecture",
    "chapter-production-planning",
    "chapter-materialization",
    "source-style-integrity-review",
    "publication-proof-handoff",
]
ACTION_STAGE_ROUTES = {
    "shape-storyline": ["storyline-architecture"],
    "materialize-book": STAGE_SEQUENCE[1:],
}
GENERATED_STAGE_PLANE_REF = "opl_generated:product_entry_manifest#/family_stage_control_plane/stages"
STAGE_PROJECTION_CAPABILITIES = {
    "opl-bookforge.storyline-architecture.stage_prompt": "family_stage_control_plane_prompt_refs",
    "opl-bookforge.story-style-architect.professional_skill": "family_stage_control_plane_skill_refs",
    "opl-bookforge.chapter-author.professional_skill": "family_stage_control_plane_skill_refs",
    "opl-bookforge.source-reference-reviewer.professional_skill": "family_stage_control_plane_skill_refs",
    "opl-bookforge.meta-reviewer.professional_skill": "family_stage_control_plane_skill_refs",
    "opl-bookforge.publication-memory-curator.professional_skill": "family_stage_control_plane_skill_refs",
    "opl-bookforge.domain-boundary.knowledge_pack": "family_stage_control_plane_knowledge_refs",
}
STAGE_PROMPT_SEMANTICS = {
    "storyline-architecture": ["reader", "author/source stance", "chapter function", "owner handoff"],
    "chapter-production-planning": ["approved storyline", "task cards", "incremental", "route-back"],
    "chapter-materialization": ["chapter Markdown", "target extent", "integrity verdict", "route-back"],
    "source-style-integrity-review": ["materialized manuscript", "evidence classes", "repair route", "integrity handoff"],
    "publication-proof-handoff": ["review_pdf", "publication_proof", "final_export", "owner/export acceptance"],
}
IMMUTABLE_PROVENANCE_ROOTS = ("docs/evidence/", "docs/history/")
TEXT_SUFFIXES = {".json", ".md", ".py", ".sh"}
FOUNDRY_SERIES_CONSUMER_REFS = {
    "canonical_policy_export": "opl-framework/foundry-agent-series-policy",
    "canonical_series_contract_ref": "contracts/opl-framework/foundry-agent-series-contract.json",
    "canonical_skeleton_contract_ref": "contracts/opl-framework/standard-domain-agent-skeleton-contract.json",
}
FOUNDRY_POLICY_FINGERPRINT = "sha256:30a1d0034eeafbf5ea042fc33c64af585c3e68276328eb97d20903105087bb5d"
LEGACY_FOUNDRY_POLICY_BODY_FIELDS = {
    "agent_membership_projection_policy",
    "app_projection_policy",
    "contract_version_policy",
    "domain_adapter_policy",
    "required_identity_fields",
    "required_stage_packets",
    "series_design_profile",
    "shared_progress_projection_fields",
    "standard_feedback_self_evolution_trigger_policy",
    "standard_public_projection_policy",
    "workspace_topology_profile",
}


def load_json(repo: Path, ref: str) -> dict:
    return json.loads((repo / ref).read_text(encoding="utf-8"))


def assert_no_retired_stage_refs(repo: Path) -> None:
    retired_stage = "-".join(("book", "materialization"))
    stale_refs: list[str] = []
    roots = [
        repo / "README.md",
        repo / "README.zh-CN.md",
        repo / "agent",
        repo / "contracts",
        repo / "docs",
        repo / "runtime",
        repo / "scripts",
        repo / "tests",
    ]
    for root in roots:
        files = [root] if root.is_file() else root.rglob("*")
        for path in files:
            if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
                continue
            rel = str(path.relative_to(repo))
            if rel.startswith(IMMUTABLE_PROVENANCE_ROOTS):
                continue
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if retired_stage in line:
                    stale_refs.append(f"{rel}:{line_number}")
    assert not stale_refs, stale_refs


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    stage_manifest = load_json(repo, "agent/stages/manifest.json")
    stage_operating_principles = load_json(repo, "contracts/stage_operating_principles.json")
    principles = load_json(repo, "contracts/standard-agent-principles-adoption.json")
    action_catalog = load_json(repo, "contracts/action_catalog.json")
    capability_map = load_json(repo, "contracts/capability_map.json")
    pack_compiler_input = load_json(repo, "contracts/pack_compiler_input.json")
    kernel_adoption = load_json(repo, "contracts/stage_artifact_kernel_adoption.json")
    closeout = load_json(repo, "contracts/stage_decomposition_closeout.json")
    foundry_series = load_json(repo, "contracts/foundry_agent_series.json")
    golden_path = load_json(repo, "contracts/golden_path_profile.json")

    manifest_stages = stage_manifest["stages"]
    assert [stage["stage_id"] for stage in manifest_stages] == STAGE_SEQUENCE
    assert len({stage["goal"] for stage in manifest_stages}) == len(STAGE_SEQUENCE)
    for stage in manifest_stages:
        prompt = (repo / stage["prompt_ref"]).read_text(encoding="utf-8")
        for semantic in STAGE_PROMPT_SEMANTICS[stage["stage_id"]]:
            assert semantic.lower() in prompt.lower(), (stage["stage_id"], semantic)
        assert "two or three" not in prompt.lower()
    assert not (repo / "contracts/stage_control_plane.json").exists()
    assert not (repo / "contracts/stage_native_artifact_contract.json").exists()
    assert not (repo / "contracts/stage_native_artifacts").exists()
    assert pack_compiler_input["standard_stage_pack_conformance"]["enforcement_ref"] == (
        "agent/stages/manifest.json"
    )
    assert kernel_adoption["domain_pack_binding"]["accepted_source_refs"] == [
        "agent/stages/manifest.json",
        "/product_entry_manifest/family_stage_control_plane",
        "contracts/foundry_agent_series.json",
    ]
    assert "contracts/stage_control_plane.json" not in json.dumps(capability_map)
    capabilities = {entry["capability_id"]: entry for entry in capability_map["capabilities"]}
    for capability_id, role in STAGE_PROJECTION_CAPABILITIES.items():
        assert capabilities[capability_id]["runtime_projection_refs"] == [{
            "ref_kind": "external_capability_ref",
            "ref": GENERATED_STAGE_PLANE_REF,
            "role": role,
        }]
    assert "stage_decomposition_pack_draft" not in closeout
    assert "agent/stages/manifest.json" in closeout["closeout_refs"]
    assert "opl-generated:family_stage_control_plane" in closeout["closeout_refs"]
    assert "stage_native_artifact_contract" not in json.dumps(closeout)
    assert foundry_series["surface_kind"] == "opl_foundry_agent_series_consumer"
    assert foundry_series["version"] == "foundry-agent-series-consumer.v1"
    for field, expected in FOUNDRY_SERIES_CONSUMER_REFS.items():
        assert foundry_series[field] == expected
    assert foundry_series["foundry_agent_id"] == "opl-bookforge"
    assert foundry_series["stage_manifest_ref"] == "agent/stages/manifest.json"
    assert foundry_series["stage_control_plane_ref"] == "opl-generated:family_stage_control_plane"
    assert foundry_series["shared_policy_release"]["policy_bundle_fingerprint"] == (
        FOUNDRY_POLICY_FINGERPRINT
    )
    assert not (LEGACY_FOUNDRY_POLICY_BODY_FIELDS & foundry_series.keys())
    assert foundry_series["authority_boundary"]
    assert all(value is False for value in foundry_series["authority_boundary"].values())
    assert "stage_native_artifact_contract" not in json.dumps(foundry_series)
    assert "-".join(("book", "materialization")) not in json.dumps(closeout)
    assert principles["source_refs"]["stage_manifest_ref"] == "agent/stages/manifest.json"
    assert principles["domain_mapping"]["domain_intake"]["domain_stage_ref"] == (
        "agent/stages/manifest.json#/stages/0"
    )
    assert principles["domain_mapping"]["domain_intake"]["stage_id"] == "storyline-architecture"
    assert principles["domain_mapping"]["domain_intake"]["prompt_ref"] == (
        "agent/prompts/storyline-architecture.md"
    )
    assert not (repo / "agent/prompts/domain_intake.md").exists()
    assert not (repo / "agent/stages/domain_intake.md").exists()
    publication_proof = next(
        stage for stage in manifest_stages if stage["stage_id"] == "publication-proof-handoff"
    )
    assert publication_proof["lane_kind"] == "variant"
    manifest_policy = stage_manifest["progress_first_policy"]
    operating_speed_policy = stage_operating_principles["speed_policy"]
    assert manifest_policy["route_selection_owner"] == "codex_cli"
    assert manifest_policy["codex_may_advance_skip_repeat_reverse_or_route_back"] is True
    assert manifest_policy["any_declared_stage_may_start_from_any_prior_stage_result"] is True
    assert manifest_policy["declared_requires_are_quality_context_not_launch_gates"] is True
    assert manifest_policy["next_stage_refs_are_recommendations_not_constraints"] is True
    assert manifest_policy["no_output_or_failure_diagnostic_advances_stage"] is True
    for field in (
        "route_selection_owner",
        "codex_may_advance_skip_repeat_reverse_or_route_back",
        "any_declared_stage_may_start_from_any_prior_stage_result",
        "declared_requires_are_quality_context_not_launch_gates",
        "next_stage_refs_are_recommendations_not_constraints",
    ):
        assert operating_speed_policy[field] == manifest_policy[field]
    declared_stage_ids = {stage["stage_id"] for stage in manifest_stages}
    assert all(set(stage["next_stage_refs"]) <= declared_stage_ids for stage in manifest_stages)

    planning = manifest_stages[1]
    progress_policy = planning["stage_contract"]["progress_first_policy"]
    assert progress_policy["ordinary_gap_outcome"] == "completed_with_quality_debt_or_route_back"
    assert progress_policy["next_forced_delta_required_for_in_progress"] is False
    assert progress_policy["ordinary_gap_can_emit_generic_typed_blocker"] is False
    assert progress_policy["independent_review_required_for_ordinary_transition"] is True
    assert planning["stage_contract"]["transition_policy"]["ordinary_transition_requires_independent_review"] is True
    planning_refs = set(planning["ensures"])
    assert "independent-gate-receipt-ref:chapter-production-planning" in planning_refs
    assert "owner-handoff-ref:storyline-architecture" in planning["requires"]
    assert "storyline-admission-ref:chapter-production-planning" in planning["ensures"]
    assert "planning-progress-ref:chapter-production-planning" in planning["ensures"]
    assert "active-production-queue-ref:chapter-production-planning" in planning["ensures"]
    assert "chapter-task-card-bundle-ref:chapter-production-planning" in planning["ensures"]
    assert "independent-gate-receipt-ref:chapter-production-planning" in planning["ensures"]
    canary = load_json(repo, "contracts/stage_run_canary_evidence.json")
    assert "strategy_retrospective" in canary["strategy_trace"]
    assert "meta_review_learning" not in canary["strategy_trace"]
    assert "strategy_retrospective_ref" in canary["role_artifact_refs"]
    assert "meta_review_ref" not in canary["role_artifact_refs"]

    materialization = manifest_stages[2]
    assert "chapter-task-card-bundle-ref:chapter-production-planning" in materialization["requires"]
    assert "chapter-draft-bundle-ref:chapter-materialization" in materialization["ensures"]
    assert "chapter-markdown-ref:chapter-materialization/{chapter_id}" in materialization["ensures"]
    assert "review-pdf-eligibility-ref:chapter-materialization" in materialization["ensures"]

    actions = {action["action_id"]: action for action in action_catalog["actions"]}
    assert set(actions) == set(ACTION_STAGE_ROUTES)
    for action_id, action in actions.items():
        allowed_stage_refs = [
            stage["stage_id"]
            for stage in manifest_stages
            if action_id in stage["allowed_action_refs"]
        ]
        if action["effect"] == "read_only":
            assert "stage_route" not in action
            assert allowed_stage_refs
            continue
        assert action["effect"] == "mutating"
        required_stage_refs = ACTION_STAGE_ROUTES[action_id]
        assert allowed_stage_refs == required_stage_refs
        assert action["stage_route"] == {
            "entry_stage_ref": required_stage_refs[0],
            "required_stage_refs": required_stage_refs,
            "optional_stage_refs": [],
            "terminal_stage_refs": [required_stage_refs[-1]],
            "route_policy": "ai_selected_progress_route",
        }
        assert action["execution_binding"] == {
            "kind": "stage_binding",
            "stage_manifest_ref": "agent/stages/manifest.json",
        }
        assert "source_command" not in action
        assert "stage_route_exempt" not in action
        assert "handler_binding" not in action
        for surface in action["supported_surfaces"].values():
            assert "command" not in surface
            assert "surface_kind" not in surface

    materialize = actions["materialize-book"]
    assert actions["shape-storyline"]["natural_language_intent"] != materialize["natural_language_intent"]
    assert "without drafting or exporting" in actions["shape-storyline"]["natural_language_intent"]
    assert "incremental chapter planning" in materialize["natural_language_intent"]
    assert materialize["stage_route"]["entry_stage_ref"] == "chapter-production-planning"
    assert materialize["human_gate_ids"] == ["chapter_planning_owner_review"]

    assert golden_path["ordinary_path"]["stage_refs"] == ["storyline-architecture"]
    assert golden_path["ordinary_path"]["follow_on_stage_refs"] == STAGE_SEQUENCE[1:]
    assert golden_path["explicit_variants"][0]["stage_refs"] == STAGE_SEQUENCE[1:]

    retired_stage = "-".join(("book", "materialization"))
    for ref in (
        f"agent/prompts/{retired_stage}.md",
        f"agent/stages/{retired_stage}.md",
        f"agent/quality_gates/{retired_stage}-quality-gate.md",
    ):
        assert not (repo / ref).exists(), ref
    assert_no_retired_stage_refs(repo)

    primary_skill = (repo / "agent/primary_skill/SKILL.md").read_text(encoding="utf-8")
    carrier_skill = (repo / "plugins/opl-bookforge/skills/opl-bookforge/SKILL.md").read_text(
        encoding="utf-8"
    )
    assert primary_skill == carrier_skill
    assert "two or three whole-book core models" not in primary_skill.lower()

    print(json.dumps({"status": "passed", "stage_sequence": STAGE_SEQUENCE}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
