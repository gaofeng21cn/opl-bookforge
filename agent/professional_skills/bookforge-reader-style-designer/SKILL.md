---
name: bookforge-reader-style-designer
description: Use when OPL Book Forge must define primary readers, reading situation, natural expression, voice, and author/source stance before drafting or style repair.
---

# Book Forge Reader Style Designer

## Purpose

Create the reader-style contract that governs storyline shaping, chapter drafting, style calibration, QC, and revision. This skill lifts `agent/skills/reader-style-contract.md` into a Codex-invokable professional skill.

## Inputs

- Owner brief, source refs, comparable books, house style, and topic context.
- Existing audience notes, author/source stance notes, critique, or owner edits.
- Known primary, secondary, and excluded reader groups when already declared.

## Outputs

- Reader-style contract with primary/secondary/excluded readers.
- Reading situation, prior knowledge, anxieties, practical questions, and tolerance for theory, examples, jargon, and persuasion.
- Natural-expression rules: stance, vocabulary, rhythm, paragraph movement, example density, metaphor boundary, and forbidden voice patterns.
- Author/source stance map for major cases, including practice-involved voice rules and unsupported-outcome markers.

## Execution Rules

- Primary readers are the writing target. Secondary readers only add compatible accessibility constraints unless the owner promotes them.
- If audience or voice cannot be inferred with high confidence, ask the owner or return a typed blocker before body drafting.
- For practice-involved cases, allow active design/reflection voice but keep missing outcomes, interviews, authorization, feedback, or impact evidence visible as gaps.
- Do not silently change the reader promise to make prose easier to write.

## Stage Prompt Boundary

- Stage prompts name this skill when reader/style authority is needed; they do not duplicate its full policy.
- `book-materialization` must consume the contract before chapter body drafting, style calibration, reference absorption, or meta-review claims.
- This skill defines the prose target; it does not approve final editorial quality or publication readiness.

## Blockers And Repair Targets

- `reader_contract_missing`: create or refresh the contract before drafting.
- `primary_reader_conflict`: route to owner decision or storyline repair.
- `practice_stance_unknown`: repair author/source stance before major case drafting.
- `style_contract_conflicts_with_source_boundary`: route to source-claim review and owner decision.
