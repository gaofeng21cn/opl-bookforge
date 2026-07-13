# Book Forge Stage Quality Cycle Roles

The Stage manifest main prompt defines the book-making task and its quality rubric defines what good means. OPL creates a new StageAttempt for every role; no role change may resume another role's Codex thread.

Cross-Stage route output has one machine shape. A decisive Attempt returns
`route_impact.stage_route_decision` with `decision_kind`, a declared
`target_stage_id` except for `complete`, and non-empty `evidence_refs`. A
non-decisive Attempt may return `route_impact.stage_route_recommendation` with
the same fields plus `reason`. Never return both or use
`route_back_stage_ref`, `selected_next_stage_ref`, `next_stage_ref`, or
`workflow_complete`.

## Producer

Produce the best current Stage artifact while preserving the declared reader, source, storyline, production, and publication boundaries. Refinement in this thread is non-authoritative `in_thread_refinement`. Return exact artifact refs/hashes, source refs, and necessary lineage for independent review.

The producer is decisive only in a primary-only StageRun such as the whole-book
Meta Review. In a StageRun with formal Review, return at most an evidence-backed
route recommendation and leave the terminal route decision to the reviewer or
re-reviewer.

For `publication-proof-handoff`, every generated PDF/export is a `review_pending` candidate. The producer cannot close publication-proof, final-export, export-ready, or ready claims.

## Reviewer

In a fresh thread, review the exact artifact bytes against the Stage rubric. Return `route_impact.stage_quality_cycle.outcome` with exactly one of `pass`, `repair_required`, `quality_debt`, `blocked`, or `human_gate`, plus findings with stable `finding_id`, `severity`, `required`, `evidence_refs`, `repair_expectation`, and acceptance-criteria fields, and a precise location and reader/editor impact when relevant. Do not return a standalone receipt `verdict`. Do not create a Review receipt or repair map, edit manuscript artifacts, or read author conversation history. The OPL StageRun controller materializes the Review receipt from this Attempt's identity, session, exact reviewed hashes, rubric, and outcome. It maps `pass`, `repair_required`, and `quality_debt` to the same receipt verdict and maps `blocked` or `human_gate` to receipt verdict `hard_stop`; `hard_stop` is never an Attempt outcome. If the outcome is `repair_required`, return only a route recommendation when the defect belongs to another Stage and let the controller continue the quality loop. When this reviewer terminalizes the StageRun with a consumable pass, quality-debt, or route-back result, it returns the terminal route decision.

For unchanged `publication-proof-handoff` producer bytes, only this fresh exact-hash Review closeout can clear `review_pending`; downstream owner/export acceptance remains separate.

## Repairer

In a fresh thread, consume only the reviewed artifact, finding refs, source/rubric refs, and necessary lineage. Repair within the owning Stage, preserving any professionally necessary storyline, source, render, and publication dependencies. Return fresh artifact refs and hashes plus a repair map keyed by every accepted `finding_id`; each entry records `repair_status`, `changed_artifact_refs`, and `repair_evidence_refs`. Do not absorb work owned by a different Stage.

A repairer never makes a terminal route decision. If a required repair belongs
outside the inherited Stage goal or authority, return only a route
recommendation for the fresh re-reviewer to judge.

For `publication-proof-handoff`, any regenerated PDF/export invalidates the prior Review receipt and remains a `review_pending` candidate. The repairer cannot close publication-proof, final-export, export-ready, or ready claims.

## Re Reviewer

In another fresh thread, inspect the exact repaired artifact refs and hashes against the prior findings, repair map, original source refs, and original rubric. Return `closed`, `partially_closed`, or `still_open` for every accepted `finding_id`, remaining quality-debt and evidence refs, and `route_impact.stage_quality_cycle.outcome` with exactly one of `pass`, `repair_required`, `quality_debt`, `blocked`, or `human_gate`. Do not return a standalone receipt `verdict`. Do not create the controller-owned Review receipt. The controller alone maps `blocked` or `human_gate` to receipt verdict `hard_stop`; `hard_stop` is not an Attempt outcome. Only `required_finding_not_closed`, `repair_regression`, or `critical_new_finding` may trigger another repair round. Record ordinary new suggestions as `optional_observation` or quality debt without reopening the loop. Do not inherit repair rationale or accept a repairer's self-report as closure.

When another repair round is required and remains available, return only a route
recommendation. When this re-reviewer terminalizes the StageRun, it returns the
terminal route decision.

For repaired `publication-proof-handoff` bytes, only this fresh exact-hash re-review closeout can clear `review_pending`; it still cannot replace downstream owner/export acceptance.
