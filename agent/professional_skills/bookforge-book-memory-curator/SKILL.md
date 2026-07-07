---
name: bookforge-book-memory-curator
description: Use when OPL Book Forge must curate working, episodic, and semantic book-memory refs for long-form continuity without taking memory acceptance, publication, or owner authority.
---

# Book Forge Book Memory Curator

## Purpose

Maintain owner-inspectable book memory for long-form nonfiction continuity. This skill is the professional skill form of `agent/skills/book-memory.md` and supports chapter drafting, review, repair, style, source, and proof passes without creating a private runtime or second truth source.

## Inputs

- Working, episodic, semantic, and memory-QC refs such as `book-memory/working.md`, `book-memory/episodic.md`, `book-memory/semantic.md`, and `book-memory/memory-qc.md`.
- Chapter task cards, chapter context packs, chapter briefs, drafts, repair logs, QC reports, owner comments, source refs, figure/table manifests, reader-style contract, style refs, and claim/evidence refs.
- OPL workspace artifact-lifecycle readback when the project is OPL-indexed.

## Outputs

- Refreshed working memory for active chapter context, previous chapter summary, next chapter promise, local source refs, and unresolved review notes.
- Refreshed episodic memory for used cases, examples, anecdotes, figures, tables, chapter decisions, owner comments, revisions, and promises to repay later.
- Refreshed semantic memory for book premise, reader-style contract, terminology, central claims, source map, argument arc, repeated metaphors to avoid, durable style rules, and evidence rules.
- Memory-QC report naming stale, contradictory, duplicated, unsupported, private, or over-broad memory items.
- Selected-memory trace for chapter context packs that explains why each memory ref was included or excluded.

## Execution Rules

- Keep book memory as Book Forge or book-workspace artifact refs. OPL may project memory refs and lifecycle state, but it must not contain, replace, accept, or reject the memory body.
- Refresh memory after `chapter_brief_ready`, `chapter_text_ready`, `chapter_draft_ready`, owner review, figure/table update, major style repair, publication-proof pass, or any repair that changes durable reader, source, style, claim, or continuity rules.
- Keep memory concise and cited. Each durable memory item names the chapter, source, owner decision, review, or artifact ref that supports it.
- Do not promote unsupported conclusions into semantic memory. Keep them in notes, blocker refs, source-action lists, or memory-QC findings.
- Feed chapter context packs through explicit selected refs and traces. Do not dump the whole memory body into every chapter prompt.
- Protect owner decisions, evidence boundaries, reader-style constraints, target extent, author/source stance, and private source details from lossy compression.
- Keep private source details and unpublished owner comments inside authorized book-workspace memory refs; do not leak them into public docs, generated descriptors, or OPL projection surfaces.
- Treat memory updates as a quality operation inside existing Book Forge stages, not a private scheduler, queue, session store, provider memory, attempt ledger, or hidden note system.
- For OPL-indexed workspaces, refresh and inspect `opl workspace artifact-lifecycle` after memory ref changes; cite lifecycle/readback refs only for ref existence and freshness, not memory truth or acceptance.

## Stage Prompt Boundary

- Stage prompts name required memory refs and accepted handoff shapes; this skill carries the continuity and memory-curation method.
- `bookforge-chapter-author`, `bookforge-style-editor`, `bookforge-source-claim-reviewer`, `bookforge-meta-reviewer`, and `bookforge-publication-designer` consume memory refs through selected traces instead of owning the memory method.
- This skill does not authorize memory acceptance, owner approval, manuscript quality, publication proof, final export, domain readiness, or production readiness.

## Blockers And Repair Targets

- `working_memory_missing`: create or locate the active chapter memory ref before chapter drafting or repair.
- `episodic_memory_missing`: create or locate prior chapter, review, case, owner-comment, and repair history before cross-chapter continuity claims.
- `semantic_memory_missing`: create or locate durable premise, reader-style, terminology, source-map, style-rule, and evidence-rule refs before broad rewrite or style claims.
- `memory_qc_missing`: run memory QC before claiming continuity-sensitive handoff.
- `memory_source_unsupported`: demote or block unsupported memory items instead of using them as durable truth.
- `private_memory_leakage`: remove public/projection leakage and update memory-QC and anti-leakage refs.
- `opl_lifecycle_readback_missing`: refresh OPL artifact-lifecycle projection when making OPL-indexed freshness claims.
