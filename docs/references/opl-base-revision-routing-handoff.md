# OPL Base Revision Routing Handoff

Owner: `opl-bookforge`
Purpose: `support_reference_opl_base_handoff`
State: `reference_landed_initial_opl_transport`
Machine boundary: Human-readable cross-repo handoff reference. Machine truth remains in BookForge contracts, OPL validator output, OPL source/tests, runtime receipts, owner receipts, and typed blockers.

## Problem

BookForge Meta Review can now discover that a manuscript should not be repaired from a sentence or chapter. Some findings require a route back to artifact target, storyline architecture, outline sequence, chapter function, evidence/model, publication design, or owner/source decisions.

The domain owns those semantics, but the OPL base should make the route easy to execute and inspect across agents.

## Landed Initial OPL Surface

The local OPL base checkout now has an initial refs-only workspace transport for this class of handoff:

- CLI: `opl workspace artifact-lifecycle --workspace <path> [--project-id <id>] [--dry-run|--apply]`.
- Implementation: `/Users/gaofeng/workspace/one-person-lab/src/workspace-artifact-lifecycle.ts`.
- Projection root: `control/opl/artifact_lifecycle/`.
- Domain handoff input: `handoff/review-repair-transport.json`.
- Review-repair output: `control/opl/artifact_lifecycle/review_repair_transport.json`.

The transport treats domain repair decisions as opaque refs:

- `revision_entrypoint_decision_ref`
- `route_back_ref`
- `repair_plan_ref`
- `typed_blocker_ref`
- `owner_decision_ref`
- `freshness_gate_ref`
- `iteration_limit_ref`
- `current_owner_delta_ref`

It projects current owner, accepted next-answer shape, route-back target, iteration count, stale downstream refs, and closure options. It does not parse or decide BookForge manuscript meaning.

## Domain-Owned Semantics

BookForge owns:

- repair level selection;
- reverse-outline interpretation;
- storyline, reader, chapter, evidence, model, style, publication design, and artifact-target refs;
- manuscript and memory body;
- quality/export verdicts;
- owner receipts and owner blockers.

## OPL-Owned Mechanics

OPL may own:

- route-back transport and projection;
- iteration cap accounting;
- stale-ref/freshness projection from declared refs;
- current-owner display;
- handoff packet lifecycle;
- generated interface descriptors that expose opaque refs only.

## Required Guardrails

- OPL must not convert `route-back-ref` into quality approval.
- OPL must not rewrite domain artifacts or memory body.
- OPL must not sign owner receipts or quality/export verdicts.
- OPL must preserve the domain's typed blocker and owner-decision labels.
- OPL should fail closed when the route-back target, current owner, or accepted answer shape is missing.

## Fresh OPL Evidence

- `npm run typecheck` in `/Users/gaofeng/workspace/one-person-lab`: passed on 2026-06-20.
- `node --experimental-strip-types --test tests/src/cli/cases/workspace-domain.initializer.test.ts` in `/Users/gaofeng/workspace/one-person-lab`: 19/19 passed on 2026-06-20.
- Focused test coverage includes a BookForge success path that materializes source passport, memory lifecycle, output lifecycle, review-repair transport, health, and index projections.
- Focused test coverage includes a fail-closed BookForge path for missing current owner, missing accepted answer shape, missing route-back target, stale downstream refs, and exceeded iteration limit.

This is local OPL source/test evidence for the transport surface. It is not hosted runtime parity, production readiness, repair acceptance, publication readiness, or owner acceptance.

## BookForge Evidence Needed Before Promotion

- A real manuscript meta-review that produces a revision entrypoint decision.
- At least one routed repair that refreshes the corresponding BookForge refs and downstream artifacts.
- A route-back case to `storyline-architecture` or `outline_sequence_repair`.
- A local prose case that proves fast-track does not bypass higher-order defects.
- BookForge `scripts/verify.sh` after the domain refs are updated.
- OPL `workspace artifact-lifecycle --apply` evidence against a real BookForge workspace with project-local handoff refs.
