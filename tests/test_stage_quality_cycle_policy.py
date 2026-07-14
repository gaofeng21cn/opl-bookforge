import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_bookforge_declares_explicit_review_policy_for_each_stage() -> None:
    manifest = read_json("agent/stages/manifest.json")
    profile = read_json("contracts/stage_quality_cycle_policy.json")
    expected_review_policy = {
        "storyline-architecture": (True, 3),
        "chapter-production-planning": (True, 3),
        "chapter-materialization": (True, 3),
        "source-style-integrity-review": (False, 0),
        "publication-proof-handoff": (True, 3),
    }

    assert manifest["quality_governance_profile_ref"] == "contracts/opl-framework/official-knowledge-deliverable-quality-profile.json"
    assert manifest["meta_review_policy_ref"] == "contracts/stage_quality_cycle_policy.json#/meta_review_policy"
    assert profile["framework_contract_ref"] == "contracts/opl-framework/stage-quality-cycle-contract.json"
    assert profile["route_selection_contract_ref"] == (
        "contracts/opl-framework/stage-quality-cycle-contract.json"
        "#/cross_stage_route_selection"
    )
    assert profile["review_attempt_contract"]["new_stage_attempt_per_role"] is True
    assert profile["review_attempt_contract"]["new_execution_session_per_attempt"] is True
    assert profile["review_attempt_contract"]["no_context_inheritance"] is True
    assert profile["review_attempt_contract"]["same_thread_resume_counts_as_review"] is False
    assert profile["review_attempt_contract"]["route_authority_contract"] == {
        "semantic_route_decision_owner": "decisive_codex_attempt",
        "stage_transition_materialization_owner": "opl_stage_run_controller",
        "primary_only_decisive_attempt_role": "producer",
        "formal_review_decisive_attempt_roles": ["reviewer", "re_reviewer"],
        "repairer_can_be_decisive_attempt": False,
        "repair_required_with_budget_remaining_route_output": (
            "route_impact.stage_route_recommendation"
        ),
        "repair_required_without_budget_and_consumable_artifact_route_output": (
            "route_impact.stage_route_decision"
        ),
        "repair_budget_exhaustion_terminal_status": "completed_with_quality_debt",
        "hard_stop_or_zero_consumable_artifact_route_output": "none",
    }
    assert profile["review_attempt_contract"]["attempt_output_contract"] == {
        "envelope_path": "route_impact.stage_quality_cycle",
        "outcome_field": "outcome",
        "outcome_required_for_roles": ["reviewer", "re_reviewer"],
        "outcome_values": [
            "pass", "repair_required", "quality_debt", "blocked", "human_gate",
        ],
        "attempts_must_not_emit_receipt_verdict": True,
        "receipt_materializer_owner": "opl_stage_run_controller",
        "review_receipt_verdict_mapping": {
            "pass": "pass",
            "repair_required": "repair_required",
            "quality_debt": "quality_debt",
            "blocked": "hard_stop",
            "human_gate": "hard_stop",
        },
    }
    assert set(profile["review_attempt_contract"]["role_prompt_refs"]) == {
        "producer", "reviewer", "repairer", "re_reviewer"
    }
    role_outputs = profile["review_attempt_contract"]["required_role_output_ref_fields"]
    assert role_outputs["reviewer"] == [
        "route_impact.stage_quality_cycle.outcome", "finding_refs", "evidence_refs",
        "acceptance_criteria_refs",
    ]
    assert "review_receipt_refs" not in role_outputs["reviewer"]
    assert "repair_map_refs" not in role_outputs["reviewer"]
    assert "repair_map_refs" in role_outputs["repairer"]
    assert "changed_artifact_refs" in role_outputs["repairer"]
    assert "re_review_closure_refs" in profile["review_attempt_contract"]["required_role_output_ref_fields"]["re_reviewer"]
    assert "review_receipt_refs" not in role_outputs["re_reviewer"]
    assert "verdict" not in role_outputs["reviewer"]
    assert "verdict" not in role_outputs["re_reviewer"]

    manifest_stages = {stage["stage_id"]: stage for stage in manifest["stages"]}
    assert set(profile["stages"]) == set(manifest_stages)
    for stage_id, policy in profile["stages"].items():
        assert manifest_stages[stage_id]["stage_quality_cycle_policy_ref"] == (
            f"contracts/stage_quality_cycle_policy.json#/stages/{stage_id}"
        )
        assert set(policy) == {
            "surface_kind", "version", "enabled", "stage_prompt_ref", "role_prompt_refs",
            "quality_rubric_refs", "in_thread_refinement", "formal_review", "budget_exhaustion",
            "attempt_boundary",
        }
        assert policy["enabled"] is True
        assert set(policy["role_prompt_refs"]) == {"producer", "reviewer", "repairer", "re_reviewer"}
        assert policy["in_thread_refinement"]["authoritative"] is False
        assert policy["stage_prompt_ref"] == manifest_stages[stage_id]["prompt_ref"]
        assert policy["quality_rubric_refs"] == manifest_stages[stage_id]["quality_gate_refs"]
        assert policy["formal_review"]["context_isolation_required"] is True
        assert set(policy["attempt_boundary"]) == {
            "inherits_stage_goal_scope_authority", "role_overlay_may_only_narrow",
            "controller_creates_next_attempt", "attempt_is_not_sub_stage",
        }
        assert all(policy["attempt_boundary"].values())
        assert (
            policy["formal_review"]["required"],
            policy["formal_review"]["max_repair_rounds"],
        ) == expected_review_policy[stage_id]

    assert manifest_stages["publication-proof-handoff"]["handoff_review_boundary"] == {
        "artifact_effect": "new_or_transformed_reviewable_bytes",
        "freezes_canonical_artifact_bytes": True,
        "issues_quality_export_publication_or_ready_claim": True,
        "downstream_owner_retains_acceptance": True,
    }


def test_publication_proof_claims_require_fresh_exact_byte_review() -> None:
    prompt = (ROOT / "agent/prompts/publication-proof-handoff.md").read_text(
        encoding="utf-8"
    )
    gate = (
        ROOT / "agent/quality_gates/publication-proof-handoff-quality-gate.md"
    ).read_text(encoding="utf-8")
    role_prompt = (ROOT / "agent/prompts/stage-quality-cycle-roles.md").read_text(
        encoding="utf-8"
    )

    for text in (prompt, gate, role_prompt):
        assert "`review_pending`" in text
        assert "publication-proof" in text
        assert "final-export" in text
        assert "owner/export acceptance" in text
    assert "Any regeneration invalidates the prior Review receipt" in gate
    assert "controller-materialized Review receipt" in prompt
    assert "controller-materialized Review receipt" in gate
    assert "`route_impact.stage_quality_cycle.outcome`" in prompt
    assert "never a standalone receipt `verdict`" in prompt
    assert "verdict terminalizes" not in prompt
    assert "producer cannot close publication-proof" in role_prompt
    assert "repairer cannot close publication-proof" in role_prompt
    assert "Do not create a Review receipt or repair map" in role_prompt
    assert "OPL StageRun controller materializes" in role_prompt
    assert "Do not create the controller-owned Review receipt" in role_prompt
    assert "reviewed final-export candidate may be handed downstream pending acceptance" in gate


def test_attempt_route_owner_and_machine_output_are_unambiguous() -> None:
    role_prompt = (ROOT / "agent/prompts/stage-quality-cycle-roles.md").read_text(
        encoding="utf-8"
    )
    meta_prompt = " ".join(
        (ROOT / "agent/prompts/source-style-integrity-review.md")
        .read_text(encoding="utf-8")
        .split()
    )
    proof_prompt = (ROOT / "agent/prompts/publication-proof-handoff.md").read_text(
        encoding="utf-8"
    )
    profile = read_json("contracts/stage_quality_cycle_policy.json")

    assert "`route_impact.stage_route_decision`" in role_prompt
    assert "`route_impact.stage_route_recommendation`" in role_prompt
    assert "`route_impact.stage_quality_cycle.outcome`" in role_prompt
    for outcome in ("pass", "repair_required", "quality_debt", "blocked", "human_gate"):
        assert f"`{outcome}`" in role_prompt
    assert "`hard_stop` is never an Attempt outcome" in role_prompt
    assert "`hard_stop` is not an Attempt outcome" in role_prompt
    assert "to its identically named receipt verdict" not in role_prompt
    assert "identical string values do not merge the Attempt outcome and receipt verdict" in role_prompt
    assert "receipt-only `verdict=pass|repair_required|quality_debt`" in role_prompt
    assert "producer is decisive only for a progress-terminal result" in role_prompt
    assert "repairer never makes a terminal route decision" in role_prompt
    assert "While repair budget remains" in role_prompt
    assert "decisive cross-Stage route owner" in meta_prompt
    assert "terminal reviewer or re-reviewer" in proof_prompt
    assert profile["meta_review_policy"]["terminal_route_output"] == (
        "route_impact.stage_route_decision"
    )
    assert profile["meta_review_policy"]["terminal_route_owner"] == "producer"
    assert "route_decision_evidence_refs" in profile["meta_review_policy"][
        "required_output_ref_fields"
    ]


def test_quality_role_prompt_terminalizes_final_budget_without_routing_hard_boundaries() -> None:
    roles = " ".join(
        (ROOT / "agent/prompts/stage-quality-cycle-roles.md")
        .read_text(encoding="utf-8")
        .split()
    )

    assert "`repair_budget_remaining`" in roles
    assert "another repair round remains" in roles
    assert "returns outcome `repair_required`" in roles
    assert "controller creates the next fresh repairer Attempt" in roles
    assert "This branch is non-terminal" in roles

    assert "`final_budget_consumable`" in roles
    assert "no repair round remains" in roles
    assert "keep outcome `repair_required`" in roles
    assert "do not relabel them `quality_debt`" in roles
    assert "exactly one `route_impact.stage_route_decision`" in roles
    assert "remaining required finding refs and quality-debt refs" in roles
    assert "classifies this branch as `terminal_quality_debt`" in roles
    assert "projects `completed_with_quality_debt`" in roles
    assert "`quality_debt` only when no required finding remains" in roles

    assert "`hard_boundary_or_zero_artifact`" in roles
    assert "literal zero consumable exact artifact is not a Stage-routing judgment" in roles
    assert "returns neither `route_impact.stage_route_decision` nor" in roles
    assert "`route_impact.stage_route_recommendation`" in roles
    assert "Literal zero consumable artifact uses `blocked`" in roles
    assert "terminalizes the StageRun as blocked or human-gated" in roles
    assert "A hard-boundary reviewer returns no route output" in roles
    assert "A hard-boundary re-reviewer returns no route output" in roles
    assert "A repairer never makes a terminal route decision" in roles

    meta_prompt = (ROOT / "agent/prompts/source-style-integrity-review.md").read_text(
        encoding="utf-8"
    )
    proof_prompt = (ROOT / "agent/prompts/publication-proof-handoff.md").read_text(
        encoding="utf-8"
    )
    proof_gate = (
        ROOT / "agent/quality_gates/publication-proof-handoff-quality-gate.md"
    ).read_text(encoding="utf-8")
    acceptance_gate = (ROOT / "agent/quality_gates/domain_acceptance.md").read_text(
        encoding="utf-8"
    )
    for prompt in (meta_prompt, proof_prompt):
        assert "no route output" in prompt
    assert "keeps outcome `repair_required`" in proof_prompt
    assert "controller projects `completed_with_quality_debt`" in proof_gate
    assert "Literal zero consumable artifact is a controller hard stop" in acceptance_gate


def test_whole_book_meta_review_is_independent_and_routes_without_inline_repair() -> None:
    manifest = read_json("agent/stages/manifest.json")
    profile = read_json("contracts/stage_quality_cycle_policy.json")
    stages = {stage["stage_id"]: stage for stage in manifest["stages"]}
    meta = profile["meta_review_policy"]

    assert stages["source-style-integrity-review"]["stage_role"] == "cross_stage_meta_review"
    assert meta["stage_id"] == "source-style-integrity-review"
    assert meta["attempt_role"] == "producer"
    assert meta["stage_prompt_ref"] == "agent/prompts/source-style-integrity-review.md"
    assert meta["independent_stage_run_required"] is True
    assert meta["new_execution_session_required"] is True
    assert meta["no_context_inheritance"] is True
    assert meta["max_route_back_rounds"] == 3
    assert meta["defect_owner_route_back"]["stage_refs"] == [
        "storyline-architecture",
        "chapter-production-planning",
        "chapter-materialization",
    ]
    prompt = (ROOT / "agent/prompts/source-style-integrity-review.md").read_text(encoding="utf-8")
    assert "do not edit manuscript artifacts inside this Meta Review Stage" in prompt
    planning_gate = (ROOT / "agent/quality_gates/chapter-production-planning-quality-gate.md").read_text(encoding="utf-8")
    assert "author-thread self-check is only `in_thread_refinement`" in planning_gate
    assert "The independent Review Attempt is required" in planning_gate
    assert "`route_impact.stage_quality_cycle.outcome=pass` is not a hard transition prerequisite" in planning_gate
    role_prompt = (ROOT / "agent/prompts/stage-quality-cycle-roles.md").read_text(encoding="utf-8")
    for semantic in (
        "stable `finding_id`",
        "`repair_expectation`",
        "repair map keyed by every accepted `finding_id`",
        "`changed_artifact_refs`",
        "`repair_regression`",
        "`critical_new_finding`",
        "`optional_observation` or quality debt without reopening the loop",
    ):
        assert semantic in role_prompt


def test_quality_policy_does_not_define_nested_stage_or_owner_graphs() -> None:
    profile = read_json("contracts/stage_quality_cycle_policy.json")
    forbidden = {
        "next_stage_refs",
        "requires",
        "ensures",
        "stage_route",
        "sub_stage_graph",
        "independent_owner",
        "stage_current_pointer",
        "stage_transition_authority",
    }

    def walk(value: object) -> None:
        if isinstance(value, dict):
            assert forbidden.isdisjoint(value)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(profile)


def main() -> int:
    test_bookforge_declares_explicit_review_policy_for_each_stage()
    test_publication_proof_claims_require_fresh_exact_byte_review()
    test_attempt_route_owner_and_machine_output_are_unambiguous()
    test_quality_role_prompt_terminalizes_final_budget_without_routing_hard_boundaries()
    test_whole_book_meta_review_is_independent_and_routes_without_inline_repair()
    test_quality_policy_does_not_define_nested_stage_or_owner_graphs()
    print(json.dumps({"status": "passed", "contract": "stage_quality_cycle_policy"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
