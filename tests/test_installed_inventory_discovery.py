#!/usr/bin/env python3
"""Verify Book Forge's v2 manifest and workspace inventory discovery contract."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstalledInventoryDiscoveryTest(unittest.TestCase):
    def test_v2_manifest_and_domain_descriptor_expose_inventory_projection(self):
        manifest = json.loads((ROOT / "opl-package.json").read_text(encoding="utf-8"))
        descriptor = json.loads((ROOT / "contracts/domain_descriptor.json").read_text(encoding="utf-8"))

        self.assertEqual(manifest["schema_version"], "opl.package.v2")
        self.assertEqual(manifest["identity"]["id"], descriptor["agent_id"])
        self.assertEqual(manifest["identity"]["id"], descriptor["package_id"])
        self.assertEqual(descriptor["kind"], "agent")
        self.assertEqual(descriptor["domain_id"], "opl-bookforge")

        inventory = descriptor["standard_agent_interface"]["inventory_projection"]
        self.assertEqual(inventory["relative_path"], "workspace_index.json")
        self.assertEqual(inventory["items_pointer"], "/projects")

        handler_script = ROOT / manifest["provides"]["contribution_handler"]["argv"][1]
        self.assertTrue(handler_script.is_file())

    def test_contribution_handler_reads_workspace_inventory_projection(self):
        with tempfile.TemporaryDirectory(prefix="obf-inventory-discovery-") as temp:
            ws = Path(temp).resolve()
            (ws / "projects/book-1").mkdir(parents=True)
            (ws / "workspace_index.json").write_text(
                json.dumps({"projects": [{"project_id": "book-1", "project_root": "projects/book-1", "title": "Book 1"}]}),
                encoding="utf-8",
            )
            request = {
                "schema_version": "opl-package-app-contribution-request.v1",
                "operation": "read",
                "package_id": "obf",
                "ref": "obf.workspace.v1#status",
                "input": {},
            }
            completed = subprocess.run(
                [sys.executable, str(ROOT / "runtime/native_helpers/bookforge_contribution_handler.py")],
                input=json.dumps(request),
                text=True,
                capture_output=True,
                env={**os.environ, "OPL_PROFILE_WORKSPACE": str(ws)},
                check=True,
            )
            response = json.loads(completed.stdout)
            self.assertEqual(response["state"], "ready")
            self.assertEqual(response["package_id"], "obf")
            self.assertEqual(response["data"]["items"][0]["id"], "book-1")


if __name__ == "__main__":
    unittest.main()
