#!/usr/bin/env python3
"""Generate and verify an editable DOCX plus a publication-layout PDF."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import shutil
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Any
from xml.dom import minidom
from zipfile import ZipFile

try:
    from bookforge_pdf_export import compile_pdf, parse_args as parse_pdf_args
    from bookforge_pdf_export import write_manifest as write_pdf_manifest
except ModuleNotFoundError as exc:
    if exc.name != "opl_framework":
        raise
    framework_root = os.environ.get("OPL_FRAMEWORK_ROOT")
    if not framework_root:
        opl_path = shutil.which("opl")
        if opl_path:
            framework_root = str(Path(opl_path).resolve().parent.parent)
    framework_python = Path(framework_root) / "python" if framework_root else None
    if not framework_python or not framework_python.is_dir():
        raise ModuleNotFoundError(
            "opl_framework is unavailable; set OPL_FRAMEWORK_ROOT to the OPL Framework checkout"
        ) from exc
    sys.path.insert(0, str(framework_python))
    from bookforge_pdf_export import compile_pdf, parse_args as parse_pdf_args
    from bookforge_pdf_export import write_manifest as write_pdf_manifest


VERSION = "bookforge-publication-bundle.v1"
MIN_SOURCE_COVERAGE = 0.985
TABLE_WIDTH_FILTER = Path(__file__).resolve().parent / "bookforge_table_widths.lua"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}


class BundleError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def normalized_text(value: str) -> str:
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", value)).replace("\u00ad", "")


def visible_ast_text(value: Any) -> str:
    """Read manuscript text without link destinations, attributes or image alt text."""
    if isinstance(value, list):
        return " ".join(visible_ast_text(item) for item in value)
    if not isinstance(value, dict):
        return ""
    kind = value.get("t")
    content = value.get("c", [])
    if kind == "Image":
        return ""
    if kind == "Str":
        return content
    if kind in {"Code", "CodeBlock", "Math"}:
        return content[-1]
    if kind in {"Space", "SoftBreak", "LineBreak"}:
        return " "
    if kind == "Link":
        return visible_ast_text(content[1])
    return visible_ast_text(content)


def source_coverage(source_text: str, extracted_text: str) -> float:
    """Multiset coverage tolerates PDF line wraps and table reading order.

    CJK characters are individual tokens; Latin words and numbers remain whole.
    Repeated occurrences count separately. This is extraction integrity evidence,
    not a substitute for semantic or rendered-page review.
    """
    def tokens(text: str) -> Counter:
        return Counter(re.findall(r"[A-Za-z0-9]+|[\u3400-\u9fff]", unicodedata.normalize("NFKC", text)))
    expected, actual = tokens(source_text), tokens(extracted_text)
    total = sum(expected.values())
    if not total:
        raise BundleError("source has no checkable visible text")
    return sum((expected & actual).values()) / total


def strip_title_block(source: str, *, title: str, author: str, date: str) -> tuple[str, bool]:
    """Remove a matching visible title/byline/date so Pandoc metadata supplies it once."""
    lines = source.lstrip("\ufeff").splitlines(keepends=True)
    first = next((index for index, line in enumerate(lines) if line.strip()), None)
    if first is None:
        raise BundleError("source Markdown is empty")
    heading = re.fullmatch(r"#\s+(.+?)\s*\n?", lines[first])
    if not heading:
        return source, False
    if normalized_text(heading.group(1)) != normalized_text(title):
        return source, False

    cursor = first + 1
    while cursor < len(lines) and not lines[cursor].strip():
        cursor += 1
    if cursor < len(lines):
        candidate_author = lines[cursor].strip()
        if candidate_author.startswith("**") and candidate_author.endswith("**"):
            candidate_author = candidate_author[2:-2].strip()
        if normalized_text(candidate_author) == normalized_text(author):
            cursor += 1
            while cursor < len(lines) and not lines[cursor].strip():
                cursor += 1
            if cursor < len(lines) and normalized_text(lines[cursor].strip()) == normalized_text(date):
                cursor += 1
                while cursor < len(lines) and not lines[cursor].strip():
                    cursor += 1
                return "".join(lines[:first] + lines[cursor:]), True
            raise BundleError("source title and byline match metadata, but the manuscript date does not")
        # A title-only manuscript is valid; leave any unrelated opening prose intact.
    return "".join(lines[:first] + lines[first + 1 :]), True


def pandoc_json(source_md: Path, *, cwd: Path) -> dict[str, Any]:
    result = run_command(["pandoc", str(source_md), "--from=gfm+pipe_tables", "-t", "json"], cwd=cwd)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise BundleError(f"Pandoc returned invalid AST JSON: {exc}") from exc


def count_nodes(value: Any, node_type: str) -> int:
    if isinstance(value, dict):
        own = 1 if value.get("t") == node_type else 0
        return own + sum(count_nodes(item, node_type) for item in value.values())
    if isinstance(value, list):
        return sum(count_nodes(item, node_type) for item in value)
    return 0


def docx_body_readback(path: Path) -> dict[str, Any]:
    with ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    body = root.find("w:body", NS)
    if body is None:
        raise BundleError("DOCX has no document body")
    blocks: list[str] = []
    table_count = 0
    drawing_count = 0
    for child in body:
        if child.tag == f"{{{W_NS}}}sectPr":
            continue
        if child.tag == f"{{{W_NS}}}tbl":
            table_count += 1
        drawing_count += sum(1 for node in child.iter() if node.tag == f"{{{W_NS}}}drawing")
        blocks.append("".join(node.text or "" for node in child.iter() if node.tag == f"{{{W_NS}}}t"))
    return {"text": "\n".join(blocks), "table_count": table_count, "figure_count": drawing_count}


def keep_docx_table_rows(path: Path) -> None:
    """Keep a table row together when it fits on one page.

    Pandoc repeats header rows but permits data rows to split by default.
    Preserve namespace declarations and every other package part while adding
    the Word row property before the editable file is rendered and hashed.
    """
    with ZipFile(path) as archive:
        entries = [(info, archive.read(info.filename)) for info in archive.infolist()]
    document_bytes = next(data for info, data in entries if info.filename == "word/document.xml")
    document = minidom.parseString(document_bytes)
    rows = document.getElementsByTagNameNS(W_NS, "tr")
    if not rows:
        return
    for row in rows:
        properties = next((child for child in row.childNodes
                           if child.nodeType == child.ELEMENT_NODE
                           and child.namespaceURI == W_NS and child.localName == "trPr"), None)
        if properties is None:
            properties = document.createElementNS(W_NS, "w:trPr")
            row.insertBefore(properties, row.firstChild)
        setting = next((child for child in properties.childNodes
                        if child.nodeType == child.ELEMENT_NODE
                        and child.namespaceURI == W_NS and child.localName == "cantSplit"), None)
        if setting is None:
            setting = document.createElementNS(W_NS, "w:cantSplit")
            properties.appendChild(setting)
        setting.setAttributeNS(W_NS, "w:val", "1")
    updated = document.toxml(encoding="UTF-8")
    ET.fromstring(updated)
    with ZipFile(path, "w") as archive:
        for info, data in entries:
            archive.writestr(info, updated if info.filename == "word/document.xml" else data)


def pdf_text_readback(path: Path, *, cwd: Path) -> str:
    result = run_command(["pdftotext", "-raw", str(path), "-"], cwd=cwd)
    # Retain repeated table labels and numeric cells. Removing repeated lines
    # globally can erase real manuscript content along with page furniture.
    return result.stdout


def run_command(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, check=False)
    except FileNotFoundError as exc:
        raise BundleError(f"required command is unavailable: {command[0]}") from exc
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "command failed").strip()[-2400:]
        raise BundleError(f"{command[0]} failed with exit code {result.returncode}: {detail}")
    return result


def pdf_args(args: argparse.Namespace, *, source_md: Path, metadata: Path, output_pdf: Path,
             pdf_manifest: Path, inspection: Path, pdf_pages: Path, design_profile: Path) -> list[str]:
    command = [
        "--root", str(args.root),
        "--source-md", str(source_md),
        "--output-pdf", str(output_pdf),
        "--manifest", str(pdf_manifest),
        "--metadata-file", str(metadata),
        "--publication-profile", args.publication_profile,
        "--publication-design-profile", str(design_profile),
        "--write-rendered-page-inspection", str(inspection),
        "--render-dir", str(pdf_pages),
        "--render-prefix", "pdf-page",
        "--artifact-role", "publication_proof",
    ]
    for path in args.resource_path:
        command.extend(["--resource-path", str(path)])
    if args.figure_asset_manifest:
        command.extend(["--figure-asset-manifest", str(args.figure_asset_manifest)])
    if not args.number_sections:
        command.append("--no-number-sections")
    if not args.table_of_contents:
        command.append("--no-toc")
    return command


def docx_command(args: argparse.Namespace, *, source_md: Path, metadata: Path, output_docx: Path) -> list[str]:
    command = [
        "pandoc", str(source_md), "--from=gfm+pipe_tables", "--standalone",
        "--metadata-file", str(metadata), "--lua-filter", str(TABLE_WIDTH_FILTER),
        "--to=docx", "--output", str(output_docx),
    ]
    if args.reference_doc:
        command.extend(["--reference-doc", str(args.reference_doc)])
    if args.number_sections:
        command.append("--number-sections")
    if args.table_of_contents:
        command.append("--toc")
    if args.resource_path:
        command.append(f"--resource-path={os.pathsep.join(str(path) for path in args.resource_path)}")
    return command


def prepare_fontconfig(explicit: Path | None, *, build_inputs: Path) -> Path | None:
    """Persist the selected font configuration, or discover macOS host font dirs."""
    target = build_inputs / "fontconfig.conf"
    if explicit:
        if not explicit.is_file():
            raise BundleError(f"Fontconfig file not found: {explicit}")
        target.write_bytes(explicit.read_bytes())
        return target
    if sys.platform != "darwin":
        return None
    font_dirs = [Path("/System/Library/Fonts"), Path("/Library/Fonts"), Path.home() / "Library/Fonts"]
    config = ET.Element("fontconfig")
    for directory in font_dirs:
        if directory.is_dir():
            ET.SubElement(config, "dir").text = str(directory)
    cache = build_inputs.parent / "font-cache"
    cache.mkdir(parents=True, exist_ok=True)
    ET.SubElement(config, "cachedir").text = str(cache)
    ET.SubElement(config, "config")
    target.write_text('<?xml version="1.0"?>\n<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">\n'
                      + ET.tostring(config, encoding="unicode") + "\n", encoding="utf-8")
    return target


def rendered_text_integrity(source: str, rendered: str, *, title: str, author: str, date: str) -> dict[str, Any]:
    normalized = normalized_text(rendered)
    return {
        "source_coverage": source_coverage(source, rendered),
        "title_byline_date_present": all(normalized_text(value) in normalized for value in (title, author, date)),
    }


def render_docx(docx: Path, *, output_dir: Path, prefix: str, cwd: Path, soffice: str,
                fontconfig: Path | None = None) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    profile = output_dir / ".libreoffice-profile"
    rendered_pdf = output_dir / f"{docx.stem}.pdf"
    rendered_pdf.unlink(missing_ok=True)
    env = dict(os.environ)
    if fontconfig:
        env["FONTCONFIG_FILE"] = str(fontconfig)
    converted = run_command([
        soffice, "--headless", f"-env:UserInstallation={profile.as_uri()}",
        "--convert-to", "pdf", "--outdir", str(output_dir), str(docx),
    ], cwd=cwd, env=env)
    if not rendered_pdf.is_file():
        raise BundleError(f"LibreOffice did not create the DOCX render PDF: {converted.stdout.strip()}")
    for previous in output_dir.glob(f"{prefix}-*.png"):
        previous.unlink()
    run_command([
        "pdftoppm", "-png", "-r", "180", str(rendered_pdf), str(output_dir / prefix),
    ], cwd=cwd)
    return sorted(output_dir.glob(f"{prefix}-*.png"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def relative_ref(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def yaml_scalar(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def build_bundle(args: argparse.Namespace) -> dict[str, Any]:
    root = args.root.resolve()
    source = args.source_md.resolve()
    output_dir = args.output_dir.resolve()
    if not source.is_file():
        raise BundleError(f"source Markdown not found: {source}")
    if not TABLE_WIDTH_FILTER.is_file():
        raise BundleError(f"table-width filter not found: {TABLE_WIDTH_FILTER}")
    output_dir.mkdir(parents=True, exist_ok=True)
    docx = output_dir / f"{args.basename}.docx"
    pdf = output_dir / f"{args.basename}.pdf"
    qa_dir = output_dir / f"{args.basename}-qa"
    docx_page_dir = qa_dir / "docx-pages"
    pdf_page_dir = qa_dir / "pdf-pages"
    inspection = qa_dir / "pdf-page-inspection.json"
    payload: dict[str, Any] = {
        "surface_kind": "opl_bookforge_publication_bundle_manifest.v1",
        "version": VERSION,
        "artifact_role": "publication_bundle",
        "status": "blocked",
        "source_markdown": relative_ref(source, root),
        "output_refs": {
            "docx": relative_ref(docx, root),
            "pdf": relative_ref(pdf, root),
        },
        "errors": [],
    }
    try:
        source_bytes = source.read_bytes()
        source_text = source_bytes.decode("utf-8")
        body_text, title_block_removed = strip_title_block(
            source_text, title=args.title, author=args.author, date=args.date
        )
        if not body_text.strip():
            raise BundleError("no manuscript body remains after title-block handling")
        output_dir.mkdir(parents=True, exist_ok=True)
        qa_dir.mkdir(parents=True, exist_ok=True)
        build_inputs = qa_dir / "build-inputs"
        build_inputs.mkdir(parents=True, exist_ok=True)
        fontconfig = prepare_fontconfig(args.fontconfig_file, build_inputs=build_inputs)
        compiled_source = build_inputs / "source.md"
        metadata = build_inputs / "metadata.yaml"
        design_profile = build_inputs / "publication-design-profile.json"
        compiled_source.write_text(body_text, encoding="utf-8")
        compiled_source_sha256 = sha256_file(compiled_source)
        metadata.write_text(
            "\n".join([
                f"title: {yaml_scalar(args.title)}",
                f"author: {yaml_scalar(args.author)}",
                f"date: {yaml_scalar(args.date)}",
                "lang: zh-CN",
                "subject: Book Forge publication bundle",
                "",
            ]),
            encoding="utf-8",
        )
        from bookforge_pdf_export_parts.profile_and_assets import resolve_publication_profile
        profile, profile_path, error = resolve_publication_profile(args.publication_profile, root)
        if error:
            raise BundleError(error)
        from bookforge_pdf_export_parts.profile_and_assets import resolve_profile_path
        selected_reference = args.reference_doc or resolve_profile_path(profile.get("word_reference_doc"), profile_path, root)
        if selected_reference is None:
            selected_reference = TABLE_WIDTH_FILTER.parent / "pdf_profiles/bookforge-zh-a4-publication-reference.docx"
        if not selected_reference.is_file():
            raise BundleError(f"Word reference document not found: {selected_reference}")
        retained_reference = build_inputs / "reference.docx"
        retained_reference.write_bytes(selected_reference.read_bytes())
        args.reference_doc = retained_reference
        embedded_design = profile.get("publication_design_profile") if isinstance(profile, dict) else None
        if args.publication_design_profile:
            design_profile.write_text(Path(args.publication_design_profile).read_text(encoding="utf-8"), encoding="utf-8")
        elif isinstance(embedded_design, dict):
            design_profile.write_text(json.dumps(embedded_design, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            raise BundleError("publication profile has no publication_design_profile; provide --publication-design-profile")

        ast = pandoc_json(compiled_source, cwd=root)
        table_count = count_nodes(ast, "Table")
        image_count = count_nodes(ast, "Image")
        run_command(docx_command(args, source_md=compiled_source, metadata=metadata, output_docx=docx), cwd=root)
        keep_docx_table_rows(docx)
        pdf_payload = compile_pdf(parse_pdf_args(pdf_args(
            args,
            source_md=compiled_source,
            metadata=metadata,
            output_pdf=pdf,
            pdf_manifest=qa_dir / "pdf-export.json",
            inspection=inspection,
            pdf_pages=pdf_page_dir,
            design_profile=design_profile,
        )))
        write_pdf_manifest(qa_dir / "pdf-export.json", pdf_payload)
        if pdf_payload.get("status") != "generated":
            raise BundleError(f"PDF export did not complete cleanly: {pdf_payload.get('error') or pdf_payload.get('status')}")
        if pdf_payload.get("artifact_gate", {}).get("status") != "passed":
            raise BundleError("publication PDF technical gate has open quality debt")

        visible_source = visible_ast_text(ast["blocks"])
        docx_readback = docx_body_readback(docx)
        pdf_body_text = pdf_text_readback(pdf, cwd=root)
        docx_body_text = docx_readback["text"]
        norm_docx = normalized_text(docx_body_text)
        norm_pdf = normalized_text(pdf_body_text)
        coverage_docx = source_coverage(visible_source, docx_body_text)
        coverage_pdf = source_coverage(visible_source, pdf_body_text)
        text_equal = norm_docx == norm_pdf
        similarity = difflib.SequenceMatcher(a=norm_docx, b=norm_pdf, autojunk=False).ratio()
        docx_pages = render_docx(docx, output_dir=docx_page_dir, prefix="docx-page", cwd=root,
                                 soffice=args.soffice, fontconfig=fontconfig)
        docx_render_pdf = docx_page_dir / f"{docx.stem}.pdf"
        render_readback = rendered_text_integrity(visible_source, pdf_text_readback(docx_render_pdf, cwd=root),
                                                   title=args.title, author=args.author, date=args.date)
        pdf_pages = sorted(pdf_page_dir.glob("pdf-page-*.png"))
        docx_page_count = len(docx_pages)
        pdf_page_count = len(pdf_pages)
        pdf_inspection = pdf_payload.get("rendered_page_inspection") or {}
        font_inspection = pdf_inspection.get("embedded_font_inspection") or {}
        expected_identity = [normalized_text(args.title), normalized_text(args.author), normalized_text(args.date)]
        identity_in_docx = all(value in norm_docx for value in expected_identity)
        identity_in_pdf = all(value in norm_pdf for value in expected_identity)
        image_refs = pdf_payload.get("markdown_image_refs") or {}
        parity = {
            "title_byline_date_equality": identity_in_docx and identity_in_pdf,
            "normalized_text_parity": text_equal,
            "source_coverage_docx": round(coverage_docx, 6),
            "source_coverage_pdf": round(coverage_pdf, 6),
            "source_coverage_docx_render": round(render_readback["source_coverage"], 6),
            "docx_render_title_byline_date_present": render_readback["title_byline_date_present"],
            "source_coverage_threshold": MIN_SOURCE_COVERAGE,
            "source_coverage_method": "nfkc_cjk_character_latin_word_multiset",
            "normalized_text_similarity": round(similarity, 6),
            "table_count_parity": table_count == docx_readback["table_count"],
            "figure_count_parity": (
                image_count == docx_readback["figure_count"]
                and image_count == image_refs.get("total", -1)
                and image_refs.get("missing_count", -1) == 0
            ),
        }
        page_and_font = {
            "docx_page_count": docx_page_count,
            "pdf_page_count": pdf_page_count,
            "docx_rendered_page_refs": [relative_ref(path, root) for path in docx_pages],
            "pdf_rendered_page_refs": [relative_ref(path, root) for path in pdf_pages],
            "pdf_font_readback": font_inspection.get("status", "missing"),
            "embedded_pdf_font_count": font_inspection.get("embedded_font_count", 0),
        }
        errors = [key for key in ("title_byline_date_equality", "table_count_parity", "figure_count_parity") if not parity[key]]
        if coverage_docx < MIN_SOURCE_COVERAGE:
            errors.append("docx_source_coverage_below_threshold")
        if coverage_pdf < MIN_SOURCE_COVERAGE:
            errors.append("pdf_source_coverage_below_threshold")
        if render_readback["source_coverage"] < MIN_SOURCE_COVERAGE:
            errors.append("docx_render_source_coverage_below_threshold")
        if not render_readback["title_byline_date_present"]:
            errors.append("docx_render_title_byline_date_missing")
        if not docx_page_count:
            errors.append("docx_rendered_pages_missing")
        if not pdf_page_count:
            errors.append("pdf_rendered_pages_missing")
        if page_and_font["pdf_font_readback"] != "passed":
            errors.append("pdf_embedded_font_readback_not_passed")
        all_pass = not errors
        payload.update({
            "status": "ready_for_owner_review" if all_pass else "completed_with_quality_debt",
            "claim_boundary": {
                "ready_for_owner_review": all_pass,
                "publication_approval": False,
                "final_export_acceptance": False,
            },
            "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
            "compiled_markdown_sha256": compiled_source_sha256,
            "docx_sha256": sha256_file(docx),
            "pdf_sha256": sha256_file(pdf),
            "source_metadata": {"title": args.title, "author": args.author, "date": args.date},
            "source_content": {"table_count": table_count, "figure_count": image_count, "title_block_removed": title_block_removed},
            "docx_readback": {"table_count": docx_readback["table_count"], "figure_count": docx_readback["figure_count"]},
            "pdf_export_status": pdf_payload.get("status"),
            "pdf_artifact_gate": pdf_payload.get("artifact_gate", {}).get("status"),
            "parity": parity,
            "build_evidence_refs": {
                "compiled_markdown": relative_ref(compiled_source, root),
                "metadata": relative_ref(metadata, root),
                "design_profile": relative_ref(design_profile, root),
                "pdf_export_receipt": relative_ref(qa_dir / "pdf-export.json", root),
                "docx_render_pdf": relative_ref(docx_render_pdf, root),
                "reference_docx": relative_ref(args.reference_doc, root) if args.reference_doc else None,
                "reference_docx_sha256": sha256_file(args.reference_doc),
                "publication_profile": relative_ref(profile_path, root) if profile_path else None,
                "fontconfig": relative_ref(fontconfig, root) if fontconfig else None,
            },
            "page_and_font": page_and_font,
            "pdf_export_evidence": {
                "artifact_role": pdf_payload.get("artifact_role"),
                "backend": pdf_payload.get("backend"),
                "status": pdf_payload.get("status"),
                "source_markdown": relative_ref(source, root),
                "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
                "pdf_page_count": pdf_page_count,
                "rendered_page_refs": [relative_ref(path, root) for path in pdf_pages],
                "embedded_font_inspection": font_inspection,
                "artifact_gate": pdf_payload.get("artifact_gate"),
                "markdown_image_refs": image_refs,
            },
            "quality_boundary": {
                "fast_path_is_orchestration_only": True,
                "rendered_page_review_required": True,
                "bundle_is_publication_approval": False,
                "bundle_is_final_export": False,
            },
        })
        payload["errors"] = errors
    except Exception as exc:
        payload["status"] = "completed_with_quality_debt" if docx.is_file() or pdf.is_file() else "blocked"
        payload["errors"] = [str(exc)]
    return payload


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--source-md", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--basename", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--author", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--reference-doc", type=Path)
    parser.add_argument("--fontconfig-file", type=Path, default=os.environ.get("FONTCONFIG_FILE"),
                        help="Explicit host Fontconfig file; macOS otherwise discovers system and user font dirs")
    parser.add_argument("--soffice", default=os.environ.get("BOOKFORGE_SOFFICE", "soffice"),
                        help="LibreOffice executable; use the host bundled runtime when available")
    parser.add_argument("--publication-profile", default="bookforge-zh-a4-publication")
    parser.add_argument("--publication-design-profile", type=Path)
    parser.add_argument("--figure-asset-manifest", type=Path)
    parser.add_argument("--resource-path", type=Path, action="append", default=[])
    parser.add_argument("--number-sections", dest="number_sections", action="store_true")
    parser.add_argument("--no-number-sections", dest="number_sections", action="store_false")
    parser.set_defaults(number_sections=False)
    parser.add_argument("--table-of-contents", dest="table_of_contents", action="store_true")
    parser.add_argument("--no-table-of-contents", dest="table_of_contents", action="store_false")
    parser.set_defaults(table_of_contents=False)
    parser.add_argument("--manifest", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    args.root = args.root.resolve()
    def rooted(path: Path | None) -> Path | None:
        if path is None:
            return None
        return path.resolve() if path.is_absolute() else (args.root / path).resolve()
    args.source_md = rooted(args.source_md)
    args.output_dir = rooted(args.output_dir)
    args.reference_doc = rooted(args.reference_doc)
    args.fontconfig_file = rooted(args.fontconfig_file)
    args.publication_design_profile = rooted(args.publication_design_profile)
    args.figure_asset_manifest = rooted(args.figure_asset_manifest)
    args.manifest = rooted(args.manifest)
    args.resource_path = [rooted(path) for path in args.resource_path] or [args.source_md.parent, args.root]
    try:
        payload = build_bundle(args)
    except Exception as exc:
        payload = {
            "surface_kind": "opl_bookforge_publication_bundle_manifest.v1",
            "version": VERSION,
            "artifact_role": "publication_bundle",
            "status": "blocked",
            "errors": [str(exc)],
        }
    manifest = args.manifest or (args.output_dir / f"{args.basename}.publication-bundle.json")
    write_json(manifest, payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload.get("status") == "ready_for_owner_review" else 1


if __name__ == "__main__":
    raise SystemExit(main())
