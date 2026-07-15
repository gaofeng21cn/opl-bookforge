#!/usr/bin/env python3
"""Executable assertions for the Book Forge native-helper verification lane."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
import zlib
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


def test_progress_diagnostic_has_no_route_authority() -> None:
    helper = load_module("bookforge_pdf_export", REPO / "runtime/native_helpers/bookforge_pdf_export.py")
    payload = helper.materialize_progress_diagnostic(
        {"output_pdf": "missing.pdf"},
        code="source_markdown_missing",
        error="source markdown does not exist",
    )
    diagnostic = payload["progress_diagnostic"]
    assert diagnostic["next_stage_may_start"] is True, diagnostic
    assert not {
        "route_selection_owner",
        "semantic_route_decision_owner",
        "stage_transition_materialization_owner",
    } & diagnostic.keys(), diagnostic


def png_chunk(kind: bytes, payload: bytes) -> bytes:
    checksum = zlib.crc32(kind + payload) & 0xFFFFFFFF
    return len(payload).to_bytes(4, "big") + kind + payload + checksum.to_bytes(4, "big")


def png_bytes(width: int = 16, height: int = 12) -> bytes:
    header = width.to_bytes(4, "big") + height.to_bytes(4, "big") + b"\x08\x06\x00\x00\x00"
    rows = b"".join(b"\x00" + b"\x00\x00\x00\xff" * width for _ in range(height))
    return (
        b"\x89PNG\r\n\x1a\n"
        + png_chunk(b"IHDR", header)
        + png_chunk(b"IDAT", zlib.compress(rows))
        + png_chunk(b"IEND", b"")
    )


def test_image_asset_candidate_contract() -> None:
    helper = load_module("bookforge_imagegen_asset", REPO / "runtime/native_helpers/bookforge_imagegen_asset.py")
    with tempfile.TemporaryDirectory(prefix="bookforge-verify-image-") as tmp:
        root = Path(tmp)
        output = root / "artifacts/figures/verify-figure.png"
        output.parent.mkdir(parents=True)
        data = png_bytes()
        output.write_bytes(data)
        payload = helper.evaluate_host_bitmap({
            "surface_kind": "opl_bookforge_host_bitmap_validation_request",
            "schema_version": 1,
            "host_context": {
                "workspace_root": str(root),
                "attempt_ref": "stage-run://verify/attempt",
                "output_ref": "stage-run://verify/output/figure",
            },
            "bitmap": {
                "bitmap_ref": "artifacts/figures/verify-figure.png",
                "sha256": helper.sha256_bytes(data),
                "format": "png",
                "media_type": "image/png",
            },
            "figure": {
                "figure_id": "verify-figure",
                "title": "图 0-1：Verify Figure",
                "artifact_role": "book_manuscript_figure",
            },
        })
        assert payload["status"] == "figure_authority_receipt_candidate", payload
        candidate = payload["figure_authority_receipt_candidate"]
        assert candidate["asset_manifest_entry_candidate"]["asset_status"] == "bitmap_validated_pending_visual_review", candidate
        assert candidate["authority_boundary"]["candidate_requires_opl_persistence"] is True, candidate


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
    figure_path = root / "artifacts/figures/smoke-figure.png"
    figure_path.parent.mkdir(parents=True)
    figure_path.write_bytes(png_bytes())
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
        embedded_font_names = {
            font["name"] for font in auto["embedded_font_inspection"]["fonts"]
        }
        assert any("FandolSong" in name for name in embedded_font_names), embedded_font_names
        assert any("FandolHei" in name for name in embedded_font_names), embedded_font_names
        assert not any(
            host_font in name
            for name in embedded_font_names
            for host_font in ("Noto", "PingFang", "Menlo")
        ), embedded_font_names
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


def test_artifact_gate_matrix() -> None:
    helper = load_module("bookforge_pdf_gate", REPO / "runtime/native_helpers/bookforge_pdf_export.py")
    with tempfile.TemporaryDirectory(prefix="bookforge-artifact-gate-") as tmp:
        root = Path(tmp)
        base_payload = {
            "artifact_role": "publication_proof",
            "render_status": "rendered",
            "rendered_pages": ["rendered/page-1.png"],
            "markdown_image_refs": {"missing_count": 0, "refs": []},
            "figure_asset_manifest_summary": {"blockers": []},
            "auto_rendered_page_inspection_ref": None,
        }
        base_args = {
            "publication_design_profile": None,
            "rendered_page_inspection": None,
            "owner_acceptance_receipt": None,
            "figure_asset_manifest": None,
            "resolved_publication_profile": None,
        }
        incomplete_inspection = dict(COMPLETE_INSPECTION)
        incomplete_inspection.pop("embedded_font_status")
        scenarios = [
            {
                "name": "missing-design",
                "payload": {},
                "design": {},
                "inspection": COMPLETE_INSPECTION,
                "args": {},
                "blocker": "publication_design_profile_missing",
            },
            {
                "name": "incomplete-page-inspection",
                "payload": {},
                "design": PUBLICATION_DESIGN,
                "inspection": incomplete_inspection,
                "args": {},
                "blocker": "rendered_page_inspection_incomplete",
            },
            {
                "name": "remote-image",
                "payload": {
                    "markdown_image_refs": {
                        "missing_count": 0,
                        "refs": [{"ref": "https://example.com/remote.png", "status": "external_or_data"}],
                    },
                },
                "design": PUBLICATION_DESIGN,
                "inspection": COMPLETE_INSPECTION,
                "args": {},
                "blocker": "markdown_image_ref_not_project_local",
            },
            {
                "name": "final-export-without-owner",
                "payload": {"artifact_role": "final_export"},
                "design": PUBLICATION_DESIGN,
                "inspection": COMPLETE_INSPECTION,
                "args": {},
                "blocker": "owner_acceptance_missing",
            },
        ]
        for scenario in scenarios:
            payload = {**base_payload, **scenario["payload"]}
            args = argparse.Namespace(**{**base_args, **scenario["args"]})
            helper.assess_artifact_gate(
                payload,
                args,
                root,
                scenario["design"],
                None,
                scenario["inspection"],
                None,
                {},
                None,
            )
            blockers = {item["blocker_type"] for item in payload["artifact_gate"]["blockers"]}
            assert scenario["blocker"] in blockers, (scenario["name"], payload["artifact_gate"])
            assert payload["artifact_gate"]["status"] == "quality_debt"
            assert payload["artifact_gate"]["quality_debt"]["blocks_stage_transition"] is False
            assert payload["artifact_gate"]["quality_debt"]["blocks_quality_export_or_ready_claims"] is True
            assert payload["artifact_gate"]["claim_boundary"] == {
                "review_pdf_counts_as_publication_proof": False,
                "publication_proof_counts_as_final_export": False,
                "helper_receipt_counts_as_owner_acceptance": False,
            }


def test_publication_profile_contract() -> None:
    profile = json.loads(
        (REPO / "runtime/native_helpers/pdf_profiles/bookforge-zh-publication-proof.json").read_text(encoding="utf-8")
    )
    tokens = profile["design_tokens"]
    expectations = profile["visual_qa_expectations"]
    variables = profile["pandoc_variables"]
    assert tokens["owner"] == "OPL Book Forge", tokens
    assert "inspired_by_kami_patterns" in tokens["source_pattern_note"], tokens
    assert "classoption=fontset=fandol" in variables, variables
    assert not any(
        host_font in variable
        for variable in variables
        for host_font in ("Noto", "PingFang", "Menlo")
    ), variables
    assert tokens["font"] == {
        "body": "FandolSong-Regular",
        "heading": "FandolHei-Regular",
        "mono": "FandolFang-Regular",
        "fontset": "fandol",
        "provider": "TeX Live CTEX distribution",
        "requires_system_font_service": False,
        "body_size": "11pt",
        "line_stretch": 1.24,
        "embedded_font_required_for_publication_proof": True,
    }, tokens["font"]
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
    parser.add_argument("--pdf-smoke-only", action="store_true", help="run only Pandoc/XeLaTeX proof-backend checks")
    args = parser.parse_args(argv)
    if not args.pdf_smoke_only:
        test_pandoc_command_shape()
        test_progress_diagnostic_has_no_route_authority()
        test_image_asset_candidate_contract()
        test_publication_profile_contract()
        test_artifact_gate_matrix()
    if args.pdf_smoke or args.pdf_smoke_only:
        test_pdf_smoke()
    print(json.dumps({
        "status": "passed",
        "test": "bookforge_verify_helpers",
        "pdf_smoke": args.pdf_smoke or args.pdf_smoke_only,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
