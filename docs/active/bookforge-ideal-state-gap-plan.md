# OPL Book Forge Ideal State Gap Plan

Owner: `opl-bookforge`
Purpose: `active_truth_plan`
State: `active_gap_owner`
Machine boundary: Human-readable active plan. Machine truth remains in contracts, agent pack files, OPL validator output, runtime receipts, pilot evidence, owner receipts, and typed blockers.

This document is the active development baton for OPL Book Forge. It tracks current completion progress, the gap from the ideal Book Forge domain pack, and the next executable agent prompt. It does not make runtime, publication, export, owner-acceptance, or production-readiness claims.

2026-06-30 SSOT refresh: this plan keeps Book Forge functional / structural
gaps only: standard scaffold/interface shape, golden-path routing, stage pack
refs, generated/hosted surface consumption, PDF/proof helper plumbing,
revision-entrypoint routing, workspace artifact-lifecycle handoff refs,
default-caller structural gates, no-active-caller/tombstone/provenance cleanup,
and no-second-truth guards. Real long-book runs, owner acceptance,
publication-proof visual acceptance, final export acceptance, direct runtime CLI
/ hosted artifact-handoff parity, physical delete authorization, and
production-ready claims are later evidence lanes. They should not be mixed into
the ideal-state or current-state gap list, and scaffold/interface validation,
pilot exports, rendered pages, docs foldback, OMA evidence, or helper plumbing
cannot replace them.

Functional and structural gaps come first when they do not require long-running or owner-gated proof: scaffold/interface shape, golden-path route shape, stage pack refs, generated/hosted surface consumption, PDF/proof helper plumbing, revision-entrypoint routing, workspace artifact-lifecycle handoff refs, default-caller structural gates, no-active-caller/tombstone/provenance cleanup, and no-second-truth guards. Owner acceptance, real long-book project evidence, final export acceptance, publication-proof visual acceptance, direct runtime CLI / hosted artifact-handoff parity, physical delete authorization, and production-ready claims are not maintained in this active plan. They only become hard gates for release/readiness/delete claims, and structural validation, OMA evidence, pilot exports, rendered pages, docs foldback, or helper proof plumbing cannot replace them.

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
| Standard Foundry Agent public projection | `done_structural_baseline` | `contracts/foundry_agent_series.json`, `contracts/generated_surface_handoff.json`, `scripts/verify.sh` | Proves Book Forge is represented as a standard domain agent and that public membership/status are not generated-surface or plugin-transport axes; does not prove direct runtime CLI or hosted artifact-handoff parity. |
| Golden path default route | `done_structural_baseline` | `contracts/golden_path_profile.json`, `contracts/stage_control_plane.json`, OPL conformance validator | The ordinary default route is `storyline-architecture` only; `book-materialization` remains a follow-on stage by handoff or explicit selection, not a second default entry or delivery-ready claim. |
| OMA Agent Lab evidence | `evidence_recorded` | `docs/evidence/oma-agent-lab/` | Supports baseline/takeover evidence, not book quality or owner acceptance. |
| Historical real short-book pilot | `evidence_recorded_owner_blocked` | `docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/` | Historical pilot evidence with owner blockers; not the current long-book source pattern. |
| Book-length workflow rules | `domain_rules_landed` | `docs/invariants.md`, `docs/decisions.md`, agent skills, quality gates | Rules exist; real long-book run evidence remains open. |
| PDF/proof helper plumbing | `helper_plumbing_landed` | `runtime/native_helpers/bookforge_pdf_export.py`, proof/profile checks in `scripts/verify.sh` | Helper evidence supports proof plumbing, not final visual judgment. |
| Revision entrypoint routing | `domain_refs_landed` | `agent/skills/revision-entrypoint-router.md`, `docs/references/opl-base-revision-routing-handoff.md` | Needs real manuscript meta-review route-back evidence. |
| OPL workspace artifact lifecycle | `handoff_contract_landed_apply_evidence_open` | OPL `workspace artifact-lifecycle` source/tests, `contracts/artifact_lifecycle_handoff.json`, Book Forge hygiene readback, and Book Forge handoff reference | Proves the OPL/Book Forge lifecycle authority split, required refs, readback command, and false-ready guard; still needs apply evidence against a real Book Forge workspace. |
| Temporal StageRun completion audit | `completion_audit_contract_landed_acceptance_tail_open` | `contracts/temporal_stage_run_consumption_policy.json#completion_audit`, `contracts/action_catalog.json`, focused policy test | Separates OPL provider completion, generated-surface readiness, and StageRun status from Book Forge `review_pdf`, `publication_proof`, `final_export`, and owner acceptance. It is a structural account boundary; live StageRun evidence, real book pilot owner receipt, human gate, and owner/export acceptance remain open. |
| Repo source byproduct hygiene | `source_structure_guard_landed` | `contracts/workspace_lifecycle_policy.json#byproduct_policy.repo_source_byproduct_guard`, `runtime/native_helpers/bookforge_project_hygiene.py --source-byproduct-check`, `scripts/verify.sh` | Proves ignored Python/cache/install residue is fail-closed before and after repo verification; does not prove workspace apply, book delivery, publication readiness, or owner acceptance. |
| Default-caller deletion structural gates | `structural_gate_landed_not_delete_ready` | `contracts/functional_privatization_audit.json`, OPL `agents default-callers --agent opl-bookforge=<repo> --json` | No-forbidden-write proof and typed-blocker refs are structurally visible to OPL; physical delete and default-caller delete readiness remain false. |

## Functional / Structural Gaps

| Gap | Current state | Needed owner action |
| --- | --- | --- |
| Long-book structural workflow | Historical pilot evidence remains package payload; long-form rules, chapter-sharded Markdown package shape, chapter QC expectations, merged-manuscript handoff refs, and active production queue semantics must stay represented as Book Forge-owned structure without becoming a production-ready claim. | Keep chapter-sharded package, QC, merge, and handoff contracts/docs aligned; route real long-book run evidence to the later evidence lane. |
| Publication-proof plumbing | Proof helper and proof rules exist; active plan only tracks helper plumbing, project-local proof-ref requirements, and false-ready boundaries. | Keep proof/profile/helper contracts and docs aligned; route visual inspection, final export acceptance, and owner decision evidence to the later evidence lane. |
| Completion account split | Completion accounts are contractually split between OPL provider/generated/StageRun accounts and Book Forge `review_pdf`, `publication_proof`, `final_export`, and owner acceptance accounts. | Keep the split visible in contracts/docs and prevent provider completion, generated descriptors, docs, rendered pages, or helper proof plumbing from closing Book Forge domain completion. |
| Revision route-back structure | Router refs exist and should stay as Book Forge-owned decision refs rather than a generic OPL repair router. | Keep `revision-entrypoint-router` and OPL handoff docs aligned; route real manuscript meta-review route-back evidence to the later evidence lane. |
| OPL artifact lifecycle boundary | OPL refs-only transport exists as local source/test evidence; Book Forge has a machine-readable handoff contract and hygiene readback for projection refs, owner split, readback command, and false-ready boundaries. | Maintain `contracts/artifact_lifecycle_handoff.json`, hygiene readback, and docs as structural boundary; route real workspace apply receipts to the later evidence lane. |
| Active portfolio coverage | Core current docs are aligned enough for the current baton; evidence package role now has a single index, evidence leaves remain package payloads rather than active truth owners, and default-caller structural delete gates are recorded without authorizing deletion. | Keep historical evidence under `docs/evidence/**` and `docs/history/**`; route evidence-package navigation through `docs/evidence/README.md`; do not convert evidence leaves into current status, active process logs, physical delete authorization, or ready claims. |

## Ready / Export Claim Boundary

This active plan does not carry owner acceptance, final export acceptance, publication-proof visual acceptance, direct runtime CLI / hosted artifact-handoff parity, live StageRun evidence, real long-book project evidence, lifecycle/currentness apply evidence, physical delete authorization, or production-ready worklists. Those belong to owner / release / runtime evidence owners. This plan may mention them only as false-ready boundaries and must not list run ids, owner receipts, human gates, screenshot paths, pilot counters, or ready-claim work items.

## Next-Round Agent Prompt

Use this prompt for the next OPL Book Forge development tranche:

```text
Task: govern OPL Book Forge from the current active truth plan.
Cwd: /Users/gaofeng/workspace/opl-bookforge
Write scope: choose exactly one narrow lane and state the allowed write set before editing. Default writable docs are docs/active/bookforge-ideal-state-gap-plan.md plus the lane's direct evidence/reference doc. Contract/schema/authority changes require scripts/verify.sh.
Non-goals: do not implement generic OPL runtime, queue, scheduler, app shell, hosted transport, default entrypoints, manuscript acceptance, publication approval, owner acceptance, production readiness, or final export readiness in this repo.
Functional truth inputs: contracts, agent pack files, scripts/verify.sh, docs/status.md, docs/invariants.md, docs/architecture.md, docs/decisions.md, docs/references/opl-base-revision-routing-handoff.md, OPL validator output, runtime/native helper output, project-local structural proof refs, and this active plan. Use owner receipts, typed blockers, and live evidence refs only to prevent false-ready claims or to route the work to the later evidence lane.
Claim boundary: structural scaffold/interface proof is not book delivery proof; helper proof plumbing is not visual acceptance; generated descriptors are not hosted runtime parity; docs are not owner acceptance.

Pick one high-confidence lane only:
1. artifact-lifecycle handoff contract / hygiene readback boundary cleanup;
2. revision-entrypoint routing docs / contract boundary cleanup;
3. publication-proof helper plumbing / false-ready guard cleanup;
4. long-book structural package, chapter QC, merge, and handoff docs cleanup.

Required actions:
- State the semantic theme, SSOT, peer docs, section classification, allowed write set, forbidden write set, owner boundary, and exact claim boundary before editing.
- Keep OPL runtime/generic lifecycle work in OPL; keep manuscript body, quality/export decisions, memory body, artifact authority, and owner receipts in Book Forge.
- Update this plan after the lane so progress, functional/structural gaps, later-evidence routing, and remaining candidates reflect fresh truth.

Verification commands:
- For docs-only lanes: git diff --check; rg -n '^(<<<<<<<|=======|>>>>>>>)' docs; targeted stale scan for the retired or rewritten terms; OPL Doc doctor as risk map.
- For contract/schema/authority or generated-interface lanes: ./scripts/verify.sh.
- For proof/export helper-plumbing lanes: ./scripts/verify.sh plus the relevant runtime/native helper or project-local proof verifier; do not claim publication/export/owner acceptance from helper proof.

Completion gate: stop only after fresh verification passes, changes are committed and pushed to main, post-push parity is checked, and remaining stale/retire candidates are folded back into this plan or recorded as blocked with owner/evidence needs.
Foldback target: docs/active/bookforge-ideal-state-gap-plan.md is the active truth owner for progress, gaps, next prompt, and remaining candidate state.
```

## Portfolio Coverage State

- Covered by this active owner: current progress, functional/structural gaps, later-evidence routing, and next executable prompt.
- Current-status SSOT remains `docs/status.md`; this file should not duplicate evidence package lists or dated run transcripts.
- Support/reference docs remain `docs/references/**`; history/provenance remains `docs/history/**`; evidence-package navigation remains `docs/evidence/README.md`, with evidence payloads under `docs/evidence/**`.
- Remaining stale/retire candidates need fresh no-active-caller or replacement-owner proof before physical deletion. Current scans mainly show history/provenance or contract-backed no-resurrection contexts, not safe delete authority.
