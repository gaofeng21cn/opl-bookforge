#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


VERSION = "bookforge-pdf-export.v1"


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def write_manifest(path: Path | None, payload: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def render_pdf_pages(pdf_path: Path, render_dir: Path, root: Path, prefix: str) -> tuple[str, str | None, list[str]]:
    if not command_exists("pdftoppm"):
        return "skipped_missing_pdftoppm", "pdftoppm not found", []

    render_dir.mkdir(parents=True, exist_ok=True)
    for old_page in render_dir.glob(f"{prefix}-*.png"):
        old_page.unlink()

    page_prefix = render_dir / prefix
    result = subprocess.run(
        ["pdftoppm", "-png", str(pdf_path), str(page_prefix)],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        error = (result.stderr or result.stdout or "pdftoppm failed").strip()
        return "failed", error[-2000:], []

    rendered_pages = [rel(path, root) for path in sorted(render_dir.glob(f"{prefix}-*.png"))]
    return "rendered", None, rendered_pages


def pandoc_xelatex_command(source_md: Path, output_pdf: Path, metadata_file: Path | None, variables: list[str]) -> tuple[list[str], str | None]:
    if not command_exists("pandoc"):
        return [], "pandoc not found"
    if not command_exists("xelatex"):
        return [], "xelatex not found"
    command = [
        "pandoc",
        str(source_md),
        "-s",
        "--pdf-engine=xelatex",
        "--toc",
        "--number-sections",
        "--metadata",
        "link-citations=true",
        "-o",
        str(output_pdf),
    ]
    if metadata_file:
        command.extend(["--metadata-file", str(metadata_file)])
    for variable in variables:
        command.extend(["-V", variable])
    return command, None


def compile_pdf(args: argparse.Namespace) -> dict[str, Any]:
    root = args.root.resolve()
    source_md = args.source_md.resolve()
    output_pdf = args.output_pdf.resolve()
    render_dir = args.render_dir.resolve() if args.render_dir else None

    payload: dict[str, Any] = {
        "surface_kind": "bookforge_pdf_export",
        "version": VERSION,
        "artifact_role": args.artifact_role,
        "backend": args.backend,
        "source_md": rel(source_md, root),
        "output_pdf": rel(output_pdf, root),
        "status": "blocked",
        "error": None,
        "render_status": "not_requested",
        "render_error": None,
        "rendered_pages": [],
        "pdf_page_count": 0,
        "command": [],
        "quality_boundary": {
            "source_is_markdown": True,
            "uses_publication_typesetting_backend": True,
            "hand_rolled_raster_renderer": False,
            "owner_acceptance_required_for_publication_claim": True,
        },
    }

    if not source_md.exists():
        payload["status"] = "blocked_missing_source_md"
        payload["error"] = f"source Markdown not found: {source_md}"
        return payload

    if args.backend != "pandoc-xelatex":
        payload["status"] = "blocked_unsupported_backend"
        payload["error"] = f"unsupported backend: {args.backend}"
        return payload

    metadata_file = args.metadata_file.resolve() if args.metadata_file else None
    if metadata_file and not metadata_file.exists():
        payload["status"] = "blocked_missing_metadata_file"
        payload["error"] = f"metadata file not found: {metadata_file}"
        return payload

    command, blocker = pandoc_xelatex_command(source_md, output_pdf, metadata_file, args.variable)
    payload["command"] = command
    if blocker:
        payload["status"] = f"blocked_missing_{blocker.split()[0]}"
        payload["error"] = blocker
        return payload

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        if output_pdf.exists():
            output_pdf.unlink()
        payload["status"] = "blocked_pdf_compile_failed"
        payload["error"] = (result.stderr or result.stdout or "pandoc failed").strip()[-2000:]
        return payload

    payload["status"] = "generated"
    payload["error"] = None

    if render_dir:
        render_status, render_error, rendered_pages = render_pdf_pages(
            output_pdf,
            render_dir,
            root,
            args.render_prefix,
        )
        payload["render_status"] = render_status
        payload["render_error"] = render_error
        payload["rendered_pages"] = rendered_pages
        payload["pdf_page_count"] = len(rendered_pages)

    return payload


def doctor() -> dict[str, Any]:
    return {
        "surface_kind": "bookforge_pdf_export_doctor",
        "version": VERSION,
        "available_backends": {
            "pandoc-xelatex": command_exists("pandoc") and command_exists("xelatex"),
        },
        "tools": {
            "pandoc": shutil.which("pandoc"),
            "xelatex": shutil.which("xelatex"),
            "pdftoppm": shutil.which("pdftoppm"),
            "quarto": shutil.which("quarto"),
            "typst": shutil.which("typst"),
        },
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="OPL BookForge publication/typesetting PDF export helper.",
    )
    parser.add_argument("--doctor", action="store_true", help="Print backend availability JSON and exit.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root for relative refs.")
    parser.add_argument("--source-md", type=Path, help="Markdown source to compile.")
    parser.add_argument("--output-pdf", type=Path, help="PDF output path.")
    parser.add_argument("--manifest", type=Path, help="Optional JSON manifest output path.")
    parser.add_argument("--render-dir", type=Path, help="Optional directory for rendered page PNGs.")
    parser.add_argument("--render-prefix", default="bookforge-page", help="Rendered page file prefix.")
    parser.add_argument("--metadata-file", type=Path, help="Optional Pandoc YAML metadata file for design/profile variables.")
    parser.add_argument(
        "-V",
        "--variable",
        action="append",
        default=[],
        help="Pandoc variable, for example geometry:inner=30mm or documentclass=ctexbook. Repeatable.",
    )
    parser.add_argument(
        "--backend",
        default="pandoc-xelatex",
        choices=["pandoc-xelatex"],
        help="Typesetting backend. v1 supports Pandoc with XeLaTeX.",
    )
    parser.add_argument(
        "--artifact-role",
        default="owner_review_only_not_final_export",
        help="Artifact role recorded in the manifest.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.doctor:
        print(json.dumps(doctor(), ensure_ascii=False, indent=2))
        return 0

    missing = [name for name in ("source_md", "output_pdf") if getattr(args, name) is None]
    if missing:
        print(f"missing required arguments: {', '.join('--' + name.replace('_', '-') for name in missing)}", file=sys.stderr)
        return 2

    payload = compile_pdf(args)
    write_manifest(args.manifest, payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["status"] == "generated" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
