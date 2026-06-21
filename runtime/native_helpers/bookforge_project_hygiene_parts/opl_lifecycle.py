from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


OPL_ARTIFACT_LIFECYCLE_DIR = Path("control/opl/artifact_lifecycle")
OPL_ARTIFACT_LIFECYCLE_INDEX_REF = OPL_ARTIFACT_LIFECYCLE_DIR / "artifact_lifecycle_index.json"
OPL_ARTIFACT_LIFECYCLE_HEALTH_REF = OPL_ARTIFACT_LIFECYCLE_DIR / "artifact_lifecycle_health.json"
OPL_ARTIFACT_LIFECYCLE_SOURCE_REF = OPL_ARTIFACT_LIFECYCLE_DIR / "source_passport.json"
OPL_ARTIFACT_LIFECYCLE_MEMORY_REF = OPL_ARTIFACT_LIFECYCLE_DIR / "memory_lifecycle.json"
OPL_ARTIFACT_LIFECYCLE_OUTPUT_REF = OPL_ARTIFACT_LIFECYCLE_DIR / "output_lifecycle.json"
ARTIFACT_LIFECYCLE_HANDOFF_CONTRACT_REF = Path("contracts/artifact_lifecycle_handoff.json")

REQUIRED_CONTRACT_FALSE_READY_FLAGS = (
    "contract_present_counts_as_workspace_apply_evidence",
    "dry_run_counts_as_workspace_apply_evidence",
    "projection_clean_counts_as_book_delivery_ready",
    "projection_clean_counts_as_publication_ready",
    "projection_clean_counts_as_final_export_ready",
    "projection_clean_counts_as_owner_acceptance",
    "projection_clean_counts_as_production_ready",
    "helper_hygiene_counts_as_book_delivery_ready",
    "helper_hygiene_counts_as_publication_ready",
    "helper_hygiene_counts_as_owner_acceptance",
)
REQUIRED_CONTRACT_FORBIDDEN_AUTHORITY_FLAGS = (
    "opl_can_write_bookforge_domain_truth",
    "opl_can_write_memory_body",
    "opl_can_mutate_manuscript_or_artifact_body",
    "opl_can_authorize_quality_export_or_publication",
    "opl_can_sign_owner_receipts",
    "bookforge_can_replace_opl_lifecycle_projection",
    "bookforge_can_create_private_lifecycle_second_truth",
)
REQUIRED_CONTRACT_PROJECTION_REFS = (
    OPL_ARTIFACT_LIFECYCLE_INDEX_REF.as_posix(),
    OPL_ARTIFACT_LIFECYCLE_SOURCE_REF.as_posix(),
    OPL_ARTIFACT_LIFECYCLE_MEMORY_REF.as_posix(),
    OPL_ARTIFACT_LIFECYCLE_OUTPUT_REF.as_posix(),
    OPL_ARTIFACT_LIFECYCLE_HEALTH_REF.as_posix(),
)


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def safe_read_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def default_opl_bin() -> str | None:
    candidates = [
        Path("/Users/gaofeng/workspace/one-person-lab/bin/opl"),
    ]
    found = shutil.which("opl")
    if found:
        candidates.append(Path(found))
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return str(candidate)
    return None


def find_opl_workspace(project_root: Path) -> tuple[Path | None, str | None]:
    resolved = project_root.resolve()
    for candidate in [resolved, *resolved.parents]:
        index_path = candidate / "workspace_index.json"
        index = safe_read_json(index_path)
        if not isinstance(index, dict):
            continue
        projects = index.get("projects")
        if not isinstance(projects, list):
            continue
        for item in projects:
            if not isinstance(item, dict):
                continue
            project_id = item.get("project_id")
            project_ref = item.get("project_root")
            if not isinstance(project_id, str) or not isinstance(project_ref, str):
                continue
            project_path_candidate = (candidate / project_ref).resolve()
            if project_path_candidate == resolved:
                return candidate, project_id
    return None, None


def opl_artifact_lifecycle_summary(root: Path, require: bool, opl_bin: str | None) -> dict[str, Any]:
    workspace_path, project_id = find_opl_workspace(root)
    projection_refs = [
        OPL_ARTIFACT_LIFECYCLE_INDEX_REF,
        OPL_ARTIFACT_LIFECYCLE_SOURCE_REF,
        OPL_ARTIFACT_LIFECYCLE_MEMORY_REF,
        OPL_ARTIFACT_LIFECYCLE_OUTPUT_REF,
        OPL_ARTIFACT_LIFECYCLE_HEALTH_REF,
    ]
    projection_files = {
        ref.as_posix(): {
            "exists": (root / ref).exists(),
            "path": rel(root / ref, root),
        }
        for ref in projection_refs
    }
    health = safe_read_json(root / OPL_ARTIFACT_LIFECYCLE_HEALTH_REF)
    index = safe_read_json(root / OPL_ARTIFACT_LIFECYCLE_INDEX_REF)
    lifecycle_status = health.get("status") if isinstance(health, dict) else None
    missing_projection_refs = [
        ref
        for ref, meta in projection_files.items()
        if not bool(meta["exists"])
    ]
    command_result: dict[str, Any] = {
        "attempted": False,
        "status": "not_run",
    }
    requested_opl_bin = opl_bin
    selected_opl_bin = opl_bin or default_opl_bin()
    opl_bin_found = bool(
        selected_opl_bin
        and Path(selected_opl_bin).exists()
        and Path(selected_opl_bin).is_file()
    )
    if workspace_path and project_id and selected_opl_bin and opl_bin_found:
        command = [
            selected_opl_bin,
            "workspace",
            "artifact-lifecycle",
            "--workspace",
            str(workspace_path),
            "--project-id",
            project_id,
            "--dry-run",
            "--json",
        ]
        command_result = {
            "attempted": True,
            "status": "error",
            "command": command,
        }
        try:
            completed = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            parsed = json.loads(completed.stdout) if completed.stdout.strip() else None
            command_result.update({
                "exit_code": completed.returncode,
                "status": "passed" if completed.returncode == 0 else "failed",
                "lifecycle_status": (
                    parsed.get("workspace_artifact_lifecycle", {}).get("lifecycle_status")
                    if isinstance(parsed, dict)
                    else None
                ),
                "stderr": completed.stderr.strip(),
            })
        except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
            command_result.update({
                "status": "error",
                "error": str(exc),
            })
    return {
        "required": require,
        "workspace_path": str(workspace_path) if workspace_path else None,
        "project_id": project_id,
        "opl_bin": selected_opl_bin if opl_bin_found else None,
        "requested_opl_bin": requested_opl_bin,
        "opl_bin_found": opl_bin_found,
        "projection_files": projection_files,
        "missing_projection_refs": missing_projection_refs,
        "health_status": lifecycle_status,
        "health_blockers": health.get("blockers") if isinstance(health, dict) else None,
        "index_status": index.get("status") if isinstance(index, dict) else None,
        "dry_run": command_result,
    }


def opl_artifact_lifecycle_issues(summary: dict[str, Any]) -> list[dict[str, Any]]:
    if not summary.get("required"):
        return []
    issues: list[dict[str, Any]] = []
    if not summary.get("workspace_path") or not summary.get("project_id"):
        issues.append({
            "kind": "opl_artifact_lifecycle_missing",
            "reason": "book project is not indexed under an OPL workspace_index.json",
        })
    if not summary.get("opl_bin"):
        issues.append({
            "kind": "opl_artifact_lifecycle_missing",
            "reason": "opl binary not found",
        })
    dry_run = summary.get("dry_run") if isinstance(summary.get("dry_run"), dict) else {}
    if dry_run.get("attempted") and dry_run.get("status") != "passed":
        issues.append({
            "kind": "opl_artifact_lifecycle_blocked",
            "reason": "OPL artifact-lifecycle dry-run failed",
            "details": dry_run,
        })
    missing_projection_refs = summary.get("missing_projection_refs")
    if isinstance(missing_projection_refs, list) and missing_projection_refs:
        issues.append({
            "kind": "opl_artifact_lifecycle_missing",
            "reason": "OPL artifact lifecycle projection refs have not been applied",
            "missing_refs": missing_projection_refs,
        })
    if summary.get("health_status") != "passed":
        issues.append({
            "kind": "opl_artifact_lifecycle_blocked",
            "reason": "OPL artifact lifecycle health is not passed",
            "health_status": summary.get("health_status"),
            "health_blockers": summary.get("health_blockers"),
        })
    return issues


def artifact_lifecycle_handoff_contract_summary(source_root: Path, *, required: bool) -> dict[str, Any]:
    contract_path = source_root.resolve() / ARTIFACT_LIFECYCLE_HANDOFF_CONTRACT_REF
    contract = safe_read_json(contract_path)
    if not isinstance(contract, dict):
        if not required:
            return {
                "required": False,
                "status": "not_applicable",
                "contract_ref": ARTIFACT_LIFECYCLE_HANDOFF_CONTRACT_REF.as_posix(),
                "contract_path": rel(contract_path, source_root),
                "issues": [],
            }
        return {
            "required": True,
            "status": "failed",
            "contract_ref": ARTIFACT_LIFECYCLE_HANDOFF_CONTRACT_REF.as_posix(),
            "contract_path": rel(contract_path, source_root),
            "issues": [{
                "kind": "artifact_lifecycle_handoff_contract_missing_or_invalid",
                "path": rel(contract_path, source_root),
                "reason": "contract JSON is missing or invalid",
            }],
        }

    issues: list[dict[str, Any]] = []
    if contract.get("surface_kind") != "bookforge_artifact_lifecycle_handoff_contract":
        issues.append({
            "kind": "artifact_lifecycle_handoff_contract_invalid",
            "path": rel(contract_path, source_root),
            "reason": "surface_kind must be bookforge_artifact_lifecycle_handoff_contract",
        })
    if contract.get("structural_gate_only") is not True:
        issues.append({
            "kind": "artifact_lifecycle_handoff_contract_invalid",
            "path": rel(contract_path, source_root),
            "reason": "structural_gate_only must be true",
        })

    projection_refs = contract.get("required_opl_projection_refs")
    missing_projection_refs = [
        ref
        for ref in REQUIRED_CONTRACT_PROJECTION_REFS
        if not isinstance(projection_refs, list) or ref not in projection_refs
    ]
    if missing_projection_refs:
        issues.append({
            "kind": "artifact_lifecycle_handoff_contract_invalid",
            "path": rel(contract_path, source_root),
            "reason": "required OPL projection refs are missing from the contract",
            "missing_refs": missing_projection_refs,
        })

    readback = contract.get("readback_surface")
    if not isinstance(readback, dict):
        readback = {}
    command = readback.get("command")
    if not isinstance(command, str) or "opl workspace artifact-lifecycle" not in command:
        issues.append({
            "kind": "artifact_lifecycle_handoff_contract_invalid",
            "path": rel(contract_path, source_root),
            "reason": "readback command must point to OPL workspace artifact-lifecycle",
        })
    if readback.get("dry_run_counts_as_workspace_apply_evidence") is not False:
        issues.append({
            "kind": "artifact_lifecycle_handoff_false_ready_guard_failed",
            "path": rel(contract_path, source_root),
            "field": "readback_surface.dry_run_counts_as_workspace_apply_evidence",
            "reason": "dry-run readback must not count as workspace apply evidence",
        })

    forbidden_authority = contract.get("forbidden_authority")
    if not isinstance(forbidden_authority, dict):
        forbidden_authority = {}
    bad_forbidden_flags = [
        flag
        for flag in REQUIRED_CONTRACT_FORBIDDEN_AUTHORITY_FLAGS
        if forbidden_authority.get(flag) is not False
    ]
    if bad_forbidden_flags:
        issues.append({
            "kind": "artifact_lifecycle_handoff_authority_guard_failed",
            "path": rel(contract_path, source_root),
            "fields": bad_forbidden_flags,
            "reason": "forbidden authority flags must be explicit false",
        })

    false_ready_guard = contract.get("false_ready_guard")
    if not isinstance(false_ready_guard, dict):
        false_ready_guard = {}
    bad_false_ready_flags = [
        flag
        for flag in REQUIRED_CONTRACT_FALSE_READY_FLAGS
        if false_ready_guard.get(flag) is not False
    ]
    if bad_false_ready_flags:
        issues.append({
            "kind": "artifact_lifecycle_handoff_false_ready_guard_failed",
            "path": rel(contract_path, source_root),
            "fields": bad_false_ready_flags,
            "reason": "false-ready guard flags must be explicit false",
        })

    return {
        "required": required,
        "status": "passed" if not issues else "failed",
        "contract_ref": ARTIFACT_LIFECYCLE_HANDOFF_CONTRACT_REF.as_posix(),
        "contract_path": rel(contract_path, source_root),
        "version": contract.get("version"),
        "structural_gate_only": contract.get("structural_gate_only"),
        "readback_command": command,
        "required_opl_projection_refs": projection_refs if isinstance(projection_refs, list) else None,
        "issues": issues,
    }
