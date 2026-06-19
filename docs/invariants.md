# OPL BookForge Invariants

Owner: `opl-bookforge`
Purpose: `invariants`
State: `active_truth`
Machine boundary: Human-readable hard constraints. Machine truth remains in contracts, agent pack files, OPL validator output, runtime receipts, owner receipts, and typed blockers.

- Do not store runtime artifacts in repo source.
- Do not implement generic OPL runtime primitives in this domain repo.
- Do not let OPL write domain truth, memory body, or quality/export verdicts.
- Do not claim production-ready book writing, publication approval, owner acceptance, or export acceptance from scaffold validation, interface descriptors, OMA evidence, pilot exports, or rendered pages alone.
- Keep `storyline-architecture` and `book-materialization` as the two primary stages unless a future decision records a stronger owner-reviewed stage model.
- Require a reader-style contract during `storyline-architecture` before body drafting or chapter expansion. It must identify target readers, reader priority, reading situation, natural-expression rules, and owner-review status; if BookForge cannot infer these with high confidence, it must ask the owner or emit a typed blocker.
- Preserve reader priority across materialization. Primary readers define the writing target. Secondary readers may only add compatible accessibility constraints unless the owner explicitly promotes them to co-primary readers; they must not silently create separate chapter obligations, explanatory detours, lower-density exposition, difficulty downgrades, or voice targets.
- Keep writing-quality checks focused on style consistency, concrete language, affirmative editorial phrasing, evidence grounding, figure/table completeness, layout, and handoff readiness.
- Make first visible chapter drafts reader-facing by default. Production metadata such as chapter task, core question, thesis, target budgets, source refs, figure asset status, QC notes, blockers, and reader-entry plans must live in briefs, drafting notes, manifests, reports, comments, or handoff refs, not in manuscript prose. If a chapter needs a routine late reader-facing rewrite to stop reading like a memo or instruction manual, the first-draft gate failed and the chapter-production pattern must be corrected before continuing production.
- Keep book prose Markdown-first: per-chapter Markdown refs own manuscript body for book-length work; scripts may assemble, count, validate, export, and report but must not be the source of truth for substantial prose.
- Keep book-length drafting chapter-sharded by default: chapter brief, chapter draft, chapter QC, merged manuscript, whole-book pass. A monolithic creative source file requires explicit owner approval.
- Convert owner/source target extent into chapter budgets and an active production queue before drafting body prose for book-length work.
- Treat chapter target budgets as completion gates. Below-target chapter prose is in progress, not drafted/done, and below-target full-book assemblies are preview artifacts, not final `book.md`.
- Treat all-chapter short coverage as seed material only. It is not completed materialization unless each chapter meets its target gate or remains visibly queued as in-progress work.
- Refresh a completed-contiguous owner-review PDF after chapter text-readiness or full readiness changes; it must include the reviewable reader sequence from the beginning of the book, stop at the first below-target required unit, label text-ready-but-asset-blocked chapters honestly, surface review-continuity blockers instead of silently skipping earlier units, and must not be presented as final export readiness.
- Treat publication PDF generation as a first-class export backend concern owned by BookForge. Project scripts may call the BookForge PDF export helper, but the normal path is Pandoc/XeLaTeX or equivalent Quarto/Typst-style typesetting backends, not ad-hoc raster page drawing.
- Distinguish review PDF, publication proof PDF, and final export. Publication proof requires an explicit publication design profile and rendered-page inspection; final export requires owner acceptance.
- Treat review PDFs, HTML previews, export command success, or uninspected rendered pages as insufficient evidence for publication proof or final export.
- Require a publication design profile and real typesetting backend for publication proof and final export; hand-rolled raster text drawing is not the normal BookForge publication path.
- Require backend resource paths or equivalent asset resolution configuration when Markdown references project-local figures, so generated PDFs cannot silently drop images.
- Require caption, callout, table, figure, cross-reference, header/footer, page-number, overflow, and visual-rhythm inspection before any publication-proof claim.
- Require owner/export acceptance receipts before any final-export claim.
- Retire invalid compact/sample drafts when the owner requires a book-length restart; do not expand an invalid compact draft in place as the active workflow.
- Keep long-form materialization auditable with a pipeline contract that names chapter packages, chapter QC refs, figure asset manifest, table plan, whole-book review, export refs, blockers, and retired drafts.
- Keep book memory owner-inspectable and domain-owned: working memory, episodic memory, and semantic memory must be refs or artifacts inside the book project, not hidden provider state.
- Keep chapter runtime expressed through OPL stage refs, chapter task cards, QC refs, repair reports, memory updates, and owner gates; do not add a domain-private scheduler, queue, attempt ledger, session store, or app shell.
- Keep style engine assets explicit: voice principles, terminology policy, rhythm rules, analogy policy, sample passages, forbidden patterns, accepted repairs, and style drift findings must be reviewable.
- Keep transparent prompt bundles with source slices, memory refs, style constraints, and quality-gate prompts for major drafting/review/repair/proofing passes.
- Preserve owner/source-declared target extent during materialization; compact/sample drafts require explicit owner approval or a typed extent blocker.
- Treat final book-bound artwork as `imagegen`-generated bitmap assets by default; SVG, local-script diagrams, and placeholders are planning aids only unless the owner explicitly requests deterministic vector output.
- Treat chat previews or generated artwork without an exposed, project-local file path as image-asset blockers, not as completed figure evidence.
- Keep final figure materialization on the BookForge native imagegen asset helper or an equivalent BookForge-owned backend adapter. The default route delegates provider credentials and model access to the Codex executor/native imagegen surface, copies the bitmap into the project, and writes a receipt; BookForge must not make direct Base URL/API-key provider calls the default figure route.
- Route missing human acceptance as owner receipt blockers or typed blockers, not as silent success.
- Treat generated MCP/OpenAI/AI SDK surfaces as descriptors until direct runtime execution evidence exists.
