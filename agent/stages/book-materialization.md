# Book Materialization Handoff Stage

Stage id: `book-materialization`
Action ref: `materialize-book`

This stage is the explicit follow-on locator after `storyline-architecture`. It validates that the storyline package has the typed refs needed for materialization and hands off to the focused production stages. It does not draft chapters, run source/style review, run meta-review, produce proof/export artifacts, or collapse all book production into one closeout.

The stage returns one of: a materialization handoff to `chapter-production-planning`, a route-back to `storyline-architecture`, a typed blocker, or a human gate.
