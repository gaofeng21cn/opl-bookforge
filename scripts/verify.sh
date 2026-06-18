#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
opl_bin="/Users/gaofeng/workspace/one-person-lab/bin/opl"

"${opl_bin}" agents scaffold --validate "${repo_dir}" --json
"${opl_bin}" agents interfaces --repo-dir "${repo_dir}" --json
