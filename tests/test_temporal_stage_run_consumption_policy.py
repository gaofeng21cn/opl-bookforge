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


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    policy = load_json(repo, "contracts/temporal_stage_run_consumption_policy.json")
    action_catalog = load_json(repo, "contracts/action_catalog.json")
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
    assert_false(policy, "forbidden_domain_repo_ownership.domain_repo_can_own_attempt_ledger")
    assert_false(policy, "write_boundary.bookforge_can_write_opl_stage_attempts")
    assert_false(policy, "write_boundary.bookforge_can_write_temporal_attempt_ledger")
    assert_true(policy, "projection_policy.projection_must_not_create_second_runtime")
    assert_true(policy, "projection_policy.projection_must_not_create_attempt_ledger")
    assert_closeout_refs(policy["completion_boundary"]["domain_completion_ref_fields"], "policy completion_boundary")

    assert action_catalog["temporal_stage_run_consumption_policy_ref"] == "contracts/temporal_stage_run_consumption_policy.json"
    assert_false(action_catalog, "authority_boundary.provider_completion_is_domain_completion")
    assert_false(action_catalog, "authority_boundary.domain_repo_can_own_temporal_runtime")
    assert_false(action_catalog, "authority_boundary.generated_surface_ready_counts_as_domain_ready")
    assert_false(action_catalog, "authority_boundary.bookforge_can_write_opl_stage_attempts")
    assert action_catalog["authority_boundary"]["temporal_attempt_ledger_owner"] == "one-person-lab"
    for action in action_catalog["actions"]:
        boundary = action["authority_boundary"]
        assert boundary["provider_completion_is_domain_completion"] is False, action["action_id"]
        assert boundary["domain_repo_can_own_temporal_runtime"] is False, action["action_id"]
        assert boundary["bookforge_can_write_opl_stage_attempts"] is False, action["action_id"]
        assert boundary["temporal_attempt_ledger_owner"] == "one-person-lab", action["action_id"]
        assert_closeout_refs(boundary["domain_completion_ref_fields"], f"action {action['action_id']}")

    assert generated_handoff["temporal_stage_run_consumption_policy_ref"] == "contracts/temporal_stage_run_consumption_policy.json"
    projection = generated_handoff["temporal_stage_run_projection"]
    assert projection["owner"] == "one-person-lab"
    assert projection["provider_completion_is_domain_completion"] is False
    assert projection["generated_surface_ready_counts_as_domain_ready"] is False
    assert projection["domain_repo_can_own_temporal_runtime"] is False
    assert projection["bookforge_can_write_opl_stage_attempts"] is False
    assert projection["temporal_attempt_ledger_owner"] == "one-person-lab"
    assert_closeout_refs(projection["domain_completion_ref_fields"], "generated handoff projection")

    assert stage_run_profile["temporal_stage_run_consumption_policy_ref"] == "contracts/temporal_stage_run_consumption_policy.json"
    embedded_policy = stage_run_profile["temporal_stage_run_consumption_policy"]
    assert embedded_policy["temporal_attempt_ledger_owner"] == "one-person-lab"
    assert embedded_policy["domain_repo_can_own_temporal_runtime"] is False
    assert embedded_policy["bookforge_can_write_opl_stage_attempts"] is False
    assert embedded_policy["provider_completion_is_domain_completion"] is False
    assert_closeout_refs(embedded_policy["domain_completion_ref_fields"], "stage run embedded policy")
    assert stage_run_profile["stage_run_state_machine"]["provider_completion_is_domain_completion"] is False
    assert stage_run_profile["authority_boundary"]["domain_repo_can_own_temporal_runtime"] is False
    assert stage_run_profile["authority_boundary"]["bookforge_can_write_opl_stage_attempts"] is False
    assert stage_run_profile["authority_boundary"]["generated_surface_ready_counts_as_domain_ready"] is False

    print(json.dumps({
        "status": "passed",
        "test": "temporal_stage_run_consumption_policy",
        "contract": "contracts/temporal_stage_run_consumption_policy.json"
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
