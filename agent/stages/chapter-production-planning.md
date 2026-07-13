# Chapter Production Planning Stage

Stage id: `chapter-production-planning`
Action ref: `materialize-book`

This is the direct entry stage for `materialize-book`. It consumes the approved `storyline-architecture` closeout, performs storyline-ref admission, and turns admitted refs into owner-inspectable chapter packages, budgets, task cards, memory refs, and an active production queue.

The stage aims to hand a complete next chapter action, target extent, reader-style contract, source boundary, and task-card refs to `chapter-materialization`. Ordinary gaps remain quality debt with a next forced delta or route back to `storyline-architecture`; they do not stop Codex from launching `chapter-materialization` or any other declared stage. Zero, corrupt, or unreadable output becomes a no-output/failure diagnostic and also advances. Typed blockers and human gates are reserved for unavailable executors, authority, safety/permission, wrong-target identity/currentness, irreversible action, or explicit human decisions.
