# OPL Revision Routing Handoff

Owner: `opl-bookforge`
Purpose: `support_reference_opl_revision_transport`
State: `active_reference`
Machine boundary: Human-readable cross-repo handoff boundary. Machine truth remains in Book Forge contracts and agent files, current OPL source/tests/readbacks, runtime receipts, owner receipts, and typed blockers.

## Purpose

Whole-book review may find that repair belongs above local prose: artifact target, storyline architecture, outline sequence, chapter function, evidence/model, publication design, or an owner/source decision. Book Forge owns that diagnosis. OPL may transport and project the resulting opaque refs so the next owner and route remain inspectable.

## Book Forge Owner Surface

Book Forge owns:

- the selected repair level and its evidence;
- reverse-outline and affected-artifact refs;
- allowed and forbidden lower-level edits;
- repair-plan, route-back, freshness, blocker, and owner-decision refs;
- manuscript and memory bodies, quality/export verdicts, and owner receipt bodies.

`contracts/artifact_lifecycle_handoff.json` declares the refs and false-ready boundary consumed by OPL. The current routing method lives in `agent/skills/revision-entrypoint-router.md`.

## OPL Owner Surface

OPL may own:

- workspace artifact-lifecycle transport and readback;
- current-owner, accepted-answer, iteration, and stale-ref projection;
- handoff packet lifecycle and generated surface descriptors;
- fail-closed validation when required routing or owner fields are absent.

OPL must not interpret manuscript semantics, edit Book Forge artifacts, sign owner receipts, or convert a route or review ref into quality/export approval.

## Verification Boundary

The Book Forge contract and repository tests prove only the declared handoff shape. Current OPL command behavior and currentness must be read from the active OPL repository and runtime readback; this reference does not pin a local checkout path, commit, dated test count, or hosted implementation claim.

A real promotion claim still requires an evidence-bound manuscript review, an actual routed repair with refreshed downstream refs, current OPL apply/readback evidence, and the relevant Book Forge review or owner receipt. None of those can be synthesized from this document.
