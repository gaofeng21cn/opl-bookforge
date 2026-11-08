# Publication Proof Handoff Stage

Stage id: `publication-proof-handoff`
Action ref: `materialize-book`

This stage generates or transforms review PDF, publication-proof, or final-export artifacts after integrity review. A producer or repairer marks each semantically changed review dimension and its declared dependents as `review_pending`; unchanged content, editorial, or reference receipts remain reusable across layout- or export-only regeneration. A content change fails closed across content, editorial, reference, display, layout, export, and package scopes.

The stage returns reviewed candidate refs, declared review-scope currentness, owner handoff refs, route evidence, typed blockers, or human gates. Producer and repairer Attempts may only recommend a route. A decisive reviewer or re-reviewer chooses the next declared Stage after inspecting the affected semantic scope and dependency closure. Artifact hashes are locators or stale hints, not content authority. With repair budget remaining the Stage continues local repair when it is the narrowest owner, but may decisively route `repair_required` to a different declared owning Stage instead of spending a local round. OPL materializes the Review receipt from that isolated Attempt. Fresh closeout is required only for stale scopes and does not replace downstream owner/export acceptance or a separate release-integrity contract; Book Forge retains final quality, export, publication, and owner authority.
