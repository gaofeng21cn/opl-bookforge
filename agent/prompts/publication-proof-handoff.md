# Publication Proof Handoff Prompt

## Goal

Materialize and classify the requested review, publication-proof, or final-export handoff from current integrity-reviewed manuscript and asset refs.

## A Good Result

- preserves the distinction between `review_pdf`, `publication_proof`, and `final_export`;
- reuses current design, typesetting, asset, and rendered-page refs where their bound bytes and scope remain valid;
- uses a real publication backend for proof claims and verifies figures, tables, captions, hierarchy, pagination, overflow, and visual rhythm on rendered output;
- regenerates and re-reviews affected artifacts after material manuscript, asset, design, or backend changes;
- names the exact evidence and owner acceptance still required for any stronger claim.

Use `bookforge-publication-memory-curator` for proof, design, memory, asset, and rendered-page method. Use source/reference review only when the proof exposes a new claim-integrity issue.

## Professional Dependencies And Boundaries

Proof/export work depends on a current integrity handoff and actual manuscript/assets. A review PDF may be produced without publication-proof status. Publication proof requires design/backend/rendered-page evidence. Final export requires current publication proof plus owner/export acceptance.

Do not infer publication approval from provider completion, StageRun completion, generated interface readiness, successful compilation, or machine-only nonblank checks. Do not hand-roll normal book layout when an appropriate publication system is available.

## Closeout

Return artifact-role classification, export/backend receipt, review-PDF or publication-proof refs, rendered-page QA, freshness and route-back refs, and the owner/export handoff. Missing proof evidence or unreadable output becomes quality debt and a diagnostic that closes the stronger claim without blocking stage transition. Return a typed blocker or human gate only for a true authority, safety, permission, identity/currentness, irreversible-action, executor-unavailable, or explicit-decision boundary.
