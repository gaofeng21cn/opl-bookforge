import json
from collections import defaultdict, deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIMENSIONS = [
    "content",
    "editorial",
    "reference",
    "display",
    "layout",
    "export",
    "package",
]
FRAMEWORK_CHANGE_CLASSES = {
    "context",
    "claim",
    "limitation",
    "reference_source",
    "citation_linkage",
    "visual_content",
    "layout",
    "render_template",
    "package_composition",
    "package_wrapper",
}


def read_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def affected_dimensions(contract: dict, changed_dimensions: list[str]) -> list[str]:
    outgoing: dict[str, list[str]] = defaultdict(list)
    for edge in contract["dependency_edges"]:
        outgoing[edge["source_dimension"]].append(edge["dependent_dimension"])

    affected = set(changed_dimensions)
    pending = deque(changed_dimensions)
    while pending:
        source = pending.popleft()
        for dependent in outgoing[source]:
            if dependent in affected:
                continue
            affected.add(dependent)
            pending.append(dependent)
    return [dimension for dimension in DIMENSIONS if dimension in affected]


def test_contract_binds_canonical_framework_and_declares_true_dependencies() -> None:
    contract = read_json("contracts/epistemic_review_adoption.json")
    compiler_input = read_json("contracts/pack_compiler_input.json")

    assert contract["surface_kind"] == "opl_bookforge_epistemic_review_adoption"
    assert contract["framework_baseline"] == {
        "canonical_sha": "367738244273664452e6b7ebfb86d5de5bb36c30",
        "currentness_contract_ref": (
            "contracts/opl-framework/epistemic-review-currentness-contract.json"
        ),
        "scope_schema_ref": (
            "contracts/opl-framework/epistemic-review-scope-v2.schema.json"
        ),
        "stage_quality_cycle_contract_ref": (
            "contracts/opl-framework/stage-quality-cycle-contract.json"
        ),
    }
    assert list(contract["review_dimensions"]) == DIMENSIONS
    assert contract["scope_materialization"] == {
        "surface_kind": "opl_epistemic_review_scope",
        "version": "opl-epistemic-review-scope.v2",
        "schema_ref": "contracts/opl-framework/epistemic-review-scope-v2.schema.json",
        "one_scope_per_review_dimension": True,
        "scope_id_template": (
            "opl-bookforge:{workspace_id}:{artifact_id}:{review_dimension}"
        ),
        "actual_reviewed_node_refs_required": True,
        "actual_artifact_claim_and_provenance_nodes_required": True,
        "actual_dependency_edges_required": True,
        "domain_dimension_to_framework_scope_mapping_ref": (
            "contracts/epistemic_review_adoption.json#/review_dimensions"
        ),
        "framework_evaluates_currentness": True,
        "bookforge_declares_nodes_edges_scope_and_verdict": True,
    }
    assert {
        dimension: profile["framework_scope_kind"]
        for dimension, profile in contract["review_dimensions"].items()
    } == {
        "content": "content",
        "editorial": "content",
        "reference": "reference",
        "display": "display",
        "layout": "display",
        "export": "package",
        "package": "package",
    }

    incoming: dict[str, list[str]] = defaultdict(list)
    for edge in contract["dependency_edges"]:
        assert edge["source_dimension"] in DIMENSIONS
        assert edge["dependent_dimension"] in DIMENSIONS
        incoming[edge["dependent_dimension"]].append(edge["source_dimension"])
    for dimension, profile in contract["review_dimensions"].items():
        assert profile["reviewed_node_roles"]
        assert profile["framework_change_classes"]
        assert set(profile["framework_change_classes"]) <= FRAMEWORK_CHANGE_CLASSES
        assert profile["artifact_dependencies"]
        assert profile["depends_on_dimensions"] == incoming[dimension]

    for changed_dimension in DIMENSIONS:
        assert contract["semantic_change_impact"][changed_dimension] == (
            affected_dimensions(contract, [changed_dimension])
        )

    adoption_ref = "contracts/epistemic_review_adoption.json"
    assert adoption_ref in compiler_input["required_domain_pack_paths"]
    assert compiler_input["source_refs"]["epistemic_review_adoption_source_ref"] == (
        adoption_ref
    )


def test_layout_export_and_hash_counterexamples_preserve_upstream_review() -> None:
    contract = read_json("contracts/epistemic_review_adoption.json")
    expectations = contract["counterexample_expectations"]

    layout = expectations["layout_only_regeneration"]
    assert affected_dimensions(contract, layout["semantic_changed_dimensions"]) == [
        "layout",
        "export",
        "package",
    ]
    assert layout["stale_review_dimensions"] == ["layout", "export", "package"]
    assert layout["current_review_dimensions"] == [
        "content",
        "editorial",
        "reference",
        "display",
    ]

    export = expectations["export_only_regeneration"]
    assert affected_dimensions(contract, export["semantic_changed_dimensions"]) == [
        "export",
        "package",
    ]
    assert export["current_review_dimensions"] == [
        "content",
        "editorial",
        "reference",
        "display",
        "layout",
    ]

    hash_only = expectations["hash_only_locator_change"]
    assert hash_only["locator_hash_changed"] is True
    assert affected_dimensions(contract, hash_only["semantic_changed_dimensions"]) == []
    assert hash_only["stale_review_dimensions"] == []
    assert hash_only["current_review_dimensions"] == DIMENSIONS


def test_content_change_fails_closed_even_when_hash_is_unchanged() -> None:
    contract = read_json("contracts/epistemic_review_adoption.json")
    content = contract["counterexample_expectations"][
        "content_change_with_unchanged_hash"
    ]

    assert content["locator_hash_changed"] is False
    assert content["fail_closed"] is True
    assert affected_dimensions(contract, content["semantic_changed_dimensions"]) == DIMENSIONS
    assert content["stale_review_dimensions"] == DIMENSIONS
    assert content["current_review_dimensions"] == []
    assert contract["currentness_policy"]["content_semantic_change_fail_closed"] is True


def test_meta_review_stage_budget_and_release_integrity_stay_separate() -> None:
    contract = read_json("contracts/epistemic_review_adoption.json")
    manifest = read_json("agent/stages/manifest.json")
    quality_policy = read_json("contracts/stage_quality_cycle_policy.json")
    stages = {stage["stage_id"]: stage for stage in manifest["stages"]}

    boundary = contract["stage_boundary"]
    assert boundary["whole_book_meta_review_stage_id"] != (
        boundary["publication_proof_stage_id"]
    )
    assert stages[boundary["whole_book_meta_review_stage_id"]]["stage_role"] == (
        "cross_stage_meta_review"
    )
    assert quality_policy["stages"][boundary["whole_book_meta_review_stage_id"]][
        "formal_review"
    ]["required"] is False
    assert quality_policy["stages"][boundary["publication_proof_stage_id"]][
        "formal_review"
    ]["required"] is True
    assert quality_policy["meta_review_policy"]["max_route_back_rounds"] == 3
    assert boundary["formal_stage_review_max_repair_rounds"] == 3

    budget = contract["budget_binding"]
    assert budget["execution_unit"] == "opl_stage_attempt"
    assert budget["foreground_review_must_use_managed_stage_attempt"] is True
    assert budget["domain_parallel_budget_or_scheduler_forbidden"] is True
    for stage_id, policy in quality_policy["stages"].items():
        formal_review = policy["formal_review"]
        assert formal_review["scope_budget"]["max_attempts"] == (
            formal_review["max_repair_rounds"]
        ), stage_id
        assert formal_review["scope_budget"][
            "foreground_execution_must_use_managed_attempt"
        ] is True

    integrity = contract["integrity_separation"]
    assert integrity["release_integrity_contract_role"] == (
        "separate_exact_byte_integrity_contract"
    )
    assert integrity["release_integrity_receipt_can_replace_epistemic_review"] is False
    assert integrity["epistemic_review_can_replace_release_integrity"] is False
    assert contract["authority_boundary"]["hash_is_content_authority"] is False


def test_blanket_regeneration_invalidation_is_retired_from_active_surfaces() -> None:
    active_surfaces = [
        "agent/stages/publication-proof-handoff.md",
        "agent/prompts/publication-proof-handoff.md",
        "agent/prompts/stage-quality-cycle-roles.md",
        "agent/quality_gates/publication-proof-handoff-quality-gate.md",
        "agent/professional_skills/bookforge-meta-reviewer/SKILL.md",
        "agent/professional_skills/bookforge-publication-memory-curator/SKILL.md",
        "docs/architecture.md",
        "docs/decisions.md",
        "docs/invariants.md",
    ]
    text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8") for path in active_surfaces
    )
    for retired_statement in (
        "Any regeneration invalidates the prior Review receipt",
        "Any regeneration invalidates the prior receipt",
        "any regenerated PDF/export invalidates the prior Review receipt",
        "regeneration invalidates old receipts",
    ):
        assert retired_statement not in text
    assert "Layout-only changes invalidate layout, export, and package" in text
    assert "content change fails closed" in text.lower()
    assert "hashes as artifact locators or stale hints only" in text
    assert "OPL-managed `source-style-integrity-review` producer StageAttempt" in text


def main() -> int:
    test_contract_binds_canonical_framework_and_declares_true_dependencies()
    test_layout_export_and_hash_counterexamples_preserve_upstream_review()
    test_content_change_fails_closed_even_when_hash_is_unchanged()
    test_meta_review_stage_budget_and_release_integrity_stay_separate()
    test_blanket_regeneration_invalidation_is_retired_from_active_surfaces()
    print(json.dumps({
        "status": "passed",
        "contract": "contracts/epistemic_review_adoption.json",
        "counterexamples": 4,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
