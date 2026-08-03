#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from temporal_stage_run_consumption_policy_cases.capability_assertions import (
    assert_capability_map_standard_kinds,
    assert_legacy_professional_skill_redirects,
    assert_opl_default_hygiene_and_probe_consumption,
    assert_private_platform_retirement_matrix,
)
from temporal_stage_run_consumption_policy_cases.entrypoint_assertions import (
    assert_default_entry_routing,
    assert_generated_handoff_temporal_projection,
    assert_handoff_current_paths_exist,
    assert_stage_run_profile,
)
from temporal_stage_run_consumption_policy_cases.evidence_assertions import (
    assert_live_stage_run_progress_evidence,
    assert_production_acceptance_tail,
)
from temporal_stage_run_consumption_policy_cases.ledger_assertions import (
    assert_generated_handoff_ledger_projection,
    assert_opl_ledger_artifact_registration,
)
from temporal_stage_run_consumption_policy_cases.policy_assertions import (
    assert_action_catalog,
    assert_completion_audit,
    assert_feedback_self_evolution_trigger,
    assert_foundry_series,
    assert_functional_closure_gate,
    assert_policy_header,
    load_json,
)


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    capability_map = load_json(repo, "contracts/capability_map.json")
    policy = load_json(repo, "contracts/temporal_stage_run_consumption_policy.json")
    action_catalog = load_json(repo, "contracts/action_catalog.json")
    foundry_series = load_json(repo, "contracts/foundry_agent_series.json")
    generated_handoff = load_json(repo, "contracts/generated_surface_handoff.json")
    functional_audit = load_json(repo, "contracts/functional_privatization_audit.json")
    agent_lab_handoff = load_json(repo, "contracts/agent_lab_handoff.json")
    stage_run_profile = load_json(repo, "contracts/stage_run_kernel_profile.json")
    live_stage_run_progress = load_json(repo, "contracts/live_stage_run_progress_evidence.json")
    production_acceptance = load_json(repo, "contracts/production_acceptance/bookforge-production-acceptance.json")
    opl_ledger_artifact_registration = load_json(repo, "contracts/opl_ledger_artifact_registration.json")

    assert_policy_header(policy)
    assert_functional_closure_gate(policy["functional_closure_gate"])
    assert_default_entry_routing(policy["default_entry_routing"])
    assert_opl_default_hygiene_and_probe_consumption(repo)
    assert_foundry_series(foundry_series)
    assert_handoff_current_paths_exist(repo, generated_handoff)
    assert_feedback_self_evolution_trigger(agent_lab_handoff["feedback_self_evolution_trigger"])
    assert_completion_audit(policy)
    assert_action_catalog(action_catalog, foundry_series)
    assert_generated_handoff_temporal_projection(generated_handoff)
    assert_generated_handoff_ledger_projection(generated_handoff)
    assert_private_platform_retirement_matrix(functional_audit, generated_handoff)
    assert_capability_map_standard_kinds(repo, capability_map)
    assert_legacy_professional_skill_redirects(repo, capability_map)
    assert_stage_run_profile(stage_run_profile)
    assert_live_stage_run_progress_evidence(live_stage_run_progress)
    assert_production_acceptance_tail(production_acceptance)
    assert_opl_ledger_artifact_registration(opl_ledger_artifact_registration)

    print(json.dumps({
        "status": "passed",
        "test": "temporal_stage_run_consumption_policy",
        "contract": "contracts/temporal_stage_run_consumption_policy.json",
        "live_stage_run_progress_evidence_contract": "contracts/live_stage_run_progress_evidence.json",
        "production_acceptance_contract": "contracts/production_acceptance/bookforge-production-acceptance.json",
        "private_platform_retirement_contract": "contracts/functional_privatization_audit.json",
        "opl_ledger_artifact_registration_contract": "contracts/opl_ledger_artifact_registration.json",
        "capability_map_contract": "contracts/capability_map.json"
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
