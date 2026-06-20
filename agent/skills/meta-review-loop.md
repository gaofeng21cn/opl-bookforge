# Meta-Review Loop Skill

Use this skill inside `book-materialization` after a full manuscript draft reaches its declared chapter and asset gates, and before owner handoff, publication proof, or final export claims.

Working policy:

- Treat meta-review as an independent editorial quality loop, not as ordinary chapter QC. The reviewer should approach the assembled book as a new reader/editor and judge the whole manuscript, not only the changed chapter.
- The meta-reviewer must be context-isolated from the drafting run as much as the execution environment allows. Prefer a separate Codex executor, subagent, model call, or explicit fresh-review prompt that receives only the manuscript and necessary contract refs, not the drafting conversation, repair rationale, or author self-evaluation.
- A valid meta-review reads the assembled manuscript plus only the minimum quality contracts needed to judge it: reader-style contract, chapter function contract, core model map, case evidence ladder, source/evidence boundaries, and current metrics. It should not read hidden drafting notes unless those are the object of review.
- The reviewer must produce a durable `meta-review/round-N.md` or equivalent ref with:
  - round number and date;
  - reviewed manuscript ref and metrics ref;
  - reviewer context boundary;
  - verdict: `pass`, `revise_minor`, or `revise_major`;
  - findings ranked by severity;
  - each finding's location, reader impact, and concrete repair suggestion;
  - each finding's likely repair layer when visible: artifact target, storyline, outline sequence, chapter function, evidence/model, publication design, local prose, or owner/source blocker;
  - a distinction between required repairs, optional preferences, and owner/source-material blockers;
  - explicit evidence-boundary notes for cases that cannot be repaired without owner materials.
- BookForge must run the revision-entrypoint-router skill before converting required findings into prose edits. The router produces `meta-review/round-N-entrypoint-decision.md`, `revision-routing/decision-N.md`, or an equivalent ref that selects the topmost repair level and names route-back, owner/source blocker, and downstream freshness obligations.
- BookForge must convert routed required meta-review findings into a `meta-review/round-N-repair-plan.md` or equivalent. Each accepted finding should map to the selected entrypoint first, then to manuscript chapter refs and, when reusable, to storyline map, chapter thesis chain, chapter task cards, style engine, concept map, core model map, case evidence ladder, publication design profile, or quality gate refs.
- After repairs, regenerate the assembly, metrics, hygiene report, and cumulative owner-review PDF before the next meta-review round. Stale PDFs or metrics cannot support a round verdict.
- Run at most three meta-review rounds by default. A round counts only when an independent review report exists against a fresh assembled manuscript.
- Stop early when the independent reviewer returns `pass`, or when remaining issues are only optional preferences, owner evidence gaps, publication-proof/final-export acceptance, or source-material blockers that cannot be solved by prose editing.
- If the third round still returns required manuscript repairs, stop and return a typed `meta_review_iteration_limit_reached` blocker with unresolved findings and owner decision options. Do not keep revising indefinitely.
- Do not let the drafting executor mark its own manuscript as passing meta-review. The drafting executor may summarize, repair, and verify, but the pass/revise verdict must come from the independent review ref or owner receipt.
- Do not hide disagreements. If BookForge rejects a meta-review suggestion, record why: conflicts with reader-style contract, unsupported by sources, weakens primary-reader density, repeats already accepted material, requires owner evidence, or is an optional taste preference.
- Do not use meta-review as a local polishing lane when the report exposes a higher-order defect. A finding that changes reader promise, argument arc, chapter order, chapter function, evidence/model burden, artifact target, or publication design must be routed to that level before sentence repair.

Review rubric:

- Core claim clarity: the reader can state the book's thesis and scope after the preface/opening.
- Whole-book logic: chapters advance in a natural order and each chapter adds a new movement.
- Concept handling: recurring terms are oriented early, defined clearly, reused consistently, and not overloaded.
- Evidence and cases: constructed scenes, documented process cases, practice-involved cases, and outcome claims stay within their evidence level.
- Red Bird or other practice-involved cases: author-team voice sounds like responsible design/reflection, not detached public-source observation or unsupported self-praise.
- Modelization: whole-book models are named, interpreted, applied, and recovered rather than appearing as isolated figures.
- Prose quality: expression is fluent, affirmative, concrete, reader-facing, and free of visible production scaffolding or obvious AI-flavor patterns.
- Publication handoff boundary: review PDF, publication proof, final export, owner acceptance, and source evidence blockers remain distinct.

Required fail-closed conditions:

- Full draft handoff occurs without a durable independent meta-review report unless the owner explicitly waives meta-review.
- The meta-reviewer receives the drafting conversation, self-justification, or repair notes as primary context and then presents the result as independent.
- Required meta-review findings are summarized in chat but not mapped to a repair plan, manuscript edits, durable style/QC refs, or typed blockers.
- Required meta-review findings lead directly to manuscript edits without a durable revision entrypoint decision.
- A `revise_major` verdict is handled as local prose repair without a route-back or blocker analysis.
- Repairs are made but assembly metrics, hygiene scans, and owner-review PDF are not refreshed before the next review or handoff.
- BookForge performs more than three review-repair rounds without returning a typed blocker or owner decision request.
- A `pass` is claimed while the latest review verdict is `revise_minor` or `revise_major` and the required findings remain unresolved.

This skill improves draft quality and iteration discipline. It does not replace owner review, source-material completion, publication proof inspection, or final export acceptance.
