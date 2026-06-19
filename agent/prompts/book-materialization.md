# Book Materialization Prompt

Goal: turn the approved storyline map into a book package with chapter drafts, illustration specs, table specs, consistency checks, wording revision, layout checks, and owner handoff refs.

Produce these refs:

- chapter draft bundle with chapter-level purpose and source refs
- chapter-sharded Markdown source refs for each chapter/part, plus a generated assembly ref for the whole manuscript
- target extent contract with page/word/count requirements inherited from the owner brief, source plan, publisher brief, or storyline map
- reader-style contract inherited from `storyline-architecture`, with audience, reading situation, and natural-expression rules used by chapter drafting and style QC
- reader-facing draft policy that keeps internal production metadata out of manuscript prose and requires first-pass chapter text to read like book prose for the declared readers
- production pipeline contract that names the active chapter packages, chapter briefs, chapter drafts, chapter QC refs, figure asset manifest, table plan, whole-book review, export refs, and any obsolete/retired drafts
- chapter production budget with target pages/chars per chapter and a status gate that distinguishes `not_started`, `outline_only`, `seed_in_progress`, `draft_in_progress`, `chapter_draft_ready`, and `blocked`
- book-memory contract with working, episodic, and semantic memory refs mapped to the active nonfiction manuscript
- chapter task cards for each active chapter, naming reader promise, chapter job, thesis movement, source refs, target extent, figure/table obligations, active memory refs, style constraints, QC state, and typed blockers
- chapter repair back-propagation report showing which accepted QC findings updated the chapter draft, task card, style engine, glossary, evidence map, or semantic memory refs
- transparent prompt bundle refs for chapter drafting, review, repair, style pass, figure/table planning, and export handoff
- illustration plan with image purpose, placement, `imagegen` prompt/spec, generated bitmap asset path when produced, rights/source boundary, and review criteria
- figure asset manifest with one record per required figure, including required/optional status, prompt ref, generated preview ref if any, project-local bitmap path, file existence/inspection status, and blocker kind when missing
- table plan with data source, claim supported, column logic, and formatting rules
- completed-chapters review PDF ref, generated through a publication/typesetting backend after any chapter reaches `chapter_draft_ready`, containing only completed chapters and clearly labeled as an owner review artifact rather than a final export
- PDF export receipt that states `artifact_role` as `review_pdf`, `publication_proof`, or `final_export`; names the real typesetting backend; records resource paths for relative figures; and records artifact-gate blockers separately from PDF compile status
- style consistency report covering voice, terminology, pacing, transitions, and repeated phrases
- AI-flavor revision report that replaces vague hedging, contrast formulas, inflated phrasing, and empty summaries with direct prose
- publication design profile that distinguishes review PDF, publication proof PDF, and final export
- layout and typography QC report
- owner handoff packet with remaining decisions and blockers

Maintain the storyline contract, reader-style contract, and declared target extent. Keep chapter prose concrete, consistent, evidence-grounded, and publication-aware. Use affirmative phrasing as the default editorial move.

Do not begin body drafting or chapter expansion when the reader-style contract is missing, generic, or unresolved. If audience and natural expression were inferred rather than owner-specified, keep the inference and owner-review status visible in the handoff and style reports.

Make the first chapter draft reader-facing by default. Before writing visible prose for each production chapter, create a reader-entry plan inside the chapter brief or drafting notes: opening scene/question, reader tension, concrete example/case, main claim, section movement, table/figure role, and closing transition. Chapter task, core question, chapter thesis, target extent, source refs, figure asset states, QC notes, blockers, and this reader-entry plan belong in chapter briefs, manifests, QC reports, comments, and owner handoff refs; they must not be emitted as visible chapter openings, section headings, or explanatory paragraphs in the manuscript body. Start chapters from a concrete scene, reader problem, tension, or practical question before moving into concepts. If a later reader-facing revision pass is useful, it is allowed, but BookForge must not depend on a late polish pass to remove predictable planning scaffolding. If a chapter needs a routine reader-facing rewrite because the first draft reads like a memo, treat that as a drafting-gate failure and fix the chapter-production pattern before continuing with more chapters.

Use a Markdown-first writing surface. Write and revise prose in per-chapter Markdown files or equivalent author-facing Markdown refs. Use generator scripts only as thin assemblers/checkers/exporters that read manuscript refs and produce metrics, reports, merged `book.md`, DOCX/PDF, or receipts. Do not embed book prose in Python/TypeScript/shell/JSON string literals as the manuscript source of truth.

Use chapter task cards as the chapter-runtime surface. They are owner-inspectable refs for intent, source slices, active memory, style constraints, figure/table obligations, QC state, and blockers. They are not a private scheduler, queue, attempt ledger, session store, or runtime truth source.

Run chapter repair as a feedback loop. First repair the chapter package; then update durable style, glossary, evidence, and semantic-memory refs only when the finding is reusable. Keep rejected repairs visible with reason and owner decision need.

For book-length work, shard drafting by chapter or part: chapter brief -> chapter Markdown draft -> chapter-level QC -> merged manuscript -> whole-book pass. Do not make a single long `book.md` the only creative working file for a multi-chapter book unless the owner explicitly requests a one-file workflow.

Before drafting body prose for a book-length target, convert the owner/source target extent into a chapter production budget and an active production queue. A "coverage pass" that puts short seed text into every chapter is not book materialization unless each chapter is intentionally labeled seed/in-progress and the next production chapter is named with its remaining character/page budget.

Make the chapter budget a production gate, not a later audit. A chapter below its inherited minimum extent is not drafted/done; it is `seed_in_progress` or `draft_in_progress`. Do not mark all chapters complete and then discover the manuscript is short. Generate `book.preview.md` for below-target whole-book previews, and reserve final `book.md` for an all-chapters-ready assembly unless the owner explicitly requests a named preview export.

After every chapter reaches `chapter_draft_ready` or a narrower text-ready checkpoint, compile a review PDF containing the contiguous reader sequence from the beginning of the book: front matter/opening matter plus chapters in order, stopping at the first below-target required unit. Do not silently skip an unfinished preface, introduction, or earlier chapter to show later ready chapters as if the book were continuous. If a later chapter is ready but an earlier required unit is not, return a typed review-continuity blocker and make the earlier unit the next production target. Name and label this artifact as an owner-review PDF, not a final book export, so the owner can review cumulative text and request corrections before the next chapters are produced. If a text-ready chapter still lacks required project-local imagegen assets, include it only as a text-review checkpoint and keep full chapter readiness blocked.

Treat PDF generation as a first-class BookForge export capability. Use the BookForge PDF export helper or an equivalent BookForge-owned backend adapter to call a real publication/typesetting backend such as Pandoc with XeLaTeX/LuaLaTeX, Quarto book rendering, or Typst. Do not implement publication PDF by hand-drawing text into images, ad-hoc canvas/Pillow page painting, or other bespoke renderer code except as a temporary diagnostic fallback with a typed blocker.

For PDF export, distinguish the target explicitly. A `review_pdf` is a readable owner/editor review artifact and cannot be upgraded by wording into a publication proof. A `publication_proof` requires a publication design profile, a real typesetting backend such as Pandoc with XeLaTeX/LuaLaTeX, Quarto, Typst, or Paged.js, resource paths that make relative figures resolve, rendered page refs, and rendered-page inspection of captions, callouts, tables, figures, hierarchy, running heads/feet, page numbers, overflow, and visual rhythm. A `final_export` requires the publication proof evidence plus owner/export acceptance receipts. If the backend, design profile, rendered-page inspection, element gates, resource paths, local figure assets, or owner receipts are missing, return a typed export blocker instead of claiming export readiness.

Before producing a publication-grade proof, establish a publication design profile. It must define page size, geometry, body font, heading scale, line length, caption style, figure placement, table style, case-box/callout style, headers/footers, page numbering, visual rhythm, and rendered-page inspection plan. A readable review PDF is useful for owner review but is not enough to claim publication quality.

When restarting after an invalid compact/sample draft, retire that draft into an archive/tombstone ref and rebuild from the chapter packages. Do not treat the compact draft as the expansion seed unless the owner explicitly accepts that route.

Do not shorten, compact, summarize, or convert a book-length target into a sample draft unless the owner explicitly changes the target extent. If the requested extent cannot be completed in the current pass, materialize the stable plan and partial manuscript, then return a typed extent blocker with the missing pages/words/chapters.

For final manuscript figures, use raster assets generated through the Codex `imagegen` skill by default. Prefer the BookForge native imagegen asset helper or an equivalent BookForge-owned backend adapter so final artwork is generated through a Codex executor with native imagegen enabled, copied into the project, recorded in a receipt, and synchronized back into the figure asset manifest by `figure_id`. Do not use SVG, script-generated diagrams, or placeholder art as final figures unless the owner explicitly requests deterministic vector output. If image generation cannot be completed, or if the generated file path is not exposed so the asset cannot be copied into the project, return a typed image-asset blocker instead of silently downgrading the figure. Do not make direct OpenAI Base URL/API-key calls the default BookForge figure route; direct API fallback is an explicit operator/owner route for large batches or unavailable built-in imagegen.
