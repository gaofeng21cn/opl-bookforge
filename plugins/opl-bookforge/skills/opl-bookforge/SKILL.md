---
name: opl-bookforge
description: Use when Codex should operate OPL Book Forge as the default book-authoring entry for storyline architecture, manuscript materialization, figures, tables, style control, publication proof/export handoff, and owner-gated book decisions.
---

# OPL Book Forge

This is the repo-owned primary Codex skill source for OPL Book Forge. It is the default Codex entry that OPL materializes into the repo-local plugin carrier at `plugins/opl-bookforge/skills/opl-bookforge/SKILL.md`. Professional skills under `agent/professional_skills/*/SKILL.md` remain repo-internal method skills and are invoked only when their focused method is needed.

## Use Cases

Use OPL Book Forge when the task is to:

- shape a book premise, reader promise, argument arc, source map, chapter thesis chain, and owner handoff;
- turn an approved storyline into chapter packages, manuscript Markdown, figure and table plans, style checks, layout QC, review PDF refs, and export handoff refs;
- repair a manuscript after owner critique, reviewer critique, whole-book meta-review, complete-version comparison, or stronger reference draft absorption;
- plan or verify review PDFs, publication proofs, final exports, figures, tables, captions, rendered pages, and publication design evidence;
- maintain book-level memory, source/claim integrity, style consistency, and chapter continuity for long-form nonfiction.

Do not use this skill to claim production readiness, publication approval, final export acceptance, owner acceptance, hosted runtime parity, or OPL runtime readiness. Those claims require their own owner receipts, typed blockers, runtime receipts, rendered proof evidence, or final-export acceptance refs.

## Reader And Style Contract

Before body drafting or chapter expansion, establish or locate a reader-style contract. It must name:

- primary readers, secondary readers, and excluded readers;
- reading situation, prior knowledge, reader anxieties, practical questions, and tolerance for theory, examples, jargon, and persuasion;
- natural-expression rules for stance, vocabulary, sentence rhythm, paragraph movement, example density, metaphors, and forbidden voice patterns;
- author/source stance for major cases, especially practice-involved cases where the author team designed, executed, evaluated, or participated in the work;
- owner-review status or typed owner question when audience or voice is inferred rather than explicitly approved.

Primary readers define the writing target. Secondary readers add only compatible accessibility constraints unless the owner explicitly promotes them to co-primary readers. Do not silently lower density, add explanatory detours, or create a competing voice target for secondary readers.

If the owner did not specify audience or voice and Book Forge cannot infer them with high confidence from source refs, choose the most defensible provisional reader-style contract, record the uncertainty as quality debt, and continue. Ask the owner when useful, but do not block stage transition unless an explicit owner decision is genuinely required for protected or irreversible work. Do not silently choose a generic educated-reader style.

Use the reader-style contract in storyline shaping, chapter task cards, chapter drafting prompts, style QC, reference absorption, meta-review, and publication proof checks. Naturalness is judged against the declared readers, not a generic prose ideal.

## Storyline Architecture

Storyline architecture owns the durable book design before materialization. Produce or repair:

- premise, reader promise, central argument, and narrative engine;
- source map, evidence map, case evidence ladder, and known source gaps;
- author/source stance map for major cases and examples;
- chapter thesis chain with each chapter's primary job, new movement, adjacent handoff, and non-repeat claims;
- early concept map for recurring terms and where they are first defined or foreshadowed;
- two or three whole-book core models with introduction, later application, figure/table candidates, and final recovery points;
- risks, owner questions, route-back refs, typed blockers, or owner handoff refs.

When critique identifies repetition, weak case density, unclear concepts, poor modelization, or publication-level monotony, absorb the finding into storyline refs, chapter task cards, style rules, evidence maps, quality gates, or publication design refs before local prose repair.

## Book Materialization Rules

Keep book prose Markdown-first. Per-chapter Markdown files, or equivalent author-facing Markdown refs, own substantial manuscript body. Scripts may assemble, count, validate, export, and write reports; they must not become the manuscript source of truth through large Python, TypeScript, shell, or JSON prose literals.

Materialize book-length nonfiction chapter by chapter:

1. approved storyline and reader-style contract;
2. target extent converted into chapter budgets and an active production queue;
3. chapter task card and chapter context pack;
4. chapter brief with reader-entry plan;
5. per-chapter Markdown draft;
6. chapter-level QC, source/claim check, style check, and memory update;
7. contiguous review PDF or equivalent owner review artifact when eligible;
8. whole-book assembly, meta-review, repair routing, proof/export handoff.

Before visible chapter prose is written, create a reader-entry plan in the chapter brief or drafting notes: opening scene/question, reader tension, concrete example/case, main claim, section movement, figure/table role, and closing transition. Keep that plan, budgets, source refs, asset status, QC notes, blockers, and internal workflow fields out of manuscript prose.

First visible drafts should read like book prose for the declared readers. Chapter openings and major transitions should start from a concrete scene, reader problem, practical question, consequence, or tension before concepts, unless the reader-style contract explicitly calls for a technical structure. If first drafts repeatedly read like memos or production scaffolds, repair the chapter-production pattern before continuing.

Target extent is a gate. Preserve owner/source-declared page, word, character, chapter, figure, table, or series targets. Below-target units remain `seed_in_progress` or `draft_in_progress`; below-target whole-book assemblies must be named previews. Do not relabel compact samples as complete drafts unless the owner explicitly changes the artifact target.

Use chapter task cards as the chapter-runtime surface: reader promise, chapter job, thesis movement, source refs, target extent, figure/table obligations, active memory refs, style constraints, QC state, next action, review-PDF eligibility, and blockers. Do not add a Book Forge-private scheduler, queue, session store, provider store, or attempt ledger.

Maintain owner-inspectable book memory:

- working memory for active chapter context, source notes, unresolved review notes, and near-term style constraints;
- episodic memory for prior chapter QC, owner decisions, revisions, figure/table decisions, and route-back history;
- semantic memory for durable thesis, reader-style contract, source canon, glossary, style assets, structural principles, and evidence rules.

Back-propagate reusable chapter QC repairs into task cards, style engine, glossary, evidence map, semantic memory, or quality gates. Do not only patch local prose when the defect is systemic.

## Revision And Review Workflow

After serious critique, complete-version comparison, or whole-book meta-review, route repair before editing. Classify the topmost repair level:

- artifact target;
- storyline architecture;
- outline sequence;
- chapter function;
- evidence/model;
- publication design;
- local prose;
- owner/source blocker.

Local fast-track repair is allowed only for bounded, evidence-safe prose or clarity fixes after the higher layer is stable or explicitly routed. Do not paste reviewer comments into prose. Classify each finding, update durable refs when needed, revise the manuscript source, regenerate affected reports/artifacts, and record downstream freshness obligations.

If a stronger reference draft, prior version, edited chapter, comparable sample, or review PDF is supplied, run reference-draft absorption before major rewriting. Extract transferable strengths into reader-entry plans, task cards, style engine, QC gates, evidence maps, or publication design refs. Do not copy reference prose or turn secondary-reader explanation style into the new primary voice.

## Source, Claims, Figures, And Tables

Every material nonfiction claim should be inspectable through source, evidence, or owner-supplied refs. Tables, figures, captions, callouts, and case boxes are claims too.

Match language to evidence class:

- constructed scene;
- typical scenario;
- documented process material;
- authorized material or interview;
- owner-supplied source;
- outcome or impact evidence;
- unsupported gap.

Remove, bracket, or downgrade unsupported non-central claims. When a readable manuscript exists but a central claim or outcome locator remains unsupported, mark `completed_with_quality_debt`, advance, and keep publication/export/readiness claims closed. Return a typed blocker only when no consumable manuscript can be produced, protected material or authorization is missing, identity/currentness is invalid, or an explicit human decision is required.

Figures and tables must carry purpose, source, placement, caption intent, claim boundary, and review criteria. Real photos, generated artwork, deterministic diagrams, tables, case boxes, and reviewer callouts are different artifact classes and need separate manifest treatment.

For final manuscript figures requiring new artwork, use Codex `imagegen` / native image generation by default through the Book Forge image asset route or an equivalent Book Forge-owned adapter. Save generated bitmap assets to project-local paths, record prompt/spec/provenance/review criteria, and synchronize the figure asset manifest by figure id. Chat-preview-only images, missing file paths, placeholders, unavailable generated assets, or failed executor receipts are asset quality debt when a readable manuscript/review artifact exists: preserve captions and intent, advance, and keep asset-ready/publication-proof/final-export claims closed. Direct OpenAI Base URL/API-key calls are not the default route; use them only as an explicit operator/owner fallback.

## Publication Proof And Export Boundary

Keep `review_pdf`, `publication_proof`, and `final_export` separate.

- `review_pdf`: readable owner/editor review artifact. It may support chapter review and cumulative reading, but it is not publication proof.
- `publication_proof`: requires a publication design profile, real typesetting backend receipt, resource-path-backed figure resolution, Markdown image-ref checks, figure asset manifest readiness, rendered-page refs, and rendered-page inspection for hierarchy, captions, tables, figures, callouts, page numbers, overflow, and visual rhythm.
- `final_export`: requires publication-proof evidence plus owner/export acceptance receipts.

Use Book Forge-owned export helpers or equivalent adapters backed by real publication/typesetting systems such as Pandoc with XeLaTeX/LuaLaTeX, Quarto book rendering, Typst, or Paged.js. Do not hand-roll normal book PDF layout with ad-hoc raster text drawing.

For Chinese nonfiction e-book proof output, use the bundled `bookforge-zh-publication-proof` profile or an owner-approved equivalent. Unstyled backend output is review-output quality, not publication-proof quality.

Machine-baseline rendered-page inspection can prove nonblank pages and asset plumbing, but it does not replace human publication-design review or owner final-export acceptance.

## Professional Skill Routing

Invoke repo-internal professional skills when the focused method is needed:

- `bookforge-story-style-architect`: storyline, reader contract, chapter function, author/source stance, and reusable prose style.
- `bookforge-chapter-author`: chapter context pack, task card, reader-entry plan, chapter Markdown drafting/repair, QC, and review-PDF eligibility.
- `bookforge-source-reference-reviewer`: claim ledger, source locator, evidence class, unsupported gaps, anti-leakage, and stronger reference absorption.
- `bookforge-meta-reviewer`: independent meta-review, revision entrypoint routing, reviewer-comment absorption, and fast-track eligibility.
- `bookforge-publication-memory-curator`: book memory, review PDF, publication proof, final export, design tokens, figures/tables, and rendered-page QA.

The primary skill chooses the route and preserves the book-level contract. Professional skills carry method. Tool catalogs describe affordances and forbidden authority. Stage prompts define target refs and accepted handoff shapes.

## Authority Boundary

Book Forge uses one semantic control plane: Codex CLI. Any readable manuscript,
outline, source finding, review finding, failed proof, partial asset set, or
diagnostic is progress and may feed the next declared stage. Retry, review, and
repair limits are quality budgets, not transition gates. Codex may advance,
repeat the current stage, or route back to storyline, production planning,
chapter materialization, source/style integrity review, or any other declared
stage. Schema, normalizer, validator, review, proof, style, and source gaps are
quality debt when a consumable artifact exists; they block publication proof,
final export, acceptance, and readiness claims, not drafting or stage progress.
Only zero consumable artifact, corrupt/unreadable bytes, permission or safety,
identity/currentness, irreversible action, or explicit owner/human authority may
hard-stop progression.

OPL materializes this repo-owned primary skill into Codex carrier surfaces. OPL owns generated interfaces, plugin packaging, generic runtime, queues, provider attempts, attempt ledger, projection, workbench, Agent Lab, registry/discovery, and generated status/readback surfaces.

OPL Book Forge owns book-domain truth, manuscript body, memory body, source/claim bodies, style policy, figure/table planning, export/publication verdict boundaries, artifact authority, owner receipts, typed blocker refs, human gates, and route-back refs.

Generated interface readiness, scaffold validation, provider completion, StageRun readiness, OMA pass, focused tests, review PDF compilation, or this skill's presence cannot claim domain readiness, production readiness, publication approval, final export readiness, owner acceptance, or live hosted parity.

Valid closeout shapes are owner receipt refs, typed blocker refs, human gate refs, route-back refs, or clearly scoped review/export artifacts with their evidence boundary named.
