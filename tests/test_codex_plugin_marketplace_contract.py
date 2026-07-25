#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_json(ref: str) -> dict:
    return json.loads((REPO_ROOT / ref).read_text(encoding="utf-8"))


def main() -> int:
    marketplace = load_json(".agents/plugins/marketplace.json")
    plugin_manifest = load_json("plugins/opl-bookforge/.codex-plugin/plugin.json")
    package_manifest = load_json("contracts/opl_agent_package_manifest.json")
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
    assert plugin["category"] == plugin_manifest["interface"]["category"]
    assert package_manifest["agent_id"] == package_manifest["package_id"] == "obf"
    assert package_manifest["codex_surface"]["plugin_id"] == plugin["name"]

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
