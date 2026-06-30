# OPL Book Forge Docs Portfolio Governance

Owner: `opl-bookforge`
Purpose: `docs_lifecycle_governance`
State: `active_support`
Machine boundary: Human-readable lifecycle map. Machine truth remains in
contracts, agent pack files, OPL validator output, evidence receipts, runtime
receipts, owner receipts, typed blockers, source, and repo-native verification.

## Current Conclusion

`opl-bookforge` is a standard OPL domain-agent package. Its docs stay lighter
than OPL/MAS/MAG/RCA canonical repositories, but every long-lived document must
still make owner, purpose, state, and machine boundary clear.

Do not create empty canonical taxonomy directories for alignment. Add
`public/`, `product/`, `runtime/`, `delivery/`, `source/`, `policies`, or
`specs` only when Book Forge has durable material with a clear owner and
machine boundary.

## Directory Responsibilities

| Path | Role | Boundary |
| --- | --- | --- |
| `docs/README.md` | Documentation entry and reading order | Navigation only |
| `docs/project.md`, `docs/status.md`, `docs/architecture.md`, `docs/invariants.md`, `docs/decisions.md` | Core current docs | Human-readable truth; executable truth stays in contracts, agent pack files, validators, source, and receipts |
| `docs/active/` | Current gap plan, next baton, and completion boundary | Not a proof ledger and not owner acceptance |
| `docs/references/` | Current support references such as OPL base handoff | Support only; current state folds back to core docs and contracts |
| `docs/evidence/` | Historical and support evidence packages | Evidence payloads only; not active truth, publication approval, production readiness, or owner acceptance |
| `docs/history/` | External learning, process provenance, and historical context | Historical only; durable conclusions must fold back to current owners |
| `docs/history/process/` | Compressed process-history index | Topic-level provenance only; not an active plan, proof ledger, verifier transcript index, or ready-claim surface |

## Evidence Package Rule

Markdown under `docs/evidence/**` can be package payload: inputs, manuscripts,
stage outputs, visual inspection notes, or verifier instructions. Package
payloads do not need the same front-matter discipline as long-lived governance
docs, but their claim boundary must be indexed by `docs/evidence/README.md`.

Current gaps and next work stay in
`docs/active/bookforge-ideal-state-gap-plan.md`; current status stays in
`docs/status.md`.

Process-history and external-learning provenance stay under
`docs/history/README.md` and `docs/history/process/README.md`. Do not append
dated tranche logs, package file lists, verifier transcripts, rendered-page
paths, worktree closeouts, or pilot proof ledgers to active docs.
