# OPL Book Forge Skills

Skill policy refs declare direct domain entry points and keep parity with OPL-hosted invocation receipts.

Temporal StageRun refs are consumed under `contracts/temporal_stage_run_consumption_policy.json`. Skills must treat provider attempt completion and generated surface readiness as OPL transport/readback evidence only, never as Book Forge domain readiness or owner acceptance.

Revision skills must preserve the Book Forge repair hierarchy. Independent meta-review diagnoses the assembled manuscript; `revision-entrypoint-router.md` decides the topmost repair layer before prose edits; fast-track revision is only for bounded local or explicitly routed low-risk fixes.

## Professional Skill Pack

Repo-local Codex professional skills live under `agent/professional_skills/*/SKILL.md`. They are the execution-facing layer for professional writing methods that used to be spread across the long stage prompt and these policy refs.

Routing:

- `bookforge-story-architect`: premise, reader promise, argument arc, chapter function, concept map, core models, case evidence ladder.
- `bookforge-reader-style-designer`: primary readers, natural expression, author/source stance, practice-involved voice.
- `bookforge-chapter-author`: chapter context pack, task card, reader-entry plan, chapter Markdown drafting/repair, QC, memory, review-PDF eligibility.
- `bookforge-style-editor`: style calibration, style engine, terminology, anti-AI-flavor scans, reusable prose rules.
- `bookforge-source-claim-reviewer`: claim ledger, source locator, evidence boundary, unsupported gaps, anti-leakage.
- `bookforge-meta-reviewer`: independent meta-review, revision entrypoint routing, fast-track eligibility, review-repair caps.
- `bookforge-publication-designer`: review PDF / publication proof / final export separation, design tokens, figure/table layout, rendered-page QA.
- `bookforge-reference-absorber`: stronger reference/version comparison and reusable adoption rules.

Stage prompts define target refs and accepted handoff shapes. Professional skills carry method. Tool catalogs describe affordances and forbidden authority. None of these skills authorize production readiness, publication readiness, final export, owner acceptance, or OPL runtime ownership.
