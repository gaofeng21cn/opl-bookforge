# Publication Proof Handoff Quality Gate

Pass conditions:

- The handoff classifies the artifact as `review_pdf`, `publication_proof`, or `final_export`, and records what each role can and cannot prove.
- Review PDF output is labeled as owner/editor review artifact only.
- Publication proof evidence includes publication design profile, concrete design tokens, template/component inventory, resource-path-backed figure resolution, Markdown image-ref checks, figure asset manifest readiness, rendered-page refs, rendered-page inspection, and pre-ship proof review.
- Every producer or repairer marks semantically changed review dimensions and their declared dependents as `review_pending`; it cannot itself close publication-proof, final-export, export-ready, or ready claims.
- A controller-materialized Review receipt binds a reviewer or re-reviewer Attempt to declared artifact nodes, transitive dependencies, rubric, and scope. Hashes are locators or stale hints only. Regeneration without semantic change does not invalidate the receipt.
- Content changes fail closed across content, editorial, reference, display, layout, export, and package. Layout-only changes invalidate layout, export, and package; export-only changes invalidate export and package. Neither invalidates content, editorial, or reference review.
- A reviewed final-export candidate may be handed downstream pending acceptance. A final-export accepted/export-ready/ready claim requires every declared review scope to be current, publication-proof evidence, separate downstream owner/export acceptance receipt refs, and any separately required release-integrity receipt.
- When no hard boundary applies, producer and repairer Attempts may return at most `stage_route_recommendation`; only a decisive reviewer or re-reviewer may return `stage_route_decision`. For `same_stage_repair_required`, while repair budget remains, a `repair_required` reviewer continues repair plus fresh re-review when `publication-proof-handoff` is the narrowest repair owner. For `cross_stage_route_back_before_budget_exhaustion`, if the narrowest owner is a different declared Stage, reviewer or re-reviewer may instead return the only permitted pre-exhaustion terminal route: outcome `repair_required` plus exactly one `stage_route_decision` with `decision_kind=route_back`, a target different from the current Stage, and non-empty finding/owner evidence. At final budget with consumable exact bytes it keeps outcome `repair_required`, returns the terminal decision, and the controller projects `completed_with_quality_debt` without clearing any stronger claim.
- Missing proof backend, design profile, asset paths, rendered-page inspection, or owner/export acceptance returns `generated_with_quality_debt`, a human gate, or route-back instead of a ready claim when a readable review artifact exists. It does not block the stage transition; it does block publication-proof/final-export/readiness claims.
- Literal zero consumable artifact, or bytes too corrupt or unreadable to bind an exact review artifact, returns `blocked` with no route output. A materialized exact-ref-and-hash diagnostic is consumable; an absent diagnostic is still literal zero.

Forbidden cross-stage blocking behavior:

- A review PDF, HTML preview, unstyled backend output, hand-rolled raster renderer, command success, or provider completion is used as publication-proof or final-export evidence.
- A producer or repairer candidate, stale affected-scope Review receipt, or receipt whose declared dependency closure no longer matches current semantics is used to close publication-proof, final-export, export-ready, or ready status.
- A hash-only or whole-package regeneration event blanket-invalidates unrelated content, editorial, or reference receipts.
- A content, claim, or limitation change reuses prior content/editorial/reference review or downstream proof review without a fresh affected-scope closeout.
- Missing publication-proof evidence is not used to block unrelated chapter drafting, source integrity, style review, or ordinary review-PDF refresh; it blocks only publication-proof, final-export, owner-accepted, or ready claims.
- The stage claims publication approval, final export acceptance, book quality acceptance, owner acceptance, domain readiness, production readiness, or runtime readiness without the required owner/domain authority refs.
