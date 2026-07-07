---
name: bookforge-chapter-author
description: Use when OPL Book Forge must draft, expand, or repair chapter Markdown from approved storyline, reader-style, source, memory, and chapter task refs.
---

# Book Forge Chapter Author

## Purpose

Produce reader-facing chapter prose through the existing Book Forge chapter package workflow. This skill combines the operative parts of `book-production`, `chapter-context-compiler`, `chapter-runtime`, `reader-facing-draft`, and `book-memory`.

## Inputs

- Approved storyline/style architecture refs, reader-style contract, chapter function contract, concept map, core model map, and case evidence ladder.
- Chapter task card, chapter context pack, source refs, memory refs, style refs, target extent, figure/table obligations, and current chapter state.
- Case priority map, reusable case motifs, public/authorization boundary, and chapter-specific case role when the chapter uses practice material.
- Owner/reviewer critique or accepted revision-entrypoint decision when the task is a repair.

## Outputs

- Chapter context pack or refreshed context trace.
- Chapter brief, reader-entry plan, chapter Markdown draft or repair, chapter QC notes, repair log, and memory updates.
- Updated production queue state: `not_started`, `outline_only`, `seed_in_progress`, `draft_in_progress`, `chapter_text_ready`, `chapter_draft_ready`, or `blocked`.
- Review-PDF eligibility note for contiguous ready/text-ready sequence.

## Execution Rules

- Start with the earliest unfinished required unit unless the owner explicitly approves a non-contiguous exploration pass.
- Compile context before drafting or repair; protect reader promise, owner decisions, source canon, evidence boundaries, target extent, author/source stance, and chapter function.
- Visible manuscript prose must read like book prose on the first pass. Keep task fields, budgets, blockers, source refs, QC status, and reader-entry plans out of the manuscript body.
- When replacing generic examples with practice cases, first bind the case to the chapter's job: which misconception it corrects, which turn or feedback changed the problem, and what evidence is allowed in reader-facing prose. Do not leave material-collection notes, public-source caveats, version labels, or author TODOs in the manuscript.
- Reuse a spine case across chapters only by changing the reader function of the scene, not by repeating the same summary. Record the reuse in the chapter task card or case map.
- Keep case boxes, figures, photos, and reviewer notes separate: a case box is prose evidence, a figure/photo is a visual asset with its own manifest entry, and reviewer notes stay outside publication prose.
- Meet chapter budget with substantive argument, examples, cases, transitions, and figure/table interpretation. Do not pad or relabel short seed text as done.
- After chapter changes, refresh QC, memory, assembly/metrics/hygiene/review refs in freshness order when those claims are made.

## Stage Prompt Boundary

- `book-materialization` states target refs and accepted output shape; this skill carries the chapter writing method.
- This skill writes or repairs chapter Markdown only inside an authorized book workspace, not in this repo's professional skill pack.
- This skill cannot claim book readiness, publication proof, final export, or owner acceptance by itself.

## Blockers And Repair Targets

- `chapter_task_card_missing`: create or repair chapter task card before drafting.
- `target_extent_missing`: repair production budget before body drafting.
- `reader_style_missing`: route to `bookforge-story-style-architect`.
- `source_locator_missing` or `practice_stance_overclaim`: route to `bookforge-source-reference-reviewer`.
- `chapter_function_conflict`: route to `bookforge-story-style-architect` or revision entrypoint.
- `case_role_ambiguous`: repair the case map or chapter task card before inserting the example.
- `review_continuity_blocker`: finish earlier required unit before later review PDF claim.
