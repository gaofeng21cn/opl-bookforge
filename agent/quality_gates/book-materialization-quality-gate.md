# Book Materialization Handoff Quality Gate

Quality gate declaration is required for every generated OPL-compatible stage.

Pass conditions:

- The consumed storyline refs include storyline map, chapter thesis chain, reader-style contract, author/source stance map, source/evidence refs, and target extent or an explicit owner/source gap.
- The stage emits a materialization handoff that names the focused next stages rather than trying to close planning, drafting, source/style review, meta-review, review PDF, publication proof, and final export in one packet.
- The handoff preserves OPL and Book Forge authority boundaries: no runtime/controller, queue, scheduler, attempt ledger, owner receipt body, typed blocker body, manuscript body, publication verdict, final export verdict, or owner acceptance is created here.
- Missing storyline, reader-style, source, target extent, or owner-decision inputs route back to `storyline-architecture`, a typed blocker, or a human gate with the exact missing owner/source.

Fail-closed conditions:

- The stage drafts or edits manuscript body.
- The stage claims chapter readiness, source/style integrity, meta-review pass, review-PDF readiness, publication-proof readiness, final-export readiness, book quality acceptance, or owner acceptance.
- The stage hides missing storyline/source/owner inputs and starts chapter planning as if the handoff were complete.
