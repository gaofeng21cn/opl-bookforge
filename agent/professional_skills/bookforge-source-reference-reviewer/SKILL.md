---
name: bookforge-source-reference-reviewer
description: Use when OPL Book Forge must review source/claim integrity or absorb stronger references without copying protected prose or weakening evidence boundaries.
---

# Book Forge Source Reference Reviewer

## Purpose

Protect nonfiction truth while converting stronger references into reusable production rules. This workflow-level skill replaces the separate source-claim reviewer and reference absorber entries.

## Inputs

- Source map, owner material, source locators, claim ledger, unsupported-gap list, chapter packages, manuscript refs, figures, tables, captions, callouts, asset/right refs, and case notes.
- Reader-style contract, author/source stance map, chapter function contract, artifact route, style engine, QC reports, publication design refs, source-memory route-back refs, proof/design memory refs, or critique refs.
- Owner-supplied stronger draft, prior version, edited chapter, comparable passage, review PDF, photo/case bundle, or reviewer-supplied material.

## Outputs

- Claim ledger with locators, evidence class, support status, provenance, freshness stamp, and audit note.
- Source locator and evidence-boundary report, unsupported-gap list, truth delta, and anti-leakage note.
- Reference absorption report with comparison scope, transferable strengths, non-transferable patterns, adopted rules, retained active-manuscript strengths, and remaining owner/source decisions.
- Source-memory route-back packet for stale, unsupported, conflicting, or owner-dependent source/memory claims.
- Asset/right/source freshness obligation list for photos, figures, tables, captions, notes, case material, public-use boundaries, and source locators affected by revision or proof work.
- Updates to reader-entry plans, chapter task cards, style engine, concept map, core model map, case evidence ladder, QC gates, source maps, memory refs, or publication design refs.

## AI-First / Contract-Light Boundary

- This skill owns the flexible professional judgment: claim/source interpretation, evidence-class assignment, reference absorption, protected-material risk, source/memory gap diagnosis, route-back choice, and owner/source handoff.
- Contracts, capability maps, locators, ledgers, and stage refs only identify sources, boundaries, and return shapes. They must not become a second source truth, copied-reference authority, memory truth, publication proof, or owner authorization surface.
- When evidence is insufficient, downgrade, bracket, remove, or route back with the exact owner/source question. Do not solve unsupported claims through contract defaults, citation-looking placeholders, or style-only repair.
- Source/reference risk is an AI judgment, not a schema lookup. Grade missing locators, unsupported claims, stale sources, protected-material copying risk, stance mismatch, caption/callout risk, and public/rights boundary before revision or proof handoff.

## Execution Rules

- Match language to evidence class: constructed scene, typical scenario, documented process material, authorized material/interview, owner-supplied source, outcome/impact evidence, or unsupported gap.
- Tables, figures, captions, callouts, case boxes, footnotes, and book notes are claims too.
- Keep source truth separate from reader-facing source display. Short book notes are allowed only when full locator detail remains in back matter, source maps, or control refs.
- For practice-involved cases, use the approved participant/designer voice and block outside-observer phrasing such as `公开资料显示` when it contradicts the stance.
- Remove, bracket, or downgrade unsupported non-central claims; return typed blockers for central unsupported claims.
- Extract craft patterns from references; do not copy protected prose, examples, claims, photos, or voice unless independently authorized.
- When a stronger reference or prior version is supplied, compare its reader function, evidence shape, structure, and style moves against the active manuscript. Adopt transferable rules, preserve active-manuscript strengths, and route non-local lessons to storyline/style, chapter task cards, memory, or publication design refs.
- Treat owner critique as source-review input only after classifying whether each point changes evidence, source stance, rights/public boundary, memory, artifact target, or prose style.
- Before adopting proof/design memory or reference examples, recheck source, asset, rights, caption, note, and public-use freshness for every affected artifact class.
- Before publication-proof or final-export handoff, clear or explicitly route back source/reference risks that affect claims, captions, tables, figures, notes, photos, rights, or durable memory. Rendered pages cannot close source risk.
- If concise review and formal publication routes diverge, record `target_artifact_choice` before more local polish.
- Reference/style lessons are advisory unless the current claim is reference absorption closure, copied-reference authority, primary-reader drift, publication proof, final export, or proof/export readiness.

## Stage Prompt Boundary

- Stage prompts may trigger source review or reference absorption, but this skill owns the review and adoption method.
- Use before strengthening claims, after major rewrites, at chapter/assembly boundaries, and before affected drafting when the owner says a reference version is stronger.
- This skill does not prove whole-book completion, publication proof, final export, owner acceptance, or source authority beyond recorded refs.

## Legacy Coverage

This workflow-level skill covers the retired `bookforge-reference-absorber` and `bookforge-source-claim-reviewer` entries. Keep reference absorption, claim integrity, evidence-class assignment, unsupported-gap triage, asset/right/source freshness, source-memory route-back, and anti-leakage review together; do not restore the retired fine-grained skill directories.

## Blockers And Repair Targets

- `source_locator_missing`: locate source or remove/bracket the claim.
- `missing_outcome_evidence`: remove outcome language or request outcome evidence.
- `owner_authorization_needed`: ask owner before using protected material.
- `asset_rights_freshness_missing`: refresh asset/source/right refs before proof, export, or public-facing artifact claims.
- `practice_stance_overclaim`: repair stance and claim wording.
- `citation_display_mismatch`: move long citation detail out of reader-facing notes or restore locator detail in control refs.
- `private_material_leakage`: remove public-facing leak and update anti-leakage refs.
- `reference_absorption_missing`: create adoption report before claiming reference feedback absorbed.
- `reference_copy_risk`: route through source authorization and style rejection.
- `source_memory_route_back_missing`: return source or memory route-back before revising durable claims.
- `publication_book_feel_gap`: decide artifact route or open formal-publication expansion queue.
- `target_artifact_choice_missing`: stop local proof/publication claims until route is recorded.
