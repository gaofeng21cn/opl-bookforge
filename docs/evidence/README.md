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
Historical process foldback and external-learning provenance stay in
`docs/history/README.md` and `docs/history/process/README.md`; evidence package
payloads should not be copied there except as compressed topic-level
provenance.

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

Add or change rows here only when a tracked evidence package is introduced,
retired, or reclassified. Do not copy package file lists, verifier transcripts,
rendered-page paths, receipt ids, or pilot closeout logs into `docs/status.md`
or the active plan. Durable rules and current claims fold back to status,
the active plan, core docs, contracts, agent pack files, validators, runtime
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
rules and current claims must fold back to the active plan, status, core docs,
contracts, agent pack files, validators, or owner receipts.
