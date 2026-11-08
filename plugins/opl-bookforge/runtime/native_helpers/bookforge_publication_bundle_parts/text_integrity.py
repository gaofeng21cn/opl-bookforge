"""Visible manuscript text and extraction-integrity checks."""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from typing import Any
from .errors import (
    BundleError,
)


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


def count_nodes(value: Any, node_type: str) -> int:
    if isinstance(value, dict):
        own = 1 if value.get("t") == node_type else 0
        return own + sum(count_nodes(item, node_type) for item in value.values())
    if isinstance(value, list):
        return sum(count_nodes(item, node_type) for item in value)
    return 0


def rendered_text_integrity(source: str, rendered: str, *, title: str, author: str, date: str) -> dict[str, Any]:
    normalized = normalized_text(rendered)
    return {
        "source_coverage": source_coverage(source, rendered),
        "title_byline_date_present": all(normalized_text(value) in normalized for value in (title, author, date)),
    }
