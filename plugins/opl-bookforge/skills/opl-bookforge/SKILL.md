---
name: opl-bookforge
description: Use when Codex needs OPL Book Forge to shape or materially produce a book-length nonfiction work, including storyline architecture, reader/style design, chapter planning and drafting, source/claim review, figures and tables, publication proof, or export handoff. Do not use for an isolated article, research paper, grant, slide deck, generic document formatting, or to claim publication/final-export approval without owner evidence.
---

# OPL Book Forge

This is the canonical Book Forge routing Skill. OPL materializes it into the Codex plugin carrier; repo-internal professional Skills provide focused methods and do not replace this entry.

## Admission

- Admit Book Forge when the requested outcome is a book or a chapter, figure, table, proof, or revision that belongs to an identifiable book project.
- Keep isolated papers with MAS, grant applications with MAG, visual presentations with RCA, and generic document-formatting tasks with their owning capability.
- Bind the current book/workspace, source cohort, intended readers, artifact target, and any accepted storyline or owner decision before choosing a production action.
- Do not infer publication approval, final-export acceptance, owner acceptance, or runtime readiness from a Skill invocation, generated file, validator pass, review PDF, or provider completion.

## Action Routing

Use the installed OPL-generated interface and one of two public actions:

- `shape-storyline`: use when the premise, reader promise, argument arc, source map, chapter thesis chain, tone, or editorial constraints are absent, materially disputed, or need restructuring. It ends at the storyline owner-review gate.
- `materialize-book`: use when a current approved storyline exists and the task is chapter planning, manuscript materialization, source/style review, publication proof, or export handoff. It begins at `chapter-production-planning` and must not silently invent a replacement storyline.

For a new end-to-end book request, run `shape-storyline` first, obtain the owner decision, then invoke `materialize-book` with the approved storyline refs. For a bounded revision, enter the action that owns the highest unresolved layer rather than patching local prose by default.

## Default Workflow

1. Shape or load the current storyline, primary reader promise, author/source stance, evidence map, chapter thesis chain, and owner questions.
2. Convert approved storyline refs into chapter task cards, reader-entry plans, target extents, figure/table obligations, source refs, and style constraints.
3. Materialize substantial manuscript body in author-facing Markdown. Scripts may assemble, validate, and export, but must not hide manuscript prose in code or JSON literals.
4. Review source/claim integrity, reader/style consistency, chapter continuity, figures, tables, captions, and higher-level structural defects before proof/export claims.
5. Keep `review_pdf`, `publication_proof`, and `final_export` distinct. Publication proof requires a real typesetting backend plus rendered-page evidence; final export additionally requires owner/export acceptance.
6. Route focused work to the relevant professional Skill: `bookforge-story-style-architect`, `bookforge-chapter-author`, `bookforge-source-reference-reviewer`, `bookforge-meta-reviewer`, or `bookforge-publication-memory-curator`.

## Quality And Hard Stops

- Treat any readable outline, manuscript fragment, review finding, source gap, negative result, failed attempt, or diagnostic as valid route context for the next declared stage.
- Retry, independent-review, and repair limits are quality budgets. On exhaustion, preserve the best artifact or diagnostic, mark `completed_with_quality_debt`, and continue with publication/final-export/owner-accepted claims closed.
- Resolve serious critique at the highest owning layer: artifact target, storyline, outline, chapter function, evidence/model, publication design, local prose, or owner/source blocker.
- Keep material claims, figures, tables, captions, callouts, and case boxes bound to inspectable source/evidence/owner refs. Downgrade or mark unsupported claims instead of fabricating support.
- Only wrong-target identity/currentness, executor unavailability, permission/safety/authority boundaries, irreversible action, protected-material authorization, or an explicit human decision may hard-stop progress.

## Output Expectations

- Return the selected public action, current book/workspace and source refs, produced manuscript/review/proof artifacts, owner/human-gate refs, route-back refs, typed blockers, and remaining quality debt.
- Name artifact maturity accurately: exploratory architecture, chapter draft, whole-book preview, review PDF, publication proof, or final export.
- Keep owner-inspectable working, episodic, and semantic book-memory refs current without creating a private scheduler, queue, session store, or attempt ledger.
- For new final artwork, use OPL-hosted image generation and return exact bitmap/path/hash evidence; chat previews or placeholders cannot satisfy figure-ready or publication-proof claims.

## References

- `contracts/action_catalog.json`
- `agent/stages/manifest.json`
- `contracts/stage_quality_cycle_policy.json`
- `contracts/owner_receipt_contract.json`
- `agent/professional_skills/bookforge-story-style-architect/SKILL.md`
- `agent/professional_skills/bookforge-chapter-author/SKILL.md`
- `agent/professional_skills/bookforge-source-reference-reviewer/SKILL.md`
- `agent/professional_skills/bookforge-meta-reviewer/SKILL.md`
- `agent/professional_skills/bookforge-publication-memory-curator/SKILL.md`
