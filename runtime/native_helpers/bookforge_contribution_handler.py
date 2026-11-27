#!/usr/bin/env python3
"""OPL v2 contribution handler for OPL Book Forge (`obf`)."""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
from typing import Any

HELPER_DIR = Path(__file__).resolve().parent
if str(HELPER_DIR) not in sys.path:
    sys.path.insert(0, str(HELPER_DIR))

from _opl_artifact_helpers import ensure_opl_client  # noqa: E402
from bookforge_app_review import artifact_projection, object_file, read_review, select_book  # noqa: E402


def _fallback_read_stdin_json() -> dict[str, Any]:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("Expected JSON object on stdin")
    return parsed


def _fallback_write_json_stdout(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, separators=(",", ":")) + "\n")
    sys.stdout.flush()


try:
    ensure_opl_client()
    from opl_client import read_stdin_json, write_json_stdout  # noqa: E402
except ModuleNotFoundError:
    read_stdin_json = _fallback_read_stdin_json
    write_json_stdout = _fallback_write_json_stdout

REQUEST_SCHEMA_VERSION = "opl-package-app-contribution-request.v1"
SUPPORTED_REFS = {
    "obf.workspace.v1#status",
    "obf.workspace.v1#artifacts",
    "obf.workspace.v1#review",
}


def _read_workspace_summary(ref: str, input_payload: dict[str, Any]) -> dict[str, Any]:
    if input_payload.get("workspace_path") or os.environ.get("OPL_PROFILE_WORKSPACE"):
        selection = select_book(input_payload)
        if isinstance(selection, dict):
            return selection
        root, project, entry, _ = selection
        book_id = entry["project_id"]
        item: dict[str, Any] = {
            "id": book_id,
            "title": entry.get("title", book_id),
            "project_root": entry["project_root"],
        }
        if ref == "obf.workspace.v1#artifacts":
            projection = artifact_projection(root, project, book_id)
            for field in ("artifacts", "current_refs"):
                item[field] = [
                    artifact for artifact in projection.get(field, [])
                    if isinstance(artifact, dict) and isinstance(artifact.get("ref"), str)
                    and (root / artifact["ref"]).resolve().is_relative_to(project)
                ]
        else:
            item["lifecycle"] = entry.get("lifecycle")
            if isinstance(pointer_ref := entry.get("current_stage_pointer_ref"), str):
                pointer_path = root / pointer_ref
                if pointer_path.is_file():
                    pointer = object_file(root, project, pointer_ref)
                    if pointer.get("surface_kind") == "opl_current_stage_pointer" and pointer.get("project_id") == book_id:
                        item["current_stage"] = pointer.get("current_stage")
        return {
            "state": "ready",
            "package_id": "obf",
            "ref": ref,
            "data": {"items": [item], "workspace_root": str(root)},
        }

    # Optional fallback to active opld workspace projection when running under opld.
    try:
        ensure_opl_client()
        from opl_client import OplClientError, connect
    except ModuleNotFoundError:
        return {
            "state": "unavailable",
            "reason": "workspace_selection_required",
            "package_id": "obf",
            "ref": ref,
        }

    try:
        with connect() as client:
            listed = client.workspace_list()
            workspaces = listed.get("workspaces", []) if isinstance(listed, dict) else []
            return {
                "state": "ready",
                "package_id": "obf",
                "ref": ref,
                "data": {"items": workspaces},
            }
    except (OSError, OplClientError):
        return {
            "state": "unavailable",
            "reason": "workspace_selection_required",
            "package_id": "obf",
            "ref": ref,
        }


def handle_request(request: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("Contribution request must be a JSON object.")
    schema_version = request.get("schema_version")
    if schema_version not in (None, REQUEST_SCHEMA_VERSION):
        raise ValueError(f"Unsupported schema_version: {schema_version}")
    package_id = request.get("package_id")
    if package_id not in (None, "obf"):
        raise ValueError(f"Unsupported package_id: {package_id}")
    operation = request.get("operation", "read")
    if operation != "read":
        raise ValueError(f"Unsupported operation for obf: {operation}")
    ref = request.get("ref")
    if ref not in SUPPORTED_REFS:
        raise ValueError(f"Unsupported contribution ref: {ref}")
    raw_input = request.get("input")
    input_payload = raw_input if isinstance(raw_input, dict) else {}
    if ref == "obf.workspace.v1#review":
        return read_review(input_payload)
    return _read_workspace_summary(ref, input_payload)


def main() -> int:
    try:
        request = read_stdin_json()
        result = handle_request(request)
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
        result = {
            "state": "unavailable",
            "reason": "book_contribution_unavailable",
            "message": str(error),
        }
    write_json_stdout(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
