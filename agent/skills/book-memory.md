# Book Memory Skill

Use this skill inside `book-materialization` for long-form nonfiction projects that need continuity across chapters, cases, figures, tables, and source claims.

Working policy:

- Maintain book memory as domain artifact refs, not OPL runtime state. OPL may project memory refs, but the memory body belongs to OPL BookForge or the book workspace.
- Keep three memory layers:
  - `working_memory`: current chapter brief, current chapter draft, previous chapter summary, next chapter promise, local source refs, and unresolved review notes.
  - `episodic_memory`: already used cases, examples, anecdotes, figures, tables, chapter decisions, owner review comments, revisions made, and promises that must be paid off later.
  - `semantic_memory`: book premise, reader-style contract, terminology, central claims, source map, argument arc, repeated metaphors to avoid, and durable style rules.
- Refresh memory after every chapter-level checkpoint: `chapter_brief_ready`, `chapter_text_ready`, `chapter_draft_ready`, owner review, figure/table update, major style repair, or publication-proof pass.
- Use memory to prevent repeated arguments, drifting terminology, forgotten examples, duplicated cases, stale blockers, and chapter-to-chapter discontinuity.
- Keep memory concise and cited. A memory item should name the chapter/source/ref that supports it; unsupported conclusions stay in notes or blockers, not semantic memory.
- Feed memory into chapter context packs through explicit selected refs and traces. Do not dump the whole memory body into every chapter prompt, and do not let compression remove owner decisions, evidence boundaries, reader-style constraints, target extent, or source stance.
- Keep private source details and unpublished owner comments inside the book workspace memory refs. Do not leak them into generated public docs or OPL-generated interface descriptors.
- Treat memory updates as a quality operation, not a separate private scheduler. The selected executor updates memory refs during the existing BookForge stages and OPL records only stage receipts, refs, and blockers.

Required memory refs for book-length work:

- `book-memory/working.md` or equivalent structured ref for active chapter context.
- `book-memory/episodic.md` or equivalent structured ref for cases, examples, review notes, and chapter events.
- `book-memory/semantic.md` or equivalent structured ref for durable claims, terminology, reader-style, and source map.
- `book-memory/memory-qc.md` or equivalent report naming stale, contradictory, duplicated, or unsupported memory items.

This skill does not authorize memory acceptance, publication readiness, or owner approval. It keeps continuity evidence available for later drafting and QC.
