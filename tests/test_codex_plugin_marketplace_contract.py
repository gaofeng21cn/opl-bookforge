#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_json(ref: str) -> dict:
    return json.loads((REPO_ROOT / ref).read_text(encoding="utf-8"))


def main() -> int:
    manifest = load_json("opl-package.json")
    package_json = load_json("package.json")

    # Zero legacy v1 mirrors must exist in the repository.
    for forbidden in (
        "plugins",
        ".codex-plugin",
        ".agents/plugins/marketplace.json",
        "contracts/carrier_projection.json",
        "contracts/opl_agent_package_manifest.json",
        "app-contribution-adapter.json",
        "scripts/project-carrier.py",
        "src/opl_framework",
    ):
        assert not (REPO_ROOT / forbidden).exists(), f"Legacy v1 artifact still exists: {forbidden}"

    assert manifest["schema_version"] == "opl.package.v2"
    identity = manifest["identity"]
    assert identity["id"] == "obf"
    assert identity["version"] == package_json["version"]
    assert identity["intent"] == "agent"
    assert identity["publisher"] == "one-person-lab"
    assert (REPO_ROOT / identity["icon"]).is_file()

    assert manifest["dependencies"]["opl_base"] == "^2.0.0"
    assert any(rt["name"] == "python" for rt in manifest["dependencies"]["runtimes"])
    assert manifest["permissions"]["workspace"]["access"] == "read_write"

    provides = manifest["provides"]
    assert provides["agent"]["stages_ref"] == "agent/stages/manifest.json"
    assert (REPO_ROOT / provides["agent"]["stages_ref"]).is_file()
    assert provides["skills"] == [
        {"id": "opl-bookforge", "path": "./skills/opl-bookforge", "exposure": "default"}
    ]
    skill_path = REPO_ROOT / "skills/opl-bookforge/SKILL.md"
    assert skill_path.is_file()
    assert skill_path.read_text(encoding="utf-8") == (REPO_ROOT / "agent/primary_skill/SKILL.md").read_text(encoding="utf-8")

    handler = provides["contribution_handler"]
    assert handler == {
        "kind": "cli",
        "argv": ["python3", "runtime/native_helpers/bookforge_contribution_handler.py"],
        "transport": "stdin_json_stdout_json",
    }
    assert (REPO_ROOT / handler["argv"][1]).is_file()

    views = manifest["ui"]["declarative"]["views"]
    assert [view["data_ref"] for view in views] == [
        "obf.workspace.v1#status",
        "obf.workspace.v1#artifacts",
        "obf.workspace.v1#review",
    ]
    assert manifest["distribution"]["oci"] == "ghcr.io/gaofeng21cn/one-person-lab-packages/obf"
    codex_hint = manifest["host_hints"]["codex"]
    assert codex_hint["sync_enabled"] is True
    assert codex_hint["plugin_name"] == "opl-bookforge"
    assert codex_hint["category"] == "Writing"

    print(
        json.dumps(
            {
                "status": "passed",
                "schema_version": manifest["schema_version"],
                "plugin_name": codex_hint["plugin_name"],
                "package_id": identity["id"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
