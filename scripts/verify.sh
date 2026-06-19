#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
opl_bin="/Users/gaofeng/workspace/one-person-lab/bin/opl"

"${opl_bin}" agents scaffold --validate "${repo_dir}" --json
"${opl_bin}" agents interfaces --repo-dir "${repo_dir}" --json

python3 "${repo_dir}/runtime/native_helpers/bookforge_pdf_export.py" --doctor
python3 "${repo_dir}/runtime/native_helpers/bookforge_imagegen_asset.py" --doctor
python3 "${repo_dir}/runtime/native_helpers/bookforge_imagegen_asset.py" --self-test

image_tmp_dir="$(mktemp -d)"
python3 - "${image_tmp_dir}" <<'PY'
import json
import sys
from pathlib import Path
root = Path(sys.argv[1])
manifest = {
    "surface_kind": "bookforge_figure_asset_manifest",
    "version": "bookforge-figure-asset-manifest.v1",
    "figures": [
        {
            "id": "verify-figure",
            "title": "图 0-1：Verify Figure",
            "chapter": "验证",
            "required": True,
            "project_local_path": "artifacts/figures/verify-figure.png",
            "asset_status": "planned",
            "blocker_kind": "imagegen_asset_not_generated",
        }
    ],
}
path = root / "artifacts/stage_outputs/book-materialization/figure-asset-manifest.json"
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
python3 "${repo_dir}/runtime/native_helpers/bookforge_imagegen_asset.py" \
  --mock \
  --root "${image_tmp_dir}" \
  --figure-id verify-figure \
  --title "图 0-1：Verify Figure" \
  --prompt "mock manifest sync smoke" \
  --output-file artifacts/figures/verify-figure.png \
  --manifest artifacts/figures/verify-figure.receipt.json \
  --asset-manifest artifacts/stage_outputs/book-materialization/figure-asset-manifest.json
python3 "${repo_dir}/runtime/native_helpers/bookforge_imagegen_asset.py" \
  --update-asset-manifest \
  --root "${image_tmp_dir}" \
  --receipt-file artifacts/figures/verify-figure.receipt.json \
  --asset-manifest artifacts/stage_outputs/book-materialization/figure-asset-manifest.json
python3 - "${image_tmp_dir}" <<'PY'
import json
import sys
from pathlib import Path
root = Path(sys.argv[1])
payload = json.loads((root / "artifacts/stage_outputs/book-materialization/figure-asset-manifest.json").read_text(encoding="utf-8"))
item = payload["figures"][0]
assert item["asset_status"] == "asset_ready", item
assert item["receipt_ref"] == "artifacts/figures/verify-figure.receipt.json", item
assert item["project_local_path"] == "artifacts/figures/verify-figure.png", item
assert (root / item["project_local_path"]).exists(), item
PY
rm -rf "${image_tmp_dir}"

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
    --artifact-role review_pdf

  if python3 "${repo_dir}/runtime/native_helpers/bookforge_pdf_export.py" \
    --root "${tmp_dir}" \
    --source-md "${tmp_dir}/sample.md" \
    --output-pdf "${tmp_dir}/sample-proof-missing-evidence.pdf" \
    --manifest "${tmp_dir}/proof-missing-evidence.json" \
    --artifact-role publication_proof; then
    echo "publication_proof without design/inspection evidence unexpectedly passed" >&2
    exit 1
  fi

  cat >"${tmp_dir}/publication-design.json" <<'EOF'
{
  "page_geometry": "A5",
  "typography_hierarchy": "defined",
  "caption_style": "defined",
  "figure_treatment": "defined",
  "table_treatment": "defined",
  "callout_style": "defined",
  "headers_footers": "defined",
  "page_numbering": "defined",
  "visual_rhythm": "defined",
  "rendered_page_inspection_plan": "sample pages"
}
EOF
  cat >"${tmp_dir}/rendered-page-inspection.json" <<'EOF'
{
  "nonblank_pages": 1,
  "overflow_or_clipping": false,
  "caption_figure_table_status": "passed",
  "callout_status": "passed",
  "heading_hierarchy_status": "passed",
  "headers_footers_status": "passed",
  "page_numbering_status": "passed",
  "visual_rhythm_status": "passed"
}
EOF
  python3 "${repo_dir}/runtime/native_helpers/bookforge_pdf_export.py" \
    --root "${tmp_dir}" \
    --source-md "${tmp_dir}/sample.md" \
    --output-pdf "${tmp_dir}/sample-proof.pdf" \
    --manifest "${tmp_dir}/proof-manifest.json" \
    --render-dir "${tmp_dir}/rendered-proof-pages" \
    --render-prefix proof-page \
    --artifact-role publication_proof \
    --publication-design-profile "${tmp_dir}/publication-design.json" \
    --rendered-page-inspection "${tmp_dir}/rendered-page-inspection.json"
fi
