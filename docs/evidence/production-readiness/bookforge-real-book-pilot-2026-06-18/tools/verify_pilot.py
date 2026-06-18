#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageStat


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18"
INPUTS = BASE / "inputs"
STORYLINE = BASE / "artifacts/stage_outputs/storyline-architecture"
MATERIALIZATION = BASE / "artifacts/stage_outputs/book-materialization"
MANUSCRIPT = BASE / "artifacts/manuscript/book.md"
FIGURES = BASE / "artifacts/figures"
RECEIPTS = BASE / "receipts"
QUALITY = BASE / "quality"
EXPORTS = BASE / "exports"
RENDERED = EXPORTS / "rendered-pages"


REQUIRED_FILES = [
    INPUTS / "book-brief.md",
    INPUTS / "source-corpus.md",
    INPUTS / "voice-and-audience.md",
    STORYLINE / "storyline-map.md",
    STORYLINE / "chapter-thesis-chain.json",
    STORYLINE / "style-contract.md",
    STORYLINE / "owner-handoff.md",
    STORYLINE / "stage.manifest.json",
    MATERIALIZATION / "chapter-drafts.md",
    MATERIALIZATION / "illustration-plan.md",
    MATERIALIZATION / "table-plan.md",
    MATERIALIZATION / "style-consistency-report.md",
    MATERIALIZATION / "ai-flavor-revision-report.md",
    MATERIALIZATION / "layout-qc-report.md",
    MATERIALIZATION / "owner-handoff.md",
    MATERIALIZATION / "stage.manifest.json",
    MANUSCRIPT,
    FIGURES / "figure-01-storyline-arc.png",
    FIGURES / "figure-02-two-stage-route.png",
    RECEIPTS / "storyline-independent-gate-receipt.json",
    RECEIPTS / "storyline-owner-blocker.json",
    RECEIPTS / "book-materialization-independent-gate-receipt.json",
    RECEIPTS / "book-owner-blocker.json",
    RECEIPTS / "production-readiness-closeout.json",
    QUALITY / "export-receipt.json",
    EXPORTS / "bookforge-pilot-book.html",
    EXPORTS / "bookforge-pilot-book.docx",
    EXPORTS / "bookforge-pilot-book.pdf",
]

AI_FLAVOR_PATTERNS = [
    "不是.*而是",
    "不仅.*而且",
    "总的来说",
    "综上所述",
    "在当今.*时代",
    "值得注意的是",
    "毋庸置疑",
    "显而易见",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def image_check(path: Path) -> dict[str, object]:
    image = Image.open(path).convert("L")
    stat = ImageStat.Stat(image)
    return {
        "path": rel(path),
        "size": list(image.size),
        "mean": round(float(stat.mean[0]), 2),
        "stddev": round(float(stat.stddev[0]), 2),
        "nonblank": stat.stddev[0] > 5,
        "content_hash": sha256(path),
    }


def docx_media_count(path: Path) -> int:
    with zipfile.ZipFile(path) as archive:
        return len([name for name in archive.namelist() if name.startswith("word/media/")])


def main() -> None:
    missing = [rel(path) for path in REQUIRED_FILES if not path.exists()]
    empty = [rel(path) for path in REQUIRED_FILES if path.exists() and path.stat().st_size == 0]

    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    heading_count = len(re.findall(r"^# ", manuscript, flags=re.MULTILINE))
    table_count = manuscript.count("\n|")
    image_refs = re.findall(r"!\[[^\]]+\]\(([^)]+)\)", manuscript)
    ai_flavor_hits = {
        pattern: re.findall(pattern, manuscript)
        for pattern in AI_FLAVOR_PATTERNS
        if re.findall(pattern, manuscript)
    }

    required_terms = [
        "故事线",
        "chapter thesis",
        "source-ref",
        "quality gate",
        "owner handoff",
        "typed blocker",
    ]
    term_presence = {term: manuscript.count(term) for term in required_terms}

    figure_checks = [
        image_check(FIGURES / "figure-01-storyline-arc.png"),
        image_check(FIGURES / "figure-02-two-stage-route.png"),
    ]
    rendered_checks = [
        image_check(path)
        for path in sorted(RENDERED.glob("page-*.png"))
    ]

    export_receipt = read_json(QUALITY / "export-receipt.json")
    docx_issue_count = int(export_receipt["docx_issues"]["data"]["count"])
    docx_issue_messages = [
        issue["message"]
        for issue in export_receipt["docx_issues"]["data"]["issues"]
    ]

    closeout = read_json(RECEIPTS / "production-readiness-closeout.json")
    story_blocker = read_json(RECEIPTS / "storyline-owner-blocker.json")
    book_blocker = read_json(RECEIPTS / "book-owner-blocker.json")

    checks = {
        "required_files_present": not missing,
        "required_files_nonempty": not empty,
        "manuscript_heading_count_min_7": heading_count >= 7,
        "manuscript_table_markers_present": table_count >= 12,
        "manuscript_image_refs_present": len(image_refs) == 2,
        "figures_nonblank": all(item["nonblank"] for item in figure_checks),
        "exports_present": all((EXPORTS / name).exists() for name in [
            "bookforge-pilot-book.html",
            "bookforge-pilot-book.docx",
            "bookforge-pilot-book.pdf",
        ]),
        "docx_schema_validation_passed": export_receipt["docx_validation"]["success"] is True,
        "docx_media_count_min_2": docx_media_count(EXPORTS / "bookforge-pilot-book.docx") >= 2,
        "pdf_rendered_pages_min_3": len(rendered_checks) >= 3,
        "pdf_rendered_pages_nonblank": all(item["nonblank"] for item in rendered_checks),
        "ai_flavor_scan_clean": not ai_flavor_hits,
        "style_terms_present": all(count > 0 for count in term_presence.values()),
        "storyline_owner_blocker_recorded": story_blocker.get("status") == "blocked_owner_acceptance_missing",
        "book_owner_blocker_recorded": book_blocker.get("status") == "blocked_owner_acceptance_missing",
        "production_ready_claim_fail_closed": closeout.get("production_ready_claim_allowed") is False,
    }

    blocking_failures = [
        name for name, passed in checks.items()
        if not passed and name != "docx_issue_count_zero"
    ]
    receipt = {
        "surface_kind": "bookforge_pilot_local_verification_receipt",
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project_id": "bookforge-production-smoke-2026-06-18",
        "verification_status": "passed_with_owner_gate_blocker" if not blocking_failures else "failed",
        "production_ready_status": "blocked_owner_acceptance_missing",
        "production_ready_claim_allowed": False,
        "checks": checks,
        "blocking_failures": blocking_failures,
        "missing_files": missing,
        "empty_files": empty,
        "manuscript_metrics": {
            "heading_count": heading_count,
            "table_marker_count": table_count,
            "image_refs": image_refs,
            "term_presence": term_presence,
            "ai_flavor_hits": ai_flavor_hits,
        },
        "figure_checks": figure_checks,
        "export_checks": {
            "docx_issue_count": docx_issue_count,
            "docx_issue_messages": docx_issue_messages,
            "docx_media_count": docx_media_count(EXPORTS / "bookforge-pilot-book.docx"),
            "rendered_page_count": len(rendered_checks),
            "rendered_page_checks": rendered_checks,
        },
        "owner_gate": {
            "owner_receipt_present": False,
            "typed_blocker_refs": [
                rel(RECEIPTS / "storyline-owner-blocker.json"),
                rel(RECEIPTS / "book-owner-blocker.json"),
            ],
            "direct_opl_hosted_parity": "blocked_no_public_opl_bookforge_runtime_cli",
        },
    }

    QUALITY.mkdir(parents=True, exist_ok=True)
    output_path = QUALITY / "local-verification-receipt.json"
    output_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    if blocking_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
