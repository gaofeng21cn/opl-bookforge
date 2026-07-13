#!/usr/bin/env python3
"""Executable assertions for the Book Forge native-helper verification lane."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"unable to load helper module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(command: list[str], *, cwd: Path = REPO, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    if check and result.returncode != 0:
        raise AssertionError(
            f"command failed ({result.returncode}): {' '.join(command)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_pandoc_command_shape() -> None:
    helper = load_module("bookforge_pdf_export", REPO / "runtime/native_helpers/bookforge_pdf_export.py")
    base_args = (
        Path("sample.md"),
        Path("sample.pdf"),
        None,
        [],
        [Path(".")],
        [],
    )
    numbered_command, blocker = helper.pandoc_xelatex_command(*base_args, number_sections=True)
    assert blocker is None, blocker
    assert "--number-sections" in numbered_command, numbered_command

    unnumbered_command, blocker = helper.pandoc_xelatex_command(*base_args, number_sections=False)
    assert blocker is None, blocker
    assert "--number-sections" not in unnumbered_command, unnumbered_command


def test_image_asset_manifest_lifecycle() -> None:
    helper = REPO / "runtime/native_helpers/bookforge_imagegen_asset.py"
    with tempfile.TemporaryDirectory(prefix="bookforge-verify-image-") as tmp:
        root = Path(tmp)
        asset_manifest = root / "artifacts/stage_outputs/chapter-materialization/figure-asset-manifest.json"
        write_json(asset_manifest, {
            "surface_kind": "bookforge_figure_asset_manifest",
            "version": "bookforge-figure-asset-manifest.v1",
            "figures": [{
                "id": "verify-figure",
                "title": "图 0-1：Verify Figure",
                "chapter": "验证",
                "required": True,
                "project_local_path": "artifacts/figures/verify-figure.png",
                "asset_status": "planned",
                "blocker_kind": "imagegen_asset_not_generated",
            }],
        })

        receipt = root / "artifacts/figures/verify-figure.receipt.json"
        output = root / "artifacts/figures/verify-figure.png"
        run([
            PYTHON,
            str(helper),
            "--mock",
            "--root",
            str(root),
            "--figure-id",
            "verify-figure",
            "--title",
            "图 0-1：Verify Figure",
            "--prompt",
            "mock manifest sync smoke",
            "--output-file",
            "artifacts/figures/verify-figure.png",
            "--manifest",
            "artifacts/figures/verify-figure.receipt.json",
            "--asset-manifest",
            "artifacts/stage_outputs/chapter-materialization/figure-asset-manifest.json",
        ])
        run([
            PYTHON,
            str(helper),
            "--update-asset-manifest",
            "--root",
            str(root),
            "--receipt-file",
            "artifacts/figures/verify-figure.receipt.json",
            "--asset-manifest",
            "artifacts/stage_outputs/chapter-materialization/figure-asset-manifest.json",
        ])

        payload = json.loads(asset_manifest.read_text(encoding="utf-8"))
        item = payload["figures"][0]
        assert item["asset_status"] == "asset_ready", item
        assert item["receipt_ref"] == "artifacts/figures/verify-figure.receipt.json", item
        assert item["project_local_path"] == "artifacts/figures/verify-figure.png", item
        assert receipt.exists(), receipt
        assert output.exists(), output


SAMPLE_MARKDOWN = """---
title: "Book Forge PDF Smoke"
author: "OPL Book Forge"
lang: zh-CN
date: "2026-06-19"
---

# 第一章

这是 OPL Book Forge PDF 出口的中文 smoke test。

> 审阅 PDF 可以检查内容连续性；出版 proof 还要检查页面节奏、图表、页眉页码和视觉层级。

## 图表与页面节奏

出版级电子书不能只有默认正文灰度。Book Forge 的出版 profile 应当给标题、表格、引用块、图注和页码一个稳定层级。

| Artifact | Gate | Evidence |
| --- | --- | --- |
| review_pdf | readable | compile and render |
| publication_proof | designed | profile and inspection |
| final_export | accepted | owner receipt |

![图 0-1：出版 proof 图片解析 smoke](artifacts/figures/smoke-figure.png)
"""


PUBLICATION_DESIGN = {
    "page_geometry": "A5",
    "typography_hierarchy": "defined",
    "caption_style": "defined",
    "figure_treatment": "defined",
    "table_treatment": "defined",
    "callout_style": "defined",
    "headers_footers": "defined",
    "page_numbering": "defined",
    "visual_rhythm": "defined",
    "rendered_page_inspection_plan": "sample pages",
}


COMPLETE_INSPECTION = {
    "nonblank_pages": 1,
    "overflow_or_clipping": False,
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
    "checklist_refs_status": "passed",
}


def prepare_pdf_fixture(root: Path) -> None:
    (root / "sample.md").write_text(SAMPLE_MARKDOWN, encoding="utf-8")
    image_helper = REPO / "runtime/native_helpers/bookforge_imagegen_asset.py"
    run([
        PYTHON,
        str(image_helper),
        "--mock",
        "--root",
        str(root),
        "--figure-id",
        "smoke-figure",
        "--title",
        "图 0-1：出版 proof 图片解析 smoke",
        "--prompt",
        "mock publication proof figure resource path smoke",
        "--output-file",
        "artifacts/figures/smoke-figure.png",
        "--manifest",
        "artifacts/figures/smoke-figure.receipt.json",
    ])
    write_json(root / "figure-asset-manifest.json", {
        "surface_kind": "bookforge_figure_asset_manifest",
        "version": "bookforge-figure-asset-manifest.v1",
        "figures": [{
            "id": "smoke-figure",
            "title": "图 0-1：出版 proof 图片解析 smoke",
            "required": True,
            "asset_status": "asset_ready",
            "project_local_path": "artifacts/figures/smoke-figure.png",
        }],
    })


def pdf_export(
    root: Path,
    output_name: str,
    manifest_name: str,
    *,
    role: str,
    source_name: str = "sample.md",
    **extra: str,
) -> subprocess.CompletedProcess[str]:
    helper = REPO / "runtime/native_helpers/bookforge_pdf_export.py"
    command = [
        PYTHON,
        str(helper),
        "--root",
        str(root),
        "--source-md",
        str(root / source_name),
        "--output-pdf",
        str(root / output_name),
        "--manifest",
        str(root / manifest_name),
        "--artifact-role",
        role,
    ]
    for key, value in extra.items():
        command.extend([f"--{key.replace('_', '-')}", value])
    return run(command, check=False)


def test_pdf_smoke() -> None:
    with tempfile.TemporaryDirectory(prefix="bookforge-verify-pdf-") as tmp:
        root = Path(tmp)
        prepare_pdf_fixture(root)

        review = pdf_export(
            root,
            "sample.pdf",
            "manifest.json",
            role="review_pdf",
            render_dir=str(root / "rendered-pages"),
            render_prefix="sample-page",
        )
        assert review.returncode == 0, review.stderr or review.stdout
        payload = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        assert payload["status"] == "generated", payload
        assert payload["artifact_role"] == "review_pdf", payload
        assert payload["artifact_gate"]["status"] == "passed", payload["artifact_gate"]
        assert payload["artifact_gate"]["claim_boundary"]["review_pdf_counts_as_publication_proof"] is False, payload["artifact_gate"]

        missing_design = pdf_export(root, "sample-proof-missing-evidence.pdf", "proof-missing-evidence.json", role="publication_proof")
        assert missing_design.returncode == 0, missing_design.stderr or missing_design.stdout
        payload = json.loads((root / "proof-missing-evidence.json").read_text(encoding="utf-8"))
        assert payload["status"] == "generated_with_quality_debt", payload
        assert payload["artifact_gate"]["status"] == "quality_debt", payload["artifact_gate"]
        assert payload["artifact_gate"]["quality_debt"]["blocks_stage_transition"] is False
        assert payload["artifact_gate"]["quality_debt"]["blocks_quality_export_or_ready_claims"] is True

        missing_source = pdf_export(
            root,
            "missing-source.pdf",
            "missing-source-diagnostic.json",
            role="review_pdf",
            source_name="does-not-exist.md",
        )
        assert missing_source.returncode == 0, missing_source.stderr or missing_source.stdout
        payload = json.loads((root / "missing-source-diagnostic.json").read_text(encoding="utf-8"))
        assert payload["status"] == "completed_with_quality_debt", payload
        assert payload["progress_diagnostic"]["code"] == "source_markdown_missing", payload
        assert payload["progress_diagnostic"]["blocks_stage_transition"] is False, payload
        assert payload["progress_diagnostic"]["next_stage_may_start"] is True, payload

        (root / "remote-image.md").write_text(
            """---
title: "Remote Image Blocker"
lang: zh-CN
---

# 第一章

![远程图片不应作为出版 proof 资产](https://example.com/remote.png)
""",
            encoding="utf-8",
        )
        write_json(root / "publication-design.json", PUBLICATION_DESIGN)
        incomplete_inspection = dict(COMPLETE_INSPECTION)
        for field in (
            "embedded_font_status",
            "page_density_status",
            "trailing_whitespace_status",
            "rendered_page_size_status",
            "sample_page_roles_status",
            "checklist_refs_status",
        ):
            incomplete_inspection.pop(field)
        write_json(root / "rendered-page-inspection-incomplete.json", incomplete_inspection)

        incomplete = pdf_export(
            root,
            "sample-proof-incomplete-inspection.pdf",
            "proof-incomplete-inspection.json",
            role="publication_proof",
            render_dir=str(root / "rendered-incomplete-proof-pages"),
            render_prefix="incomplete-proof-page",
            publication_design_profile=str(root / "publication-design.json"),
            rendered_page_inspection=str(root / "rendered-page-inspection-incomplete.json"),
            figure_asset_manifest=str(root / "figure-asset-manifest.json"),
        )
        assert incomplete.returncode == 0, incomplete.stderr or incomplete.stdout
        payload = json.loads((root / "proof-incomplete-inspection.json").read_text(encoding="utf-8"))
        assert payload["status"] == "generated_with_quality_debt", payload
        blocker_types = {item["blocker_type"] for item in payload["artifact_gate"]["blockers"]}
        assert "rendered_page_inspection_incomplete" in blocker_types, payload["artifact_gate"]

        write_json(root / "rendered-page-inspection.json", COMPLETE_INSPECTION)
        complete = pdf_export(
            root,
            "sample-proof.pdf",
            "proof-manifest.json",
            role="publication_proof",
            render_dir=str(root / "rendered-proof-pages"),
            render_prefix="proof-page",
            publication_design_profile=str(root / "publication-design.json"),
            rendered_page_inspection=str(root / "rendered-page-inspection.json"),
            figure_asset_manifest=str(root / "figure-asset-manifest.json"),
        )
        assert complete.returncode == 0, complete.stderr or complete.stdout

        remote = pdf_export(
            root,
            "remote-image-proof.pdf",
            "remote-image-proof-manifest.json",
            role="publication_proof",
            source_name="remote-image.md",
            render_dir=str(root / "rendered-remote-image-proof-pages"),
            render_prefix="remote-image-proof-page",
            publication_design_profile=str(root / "publication-design.json"),
            rendered_page_inspection=str(root / "rendered-page-inspection.json"),
        )
        assert remote.returncode == 0, remote.stderr or remote.stdout
        payload = json.loads((root / "remote-image-proof-manifest.json").read_text(encoding="utf-8"))
        assert payload["status"] == "generated_with_quality_debt", payload
        blocker_types = {item["blocker_type"] for item in payload["artifact_gate"]["blockers"]}
        assert "markdown_image_ref_not_project_local" in blocker_types, payload["artifact_gate"]

        bundled = pdf_export(
            root,
            "sample-bundled-profile-proof.pdf",
            "bundled-profile-proof-manifest.json",
            role="publication_proof",
            render_dir=str(root / "rendered-bundled-profile-pages"),
            render_prefix="bundled-proof-page",
            write_rendered_page_inspection=str(root / "auto-rendered-page-inspection.json"),
            figure_asset_manifest=str(root / "figure-asset-manifest.json"),
        )
        assert bundled.returncode == 0, bundled.stderr or bundled.stdout
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


def test_publication_profile_contract() -> None:
    profile = json.loads(
        (REPO / "runtime/native_helpers/pdf_profiles/bookforge-zh-publication-proof.json").read_text(encoding="utf-8")
    )
    tokens = profile["design_tokens"]
    expectations = profile["visual_qa_expectations"]
    assert tokens["owner"] == "OPL Book Forge", tokens
    assert "inspired_by_kami_patterns" in tokens["source_pattern_note"], tokens
    for key in (
        "page",
        "font",
        "heading",
        "body",
        "caption",
        "table",
        "callout",
        "front_matter",
        "running_head",
        "page_number",
    ):
        assert key in tokens, key
    assert expectations["fail_close_artifact_roles"] == ["publication_proof", "final_export"], expectations
    assert expectations["review_pdf_policy"].startswith("unchecked proof QA remains warning-only"), expectations
    assert {"front_matter", "table_of_contents", "chapter_opening", "dense_body", "figure_or_table", "callout"} <= set(expectations["sample_page_roles"]), expectations
    assert {"embedded_fonts", "rendered_page_size", "trailing_whitespace"} <= set(expectations["checklist_refs"]), expectations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-smoke", action="store_true", help="run Pandoc/XeLaTeX proof-backend checks")
    args = parser.parse_args(argv)
    test_pandoc_command_shape()
    test_image_asset_manifest_lifecycle()
    test_publication_profile_contract()
    if args.pdf_smoke:
        test_pdf_smoke()
    print(json.dumps({
        "status": "passed",
        "test": "bookforge_verify_helpers",
        "pdf_smoke": args.pdf_smoke,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
