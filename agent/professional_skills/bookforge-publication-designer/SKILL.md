---
name: bookforge-publication-designer
description: Use when OPL Book Forge must design or verify review PDF, publication proof, final export, figure/table layout, PDF evidence, and artifact-role boundaries.
---

# Book Forge Publication Designer

## Purpose

Move a manuscript from readable review output toward publication proof without confusing artifact roles. This skill lifts `agent/skills/publication-design.md` and the PDF/export parts of `book-production` into a Codex skill.

## Inputs

- Artifact target: `review_pdf`, `publication_proof`, or `final_export`.
- Manuscript refs, publication design profile, PDF/export receipt, figure asset manifest, table plan, resource paths, rendered pages, font/readback evidence, and owner/export receipts when present.
- Owner design preferences, comparable proof refs, or figure-style decisions.

## Outputs

- Publication design profile with page geometry, typography, captions, tables, case boxes/callouts, headers/footers, numbering, and inspection plan.
- Design tokens, template/component inventory, font actual-load/readback, rendered-page QA checklist, front matter/TOC policy, material/asset coverage, and pre-ship proof review.
- PDF export receipt boundary and typed blockers for missing proof/final-export evidence.

## Execution Rules

- Keep `review_pdf`, `publication_proof`, and `final_export` separate.
- Use real typesetting backends such as Pandoc/XeLaTeX, Quarto, Typst, or Paged.js through Book Forge-owned adapters. Do not hand-roll book PDFs with raster text drawing.
- A readable review PDF is not publication proof. Publication proof needs design profile, resource-path-backed assets, rendered-page inspection, and proof gates.
- Final export additionally requires owner/export acceptance.
- Missing proof tokens or font/rendered-page evidence blocks proof/export claims only; it does not block ordinary drafting or review-only PDFs.
- Figure style must be chosen consistently before proof when figure style is questioned.

## Stage Prompt Boundary

- Stage prompts name required artifact role and evidence refs; this skill owns design/proof gate method.
- Use this skill after text/source/style gates when the task claims proof/export quality, or earlier only to define proof expectations.
- This skill cannot create owner acceptance, publication approval, or final-export readiness without receipts.

## Blockers And Repair Targets

- `publication_design_profile_missing`: create design profile before proof claim.
- `font_readback_missing`: block proof/export claim until readback or accepted fallback inspection exists.
- `figure_asset_missing`: keep review text possible, block full chapter/proof readiness.
- `rendered_page_qa_missing`: run inspection before proof handoff.
- `front_matter_or_toc_polluted`: repair publication design/profile and source headings before proof claim.
- `owner_export_acceptance_missing`: block final export claim.
