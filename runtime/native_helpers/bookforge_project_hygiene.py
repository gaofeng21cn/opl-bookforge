#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

HELPER_DIR = Path(__file__).resolve().parent
if str(HELPER_DIR) not in sys.path:
    sys.path.insert(0, str(HELPER_DIR))

from bookforge_project_hygiene_parts.opl_lifecycle import (
    ARTIFACT_LIFECYCLE_HANDOFF_CONTRACT_REF,
    OPL_ARTIFACT_LIFECYCLE_HEALTH_REF,
    OPL_ARTIFACT_LIFECYCLE_INDEX_REF,
    OPL_ARTIFACT_LIFECYCLE_MEMORY_REF,
    OPL_ARTIFACT_LIFECYCLE_OUTPUT_REF,
    OPL_ARTIFACT_LIFECYCLE_SOURCE_REF,
    artifact_lifecycle_handoff_contract_summary,
    opl_artifact_lifecycle_issues,
    opl_artifact_lifecycle_summary,
)
from bookforge_project_hygiene_parts.status import chapter_statuses, figure_asset_summary, review_pdf_export_summary

VERSION = "bookforge-project-hygiene.v2"

DEFAULT_ARCHIVE_DIRS = ("archive",)
DEFAULT_VOICE_PATHS = (
    "README.md",
    "inputs",
    "artifacts/manuscript",
    "artifacts/review",
    "artifacts/stage_outputs/publication-proof-handoff/owner-handoff.md",
    "artifacts/stage_outputs/source-style-integrity-review/style-consistency-report.md",
)
DEFAULT_STATUS_PATHS = (
    "README.md",
    "artifacts/stage_outputs",
    "quality",
    "receipts",
)
CURRENT_STATUS_METRIC_FILENAMES = (
    "plan-completion-audit.md",
    "owner-handoff.md",
    "manuscript-metrics.md",
    "pdf-backend-audit.md",
    "imagegen-asset-path-audit.md",
)
HIGH_QUALITY_REF_GROUPS = {
    "chapter_function_contract": (
        "chapter-function-contract.md",
        "chapter-function-contract.json",
    ),
    "concept_map": (
        "concept-map.md",
        "concept-map-application.md",
        "early-concept-map.md",
    ),
    "core_model_map": (
        "core-model-map.md",
        "whole-book-core-model-map.md",
        "core-model-application.md",
    ),
    "case_evidence_ladder": (
        "case-evidence-ladder.md",
        "case-evidence-ladder.json",
    ),
    "high_quality_review_audit": (
        "high-quality-book-review-audit.md",
        "reviewer-suggestion-absorption.md",
        "reviewer-critique-absorption.md",
    ),
    "meta_review_loop": (
        "round-1.md",
        "round-1-repair-plan.md",
    ),
}
TEXT_EXTENSIONS = (".md", ".txt", ".json", ".yaml", ".yml")
RETIRED_FULLTEXT_MARKERS = (
    "retired_no_longer_searchable_source",
    "tombstone",
    "TOMBSTONE",
)
RED_BIRD_OBSERVER_PATTERNS = (
    "公开可观察",
    "教育实验观察窗口",
    "公开观察窗口",
    "公开资料显示",
    "公开资料可以支持我们观察",
    "观察它如何强调",
    "红鸟硕士班公开资料足以支持",
    "可以被看作 AI 时代高等教育转型的观察窗口",
    "把它作为公开",
    "把它作为公开可观察",
    "外部旁观",
    "第三者观察",
)
STALE_STATUS_PATTERNS = (
    "第一章、第二章和第三章正文已达到章节预算门槛",
    "第四章及后续章节仍是 `draft_in_progress`",
    "当前全书计数字符为 55,042",
    "80,849 counted Chinese characters",
    "Chapter 6 remains `draft_in_progress`",
    "Chapter 7: expand using the practice-involved Red Bird stance",
    "7/11 required figures",
    "41 页，包含前言、第一章、第二章和第三章",
    "128 rendered pages",
)
STATUS_NUMBER_RE = r"([0-9][0-9,_，]*)"


def project_path(root: Path, ref: str) -> Path:
    path = Path(ref)
    return path if path.is_absolute() else root / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def iter_text_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if not path.exists():
            continue
        if path.is_file() and path.suffix in TEXT_EXTENSIONS:
            files.append(path)
        elif path.is_dir():
            for item in path.rglob("*"):
                if item.is_file() and item.suffix in TEXT_EXTENSIONS:
                    files.append(item)
    return sorted(set(files))


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def contains_any(text: str, patterns: tuple[str, ...]) -> list[str]:
    return [pattern for pattern in patterns if pattern in text]


def parse_int_claim(value: str) -> int | None:
    cleaned = value.replace(",", "").replace("_", "").replace("，", "")
    try:
        return int(cleaned)
    except ValueError:
        return None


def chapter_chars_by_label(metrics: dict[str, Any]) -> dict[str, int]:
    chapters = metrics.get("chapters") if isinstance(metrics.get("chapters"), list) else []
    mapping: dict[str, int] = {}
    for row in chapters:
        title = str(row.get("title", ""))
        chars = row.get("chars")
        if not isinstance(chars, int):
            continue
        if title.startswith("第八章"):
            mapping["Chapter 8"] = chars
        if title.startswith("结语"):
            mapping["conclusion"] = chars
    return mapping


def stale_metric_claims(root: Path, path: Path, text: str, metrics: dict[str, Any]) -> list[dict[str, Any]]:
    if path.name not in CURRENT_STATUS_METRIC_FILENAMES:
        return []

    export_summary = review_pdf_export_summary(root)
    expected = {
        "total_chars": metrics.get("total_chars"),
        "pdf_page_count": metrics.get("review_pdf", {}).get("pdf_page_count"),
        "nonblank_pages": export_summary.get("nonblank_pages"),
    }
    patterns = (
        ("total_chars", rf"total_chars\s*=?\s*`?{STATUS_NUMBER_RE}`?"),
        ("pdf_page_count", rf"completed-chapters\.review\.pdf`?:\s*{STATUS_NUMBER_RE}\s+pages"),
        ("pdf_page_count", rf"current\s+A5\s+review\s+PDF\s+is\s+{STATUS_NUMBER_RE}\s+pages"),
        ("nonblank_pages", rf"nonblank_pages\s*=?\s*`?{STATUS_NUMBER_RE}`?"),
    )
    issues: list[dict[str, Any]] = []
    for metric_name, pattern in patterns:
        current_value = expected.get(metric_name)
        if not isinstance(current_value, int):
            continue
        for match in re.finditer(pattern, text, re.IGNORECASE):
            claimed_value = parse_int_claim(match.group(1))
            if claimed_value is None or claimed_value == current_value:
                continue
            issues.append({
                "kind": "stale_status_metric",
                "path": rel(path, root),
                "metric": metric_name,
                "claimed": claimed_value,
                "current": current_value,
                "excerpt": match.group(0),
            })

    chapter_chars = chapter_chars_by_label(metrics)
    for label, current_chars in chapter_chars.items():
        pattern = rf"{re.escape(label)}\s+`{STATUS_NUMBER_RE}/[0-9,_，]+`"
        for match in re.finditer(pattern, text):
            claimed_chars = parse_int_claim(match.group(1))
            if claimed_chars is None or claimed_chars == current_chars:
                continue
            issues.append({
                "kind": "stale_status_metric",
                "path": rel(path, root),
                "metric": f"{label}.chars",
                "claimed": claimed_chars,
                "current": current_chars,
                "excerpt": match.group(0),
            })
    issues.extend(stale_figure_asset_claims(root, path, text))
    return issues


def stale_figure_asset_claims(root: Path, path: Path, text: str) -> list[dict[str, Any]]:
    if path.name != "imagegen-asset-path-audit.md":
        return []
    figure_summary = figure_asset_summary(root)
    export_summary = review_pdf_export_summary(root)
    issues: list[dict[str, Any]] = []
    if figure_summary.get("figure_files", 0) > 0 and re.search(r"artifacts/figures/`?\s+contains\s+0\s+files", text):
        issues.append({
            "kind": "stale_figure_asset_status",
            "path": rel(path, root),
            "metric": "artifacts/figures.file_count",
            "claimed": 0,
            "current": figure_summary["figure_files"],
            "excerpt": "artifacts/figures contains 0 files",
        })
    if figure_summary.get("preview_only") == 0 and re.search(r"records[^\n]+as\s+`preview_only`|`preview_only`,\s+not\s+`asset_ready`", text):
        issues.append({
            "kind": "stale_figure_asset_status",
            "path": rel(path, root),
            "metric": "figure_manifest.preview_only",
            "claimed": "preview_only_present",
            "current": 0,
            "excerpt": "preview_only",
        })
    if figure_summary.get("asset_ready", 0) > 0 and "not `asset_ready`" in text:
        issues.append({
            "kind": "stale_figure_asset_status",
            "path": rel(path, root),
            "metric": "figure_manifest.asset_ready",
            "claimed": "not_asset_ready",
            "current": figure_summary["asset_ready"],
            "excerpt": "not `asset_ready`",
        })
    if export_summary.get("markdown_image_refs_present", 0) > 0 and re.search(r"no embedded images|returned no embedded images", text, re.IGNORECASE):
        issues.append({
            "kind": "stale_figure_asset_status",
            "path": rel(path, root),
            "metric": "review_pdf.images",
            "claimed": "no_embedded_images",
            "current": export_summary["markdown_image_refs_present"],
            "excerpt": "no embedded images",
        })
    return issues


def is_book_length_final_nonfiction_candidate(metrics: dict[str, Any]) -> bool:
    total_chars = metrics.get("total_chars")
    target_chars_min = metrics.get("target_chars_min")
    chapters = metrics.get("chapters") if isinstance(metrics.get("chapters"), list) else []
    assembly_status = metrics.get("assembly_status")
    extent_status = metrics.get("extent_status")
    if assembly_status == "final_book_assembly_ready" and extent_status == "meets_target":
        return True
    if isinstance(total_chars, int) and total_chars >= 50000 and len(chapters) >= 6:
        return True
    if isinstance(target_chars_min, int) and target_chars_min >= 50000 and len(chapters) >= 6:
        return True
    return False


def extract_meta_review_round(path: Path) -> int:
    match = re.match(r"round-(\d+)\.md$", path.name)
    return int(match.group(1)) if match else 0


def extract_meta_review_verdict(text: str) -> str:
    match = re.search(r"verdict\s*[:：]\s*`?([a-zA-Z_]+)`?", text, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    if re.search(r"##\s*Verdict\s*\n\s*`?([a-zA-Z_]+)`?", text, re.IGNORECASE):
        return re.search(r"##\s*Verdict\s*\n\s*`?([a-zA-Z_]+)`?", text, re.IGNORECASE).group(1).lower()  # type: ignore[union-attr]
    return ""


def is_independent_meta_review(text: str) -> bool:
    lower = text.lower()
    if "owner waived meta-review" in lower or "owner explicitly waived meta-review" in lower:
        return True
    if "same-executor" in lower or "self-review" in lower or "not an independent" in lower:
        return False
    return "independent" in lower or "context-isolated" in lower or "context isolated" in lower


def meta_review_loop_status(root: Path) -> dict[str, Any]:
    meta_review_dir = root / "quality/meta-review"
    round_paths = sorted(
        (
            path
            for path in meta_review_dir.glob("round-*.md")
            if re.match(r"round-\d+\.md$", path.name)
        ),
        key=extract_meta_review_round,
    ) if meta_review_dir.exists() else []
    if not round_paths:
        return {"ok": False, "reason": "missing_meta_review_round"}
    if len(round_paths) > 3:
        return {
            "ok": False,
            "reason": "meta_review_iteration_limit_exceeded",
            "round_count": len(round_paths),
        }

    round_reports = []
    missing_repair_plans = []
    for path in round_paths:
        text = read_text(path)
        round_no = extract_meta_review_round(path)
        verdict = extract_meta_review_verdict(text)
        independent = is_independent_meta_review(text)
        if verdict in {"revise_minor", "revise_major", "revise"}:
            repair_plan = meta_review_dir / f"round-{round_no}-repair-plan.md"
            if not repair_plan.exists():
                missing_repair_plans.append(rel(repair_plan, root))
        round_reports.append({
            "round": round_no,
            "ref": rel(path, root),
            "verdict": verdict,
            "independent": independent,
        })

    if missing_repair_plans:
        return {
            "ok": False,
            "reason": "missing_meta_review_repair_plan",
            "missing_repair_plans": missing_repair_plans,
            "rounds": round_reports,
        }

    independent_rounds = [item for item in round_reports if item["independent"]]
    if not independent_rounds:
        return {
            "ok": False,
            "reason": "missing_independent_meta_review_round",
            "rounds": round_reports,
        }
    latest = independent_rounds[-1]
    if latest["verdict"] != "pass":
        return {
            "ok": False,
            "reason": "latest_independent_meta_review_not_pass",
            "latest_independent_round": latest,
            "rounds": round_reports,
        }
    return {
        "ok": True,
        "latest_independent_round": latest,
        "rounds": round_reports,
    }


def high_quality_ref_scan(root: Path, metrics: dict[str, Any]) -> list[dict[str, Any]]:
    if not is_book_length_final_nonfiction_candidate(metrics):
        return []
    search_roots = [
        root / "artifacts/stage_outputs/storyline-architecture",
        root / "artifacts/stage_outputs",
        root / "quality",
    ]
    existing = {path.name for path in iter_text_files(search_roots)}
    issues: list[dict[str, Any]] = []
    for group, filenames in HIGH_QUALITY_REF_GROUPS.items():
        has_required_ref = any(filename in existing for filename in filenames)
        if group == "meta_review_loop":
            meta_status = meta_review_loop_status(root)
            has_required_ref = bool(meta_status.get("ok"))
            if not has_required_ref:
                issues.append({
                    "kind": "missing_high_quality_nonfiction_ref",
                    "group": group,
                    "expected_any_of": list(filenames),
                    "reason": "book-length final assemblies should have a bounded independent meta-review loop whose latest independent verdict is pass, or a typed blocker/owner waiver",
                    "meta_review_status": meta_status,
                })
                continue
        if has_required_ref:
            continue
        issues.append({
            "kind": "missing_high_quality_nonfiction_ref",
            "group": group,
            "expected_any_of": list(filenames),
                "reason": "book-length final assemblies should carry chapter-function, concept, model, case-evidence, critique-absorption, and independent meta-review refs",
            })
    return issues


def active_scan(root: Path, voice_paths: list[Path], status_paths: list[Path], metrics: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for path in iter_text_files(voice_paths):
        text = read_text(path)
        observer_hits = contains_any(text, RED_BIRD_OBSERVER_PATTERNS)
        if observer_hits:
            issues.append({
                "kind": "red_bird_observer_voice",
                "path": rel(path, root),
                "patterns": observer_hits,
            })
    for path in iter_text_files(status_paths):
        if path.name == "book-project-hygiene.json":
            continue
        text = read_text(path)
        stale_hits = contains_any(text, STALE_STATUS_PATTERNS)
        if stale_hits:
            issues.append({
                "kind": "stale_workbench_status",
                "path": rel(path, root),
                "patterns": stale_hits,
            })
        issues.extend(stale_metric_claims(root, path, text, metrics))
    return issues


def archive_scan(root: Path, archive_paths: list[Path]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for path in iter_text_files(archive_paths):
        text = read_text(path)
        marker_hit = any(marker in text for marker in RETIRED_FULLTEXT_MARKERS)
        observer_hits = contains_any(text, RED_BIRD_OBSERVER_PATTERNS)
        if observer_hits and not marker_hit:
            issues.append({
                "kind": "archive_exposes_retired_observer_voice_without_tombstone",
                "path": rel(path, root),
                "patterns": observer_hits,
            })
        if path.name != "TOMBSTONE.md" and len(re.sub(r"\s+", "", text)) > 1200 and not marker_hit:
            issues.append({
                "kind": "archive_retired_fulltext_exposed",
                "path": rel(path, root),
                "chars_no_space": len(re.sub(r"\s+", "", text)),
            })
    return issues


def run_check(args: argparse.Namespace) -> dict[str, Any]:
    root = args.root.resolve()
    source_root = Path(getattr(args, "source_root", None) or root).resolve()
    source_root_arg = getattr(args, "source_root", None)
    source_root_looks_like_bookforge_repo = (
        (source_root / "contracts/workspace_lifecycle_policy.json").exists()
        and (source_root / "runtime/native_helpers/bookforge_project_hygiene.py").exists()
    )
    voice_paths = [project_path(root, ref) for ref in args.voice_path]
    status_paths = [project_path(root, ref) for ref in args.status_path]
    archive_paths = [project_path(root, ref) for ref in args.archive_dir]
    issues = []
    metrics = chapter_statuses(root)
    issues.extend(active_scan(root, voice_paths, status_paths, metrics))
    issues.extend(archive_scan(root, archive_paths))
    issues.extend(high_quality_ref_scan(root, metrics))
    lifecycle_summary = opl_artifact_lifecycle_summary(
        root,
        require=bool(getattr(args, "require_opl_lifecycle", False)),
        opl_bin=getattr(args, "opl_bin", None),
    )
    issues.extend(opl_artifact_lifecycle_issues(lifecycle_summary))
    handoff_contract_summary = artifact_lifecycle_handoff_contract_summary(
        source_root,
        required=bool(source_root_arg) or source_root_looks_like_bookforge_repo,
    )
    issues.extend(handoff_contract_summary["issues"])
    payload = {
        "surface_kind": "bookforge_project_hygiene",
        "version": VERSION,
        "root": str(root),
        "status": "passed" if not issues else "failed",
        "issues": issues,
        "metrics_summary": metrics,
        "opl_artifact_lifecycle": lifecycle_summary,
        "artifact_lifecycle_handoff_contract": handoff_contract_summary,
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def run_self_test() -> None:
    import tempfile

    def write_valid_handoff_contract(source_root: Path, **false_ready_overrides: bool) -> None:
        contract_path = source_root / ARTIFACT_LIFECYCLE_HANDOFF_CONTRACT_REF
        contract_path.parent.mkdir(parents=True, exist_ok=True)
        false_ready_guard = {
            "contract_present_counts_as_workspace_apply_evidence": False,
            "dry_run_counts_as_workspace_apply_evidence": False,
            "projection_clean_counts_as_book_delivery_ready": False,
            "projection_clean_counts_as_publication_ready": False,
            "projection_clean_counts_as_final_export_ready": False,
            "projection_clean_counts_as_owner_acceptance": False,
            "projection_clean_counts_as_production_ready": False,
            "helper_hygiene_counts_as_book_delivery_ready": False,
            "helper_hygiene_counts_as_publication_ready": False,
            "helper_hygiene_counts_as_owner_acceptance": False,
        }
        false_ready_guard.update(false_ready_overrides)
        contract_path.write_text(json.dumps({
            "surface_kind": "bookforge_artifact_lifecycle_handoff_contract",
            "version": "bookforge-artifact-lifecycle-handoff.v1",
            "structural_gate_only": True,
            "required_opl_projection_refs": [
                OPL_ARTIFACT_LIFECYCLE_INDEX_REF.as_posix(),
                OPL_ARTIFACT_LIFECYCLE_SOURCE_REF.as_posix(),
                OPL_ARTIFACT_LIFECYCLE_MEMORY_REF.as_posix(),
                OPL_ARTIFACT_LIFECYCLE_OUTPUT_REF.as_posix(),
                OPL_ARTIFACT_LIFECYCLE_HEALTH_REF.as_posix(),
            ],
            "readback_surface": {
                "command": "opl workspace artifact-lifecycle --workspace <workspace> --project-id <project-id> --dry-run|--apply --json",
                "dry_run_counts_as_workspace_apply_evidence": False,
            },
            "forbidden_authority": {
                "opl_can_write_bookforge_domain_truth": False,
                "opl_can_write_memory_body": False,
                "opl_can_mutate_manuscript_or_artifact_body": False,
                "opl_can_authorize_quality_export_or_publication": False,
                "opl_can_sign_owner_receipts": False,
                "bookforge_can_replace_opl_lifecycle_projection": False,
                "bookforge_can_create_private_lifecycle_second_truth": False,
            },
            "false_ready_guard": false_ready_guard,
        }), encoding="utf-8")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        active = root / "artifacts/manuscript/chapters"
        active.mkdir(parents=True)
        (active / "07-red-bird.md").write_text("红鸟硕士班公开资料可以支持我们观察它如何强调项目制。", encoding="utf-8")
        archive = root / "archive/obsolete"
        archive.mkdir(parents=True)
        (archive / "old.md").write_text("第七章讨论红鸟硕士班，把它作为公开可观察的教育实验观察窗口。", encoding="utf-8")
        payload = run_check(argparse.Namespace(
            root=root,
            voice_path=[str(active)],
            status_path=[str(active)],
            archive_dir=[str(root / "archive")],
            report=None,
        ))
        kinds = {issue["kind"] for issue in payload["issues"]}
        assert "red_bird_observer_voice" in kinds, payload
        assert "archive_exposes_retired_observer_voice_without_tombstone" in kinds, payload

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "artifacts/manuscript/chapters").mkdir(parents=True)
        (root / "artifacts/manuscript/chapters/07-red-bird.md").write_text("我们预判到这些变化，所以这样设计。", encoding="utf-8")
        (root / "archive/obsolete").mkdir(parents=True)
        (root / "archive/obsolete/TOMBSTONE.md").write_text("State: `retired_no_longer_searchable_source`\n", encoding="utf-8")
        payload = run_check(argparse.Namespace(
            root=root,
            voice_path=["artifacts/manuscript"],
            status_path=["README.md"],
            archive_dir=["archive"],
            report=None,
        ))
        assert payload["status"] == "passed", payload

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        stage = root / "artifacts/stage_outputs/chapter-materialization"
        stage.mkdir(parents=True)
        (stage / "manuscript-metrics.json").write_text(json.dumps({
            "assembly_status": "final_book_assembly_ready",
            "extent_status": "meets_target",
            "total_chars": 120000,
            "target_chars_min": 120000,
            "missing_chars_min": 0,
            "chapters": [{"id": str(i), "status": "chapter_draft_ready"} for i in range(8)],
        }), encoding="utf-8")
        payload = run_check(argparse.Namespace(
            root=root,
            voice_path=["artifacts/manuscript"],
            status_path=["README.md"],
            archive_dir=["archive"],
            report=None,
        ))
        missing_groups = {
            issue["group"]
            for issue in payload["issues"]
            if issue["kind"] == "missing_high_quality_nonfiction_ref"
        }
        assert {
            "chapter_function_contract",
            "concept_map",
            "core_model_map",
            "case_evidence_ladder",
            "high_quality_review_audit",
            "meta_review_loop",
        } <= missing_groups, payload

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        stage = root / "artifacts/stage_outputs/chapter-materialization"
        quality = root / "quality"
        story = root / "artifacts/stage_outputs/storyline-architecture"
        stage.mkdir(parents=True)
        quality.mkdir(parents=True)
        story.mkdir(parents=True)
        (stage / "manuscript-metrics.json").write_text(json.dumps({
            "assembly_status": "final_book_assembly_ready",
            "extent_status": "meets_target",
            "total_chars": 120000,
            "target_chars_min": 120000,
            "missing_chars_min": 0,
            "chapters": [{"id": str(i), "status": "chapter_draft_ready"} for i in range(8)],
        }), encoding="utf-8")
        (stage / "chapter-function-contract.md").write_text("# Chapter Function Contract\n", encoding="utf-8")
        (story / "concept-map.md").write_text("# Concept Map\n", encoding="utf-8")
        (stage / "core-model-map.md").write_text("# Core Model Map\n", encoding="utf-8")
        (stage / "case-evidence-ladder.md").write_text("# Case Evidence Ladder\n", encoding="utf-8")
        (quality / "high-quality-book-review-audit.md").write_text("# High Quality Book Review Audit\n", encoding="utf-8")
        meta_review = quality / "meta-review"
        meta_review.mkdir()
        (meta_review / "round-1.md").write_text(
            "# Round 1\n\nReviewer context boundary: `same-executor-limited-meta-review`\n\nVerdict: `revise_minor`\n",
            encoding="utf-8",
        )
        (meta_review / "round-1-repair-plan.md").write_text("# Round 1 Repair Plan\n", encoding="utf-8")
        payload = run_check(argparse.Namespace(
            root=root,
            voice_path=["artifacts/manuscript"],
            status_path=["README.md"],
            archive_dir=["archive"],
            report=None,
        ))
        meta_issues = [
            issue
            for issue in payload["issues"]
            if issue["kind"] == "missing_high_quality_nonfiction_ref" and issue["group"] == "meta_review_loop"
        ]
        assert meta_issues, payload

        (meta_review / "round-2.md").write_text(
            "# Round 2\n\nReviewer context boundary: independent subagent review; reviewer received assembled manuscript and limited quality refs, not the drafting conversation.\n\n## Verdict\n\n`pass`\n",
            encoding="utf-8",
        )
        payload = run_check(argparse.Namespace(
            root=root,
            voice_path=["artifacts/manuscript"],
            status_path=["README.md"],
            archive_dir=["archive"],
            report=None,
        ))
        assert not [
            issue
            for issue in payload["issues"]
            if issue["kind"] == "missing_high_quality_nonfiction_ref"
        ], payload

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        stage = root / "artifacts/stage_outputs/chapter-materialization"
        review = root / "artifacts/review"
        quality = root / "quality"
        stage.mkdir(parents=True)
        review.mkdir(parents=True)
        quality.mkdir(parents=True)
        (stage / "manuscript-metrics.json").write_text(json.dumps({
            "assembly_status": "final_book_assembly_ready",
            "extent_status": "meets_declared_minimum",
            "total_chars": 126955,
            "estimated_pages_at_600_chars": 211.6,
            "target_chars_min": 120000,
            "missing_chars_min": 0,
            "completed_chapters_review": {"pdf_page_count": 167},
            "chapters": [
                {"title": "第八章 大学的未来意义", "chars": 11780},
                {"title": "结语 教学生发现值得干的事", "chars": 3099},
            ],
        }), encoding="utf-8")
        (review / "completed-chapters.review-pdf-export.json").write_text(json.dumps({
            "rendered_page_inspection": {"nonblank_pages": 167},
        }), encoding="utf-8")
        (quality / "plan-completion-audit.md").write_text(
            "`total_chars=124153`\n"
            "`artifacts/review/completed-chapters.review.pdf`: 166 pages\n"
            "`nonblank_pages=166`\n"
            "Chapter 8 `11306/9600`; conclusion `2788/2400`\n",
            encoding="utf-8",
        )
        payload = run_check(argparse.Namespace(
            root=root,
            voice_path=["artifacts/manuscript"],
            status_path=["quality"],
            archive_dir=["archive"],
            report=None,
        ))
        stale_metrics = [issue for issue in payload["issues"] if issue["kind"] == "stale_status_metric"]
        stale_metric_names = {issue["metric"] for issue in stale_metrics}
        assert {"total_chars", "pdf_page_count", "nonblank_pages", "Chapter 8.chars", "conclusion.chars"} <= stale_metric_names, payload

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        stage = root / "artifacts/stage_outputs/chapter-materialization"
        review = root / "artifacts/review"
        quality = root / "quality"
        figures = root / "artifacts/figures"
        stage.mkdir(parents=True)
        review.mkdir(parents=True)
        quality.mkdir(parents=True)
        figures.mkdir(parents=True)
        (stage / "manuscript-metrics.json").write_text(json.dumps({
            "assembly_status": "final_book_assembly_ready",
            "extent_status": "meets_declared_minimum",
            "total_chars": 126955,
            "target_chars_min": 120000,
            "missing_chars_min": 0,
            "completed_chapters_review": {"pdf_page_count": 167},
            "chapters": [],
        }), encoding="utf-8")
        (stage / "figure-asset-manifest.json").write_text(json.dumps({
            "figures": [
                {
                    "id": "fig-1-1",
                    "asset_status": "asset_ready",
                    "project_local_path": "artifacts/figures/fig-1-1.png",
                }
            ]
        }), encoding="utf-8")
        (figures / "fig-1-1.png").write_bytes(b"png")
        (review / "completed-chapters.review-pdf-export.json").write_text(json.dumps({
            "markdown_image_refs": {"present_count": 1, "total": 1, "missing_count": 0},
        }), encoding="utf-8")
        (quality / "imagegen-asset-path-audit.md").write_text(
            "- `artifacts/figures/` contains 0 files.\n"
            "- `figure-asset-manifest.json` records 图 1-1 as `preview_only`, not `asset_ready`.\n"
            "- `pdfimages -list artifacts/review/completed-chapters.review.pdf` returned no embedded images.\n",
            encoding="utf-8",
        )
        payload = run_check(argparse.Namespace(
            root=root,
            voice_path=["artifacts/manuscript"],
            status_path=["quality"],
            archive_dir=["archive"],
            report=None,
        ))
        stale_figure_metrics = {
            issue["metric"]
            for issue in payload["issues"]
            if issue["kind"] == "stale_figure_asset_status"
        }
        assert {
            "artifacts/figures.file_count",
            "figure_manifest.preview_only",
            "figure_manifest.asset_ready",
            "review_pdf.images",
        } <= stale_figure_metrics, payload

    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / "Book"
        root = workspace / "book-001"
        root.mkdir(parents=True)
        (workspace / "workspace_index.json").write_text(json.dumps({
            "projects": [
                {
                    "project_id": "book-001",
                    "project_root": "book-001",
                },
            ],
        }), encoding="utf-8")

        payload = run_check(argparse.Namespace(
            root=root,
            voice_path=["artifacts/manuscript"],
            status_path=["README.md"],
            archive_dir=["archive"],
            report=None,
            require_opl_lifecycle=True,
            opl_bin=None,
        ))
        lifecycle_issue_kinds = {
            issue["kind"]
            for issue in payload["issues"]
            if issue["kind"].startswith("opl_artifact_lifecycle")
        }
        assert "opl_artifact_lifecycle_missing" in lifecycle_issue_kinds, payload
        assert "opl_artifact_lifecycle_blocked" in lifecycle_issue_kinds, payload

        for ref in [
            OPL_ARTIFACT_LIFECYCLE_INDEX_REF,
            OPL_ARTIFACT_LIFECYCLE_SOURCE_REF,
            OPL_ARTIFACT_LIFECYCLE_MEMORY_REF,
            OPL_ARTIFACT_LIFECYCLE_OUTPUT_REF,
        ]:
            path = root / ref
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"status": "passed"}), encoding="utf-8")
        (root / OPL_ARTIFACT_LIFECYCLE_HEALTH_REF).write_text(json.dumps({
            "status": "passed",
            "blockers": [],
        }), encoding="utf-8")

        payload = run_check(argparse.Namespace(
            root=root,
            voice_path=["artifacts/manuscript"],
            status_path=["README.md"],
            archive_dir=["archive"],
            report=None,
            require_opl_lifecycle=True,
            opl_bin=str(root / "missing-opl"),
        ))
        lifecycle_issues = [
            issue
            for issue in payload["issues"]
            if issue["kind"].startswith("opl_artifact_lifecycle")
        ]
        assert lifecycle_issues == [
            {
                "kind": "opl_artifact_lifecycle_missing",
                "reason": "opl binary not found",
            },
        ], payload

        fake_opl = root / "fake-opl"
        fake_opl.write_text(
            "#!/usr/bin/env bash\n"
            "printf '{\"workspace_artifact_lifecycle\":{\"lifecycle_status\":\"passed\"}}\\n'\n",
            encoding="utf-8",
        )
        fake_opl.chmod(0o755)
        payload = run_check(argparse.Namespace(
            root=root,
            voice_path=["artifacts/manuscript"],
            status_path=["README.md"],
            archive_dir=["archive"],
            report=None,
            require_opl_lifecycle=True,
            opl_bin=str(fake_opl),
        ))
        assert not [
            issue
            for issue in payload["issues"]
            if issue["kind"].startswith("opl_artifact_lifecycle")
        ], payload

    with tempfile.TemporaryDirectory() as tmp:
        source_root = Path(tmp) / "repo"
        source_root.mkdir()
        write_valid_handoff_contract(source_root)
        payload = run_check(argparse.Namespace(
            root=source_root,
            source_root=source_root,
            voice_path=["artifacts/manuscript"],
            status_path=["README.md"],
            archive_dir=["archive"],
            report=None,
            require_opl_lifecycle=False,
            opl_bin=None,
        ))
        assert payload["artifact_lifecycle_handoff_contract"]["status"] == "passed", payload

        write_valid_handoff_contract(
            source_root,
            projection_clean_counts_as_publication_ready=True,
        )
        payload = run_check(argparse.Namespace(
            root=source_root,
            source_root=source_root,
            voice_path=["artifacts/manuscript"],
            status_path=["README.md"],
            archive_dir=["archive"],
            report=None,
            require_opl_lifecycle=False,
            opl_bin=None,
        ))
        false_ready_issues = [
            issue
            for issue in payload["issues"]
            if issue["kind"] == "artifact_lifecycle_handoff_false_ready_guard_failed"
        ]
        assert false_ready_issues, payload

def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Book Forge project hygiene for active manuscript and retired draft archives.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Book project root.")
    parser.add_argument("--active-path", action="append", default=None, help="Backward-compatible alias: add the same active text path to voice and status scans. Repeatable.")
    parser.add_argument("--voice-path", action="append", default=None, help="Active reader-facing or handoff path to scan for forbidden case-stance phrases. Repeatable.")
    parser.add_argument("--status-path", action="append", default=None, help="Active status/handoff path to scan for stale metrics and blockers. Repeatable.")
    parser.add_argument("--archive-dir", action="append", default=list(DEFAULT_ARCHIVE_DIRS), help="Retired archive directory to scan. Repeatable.")
    parser.add_argument("--report", type=Path, help="Optional JSON report path.")
    parser.add_argument("--require-opl-lifecycle", action="store_true", help="Require passed OPL workspace artifact-lifecycle refs and dry-run readback.")
    parser.add_argument("--opl-bin", help="Path to the OPL CLI used for artifact-lifecycle dry-run readback.")
    parser.add_argument("--source-root", type=Path, help="Optional Book Forge source root used to validate the artifact-lifecycle handoff contract.")
    parser.add_argument("--self-test", action="store_true", help="Run helper self-test.")
    args = parser.parse_args(argv)
    if args.active_path:
        args.voice_path = list(args.active_path)
        args.status_path = list(args.active_path)
    else:
        args.voice_path = list(args.voice_path or DEFAULT_VOICE_PATHS)
        args.status_path = list(args.status_path or DEFAULT_STATUS_PATHS)
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.self_test:
        run_self_test()
        print(json.dumps({"status": "passed", "self_test": True, "version": VERSION}, ensure_ascii=False))
        return 0
    payload = run_check(args)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
