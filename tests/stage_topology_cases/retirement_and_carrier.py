from __future__ import annotations

from pathlib import Path

from .stage_and_action import STAGE_SEQUENCE


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

    primary_skill = (repo / "agent/primary_skill/SKILL.md").read_text(encoding="utf-8")
    carrier_skill = (repo / "plugins/opl-bookforge/skills/opl-bookforge/SKILL.md").read_text(
        encoding="utf-8"
    )
    assert primary_skill == carrier_skill
