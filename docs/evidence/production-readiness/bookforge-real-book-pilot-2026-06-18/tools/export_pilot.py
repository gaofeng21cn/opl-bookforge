#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18"
MANUSCRIPT = BASE / "artifacts/manuscript/book.md"
EXPORTS = BASE / "exports"
QUALITY = BASE / "quality"
LOGS = BASE / "logs"
HTML = EXPORTS / "bookforge-pilot-book.html"
DOCX = EXPORTS / "bookforge-pilot-book.docx"
PDF = EXPORTS / "bookforge-pilot-book.pdf"
RENDERED = EXPORTS / "rendered-pages"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def run(args: list[str], *, cwd: Path = ROOT) -> dict[str, object]:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    return {
        "args": args,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def must(command: dict[str, object]) -> None:
    if command["returncode"] != 0:
        raise SystemExit(json.dumps(command, ensure_ascii=False, indent=2))


def docx_body_paths(selector: str) -> list[str]:
    result = subprocess.check_output(
        ["officecli", "query", str(DOCX), selector, "--json"],
        text=True,
        cwd=ROOT,
    )
    parsed = json.loads(result)
    return [item["path"] for item in parsed["data"]["results"]]


def postprocess_docx() -> list[str]:
    paths: list[str] = []
    for selector in ["paragraph[style=BodyText]", "paragraph[style=FirstParagraph]"]:
        for path in docx_body_paths(selector):
            if path not in paths:
                paths.append(path)
    for path in paths:
        must(run(["officecli", "set", str(DOCX), path, "--prop", "firstLineChars=200"]))
        must(run(["officecli", "set", str(DOCX), path, "--prop", "firstLineIndent=24pt"]))
    return paths


def main() -> None:
    EXPORTS.mkdir(parents=True, exist_ok=True)
    QUALITY.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    RENDERED.mkdir(parents=True, exist_ok=True)

    resource_path = (
        f"{BASE / 'artifacts/manuscript'}:"
        f"{BASE / 'artifacts'}"
    )
    commands: list[dict[str, object]] = []
    commands.append(run([
        "pandoc",
        str(MANUSCRIPT),
        f"--resource-path={resource_path}",
        "-s",
        "--metadata=title:从想法到书稿",
        "-o",
        str(HTML),
    ]))
    must(commands[-1])
    commands.append(run([
        "pandoc",
        str(MANUSCRIPT),
        f"--resource-path={resource_path}",
        "-s",
        "-o",
        str(DOCX),
    ]))
    must(commands[-1])

    postprocessed_paths = postprocess_docx()

    validation = run(["officecli", "validate", str(DOCX), "--json"])
    must(validation)
    issues = run(["officecli", "view", str(DOCX), "issues", "--json"])
    must(issues)
    outline = run(["officecli", "view", str(DOCX), "outline"])
    must(outline)

    commands.extend([validation, issues, outline])

    if PDF.exists():
        PDF.unlink()
    commands.append(run([
        "soffice",
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        str(EXPORTS),
        str(DOCX),
    ]))
    must(commands[-1])

    for old_page in RENDERED.glob("page-*.png"):
        old_page.unlink()
    commands.append(run([
        "pdftoppm",
        "-png",
        "-r",
        "144",
        str(PDF),
        str(RENDERED / "page"),
    ]))
    must(commands[-1])

    receipt = {
        "surface_kind": "bookforge_pilot_export_receipt",
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "export_status": "exported_and_rendered",
        "tools": {
            "pandoc": shutil.which("pandoc"),
            "officecli": shutil.which("officecli"),
            "soffice": shutil.which("soffice"),
            "pdftoppm": shutil.which("pdftoppm"),
        },
        "exports": {
            "html": rel(HTML),
            "docx": rel(DOCX),
            "pdf": rel(PDF),
            "rendered_pages": [rel(path) for path in sorted(RENDERED.glob("page-*.png"))],
        },
        "docx_postprocess": {
            "body_paragraph_first_line_indent": "24pt",
            "updated_paths": postprocessed_paths,
        },
        "docx_validation": json.loads(validation["stdout"]),
        "docx_issues": json.loads(issues["stdout"]),
        "docx_outline_text": outline["stdout"],
        "commands": commands,
    }
    (QUALITY / "export-receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
