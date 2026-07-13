# Book Forge Stage Quality Cycle Roles

The Stage manifest main prompt defines the book-making task and its quality rubric defines what good means. OPL creates a new StageAttempt for every role; no role change may resume another role's Codex thread.

Cross-Stage route output has one machine shape. A progress-terminal decisive Attempt returns
`route_impact.stage_route_decision` with `decision_kind`, a declared
`target_stage_id` except for `complete`, and non-empty `evidence_refs`. A
non-decisive Attempt may return `route_impact.stage_route_recommendation` with
the same fields plus `reason`. Never return both or use
`route_back_stage_ref`, `selected_next_stage_ref`, `next_stage_ref`, or
`workflow_complete`.

## Quality Budget And Hard Boundaries

Use the controller-provided `quality_round_index`, `max_repair_rounds`, and exact
artifact identity to choose one branch:

- `repair_budget_remaining`: when required defects still need repair and another
  repair round remains, a reviewer or re-reviewer returns outcome
  `repair_required` and at most `route_impact.stage_route_recommendation`. This
  branch is non-terminal; the controller creates the next fresh repairer Attempt.
- `final_budget_consumable`: when required findings remain, no repair round
  remains, and the exact artifact refs and hashes are consumable, the current
  reviewer or re-reviewer is the terminal decisive Attempt. Required findings
  keep outcome `repair_required`; do not relabel them `quality_debt`. Return
  exactly one `route_impact.stage_route_decision` whose `evidence_refs` bind the
  remaining required finding refs and quality-debt refs. The controller
  classifies this branch as `terminal_quality_debt`, projects
  `completed_with_quality_debt`, and follows the selected route. That debt still
  forbids quality, publication, export, or ready claims. Use outcome
  `quality_debt` only when no required finding remains and ordinary non-required
  debt is carried forward.
- `hard_boundary_or_zero_artifact`: an authority, safety, permission, identity,
  currentness, irreversible-action, or human-decision gate, or literal zero
  consumable exact artifact is not a Stage-routing judgment. A reviewer or
  re-reviewer returns outcome `blocked` or `human_gate` with the applicable
  boundary evidence; every Attempt returns neither
  `route_impact.stage_route_decision` nor
  `route_impact.stage_route_recommendation`. Literal zero consumable artifact
  uses `blocked`. The controller terminalizes the StageRun as blocked or
  human-gated.

## Producer

Produce the best current Stage artifact while preserving the declared reader, source, storyline, production, and publication boundaries. Refinement in this thread is non-authoritative `in_thread_refinement`. Return exact artifact refs/hashes, source refs, and necessary lineage for independent review.

The producer is decisive only for a progress-terminal result in a primary-only
StageRun such as the whole-book Meta Review. In a StageRun with formal Review,
return at most an evidence-backed
route recommendation and leave the terminal route decision to the reviewer or
re-reviewer. Under `hard_boundary_or_zero_artifact`, return no route output.

For `publication-proof-handoff`, every generated PDF/export is a `review_pending` candidate. The producer cannot close publication-proof, final-export, export-ready, or ready claims.

## Reviewer

In a fresh thread, review the exact artifact bytes against the Stage rubric. Return `route_impact.stage_quality_cycle.outcome` with exactly one of `pass`, `repair_required`, `quality_debt`, `blocked`, or `human_gate`, plus findings with stable `finding_id`, `severity`, `required`, `evidence_refs`, `repair_expectation`, and acceptance-criteria fields, and a precise location and reader/editor impact when relevant. Do not return a standalone receipt `verdict`. Do not create a Review receipt or repair map, edit manuscript artifacts, or read author conversation history. The OPL StageRun controller materializes the Review receipt from this Attempt's identity, session, exact reviewed hashes, rubric, and outcome. It maps `pass`, `repair_required`, and `quality_debt` to the same receipt verdict and maps `blocked` or `human_gate` to receipt verdict `hard_stop`; `hard_stop` is never an Attempt outcome. While repair budget remains, a `repair_required` reviewer is non-terminal and returns at most a route recommendation when the defect belongs to another Stage. At final consumable budget it keeps outcome `repair_required` and follows `final_budget_consumable`. A progress-terminal reviewer returns the terminal route decision; a hard-boundary reviewer returns no route output.

For unchanged `publication-proof-handoff` producer bytes, only this fresh exact-hash Review closeout can clear `review_pending`; downstream owner/export acceptance remains separate.

## Repairer

In a fresh thread, consume only the reviewed artifact, finding refs, source/rubric refs, and necessary lineage. Repair within the owning Stage, preserving any professionally necessary storyline, source, render, and publication dependencies. Return fresh artifact refs and hashes plus a repair map keyed by every accepted `finding_id`; each entry records `repair_status`, `changed_artifact_refs`, and `repair_evidence_refs`. Do not absorb work owned by a different Stage.

A repairer never makes a terminal route decision. When no hard boundary applies,
if a required repair belongs outside the inherited Stage goal or authority,
return only a route recommendation for the fresh re-reviewer to judge. Under
`hard_boundary_or_zero_artifact`, return no route output.

For `publication-proof-handoff`, any regenerated PDF/export invalidates the prior Review receipt and remains a `review_pending` candidate. The repairer cannot close publication-proof, final-export, export-ready, or ready claims.

## Re Reviewer

In another fresh thread, inspect the exact repaired artifact refs and hashes against the prior findings, repair map, original source refs, and original rubric. Return `closed`, `partially_closed`, or `still_open` for every accepted `finding_id`, remaining quality-debt and evidence refs, and `route_impact.stage_quality_cycle.outcome` with exactly one of `pass`, `repair_required`, `quality_debt`, `blocked`, or `human_gate`. Do not return a standalone receipt `verdict`. Do not create the controller-owned Review receipt. The controller alone maps `blocked` or `human_gate` to receipt verdict `hard_stop`; `hard_stop` is not an Attempt outcome. Only `required_finding_not_closed`, `repair_regression`, or `critical_new_finding` may trigger another repair round. Record ordinary new suggestions as `optional_observation` or quality debt without reopening the loop. Do not inherit repair rationale or accept a repairer's self-report as closure.

When another repair round is required and remains available, return only a route
recommendation. On the final consumable round, keep outcome `repair_required`
and return the route decision for controller-classified terminal quality debt.
When this re-reviewer progress-terminalizes the StageRun, it returns the terminal
route decision. A hard-boundary re-reviewer returns no route output.

For repaired `publication-proof-handoff` bytes, only this fresh exact-hash re-review closeout can clear `review_pending`; it still cannot replace downstream owner/export acceptance.
