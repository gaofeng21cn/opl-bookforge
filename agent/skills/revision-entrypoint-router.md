# Revision Entrypoint Router Skill

Use this skill inside `book-materialization` after independent meta-review, serious owner/reviewer critique, complete-version comparison, or any finding that may require more than local prose edits.

Purpose:

- Decide where revision must begin before editing starts.
- Keep higher-order book defects from being hidden by sentence-level polishing.
- Route structural findings back to the correct Book Forge domain refs while keeping OPL as a refs-only transport layer.

External practice basis:

- Writing-center revision practice separates higher-order concerns such as thesis, audience, purpose, organization, and development from lower-order sentence concerns. Book Forge maps this to book-level storyline, reader promise, chapter sequence, evidence/model development, and local prose.
- Developmental or structural editing treats content, organization, genre, and manuscript structure as distinct from copyediting. Book Forge therefore allows route-back to storyline or outline refs before paragraph repair.
- Reverse outlining turns a completed draft back into a structure map so reviewers can see what the manuscript is actually doing. Book Forge uses reverse-outline evidence before deciding whether the draft follows the approved chapter thesis chain.
- Architecture evaluation practice classifies scenarios, risks, tradeoffs, sensitivity points, and risk themes before changing architecture. Book Forge uses the same discipline for manuscript repair: classify the risk layer first, then choose the smallest truthful repair route.
- Hierarchical architecture views keep system, container, component, and code concerns separate. Book Forge uses an analogous zoom ladder for artifact target, storyline, outline, chapter function, evidence/model, publication design, and local prose.

Required inputs:

- Latest independent meta-review report, owner critique, or complete-version comparison ref.
- Current assembled manuscript ref and metrics/hygiene refs.
- Current storyline map, reader-style contract, chapter thesis chain, chapter function contracts, concept map, core model map, case evidence ladder, publication design profile, and artifact target decision when available.
- Reverse outline or equivalent structure extraction of the assembled manuscript. At minimum it should list each front-matter/chapter/major-section unit, its actual job, repeated claims, missing handoffs, evidence/model use, and relation to the approved chapter chain.
- Source/owner blockers that cannot be solved by manuscript editing.

Durable output:

Produce `revision-routing/decision-N.md`, `meta-review/round-N-entrypoint-decision.md`, or an equivalent owner-inspectable ref with:

- trigger, date, reviewed refs, and reviewer/router context boundary;
- one-line revision objective;
- reverse-outline summary and key structure deltas from the approved storyline;
- finding-to-level table with severity, affected refs, reader impact, evidence/source boundary, and reusable repair refs;
- selected topmost repair entrypoint;
- allowed lower-level repairs that may proceed in the same pass;
- forbidden lower-level edits that would mask unresolved higher-level defects;
- route-back refs, owner/source blockers, and next owner decision when needed;
- downstream freshness obligations after repair.

Repair entrypoint levels:

1. `artifact_target_repair`
   - Use when the manuscript target is wrong or ambiguous, for example concise review edition versus formal publication manuscript.
   - Update target artifact choice, owner handoff, publication design expectations, and downstream readiness language before manuscript repair.

2. `storyline_architecture_repair`
   - Use when the reader promise, primary audience, central thesis, argument arc, source map, author/source stance, or evidence burden is wrong.
   - Route back to `storyline-architecture` refs before chapter rewriting. Materialization may only preserve evidence, prepare diagnostics, or make owner-approved emergency local fixes.

3. `outline_sequence_repair`
   - Use when chapter order, chapter split/merge, part structure, front matter, conclusion path, or major handoff sequence prevents the book from working.
   - Update chapter thesis chain, chapter function contracts, reader-entry plans, production queue, and review-PDF continuity before rewriting affected chapters.

4. `chapter_function_repair`
   - Use when one or more chapters repeat adjacent jobs, lack a primary movement, carry too many jobs, or fail their handoff.
   - Update chapter task cards, chapter function contracts, local concept/model/case obligations, and then repair the chapter Markdown.

5. `evidence_model_repair`
   - Use when claims, cases, concepts, or core models are underdeveloped or overclaimed but the storyline and chapter order are still sound.
   - Update source-claim integrity refs, case evidence ladder, concept map, model map, figure/table plans, and typed evidence gaps before strengthening prose.

6. `publication_design_repair`
   - Use when the content route is acceptable but PDF/proof/TOC/front-matter/figure-style decisions block the target artifact.
   - Update publication design profile, figure stance, proof checklist, export receipt expectations, and rendered-page inspection plan before proof claims.

7. `local_prose_repair`
   - Use only when thesis, reader target, outline, chapter functions, evidence/model route, and artifact target are stable.
   - Eligible fixes include sentence rhythm, transitions, local repetition, terminology clarity, paragraph movement, and AI-flavor/internal-language residue.

8. `owner_source_blocker_only`
   - Use when no honest repair can close the finding without owner decision, missing source material, authorization, outcome evidence, or publication acceptance.
   - Return typed blockers and owner decision options instead of polishing around the gap.

Routing rules:

- Pick the topmost level that materially affects reader understanding, artifact target, evidence truth, or owner acceptance. Lower-level repairs may be batched only if they do not depend on unresolved higher-level decisions.
- A `revise_major` meta-review verdict must produce a revision entrypoint decision before any manuscript repair. A `revise_minor` verdict may still require routing if findings touch chapter function, evidence/model, or publication design.
- Fast-track revision is allowed only after this router classifies the suggestion as `local_prose_repair` or another explicitly bounded low-risk repair with named touched refs.
- If the selected level is `storyline_architecture_repair`, emit a route-back ref to `storyline-architecture` and update or request owner review of storyline refs before claiming manuscript repair.
- If the selected level is `artifact_target_repair`, do not continue local polish while calling the formal-publication critique absorbed. Record the target artifact route first.
- If evidence is missing, do not rewrite as if evidence exists. Emit `owner_source_blocker_only` or an evidence-scoped route with typed gaps.
- After any accepted repair, refresh the affected source refs first, then assembly, metrics, hygiene scans, review PDF, and handoff refs in freshness order.

OPL boundary:

- OPL may transport and display the router output as opaque `revision-entrypoint-decision-ref`, `route-back-ref`, `repair-plan-ref`, `typed-blocker-ref`, and `owner-decision-ref`.
- OPL must not decide the repair level, rewrite manuscript body, update book memory body, authorize quality/export, or sign owner receipts.
- A future OPL generic review-repair transport should support route-back refs, current-owner projection, iteration caps, and freshness gates without reading or owning Book Forge manuscript semantics.

Fail-closed conditions:

- Required meta-review or owner critique findings are edited directly without a durable revision entrypoint decision.
- A higher-order defect is classified as local prose because local editing is cheaper.
- A route-back decision changes storyline, outline, reader, evidence, artifact target, or publication design without updating the corresponding durable refs.
- A fast-track audit is used while unresolved storyline, outline, chapter-function, evidence/model, or artifact-target defects remain.
- A typed owner/source blocker is replaced by smoother prose.
- OPL-generated or hosted surfaces expose router refs as quality approval, publication readiness, or owner acceptance.
