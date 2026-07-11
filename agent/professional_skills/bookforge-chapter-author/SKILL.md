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
- Owner/reviewer critique, complete-version comparison refs, proof/design memory refs, asset/right/source freshness refs, or accepted revision-entrypoint decision when the task is a repair.

## Outputs

- Chapter context pack or refreshed context trace.
- Chapter brief, reader-entry plan, chapter Markdown draft or repair, chapter QC notes, repair log, and memory updates.
- Owner critique absorption log for chapter-level concerns, non-local route-backs, accepted no-change decisions, and downstream freshness obligations.
- Source-memory, asset/right/source, proof/design memory, or complete-version route-back refs when chapter prose cannot safely absorb the issue locally.
- Updated production queue state: `not_started`, `outline_only`, `seed_in_progress`, `draft_in_progress`, `chapter_text_ready`, `chapter_draft_ready`, or `blocked`.
- Review-PDF eligibility note for contiguous ready/text-ready sequence.

## AI-First / Contract-Light Boundary

- This skill owns the flexible professional judgment: context sufficiency, material-gap recognition, chapter repair shape, prose quality, continuity risk, review-PDF eligibility, route-back target, and owner-facing handoff.
- Contracts, capability maps, queue refs, memory refs, and artifact refs only locate inputs, declare boundaries, and preserve traceable return shapes. They must not become a second manuscript body, memory body, quality verdict, or publication/export readiness authority.
- Use AI review to decide whether a defect belongs to local prose, source/claim integrity, storyline/style architecture, memory continuity, asset readiness, or owner decision. Route upward instead of masking the defect with a local rewrite.
- Obey accepted revision-entrypoint routing. Draft or repair chapter Markdown only when the topmost defect is local chapter prose; route back when the defect is structural, source/reference, memory, proof/artifact, or owner-decision level.
- Reuse proof/design memory and complete-version comparison only as constraints on local chapter prose; route broad style, asset, rights, source, or publication-design changes to the owning skill/ref.

## Execution Rules

- Start with the earliest unfinished required unit unless the owner explicitly approves a non-contiguous exploration pass.
- Compile context before drafting or repair; protect reader promise, owner decisions, source canon, evidence boundaries, target extent, author/source stance, and chapter function.
- For long-book work, operate on the chapter-sharded package: chapter task card, context pack, chapter Markdown, QC note, repair log, memory trace, and production queue state. Do not treat merged `book.md` or a compact preview as the repair source of truth.
- Visible manuscript prose must read like book prose on the first pass. Keep task fields, budgets, blockers, source refs, QC status, and reader-entry plans out of the manuscript body.
- When replacing generic examples with practice cases, first bind the case to the chapter's job: which misconception it corrects, which turn or feedback changed the problem, and what evidence is allowed in reader-facing prose. Do not leave material-collection notes, public-source caveats, version labels, or author TODOs in the manuscript.
- Absorb owner critique only after routing each point to local prose, chapter function, source/reference, memory, proof/design, asset/rights, or owner decision; do not let local prose repair hide a higher-layer defect.
- Reuse a spine case across chapters only by changing the reader function of the scene, not by repeating the same summary. Record the reuse in the chapter task card or case map.
- Keep case boxes, figures, photos, and reviewer notes separate: a case box is prose evidence, a figure/photo is a visual asset with its own manifest entry, and reviewer notes stay outside publication prose.
- Before claiming chapter text ready, state which source ledger, memory refs, asset/right refs, and proof/design refs are fresh enough for that claim or route them back.
- Meet chapter budget with substantive argument, examples, cases, transitions, and figure/table interpretation. Do not pad or relabel short seed text as done.
- After accepted local repair, report which source ledger, memory refs, assembly metrics, review PDF, or publication-proof refs need refresh. Do not claim proof/export/owner progress from chapter prose alone.
- After chapter changes, refresh QC, memory, assembly/metrics/hygiene/review refs in freshness order when those claims are made.

## Stage Prompt Boundary

- `chapter-production-planning` states admitted target refs and task-card shape; `chapter-materialization` carries the authorized drafting route, and this skill provides the chapter writing method.
- This skill writes or repairs chapter Markdown only inside an authorized book workspace, not in this repo's professional skill pack.
- This skill cannot claim book readiness, publication proof, final export, or owner acceptance by itself.

## Legacy Coverage

This workflow-level skill covers the retired `book-production`, `chapter-context-compiler`, `chapter-runtime`, `reader-facing-draft`, and `book-memory` chapter-production entries named in the purpose. Keep context compilation, chapter drafting, reader-facing repair, production queue state, owner critique absorption, and memory-aware chapter handoff together; do not restore the retired fine-grained skill directories.

## Blockers And Repair Targets

- `chapter_task_card_missing`: create or repair chapter task card before drafting.
- `target_extent_missing`: repair production budget before body drafting.
- `reader_style_missing`: route to `bookforge-story-style-architect`.
- `source_locator_missing` or `practice_stance_overclaim`: route to `bookforge-source-reference-reviewer`.
- `chapter_function_conflict`: route to `bookforge-story-style-architect` or revision entrypoint.
- `case_role_ambiguous`: repair the case map or chapter task card before inserting the example.
- `owner_critique_route_missing`: classify critique by repair layer before local chapter edits.
- `source_memory_route_back_missing`: route durable source or memory defects before chapter-ready claims.
- `asset_rights_freshness_missing`: refresh or route asset/source/right refs before chapter text or proof-facing handoff claims.
- `proof_design_memory_stale`: refresh or route proof/design memory before layout-sensitive chapter repairs.
- `review_continuity_blocker`: finish earlier required unit before later review PDF claim.
