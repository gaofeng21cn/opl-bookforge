"""DOCX package readback, note order and table-row preservation."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
from xml.dom import minidom
from zipfile import ZipFile
from .errors import (
    BundleError,
)
from .text_integrity import (
    normalized_text,
    visible_ast_text,
)


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


NS = {"w": W_NS}


def docx_body_readback(path: Path) -> dict[str, Any]:
    note_parts: dict[str, dict[str, ET.Element]] = {}
    with ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
        for kind in ("footnote", "endnote"):
            part = f"word/{kind}s.xml"
            definitions: dict[str, ET.Element] = {}
            if part in archive.namelist():
                for note in ET.fromstring(archive.read(part)):
                    if note.tag != f"{{{W_NS}}}{kind}":
                        continue
                    if note.get(f"{{{W_NS}}}type", "normal") != "normal":
                        continue
                    note_id = note.get(f"{{{W_NS}}}id")
                    if note_id is None or note_id in definitions:
                        raise BundleError(f"DOCX {kind} has missing or duplicate id: {note_id}")
                    definitions[note_id] = note
            note_parts[kind] = definitions
    body = root.find("w:body", NS)
    if body is None:
        raise BundleError("DOCX has no document body")
    blocks: list[str] = []
    table_count = 0
    drawing_count = 0
    notes: list[dict[str, str]] = []
    used: dict[str, set[str]] = {kind: set() for kind in note_parts}
    text_tag = f"{{{W_NS}}}t"
    reference_tags = {f"{{{W_NS}}}{kind}Reference": kind for kind in note_parts}
    for child in body:
        if child.tag == f"{{{W_NS}}}sectPr":
            continue
        table_count += sum(1 for node in child.iter() if node.tag == f"{{{W_NS}}}tbl")
        drawing_count += sum(1 for node in child.iter() if node.tag == f"{{{W_NS}}}drawing")
        text: list[str] = []
        for node in child.iter():
            if node.tag == text_tag:
                text.append(node.text or "")
            elif node.tag in reference_tags:
                kind = reference_tags[node.tag]
                note_id = node.get(f"{{{W_NS}}}id")
                note = note_parts[kind].get(note_id)
                if note is None:
                    raise BundleError(f"DOCX {kind} reference has no definition: {note_id}")
                if any(item.tag in reference_tags for item in note.iter()):
                    raise BundleError(f"DOCX nested note reference is unsupported: {kind} {note_id}")
                note_text = "".join(item.text or "" for item in note.iter() if item.tag == text_tag)
                notes.append({"kind": kind, "id": note_id, "text": note_text})
                text.append(f"\n{note_text}\n")
                used[kind].add(note_id)
                table_count += sum(1 for item in note.iter() if item.tag == f"{{{W_NS}}}tbl")
                drawing_count += sum(1 for item in note.iter() if item.tag == f"{{{W_NS}}}drawing")
        blocks.append("".join(text))
    for kind, definitions in note_parts.items():
        orphaned = set(definitions) - used[kind]
        if orphaned:
            raise BundleError(f"DOCX {kind} definitions have no reference: {', '.join(sorted(orphaned))}")
    return {"text": "\n".join(blocks), "table_count": table_count,
            "figure_count": drawing_count, "notes": notes}


def note_integrity(ast: Any, readback: dict[str, Any]) -> dict[str, Any]:
    """Compare notes in anchor order so a global coverage score cannot hide loss or swaps."""
    expected: list[str] = []

    def collect(value: Any) -> None:
        if isinstance(value, dict):
            if value.get("t") == "Note":
                expected.append(visible_ast_text(value["c"]))
            else:
                for item in value.values():
                    collect(item)
        elif isinstance(value, list):
            for item in value:
                collect(item)

    collect(ast)
    actual = readback["notes"]
    mismatches = []
    for index, (source, note) in enumerate(zip(expected, actual), 1):
        if normalized_text(source) != normalized_text(note["text"]):
            mismatches.append({"ordinal": index, "kind": note["kind"], "id": note["id"]})
    return {"source_count": len(expected), "docx_count": len(actual),
            "count_parity": len(expected) == len(actual),
            "text_parity": len(expected) == len(actual) and not mismatches,
            "mismatches": mismatches}


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
