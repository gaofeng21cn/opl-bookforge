# Chapter Runtime Skill

Use this skill inside `chapter-materialization` when a book-length manuscript should advance chapter by chapter with review, repair, and state feedback after each chapter.

Working policy:

- Treat chapter runtime as a Book Forge domain workflow pattern executed inside the existing OPL stage runtime. Do not create a private scheduler, queue, control plane, session store, or attempt ledger.
- Every production chapter should move through a visible package:
  - chapter context pack with selected refs, rule stack, protected/compressible context, and trace
  - chapter brief
  - reader-entry plan
  - source/evidence slice
  - target budget
  - figure/table requirements
  - chapter Markdown draft
  - chapter QC
  - repair log
  - memory update
  - review PDF refresh when eligible
- The active production queue must carry the inherited minimum extent, current measured extent, missing extent, next action, and blocker state for every required unit. Do not rely on a later whole-book metrics surprise to discover that all chapters are thin.
- The active chapter package must carry the chapter function contract: one job, new movement, adjacent handoffs, and non-repeat claims. A chapter that mainly restates an adjacent chapter's movement remains in repair, even if it meets the character budget.
- The chapter context pack must be refreshed before drafting, repair, or resume when source refs, memory refs, style rules, owner decisions, figure/table obligations, or target budgets changed since the last chapter action.
- Chapter QC should check concept-map placement, core-model usage, and case evidence level when the chapter uses recurring concepts, whole-book models, or major examples.
- Start with the earliest unfinished required unit. Do not continue later chapters when an earlier required preface, introduction, or chapter is below target unless the owner explicitly approves a non-contiguous exploration pass.
- Classify chapter states conservatively:
  - `not_started`: no usable chapter package.
  - `outline_only`: chapter idea or headings exist, but no reader-facing prose.
  - `seed_in_progress`: short material exists and is useful, but it is below the production target.
  - `draft_in_progress`: chapter prose is being expanded toward the target and still has known blockers.
  - `chapter_text_ready`: prose meets target and source/style gates, but required figures/tables or export checks may still block full readiness.
  - `chapter_draft_ready`: text, source, style, memory, figure/table, and review-package gates pass for this chapter.
  - `blocked`: a typed blocker prevents honest progress.
- After drafting, run chapter QC before marking the chapter ready. QC should cover target extent, chapter function, argument movement, reader-style alignment, concept-map fit, source grounding, case evidence level, core-model application, figure/table status, memory update, repeated claims, and AI-flavor patterns.
- If QC finds local problems, repair the chapter package before expanding other chapters. If QC finds a systemic drafting-pattern failure, update the reader-entry or style pattern before continuing the production queue.
- Run assembly, metrics, hygiene, and readiness checks sequentially after the chapter files they inspect have changed. A stale metrics report, hygiene report, review PDF receipt, or handoff ref older than the chapter/source files cannot support a readiness claim.
- When the book project is indexed by an OPL workspace, refresh `opl workspace artifact-lifecycle --apply` after chapter source refs, book-memory refs, figure manifests, review PDFs, metrics, hygiene reports, or other current output refs change. Chapter readiness claims may cite OPL refs-only lifecycle health, but OPL health does not replace Book Forge chapter QC or owner acceptance.
- If an owner-supplied reference version is stronger than the active chapter package, run reference absorption before the next chapter state transition. Apply accepted reference-derived repairs to the chapter task card, reader-entry plan, style engine, and QC report before calling the chapter `chapter_text_ready` or `chapter_draft_ready`.
- Keep repair logs as domain refs. A repair log should say what changed, why, which gate it addressed, and whether memory or downstream chapters need updates.
- Refresh cumulative owner-review PDFs only from contiguous ready/text-ready sequence from the start of the book. A later ready chapter cannot hide an earlier blocker.

This skill creates chapter-level operating discipline while leaving orchestration, lifecycle receipts, hosted interfaces, and attempt projection to OPL.
