# OPL BookForge Evidence Packages

Owner: `opl-bookforge`
Purpose: `evidence_package_index`
State: `historical_evidence_index`
Machine boundary: Human-readable index for tracked evidence packages. Machine truth remains in the evidence JSON/receipts/artifacts themselves, `scripts/verify.sh`, OPL scaffold/interface validators, runtime receipts, owner receipts, and typed blockers.

This directory stores historical and support evidence for OPL BookForge. It is
not the active truth owner for current gaps, production readiness, publication
approval, final export readiness, hosted runtime parity, or owner acceptance.
Current status stays in `docs/status.md`; current gaps and next work stay in
`docs/active/bookforge-ideal-state-gap-plan.md`.

## Package Index

| Package | Role | Claim boundary |
| --- | --- | --- |
| `oma-agent-lab/` | OMA Agent Lab takeover, AI reviewer, external-suite self-evolution, candidate, and no-patch receipts. | Supports baseline/takeover evidence only; it does not prove book quality, production readiness, publication readiness, or owner acceptance. |
| `production-readiness/bookforge-real-book-pilot-2026-06-18/` | Historical short-book pilot with inputs, stage outputs, manuscript, figures, exports, rendered pages, quality receipts, owner blockers, and verifier tools. | Historical pilot evidence with owner blockers; it is not the current long-book materialization pattern and does not prove final production readiness, publication approval, or owner acceptance. |

## Reading Rule

Evidence leaves under this directory may include manuscript excerpts, stage
outputs, generated artifacts, historical receipts, or verifier tools. Read them
as package payloads, not as long-lived current governance documents. Durable
rules and current claims must fold back to the active plan, status, core docs,
contracts, agent pack files, validators, or owner receipts.
