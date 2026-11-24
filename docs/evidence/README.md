# OPL BookForge Evidence Packages

Owner: `opl-bookforge`
Purpose: `evidence_package_index`
State: `historical_evidence_index`
Machine boundary: Human-readable index for tracked evidence packages. Machine truth remains in the evidence JSON/receipts/artifacts themselves, `scripts/verify.sh`, OPL scaffold/interface validators, runtime receipts, owner receipts, and typed blockers.

This directory stores historical and support evidence for OPL BookForge. It is
not the active truth owner for current gaps, production readiness, publication
approval, final export readiness, hosted runtime parity, or owner acceptance.
Current status and unproven acceptance claims stay in `docs/status.md`.
External source attribution stays in `docs/references/design-source-attribution.md`. Completed
implementation narratives and unreferenced historical intermediates remain in
Git history (pre-cleanup revision `aff9cc8cf2fbe2e67a3b6ca164cc0e1f638fc4cd`).

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

Retention is bounded to active contract- and hash-bound evidence artifacts:
the historical pilot's typed owner blockers, verification/closeout receipts,
and SHA-256-bound rendered figures/pages referenced by
`contracts/production_acceptance/bookforge-production-acceptance.json`, plus the
two baseline topology receipts referenced by
`contracts/live_stage_run_progress_evidence.json`. Intermediate short-book
pilot prose/exports, obsolete OMA takeover/improvement files, and unsupported
pilot scripts live in Git history at `aff9cc8cf2fbe2e67a3b6ca164cc0e1f638fc4cd`.

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
| `oma-agent-lab/` | Immutable superseded-topology receipts under `provenance/` referenced by `contracts/live_stage_run_progress_evidence.json`. | Supports historical topology provenance only; it does not define active Stage topology or prove book quality, production readiness, publication readiness, or owner acceptance. |
| `production-readiness/bookforge-real-book-pilot-2026-06-18/` | Historical short-book pilot manifest, owner blockers, closeout/local-verification receipts, and SHA-256-bound figures and rendered pages. | Historical pilot evidence with owner blockers; the `production-readiness/` path is an archive classification, not a ready claim. It is not the current long-book materialization pattern and does not prove final production readiness, publication approval, final export acceptance, hosted runtime parity, or owner acceptance. |

## Reading Rule

Read retained JSON receipts and SHA-bound images under this directory as frozen
evidence payloads, not as long-lived governance rules or active runtime commands.
Durable rules and current claims belong in status, core docs, contracts, agent
pack files, validators, or owner receipts.
