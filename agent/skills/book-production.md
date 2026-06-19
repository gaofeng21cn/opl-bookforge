# Book Production Skill

Use this skill when drafting or revising a book package from an approved storyline map.

Working policy:

- Draft chapters from the chapter thesis chain and evidence map.
- Keep prose in author-facing Markdown chapter files or equivalent Markdown refs. Treat scripts as thin assembly, metrics, validation, export, and report helpers; do not make generator-code string literals the manuscript source of truth.
- For book-length work, draft and review by chapter/part first, then assemble and run whole-book checks. The assembled `book.md` is a delivery/export ref, not the only creative working file unless the owner explicitly chooses that workflow.
- Preserve the target extent declared by the owner brief, source plan, publisher brief, or storyline map. Do not reduce a book-length target to a compact/sample draft unless the owner explicitly changes that target; record any shortfall as a typed extent blocker.
- When a compact/sample draft was produced against a book-length target, retire it as an obsolete draft and rebuild the active manuscript from chapter packages rather than expanding the invalid file in place.
- Maintain a production pipeline contract for long manuscripts: chapter packages, briefs, drafts, chapter QC, figure asset manifest, table plan, whole-book review, export refs, and blockers.
- Keep voice, terminology, chapter structure, and transition style consistent.
- Plan illustrations and tables as meaning-bearing book elements, with source and rights boundaries attached.
- Generate final book-bound bitmap illustrations through the Codex `imagegen` skill when image assets are required. Keep the prompt, project-local generated asset path, source/rights boundary, and review criteria with the illustration ref and figure asset manifest. Do not substitute SVG, local script diagrams, decorative placeholders, chat-preview-only images, or unlocatable generated images for final manuscript figures unless the owner explicitly asks for deterministic vector output.
- Run a wording pass that favors direct claims, precise verbs, concrete nouns, and affirmative editorial movement.
- Run layout and typography checks before handoff.
- Return typed blockers for missing manuscript, source, image, table, layout, or owner gate refs.

This skill does not publish, export, or approve final book quality without owner receipt.
