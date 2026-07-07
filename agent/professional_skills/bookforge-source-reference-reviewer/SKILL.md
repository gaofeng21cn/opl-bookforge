---
name: bookforge-source-reference-reviewer
description: Use when OPL Book Forge must review source/claim integrity or absorb stronger references without copying protected prose or weakening evidence boundaries.
---

# Book Forge Source Reference Reviewer

## Purpose

Protect nonfiction truth while converting stronger references into reusable production rules. This workflow-level skill replaces the separate source-claim reviewer and reference absorber entries.

## Inputs

- Source map, owner material, source locators, claim ledger, unsupported-gap list, chapter packages, manuscript refs, figures, tables, captions, callouts, and case notes.
- Reader-style contract, author/source stance map, chapter function contract, artifact route, style engine, QC reports, publication design refs, or critique refs.
- Owner-supplied stronger draft, prior version, edited chapter, comparable passage, review PDF, photo/case bundle, or reviewer-supplied material.

## Outputs

- Claim ledger with locators, evidence class, support status, provenance, freshness stamp, and audit note.
- Source locator and evidence-boundary report, unsupported-gap list, truth delta, and anti-leakage note.
- Reference absorption report with comparison scope, transferable strengths, non-transferable patterns, adopted rules, retained active-manuscript strengths, and remaining owner/source decisions.
- Updates to reader-entry plans, chapter task cards, style engine, concept map, core model map, case evidence ladder, QC gates, source maps, or publication design refs.

## Execution Rules

- Match language to evidence class: constructed scene, typical scenario, documented process material, authorized material/interview, owner-supplied source, outcome/impact evidence, or unsupported gap.
- Tables, figures, captions, callouts, case boxes, footnotes, and book notes are claims too.
- Keep source truth separate from reader-facing source display. Short book notes are allowed only when full locator detail remains in back matter, source maps, or control refs.
- For practice-involved cases, use the approved participant/designer voice and block outside-observer phrasing such as `公开资料显示` when it contradicts the stance.
- Remove, bracket, or downgrade unsupported non-central claims; return typed blockers for central unsupported claims.
- Extract craft patterns from references; do not copy protected prose, examples, claims, photos, or voice unless independently authorized.
- If concise review and formal publication routes diverge, record `target_artifact_choice` before more local polish.
- Reference/style lessons are advisory unless the current claim is reference absorption closure, copied-reference authority, primary-reader drift, publication proof, final export, or proof/export readiness.

## Stage Prompt Boundary

- Stage prompts may trigger source review or reference absorption, but this skill owns the review and adoption method.
- Use before strengthening claims, after major rewrites, at chapter/assembly boundaries, and before affected drafting when the owner says a reference version is stronger.
- This skill does not prove whole-book completion, publication proof, final export, owner acceptance, or source authority beyond recorded refs.

## Blockers And Repair Targets

- `source_locator_missing`: locate source or remove/bracket the claim.
- `missing_outcome_evidence`: remove outcome language or request outcome evidence.
- `owner_authorization_needed`: ask owner before using protected material.
- `practice_stance_overclaim`: repair stance and claim wording.
- `citation_display_mismatch`: move long citation detail out of reader-facing notes or restore locator detail in control refs.
- `private_material_leakage`: remove public-facing leak and update anti-leakage refs.
- `reference_absorption_missing`: create adoption report before claiming reference feedback absorbed.
- `reference_copy_risk`: route through source authorization and style rejection.
- `publication_book_feel_gap`: decide artifact route or open formal-publication expansion queue.
- `target_artifact_choice_missing`: stop local proof/publication claims until route is recorded.
