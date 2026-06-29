# OPL Book Forge Skills

Skill policy refs declare direct domain entry points and keep parity with OPL-hosted invocation receipts.

Temporal StageRun refs are consumed under `contracts/temporal_stage_run_consumption_policy.json`. Skills must treat provider attempt completion and generated surface readiness as OPL transport/readback evidence only, never as Book Forge domain readiness or owner acceptance.

Revision skills must preserve the Book Forge repair hierarchy. Independent meta-review diagnoses the assembled manuscript; `revision-entrypoint-router.md` decides the topmost repair layer before prose edits; fast-track revision is only for bounded local or explicitly routed low-risk fixes.
