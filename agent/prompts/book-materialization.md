# Book Materialization Prompt

Goal: turn the approved storyline map into a book package with chapter drafts, illustration specs, table specs, consistency checks, wording revision, layout checks, and owner handoff refs.

Produce these refs:

- chapter draft bundle with chapter-level purpose and source refs
- chapter-sharded Markdown source refs for each chapter/part, plus a generated assembly ref for the whole manuscript
- target extent contract with page/word/count requirements inherited from the owner brief, source plan, publisher brief, or storyline map
- production pipeline contract that names the active chapter packages, chapter briefs, chapter drafts, chapter QC refs, figure asset manifest, table plan, whole-book review, export refs, and any obsolete/retired drafts
- illustration plan with image purpose, placement, `imagegen` prompt/spec, generated bitmap asset path when produced, rights/source boundary, and review criteria
- figure asset manifest with one record per required figure, including required/optional status, prompt ref, generated preview ref if any, project-local bitmap path, file existence/inspection status, and blocker kind when missing
- table plan with data source, claim supported, column logic, and formatting rules
- style consistency report covering voice, terminology, pacing, transitions, and repeated phrases
- AI-flavor revision report that replaces vague hedging, contrast formulas, inflated phrasing, and empty summaries with direct prose
- layout and typography QC report
- owner handoff packet with remaining decisions and blockers

Maintain the storyline contract and declared target extent. Keep chapter prose concrete, consistent, evidence-grounded, and publication-aware. Use affirmative phrasing as the default editorial move.

Use a Markdown-first writing surface. Write and revise prose in per-chapter Markdown files or equivalent author-facing Markdown refs. Use generator scripts only as thin assemblers/checkers/exporters that read manuscript refs and produce metrics, reports, merged `book.md`, DOCX/PDF, or receipts. Do not embed book prose in Python/TypeScript/shell/JSON string literals as the manuscript source of truth.

For book-length work, shard drafting by chapter or part: chapter brief -> chapter Markdown draft -> chapter-level QC -> merged manuscript -> whole-book pass. Do not make a single long `book.md` the only creative working file for a multi-chapter book unless the owner explicitly requests a one-file workflow.

When restarting after an invalid compact/sample draft, retire that draft into an archive/tombstone ref and rebuild from the chapter packages. Do not treat the compact draft as the expansion seed unless the owner explicitly accepts that route.

Do not shorten, compact, summarize, or convert a book-length target into a sample draft unless the owner explicitly changes the target extent. If the requested extent cannot be completed in the current pass, materialize the stable plan and partial manuscript, then return a typed extent blocker with the missing pages/words/chapters.

For final manuscript figures, use raster assets generated through the Codex `imagegen` skill by default. Do not use SVG, script-generated diagrams, or placeholder art as final figures unless the owner explicitly requests deterministic vector output. If image generation cannot be completed, or if the generated file path is not exposed so the asset cannot be copied into the project, return a typed image-asset blocker instead of silently downgrading the figure.
