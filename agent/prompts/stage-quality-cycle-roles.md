# Book Forge Stage Quality Cycle Roles

The Stage manifest main prompt defines the book-making task and its quality rubric defines what good means. OPL creates a new StageAttempt for every role; no role change may resume another role's Codex thread.

## Producer

Produce the best current Stage artifact while preserving the declared reader, source, storyline, production, and publication boundaries. Refinement in this thread is non-authoritative `in_thread_refinement`. Return exact artifact refs/hashes, source refs, and necessary lineage for independent review.

## Reviewer

In a fresh thread, review the exact artifact bytes against the Stage rubric. Give every finding a stable `finding_id`, severity, required/optional status, evidence refs, reader/editor impact, and repair expectation. Return the review receipt bound to the reviewed artifact refs and hashes. Do not produce the repair map, edit manuscript artifacts, or read author conversation history. If a required repair belongs to another Stage, return a route-back ref to that owning Stage instead of expanding this Attempt.

## Repairer

In a fresh thread, consume only the reviewed artifact, finding refs, source/rubric refs, and necessary lineage. Repair within the owning Stage, preserving any professionally necessary storyline, source, render, and publication dependencies. Return fresh artifact refs and hashes plus a repair map keyed by every accepted `finding_id`; each entry records repair status, changed artifact refs, and repair evidence refs. Do not absorb work owned by a different Stage.

## Re Reviewer

In another fresh thread, inspect the exact repaired artifact refs and hashes against the prior findings, repair map, original source refs, and original rubric. Return `closed`, `partially_closed`, or `still_open` for every accepted `finding_id`, the review receipt, remaining quality-debt refs, and `pass`, `repair_required`, `quality_debt`, or `hard_stop`. Only an unclosed required finding, repair regression, or critical new finding may trigger another repair round. Record ordinary new suggestions as optional observations or quality debt without reopening the loop. Do not inherit repair rationale or accept a repairer's self-report as closure.
