from __future__ import annotations

import fnmatch
import json
import os
from pathlib import Path
from typing import Any


SOURCE_SCAN_EXCLUDED_DIRS = (".git", ".worktrees", "worktrees")
SOURCE_BYPRODUCT_DIR_NAMES = (
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "dist",
    "coverage",
    "node_modules",
)
SOURCE_BYPRODUCT_FILE_GLOBS = ("*.pyc", "*.pyo")
SOURCE_BYPRODUCT_SUFFIXES = (".egg-info",)


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def source_byproduct_scan(source_root: Path) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if not source_root.exists():
        return [{
            "kind": "repo_source_byproduct_scan_failed",
            "path": str(source_root),
            "reason": "source_root_missing",
        }]
    for dirpath, dirnames, filenames in os.walk(source_root):
        current = Path(dirpath)
        try:
            rel_parts = current.resolve().relative_to(source_root.resolve()).parts
        except ValueError:
            rel_parts = ()
        if any(part in SOURCE_SCAN_EXCLUDED_DIRS for part in rel_parts):
            dirnames[:] = []
            continue

        kept_dirnames = []
        for dirname in dirnames:
            if dirname in SOURCE_SCAN_EXCLUDED_DIRS:
                continue
            if dirname in SOURCE_BYPRODUCT_DIR_NAMES or dirname.endswith(SOURCE_BYPRODUCT_SUFFIXES):
                byproduct_path = current / dirname
                issues.append({
                    "kind": "repo_source_generated_byproduct",
                    "path": rel(byproduct_path, source_root),
                    "byproduct_type": "directory",
                    "reason": "repo source must not rely on ignored Python/cache/install byproducts",
                })
                continue
            kept_dirnames.append(dirname)
        dirnames[:] = kept_dirnames

        for filename in filenames:
            if (
                any(fnmatch.fnmatch(filename, glob) for glob in SOURCE_BYPRODUCT_FILE_GLOBS)
                or filename.endswith(SOURCE_BYPRODUCT_SUFFIXES)
            ):
                byproduct_path = current / filename
                issues.append({
                    "kind": "repo_source_generated_byproduct",
                    "path": rel(byproduct_path, source_root),
                    "byproduct_type": "file",
                    "reason": "repo source must not rely on ignored Python/cache/install byproducts",
                })
    return issues


def repo_source_byproduct_summary(args: Any) -> dict[str, Any]:
    required = bool(getattr(args, "require_source_byproduct_clean", False))
    source_root = getattr(args, "source_root", None) or getattr(args, "root", Path.cwd())
    source_root = Path(source_root).resolve()
    issues = source_byproduct_scan(source_root) if required else []
    return {
        "required": required,
        "source_root": str(source_root),
        "status": "passed" if not issues else "failed",
        "issues": issues,
        "excluded_dirs": list(SOURCE_SCAN_EXCLUDED_DIRS),
        "forbidden_dir_names": list(SOURCE_BYPRODUCT_DIR_NAMES),
        "forbidden_file_globs": list(SOURCE_BYPRODUCT_FILE_GLOBS),
        "forbidden_suffixes": list(SOURCE_BYPRODUCT_SUFFIXES),
    }


def run_source_byproduct_check(args: Any, *, version: str) -> dict[str, Any]:
    summary = repo_source_byproduct_summary(args)
    payload = {
        "surface_kind": "bookforge_repo_source_byproduct_hygiene",
        "version": version,
        "root": str(Path(getattr(args, "root", Path.cwd())).resolve()),
        "status": summary["status"],
        "issues": summary["issues"],
        "repo_source_byproducts": summary,
        "claim_boundary": {
            "byproduct_clean_counts_as_book_delivery_ready": False,
            "byproduct_clean_counts_as_publication_ready": False,
            "byproduct_clean_counts_as_owner_acceptance": False,
        },
    }
    if getattr(args, "report", None):
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload
