#!/usr/bin/env python3
"""Project Book Forge's domain resources into its native plugin carrier."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CARRIER = ROOT / "plugins/opl-bookforge"
RESOURCE_ROOTS = ("agent", "contracts", "runtime", "docs")


def resource_paths() -> list[Path]:
    tracked = subprocess.check_output(
        ["git", "ls-files", "-z", "--", *RESOURCE_ROOTS], cwd=ROOT
    ).decode().split("\0")
    return [Path(ref) for ref in tracked if ref and not ref.startswith((
        "docs/evidence/", "docs/history/", "docs/site/",
    ))] + [Path("docs/evidence/README.md"), Path("docs/history/README.md")]


def json_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    owner = json.loads((ROOT / "contracts/opl_agent_package_manifest.json").read_text())
    descriptor = {key: owner[key] for key in (
        "surface_kind", "agent_id", "package_id", "display_name", "presentation",
        "publisher", "version", "domain_descriptor_ref", "source", "carrier_source_role",
    )}
    descriptor["entrypoints"] = []
    descriptor["codex_surface"] = {"plugin_id": owner["codex_surface"]["plugin_id"],
        "plugin_source_path": ".", **{key: owner["codex_surface"][key] for key in (
            "configured_codex_plugin_carrier", "required_skill_ids",
            "app_contribution_abi", "app_contribution_adapter",
        )}}
    descriptor["app_contributions"] = owner["app_contributions"]
    descriptor["capability_dependencies"] = owner["capability_dependencies"]
    expected = {ref: (ROOT / ref).read_bytes() for ref in resource_paths()}
    icon = Path(owner["presentation"]["icon_ref"])
    expected[icon] = (ROOT / icon).read_bytes()
    expected[Path("skills/opl-bookforge/SKILL.md")] = (ROOT / "agent/primary_skill/SKILL.md").read_bytes()
    expected[Path("app-contribution-adapter.json")] = (ROOT / "app-contribution-adapter.json").read_bytes()
    expected[Path("opl-package.json")] = json_bytes(descriptor)
    for ref in (Path("plugin.json"), Path(".codex-plugin/plugin.json")):
        manifest = json.loads((CARRIER / ref).read_text())
        manifest["version"] = owner["version"]
        expected[ref] = json_bytes(manifest)
    stale = [p for name in RESOURCE_ROOTS for p in (CARRIER / name).rglob("*")
             if p.is_file() and p.relative_to(CARRIER) not in expected]
    drift = [str(ref) for ref, body in expected.items()
             if not (CARRIER / ref).is_file() or (CARRIER / ref).read_bytes() != body]
    if args.check:
        if drift or stale:
            raise SystemExit(json.dumps({"status": "stale", "changed": drift,
                "removed": [str(p.relative_to(CARRIER)) for p in stale]}))
    else:
        for name in RESOURCE_ROOTS:
            shutil.rmtree(CARRIER / name, ignore_errors=True)
        for ref, body in expected.items():
            target = CARRIER / ref
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
            source = ROOT / ref
            if source.is_file():
                target.chmod(source.stat().st_mode & 0o777)
    print(json.dumps({"status": "current" if args.check else "projected",
        "source_root": "plugins/opl-bookforge", "projected_files": len(expected),
        "installed": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
