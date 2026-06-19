# OPL BookForge Docs Guide

Owner: `opl-bookforge`
Purpose: `docs_index`
State: `active_index`
Machine boundary: Human-readable navigation. Machine truth remains in contracts, agent pack files, OPL validator output, OMA Agent Lab evidence, pilot evidence, future runtime receipts, owner receipts, and typed blockers.

This directory is the documentation entry for the OPL BookForge domain agent package.

## Current Reading Order

1. [Project](./project.md)
2. [Status](./status.md)
3. [Architecture](./architecture.md)
4. [Invariants](./invariants.md)
5. [Decisions](./decisions.md)
6. OMA Agent Lab evidence under [evidence/oma-agent-lab](./evidence/oma-agent-lab/)
7. Real pilot evidence under [evidence/production-readiness/bookforge-real-book-pilot-2026-06-18](./evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/)

## Evidence Surfaces

- Structural validation: `scripts/verify.sh`.
- PDF backend helper doctor: `python3 runtime/native_helpers/bookforge_pdf_export.py --doctor`.
- OMA baseline takeover and self-evolution evidence: `docs/evidence/oma-agent-lab/`.
- Real short-book pilot evidence: `docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/`.
- Pilot verifier: `python3 docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/tools/verify_pilot.py`.

## Claim Boundary

Current evidence supports OPL-standard scaffold validity, generated interface descriptors, OMA Agent Lab takeover evidence, external-suite self-evolution evidence, and a real short-book pilot with DOCX/HTML/PDF exports and render checks.

Current evidence does not support production-ready book-writing claims, publication approval, owner acceptance, or hosted runtime parity. Those require human owner receipt and direct `opl-bookforge` runtime CLI or hosted artifact-handoff parity evidence.
