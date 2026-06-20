# OPL Book Forge Ideal State Gap Plan

Owner: `opl-bookforge`
Purpose: `active_truth_plan`
State: `active_gap_owner`
Machine boundary: Human-readable active plan. Machine truth remains in contracts, agent pack files, OPL validator output, runtime receipts, pilot evidence, owner receipts, and typed blockers.

This document is the active development baton for OPL Book Forge. It tracks current completion progress, the gap from the ideal Book Forge domain pack, and the next executable agent prompt. It does not make runtime, publication, export, owner-acceptance, or production-readiness claims.

## Ideal-State Reference

Book Forge should be an OPL-standard Foundry Agent domain pack for long-form book authoring:

- declarative domain pack plus minimal Book Forge authority functions;
- two coarse primary stages, `storyline-architecture` and `book-materialization`;
- book-length materialization from chapter-sharded Markdown refs, chapter task cards, context packs, style/claim/proof refs, memory refs, and owner handoff receipts;
- routed revision entrypoint decisions before serious manuscript repairs;
- publication-proof and final-export gates backed by Book Forge-owned proof refs, real typesetting backend evidence, rendered-page inspection, and owner/export acceptance;
- OPL-generated or OPL-hosted surfaces carrying descriptors, lifecycle refs, artifact-lifecycle projections, and interface metadata only.

Book Forge owns manuscript bodies, book-domain truth, memory body, style/claim rules, quality/export verdict boundaries, artifact authority, and owner receipts. OPL owns generated surfaces, framework runtime/projection, workspace artifact lifecycle, dependency doctor routes, and hosted transport.

## Current Completion Progress

| Area | Current status | Evidence owner | Boundary |
| --- | --- | --- | --- |
| OPL standard structure | `done_structural_baseline` | `scripts/verify.sh`, OPL scaffold/interface validators, contracts and agent pack files | Proves structure/interface readability only. |
| OMA Agent Lab evidence | `evidence_recorded` | `docs/evidence/oma-agent-lab/` | Supports baseline/takeover evidence, not book quality or owner acceptance. |
| Historical real short-book pilot | `evidence_recorded_owner_blocked` | `docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/` | Historical pilot evidence with owner blockers; not the current long-book source pattern. |
| Book-length workflow rules | `domain_rules_landed` | `docs/invariants.md`, `docs/decisions.md`, agent skills, quality gates | Rules exist; real long-book run evidence remains open. |
| PDF/proof helper plumbing | `helper_plumbing_landed` | `runtime/native_helpers/bookforge_pdf_export.py`, proof/profile checks in `scripts/verify.sh` | Helper evidence supports proof plumbing, not final visual judgment. |
| Revision entrypoint routing | `domain_refs_landed` | `agent/skills/revision-entrypoint-router.md`, `docs/references/opl-base-revision-routing-handoff.md` | Needs real manuscript meta-review route-back evidence. |
| OPL workspace artifact lifecycle | `local_transport_reference_landed` | OPL `workspace artifact-lifecycle` source/tests and Book Forge handoff reference | Needs apply evidence against a real Book Forge workspace. |
| Default-caller deletion structural gates | `structural_gate_landed_not_delete_ready` | `contracts/functional_privatization_audit.json`, OPL `agents default-callers --agent opl-bookforge=<repo> --json` | No-forbidden-write proof and typed-blocker refs are structurally visible to OPL; physical delete and default-caller delete readiness remain false. |

## Functional / Structural Gaps

| Gap | Current state | Needed owner action |
| --- | --- | --- |
| Real long-book materialization | Existing historical pilot is short-book evidence; long-form rules are recorded but not exercised end to end. | Run a real book project through chapter-sharded Markdown packages, active production queue, chapter QC, merged manuscript, and owner handoff refs. |
| Publication-proof run | Proof helper and proof rules exist, but no book-specific publication-proof visual inspection package closes the proof route. | Produce a project-local publication design profile, rendered pages, asset/font/readback evidence, visual inspection, and owner/export decision. |
| Revision route-back evidence | Router refs exist; current evidence does not show a real independent meta-review finding routed back to storyline, outline, chapter, evidence/model, publication design, local prose, or owner blocker. | Exercise `revision-entrypoint-router` on a real manuscript review and refresh the owning Book Forge refs. |
| OPL artifact lifecycle integration | OPL refs-only transport exists as local source/test evidence; Book Forge has no real workspace apply receipt for review-repair transport and refreshed downstream refs. | Run `opl workspace artifact-lifecycle --apply` against a real Book Forge workspace with `handoff/review-repair-transport.json`. |
| Active portfolio coverage | Core current docs are aligned enough for the current baton; evidence package role now has a single index, evidence leaves remain package payloads rather than active truth owners, and default-caller structural delete gates are recorded without authorizing deletion. | Keep historical evidence under `docs/evidence/**` and `docs/history/**`; route evidence-package navigation through `docs/evidence/README.md`; do not convert evidence leaves into current status, active process logs, physical delete authorization, or ready claims. |

## Test / Evidence Gaps

| Evidence gap | Why it matters | Minimum proof |
| --- | --- | --- |
| Owner acceptance | Required before publication, final export, or production-ready claims. | Owner receipt accepting topic, reader promise, manuscript quality, figure/table plan, layout, and publication intent. |
| Runtime/hosted parity | Generated descriptors are not runtime execution. | Direct `opl-bookforge` runtime CLI evidence or hosted OPL artifact-handoff parity evidence. |
| Publication proof visual acceptance | Rendered/nonblank pages do not prove human visual quality. | Visual inspection report for front matter, chapter openings, dense pages, figures/tables, callouts, closing pages, and owner-directed design preferences. |
| Lifecycle/currentness readback | Book-length workspaces need refs-only lifecycle/currentness projection before handoff/readiness claims. | Fresh OPL artifact-lifecycle apply/readback over Book Forge project refs. |

## Next-Round Agent Prompt

Use this prompt for the next OPL Book Forge development tranche:

```text
Task: govern OPL Book Forge from the current active truth plan.
Cwd: /Users/gaofeng/workspace/opl-bookforge
Write scope: choose exactly one narrow lane and state the allowed write set before editing. Default writable docs are docs/active/bookforge-ideal-state-gap-plan.md plus the lane's direct evidence/reference doc. Contract/schema/authority changes require scripts/verify.sh.
Non-goals: do not implement generic OPL runtime, queue, scheduler, app shell, hosted transport, default entrypoints, manuscript acceptance, publication approval, owner acceptance, production readiness, or final export readiness in this repo.
Live truth inputs: contracts, agent pack files, scripts/verify.sh, docs/status.md, docs/invariants.md, docs/architecture.md, docs/decisions.md, docs/references/opl-base-revision-routing-handoff.md, OPL validator output, runtime/native helper output, project-local proof refs, owner receipts, typed blockers, and this active plan.
Claim boundary: structural scaffold/interface proof is not book delivery proof; helper proof plumbing is not visual acceptance; generated descriptors are not hosted runtime parity; docs are not owner acceptance.

Pick one high-confidence lane only:
1. real Book Forge workspace artifact-lifecycle apply/readback for review-repair transport;
2. real manuscript revision-entrypoint route-back evidence;
3. publication-proof visual inspection package with project-local proof refs;
4. long-book materialization evidence foldback from chapter-sharded Markdown refs.

Required actions:
- State the semantic theme, SSOT, peer docs, section classification, allowed write set, forbidden write set, owner boundary, and exact claim boundary before editing.
- Keep OPL runtime/generic lifecycle work in OPL; keep manuscript body, quality/export decisions, memory body, artifact authority, and owner receipts in Book Forge.
- Update this plan after the lane so progress, functional gaps, evidence gaps, and remaining candidates reflect fresh truth.

Verification commands:
- For docs-only lanes: git diff --check; rg -n '^(<<<<<<<|=======|>>>>>>>)' docs; targeted stale scan for the retired or rewritten terms; OPL Doc doctor as risk map.
- For contract/schema/authority or generated-interface lanes: ./scripts/verify.sh.
- For proof/export lanes: ./scripts/verify.sh plus the relevant runtime/native helper or project-local proof verifier.

Completion gate: stop only after fresh verification passes, changes are committed and pushed to main, post-push parity is checked, and remaining stale/retire candidates are folded back into this plan or recorded as blocked with owner/evidence needs.
Foldback target: docs/active/bookforge-ideal-state-gap-plan.md is the active truth owner for progress, gaps, next prompt, and remaining candidate state.
```

## Portfolio Coverage State

- Covered by this active owner: current progress, functional/structural gaps, test/evidence gaps, and next executable prompt.
- Current-status SSOT remains `docs/status.md`; this file should not duplicate evidence package lists or dated run transcripts.
- Support/reference docs remain `docs/references/**`; history/provenance remains `docs/history/**`; evidence-package navigation remains `docs/evidence/README.md`, with evidence payloads under `docs/evidence/**`.
- Remaining stale/retire candidates need fresh no-active-caller or replacement-owner proof before physical deletion. Current scans mainly show history/provenance or contract-backed no-resurrection contexts, not safe delete authority.
