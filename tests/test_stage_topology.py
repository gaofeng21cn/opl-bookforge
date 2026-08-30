#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from stage_topology_cases.hosted_runtime_and_schema import assert_hosted_runtime_and_schema
from stage_topology_cases.retirement_and_carrier import assert_retirement_and_carrier
from stage_topology_cases.stage_and_action import (
    STAGE_SEQUENCE,
    assert_stage_and_action_contracts,
)


def load_json(repo: Path, ref: str) -> dict:
    return json.loads((repo / ref).read_text(encoding="utf-8"))


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    stage_manifest = load_json(repo, "agent/stages/manifest.json")
    stage_operating_principles = load_json(repo, "contracts/stage_operating_principles.json")
    stage_run_kernel_profile = load_json(repo, "contracts/stage_run_kernel_profile.json")
    principles = load_json(repo, "contracts/standard-agent-principles-adoption.json")
    action_catalog = load_json(repo, "contracts/action_catalog.json")
    capability_map = load_json(repo, "contracts/capability_map.json")
    pack_compiler_input = load_json(repo, "contracts/pack_compiler_input.json")
    kernel_adoption = load_json(repo, "contracts/stage_artifact_kernel_adoption.json")
    closeout = load_json(repo, "contracts/stage_decomposition_closeout.json")
    foundry_series = load_json(repo, "contracts/foundry_agent_series.json")
    golden_path = load_json(repo, "contracts/golden_path_profile.json")
    canary = load_json(repo, "contracts/stage_run_canary_evidence.json")

    actions = assert_stage_and_action_contracts(
        repo,
        stage_manifest=stage_manifest,
        stage_operating_principles=stage_operating_principles,
        stage_run_kernel_profile=stage_run_kernel_profile,
        principles=principles,
        action_catalog=action_catalog,
        capability_map=capability_map,
        pack_compiler_input=pack_compiler_input,
        kernel_adoption=kernel_adoption,
        closeout=closeout,
        foundry_series=foundry_series,
        canary=canary,
    )
    assert_hosted_runtime_and_schema(repo, actions)
    assert_retirement_and_carrier(repo, golden_path)

    print(json.dumps({"status": "passed", "stage_sequence": STAGE_SEQUENCE}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
