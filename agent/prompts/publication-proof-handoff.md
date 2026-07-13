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

Refinement in the current Codex thread is `in_thread_refinement` only. Producer and repairer Attempts may return only candidate artifact refs/hashes with `review_pending`; they cannot close publication-proof, final-export, export-ready, or ready claims and may return only `route_impact.stage_route_recommendation`. Formal review, repair, and re-review run as separate StageAttempts with fresh threads and receive only the exact artifact, source, quality-rubric, and necessary lineage refs. The initial reviewer returns `route_impact.stage_quality_cycle.outcome`, never a standalone receipt `verdict`; for unchanged producer bytes, the OPL StageRun controller may close Review only from that isolated Attempt's terminal outcome, route decision, exact hashes, and rubric. After any repair or regeneration, only a fresh re-reviewer outcome bound to the repaired hashes can close Review. A `repair_required` reviewer continues the quality loop and may only recommend a route. The terminal reviewer or re-reviewer returns `route_impact.stage_route_decision`; OPL validates its role and declared target, then materializes the Review receipt without replacing Book Forge owner/export acceptance. A same-thread resume can only complete the closeout protocol and cannot create a Review receipt.

## Closeout

Return artifact-role classification, candidate export/backend receipt, review-PDF or publication-proof refs, rendered-page QA, exact artifact hashes, Review freshness and route evidence, and the owner/export handoff. A publication-proof, final-export, export-ready, or ready claim requires a fresh reviewer or re-reviewer closeout over those exact bytes; downstream owner/export acceptance remains a separate required authority. The terminal reviewer or re-reviewer may advance, repeat, reverse, route back to any declared Stage, or complete, but must use the single route-decision shape and cite non-empty evidence refs. Missing proof evidence or unreadable output becomes quality debt and a diagnostic that closes the stronger claim without blocking stage transition. Return a typed blocker or human gate only for a true authority, safety, permission, identity/currentness, irreversible-action, executor-unavailable, or explicit-decision boundary.
