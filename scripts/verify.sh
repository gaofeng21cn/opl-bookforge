#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
opl_bin="${OPL_BIN:-/Users/gaofeng/workspace/one-person-lab/bin/opl}"

"${opl_bin}" agents scaffold --validate "${repo_dir}" --json
"${opl_bin}" agents interfaces --repo-dir "${repo_dir}" --json

python3 "${repo_dir}/runtime/native_helpers/bookforge_pdf_export.py" --doctor
python3 - "${repo_dir}" <<'PY'
import importlib.util
import sys
from pathlib import Path

repo = Path(sys.argv[1])
module_path = repo / "runtime/native_helpers/bookforge_pdf_export.py"
spec = importlib.util.spec_from_file_location("bookforge_pdf_export", module_path)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

base_args = (
    Path("sample.md"),
    Path("sample.pdf"),
    None,
    [],
    [Path(".")],
    [],
)
numbered_command, blocker = module.pandoc_xelatex_command(*base_args, number_sections=True)
assert blocker is None, blocker
assert "--number-sections" in numbered_command, numbered_command

unnumbered_command, blocker = module.pandoc_xelatex_command(*base_args, number_sections=False)
assert blocker is None, blocker
assert "--number-sections" not in unnumbered_command, unnumbered_command
PY
python3 "${repo_dir}/runtime/native_helpers/bookforge_imagegen_asset.py" --doctor
python3 "${repo_dir}/runtime/native_helpers/bookforge_imagegen_asset.py" --self-test
python3 "${repo_dir}/runtime/native_helpers/bookforge_project_hygiene.py" --self-test

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
date: "2026-06-19"
---

# 第一章

这是 OPL BookForge PDF 出口的中文 smoke test。

> 审阅 PDF 可以检查内容连续性；出版 proof 还要检查页面节奏、图表、页眉页码和视觉层级。

## 图表与页面节奏

出版级电子书不能只有默认正文灰度。BookForge 的出版 profile 应当给标题、表格、引用块、图注和页码一个稳定层级。

| Artifact | Gate | Evidence |
| --- | --- | --- |
| review_pdf | readable | compile and render |
| publication_proof | designed | profile and inspection |
| final_export | accepted | owner receipt |

![图 0-1：出版 proof 图片解析 smoke](artifacts/figures/smoke-figure.png)
EOF
  mkdir -p "${tmp_dir}/artifacts/figures"
  python3 "${repo_dir}/runtime/native_helpers/bookforge_imagegen_asset.py" \
    --mock \
    --root "${tmp_dir}" \
    --figure-id smoke-figure \
    --title "图 0-1：出版 proof 图片解析 smoke" \
    --prompt "mock publication proof figure resource path smoke" \
    --output-file artifacts/figures/smoke-figure.png \
    --manifest artifacts/figures/smoke-figure.receipt.json
  cat >"${tmp_dir}/figure-asset-manifest.json" <<'EOF'
{
  "surface_kind": "bookforge_figure_asset_manifest",
  "version": "bookforge-figure-asset-manifest.v1",
  "figures": [
    {
      "id": "smoke-figure",
      "title": "图 0-1：出版 proof 图片解析 smoke",
      "required": true,
      "asset_status": "asset_ready",
      "project_local_path": "artifacts/figures/smoke-figure.png"
    }
  ]
}
EOF
  python3 "${repo_dir}/runtime/native_helpers/bookforge_pdf_export.py" \
    --root "${tmp_dir}" \
    --source-md "${tmp_dir}/sample.md" \
    --output-pdf "${tmp_dir}/sample.pdf" \
    --manifest "${tmp_dir}/manifest.json" \
    --render-dir "${tmp_dir}/rendered-pages" \
    --render-prefix sample-page \
    --artifact-role review_pdf
  python3 - "${tmp_dir}" <<'PY'
import json
import sys
from pathlib import Path
root = Path(sys.argv[1])
payload = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
assert payload["status"] == "generated", payload
assert payload["artifact_role"] == "review_pdf", payload
assert payload["artifact_gate"]["status"] == "passed", payload["artifact_gate"]
assert payload["artifact_gate"]["claim_boundary"]["review_pdf_counts_as_publication_proof"] is False, payload["artifact_gate"]
PY

  if python3 "${repo_dir}/runtime/native_helpers/bookforge_pdf_export.py" \
    --root "${tmp_dir}" \
    --source-md "${tmp_dir}/sample.md" \
    --output-pdf "${tmp_dir}/sample-proof-missing-evidence.pdf" \
    --manifest "${tmp_dir}/proof-missing-evidence.json" \
    --artifact-role publication_proof; then
    echo "publication_proof without design/inspection evidence unexpectedly passed" >&2
    exit 1
  fi
  cat >"${tmp_dir}/remote-image.md" <<'EOF'
---
title: "Remote Image Blocker"
lang: zh-CN
---

# 第一章

![远程图片不应作为出版 proof 资产](https://example.com/remote.png)
EOF

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
  cat >"${tmp_dir}/rendered-page-inspection-incomplete.json" <<'EOF'
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
  if python3 "${repo_dir}/runtime/native_helpers/bookforge_pdf_export.py" \
    --root "${tmp_dir}" \
    --source-md "${tmp_dir}/sample.md" \
    --output-pdf "${tmp_dir}/sample-proof-incomplete-inspection.pdf" \
    --manifest "${tmp_dir}/proof-incomplete-inspection.json" \
    --render-dir "${tmp_dir}/rendered-incomplete-proof-pages" \
    --render-prefix incomplete-proof-page \
    --artifact-role publication_proof \
    --publication-design-profile "${tmp_dir}/publication-design.json" \
    --rendered-page-inspection "${tmp_dir}/rendered-page-inspection-incomplete.json" \
    --figure-asset-manifest "${tmp_dir}/figure-asset-manifest.json"; then
    echo "publication_proof with incomplete machine proof QA unexpectedly passed" >&2
    exit 1
  fi
  python3 - "${tmp_dir}" <<'PY'
import json
import sys
from pathlib import Path
root = Path(sys.argv[1])
payload = json.loads((root / "proof-incomplete-inspection.json").read_text(encoding="utf-8"))
blocker_types = {item["blocker_type"] for item in payload["artifact_gate"]["blockers"]}
assert "rendered_page_inspection_incomplete" in blocker_types, payload["artifact_gate"]
PY
  cat >"${tmp_dir}/rendered-page-inspection.json" <<'EOF'
{
  "nonblank_pages": 1,
  "overflow_or_clipping": false,
  "caption_figure_table_status": "passed",
  "callout_status": "passed",
  "heading_hierarchy_status": "passed",
  "headers_footers_status": "passed",
  "page_numbering_status": "passed",
  "visual_rhythm_status": "passed",
  "embedded_font_status": "passed",
  "page_density_status": "passed",
  "trailing_whitespace_status": "passed",
  "rendered_page_size_status": "passed",
  "sample_page_roles_status": "passed",
  "checklist_refs_status": "passed"
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
    --rendered-page-inspection "${tmp_dir}/rendered-page-inspection.json" \
    --figure-asset-manifest "${tmp_dir}/figure-asset-manifest.json"
  if python3 "${repo_dir}/runtime/native_helpers/bookforge_pdf_export.py" \
    --root "${tmp_dir}" \
    --source-md "${tmp_dir}/remote-image.md" \
    --output-pdf "${tmp_dir}/remote-image-proof.pdf" \
    --manifest "${tmp_dir}/remote-image-proof-manifest.json" \
    --render-dir "${tmp_dir}/rendered-remote-image-proof-pages" \
    --render-prefix remote-image-proof-page \
    --artifact-role publication_proof \
    --publication-design-profile "${tmp_dir}/publication-design.json" \
    --rendered-page-inspection "${tmp_dir}/rendered-page-inspection.json"; then
    echo "publication_proof with external image ref unexpectedly passed" >&2
    exit 1
  fi
  python3 - "${tmp_dir}" <<'PY'
import json
import sys
from pathlib import Path
root = Path(sys.argv[1])
payload = json.loads((root / "remote-image-proof-manifest.json").read_text(encoding="utf-8"))
blocker_types = {item["blocker_type"] for item in payload["artifact_gate"]["blockers"]}
assert "markdown_image_ref_not_project_local" in blocker_types, payload["artifact_gate"]
PY

  python3 "${repo_dir}/runtime/native_helpers/bookforge_pdf_export.py" \
    --root "${tmp_dir}" \
    --source-md "${tmp_dir}/sample.md" \
    --output-pdf "${tmp_dir}/sample-bundled-profile-proof.pdf" \
    --manifest "${tmp_dir}/bundled-profile-proof-manifest.json" \
    --render-dir "${tmp_dir}/rendered-bundled-profile-pages" \
    --render-prefix bundled-proof-page \
    --artifact-role publication_proof \
    --write-rendered-page-inspection "${tmp_dir}/auto-rendered-page-inspection.json" \
    --figure-asset-manifest "${tmp_dir}/figure-asset-manifest.json"
  python3 - "${tmp_dir}" <<'PY'
import json
import sys
from pathlib import Path
root = Path(sys.argv[1])
payload = json.loads((root / "bundled-profile-proof-manifest.json").read_text(encoding="utf-8"))
auto = json.loads((root / "auto-rendered-page-inspection.json").read_text(encoding="utf-8"))
assert payload["status"] == "generated", payload
assert payload["artifact_gate"]["status"] == "passed", payload["artifact_gate"]
assert payload["publication_profile"]["profile_id"] == "bookforge-zh-publication-proof", payload["publication_profile"]
assert payload["markdown_image_refs"]["total"] == 1, payload["markdown_image_refs"]
assert payload["markdown_image_refs"]["missing_count"] == 0, payload["markdown_image_refs"]
assert payload["figure_asset_manifest_summary"]["ready_required_count"] == 1, payload["figure_asset_manifest_summary"]
assert payload["artifact_gate"]["evidence_refs"]["rendered_page_inspection"] == "auto-rendered-page-inspection.json", payload["artifact_gate"]
assert auto["inspection_kind"] == "machine_baseline", auto
assert auto["embedded_font_status"] == "passed", auto
assert auto["embedded_font_inspection"]["embedded_font_count"] > 0, auto
assert auto["page_density_status"] in {"passed", "checked_with_warnings"}, auto
assert auto["trailing_whitespace_status"] in {"passed", "checked_with_warnings"}, auto
assert auto["rendered_page_size_status"] == "passed", auto
assert auto["sample_page_roles_status"] == "passed", auto
assert auto["checklist_refs_status"] == "passed", auto
assert "front_matter" in auto["sample_page_roles"], auto
assert "embedded_fonts" in auto["checklist_refs"], auto
assert auto["nonblank_pages"] == len(payload["rendered_pages"]), auto
assert payload["rendered_pages"], payload
for ref in payload["rendered_pages"]:
    path = root / ref
    assert path.exists() and path.stat().st_size > 1000, ref
PY
fi


python3 - "${repo_dir}" <<'PY'
import json
import sys
from pathlib import Path

repo = Path(sys.argv[1])
profile = json.loads((repo / "runtime/native_helpers/pdf_profiles/bookforge-zh-publication-proof.json").read_text(encoding="utf-8"))
tokens = profile["design_tokens"]
expectations = profile["visual_qa_expectations"]
assert tokens["owner"] == "OPL BookForge", tokens
assert "inspired_by_kami_patterns" in tokens["source_pattern_note"], tokens
for key in ("page", "font", "heading", "body", "caption", "table", "callout", "front_matter", "running_head", "page_number"):
    assert key in tokens, key
assert expectations["fail_close_artifact_roles"] == ["publication_proof", "final_export"], expectations
assert expectations["review_pdf_policy"].startswith("unchecked proof QA remains warning-only"), expectations
assert {"front_matter", "table_of_contents", "chapter_opening", "dense_body", "figure_or_table", "callout"} <= set(expectations["sample_page_roles"]), expectations
assert {"embedded_fonts", "rendered_page_size", "trailing_whitespace"} <= set(expectations["checklist_refs"]), expectations
PY
