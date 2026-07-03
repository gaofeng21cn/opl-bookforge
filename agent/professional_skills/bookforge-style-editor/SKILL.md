---
name: bookforge-style-editor
description: Use when OPL Book Forge must calibrate, apply, or audit reusable book prose style, anti-AI-flavor rules, terminology, rhythm, and reader-facing expression.
---

# Book Forge Style Editor

## Purpose

Maintain book-specific prose style as a durable Book Forge domain ref, not a generic humanizer. This skill combines `agent/skills/style-engine.md`, `style-calibration.md`, and reader-facing style repair rules.

## Inputs

- Reader-style contract, source stance map, chapter function contract, source/evidence boundary, and house style.
- Owner samples, reference drafts, comparable works, prior chapters, QC findings, meta-review findings, or fatigue scans.
- Active manuscript refs or chapter refs to scan.

## Outputs

- Style profile with adoption/rejection rules and owner-review status.
- Sentence rhythm, paragraph movement, terminology map, forbidden patterns, fatigue list, and accepted exceptions.
- Style QC report with concrete locations/counts or a no-occurrence statement.
- Back-propagated updates to style engine, chapter task cards, glossary, reader-entry plans, QC reports, or semantic memory.

## Execution Rules

- Confirm reader-style and source stance first; style cannot override reader promise or evidence boundary.
- Extract transferable craft rules from references; do not copy reference prose, examples, claims, or protected voice.
- Prefer affirmative, concrete movement, precise verbs, stable terms, and reader-action openings.
- Treat high-risk workflow/internal language and formulaic AI-flavor patterns as scan targets, not impressionistic polish.
- Preserve argument density and source restraint while improving rhythm.

## Stage Prompt Boundary

- Stage prompts may request a style profile or QC result; this skill owns the editorial method and scan discipline.
- Use this skill before broad chapter rewriting when recurring style defects, owner samples, stronger references, or repeated QC findings exist.
- This skill does not approve manuscript quality, publication readiness, or owner acceptance.

## Blockers And Repair Targets

- `reader_style_missing`: route to `bookforge-reader-style-designer`.
- `style_profile_conflicts_with_primary_reader`: repair reader contract or reject imported pattern.
- `reference_copy_risk`: route to `bookforge-reference-absorber` and source review.
- `style_repair_hides_source_gap`: route to `bookforge-source-claim-reviewer`.
- `systemic_memo_like_drafting`: update style engine and chapter authoring pattern before continuing.
