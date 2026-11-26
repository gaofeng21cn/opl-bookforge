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
from bookforge_app_review import object_file, read_review  # noqa: E402

ensure_opl_client()
from opl_client import OplClientError, connect, read_stdin_json, write_json_stdout  # noqa: E402

REQUEST_SCHEMA_VERSION = "opl-package-app-contribution-request.v1"
SUPPORTED_REFS = {
    "obf.workspace.v1#status",
    "obf.workspace.v1#artifacts",
    "obf.workspace.v1#review",
}


def _read_workspace_summary(ref: str, input_payload: dict[str, Any]) -> dict[str, Any]:
    workspace_env = os.environ.get("OPL_PROFILE_WORKSPACE", "").strip()
    if workspace_env:
        workspace_path = Path(workspace_env)
        if not workspace_path.is_absolute():
            return {"state": "unavailable", "reason": "workspace_selection_required"}
        root = workspace_path.resolve(strict=True)
        inventory = object_file(root, root, "workspace_index.json")
        projects = [p for p in inventory.get("projects", []) if isinstance(p, dict)]
        book_id = input_payload.get("book_id")
        if book_id:
            projects = [p for p in projects if p.get("project_id") == book_id]
        items: list[dict[str, Any]] = []
        for entry in projects:
            pid = entry.get("project_id")
            proot = entry.get("project_root")
            if not isinstance(pid, str) or not isinstance(proot, str):
                continue
            project_dir = (root / proot).resolve()
            if not project_dir.is_relative_to(root):
                continue
            item: dict[str, Any] = {
                "id": pid,
                "title": entry.get("title", pid),
                "project_root": proot,
            }
            if ref == "obf.workspace.v1#artifacts":
                lifecycle_file = project_dir / "control/opl/artifact_lifecycle/output_lifecycle.json"
                if lifecycle_file.is_file():
                    lifecycle = object_file(root, project_dir, lifecycle_file.relative_to(root).as_posix())
                    item["artifacts"] = lifecycle.get("artifacts", [])
                    item["current_refs"] = lifecycle.get("current_refs", [])
                else:
                    item["artifacts"] = []
                    item["current_refs"] = []
            items.append(item)
        return {
            "state": "ready",
            "package_id": "obf",
            "ref": ref,
            "data": {"items": items, "workspace_root": str(root)},
        }

    # Optional fallback to active opld workspace projection when running under opld.
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
