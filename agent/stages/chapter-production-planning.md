# Chapter Production Planning Stage

Stage id: `chapter-production-planning`
Action ref: `materialize-book`

This is the direct entry stage for `materialize-book`. It consumes the approved `storyline-architecture` closeout, performs storyline-ref admission, and turns admitted refs into owner-inspectable chapter packages, budgets, task cards, memory refs, and an active production queue.

The stage hands off to `chapter-materialization` only when the next chapter action, target extent, reader-style contract, source boundary, and task-card refs are explicit. Ordinary gaps remain `in_progress` with a next forced delta or route back to `storyline-architecture`; typed blockers and human gates are reserved for missing authority or inputs that cannot be repaired safely. Independent review is not an ordinary transition prerequisite.
