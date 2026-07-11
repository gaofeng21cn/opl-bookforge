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
HISTORICAL_RECEIPTS = {
    "contracts/baseline_delivery_receipt.json",
    "contracts/live_stage_run_progress_evidence.json",
    "contracts/stage_decomposition_attempt_receipt.json",
    "contracts/stage_decomposition_closeout.json",
}
TEXT_SUFFIXES = {".json", ".md", ".py", ".sh"}


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
            if rel in HISTORICAL_RECEIPTS or rel.startswith(("docs/evidence/", "docs/history/")):
                continue
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if retired_stage in line and "docs/evidence/" not in line:
                    stale_refs.append(f"{rel}:{line_number}")
    assert not stale_refs, stale_refs


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    plane = load_json(repo, "contracts/stage_control_plane.json")
    stage_manifest = load_json(repo, "agent/stages/manifest.json")
    action_catalog = load_json(repo, "contracts/action_catalog.json")
    golden_path = load_json(repo, "contracts/golden_path_profile.json")
    native_contract = load_json(repo, "contracts/stage_native_artifact_contract.json")

    stages = plane["stages"]
    manifest_stages = stage_manifest["stages"]
    assert [stage["stage_id"] for stage in stages] == STAGE_SEQUENCE
    assert [stage["stage_id"] for stage in manifest_stages] == STAGE_SEQUENCE
    assert [stage["handoff"]["next_stage_refs"] for stage in stages] == [
        [stage_id] for stage_id in STAGE_SEQUENCE[1:]
    ] + [[]]
    assert [stage["next_stage_refs"] for stage in manifest_stages] == [
        [stage_id] for stage_id in STAGE_SEQUENCE[1:]
    ] + [[]]

    planning = stages[1]
    assert planning["progress_first_policy"]["ordinary_gap_outcome"] == "in_progress_or_route_back"
    assert planning["progress_first_policy"]["ordinary_gap_can_emit_generic_typed_blocker"] is False
    assert planning["progress_first_policy"]["independent_review_required_for_ordinary_transition"] is False
    assert planning["independent_gate_policy"]["ordinary_transition_requires_independent_review"] is False
    planning_refs = {
        *planning["handoff"]["allowed_closure_refs"],
        *planning["stage_contract"]["ensures"],
        *(entry["ref"] for entry in planning["stage_contract"]["expected_receipt_refs"]),
    }
    assert "independent-gate-receipt-ref:chapter-production-planning" not in planning_refs
    assert "owner-handoff-ref:storyline-architecture" in planning["stage_contract"]["requires"]
    assert "storyline-admission-ref:chapter-production-planning" in planning["stage_contract"]["ensures"]
    manifest_planning = manifest_stages[1]
    assert manifest_planning["stage_contract"]["progress_first_policy"] == planning["progress_first_policy"]
    assert manifest_planning["stage_contract"]["transition_policy"]["ordinary_transition_requires_independent_review"] is False
    assert "independent-gate-receipt-ref:chapter-production-planning" not in manifest_planning["ensures"]

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
            "route_policy": "ordered_stage_attempts_no_skip",
        }

    materialize = actions["materialize-book"]
    expected_command = "opl family-runtime attempt create --domain opl-bookforge --stage chapter-production-planning --provider temporal "
    assert materialize["source_command"]["command"].startswith(expected_command)
    assert materialize["supported_surfaces"]["cli"]["command"] == materialize["source_command"]["command"]
    assert materialize["supported_surfaces"]["product_entry"]["command"] == materialize["source_command"]["command"]
    assert materialize["human_gate_ids"] == ["chapter_planning_owner_review"]

    assert golden_path["ordinary_path"]["stage_refs"] == ["storyline-architecture"]
    assert golden_path["ordinary_path"]["follow_on_stage_refs"] == STAGE_SEQUENCE[1:]
    assert golden_path["explicit_variants"][0]["stage_refs"] == STAGE_SEQUENCE[1:]
    assert [contract["stage_id"] for contract in native_contract["contracts"]] == STAGE_SEQUENCE
    native_dirs = sorted(
        path.name
        for path in (repo / "contracts/stage_native_artifacts").iterdir()
        if path.is_dir()
    )
    assert native_dirs == sorted(STAGE_SEQUENCE)

    retired_stage = "-".join(("book", "materialization"))
    for ref in (
        f"agent/prompts/{retired_stage}.md",
        f"agent/stages/{retired_stage}.md",
        f"agent/quality_gates/{retired_stage}-quality-gate.md",
        f"contracts/stage_native_artifacts/{retired_stage}",
    ):
        assert not (repo / ref).exists(), ref
    assert_no_retired_stage_refs(repo)

    print(json.dumps({"status": "passed", "stage_sequence": STAGE_SEQUENCE}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
