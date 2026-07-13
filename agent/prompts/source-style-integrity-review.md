# Whole-Book Meta Review And Integrity Gate Prompt

## Goal

In an independent StageRun, assess the assembled manuscript for source/claim fidelity, author stance, style consistency, chapter continuity, whole-book coherence, and the earliest owning repair route before proof/export handoff.

## A Good Result

- checks material claims, figures, tables, captions, callouts, and cases against inspectable evidence classes;
- judges naturalness and consistency against the declared readers and style contract rather than a generic prose ideal;
- distinguishes whole-book, storyline, chapter-function, evidence/model, publication-design, and local-prose defects;
- sends each finding to the highest owning surface without forcing local issues through a full storyline rewrite;
- refreshes review evidence after material changes and clearly separates pass, quality debt, route-back, and authority blockers.

Use `bookforge-source-reference-reviewer` for claim integrity and reference absorption, `bookforge-meta-reviewer` for independent whole-book routing, and the story/style specialist when durable architecture needs repair.

This independent Meta Review StageRun uses a `producer` Attempt and a fresh Codex thread. Optional multi-axis subagents remain inside that Attempt and do not become OPL ledger roles. Its inputs are limited to exact manuscript/artifact hashes, Stage Review receipts, source and reader/style refs, the whole-book rubric, and necessary lineage; drafting or repair conversations, thread resumes, and author self-justification are forbidden review context.

Because this StageRun is primary-only, its producer is the decisive cross-Stage
route owner. It may select any Stage declared by the manifest; OPL validates only
the Attempt role and target identity and does not reinterpret the editorial
diagnosis.

## Professional Dependencies And Boundaries

This review depends on actual materialized manuscript refs. Route reader promise, argument arc, or chapter-role defects to `storyline-architecture`; production-plan, task-card, context, or extent defects to `chapter-production-planning`; manuscript, claim, evidence, or local prose defects to `chapter-materialization`. Choose the earliest Stage that can close the root cause and do not edit manuscript artifacts inside this Meta Review Stage. The target Stage creates a new generation, completes its independent Stage Review, and then re-enters Meta Review.

Major repairs require review of the changed bytes before an integrity handoff can be reused. A consumable manuscript may advance with explicit non-central quality debt, but publication/export/readiness claims remain closed while central evidence or systemic integrity gaps remain.

A materialized no-output diagnostic with its own exact ref and hash is a
consumable diagnostic artifact. Literal zero consumable manuscript/review
artifact is a controller hard stop: return the typed blocker or human-gate
evidence and neither `route_impact.stage_route_decision` nor
`route_impact.stage_route_recommendation`.

Do not rewrite source evidence, invent owner authorization, generate proof/export artifacts, or sign owner acceptance.

## Closeout

Return the integrity review, defect-owner matrix, claim/evidence and style findings, accepted quality debt, route evidence, invalidated downstream refs, freshness obligations, and an integrity handoff for proof/export work when eligible. Return the terminal selection as `route_impact.stage_route_decision`, with non-empty `evidence_refs` and a declared `target_stage_id` except for `complete`. If no review result is produced, return a no-output diagnostic and select the next declared owner Stage when work can continue; reserve typed blocker or human gate for true hard-stop boundaries.

The route decision is only for a progress-terminal result. A typed blocker or
human gate returns no route output and is terminalized by the controller.
