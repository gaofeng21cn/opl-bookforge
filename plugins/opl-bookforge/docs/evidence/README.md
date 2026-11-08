# OPL BookForge Evidence Packages

Owner: `opl-bookforge`
Purpose: `evidence_package_index`
State: `historical_evidence_index`
Machine boundary: Human-readable index for tracked evidence packages. Machine truth remains in the evidence JSON/receipts/artifacts themselves, `scripts/verify.sh`, OPL scaffold/interface validators, runtime receipts, owner receipts, and typed blockers.

This directory stores historical and support evidence for OPL BookForge. It is
not the active truth owner for current gaps, production readiness, publication
approval, final export readiness, hosted runtime parity, or owner acceptance.
Current status and unproven acceptance claims stay in `docs/status.md`.
External source attribution stays in `docs/history/README.md`. Completed
implementation narratives and audit seeds belong in Git history, not an
evidence package merely because they were labeled historical.

## SSOT And Foldback

This README is the evidence-package navigation SSOT. It owns package names,
roles, and claim boundaries. It does not own current status, active gaps,
production-readiness tasks, publication approval, final-export acceptance,
hosted runtime parity, or owner acceptance.

Package-level README files are package manifests and may carry lifecycle
headers. Markdown leaves under package `inputs/`, `artifacts/`, `stage_outputs/`,
`quality/`, `receipts/`, or verifier/export folders are evidence payloads, not
active docs truth owners. Do not rewrite those payload bodies just to add
lifecycle headers; promote a payload into a governed document only after a new
semantic owner is chosen.

Retention requires an inspectable relationship to a source, artifact, or receipt.
The pilot inputs, manuscript, figures, stage manifests, exported bytes, rendered
pages, and original generation/export/verification source reconstruct its
recorded output. Its owner blockers and verification receipts remain referenced
by `contracts/production_acceptance/bookforge-production-acceptance.json`.
The original OMA suites, critiques, candidates, and receipts preserve the
design/evaluation inputs and result lineage, including the two baseline refs in
`contracts/live_stage_run_progress_evidence.json`. They are historical outputs
of the retired OMA protocol, not executable work orders, migration tasks, or
current Foundry acceptance. A pending candidate gate is not treated as accepted.

Add or change rows here only when a tracked evidence package is introduced,
retired, or reclassified. Do not copy package file lists, verifier transcripts,
rendered-page paths, receipt ids, or pilot closeout logs into `docs/status.md`
or an implementation plan. Durable rules and current claims fold back to status,
core docs, contracts, agent pack files, validators, runtime
receipts, owner receipts, or typed blockers; package payload detail stays in
the package directory or git history.

## Package Index

| Package | Role | Claim boundary |
| --- | --- | --- |
| `oma-agent-lab/` | OMA Agent Lab takeover, AI reviewer, external-suite self-evolution, candidate, no-patch receipts, and immutable superseded-topology receipts under `provenance/`. | Supports baseline/takeover and historical topology provenance only; it does not define active Stage topology or prove book quality, production readiness, publication readiness, or owner acceptance. |
| `production-readiness/bookforge-real-book-pilot-2026-06-18/` | Historical short-book pilot package manifest plus evidence payloads: inputs, stage outputs, manuscript, figures, exports, rendered pages, quality receipts, owner blockers, and verifier tools. | Historical pilot evidence with owner blockers; the `production-readiness/` path is an archive classification, not a ready claim. It is not the current long-book materialization pattern and does not prove final production readiness, publication approval, final export acceptance, hosted runtime parity, or owner acceptance. |

## Reading Rule

Evidence leaves under this directory may include manuscript excerpts, stage
outputs, generated artifacts, historical receipts, or verifier tools. Read them
as package payloads, not as long-lived current governance documents. Durable
rules and current claims must fold back to status, core docs,
contracts, agent pack files, validators, or owner receipts.
