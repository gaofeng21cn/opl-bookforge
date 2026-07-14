# Publication Proof Handoff Prompt

## Goal

Materialize and classify the requested review, publication-proof, or final-export handoff from current integrity-reviewed manuscript and asset refs.

## A Good Result

- preserves the distinction between `review_pdf`, `publication_proof`, and `final_export`;
- reuses current design, typesetting, asset, and rendered-page refs where their bound bytes and scope remain valid;
- uses a real publication backend for proof claims and verifies figures, tables, captions, hierarchy, pagination, overflow, and visual rhythm on rendered output;
- marks every produced or repaired PDF/export as `review_pending` until a controller-materialized Review receipt binds a fresh reviewer or re-reviewer Attempt to its exact current hash;
- treats any regeneration after Review as invalidating the prior Review receipt and re-reviews the changed bytes;
- names the exact evidence and owner acceptance still required for any stronger claim.

Use `bookforge-publication-memory-curator` for proof, design, memory, asset, and rendered-page method. Use source/reference review only when the proof exposes a new claim-integrity issue.

## Professional Dependencies And Boundaries

Proof/export work depends on a current integrity handoff and actual manuscript/assets. A review PDF may be produced without publication-proof status. Publication proof requires design/backend/rendered-page evidence. Final export requires current publication proof plus owner/export acceptance.

Do not infer publication approval from provider completion, StageRun completion, generated interface readiness, successful compilation, or machine-only nonblank checks. Do not hand-roll normal book layout when an appropriate publication system is available.

## Independent Stage Review Boundary

Refinement in the current Codex thread is `in_thread_refinement` only. Producer and repairer Attempts may return only candidate artifact refs/hashes with `review_pending`; they cannot close publication-proof, final-export, export-ready, or ready claims and, when no hard boundary applies, may return at most `route_impact.stage_route_recommendation`. Formal review, repair, and re-review run as separate StageAttempts with fresh threads and receive only the exact artifact, source, quality-rubric, and necessary lineage refs. The initial reviewer returns `route_impact.stage_quality_cycle.outcome`, never a standalone receipt `verdict`; same-named `outcome` and receipt `verdict` values remain separate fields with separate owners. For unchanged producer bytes, the OPL StageRun controller may close Review only from that isolated Attempt's terminal outcome, route decision, exact hashes, and rubric. After any repair or regeneration, only a fresh re-reviewer outcome bound to the repaired hashes can close Review. For `same_stage_repair_required`, while repair budget remains, a `repair_required` reviewer or re-reviewer continues the quality loop when the narrowest repair owner is `publication-proof-handoff`. For `cross_stage_route_back_before_budget_exhaustion`, if the narrowest owner is a different declared Stage, it may instead end this StageRun with outcome `repair_required` plus exactly one `route_impact.stage_route_decision` whose `decision_kind=route_back`, whose `target_stage_id` differs from the current Stage, and whose non-empty `evidence_refs` bind the finding and owner diagnosis. This is the only terminal route allowed for `repair_required` before budget exhaustion. At final budget with consumable exact bytes, it keeps outcome `repair_required`, returns the terminal `route_impact.stage_route_decision`, and lets the controller project `completed_with_quality_debt`; neither branch clears publication-proof, final-export, export-ready, or ready claims. The decisive reviewer or re-reviewer is `semantic_route_decision_owner=decisive_codex_attempt`; `stage_transition_materialization_owner=opl_stage_run_controller` validates its role and declared target, then materializes the transition and Review receipt without replacing Book Forge owner/export acceptance. A hard-boundary or literal-zero-artifact Attempt returns no route output. A same-thread resume can only complete the closeout protocol and cannot create a Review receipt.

## Closeout

Return artifact-role classification, candidate export/backend receipt, review-PDF or publication-proof refs, rendered-page QA, exact artifact hashes, Review freshness and route evidence, and the owner/export handoff. A publication-proof, final-export, export-ready, or ready claim requires a fresh reviewer or re-reviewer closeout over those exact bytes; downstream owner/export acceptance remains a separate required authority. A progress-terminal reviewer or re-reviewer may advance, repeat, reverse, route back to any declared Stage, or complete, but must use the single route-decision shape and cite non-empty evidence refs. Missing proof evidence becomes quality debt and a diagnostic that closes the stronger claim without blocking stage transition only when a readable exact-hash review artifact remains. Literal zero consumable artifact, or output too corrupt or unreadable to provide any consumable exact artifact, returns `blocked` and no route output. Return a typed blocker or human gate only for a true authority, safety, permission, identity/currentness, irreversible-action, executor-unavailable, explicit-decision, or literal-zero-consumable-artifact boundary.
