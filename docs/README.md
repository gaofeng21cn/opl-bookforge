# OPL Book Forge Docs Guide

Owner: `opl-bookforge`
Purpose: `docs_index`
State: `active_index`
Machine boundary: Human-readable navigation. Machine truth remains in contracts, agent pack files, OPL validator output, OMA Agent Lab evidence, pilot evidence, future runtime receipts, owner receipts, and typed blockers.

This directory is the documentation entry for the OPL Book Forge domain agent package.

## Current Reading Order

1. [Project](./project.md)
2. [Status](./status.md)
3. [Active gap plan](./active/bookforge-ideal-state-gap-plan.md)
4. [Architecture](./architecture.md)
5. [Invariants](./invariants.md)
6. [Decisions](./decisions.md)
7. [Docs portfolio governance](./docs_portfolio_consolidation.md)
8. [OPL base revision routing handoff](./references/opl-base-revision-routing-handoff.md)
9. [Evidence package index](./evidence/README.md)
10. [History index](./history/README.md)
11. [Process history index](./history/process/README.md)

## Evidence Surfaces

- Fast policy validation: `scripts/verify.sh`.
- OPL structural readback: `scripts/verify.sh structural`.
- Native-helper and adapter validation: `scripts/verify.sh helpers`.
- Proof-backend E2E: `scripts/verify.sh pdf`.
- Deduplicated integration union: `scripts/verify.sh full`.
- Helper executable readback: `opl pack native-helper probe --descriptor runtime/native_helpers/bookforge_pdf_export.native-helper-probe.json --json`.
- Evidence package index: `docs/evidence/README.md`.
- Pilot verifier: `python3 docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/tools/verify_pilot.py`.
- Revision routing design: `agent/skills/revision-entrypoint-router.md`, `docs/history/external-learning/revision-routing-2026-06-20.md`, and `docs/references/opl-base-revision-routing-handoff.md`.
- Kami-inspired publication proof design: `agent/skills/publication-design.md`, `agent/quality_gates/publication-proof-handoff-quality-gate.md`, and `docs/history/external-learning/kami-publication-proof-2026-06-20.md`.
- Process and historical provenance: `docs/history/README.md` and
  `docs/history/process/README.md`.

## Optional Support Directories

This docs tree intentionally has no `docs/runtime/` support directory today.
Use the executable helper paths under `runtime/native_helpers/` and the current
core docs above; do not link to a nonexistent runtime README. Create a runtime
docs README only when Book Forge has durable runtime-support prose with its own
owner, purpose, state, and machine boundary.

## Claim Boundary

Current evidence supports OPL-standard scaffold validity, generated interface descriptors, OMA Agent Lab takeover evidence, external-suite self-evolution evidence, and a real short-book pilot with DOCX/HTML/PDF exports and render checks.

Current evidence does not support production-ready book-writing claims, publication approval, owner acceptance, or hosted runtime parity. Those require human owner receipt plus live OPL StageRun or hosted artifact-handoff parity evidence.

Kami-inspired publication proof rules are Book Forge-owned domain contracts plus helper machine-baseline proof plumbing. They do not import Kami's runtime or visual identity, and they still do not replace human publication-design review, final-export acceptance, or owner proof readiness evidence.
