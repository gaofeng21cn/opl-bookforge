#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
opl_bin="/Users/gaofeng/workspace/one-person-lab/bin/opl"

"${opl_bin}" agents scaffold --validate "${repo_dir}" --json
"${opl_bin}" agents interfaces --repo-dir "${repo_dir}" --json

python3 "${repo_dir}/runtime/native_helpers/bookforge_pdf_export.py" --doctor
python3 "${repo_dir}/runtime/native_helpers/bookforge_imagegen_asset.py" --doctor
python3 "${repo_dir}/runtime/native_helpers/bookforge_imagegen_asset.py" --self-test

if command -v pandoc >/dev/null 2>&1 && command -v xelatex >/dev/null 2>&1; then
  tmp_dir="$(mktemp -d)"
  trap 'rm -rf "${tmp_dir}"' EXIT
  cat >"${tmp_dir}/sample.md" <<'EOF'
---
title: "BookForge PDF Smoke"
author: "OPL BookForge"
lang: zh-CN
mainfont: "Noto Sans CJK SC"
CJKmainfont: "Noto Sans CJK SC"
---

# 第一章

这是 OPL BookForge PDF 出口的中文 smoke test。
EOF
  python3 "${repo_dir}/runtime/native_helpers/bookforge_pdf_export.py" \
    --root "${tmp_dir}" \
    --source-md "${tmp_dir}/sample.md" \
    --output-pdf "${tmp_dir}/sample.pdf" \
    --manifest "${tmp_dir}/manifest.json" \
    --render-dir "${tmp_dir}/rendered-pages" \
    --render-prefix sample-page \
    --artifact-role verify_smoke_not_publication
fi
