---
name: opl-bookforge
description: Use when Codex needs OPL Book Forge to shape or materially produce a book-length nonfiction work, including storyline architecture, reader/style design, chapter planning and drafting, source/claim review, figures and tables, publication proof, or export handoff. Do not use for an isolated article, research paper, grant, slide deck, generic document formatting, or to claim publication/final-export approval without owner evidence.
---

# OPL Book Forge

This is the canonical Book Forge routing Skill. OPL materializes it into the Codex plugin carrier; repo-internal professional Skills provide focused methods and do not replace this entry.

All source paths below resolve from the installed plugin root, two directories above this Skill. The carrier includes the domain descriptor, professional Skills, contracts, and publishing helpers; use that root as `<agent-root>` without requiring a source checkout. OPL Framework remains the external runtime and Python support dependency.

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
   Follow the owner-approved style contract and supplied samples for narrative form; do not introduce teaching scenarios or other devices from a generic textbook template. State evidence scope through study population, design, endpoint, validation stage, and intended use, and remove preventive disclaimers and generalized caveats from reader-facing prose.
5. When the owner requests a Word and PDF delivery, use `runtime/native_helpers/bookforge_publication_bundle.py` under `materialize-book` / `publication-proof-handoff` and `contracts/publication_bundle_contract.json`: generate both files from the same Markdown source, metadata, figures, tables, and design profile, then write a bundle manifest with SHA-256, page counts, font readback, content-parity checks, and rendered-page refs. The fast path shortens orchestration; it does not skip source, asset, font, or page-render checks.
6. Keep `review_pdf`, `publication_proof`, `publication_bundle`, and `final_export` distinct. A publication bundle can be ready for owner review after both formats pass the shared-source and rendered-page checks; publication proof still requires a real typesetting backend and design evidence, and final export additionally requires owner/export acceptance.
7. Route focused work to the relevant professional Skill: `bookforge-story-style-architect`, `bookforge-chapter-author`, `bookforge-source-reference-reviewer`, `bookforge-meta-reviewer`, or `bookforge-publication-memory-curator`.

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

## Knowledge Sources And Book Continuity

Both public actions require the exact `book_id` registered as `project_id` in
`workspace_index.json#/projects`. Framework resolves the book root from this
inventory; a workspace path alone cannot select a book or its private knowledge.

Use the Framework knowledge lifecycle v2. `scope` distinguishes product,
owner/team, topic, and project knowledge; `content_kind` independently identifies
mechanism, policy, state, or decision. Reusable product policies are indexed by
`contracts/durable_knowledge_catalog.json`. The user's writing preferences and
long-lived topic knowledge remain in their chosen knowledge source, including an
existing Obsidian vault. Book-specific sources may remain in the book directory.
Without a separate personal library, ordinary workspace Markdown is the source.
Bind those sources through Framework's `shared/memory/knowledge-bindings.json`,
using the shared source registry schema; do not create a second editable copy or
a Book Forge-specific source registry format.

The hosted StageRun freezes the selected source versions for producer, reviewer,
and repair roles. Direct Skill use prepares and reads the same Framework
snapshot. Cite knowledge identities, scopes, content kinds, and digests, and
record unavailable or stale knowledge. Required source/owner constraints block
only the dependent action; optional context gaps remain visible quality debt.
Working, episodic, and semantic book-memory views organize editorial continuity;
they are not additional source ownership layers. Derived summaries retain their
source identities and revisions and are refreshed when their sources change.

Updates are proposals until the authorized user, topic, or project owner accepts
their evidence and scope. Apply accepted changes to the unique original through
the shared writer, preserving concurrent edits and a writeback receipt. A new
book lesson does not automatically become a personal policy or product rule.
Recheck critical permissions and owner constraints before publication or export.

For a direct Skill run, resolve `<book-root>` from the registered `book_id`, then
use the current stage and action with a new private binding path:

```text
opl knowledge prepare --repo <agent-root> --domain opl-bookforge --stage <stage-id> --task-intent <action-id> --workspace <workspace-root> --project <book-root> --output <new-binding.json> --json
opl knowledge read-context --binding <new-binding.json> --json
opl knowledge revalidate --binding <new-binding.json> --for-action --json
```

The final command is the pre-action check. Knowledge writeback uses the shared
`knowledge propose`, `knowledge review`, and `knowledge apply` lifecycle; reviewed
edits made directly in the original use `knowledge review-source`.
