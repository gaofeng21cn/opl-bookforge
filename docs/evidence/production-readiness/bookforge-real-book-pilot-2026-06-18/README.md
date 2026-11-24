# BookForge Real Book Pilot Evidence

Owner: `opl-bookforge`
Purpose: `evidence_package_manifest`
State: `historical_pilot_evidence_manifest`
Machine boundary: Human-readable manifest and claim boundary for this tracked evidence package. Machine truth remains in payload artifacts, receipts, verifier output, owner receipts, typed blockers, repo validators, and runtime/readback evidence.

Run id: `bookforge-real-book-pilot-2026-06-18`

This evidence package records a historical OPL BookForge short-book pilot using BookForge's own contracts and OMA evidence as source corpus.

Lifecycle boundary:

- This README is the package manifest and claim-boundary owner.
- Markdown leaves under `inputs/`, `artifacts/manuscript/`, `artifacts/stage_outputs/`, and `quality/` are evidence payload bodies, not active docs truth owners.
- Do not rewrite payload bodies to add lifecycle headers unless a future governance pass promotes a specific payload into a long-lived document with its own semantic owner.
- The `production-readiness/` path is an archive classification, not a production-ready, owner-accepted, publication-approved, final-export-ready, or hosted-runtime-ready claim.

Current design boundary:

- This pilot is historical short-book evidence.
- Its generator embedded prose in code for a bounded pilot; that pattern is superseded.
- Current BookForge materialization is Markdown-first and chapter-sharded: substantial prose belongs in per-chapter Markdown refs, while scripts only assemble, count, validate, export, and report.

The former pilot `tools/` scripts, intermediate manuscript/stage prose, and
unreferenced export files are retained in Git history at commit
`aff9cc8cf2fbe2e67a3b6ca164cc0e1f638fc4cd` rather than in the active working
tree; they are not supported current commands or governance docs.

Claim boundary:

- The package may support: historical two-stage pilot run provenance, owner-blocker lineage, and SHA-256-bound figure/rendered-page verification after verification.
- The package may not support: current production-ready claim, publication approval, final export acceptance, owner acceptance, or hosted runtime parity.

Retained contract- and hash-bound artifacts:

- SHA-256-bound figures: `artifacts/figures/` (`figure-01-storyline-arc.png`, `figure-02-two-stage-route.png`)
- Receipts and blockers: `receipts/` (`storyline-owner-blocker.json`, `book-owner-blocker.json`, `production-readiness-closeout.json`)
- SHA-256-bound rendered pages: `exports/rendered-pages/` (`page-1.png`..`page-5.png`)
- Verification output: `quality/local-verification-receipt.json`
