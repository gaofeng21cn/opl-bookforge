# OPL Book Forge Docs Guide

Owner: `opl-bookforge`
Purpose: `docs_index`
State: `active_index`
Machine boundary: Human-readable navigation and lifecycle map. Machine truth remains in contracts, agent pack files, source, tests, OPL validator/readback output, runtime receipts, owner receipts, and typed blockers.

## Reading Order

1. [Project](./project.md): product role and scope.
2. [Status](./status.md): concise current implementation and claim boundary.
3. [Active Truth plan](./active/bookforge-ideal-state-gap-plan.md): current state, open gaps, and next executable prompt.
4. [Architecture](./architecture.md): ownership and protocol flow.
5. [Invariants](./invariants.md): hard domain and authority constraints.
6. [Decisions](./decisions.md): durable accepted design decisions.
7. [OPL revision-routing handoff](./references/opl-base-revision-routing-handoff.md): current cross-repo support boundary.
8. [Evidence index](./evidence/README.md): tracked package roles and claim limits.
9. [History index](./history/README.md): external-learning and retirement provenance.

## Single-Owner Map

| Theme | Owner surface |
| --- | --- |
| Product role and scope | `docs/project.md` |
| Current implementation and claim boundary | `docs/status.md` |
| Current state, open gaps, next prompt, coverage ledger | `docs/active/bookforge-ideal-state-gap-plan.md` |
| Ownership and stage architecture | `docs/architecture.md` |
| Hard rules | `docs/invariants.md` |
| Accepted design choices | `docs/decisions.md` |
| Evidence package names, roles, and claim boundaries | `docs/evidence/README.md` |
| Historical provenance | `docs/history/README.md` |

Do not add empty taxonomy directories. Create a new `public/`, `product/`, `runtime/`, `delivery/`, `source/`, `policies/`, or `specs/` area only when durable content has a distinct owner, purpose, state, and machine boundary.

## Evidence Payload Rule

Package READMEs under `docs/evidence/**` are manifests. Markdown leaves under package `inputs/`, `artifacts/`, `stage_outputs/`, `quality/`, `receipts/`, verifier, or export directories are historical evidence bodies. They do not need governance headers and must not be rewritten merely to satisfy doctor output. Promote one only after choosing a new semantic owner.

The current short-book pilot deliberately retains its old two-stage vocabulary and now-missing source paths because those bytes describe the historical run. Current topology and claim truth stay in status, the Active Truth plan, contracts, and agent files.

## Verification And Claims

Use `scripts/verify.sh` for the fast policy lane and `scripts/verify.sh full` for the full repo/OPL structural union. `helpers`, `pdf`, and `full-local` are explicit heavier lanes described in [Status](./status.md).

No documentation, validator, helper, evidence package, or rendered page can by itself establish live execution, book quality, publication approval, final-export readiness, hosted parity, owner acceptance, release, or production readiness.
