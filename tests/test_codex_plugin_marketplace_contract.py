#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

CONFIGURED_CODEX_PLUGIN_CARRIER = {
    "kind": "codex_plugin_manager",
    "plugin_selector": "opl-bookforge@opl-bookforge-local",
    "executor_route": "codex_cli",
    "marketplace_source": "gaofeng21cn/opl-bookforge",
    "publication_ref": (
        "ghcr.io/gaofeng21cn/one-person-lab-packages/obf:latest-stable"
    ),
}


def load_json(ref: str) -> dict:
    return json.loads((REPO_ROOT / ref).read_text(encoding="utf-8"))


def assert_configured_carrier_projection(
    package_manifest: dict, carrier_manifest: dict
) -> None:
    owner_carrier = package_manifest["codex_surface"].get(
        "configured_codex_plugin_carrier"
    )
    projected_carrier = carrier_manifest["codex_surface"].get(
        "configured_codex_plugin_carrier"
    )
    assert owner_carrier == CONFIGURED_CODEX_PLUGIN_CARRIER
    assert projected_carrier == owner_carrier


def assert_carrier_guard_rejects(
    package_manifest: dict, carrier_manifest: dict, label: str
) -> None:
    try:
        assert_configured_carrier_projection(package_manifest, carrier_manifest)
    except AssertionError:
        return
    raise AssertionError(f"configured carrier guard accepted {label}")


def main() -> int:
    marketplace = load_json(".agents/plugins/marketplace.json")
    plugin_manifest = load_json("plugins/opl-bookforge/.codex-plugin/plugin.json")
    portable_plugin_manifest = load_json("plugins/opl-bookforge/plugin.json")
    package_manifest = load_json("contracts/opl_agent_package_manifest.json")
    carrier_manifest = load_json("plugins/opl-bookforge/opl-package.json")
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    assert marketplace["name"] == "opl-bookforge-local"
    assert marketplace["interface"]["displayName"] == "OPL Book Forge"
    assert marketplace["plugins"] == [
        {
            "name": "opl-bookforge",
            "source": {
                "source": "local",
                "path": "./plugins/opl-bookforge",
            },
            "policy": {
                "installation": "AVAILABLE",
                "authentication": "ON_INSTALL",
            },
            "category": "Writing",
        }
    ]

    plugin = marketplace["plugins"][0]
    source_path = REPO_ROOT / plugin["source"]["path"]
    assert source_path.is_dir()
    assert plugin["name"] == plugin_manifest["name"] == "opl-bookforge"
    assert portable_plugin_manifest["$schema"] == (
        "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    )
    assert portable_plugin_manifest["name"] == plugin_manifest["name"]
    assert portable_plugin_manifest["version"] == plugin_manifest["version"]
    assert portable_plugin_manifest["extensions"]["com.openai"]["interface"] == (
        plugin_manifest["interface"]
    )
    assert "skills" not in portable_plugin_manifest
    assert not (source_path / "mcp.json").exists()
    assert CONFIGURED_CODEX_PLUGIN_CARRIER["plugin_selector"] == (
        f"{plugin['name']}@{marketplace['name']}"
    )
    assert plugin["category"] == plugin_manifest["interface"]["category"]
    assert package_manifest["agent_id"] == package_manifest["package_id"] == "obf"
    assert package_manifest["codex_surface"]["plugin_id"] == plugin["name"]
    assert_configured_carrier_projection(package_manifest, carrier_manifest)
    assert carrier_manifest == {
        "surface_kind": package_manifest["surface_kind"],
        "agent_id": package_manifest["agent_id"],
        "package_id": package_manifest["package_id"],
        "display_name": package_manifest["display_name"],
        "presentation": package_manifest["presentation"],
        "publisher": package_manifest["publisher"],
        "version": package_manifest["version"],
        "source": package_manifest["source"],
        "carrier_source_role": package_manifest["carrier_source_role"],
        "entrypoints": [],
        "codex_surface": {
            "plugin_id": package_manifest["codex_surface"]["plugin_id"],
            "plugin_source_path": ".",
            "configured_codex_plugin_carrier": CONFIGURED_CODEX_PLUGIN_CARRIER,
            "required_skill_ids": package_manifest["codex_surface"][
                "required_skill_ids"
            ],
        },
        "capability_dependencies": [],
    }
    assert carrier_manifest["version"] == plugin_manifest["version"]
    assert carrier_manifest["codex_surface"]["plugin_id"] == plugin_manifest["name"]

    missing_owner_carrier = deepcopy(package_manifest)
    missing_owner_carrier["codex_surface"].pop("configured_codex_plugin_carrier")
    assert_carrier_guard_rejects(
        missing_owner_carrier, carrier_manifest, "missing owner carrier"
    )

    missing_projected_carrier = deepcopy(carrier_manifest)
    missing_projected_carrier["codex_surface"].pop(
        "configured_codex_plugin_carrier"
    )
    assert_carrier_guard_rejects(
        package_manifest, missing_projected_carrier, "missing projected carrier"
    )

    mismatched_projected_carrier = deepcopy(carrier_manifest)
    mismatched_projected_carrier["codex_surface"][
        "configured_codex_plugin_carrier"
    ]["publication_ref"] = (
        "ghcr.io/gaofeng21cn/one-person-lab-packages/obf:0.3.7"
    )
    assert_carrier_guard_rejects(
        package_manifest, mismatched_projected_carrier, "mismatched carrier"
    )

    required_readme_fragments = (
        "## For Codex / Agents",
        'codex plugin marketplace add "$(pwd -P)" --json',
        "codex plugin marketplace list --json",
        "codex plugin list --marketplace opl-bookforge-local --available --json",
        "codex plugin add opl-bookforge@opl-bookforge-local --json",
        "codex plugin remove opl-bookforge@opl-bookforge-local --json",
        "codex plugin marketplace remove opl-bookforge-local --json",
        "opl packages status --package-id obf --json",
        "opl app state --profile fast --json",
        "do not prove that the complete OPL Package/runtime is",
        "Keep manuscript truth, quality/export verdicts, final artifact bytes,",
    )
    for fragment in required_readme_fragments:
        assert fragment in readme, fragment

    print(
        json.dumps(
            {
                "status": "passed",
                "marketplace": marketplace["name"],
                "plugin_id": plugin["name"],
                "package_id": package_manifest["package_id"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
