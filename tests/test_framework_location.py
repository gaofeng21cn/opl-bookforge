#!/usr/bin/env python3
"""Run the verification entrypoint against isolated Framework layouts."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from stage_topology_cases.hosted_runtime_and_schema import framework_candidate_roots

ROOT = Path(__file__).resolve().parents[1]


class FrameworkLocationTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="obf-framework-location-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.repo = self.root / "projects/bookforge"
        (self.repo / "scripts").mkdir(parents=True)
        shutil.copyfile(ROOT / "scripts/verify.sh", self.repo / "scripts/verify.sh")
        (self.repo / "tests").symlink_to(ROOT / "tests", target_is_directory=True)
        self.bin = self.root / "commands"
        self.bin.mkdir()
        self.log = self.root / "calls.jsonl"
        recorder = (
            "import json, os, sys\n"
            "with open(os.environ['OBF_LOCATION_LOG'], 'a') as stream:\n"
            " stream.write(json.dumps({'argv': sys.argv, 'root': os.environ.get('OPL_FRAMEWORK_ROOT'), "
            "'bin': os.environ.get('OPL_BIN'), 'pythonpath': os.environ.get('PYTHONPATH')}) + '\\n')\n"
        )
        self.recorder = f"#!{sys.executable}\n" + recorder
        python = self.bin / "python3"
        python.write_text(
            f"#!{sys.executable}\nimport os, sys\n"
            f"if sys.argv[1] == '-': os.execv({sys.executable!r}, [{sys.executable!r}, *sys.argv[1:]])\n"
            + recorder
        )
        python.chmod(0o755)
        self.env = {key: value for key, value in os.environ.items()
                    if key not in {"OPL_BIN", "OPL_FRAMEWORK_ROOT", "PYTHONPATH"}}
        self.env.update(PATH=f"{self.bin}:/usr/bin:/bin", OBF_LOCATION_LOG=str(self.log),
                        PYTHONDONTWRITEBYTECODE="1")

    def framework(self, name):
        root = self.root / name
        (root / "bin").mkdir(parents=True)
        (root / "python/opl_framework").mkdir(parents=True)
        cli = root / "bin/opl"
        cli.write_text(self.recorder)
        cli.chmod(0o755)
        return root

    def run_entry(self, root, **configuration):
        result = subprocess.run(
            ["/bin/bash", str(self.repo / "scripts/verify.sh"), "structural"],
            cwd=self.root, env=self.env | configuration, text=True, capture_output=True,
        )
        if root is None:
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(self.log.exists(), "No checks should run with an invalid Framework")
            return result
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertGreater(len(calls), 2)
        for call in calls:
            self.assertEqual(Path(call["root"]).resolve(), root)
            self.assertEqual(Path(call["bin"]).resolve(), root / "bin/opl")
            self.assertEqual(call["pythonpath"].split(os.pathsep)[0], str(root / "python"))
        self.assertEqual([call["argv"][1:3] for call in calls[-2:]],
                         [["agents", "check"], ["workspace", "source-hygiene"]])
        return result

    def test_explicit_root_overrides_sibling_and_path(self):
        selected = self.framework("configured framework")
        sibling = self.framework("projects/one-person-lab")
        (self.bin / "opl").symlink_to(sibling / "bin/opl")
        self.run_entry(selected, OPL_FRAMEWORK_ROOT=str(selected))

    def test_explicit_bin_symlink_selects_its_framework(self):
        selected = self.framework("configured framework")
        link = self.bin / "selected-opl"
        link.symlink_to(selected / "bin/opl")
        self.framework("projects/one-person-lab")
        self.run_entry(selected, OPL_BIN=str(link))

    def test_sibling_checkout(self):
        self.run_entry(self.framework("projects/one-person-lab"))

    def test_path_symlink(self):
        selected = self.framework("installed framework")
        (self.bin / "opl").symlink_to(selected / "bin/opl")
        self.run_entry(selected)

    def test_conflicting_explicit_configuration_stops_before_checks(self):
        first, second = self.framework("first"), self.framework("second")
        result = self.run_entry(None, OPL_FRAMEWORK_ROOT=str(first), OPL_BIN=str(second / "bin/opl"))
        self.assertIn("must select the same Framework", result.stderr)

    def test_missing_explicit_framework_does_not_fall_back(self):
        self.framework("projects/one-person-lab")
        result = self.run_entry(None, OPL_FRAMEWORK_ROOT=str(self.root / "missing"))
        self.assertIn("CLI and Python helpers are unavailable", result.stderr)

    def test_missing_explicit_binary_stops_before_checks(self):
        selected = self.framework("configured framework")
        result = self.run_entry(None, OPL_BIN=str(selected / "bin/missing"))
        self.assertIn("CLI and Python helpers are unavailable", result.stderr)

    def test_shallow_checkout_can_resolve_candidates(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertIn(Path("/one-person-lab"), framework_candidate_roots(Path("/bookforge")))


if __name__ == "__main__":
    unittest.main()
