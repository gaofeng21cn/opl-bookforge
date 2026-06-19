# Book Materialization Quality Gate

Quality gate declaration is required for every generated OPL-compatible stage.
Dedicated review stage is conditional: create one when chapter drafts, illustration/table plans, style decisions, layout decisions, export packaging, or owner handoff affects final book quality.

Pass conditions:

- Chapter drafts follow the storyline map and preserve a coherent book-level arc.
- Chapter drafts cite and obey the reader-style contract from `storyline-architecture`; naturalness is judged against the declared reader groups and reading situation, not a generic prose ideal.
- Each production chapter has a reader-entry plan in the chapter brief or drafting notes before visible prose is drafted, covering opening scene/question, reader tension, concrete example/case, main claim, section movement, table/figure role, and closing transition.
- Chapter drafts are reader-facing on the first visible manuscript pass: internal chapter task, core question, thesis, target budget, source refs, figure asset status, QC notes, and blockers are kept in briefs/manifests/reports rather than exposed as book prose.
- Chapter openings and major section transitions start from a scene, reader tension, practical question, or consequence before moving into concepts, unless the reader-style contract explicitly calls for a more technical structure.
- Book-length manuscript source is Markdown-first and chapter-sharded; the merged `book.md` or export file is produced from chapter refs rather than used as the only creative working surface.
- The production pipeline contract identifies chapter packages, chapter briefs, chapter drafts, chapter QC refs, figure asset manifest, table plan, whole-book review, export refs, and retired obsolete drafts.
- The owner/source target extent is converted into chapter-level page/character budgets and an active production queue before body drafting starts.
- Chapter budget gates are enforced before completion labels: below-target chapter prose is `seed_in_progress` or `draft_in_progress`, not `chapter_draft_ready`, `done`, or whole-book completion.
- The manuscript obeys the declared target extent from the owner brief, source plan, publisher brief, or storyline map; any shortfall is quantified as a typed extent blocker.
- Claims, examples, tables, and illustrations are grounded in declared source refs.
- Style, terminology, stance, tense, chapter rhythm, and example density remain consistent with the reader-style contract across the manuscript.
- The wording pass replaces generic AI-flavored phrasing with direct, specific, affirmative prose.
- Illustration and table plans state purpose, placement, data/source boundary, review criteria, and owner decision needs.
- A figure asset manifest records every required figure and distinguishes `planned`, `preview_only`, `asset_ready`, and `blocked_missing_project_bitmap` states.
- Final manuscript figures that require new artwork are generated bitmap assets from the Codex `imagegen` skill, with prompt/spec, project-local saved asset path, source/rights boundary, helper receipt/provenance, and visual review criteria recorded.
- The default final-figure route uses the BookForge native imagegen asset helper or an equivalent BookForge-owned backend adapter that delegates provider credentials to the Codex executor/native imagegen surface; direct Base URL/API-key provider calls are not the default route.
- A completed-contiguous review PDF is refreshed after chapter text-readiness or full readiness changes through a real publication/typesetting backend; it includes the reviewable reader sequence from the beginning of the book, stops at the first below-target required unit, and is labeled as an owner review artifact, not final export readiness.
- Review PDF, publication proof PDF, and final export are separate artifact levels. Publication proof requires a publication design profile covering page geometry, typography, captions, figures, tables, case boxes/callouts, headers/footers, numbering, visual rhythm, and rendered-page inspection.
- Layout QC covers hierarchy, page rhythm, captions, cross-references, table readability, image placement, and export target constraints.
- Handoff includes artifacts, receipts, blockers, remaining owner decisions, and verification refs.

Fail-closed conditions:

- Missing storyline map, reader-style contract, chapter plan, source refs, manuscript body refs, image/table refs, layout target, or owner gate.
- Chapter prose uses a generic style that does not match the declared reader groups, or materialization proceeds after the reader-style contract asks for owner clarification.
- A production chapter lacks a reader-entry plan before body drafting, or the plan is exposed as manuscript prose instead of staying in briefs, notes, manifests, reports, comments, or handoff refs.
- Reader-facing manuscript body exposes production scaffold as prose, including visible "chapter task", "core question", "chapter conclusion", "asset status", manifest paths, target budgets, QC notes, or blocker refs.
- Chapter or section writing reads like a planning memo, technical spec, or instruction manual because it lists framework elements without reader scenes, concrete questions, consequences, or natural transitions required by the reader-style contract.
- BookForge relies on a routine late "reader-facing rewrite" to remove predictable memo/instruction-manual prose instead of treating the memo-like first draft as a drafting-gate failure.
- Missing chapter production budget or active production queue for a book-length target before manuscript body drafting.
- Book prose is stored primarily as large generator-code string literals instead of author-facing Markdown chapter refs, or a book-length project uses only one monolithic creative source file without explicit owner approval.
- Requested or source-declared extent is silently reduced, summarized, or turned into a compact/sample draft without explicit owner approval.
- A whole-book coverage pass creates short text for every chapter and is then presented as completed materialization instead of a seed/preview skeleton with named next chapter production work.
- A below-target chapter is labeled drafted, complete, ready, done, or used to claim that all chapter content is done.
- A below-target whole-book preview is written or referenced as final `book.md` without explicit preview naming and typed blockers.
- A completed-contiguous review PDF skips an unfinished preface, introduction, or earlier required chapter to include later ready chapters, includes below-target required units without labeling/blocking, or is named/described as a final publication/export artifact before all gates pass.
- A review PDF is used to claim publication quality, final proof readiness, or final export readiness without a publication design profile and rendered-page inspection.
- Publication PDF generation bypasses the BookForge export helper or equivalent BookForge-owned backend adapter and is implemented by ad-hoc raster text drawing or bespoke page renderer code instead of a real export/typesetting backend, unless explicitly marked as a temporary diagnostic fallback with a typed blocker.
- An invalid compact/sample draft remains on the active manuscript path after the owner asks to restart from the correct chapter-sharded workflow.
- Chapters drift from the premise or repeat the same argument without new movement.
- Tables or illustrations introduce unsupported claims.
- Required final figures are replaced by SVG, local-script diagrams, generic placeholders, undocumented generated assets, or generated assets whose file paths are not exposed and copied into the project, without an explicit owner-approved vector requirement.
- A figure is marked complete when only a chat preview exists and no project-local bitmap can be inspected.
- A generated figure lacks a helper receipt/provenance proving project-local bitmap materialization, or the normal route bypasses Codex native imagegen with direct provider credentials without an explicit fallback decision.
- Review relies on provider completion, generated interface readiness, or suite pass as final quality evidence.
- Any generated surface claims publication approval, export readiness, or final editorial acceptance.
