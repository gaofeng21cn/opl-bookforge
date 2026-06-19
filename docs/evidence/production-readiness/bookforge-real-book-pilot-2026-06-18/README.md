# BookForge Real Book Pilot Evidence

Run id: `bookforge-real-book-pilot-2026-06-18`

This evidence pack runs OPL BookForge through a real short-book pilot using BookForge's own contracts and OMA evidence as source corpus.

Current design boundary:

- This pilot is historical short-book evidence.
- Its generator embedded prose in code for a bounded pilot; that pattern is superseded.
- Current BookForge materialization is Markdown-first and chapter-sharded: substantial prose belongs in per-chapter Markdown refs, while scripts only assemble, count, validate, export, and report.

Claim boundary:

- The pack may support: two-stage pilot run evidence, manuscript artifact evidence, figure/table planning evidence, quality gate evidence, export/render evidence after verification.
- The pack may not support: final production-ready claim, publication approval, owner acceptance, or hosted runtime parity.

Primary artifacts:

- Inputs: `inputs/`
- Stage 1 outputs: `artifacts/stage_outputs/storyline-architecture/`
- Stage 2 outputs: `artifacts/stage_outputs/book-materialization/`
- Manuscript: `artifacts/manuscript/book.md`
- Figures: `artifacts/figures/`
- Receipts and blockers: `receipts/`
- Exports: `exports/`
- Verification output: `quality/local-verification-receipt.json`
