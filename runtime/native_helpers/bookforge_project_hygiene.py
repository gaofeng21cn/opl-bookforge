#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


VERSION = "bookforge-project-hygiene.v1"

DEFAULT_ACTIVE_PATHS = (
    "README.md",
    "inputs",
    "artifacts/manuscript",
    "artifacts/review",
    "artifacts/stage_outputs",
    "quality",
    "receipts",
)
DEFAULT_ARCHIVE_DIRS = ("archive",)
DEFAULT_VOICE_PATHS = (
    "README.md",
    "inputs",
    "artifacts/manuscript",
    "artifacts/review",
    "artifacts/stage_outputs/book-materialization/owner-handoff.md",
    "artifacts/stage_outputs/book-materialization/style-consistency-report.md",
)
DEFAULT_STATUS_PATHS = (
    "README.md",
    "artifacts/stage_outputs/book-materialization",
    "quality",
    "receipts",
)
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


def chapter_statuses(root: Path) -> dict[str, Any]:
    metrics_path = root / "artifacts/stage_outputs/book-materialization/manuscript-metrics.json"
    if not metrics_path.exists():
        return {"status": "missing_metrics", "path": rel(metrics_path, root)}
    try:
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"status": "invalid_metrics", "path": rel(metrics_path, root), "error": str(exc)}
    chapters = metrics.get("chapters")
    return {
        "status": "loaded" if isinstance(chapters, list) else "missing_chapters",
        "total_chars": metrics.get("total_chars"),
        "missing_chars_min": metrics.get("missing_chars_min"),
        "review_pdf": metrics.get("completed_chapters_review", {}),
        "chapters": chapters if isinstance(chapters, list) else [],
    }


def active_scan(root: Path, voice_paths: list[Path], status_paths: list[Path]) -> list[dict[str, Any]]:
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
    voice_paths = [project_path(root, ref) for ref in args.voice_path]
    status_paths = [project_path(root, ref) for ref in args.status_path]
    archive_paths = [project_path(root, ref) for ref in args.archive_dir]
    issues = []
    issues.extend(active_scan(root, voice_paths, status_paths))
    issues.extend(archive_scan(root, archive_paths))
    metrics = chapter_statuses(root)
    payload = {
        "surface_kind": "bookforge_project_hygiene",
        "version": VERSION,
        "root": str(root),
        "status": "passed" if not issues else "failed",
        "issues": issues,
        "metrics_summary": metrics,
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def run_self_test() -> None:
    import tempfile

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


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check BookForge project hygiene for active manuscript and retired draft archives.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Book project root.")
    parser.add_argument("--active-path", action="append", default=None, help="Backward-compatible alias: add the same active text path to voice and status scans. Repeatable.")
    parser.add_argument("--voice-path", action="append", default=None, help="Active reader-facing or handoff path to scan for forbidden case-stance phrases. Repeatable.")
    parser.add_argument("--status-path", action="append", default=None, help="Active status/handoff path to scan for stale metrics and blockers. Repeatable.")
    parser.add_argument("--archive-dir", action="append", default=list(DEFAULT_ARCHIVE_DIRS), help="Retired archive directory to scan. Repeatable.")
    parser.add_argument("--report", type=Path, help="Optional JSON report path.")
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
