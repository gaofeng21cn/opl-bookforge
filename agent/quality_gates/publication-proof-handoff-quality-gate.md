# Publication Proof Handoff Quality Gate

Pass conditions:

- The handoff classifies the artifact as `review_pdf`, `publication_proof`, or `final_export`, and records what each role can and cannot prove.
- Review PDF output is labeled as owner/editor review artifact only.
- Publication proof evidence includes publication design profile, concrete design tokens, template/component inventory, resource-path-backed figure resolution, Markdown image-ref checks, figure asset manifest readiness, rendered-page refs, rendered-page inspection, and pre-ship proof review.
- Final export handoff requires publication-proof evidence plus owner/export acceptance receipt refs.
- Missing proof backend, design profile, asset paths, rendered-page inspection, or owner/export acceptance returns `generated_with_quality_debt`, a human gate, or route-back instead of a ready claim when a readable review artifact exists. It does not block the stage transition; it does block publication-proof/final-export/readiness claims.

Fail-closed conditions:

- A review PDF, HTML preview, unstyled backend output, hand-rolled raster renderer, command success, or provider completion is used as publication-proof or final-export evidence.
- Missing publication-proof evidence is used to block unrelated chapter drafting, source integrity, style review, or ordinary review-PDF refresh instead of only blocking publication-proof or final-export claims.
- The stage claims publication approval, final export acceptance, book quality acceptance, owner acceptance, domain readiness, production readiness, or runtime readiness without the required owner/domain authority refs.
