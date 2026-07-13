# Publication Proof Handoff Stage

Stage id: `publication-proof-handoff`
Action ref: `materialize-book`

This stage generates or transforms review PDF, publication-proof, or final-export bytes after integrity review. Every producer or repairer output remains a `review_pending` candidate. Any regeneration invalidates the prior Review receipt; a fresh reviewer or re-reviewer must bind the exact current hashes before publication-proof, final-export, export-ready, or ready claims can close.

The stage returns reviewed candidate refs, owner handoff refs, route evidence, typed blockers, or human gates. Producer and repairer Attempts may only recommend a route. A terminal reviewer or re-reviewer chooses the next declared Stage after inspecting the exact current hashes, and OPL materializes the Review receipt from that isolated Attempt. A fresh Review closeout is necessary but does not replace downstream owner/export acceptance; Book Forge retains final quality, export, publication, and owner authority.
