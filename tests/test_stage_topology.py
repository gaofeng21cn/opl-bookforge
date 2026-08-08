#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import tarfile
import tempfile
from contextlib import contextmanager
from pathlib import Path


STAGE_SEQUENCE = [
    "storyline-architecture",
    "chapter-production-planning",
    "chapter-materialization",
    "source-style-integrity-review",
    "publication-proof-handoff",
]
STAGE_DISPLAY_NAMES = {
    "storyline-architecture": {
        "en-US": "Storyline Architecture",
        "zh-CN": "全书叙事架构",
    },
    "chapter-production-planning": {
        "en-US": "Chapter Production Planning",
        "zh-CN": "章节写作规划",
    },
    "chapter-materialization": {
        "en-US": "Chapter Materialization",
        "zh-CN": "章节撰写",
    },
    "source-style-integrity-review": {
        "en-US": "Whole-Book Meta Review And Integrity Gate",
        "zh-CN": "全书总审与完整性检查",
    },
    "publication-proof-handoff": {
        "en-US": "Publication Proof Handoff",
        "zh-CN": "出版校样交接",
    },
}
ACTION_STAGE_ROUTES = {
    "shape-storyline": ["storyline-architecture"],
    "materialize-book": STAGE_SEQUENCE[1:],
}
ACTION_OUTPUT_SCHEMA_REFS = {
    "shape-storyline": "contracts/schemas/shape-storyline.output.schema.json",
    "materialize-book": "contracts/schemas/materialize-book.output.schema.json",
}
STAGE_ACTION_STATUSES = {
    "completed",
    "completed_with_quality_debt",
    "route_back",
    "typed_blocker",
    "human_gate",
    "failed",
    "no_output",
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
FOUNDRY_POLICY_FINGERPRINT = "sha256:11dae4f01d2647ba77b5bee332ceda0004be62984daab26903abe85f61e36722"
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


def framework_candidate_roots(repo: Path) -> list[Path]:
    candidates: list[Path] = []
    if configured := os.environ.get("OPL_FRAMEWORK_ROOT"):
        candidates.append(Path(configured))
    for entry in os.environ.get("PYTHONPATH", "").split(os.pathsep):
        if entry:
            candidate = Path(entry)
            candidates.append(candidate.parent if candidate.name == "python" else candidate)
    if configured_bin := os.environ.get("OPL_BIN"):
        candidates.append(Path(configured_bin).resolve().parent.parent)
    candidates.extend([
        repo.parent / "one-person-lab",
        repo.parents[2] / "one-person-lab",
    ])
    return list(dict.fromkeys(candidate.absolute() for candidate in candidates))


def framework_loader_module(repo: Path, candidates: list[Path] | None = None) -> Path:
    roots = candidates if candidates is not None else framework_candidate_roots(repo)
    for module_ref in (
        "dist/modules/runway/hosted-agent-runtime-binding.js",
        "src/modules/runway/hosted-agent-runtime-binding.ts",
    ):
        for root in roots:
            module = root / module_ref
            if module.is_file():
                return module.absolute()
    raise AssertionError("Framework hosted Agent runtime loader is unavailable")


def framework_node_command(module: Path, script: str) -> list[str]:
    command = ["node"]
    if module.suffix == ".ts":
        command.append("--experimental-strip-types")
    command.extend(["--input-type=module", "-e", script])
    return command


def framework_schema_validator_module(loader_module: Path) -> Path:
    module = loader_module.parents[2] / "kernel" / f"repo-json-schema{loader_module.suffix}"
    if module.is_file():
        return module.absolute()
    raise AssertionError("Framework JSON Schema validator is unavailable")


@contextmanager
def dist_only_framework_root(loader_module: Path):
    framework_root = loader_module.parents[3]
    with tempfile.TemporaryDirectory(prefix="obf-framework-dist-") as temporary_directory:
        temporary_root = Path(temporary_directory)
        package = load_json(framework_root, "package.json")
        archive = (
            framework_root
            / "dist/packages/framework"
            / f"one-person-lab-framework-{package['version']}.tar.gz"
        )
        archive_root = temporary_root / "one-person-lab"
        if archive.is_file():
            with tarfile.open(archive, "r:gz") as bundle:
                bundle.extractall(temporary_root, filter="data")
        else:
            archive_root.mkdir()
            os.symlink(framework_root / "dist", archive_root / "dist", target_is_directory=True)
            os.symlink(framework_root / "package.json", archive_root / "package.json")
        assert (archive_root / "dist").is_dir()
        assert not (archive_root / "src").exists()
        if not (archive_root / "node_modules").exists():
            os.symlink(
                framework_root / "node_modules",
                archive_root / "node_modules",
                target_is_directory=True,
            )
        yield archive_root


def load_hosted_action_contracts(repo: Path, module: Path | None = None) -> dict:
    module = module or framework_loader_module(repo)
    script = f"""
import {{ readHostedAgentRuntimeActionContracts }} from {json.dumps(module.as_uri())};
const {{ catalog, registry }} = readHostedAgentRuntimeActionContracts(
  {json.dumps(str(repo))},
  ["opl-bookforge"],
);
console.log(JSON.stringify({{
  target_domain_id: catalog.target_domain_id,
  actions: catalog.actions.map((action) => ({{
    action_id: action.action_id,
    input_schema_ref: action.input_schema_ref,
    output_schema_ref: action.output_schema_ref,
    execution_binding: action.execution_binding,
  }})),
  handler_ids: registry?.handlers.map((handler) => handler.handler_id) ?? [],
}}));
"""
    completed = subprocess.run(
        framework_node_command(module, script),
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, {
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
    return json.loads(completed.stdout)


def stage_action_payload(stage_id: str, status: str, **evidence: object) -> dict:
    return {
        "surface_kind": "opl_bookforge_stage_action_result",
        "schema_version": 1,
        "stage_id": stage_id,
        "status": status,
        "artifact_refs": [],
        "quality_debt_refs": [],
        "negative_result_refs": [],
        "failed_path_refs": [],
        "authority_boundary": {
            "domain_truth_owner": "opl-bookforge",
            "quality_verdict_owner": "opl-bookforge",
            "artifact_authority_owner": "opl-bookforge",
            "opl_can_write_domain_truth": False,
            "opl_can_mutate_domain_artifact_body": False,
            "opl_can_authorize_quality_or_export": False,
            "provider_completion_is_domain_completion": False,
        },
        **evidence,
    }


def assert_output_schema_payloads(repo: Path, loader_module: Path) -> None:
    validator_module = framework_schema_validator_module(loader_module)
    content_ref = {
        "kind": "obf_stage_diagnostic",
        "ref": "obf://stage-diagnostic/exact-result",
        "sha256": f"sha256:{'a' * 64}",
    }
    valid_evidence = {
        "completed": {"owner_receipt_ref": "obf://owner-receipt/completed"},
        "completed_with_quality_debt": {
            "owner_receipt_ref": "obf://owner-receipt/completed-with-quality-debt",
            "quality_debt_refs": ["obf://quality-debt/open-findings"],
        },
        "route_back": {"route_back_ref": "obf://route-back/storyline-architecture"},
        "typed_blocker": {"typed_blocker_ref": "obf://typed-blocker/protected-source"},
        "human_gate": {"human_gate_ref": "obf://human-gate/owner-decision"},
        "failed": {"failed_path_refs": [content_ref]},
        "no_output": {"negative_result_refs": [content_ref]},
    }
    cases: list[dict] = []
    for action_id, schema_ref in ACTION_OUTPUT_SCHEMA_REFS.items():
        stage_id = ACTION_STAGE_ROUTES[action_id][0]
        for status, evidence in valid_evidence.items():
            cases.append({
                "label": f"{action_id}:{status}:valid",
                "schema_ref": schema_ref,
                "payload": stage_action_payload(stage_id, status, **evidence),
                "valid": True,
            })
        for status in STAGE_ACTION_STATUSES:
            cases.append({
                "label": f"{action_id}:{status}:missing-status-evidence",
                "schema_ref": schema_ref,
                "payload": stage_action_payload(stage_id, status),
                "valid": False,
            })
        for status, field in (
            ("completed", "owner_receipt_ref"),
            ("completed_with_quality_debt", "owner_receipt_ref"),
            ("route_back", "route_back_ref"),
            ("typed_blocker", "typed_blocker_ref"),
            ("human_gate", "human_gate_ref"),
        ):
            cases.append({
                "label": f"{action_id}:{status}:null-status-evidence",
                "schema_ref": schema_ref,
                "payload": stage_action_payload(stage_id, status, **{field: None}),
                "valid": False,
            })
        for label, status, evidence in (
            ("completed-with-blocker", "completed", {"typed_blocker_ref": "obf://blocker/wrong"}),
            ("blocker-with-receipt", "typed_blocker", {"owner_receipt_ref": "obf://receipt/wrong"}),
            ("failed-with-negative-result", "failed", {"negative_result_refs": [content_ref]}),
            ("no-output-with-failed-path", "no_output", {"failed_path_refs": [content_ref]}),
        ):
            cases.append({
                "label": f"{action_id}:{label}",
                "schema_ref": schema_ref,
                "payload": stage_action_payload(stage_id, status, **evidence),
                "valid": False,
            })
        for status, field in (
            ("failed", "failed_path_refs"),
            ("no_output", "negative_result_refs"),
        ):
            for label, refs in (
                ("string-only", ["obf://diagnostic/no-hash"]),
                (
                    "object-without-hash",
                    [{"kind": "obf_stage_diagnostic", "ref": "obf://diagnostic/no-hash"}],
                ),
            ):
                cases.append({
                    "label": f"{action_id}:{status}:{label}",
                    "schema_ref": schema_ref,
                    "payload": stage_action_payload(stage_id, status, **{field: refs}),
                    "valid": False,
                })
    script = f"""
import {{ assertRepoJsonSchemaPayload }} from {json.dumps(validator_module.as_uri())};
const cases = {json.dumps(cases)};
for (const testCase of cases) {{
  let error = null;
  try {{
    assertRepoJsonSchemaPayload({{
      repoRoot: {json.dumps(str(repo))},
      schemaRef: testCase.schema_ref,
      payload: testCase.payload,
      label: testCase.label,
    }});
  }} catch (candidate) {{
    error = candidate;
  }}
  if (testCase.valid && error) throw error;
  if (!testCase.valid && (!error || error.code !== "contract_shape_invalid")) {{
    throw new Error(`Expected contract_shape_invalid for ${{testCase.label}}`);
  }}
}}
console.log(JSON.stringify({{ validated_cases: cases.length }}));
"""
    completed = subprocess.run(
        framework_node_command(validator_module, script),
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, {
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
    assert json.loads(completed.stdout) == {"validated_cases": len(cases)}


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
    stage_run_kernel_profile = load_json(repo, "contracts/stage_run_kernel_profile.json")
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
    assert {
        stage["stage_id"]: stage["display_names"] for stage in manifest_stages
    } == STAGE_DISPLAY_NAMES
    assert all(
        stage["display_names"]["en-US"] == stage["title"] for stage in manifest_stages
    )
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
    kernel_route_policy = stage_run_kernel_profile["codex_semantic_route_policy"]
    route_owner_contract = {
        "semantic_route_decision_owner": "decisive_codex_attempt",
        "stage_transition_materialization_owner": "opl_stage_run_controller",
    }
    for field, expected in route_owner_contract.items():
        assert manifest_policy[field] == expected
        assert operating_speed_policy[field] == expected
        assert kernel_route_policy[field] == expected
    assert "route_selection_owner" not in manifest_policy
    assert "route_selection_owner" not in operating_speed_policy
    assert "semantic_owner" not in kernel_route_policy
    assert manifest_policy["codex_may_advance_skip_repeat_reverse_or_route_back"] is True
    assert manifest_policy["any_declared_stage_may_start_from_any_prior_stage_result"] is True
    assert manifest_policy["declared_requires_are_quality_context_not_launch_gates"] is True
    assert manifest_policy["next_stage_refs_are_recommendations_not_constraints"] is True
    assert manifest_policy["no_output_or_failure_diagnostic_advances_stage"] is True
    for field in (
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
        assert action["output_schema_ref"] == ACTION_OUTPUT_SCHEMA_REFS[action_id]
        output_schema = load_json(repo, action["output_schema_ref"])
        assert output_schema["type"] == "object"
        assert output_schema["additionalProperties"] is False
        assert output_schema["properties"]["surface_kind"]["const"] == (
            "opl_bookforge_stage_action_result"
        )
        assert set(output_schema["properties"]["status"]["enum"]) == STAGE_ACTION_STATUSES
        stage_id_schema = output_schema["properties"]["stage_id"]
        schema_stage_ids = (
            [stage_id_schema["const"]]
            if "const" in stage_id_schema
            else stage_id_schema["enum"]
        )
        assert schema_stage_ids == ACTION_STAGE_ROUTES[action_id]
        authority = output_schema["properties"]["authority_boundary"]
        for field in (
            "domain_truth_owner",
            "quality_verdict_owner",
            "artifact_authority_owner",
        ):
            assert authority["properties"][field]["const"] == "opl-bookforge"
        for field in (
            "opl_can_write_domain_truth",
            "opl_can_mutate_domain_artifact_body",
            "opl_can_authorize_quality_or_export",
            "provider_completion_is_domain_completion",
        ):
            assert authority["properties"][field]["const"] is False
        assert "source_command" not in action
        assert "stage_route_exempt" not in action
        assert "handler_binding" not in action
        for surface in action["supported_surfaces"].values():
            assert "command" not in surface
            assert "surface_kind" not in surface

    materialize = actions["materialize-book"]
    assert "natural_language_intent" not in actions["shape-storyline"]
    assert "natural_language_intent" not in materialize
    assert actions["shape-storyline"]["summary"] != materialize["summary"]
    assert materialize["stage_route"]["entry_stage_ref"] == "chapter-production-planning"
    assert materialize["human_gate_ids"] == ["chapter_planning_owner_review"]

    framework_module = framework_loader_module(repo)
    assert ("--experimental-strip-types" in framework_node_command(framework_module, "")) == (
        framework_module.suffix == ".ts"
    )
    hosted_contracts = load_hosted_action_contracts(repo, framework_module)
    assert hosted_contracts == {
        "target_domain_id": "opl-bookforge",
        "actions": [
            {
                "action_id": action_id,
                "input_schema_ref": actions[action_id]["input_schema_ref"],
                "output_schema_ref": ACTION_OUTPUT_SCHEMA_REFS[action_id],
                "execution_binding": {
                    "kind": "stage_binding",
                    "stage_manifest_ref": "agent/stages/manifest.json",
                },
            }
            for action_id in ACTION_STAGE_ROUTES
        ],
        "handler_ids": ["obf.figure-asset-authority-evaluate"],
    }
    assert_output_schema_payloads(repo, framework_module)

    framework_root = framework_module.parents[3]
    with tempfile.TemporaryDirectory(prefix="obf-framework-locator-") as locator_directory:
        locator_root = Path(locator_directory)
        source_only_root = locator_root / "source-only"
        dist_only_root = locator_root / "dist-only"
        source_only_root.mkdir()
        dist_only_root.mkdir()
        os.symlink(framework_root / "src", source_only_root / "src", target_is_directory=True)
        os.symlink(framework_root / "dist", dist_only_root / "dist", target_is_directory=True)
        preferred_module = framework_loader_module(repo, [source_only_root, dist_only_root])
        assert preferred_module == (
            dist_only_root / "dist/modules/runway/hosted-agent-runtime-binding.js"
        )
        fallback_module = framework_loader_module(repo, [source_only_root])
        assert fallback_module == (
            source_only_root / "src/modules/runway/hosted-agent-runtime-binding.ts"
        )
        assert "--experimental-strip-types" in framework_node_command(fallback_module, "")

    with dist_only_framework_root(framework_module) as archive_root:
        archive_module = framework_loader_module(repo, [archive_root])
        assert archive_module.suffix == ".js"
        assert load_hosted_action_contracts(repo, archive_module) == hosted_contracts

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
    assert "description: Use when Codex needs OPL Book Forge to shape or materially produce a book-length nonfiction work" in primary_skill
    assert "Do not use for an isolated article, research paper, grant, slide deck, generic document formatting" in primary_skill
    for heading in (
        "Admission",
        "Action Routing",
        "Default Workflow",
        "Quality And Hard Stops",
        "Output Expectations",
        "References",
    ):
        assert f"## {heading}\n" in primary_skill
    assert "`shape-storyline`: use when the premise" in primary_skill
    assert "`materialize-book`: use when a current approved storyline exists" in primary_skill
    assert "run `shape-storyline` first, obtain the owner decision, then invoke `materialize-book`" in primary_skill
    assert "begins at `chapter-production-planning` and must not silently invent a replacement storyline" in primary_skill
    assert "Scripts may assemble, validate, and export, but must not hide manuscript prose in code or JSON literals" in primary_skill
    assert "Keep `review_pdf`, `publication_proof`, and `final_export` distinct" in primary_skill
    assert "Retry, independent-review, and repair limits are quality budgets" in primary_skill

    print(json.dumps({"status": "passed", "stage_sequence": STAGE_SEQUENCE}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
