# Whole-Book Meta Review And Integrity Gate Stage

Stage id: `source-style-integrity-review`
Action ref: `materialize-book`

This independent StageRun reviews materialized chapter packages for whole-book coherence, source/claim safety, style consistency, internal-language leakage, sentence integrity, and defect-owner routing. It uses one new `producer` Attempt and a fresh Codex thread that cannot inherit or resume author or repair conversations. It does not start reviewer, repairer, or re-reviewer Attempts inside this Meta Review StageRun.

The stage does not edit manuscript artifacts. It returns an integrity handoff to `publication-proof-handoff`, route-back refs to the earliest owning storyline/planning/materialization Stage, closure criteria, typed blockers, or human gates.
