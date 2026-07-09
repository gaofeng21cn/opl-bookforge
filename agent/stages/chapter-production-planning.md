# Chapter Production Planning Stage

Stage id: `chapter-production-planning`
Action ref: `materialize-book`

This stage turns the storyline handoff into owner-inspectable chapter packages, budgets, task cards, memory refs, and an active production queue. It owns the production-planning judgment before prose creation.

The stage should hand off to `chapter-materialization` only when the next chapter action, target extent, reader-style contract, source boundary, and task-card refs are explicit. Otherwise it routes back or returns a typed blocker for the missing owner/source.
