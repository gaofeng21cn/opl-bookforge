#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
opl_bin="${OPL_BIN:-/Users/gaofeng/workspace/one-person-lab/bin/opl}"
lane="${1:-default}"

export PYTHONDONTWRITEBYTECODE=1

run_policy_tests() {
  python3 "${repo_dir}/tests/test_foundry_agent_os_domain_kernel_manifest_contract.py"
  python3 "${repo_dir}/tests/test_stage_quality_cycle_policy.py"
  python3 "${repo_dir}/tests/test_stage_topology.py"
  python3 "${repo_dir}/tests/test_temporal_stage_run_consumption_policy.py"
}

run_structural_readback() {
  "${opl_bin}" agents scaffold --validate "${repo_dir}" --json
  "${opl_bin}" agents interfaces --repo-dir "${repo_dir}" --json
  "${opl_bin}" workspace source-hygiene --source-root "${repo_dir}" --json
}

run_helper_tests() {
  "${opl_bin}" pack native-helper probe --descriptor "${repo_dir}/runtime/native_helpers/bookforge_pdf_export.native-helper-probe.json" --json
  "${opl_bin}" pack native-helper probe --descriptor "${repo_dir}/runtime/native_helpers/bookforge_imagegen_asset.native-helper-probe.json" --json
  python3 "${repo_dir}/tests/test_verify_helpers.py"
  python3 "${repo_dir}/tests/test_imagegen_opl_executor_adapter.py"
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
  full)
    run_policy_tests
    run_structural_readback
    "${opl_bin}" pack native-helper probe --descriptor "${repo_dir}/runtime/native_helpers/bookforge_pdf_export.native-helper-probe.json" --json
    "${opl_bin}" pack native-helper probe --descriptor "${repo_dir}/runtime/native_helpers/bookforge_imagegen_asset.native-helper-probe.json" --json
    python3 "${repo_dir}/tests/test_verify_helpers.py" --pdf-smoke
    python3 "${repo_dir}/tests/test_imagegen_opl_executor_adapter.py"
    ;;
  *)
    echo "Unknown lane: ${lane}" >&2
    echo "Usage: scripts/verify.sh [fast|structural|helpers|pdf|full]" >&2
    exit 1
    ;;
esac
