#!/usr/bin/env python3
"""Exercise Book Forge's descriptor through Framework's installed discovery."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from stage_topology_cases.hosted_runtime_and_schema import framework_loader_module, framework_node_command

ROOT = Path(__file__).resolve().parents[1]


def discover(roots: list[Path]) -> list[dict]:
    loader = framework_loader_module(ROOT)
    tree = loader.parents[2]
    parser = tree / f"kernel/standard-agent-interface{loader.suffix}"
    discovery = tree / f"adapters/integration/standard-agent-interface-discovery{loader.suffix}"
    script = f"""
import {{ readStandardAgentDescriptorInterface }} from {json.dumps(parser.as_uri())};
import {{ readInstalledStandardAgentDescriptorForPackage }} from {json.dumps(discovery.as_uri())};
const result = {json.dumps([str(root) for root in roots])}.map(root => {{
  const parsed = readStandardAgentDescriptorInterface(root);
  const installed = readInstalledStandardAgentDescriptorForPackage('obf', () => ({{
    opl_agent_package_status: {{
      agent_id: 'obf', installed_package_count: 1,
      installed_carrier_readback: {{ lifecycle_authority: 'carrier_owned', source_ref: root }},
      installed_readiness: {{ installed: true, physical_status: 'available' }},
    }},
  }}));
  return {{ parsed, installed }};
}});
console.log(JSON.stringify(result));
"""
    result = subprocess.run(
        framework_node_command(loader, script),
        text=True, capture_output=True, check=True,
    )
    return json.loads(result.stdout)


class InstalledInventoryDiscoveryTest(unittest.TestCase):
    def test_canonical_and_carrier_expose_inventory_as_installed_agent(self):
        carrier = ROOT / "plugins/opl-bookforge"
        descriptor_ref = Path("contracts/domain_descriptor.json")
        self.assertEqual((ROOT / descriptor_ref).read_bytes(), (carrier / descriptor_ref).read_bytes())
        manifest = json.loads((ROOT / "contracts/opl_agent_package_manifest.json").read_text())
        for result in discover([ROOT, carrier]):
            for descriptor in (result["parsed"], result["installed"]):
                self.assertIsNotNone(descriptor)
                self.assertEqual(descriptor["kind"], "agent")
                self.assertEqual(descriptor["agent_id"], manifest["agent_id"])
                self.assertEqual(descriptor["package_id"], manifest["package_id"])
                self.assertEqual(descriptor["domain_id"], "opl-bookforge")
                inventory = descriptor["interface"]["inventory_projection"]
                self.assertEqual(inventory["relative_path"], "workspace_index.json")
                self.assertEqual(inventory["items_pointer"], "/projects")

    def test_pre_fix_descriptor_is_rejected_by_installed_discovery(self):
        descriptor = json.loads((ROOT / "contracts/domain_descriptor.json").read_text())
        for key in ("kind", "agent_id", "package_id"):
            descriptor.pop(key)
        with tempfile.TemporaryDirectory(prefix="obf-descriptor-regression-") as temp:
            root = Path(temp)
            (root / "contracts").mkdir()
            (root / "contracts/domain_descriptor.json").write_text(json.dumps(descriptor))
            result = discover([root])[0]
        self.assertIsNotNone(result["parsed"]["interface"]["inventory_projection"])
        self.assertIsNone(result["parsed"]["kind"])
        self.assertIsNone(result["installed"])


if __name__ == "__main__":
    unittest.main()
