# OPL Book Forge Status

Owner: `opl-bookforge`
Purpose: `current_status`
State: `active_truth`
Machine boundary: Human-readable status summary. Machine truth remains in contracts, agent pack files, OPL validator output, runtime receipts, evidence receipts, owner receipts, and typed blockers.

Current state: OPL standard structural baseline plus one historical real short-book pilot evidence pack with owner-gated production-readiness blocker.

Live Evidence deferred / functional structure first is the current Book Forge development rule. Functional and structural lanes may close first: OPL standard scaffold/interface shape, golden-path routing, stage pack refs, generated/hosted surface consumption, PDF/proof helper plumbing, revision-entrypoint routing, workspace artifact-lifecycle handoff refs, default-caller structural gates, and no-second-truth guards. Owner acceptance, real long-book project runs, final export acceptance, publication-proof visual acceptance, direct `opl-bookforge` runtime CLI / hosted artifact-handoff parity, physical delete authorization, and production-ready claims remain later evidence lanes. They must not block independent structural cleanup, and structural validation, OMA evidence, pilot exports, rendered pages, docs, or helper proof plumbing cannot replace them.

## Current Validated Surfaces

- OPL standard scaffold and generated interface descriptors validate through `scripts/verify.sh`.
- The stage pack exposes two primary stages, `storyline-architecture` and `book-materialization`, plus domain refs for revision routing, chapter context, source-claim integrity, style calibration, publication design, PDF proof gates, image asset receipts, and workspace lifecycle hygiene. The OPL golden path profile keeps `storyline-architecture` as the only ordinary default route; `book-materialization` remains the follow-on stage reached through storyline handoff or explicit stage selection, not a second default App/CLI entry.
- The PDF export helper uses real typesetting backends, distinguishes `review_pdf`, `publication_proof`, and `final_export`, scans Markdown image refs, checks figure asset manifest readiness, writes rendered-page machine-baseline inspection when requested, reads embedded fonts through `pdffonts` when available, scans rendered-page density and trailing whitespace, and fail-closes `publication_proof` / `final_export` claims when required proof evidence or machine QA fields are missing.
- Book Forge consumes OPL-owned dependency and workspace-lifecycle routes. It does not own OS/TeX package installation, OPL runtime, queue, attempt ledger, generated interface hosting, or app shell routing.
- `contracts/artifact_lifecycle_handoff.json` is now the machine-readable Book Forge handoff contract for OPL `workspace artifact-lifecycle` projections. The project hygiene helper reads it back as a repo-source structural gate, verifies the OPL-owned projection refs, Book Forge-owned authority boundary, readback command, and false-ready flags, and keeps dry-run/projection-clean/helper-clean states from counting as workspace apply, publication readiness, final export readiness, owner acceptance, or production readiness.
- `scripts/verify.sh` now runs the Book Forge source-byproduct hygiene guard before and after repo verification and sets `PYTHONDONTWRITEBYTECODE=1`, so ignored Python/cache/install residue such as `.venv`, `__pycache__`, `.pytest_cache`, `*.pyc`, `*.pyo`, `*.egg-info`, `dist`, `coverage`, and `node_modules` cannot be treated as clean source state. This is a source-structure guard only; it does not prove book delivery, publication readiness, or owner acceptance.
- `contracts/functional_privatization_audit.json` now declares bridge exit gates for generated wrapper handler targets, the domain handler target, and refs-only status/workbench projection. Fresh OPL default-caller readback for this repo observes no missing no-forbidden-write proof and observes typed-blocker refs for the physical-delete decision path, while keeping `physical_delete_authorized=false` and `default_caller_delete_ready=false`.

## Evidence Packages

OMA / Agent Lab evidence:

- Takeover suite: `docs/evidence/oma-agent-lab/agent-lab-takeover-suite.json`.
- Takeover receipt: `docs/evidence/oma-agent-lab/takeover-receipt.json`, status `testing_takeover_recorded`.
- Takeover learning candidate: `docs/evidence/oma-agent-lab/takeover-online-learning-candidate.json`, status `candidate_recorded_requires_explicit_gate`.
- Takeover mechanism patch proposal: `docs/evidence/oma-agent-lab/takeover-mechanism-patch-proposal.json`, status `proposal_recorded_requires_explicit_gate`.
- AI reviewer evaluation: `docs/evidence/oma-agent-lab/bookforge-ai-reviewer-evaluation.json`, verdict `baseline_ready_with_agent_lab_takeover_and_owner_gate`.
- External-suite improvement receipt: `docs/evidence/oma-agent-lab/external-suite-improvement/meta-agent-improvement-receipt.json`, status `external_suite_passed_no_mechanism_patch_required`.
- Target capability candidate: `docs/evidence/oma-agent-lab/external-suite-improvement/target-capability-improvement-candidate.json`, status `candidate_recorded_requires_target_owner_gate`.
- Developer patch work order: `docs/evidence/oma-agent-lab/external-suite-improvement/developer-patch-work-order.json`, status `no_patch_required`.

Real book pilot production-readiness evidence:

- Evidence root: `docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/`.
- Boundary: this pilot remains historical short-book evidence; it is not the current implementation pattern for book-length manuscript source management.
- Source corpus and owner brief: `inputs/`.
- Stage 1 outputs: `artifacts/stage_outputs/storyline-architecture/`, including storyline map, chapter thesis chain, style contract, stage manifest, and owner handoff.
- Stage 2 outputs: `artifacts/stage_outputs/book-materialization/`, including chapter draft bundle, illustration plan, table plan, style consistency report, AI-flavor revision report, layout QC report, stage manifest, and owner handoff.
- Manuscript and assets: `artifacts/manuscript/book.md`, `artifacts/figures/figure-01-storyline-arc.png`, and `artifacts/figures/figure-02-two-stage-route.png`.
- Exports: `exports/bookforge-pilot-book.html`, `exports/bookforge-pilot-book.docx`, `exports/bookforge-pilot-book.pdf`, and rendered page PNGs under `exports/rendered-pages/`.
- Local verification receipt: `quality/local-verification-receipt.json`, status `passed_with_owner_gate_blocker`; all required files present and nonempty, DOCX schema validation passed, DOCX has two media files, PDF rendered to five nonblank pages, AI-flavor scan is clean, style terms are present, and production-ready claim remains fail-closed.
- Visual inspection note: `quality/visual-render-inspection.md`.
- Owner blockers: `receipts/storyline-owner-blocker.json` and `receipts/book-owner-blocker.json`, both status `blocked_owner_acceptance_missing`.
- After-pilot OMA takeover receipt: `oma-takeover-after-pilot/takeover-receipt.json`, status `testing_takeover_recorded`.
- After-pilot OMA external-suite improvement receipt: `oma-external-suite-after-pilot/meta-agent-improvement-receipt.json`, status `external_suite_passed_no_mechanism_patch_required`.
- After-pilot developer patch work order: `oma-external-suite-after-pilot/developer-patch-work-order.json`, status `no_patch_required`.

External-learning and handoff provenance:

- Revision-routing learning record: `docs/history/external-learning/revision-routing-2026-06-20.md`.
- Kami-inspired publication-proof learning record: `docs/history/external-learning/kami-publication-proof-2026-06-20.md`.
- OPL base revision-routing transport reference: `docs/references/opl-base-revision-routing-handoff.md`.

## Claim Boundary

- Existing evidence proves a valid OPL standard scaffold, generated interface descriptors, single-default golden path structure, OMA Agent Lab baseline evidence, external-suite self-evolution evidence, and a historical short-book pilot with generated artifacts, exports, rendered pages, quality receipts, and owner blockers.
- Existing evidence does not prove real workspace artifact-lifecycle apply, final production readiness, publication approval, owner acceptance, direct `opl-bookforge` runtime CLI availability, hosted OPL artifact-handoff parity, physical delete authorization, default-caller delete readiness, or book-specific publication-proof visual acceptance.
- The historical pilot generator's prose-in-code pattern is superseded by the current Markdown-first, chapter-sharded materialization invariant. Keep the pilot as evidence, not as the current implementation pattern for book-length manuscript source management.

## Next Evidence Required

- Human owner receipt accepting the pilot topic, reader promise, manuscript quality, figure/table plan, DOCX/PDF layout, and publication intent.
- A real book project receipt from `runtime/native_helpers/bookforge_pdf_export.py` using a project-local publication design profile, resource-path-backed asset resolution, rendered-page refs, rendered-page inspection, and owner/export acceptance when the target is `final_export`.
- Fresh OPL dependency doctor readback for `bookforge-publication-proof` when making publication-proof or final-export claims.
- A real manuscript run that exercises `revision-entrypoint-router` with independent meta-review evidence, route-back or repair-plan refs, refreshed artifacts, and owner decisions.
- A real Book Forge workspace run that exercises OPL `workspace artifact-lifecycle --apply` against domain-owned `handoff/review-repair-transport.json` and refreshed downstream refs.
- A book-specific publication-proof visual inspection report covering front matter, chapter openings, dense body pages, figure/table pages, callouts, closing pages, and owner-directed design preferences.
- A real publication-proof run that exercises the Kami-inspired Book Forge proof refs: design token receipt, component inventory, font actual-load/readback, rendered-page QA, front matter/TOC cleanliness, page rhythm/density/orphan checks, material/asset coverage, and pre-ship proof review.
- Direct `opl-bookforge` runtime CLI or hosted OPL artifact-handoff parity evidence.
