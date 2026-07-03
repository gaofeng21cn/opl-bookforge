---
name: bookforge-story-architect
description: Use when OPL Book Forge must shape a book premise, reader promise, argument arc, chapter thesis chain, evidence map, and storyline handoff before chapter drafting.
---

# Book Forge Story Architect

## Purpose

Turn owner intent and source refs into the durable storyline package that `storyline-architecture` owns. This is the professional skill form of `agent/skills/storyline-architecture.md` plus the reader/style and evidence boundaries it requires.

## Inputs

- Owner brief, source plan, comparable book refs, and constraints.
- Existing storyline map, reader-style contract, source map, chapter thesis chain, or critique refs when present.
- Target artifact route when the owner distinguishes review edition, formal publication manuscript, publication proof, or final export.

## Outputs

- Premise, reader promise, argument path, chapter thesis chain, and chapter function contract.
- Early concept map, whole-book core model map, and case evidence ladder.
- Author/source stance map for major cases, including practice-involved cases.
- Storyline handoff with typed blockers, owner questions, or route-back refs.

## Execution Rules

- Establish reader-style and author/source stance before body drafting.
- Give each chapter one primary job, one new argument movement, adjacent handoffs, and non-repeat claims.
- Define or foreshadow recurring terms before readers must rely on them.
- Select two or three core models and state where they are introduced, applied, and recovered.
- Match case language to evidence class; do not turn typical scenes into outcome claims.
- Preserve Book Forge domain truth. OPL may transport refs, but does not decide book semantics or quality.

## Stage Prompt Boundary

- `agent/prompts/book-materialization.md` may request or consume this skill's refs, but it must not inline the full architecture method.
- Use this skill before `bookforge-chapter-author` when storyline, reader promise, chapter function, concept map, core models, or case stance are missing.
- This skill does not draft manuscript bodies, run publication proof, or approve final quality.

## Blockers And Repair Targets

- `reader_style_missing`: route to `bookforge-reader-style-designer`.
- `source_map_missing` or `case_evidence_level_unknown`: route to `bookforge-source-claim-reviewer`.
- `chapter_function_conflict`: repair chapter thesis chain and function contract before prose edits.
- `artifact_target_ambiguous`: record owner decision need before publication-route claims.
- `owner_authorization_needed`: return owner question or typed blocker instead of smoothing the claim.
