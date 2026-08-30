from __future__ import annotations

from pathlib import Path

from .stage_and_action import STAGE_SEQUENCE

IMMUTABLE_PROVENANCE_ROOTS = ("docs/evidence/", "docs/history/")
TEXT_SUFFIXES = {".json", ".md", ".py", ".sh"}


def assert_no_retired_stage_refs(repo: Path) -> None:
    retired_stage = "-".join(("book", "materialization"))
    stale_refs: list[str] = []
    roots = [
        repo / "README.md",
        repo / "README.zh-CN.md",
        repo / "agent",
        repo / "contracts",
        repo / "docs",
        repo / "runtime",
        repo / "scripts",
        repo / "tests",
    ]
    for root in roots:
        files = [root] if root.is_file() else root.rglob("*")
        for path in files:
            if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
                continue
            rel = str(path.relative_to(repo))
            if rel.startswith(IMMUTABLE_PROVENANCE_ROOTS):
                continue
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if retired_stage in line:
                    stale_refs.append(f"{rel}:{line_number}")
    assert not stale_refs, stale_refs


def assert_retirement_and_carrier(repo: Path, golden_path: dict) -> None:
    assert golden_path["ordinary_path"]["stage_refs"] == ["storyline-architecture"]
    assert golden_path["ordinary_path"]["follow_on_stage_refs"] == STAGE_SEQUENCE[1:]
    assert golden_path["explicit_variants"][0]["stage_refs"] == STAGE_SEQUENCE[1:]

    retired_stage = "-".join(("book", "materialization"))
    for ref in (
        f"agent/prompts/{retired_stage}.md",
        f"agent/stages/{retired_stage}.md",
        f"agent/quality_gates/{retired_stage}-quality-gate.md",
    ):
        assert not (repo / ref).exists(), ref
    assert_no_retired_stage_refs(repo)

    primary_skill = (repo / "agent/primary_skill/SKILL.md").read_text(encoding="utf-8")
    carrier_skill = (repo / "plugins/opl-bookforge/skills/opl-bookforge/SKILL.md").read_text(
        encoding="utf-8"
    )
    assert primary_skill == carrier_skill
    assert "two or three whole-book core models" not in primary_skill.lower()
    assert "description: Use when Codex needs OPL Book Forge to shape or materially produce a book-length nonfiction work" in primary_skill
    assert "Do not use for an isolated article, research paper, grant, slide deck, generic document formatting" in primary_skill
    for heading in (
        "Admission",
        "Action Routing",
        "Default Workflow",
        "Quality And Hard Stops",
        "Output Expectations",
        "References",
    ):
        assert f"## {heading}\n" in primary_skill
    assert "`shape-storyline`: use when the premise" in primary_skill
    assert "`materialize-book`: use when a current approved storyline exists" in primary_skill
    assert "run `shape-storyline` first, obtain the owner decision, then invoke `materialize-book`" in primary_skill
    assert "begins at `chapter-production-planning` and must not silently invent a replacement storyline" in primary_skill
    assert "Scripts may assemble, validate, and export, but must not hide manuscript prose in code or JSON literals" in primary_skill
    assert "Keep `review_pdf`, `publication_proof`, and `final_export` distinct" in primary_skill
    assert "Retry, independent-review, and repair limits are quality budgets" in primary_skill
