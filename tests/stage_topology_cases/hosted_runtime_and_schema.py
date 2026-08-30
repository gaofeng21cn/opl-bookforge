from __future__ import annotations

import json
import os
import subprocess
import tarfile
import tempfile
from contextlib import contextmanager
from pathlib import Path

from .stage_and_action import (
    ACTION_OUTPUT_SCHEMA_REFS,
    ACTION_STAGE_ROUTES,
    STAGE_ACTION_STATUSES,
)


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
        "dist/adapters/execution/hosted-agent-runtime-binding.js",
        "src/adapters/execution/hosted-agent-runtime-binding.ts",
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
        package = json.loads((framework_root / "package.json").read_text(encoding="utf-8"))
        archive = (
            framework_root
            / "dist/packages/framework"
            / f"one-person-lab-framework-{package['version']}.tar.gz"
        )
        archive_root = temporary_root / "one-person-lab"
        current_loader_ref = (
            "one-person-lab/dist/adapters/execution/hosted-agent-runtime-binding.js"
        )
        archive_current = False
        if archive.is_file():
            with tarfile.open(archive, "r:gz") as bundle:
                archive_current = current_loader_ref in bundle.getnames()
                if archive_current:
                    bundle.extractall(temporary_root, filter="data")
        if not archive_current:
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


def assert_hosted_runtime_and_schema(repo: Path, actions: dict) -> None:
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
            dist_only_root / "dist/adapters/execution/hosted-agent-runtime-binding.js"
        )
        fallback_module = framework_loader_module(repo, [source_only_root])
        assert fallback_module == (
            source_only_root / "src/adapters/execution/hosted-agent-runtime-binding.ts"
        )
        assert "--experimental-strip-types" in framework_node_command(fallback_module, "")

    with dist_only_framework_root(framework_module) as archive_root:
        archive_module = framework_loader_module(repo, [archive_root])
        assert archive_module.suffix == ".js"
        assert load_hosted_action_contracts(repo, archive_module) == hosted_contracts
