# OPL Base Revision Routing Handoff

Owner: `opl-bookforge`
Purpose: `opl_base_handoff`
State: `proposal_for_opl_owner`
Machine boundary: Human-readable handoff proposal. Machine truth remains in BookForge contracts, OPL validator output, runtime receipts, owner receipts, and typed blockers.

## Problem

BookForge Meta Review can now discover that a manuscript should not be repaired from a sentence or chapter. Some findings require a route back to artifact target, storyline architecture, outline sequence, chapter function, evidence/model, publication design, or owner/source decisions.

The domain owns those semantics, but the OPL base should make the route easy to execute and inspect across agents.

## Desired OPL Base Surface

OPL should provide a generic review-repair transport that treats domain repair decisions as opaque refs:

- `revision-entrypoint-decision-ref`
- `route-back-ref`
- `repair-plan-ref`
- `typed-blocker-ref`
- `owner-decision-ref`
- `freshness-gate-ref`
- `iteration-limit-ref`
- `current-owner-delta-ref`

The transport should show the current owner, accepted next-delta shape, iteration count, stale downstream refs, and closure options. It should not parse or decide BookForge manuscript meaning.

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

## BookForge Evidence Needed Before Promotion

- A real manuscript meta-review that produces a revision entrypoint decision.
- At least one routed repair that refreshes the corresponding BookForge refs and downstream artifacts.
- A route-back case to `storyline-architecture` or `outline_sequence_repair`.
- A local prose case that proves fast-track does not bypass higher-order defects.
- OPL scaffold/interfaces validation after the domain refs are updated.
