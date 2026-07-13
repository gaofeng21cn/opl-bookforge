# Book Forge Stage Quality Cycle Roles

The Stage manifest main prompt defines the book-making task and its quality rubric defines what good means. OPL creates a new StageAttempt for every role; no role change may resume another role's Codex thread.

## Producer

Produce the best current Stage artifact while preserving the declared reader, source, storyline, production, and publication boundaries. Refinement in this thread is non-authoritative `in_thread_refinement`. Return exact artifact refs/hashes, source refs, and necessary lineage for independent review.

## Reviewer

In a fresh thread, review the exact artifact bytes against the Stage rubric. Return finding refs with severity, location, evidence, reader/editor impact, and closure criteria, plus a repair-map ref naming the narrowest owning Stage. Do not edit manuscript artifacts or read author conversation history.

## Repairer

In a fresh thread, consume only the reviewed artifact, finding refs, repair map, source/rubric refs, and necessary lineage. Repair within the owning Stage, preserving any professionally necessary storyline, source, render, and publication dependencies. Return fresh artifact hashes, repair-delta refs, and lineage.

## Re Reviewer

In another fresh thread, inspect the repaired artifact hashes against every accepted finding and the same rubric. Return re-review closure refs per finding, remaining quality-debt refs, and `pass`, `repair_required`, `quality_debt`, or `hard_stop`. Do not inherit repair rationale or accept a repairer's self-report as closure.
