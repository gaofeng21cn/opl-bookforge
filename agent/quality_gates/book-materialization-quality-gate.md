# Book Materialization Quality Gate

Quality gate declaration is required for every generated OPL-compatible stage.
Dedicated review stage is conditional: create one when chapter drafts, illustration/table plans, style decisions, layout decisions, export packaging, or owner handoff affects final book quality.

Pass conditions:

- Chapter drafts follow the storyline map and preserve a coherent book-level arc.
- Book-length manuscript source is Markdown-first and chapter-sharded; the merged `book.md` or export file is produced from chapter refs rather than used as the only creative working surface.
- The production pipeline contract identifies chapter packages, chapter briefs, chapter drafts, chapter QC refs, figure asset manifest, table plan, whole-book review, export refs, and retired obsolete drafts.
- The manuscript obeys the declared target extent from the owner brief, source plan, publisher brief, or storyline map; any shortfall is quantified as a typed extent blocker.
- Claims, examples, tables, and illustrations are grounded in declared source refs.
- Style, terminology, stance, tense, and chapter rhythm remain consistent across the manuscript.
- The wording pass replaces generic AI-flavored phrasing with direct, specific, affirmative prose.
- Illustration and table plans state purpose, placement, data/source boundary, review criteria, and owner decision needs.
- A figure asset manifest records every required figure and distinguishes `planned`, `preview_only`, `asset_ready`, and `blocked_missing_project_bitmap` states.
- Final manuscript figures that require new artwork are generated bitmap assets from the Codex `imagegen` skill, with prompt/spec, project-local saved asset path, source/rights boundary, and visual review criteria recorded.
- Layout QC covers hierarchy, page rhythm, captions, cross-references, table readability, image placement, and export target constraints.
- Handoff includes artifacts, receipts, blockers, remaining owner decisions, and verification refs.

Fail-closed conditions:

- Missing storyline map, chapter plan, source refs, manuscript body refs, image/table refs, layout target, or owner gate.
- Book prose is stored primarily as large generator-code string literals instead of author-facing Markdown chapter refs, or a book-length project uses only one monolithic creative source file without explicit owner approval.
- Requested or source-declared extent is silently reduced, summarized, or turned into a compact/sample draft without explicit owner approval.
- An invalid compact/sample draft remains on the active manuscript path after the owner asks to restart from the correct chapter-sharded workflow.
- Chapters drift from the premise or repeat the same argument without new movement.
- Tables or illustrations introduce unsupported claims.
- Required final figures are replaced by SVG, local-script diagrams, generic placeholders, undocumented generated assets, or generated assets whose file paths are not exposed and copied into the project, without an explicit owner-approved vector requirement.
- A figure is marked complete when only a chat preview exists and no project-local bitmap can be inspected.
- Review relies on provider completion, generated interface readiness, or suite pass as final quality evidence.
- Any generated surface claims publication approval, export readiness, or final editorial acceptance.
