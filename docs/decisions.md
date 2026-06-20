# OPL BookForge Decisions

Owner: `opl-bookforge`
Purpose: `decisions`
State: `active_truth`
Machine boundary: Human-readable decision log. Machine truth remains in contracts, agent pack files, OPL validator output, OMA evidence, pilot evidence, runtime receipts, owner receipts, and typed blockers.

- Adopt `OPL BookForge` as the product name and `opl-bookforge` as the repo slug, `domain_id`, and `foundry_agent_id`.
- Follow the OPL series repo naming style used by `opl-meta-agent`, `opl-flow`, `opl-hermes-shell`, `opl-aion-shell`, and `opl-doc`.
- Adopt OPL standard domain-agent scaffold v1 and standard stage pack v2.
- Keep this repo as a declarative domain pack plus minimal authority functions.
- Model the book-writing workflow as two primary stages: `storyline-architecture` and `book-materialization`.
- Keep reader and natural-expression decisions inside `storyline-architecture` as a required reader-style contract, not as an implicit taste note during drafting. Missing or low-confidence audience/style information routes to an owner question or typed blocker.
- Record reader priority in the reader-style contract. Secondary readers are read-along or accessibility constraints by default; BookForge must not write chapters for them as hidden co-primary audiences, lower-density exposition targets, or competing voice targets unless the owner explicitly changes the audience contract.
- Record major-case author/source stance during storyline architecture. If the author team is an executor, designer, participant, evaluator, or advocate in a case, BookForge must not default the initial chapter draft to outside observation of public materials; it should use the owner-approved practice-involved stance while keeping unsupported outcomes as evidence gaps.
- Make reader-facing chapter prose a first-draft target inside `book-materialization`. Production scaffolding and reader-entry plans belong in briefs, manifests, QC reports, drafting notes, and handoff refs; they must not leak into manuscript openings and headings that the owner reads as book text. A routine late reader-facing rewrite is not the normal quality path; memo-like first drafts are drafting-gate failures that require improving the chapter-production pattern.
- Treat structural validation as L4 baseline evidence only; do not use it as book quality, production readiness, publication readiness, or owner acceptance evidence.
- Use OMA Agent Lab takeover, independent AI reviewer evaluation, and external-suite self-evolution as required new-agent baseline evidence. Scaffold/interface readiness alone is not a delivered-agent claim.
- Treat the 2026-06-18 real short-book pilot as evidence for two-stage workflow execution, manuscript/export generation, quality checks, and owner-gate blocker handling. It does not authorize a production-ready claim.
- Supersede the pilot generator's prose-in-code pattern for future work. Current BookForge materialization is Markdown-first and chapter-sharded; scripts may assemble, count, validate, export, and report, but substantial book prose must live in chapter Markdown refs.
- For book-length targets, use a RCA-like chapter package workflow: detailed chapter plan, per-chapter draft, figure/table production, chapter QC, whole-book review, and final assembly. Invalid compact drafts are retired instead of expanded in place.
- Require chapter budget allocation and an active production queue before body drafting. The workflow must start from target extent -> per-chapter budgets -> named next chapter package, not from a whole-book skim followed by after-the-fact metrics.
- Treat chapter extent as a production gate. BookForge must not complete all chapters and then discover the book is short; it must keep below-target chapters in the active production queue and emit only named preview assemblies until all chapter minimums pass.
- Produce a cumulative completed-contiguous review PDF after chapter text-readiness or full readiness changes. This gives the owner an inspectable book-like artifact during chapter-by-chapter production while preventing a later ready chapter from hiding an unfinished preface, introduction, or earlier chapter. Text-ready-but-missing-asset chapters may be shown for reading, but remain blocked from full readiness.
- Make publication PDF generation a BookForge export backend, not project-local renderer code. The current native helper is `runtime/native_helpers/bookforge_pdf_export.py`, defaulting to Pandoc with XeLaTeX when available and accepting optional metadata/variable profile inputs; Quarto book rendering and Typst are valid future backends for richer book projects.
- Add a publication design profile before publication-grade proof output. Review PDF, publication proof PDF, and final export are separate artifact levels; readable review output does not imply publication-quality design.
- Distinguish `review_pdf`, `publication_proof`, and `final_export` in the BookForge PDF export helper. A successful PDF compile is not enough for publication proof; proof evidence requires design profile, resource-path-backed asset resolution, rendered pages, rendered-page inspection, and element gates. Final export additionally requires owner/export acceptance receipts.
- Add the bundled `bookforge-zh-publication-proof` PDF profile as the default publication-proof style for Chinese nonfiction e-books. It is a BookForge-owned Pandoc/XeLaTeX profile, not a project-private renderer, and it raises proof output above unstyled backend defaults through page geometry, Chinese typography, headings, captions, table/callout treatment, headers/footers, page numbers, and visual-rhythm inspection.
- Make proof plumbing evidence executable: the PDF export helper scans Markdown image refs against backend resource paths, checks required figure-asset-manifest readiness, and can write a rendered-page machine-baseline inspection JSON. This supports publication-proof gates for asset resolution and nonblank rendered pages, while final design judgment and final export still require human/owner evidence.
- Track required `imagegen` outputs through a figure asset manifest. A chat preview without a project-local bitmap path is `preview_only` or blocked evidence, not a completed figure asset.
- Use a RCA-like native imagegen asset route for final manuscript figures: BookForge launches a child Codex executor with native `imagegen` / `image_generation`, materializes the bitmap into the book project, and records a helper receipt. BookForge must not read OpenAI Base URL or API keys as its default path; direct API fallback requires an explicit operator/owner decision for large batches or unavailable built-in imagegen.
- Adopt long-form writing lessons as OPL stage refs rather than a new private controller: book memory, chapter runtime, style engine, and transparent prompt bundles live in skills, prompts, quality gates, contracts, receipts, and project artifacts.
- Map nonfiction memory into three layers: working memory for active chapter context, episodic memory for chapter/owner/revision history, and semantic memory for durable thesis, source canon, glossary, style assets, and evidence rules.
- Treat chapter task cards plus chapter QC and repair refs as the chapter-runtime surface. They are not a scheduler, queue, attempt ledger, session store, or second source of truth.
- Treat style engine assets as reusable writing constraints and review inputs, not as authority to claim final quality or publication acceptance.
- Adopt reference-draft absorption as a first-class BookForge materialization skill. When an owner says a prior/reference version is better, BookForge must compare it, extract transferable book-prose strengths, and update durable domain refs such as style engine, chapter task cards, reader-entry plans, QC gates, evidence maps, or publication design profiles. This stays inside OPL BookForge's domain pack and does not create a private controller or OPL runtime surface.

## 2026-06-19: Project Hygiene Gate For Retired Drafts And Case Stance

- Add a BookForge project hygiene helper for concrete workflow regressions found during the 200-page manuscript run.
- Retired invalid compact drafts and misclassified coverage skeletons should not remain as full searchable book prose inside the active workspace archive. Keep tombstone refs with reason and current source-of-truth refs instead.
- Practice-involved cases require deterministic forbidden-phrase scans in addition to editorial review when a concrete regression has been found. For the Red Bird case, active refs must not keep outside-observer phrases such as `公开可观察`, `公开资料显示`, `教育实验观察窗口`, or `观察它如何强调` after the reader-style contract calls for practice-involved voice.
- README and owner-handoff refs must be refreshed from current metrics or treated as stale status blockers after chapter readiness, figure counts, or review-PDF page counts change.
- Keep App/default product exposure separate until a product owner decision and App-owned contracts add BookForge to visible default routes.

## 2026-06-19: First-Draft Quality Gates From Real Manuscript Run

- Treat first-draft quality as a workflow property, not a late polishing task. Reader-style contract, author/source stance, chapter budget, active production queue, reader-entry plan, figure/table obligations, and anti-AI-flavor rules must shape chapter prompts before visible prose is drafted.
- Require active production queues to track target minimum, current measured extent, missing extent, next action, review-PDF eligibility, and typed blockers for every required unit. This prevents a thin all-chapter pass from being mislabeled as a completed manuscript.
- Block reader-facing manuscript text that leaks internal workflow or status language, including current-version commentary, source-of-truth mechanics, QC/blocker/manifest terms, backend/PDF readiness notes, and known outside-observer case phrases that violate the stance contract.
- Make AI-flavor review concrete and repeatable. Style reports should scan high-risk formulaic negation, generic intensifiers, outline scaffolds, and empty summaries, then record accepted exceptions or repairs instead of relying on impressionistic "polished" claims.
- Treat freshness as part of readiness. Assembly metrics, hygiene scans, review-PDF receipts, image-resolution checks, and owner-handoff refs must be newer than, or digest-linked to, the chapter Markdown, figure manifest, PDF source, and style refs they inspect.
- Require review/publication PDF evidence to prove image resolution when figures are expected. A PDF that compiles but omits `asset_ready` project-local figures is an export blocker, not a usable review or proof artifact.

## 2026-06-19: Reference Revision Absorption For Better First Drafts

- When a reference or edited version reads better, convert the improvement into reusable editorial actions: reader-action openings, relationship sentences, chapter-scope narrowing, process-chain movement, argument-embedded cases, and prose-prepared figure/table interpretation.
- Treat reference absorption as workflow learning before further drafting. Update style engine, chapter task cards, reader-entry plans, QC gates, or publication design refs instead of only patching the visible text.
- Guard against the main side effects of smoother reference revisions: over-compression, loss of reasoning, weakened primary-reader density, local-slice scope being mistaken for whole-book completion, and merge artifacts such as sentence fragments or duplicated labels.

## 2026-06-19: High-Quality Nonfiction Gates From Owner Critique

- Treat serious owner or reviewer critique as BookForge workflow input, not only prose feedback. Repetition, unclear concepts, thin cases, weak modelization, and publication-quality concerns must update the relevant storyline, chapter, evidence, style, QC, or publication-design refs before manuscript repair is claimed.
- Require a chapter function contract for book-length nonfiction: one primary job, one new argument movement, adjacent-chapter handoffs, and explicit non-repeat claims for each chapter. Character budget alone does not make a chapter ready.
- Require an early concept map for recurring terms that carry the argument. Readers should get orientation before the first sustained use, then deeper definitions and applications in the assigned chapters.
- Require a whole-book core model map. Two or three selected models should be introduced, interpreted, applied in later chapters or cases, and recovered in final synthesis; local tables alone do not satisfy modelization.
- Require a case evidence ladder for major examples. Constructed scenes, typical scenarios, documented process materials, authorized interviews/materials, and outcome evidence support different claim strengths, and missing real-case material remains a typed evidence gap.

## 2026-06-19: Reference PDF Front Matter And TOC Absorption

- When the owner supplies a stronger PDF/proof artifact as a reference version, BookForge must compare front matter, proof label, page geometry, image placement, chapter punctuation, and table-of-contents hierarchy as production quality inputs, not only body prose.
- A reader-facing TOC is an argument map. Review notes, production metadata, case-box labels, table labels, figure labels, empty headings, and blocker/status language must not appear as normal TOC entries in review PDFs, publication proofs, or final exports.
- Chinese nonfiction outputs should normalize chapter labels toward `前言：...`, `第一章：...`, and `结语：...` in reader-facing PDF/export surfaces unless an owner-approved house style says otherwise.

## 2026-06-19: Independent Meta-Review Loop

- Add an independent full-manuscript meta-review loop after the assembled draft reaches chapter budget and required asset gates. This mirrors MAS-style independent review: a context-isolated reviewer evaluates viewpoint clarity, whole-book logic, prose fluency, chapter repetition, evidence/case adequacy, practice-involved case voice, and AI-flavor/internal-language residue.
- Treat meta-review as a bounded quality loop, not an infinite polishing lane. Each round must produce a durable review report, a repair plan for required findings, manuscript/source/style/QC updates where accepted, regenerated metrics/hygiene/review-PDF evidence, and then a fresh review if needed.
- Stop early on `pass` or when remaining comments are optional preferences, owner/source-material gaps, publication-proof inspection, or final-export acceptance. If required manuscript repairs remain after three rounds, return a typed `meta_review_iteration_limit_reached` blocker with owner decision options.

## 2026-06-20: Fast-Track Revision Lane

- Add a fast-track revision lane for owner/reviewer suggestions that are small, local, and evidence-bounded after a manuscript or review PDF already exists.
- Fast-track is allowed for local prose rhythm, model short-name memory aids, chapter-boundary clarification, small action checklists, and evidence-label clarity. It is not allowed for new source facts, Red Bird outcome claims, broad chapter-function changes, reader-contract changes, target-extent changes, publication-proof decisions, final-export acceptance, or owner title/subtitle decisions.
- Every fast-track pass must leave a durable audit with suggestion classification, touched refs, accepted repairs, deferred owner/source-material items, evidence boundaries, refreshed artifacts, and validation commands. It reduces unnecessary meta-review cycles without bypassing BookForge quality, source, export, or owner gates.

## 2026-06-20: External Writing-Agent Learning Landing

- Adopt useful patterns from current long-form writing agents as BookForge domain refs: autonomous writing pipelines become `plan -> compose -> write` chapter context discipline, local workspaces become Markdown chapter packages and owner-inspectable refs, multi-agent roles become bounded skills/gates, and retrieval/cross-reference behavior becomes BookForge-scoped source locators and claim ledgers.
- Add a chapter context compiler skill so each active chapter carries intent, selected refs, Standards/Novel/Manuscripts rule stack, protected/compressible context, context trace, missing extent, evidence boundary, task-card linkage, and one next action before drafting or repair.
- Add a source-claim integrity skill so nonfiction claims, tables, figures, captions, callouts, and case boxes carry claim IDs, source locators, evidence classes, provenance, unsupported gaps, truth deltas, and anti-leakage notes.
- Add a style calibration skill so owner samples, reference drafts, comparable works, house style, prior chapters, and QC findings become reusable style profiles, fatigue scans, adopted/rejected rules, accepted exceptions, and style-engine updates.
- Reject importing external runtimes such as generic multi-agent orchestrators, Dify/CrewAI-style controllers, private vector stores, hidden schedulers, or second truth sources. OPL keeps runtime/projection ownership; OPL BookForge keeps manuscript, evidence, memory, quality, export, and owner-gate truth.

## 2026-06-20: Complete-Version Reference Absorption

- When the owner compares two full-book review PDFs or says another version is more publishable, BookForge must run a complete-version absorption pass, not a local wording pass.
- The pass compares reader-entry path, localized scope language, chapter decomposition, book-like transition and explanation density, practice-chapter methodization, conclusion action path, PDF/TOC hierarchy, and active-manuscript strengths to retain.
- The default repair rule is to preserve cases and transitions that help readers follow the argument, compress repeated central judgments that do not add evidence or mechanism, keep the primary-reader contract stable, and avoid inflating length only to imitate the reference.
- Durable outputs must update the reference absorption report plus the relevant reader-entry plans, chapter function contracts, style/QC rules, or publication-design refs before manuscript repair is claimed.

## 2026-06-20: OPL-Owned Publication Proof Dependency Route

- BookForge publication proof depends on local Pandoc, XeLaTeX, Poppler, and TeX Live package availability, but dependency diagnosis and maintenance belong to the OPL system layer.
- The canonical read route is `opl system dependency-doctor --profile bookforge-publication-proof --json`; the canonical maintenance plan route is `opl system dependency-maintenance --profile bookforge-publication-proof --json`.
- BookForge may use the doctor result as proof/export gate input, but it must not implement a private OS package manager, TeX package installer, runtime scheduler, or second dependency truth source inside this repo.
- Dependency failures block `publication_proof` and `final_export` claims, not ordinary writing progress. Storyline shaping, chapter drafting, context packs, claim integrity, style calibration, and other narrower honest actions should continue when they do not require the missing proof backend.
- The bundled proof header removed `titling.sty` and `tocloft.sty`; those packages are legacy diagnostics only and must not be required by the current BookForge proof profile.
