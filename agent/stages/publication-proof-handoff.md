# Publication Proof Handoff Stage

Stage id: `publication-proof-handoff`
Action ref: `materialize-book`

This stage generates or transforms review PDF, publication-proof, or final-export bytes after integrity review. Every producer or repairer output remains a `review_pending` candidate. Any regeneration invalidates the prior Review receipt; a fresh reviewer or re-reviewer must bind the exact current hashes before publication-proof, final-export, export-ready, or ready claims can close.

The stage returns reviewed candidate refs, owner handoff refs, route evidence, typed blockers, or human gates. Producer and repairer Attempts may only recommend a route. A decisive reviewer or re-reviewer chooses the next declared Stage after inspecting the exact current hashes. With repair budget remaining it continues local repair when this Stage is the narrowest owner, but may decisively route `repair_required` to a different declared owning Stage instead of spending a local round. OPL materializes the Review receipt from that isolated Attempt. A fresh Review closeout is necessary but does not replace downstream owner/export acceptance; Book Forge retains final quality, export, publication, and owner authority.
