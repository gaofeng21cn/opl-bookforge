#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
lane="${1:-default}"

export PYTHONDONTWRITEBYTECODE=1
resolved_paths="$(python3 - "${repo_dir}" <<'PY'
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

explicit_sdk = os.environ.get("OPL_PYTHON_SDK_ROOT")
for root in roots:
    configured_bin = os.environ.get("OPL_BIN")
    binary = (shutil.which(configured_bin) or configured_bin) if configured_bin else root / "bin/opl"
    sdk_candidates = [
        Path(explicit_sdk) if explicit_sdk else None,
        root / "sdks/python-client/src",
    ]
    sdk_dir = next((p for p in sdk_candidates if p is not None and (p / "opl_client").is_dir()), None)
    if os.access(binary, os.X_OK) and sdk_dir is not None:
        print(f"{root}\t{binary}\t{sdk_dir}")
        break
else:
    raise SystemExit("Framework v2 CLI and opl_client SDK are unavailable; set OPL_BIN, OPL_FRAMEWORK_ROOT, or OPL_PYTHON_SDK_ROOT.")
PY
)"
IFS=$'\t' read -r framework_root opl_bin sdk_root <<<"${resolved_paths}"
export OPL_FRAMEWORK_ROOT="${framework_root}"
export OPL_BIN="${opl_bin}"
export OPL_PYTHON_SDK_ROOT="${sdk_root}"
export PYTHONPATH="${sdk_root}${PYTHONPATH:+:${PYTHONPATH}}"

run_policy_tests() {
  python3 "${repo_dir}/tests/test_framework_location.py"
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
  "${opl_bin}" pack inspect "${repo_dir}" --json
  "${opl_bin}" pack build "${repo_dir}" --no-write-lock --json
}

run_helper_tests() {
  python3 "${repo_dir}/runtime/native_helpers/bookforge_imagegen_asset.py" --self-test
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
    python3 "${repo_dir}/runtime/native_helpers/bookforge_imagegen_asset.py" --self-test
    python3 "${repo_dir}/tests/test_verify_helpers.py" --pdf-smoke
    python3 "${repo_dir}/tests/test_imagegen_host_asset_handler.py"
    ;;
  full)
    run_policy_tests
    run_structural_readback
    python3 "${repo_dir}/runtime/native_helpers/bookforge_imagegen_asset.py" --self-test
    python3 "${repo_dir}/tests/test_verify_helpers.py" --pdf-smoke
    python3 "${repo_dir}/tests/test_imagegen_host_asset_handler.py"
    ;;
  *)
    echo "Unknown lane: ${lane}" >&2
    echo "Usage: scripts/verify.sh [fast|structural|helpers|pdf|full-local|full]" >&2
    exit 1
    ;;
esac
