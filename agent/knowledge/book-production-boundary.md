# Book Production Boundary

Book production covers chapter text, illustration and table planning, style consistency, wording revision, layout QC, and owner handoff.

Chapter prose is judged against the book's reader-style contract, not a generic naturalness ideal. The contract should define the target readers, reading situation, prior knowledge, emotional temperature, example density, jargon boundary, sentence rhythm, and forbidden voice patterns. If the contract is missing or unresolved, book-length drafting should stop for owner clarification.

Manuscript prose is domain artifact body, not generator code. BookForge materialization should keep author-facing prose in Markdown chapter files and use scripts only for deterministic assembly, metrics, validation, export, and reports. Large blocks of manuscript text embedded in Python, TypeScript, shell, JSON string literals, or other generator code are a design smell and should be migrated to chapter Markdown refs.

Book-length materialization is chapter-sharded by default. A complete draft should progress through chapter briefs, per-chapter Markdown drafts, chapter-level quality checks, merge assembly, and whole-book review. A single `book.md` is the assembled/export manuscript ref, not the primary writing surface for a long book unless the owner explicitly requests a one-file manuscript workflow.

Target budgets are gates, not post-hoc metrics. A chapter that has 2,000 characters against a 13,000-character target is not a completed chapter draft; it is a seed or in-progress chapter package. Below-target full-book assemblies must be named previews and must not occupy the final `book.md` slot unless the owner explicitly defines `book.md` as preview-only for that run.

If an earlier pass produced a compact or sample draft against a book-length target, that draft is historical evidence, not the active seed for completion. Retire it to an archive/tombstone ref and restart the active manuscript from chapter packages, briefs, drafts, QC refs, and final assembly.

Target extent is part of book truth. If the owner brief, source plan, publisher brief, or storyline map declares a page count, word count, chapter count, or series volume, materialization must preserve that target or return a typed extent blocker. A compact draft, sample chapter, or synopsis is a different deliverable and needs an explicit owner decision.

PDF export is a BookForge capability boundary. Project-local scripts may assemble chapter refs and invoke the BookForge PDF export helper, but they should not own publication layout engines or hand-roll page rendering. The normal path is Markdown or chapter sources into a BookForge-owned backend adapter for Pandoc/XeLaTeX, Quarto, Typst, or an equivalent publication/typesetting system, followed by rendered-page inspection and an export manifest.

Illustrations and tables must carry purpose, source, placement, and review criteria. Decorative assets, unsourced tables, invented data, and generic filler weaken the manuscript and should become revision items or typed blockers.

When a real manuscript needs new visual artwork, final figures default to Codex `imagegen` skill outputs saved as project-bound bitmap assets. SVG, local script diagrams, placeholders, chat previews, or generated images without exposed file paths can support planning, but they do not satisfy final illustration evidence unless the owner explicitly chooses deterministic vector output. Long-form projects should keep a figure asset manifest so missing local bitmaps remain visible.

The AI-flavor check favors confident human editing: direct sentence openings, concrete causal links, stable terminology, varied rhythm, and precise transitions. The check flags hedging, inflated abstractions, repetitive framing, and contrast formulas that make the prose feel machine-generated.

Final quality, export readiness, print readiness, and publication approval require owner receipts.
