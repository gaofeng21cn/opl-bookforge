# Chapter Production Planning Prompt

Goal: accept the approved storyline closeout, decide whether its typed refs are sufficient to begin chapter production, and convert the admitted refs into a production plan before visible prose is drafted.

Primary open judgment: whether and how the approved storyline can enter chapter production, including what units can be produced next, at what extent, and with which source, style, memory, and owner constraints.

Use the professional method layer when needed:

- `bookforge-chapter-author` for chapter task cards, chapter context shape, reader-entry plans, and production queue design.
- `bookforge-story-style-architect` for reader-style, chapter-function, concept-map, core-model, or author/source-stance gaps that must route back.

Produce these refs:

- storyline admission ref naming the consumed storyline map, chapter thesis chain, reader-style contract, author/source stance map, target extent, source/evidence refs, and owner decisions.
- target extent contract with page/word/character/chapter/figure/table targets inherited from owner/source/storyline refs.
- chapter production budget with each required unit's minimum extent, current state, missing extent, and next production action.
- active production queue distinguishing `not_started`, `outline_only`, `seed_in_progress`, `draft_in_progress`, `chapter_draft_ready`, and `blocked`.
- chapter task card bundle naming reader promise, chapter job, thesis movement, source refs, target extent, figure/table obligations, memory refs, style constraints, QC state, and blockers.
- chapter context compiler plan naming protected context, compressible context, evidence boundaries, and one next chapter action.
- book-memory contract for working, episodic, and semantic refs.
- planning progress ref with the current state, ordinary missing deltas, and next forced delta.
- planning handoff to `chapter-materialization`, or a route-back ref to `storyline-architecture` when the storyline, reader-style, source, target extent, publication target, or owner-decision refs need repair.

Ordinary incompleteness stays inside this stage as `in_progress` with a next forced delta, or routes back with exact repair refs. Do not convert a normal planning gap into a hard error or typed blocker. Reserve typed blockers and human gates for missing protected source/owner authority, unsafe inference, or another condition that the stage cannot legally repair or route back.

An independent review receipt is not required for the ordinary transition to `chapter-materialization`. The planning quality gate is a domain self-check over direct refs; create a separate review only when an explicit high-risk owner, truth, or authority decision requires one.

Do not draft manuscript body, claim chapter readiness, run source/style integrity verdicts, run meta-review, generate PDFs, or authorize publication/final export.
