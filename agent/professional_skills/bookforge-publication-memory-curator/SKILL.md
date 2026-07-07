---
name: bookforge-publication-memory-curator
description: Use when OPL Book Forge must curate long-form book memory or design review/proof/export artifacts while preserving publication, memory, and owner authority boundaries.
---

# Book Forge Publication Memory Curator

## Purpose

Maintain owner-inspectable book memory and publication-facing artifact discipline without creating a private runtime or export authority. This workflow-level skill replaces the separate publication designer and book-memory curator entries.

## Inputs

- Artifact target: `review_pdf`, `publication_proof`, or `final_export`.
- Manuscript refs, chapter task cards, chapter context packs, repair logs, QC reports, owner comments, style refs, claim/evidence refs, figure/table manifests, and publication design refs.
- Working, episodic, semantic, and memory-QC refs such as `book-memory/working.md`, `book-memory/episodic.md`, `book-memory/semantic.md`, and `book-memory/memory-qc.md`.
- PDF/export receipt, rendered pages, font/readback evidence, resource paths, owner/export receipts, and OPL workspace artifact-lifecycle readback when the project is OPL-indexed.

## Outputs

- Refreshed working, episodic, and semantic memory refs plus memory-QC report and selected-memory trace.
- Publication design profile with page geometry, typography, captions, tables, case boxes/callouts, headers/footers, numbering, and inspection plan.
- Design tokens, template/component inventory, font actual-load/readback, rendered-page QA checklist, front matter/TOC policy, material/asset coverage, note display policy, and pre-ship proof review.
- PDF export receipt boundary and typed blockers for missing memory, proof, final-export, owner, asset, or lifecycle evidence.

## Execution Rules

- Keep book memory as Book Forge or book-workspace artifact refs. OPL may project memory refs and lifecycle state, but it must not contain, accept, reject, or replace memory bodies.
- Refresh memory after chapter readiness, owner review, figure/table updates, major style/source repair, publication-proof pass, or any repair that changes durable reader, source, style, claim, or continuity rules.
- Keep memory concise and cited. Do not promote unsupported conclusions into semantic memory.
- Feed chapter context packs through selected refs and traces; do not dump the whole memory body into every chapter prompt.
- Keep `review_pdf`, `publication_proof`, and `final_export` separate.
- Use real typesetting backends such as Pandoc/XeLaTeX, Quarto, Typst, or Paged.js through Book Forge-owned adapters. Do not hand-roll book PDFs with raster text drawing.
- Missing proof tokens or font/rendered-page evidence blocks proof/export claims only; it does not block ordinary drafting or review-only PDFs.
- Final export additionally requires owner/export acceptance.
- Treat real photos, generated figures, diagrams, tables, case boxes, and reviewer callouts as different artifact classes.

## Stage Prompt Boundary

- Stage prompts name required memory and artifact refs; this skill owns continuity curation and publication/proof gate method.
- Use after text/source/style gates when the task claims proof/export quality, or earlier to define proof expectations or refresh continuity refs.
- This skill cannot create owner acceptance, publication approval, final-export readiness, domain readiness, production readiness, or memory acceptance. It may only cite existing owner/export/memory authority refs and return blockers when they are missing.

## Blockers And Repair Targets

- `working_memory_missing`: create or locate active chapter memory before chapter drafting or repair.
- `episodic_memory_missing`: create or locate prior chapter, review, case, owner-comment, and repair history before continuity claims.
- `semantic_memory_missing`: create or locate durable premise, reader-style, terminology, source-map, style-rule, and evidence-rule refs before broad rewrite or style claims.
- `memory_qc_missing`: run memory QC before continuity-sensitive handoff.
- `memory_source_unsupported`: demote or block unsupported memory items.
- `private_memory_leakage`: remove public/projection leakage and update memory-QC and anti-leakage refs.
- `publication_design_profile_missing`: create design profile before proof claim.
- `font_readback_missing`: block proof/export claim until readback or accepted fallback inspection exists.
- `figure_asset_missing`: keep review text possible, block full chapter/proof readiness.
- `photo_asset_boundary_missing`: block proof/export claims until photo refs, captions, and public/rights boundary are recorded.
- `rendered_page_qa_missing`: run inspection before proof handoff.
- `owner_export_acceptance_missing`: block final export claim.
