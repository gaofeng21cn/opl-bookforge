# OPL Book Forge Skills

Skill policy refs declare direct domain entry points and keep parity with OPL-hosted invocation receipts.

Temporal StageRun refs are consumed under `contracts/temporal_stage_run_consumption_policy.json`. Skills must treat provider attempt completion and generated surface readiness as OPL transport/readback evidence only, never as Book Forge domain readiness or owner acceptance.

Revision skills must preserve the Book Forge repair hierarchy. Independent meta-review diagnoses the assembled manuscript; `revision-entrypoint-router.md` decides the topmost repair layer before prose edits; fast-track revision is only for bounded local or explicitly routed low-risk fixes.

## Professional Skill Pack

Repo-local Codex professional skills live under `agent/professional_skills/*/SKILL.md`. They are the execution-facing layer for professional writing methods that used to be spread across the long stage prompt and these policy refs.

The [professional Skill index](../professional_skills/README.md) owns workflow
routing. The focused policy files in this directory remain active method inputs;
their names are not retired aliases for the professional Skills.

Stage prompts define target refs and accepted handoff shapes. Professional skills carry method. Tool catalogs describe affordances and forbidden authority. None of these skills authorize production readiness, publication readiness, final export, owner acceptance, or OPL runtime ownership.
