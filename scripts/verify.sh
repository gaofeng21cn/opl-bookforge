#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
lane="${1:-default}"

export PYTHONDONTWRITEBYTECODE=1
framework_root="$(python3 - "${repo_dir}" <<'PY'
import os
from pathlib import Path
import shutil
import sys

repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "tests"))
from stage_topology_cases.hosted_runtime_and_schema import framework_candidate_roots

try:
    roots = framework_candidate_roots(repo)
except ValueError as error:
    raise SystemExit(str(error)) from error
for root in roots:
    configured_bin = os.environ.get("OPL_BIN")
    binary = (shutil.which(configured_bin) or configured_bin) if configured_bin else root / "bin/opl"
    if os.access(binary, os.X_OK) and (root / "python/opl_framework").is_dir():
        print(root)
        break
else:
    raise SystemExit("Framework CLI and Python helpers are unavailable; set OPL_BIN or OPL_FRAMEWORK_ROOT.")
PY
)"
export OPL_FRAMEWORK_ROOT="${framework_root}"
export OPL_BIN="${OPL_BIN:-${framework_root}/bin/opl}"
opl_bin="${OPL_BIN}"
export PYTHONPATH="${framework_root}/python${PYTHONPATH:+:${PYTHONPATH}}"

run_policy_tests() {
  python3 "${repo_dir}/tests/test_framework_location.py"
  python3 "${repo_dir}/scripts/project-carrier.py" --check
  python3 "${repo_dir}/tests/test_publication_bundle_contract.py"
  python3 "${repo_dir}/tests/test_codex_plugin_marketplace_contract.py"
  python3 "${repo_dir}/tests/test_foundry_agent_os_domain_kernel_manifest_contract.py"
  python3 "${repo_dir}/tests/test_installed_inventory_discovery.py"
  python3 "${repo_dir}/tests/test_stage_quality_cycle_policy.py"
  python3 "${repo_dir}/tests/test_epistemic_review_adoption.py"
  python3 "${repo_dir}/tests/test_stage_topology.py"
  python3 "${repo_dir}/tests/test_book_knowledge_scope.py"
  python3 "${repo_dir}/tests/test_book_review_contribution.py"
  python3 "${repo_dir}/tests/test_temporal_stage_run_consumption_policy.py"
}

run_structural_readback() {
  "${opl_bin}" agents check --repo "${repo_dir}" --json
  "${opl_bin}" workspace source-hygiene --source-root "${repo_dir}" --json
}

run_helper_tests() {
  "${opl_bin}" pack native-helper probe --descriptor "${repo_dir}/runtime/native_helpers/bookforge_pdf_export.native-helper-probe.json" --json
  "${opl_bin}" pack native-helper probe --descriptor "${repo_dir}/runtime/native_helpers/bookforge_imagegen_asset.native-helper-probe.json" --json
  python3 "${repo_dir}/tests/test_verify_helpers.py"
  python3 "${repo_dir}/tests/test_imagegen_host_asset_handler.py"
}

case "${lane}" in
  default|fast)
    run_policy_tests
    ;;
  structural)
    run_policy_tests
    run_structural_readback
    ;;
  helpers)
    run_helper_tests
    ;;
  pdf-smoke|pdf)
    python3 "${repo_dir}/tests/test_verify_helpers.py" --pdf-smoke-only
    ;;
  full-local)
    run_policy_tests
    "${opl_bin}" pack native-helper probe --descriptor "${repo_dir}/runtime/native_helpers/bookforge_pdf_export.native-helper-probe.json" --json
    "${opl_bin}" pack native-helper probe --descriptor "${repo_dir}/runtime/native_helpers/bookforge_imagegen_asset.native-helper-probe.json" --json
    python3 "${repo_dir}/tests/test_verify_helpers.py" --pdf-smoke
    python3 "${repo_dir}/tests/test_imagegen_host_asset_handler.py"
    ;;
  full)
    run_policy_tests
    run_structural_readback
    "${opl_bin}" pack native-helper probe --descriptor "${repo_dir}/runtime/native_helpers/bookforge_pdf_export.native-helper-probe.json" --json
    "${opl_bin}" pack native-helper probe --descriptor "${repo_dir}/runtime/native_helpers/bookforge_imagegen_asset.native-helper-probe.json" --json
    python3 "${repo_dir}/tests/test_verify_helpers.py" --pdf-smoke
    python3 "${repo_dir}/tests/test_imagegen_host_asset_handler.py"
    ;;
  *)
    echo "Unknown lane: ${lane}" >&2
    echo "Usage: scripts/verify.sh [fast|structural|helpers|pdf|full-local|full]" >&2
    exit 1
    ;;
esac
