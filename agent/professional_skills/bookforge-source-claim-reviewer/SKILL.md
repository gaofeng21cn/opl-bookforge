---
name: bookforge-source-claim-reviewer
description: Use when OPL Book Forge must verify nonfiction claims, source locators, evidence classes, case boundaries, anti-leakage, and unsupported gaps.
---

# Book Forge Source Claim Reviewer

## Purpose

Protect nonfiction truth and source boundaries during drafting, repair, packaging, and handoff. This skill is the Codex skill form of `agent/skills/source-claim-integrity.md`.

## Inputs

- Source map, owner-supplied material, source locators, chapter packages, manuscript refs, tables, figures, captions, callouts, and case notes.
- Reader-style contract and author/source stance map.
- Citation display policy for the artifact target, including footnote/endnote/back-matter split when present.
- Existing claim ledger, unsupported-gap list, source passport/lifecycle projection, or truth-delta refs.

## Outputs

- Claim ledger with claim ids, locators, evidence class, support status, source provenance, freshness stamp, and audit note.
- Source locator and evidence-boundary report.
- Unsupported-gap list with typed blockers or next-source-actions.
- Truth delta and anti-leakage note after claim repairs.

## Execution Rules

- Match language to evidence class: constructed scene, typical scenario, documented process material, authorized material/interview, owner-supplied source, outcome/impact evidence, or unsupported gap.
- Tables, figures, captions, callouts, and case boxes are claims too.
- For book-length nonfiction, separate source truth from source display. External reports, policies, public data, and third-party cases need locators; reader-facing footnotes may be short book notes when full source data is preserved in back matter, source maps, or control refs.
- Practice-involved cases do not become external-source claims just because public materials helped verification. Use the approved participant/designer voice in prose, keep public/authorization/source locators in control refs, and block public-facing text that says `公开资料显示`, `公开报道显示`, or similar outside-observer phrasing for such cases.
- Remove, bracket, or downgrade unsupported non-central claims; return a typed blocker when a central claim lacks required evidence.
- Do not fabricate locators, invent source authority, leak private owner material, or turn weak evidence into outcome language.
- OPL lifecycle/readback can project refs only; Book Forge owns claim and source bodies.

## Stage Prompt Boundary

- `book-materialization` invokes this skill before strengthening claims, after major rewrites, and at chapter/assembly boundaries.
- Stage prompts do not contain source-review logic beyond naming required refs and accepted blocker shapes.
- This skill blocks only the affected claim, section, chapter, handoff, proof, or readiness claim; it should not freeze unrelated drafting.

## Blockers And Repair Targets

- `source_locator_missing`: locate source or remove/bracket claim.
- `missing_outcome_evidence`: remove outcome language or request outcome evidence.
- `owner_authorization_needed`: ask owner before using protected material.
- `practice_stance_overclaim`: repair author/source stance and claim wording.
- `citation_display_mismatch`: move long academic-style citation detail out of reader-facing notes or restore missing locator detail in back matter/control refs.
- `stale_claim_audit`: rerun claim review after source or manuscript changes.
- `private_material_leakage`: remove public-facing leak and update anti-leakage note.
