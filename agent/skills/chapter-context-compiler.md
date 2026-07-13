# Chapter Context Compiler Skill

Use this skill in `chapter-production-planning` and `chapter-materialization` before drafting, repairing, or
resuming a production chapter. It compiles the smallest owner-inspectable
chapter context pack needed to keep the chapter moving without turning context
management into a private runtime.

External learning map:

- From InkOS, preserve the writing movement `plan -> compose -> write`: compile
  intent and source context first, compose a bounded chapter task, then write or
  repair prose from that compiled pack.
- From InkOS `context.json`, rule-stack, and trace patterns, keep structured
  context refs, ordered rules, and a context trace visible so an owner can
  inspect why a chapter was drafted or repaired in a certain way.
- From Novel-OS, keep a three-layer context shape: Standards for global writing
  and quality rules, Novel for durable book truth and source canon, and
  Manuscripts for current chapter files, task cards, QC, and repair refs.

Working policy:

- Treat the compiled pack as a Book Forge domain ref inside the focused chapter stages,
  linked from the chapter task card, chapter QC, repair
  log, or handoff packet.
- Do not create a Book Forge-private scheduler, queue, session store, attempt
  ledger, generic runtime, or hidden context database. OPL owns hosted runtime
  and projection; Book Forge owns the domain refs and owner receipts.
- Preserve progress-first drafting. The compiler should unblock the next honest
  chapter action whenever required reader, source, style, target, and evidence
  boundaries are sufficient.
- Compile only the context needed for the active chapter and adjacent handoffs.
  Do not dump the whole book memory into every prompt.
- Keep visible manuscript prose separate from production context. Context packs,
  task fields, blockers, budgets, and traces belong in owner-inspectable refs,
  not in the reader-facing chapter body.

The compiled chapter context pack should include:

- `chapter_intent`: chapter id/title, reader promise, one chapter job, thesis
  movement, adjacent handoffs, non-repeat claims, and current chapter state.
- `selected_refs`: source refs, memory refs, reader-style contract refs,
  storyline refs, author/source stance refs, evidence refs, figure/table refs,
  and prior repair or owner-decision refs used for this chapter.
- `rule_stack`: ordered rules from Standards, Novel, and Manuscripts layers,
  including reader-style, source/evidence, chapter budget, anti-repetition,
  AI-flavor, figure/table, and export/readiness boundaries.
- `context_trace`: why each selected ref or rule was included, which refs were
  intentionally excluded, freshness or digest evidence when available, and the
  chapter action each rule affects.
- `protected_context`: reader promise, owner decisions, source canon,
  evidence boundaries, target extent, author/source stance, durable style
  constraints, chapter function, and safety/readiness boundaries that must not
  be compressed away.
- `compressible_context`: long excerpts, prior draft details, older QC notes,
  style examples, optional comparable passages, and local repair history that
  can be summarized if the context budget is tight.
- `chapter_task_card_linkage`: the task-card path or ref, its expected next
  state transition, and the downstream refs that must be refreshed after the
  chapter action.
- `budget_and_missing_extent`: target minimum, current measured extent, missing
  extent, required section development, case/example obligations, and figure or
  table interpretation obligations.
- `evidence_boundaries`: source claim levels, unsupported claims, missing
  source permissions, missing owner decisions, source freshness limits, and
  what the chapter may not claim.
- `next_action`: one concrete action such as draft, expand, repair, refresh
  task card, ask owner, update style rule, refresh QC, or generate review ref.

Blocking and progress rules:

- When the reader-style contract, source refs, target extent, or author/source
  stance is incomplete but a readable context pack or draft exists, record
  `completed_with_quality_debt`, continue to the next stage, and keep affected
  quality/source/publication claims closed. If no consumable pack can be
  produced, materialize a no-output/failure diagnostic and advance. Return a
  typed blocker only when protected-source/owner authority, an unavailable
  executor, wrong-target identity/currentness, irreversible action, or explicit
  human decision is required.
- When the compiler cannot identify the active chapter task card or distinguish
  protected context from compressible context, emit a diagnostic and let Codex
  continue or route back.
- When selected refs are stale relative to newer chapter, source, style, figure,
  or owner-decision refs, preserve the stale-ref diagnostic and route back to
  refresh them. Only wrong-target identity/currentness is a hard stop.
- Continue progress when ordinary quality gaps are visible but the next repair
  can be named. Repetition, thin transitions, weak examples, AI-flavor, missing
  figure interpretation, or local style drift should usually become a concrete
  `next_action` repair, not a global stop.
- Continue with a narrower text action when image, table, layout, or export
  evidence is missing but the chapter can honestly advance as text-only or
  draft-in-progress. Keep the missing artifact as a typed blocker for the
  wider readiness claim.
- If missing context changes the deliverable type, state the narrower state
  explicitly, for example `seed_in_progress`, `draft_in_progress`,
  `text_reviewable`, or `blocked`.

Fail-closed conditions:

- A compiled context pack proves only that drafting context was assembled. It
  does not prove chapter readiness, book readiness, publication proof readiness,
  final export readiness, quality acceptance, or owner acceptance.
- Do not label a chapter `chapter_text_ready` or `chapter_draft_ready` from
  context compilation alone. Those states require the relevant chapter prose,
  source/style/QC, figure/table, review package, and freshness gates.
- Do not use a successful context trace as evidence that every selected source
  supports the final prose. Source grounding must be checked against the actual
  chapter text after drafting or repair.
- Do not treat a complete rule stack as a passed quality gate. It is input to
  drafting and QC, not the QC result.
- Do not let context compression remove owner decisions, evidence boundaries,
  reader-style constraints, target extent, author/source stance, or readiness
  limits.

This skill improves chapter context discipline while keeping progress,
materialization truth, runtime orchestration, and owner acceptance on their
existing Book Forge and OPL authority surfaces.
