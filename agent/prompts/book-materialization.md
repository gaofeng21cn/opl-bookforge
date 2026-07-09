# Book Materialization Handoff Prompt

Goal: accept an approved `storyline-architecture` closeout and route the work into the right-sized materialization stages. This prompt no longer drafts chapters, reviews source/style integrity, runs meta-review, or claims publication proof in one closeout.

Primary open judgment: whether the storyline package has enough typed refs to enter chapter production planning, or must route back to storyline/owner/source blockers.

Professional skill boundary: keep this stage as the route and handoff contract. Route method work to repo-local professional skills only in the later focused stages:

- chapter planning and authoring -> `bookforge-chapter-author`
- source/reference review -> `bookforge-source-reference-reviewer`
- meta-review and revision routing -> `bookforge-meta-reviewer`
- proof/export handoff and memory curation -> `bookforge-publication-memory-curator`

Produce these refs:

- `materialization-handoff-ref:book-materialization` naming the consumed storyline map, chapter thesis chain, reader-style contract, author/source stance map, target extent refs, source refs, and owner decisions.
- `materialization-stage-sequence-ref:book-materialization` with the next stages: `chapter-production-planning`, `chapter-materialization`, `source-style-integrity-review`, and `publication-proof-handoff`.
- `materialization-entry-gate-ref:book-materialization` stating whether chapter production planning may start.
- `route-back-ref:book-materialization` when storyline, reader-style, target extent, source corpus, publication target, or owner decision refs are missing.
- `typed-blocker-ref:book-materialization` when the missing input has a known owner/source and cannot be inferred safely.

Do not produce manuscript body, chapter drafts, claim ledgers, style verdicts, meta-review verdicts, review PDFs, publication proofs, final exports, owner receipts, typed blockers by hand, runtime queues, attempt ledgers, schedulers, or publication/export authority. Those belong to later Book Forge stages or owner-gated surfaces.

Close with an explicit next-stage handoff to `chapter-production-planning`, route back to `storyline-architecture`, or a typed blocker/human gate.
