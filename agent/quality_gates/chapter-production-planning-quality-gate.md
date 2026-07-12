# Chapter Production Planning Quality Gate

Quality gate declaration is required for every generated OPL-compatible stage. This gate is the planning stage's domain self-check; an independent review receipt is not required for the ordinary transition to `chapter-materialization`.

Pass conditions:

- The consumed storyline refs include the storyline map, chapter thesis chain, reader-style contract, author/source stance map, source/evidence refs, target extent, and owner decisions, or the stage records an exact in-progress delta or route-back repair ref.
- Target extent is converted into chapter-level budgets before body drafting starts.
- The active production queue names each required unit's target minimum, current measured state, missing extent, next action, review-PDF eligibility, and typed blocker state.
- Every planned production chapter has a chapter task card with reader promise, chapter job, thesis movement, source refs, figure/table obligations, active memory refs, style constraints, QC state, and blockers.
- Planning consumes the reader-style contract, author/source stance map, chapter function contract, early concept map, core model map, and case evidence ladder from `storyline-architecture` when relevant.
- The chapter context compiler plan separates protected context from compressible context and names the first concrete chapter action.
- Book memory refs are owner-inspectable working, episodic, and semantic refs, not a private scheduler or second truth source.
- Ordinary missing detail stays `in_progress` with a next forced delta or routes back to `storyline-architecture`; it does not become a generic typed blocker or hard stop.
- Quality acceptance for the planning artifact requires an explicit storyline, next chapter action, target extent, source boundary, style constraints, and task-card refs. Missing items become quality debt; Codex may still start `chapter-materialization` or any other declared stage.

Quality-debt and claim-closed conditions:

- The stage hides missing storyline/source/owner refs and starts chapter drafting as if admission had passed.
- Visible chapter prose is drafted before task cards, target extent, reader-style, source boundary, and next action are explicit.
- A below-target coverage skeleton is labeled as completed materialization.
- Planning creates or depends on a private queue, scheduler, session store, attempt ledger, runtime state, owner receipt, typed blocker body, or publication authority.
- An independent review is made a blanket prerequisite for ordinary planning-to-materialization transition.

None of these conditions lets a validator stop another declared stage when a readable plan or diagnostic exists.
