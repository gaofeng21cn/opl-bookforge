#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
opl_bin="${OPL_BIN:-/Users/gaofeng/workspace/one-person-lab/bin/opl}"
lane="${1:-default}"
helper_args=()

case "${lane}" in
  default|fast|structural)
    ;;
  pdf-smoke|full)
    helper_args+=(--pdf-smoke)
    ;;
  *)
    echo "Unknown lane: ${lane}" >&2
    echo "Usage: scripts/verify.sh [default|fast|structural|pdf-smoke|full]" >&2
    exit 1
    ;;
esac

export PYTHONDONTWRITEBYTECODE=1

"${opl_bin}" workspace source-hygiene --source-root "${repo_dir}" --json
python3 "${repo_dir}/tests/test_stage_topology.py"
python3 "${repo_dir}/tests/test_temporal_stage_run_consumption_policy.py"

"${opl_bin}" agents scaffold --validate "${repo_dir}" --json
"${opl_bin}" agents interfaces --repo-dir "${repo_dir}" --json

"${opl_bin}" pack native-helper probe --descriptor "${repo_dir}/runtime/native_helpers/bookforge_pdf_export.native-helper-probe.json" --json
"${opl_bin}" pack native-helper probe --descriptor "${repo_dir}/runtime/native_helpers/bookforge_imagegen_asset.native-helper-probe.json" --json
python3 "${repo_dir}/tests/test_verify_helpers.py" "${helper_args[@]}"
python3 "${repo_dir}/runtime/native_helpers/bookforge_imagegen_asset.py" --self-test
python3 "${repo_dir}/tests/test_imagegen_opl_executor_adapter.py"

"${opl_bin}" workspace source-hygiene --source-root "${repo_dir}" --json
