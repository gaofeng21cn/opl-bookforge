# Publication Proof Handoff Quality Gate

Pass conditions:

- The handoff classifies the artifact as `review_pdf`, `publication_proof`, or `final_export`, and records what each role can and cannot prove.
- Review PDF output is labeled as owner/editor review artifact only.
- Publication proof evidence includes publication design profile, concrete design tokens, template/component inventory, resource-path-backed figure resolution, Markdown image-ref checks, figure asset manifest readiness, rendered-page refs, rendered-page inspection, and pre-ship proof review.
- Every producer or repairer output is a `review_pending` candidate; it cannot itself close publication-proof, final-export, export-ready, or ready claims.
- A controller-materialized Review receipt binds the exact current PDF/export hashes to a fresh reviewer Attempt for unchanged producer bytes or a fresh re-reviewer Attempt after repair. Any regeneration invalidates the prior Review receipt.
- A reviewed final-export candidate may be handed downstream pending acceptance. A final-export accepted/export-ready/ready claim requires the fresh exact-byte Review closeout, publication-proof evidence, and separate downstream owner/export acceptance receipt refs.
- When no hard boundary applies, producer and repairer Attempts may return at most `stage_route_recommendation`; only a decisive reviewer or re-reviewer may return `stage_route_decision`. While repair budget remains, a `repair_required` reviewer continues repair plus fresh re-review when `publication-proof-handoff` is the narrowest repair owner. If the narrowest owner is a different declared Stage, reviewer or re-reviewer may instead return the only permitted pre-exhaustion terminal route: outcome `repair_required` plus exactly one `stage_route_decision` with `decision_kind=route_back`, a target different from the current Stage, and non-empty finding/owner evidence. At final budget with consumable exact bytes it keeps outcome `repair_required`, returns the terminal decision, and the controller projects `completed_with_quality_debt` without clearing any stronger claim.
- Missing proof backend, design profile, asset paths, rendered-page inspection, or owner/export acceptance returns `generated_with_quality_debt`, a human gate, or route-back instead of a ready claim when a readable review artifact exists. It does not block the stage transition; it does block publication-proof/final-export/readiness claims.
- Literal zero consumable artifact, or bytes too corrupt or unreadable to bind an exact review artifact, returns `blocked` with no route output. A materialized exact-ref-and-hash diagnostic is consumable; an absent diagnostic is still literal zero.

Forbidden cross-stage blocking behavior:

- A review PDF, HTML preview, unstyled backend output, hand-rolled raster renderer, command success, or provider completion is used as publication-proof or final-export evidence.
- A producer or repairer candidate, stale Review receipt, or receipt bound to different bytes is used to close publication-proof, final-export, export-ready, or ready status.
- Missing publication-proof evidence is not used to block unrelated chapter drafting, source integrity, style review, or ordinary review-PDF refresh; it blocks only publication-proof, final-export, owner-accepted, or ready claims.
- The stage claims publication approval, final export acceptance, book quality acceptance, owner acceptance, domain readiness, production readiness, or runtime readiness without the required owner/domain authority refs.
