from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path
from typing import Any

from .stage_and_action import (
    ACTION_OUTPUT_SCHEMA_REFS,
    ACTION_STAGE_ROUTES,
    STAGE_ACTION_STATUSES,
)


def framework_candidate_roots(repo: Path) -> list[Path]:
    configured = os.environ.get("OPL_FRAMEWORK_ROOT")
    configured_bin = os.environ.get("OPL_BIN")
    binary_root = (
        Path(shutil.which(configured_bin) or configured_bin).resolve().parent.parent
        if configured_bin else None
    )
    if configured:
        root = Path(configured).resolve()
        if binary_root is not None and binary_root != root:
            raise ValueError("OPL_BIN and OPL_FRAMEWORK_ROOT must select the same Framework")
        return [root]
    if binary_root is not None:
        return [binary_root]
    candidates: list[Path] = []
    for entry in os.environ.get("PYTHONPATH", "").split(os.pathsep):
        if entry:
            candidate = Path(entry)
            if candidate.name == "src" and candidate.parent.name == "python-client":
                candidates.append(candidate.parent.parent.parent)
            elif candidate.name == "python":
                candidates.append(candidate.parent)
            else:
                candidates.append(candidate)
    candidates.append(repo.parent / ".worktrees/opl-v2")
    candidates.append(repo.parent / "one-person-lab")
    if len(repo.parents) > 2:
        candidates.append(repo.parents[2] / "one-person-lab")
    if installed_bin := shutil.which("opl"):
        candidates.append(Path(installed_bin).resolve().parent.parent)
    return list(dict.fromkeys(candidate.resolve() for candidate in candidates))


class ContractShapeError(AssertionError):
    code = "contract_shape_invalid"


def _resolve_ref(root_schema: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    ref = schema.get("$ref")
    if not ref:
        return schema
    if not ref.startswith("#/"):
        raise ContractShapeError(f"Unsupported $ref: {ref}")
    target: Any = root_schema
    for part in ref[2:].split("/"):
        target = target[part]
    return target


def _validate_node(root_schema: dict[str, Any], schema: dict[str, Any], value: Any, path: str) -> None:
    schema = _resolve_ref(root_schema, schema)
    if "const" in schema and (value != schema["const"] or isinstance(value, bool) != isinstance(schema["const"], bool)):
        raise ContractShapeError(f"{path}: expected const {schema['const']!r}, got {value!r}")
    if "enum" in schema and value not in schema["enum"]:
        raise ContractShapeError(f"{path}: expected one of {schema['enum']!r}, got {value!r}")
    expected_type = schema.get("type")
    if expected_type == "null":
        if value is not None:
            raise ContractShapeError(f"{path}: expected null")
    elif expected_type == "string":
        if not isinstance(value, str):
            raise ContractShapeError(f"{path}: expected string")
        if "minLength" in schema and len(value) < schema["minLength"]:
            raise ContractShapeError(f"{path}: string shorter than {schema['minLength']}")
        if "pattern" in schema and not re.match(schema["pattern"], value):
            raise ContractShapeError(f"{path}: string does not match pattern {schema['pattern']}")
    elif expected_type == "object" or (
        expected_type is None
        and isinstance(value, dict)
        and any(k in schema for k in ("properties", "required", "additionalProperties"))
    ):
        if not isinstance(value, dict):
            raise ContractShapeError(f"{path}: expected object")
        for req in schema.get("required", []):
            if req not in value:
                raise ContractShapeError(f"{path}: missing required key {req}")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            unknown = set(value) - set(props)
            if unknown:
                raise ContractShapeError(f"{path}: unsupported keys {sorted(unknown)}")
        for k, subschema in props.items():
            if k in value:
                _validate_node(root_schema, subschema, value[k], f"{path}.{k}")
    elif expected_type == "array":
        if not isinstance(value, list):
            raise ContractShapeError(f"{path}: expected array")
        if "minItems" in schema and len(value) < schema["minItems"]:
            raise ContractShapeError(f"{path}: fewer than {schema['minItems']} items")
        item_schema = schema.get("items")
        if item_schema is not None:
            for idx, item in enumerate(value):
                _validate_node(root_schema, item_schema, item, f"{path}[{idx}]")
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, sort_keys=True) for item in value]
            if len(serialized) != len(set(serialized)):
                raise ContractShapeError(f"{path}: duplicate array items")
    if "oneOf" in schema:
        matches = 0
        for branch in schema["oneOf"]:
            try:
                _validate_node(root_schema, branch, value, path)
                matches += 1
            except ContractShapeError:
                pass
        if matches != 1:
            raise ContractShapeError(f"{path}: expected exactly 1 oneOf match, got {matches}")


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


def assert_output_schema_payloads(repo: Path) -> None:
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

    schema_cache: dict[str, dict[str, Any]] = {}
    for case in cases:
        schema = schema_cache.setdefault(
            case["schema_ref"],
            json.loads((repo / case["schema_ref"]).read_text(encoding="utf-8")),
        )
        error: ContractShapeError | None = None
        try:
            _validate_node(schema, schema, case["payload"], case["label"])
        except ContractShapeError as exc:
            error = exc
        if case["valid"] and error is not None:
            raise AssertionError(f"Valid payload failed {case['label']}: {error}")
        if not case["valid"] and error is None:
            raise AssertionError(f"Expected contract_shape_invalid for {case['label']}")


def assert_hosted_runtime_and_schema(repo: Path, actions: dict) -> None:
    catalog = json.loads((repo / "contracts/action_catalog.json").read_text(encoding="utf-8"))
    registry = json.loads((repo / "contracts/domain_handler_registry.json").read_text(encoding="utf-8"))
    manifest = json.loads((repo / "opl-package.json").read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "opl.package.v2"
    assert manifest["provides"]["agent"]["stages_ref"] == "agent/stages/manifest.json"
    assert catalog["target_domain_id"] == "opl-bookforge"
    assert [
        {
            "action_id": action["action_id"],
            "input_schema_ref": action["input_schema_ref"],
            "output_schema_ref": action["output_schema_ref"],
            "execution_binding": action["execution_binding"],
        }
        for action in catalog["actions"]
    ] == [
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
    ]
    assert [h["handler_id"] for h in registry["handlers"]] == ["obf.figure-asset-authority-evaluate"]
    assert_output_schema_payloads(repo)
