# OPL Book Forge Ideal State Gap Plan

Owner: `opl-bookforge`
Purpose: `active_truth_plan`
State: `active_gap_owner`
Machine boundary: Human-readable active plan. Machine truth remains in contracts, agent pack files, OPL validator output, runtime receipts, pilot evidence, owner receipts, and typed blockers.

This document is the active development baton for OPL Book Forge. It tracks the current structural baseline, the functional / structural gaps from the ideal Book Forge domain pack, and the next executable agent prompt. It does not make runtime, publication, export, owner-acceptance, or production-readiness claims.

Current SSOT reading: this plan keeps Book Forge functional / structural gaps only: standard scaffold/interface shape, golden-path routing, stage pack refs, generated/hosted surface consumption, PDF/proof helper plumbing, revision-entrypoint routing, workspace artifact-lifecycle handoff refs, default-caller structural gates, no-active-caller/tombstone/provenance cleanup, and no-second-truth guards. Real long-book runs, owner acceptance, publication-proof visual acceptance, final export acceptance, live OPL StageRun / hosted artifact-handoff parity, physical delete authorization, and production-ready claims are later evidence lanes. They must not be mixed into this active gap list, and scaffold/interface validation, pilot exports, rendered pages, docs foldback, OMA evidence, or helper plumbing cannot replace them.

## Ideal-State Reference

Book Forge should be an OPL-standard Foundry Agent domain pack for long-form book authoring:

- declarative domain pack plus minimal Book Forge authority functions;
- a five-stage sequence: `storyline-architecture` -> `chapter-production-planning` -> `chapter-materialization` -> `source-style-integrity-review` -> `publication-proof-handoff`;
- book-length materialization from chapter-sharded Markdown refs, chapter task cards, context packs, style/claim/proof refs, memory refs, and owner handoff receipts;
- routed revision entrypoint decisions before serious manuscript repairs;
- publication-proof and final-export gates backed by Book Forge-owned proof refs, real typesetting backend evidence, rendered-page inspection, and owner/export acceptance;
- OPL-generated or OPL-hosted surfaces carrying descriptors, lifecycle refs, artifact-lifecycle projections, generated `opl agents run` entries, hosted surface kinds, and interface metadata only.

Book Forge owns manuscript bodies, book-domain truth, memory body, style/claim rules, quality/export verdict boundaries, artifact authority, and owner receipts. OPL owns generated surfaces, framework runtime/projection, workspace artifact lifecycle, dependency doctor routes, and hosted transport.

## Current Structural Baseline

| Area | Current status | Evidence owner | Boundary |
| --- | --- | --- | --- |
| OPL standard structure | `done_structural_baseline` | `scripts/verify.sh`, OPL scaffold/interface validators, contracts and agent pack files | Proves structure/interface readability only. |
| Agent Lab self-evolution capability map | `structural_routing_fields_landed` | `contracts/capability_map.json`, OPL scaffold validator readback | Capability entries now expose improvement tokens, canonical target paths, verification refs, forbidden surfaces, and owner closeout boundary refs for Agent Lab routing, including all repo-local professional skill locators. This is resolver metadata only, not owner acceptance, memory-body authority, typed blocker creation, domain readiness, or production readiness. |
| Standard Foundry Agent public projection | `done_structural_baseline` | `contracts/foundry_agent_series.json`, `contracts/generated_surface_handoff.json`, `scripts/verify.sh` | Book Forge consumes the canonical OPL Foundry policy export and release pin without copying policy body; its consumer authority flags are all false. This proves structural standard-agent projection only, not live OPL StageRun execution or hosted artifact-handoff parity. |
| Golden path default route | `done_structural_baseline` | `contracts/golden_path_profile.json`, `agent/stages/manifest.json`, OPL generated control plane and conformance validator | The ordinary default route is `storyline-architecture` only; `materialize-book` enters `chapter-production-planning` directly, then follows the remaining focused stages without creating a second default entry or delivery-ready claim. |
| OMA Agent Lab evidence | `evidence_recorded` | `docs/evidence/oma-agent-lab/` | Supports baseline/takeover evidence, not book quality or owner acceptance. |
| Historical real short-book pilot | `evidence_recorded_owner_blocked` | `docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/` | Historical pilot evidence with owner blockers; not the current long-book source pattern. |
| Book-length workflow rules | `domain_rules_landed` | `docs/invariants.md`, `docs/decisions.md`, agent skills, professional skills, quality gates | Rules exist, including the professional book-memory curator method layer; real long-book run evidence remains open. |
| PDF/proof helper plumbing | `helper_plumbing_landed` | `runtime/native_helpers/bookforge_pdf_export.py`, OPL native-helper probe/profile checks in `scripts/verify.sh helpers`, two compile/render E2E cases in `scripts/verify.sh pdf`, and the table-driven canonical gate matrix | Default verification stays policy-only; heavy proof-backend behavior is explicit without recompiling every negative gate variant. Helper evidence supports proof plumbing, not final visual judgment. |
| Hosted image asset authority boundary | `closed_registry_handler_landed_live_hosted_evidence_open` | `contracts/image_asset_host_handoff.json`, closed `contracts/domain_handler_registry.json`, input/output schemas, read-only helper, focused handler test | OPL owns generation, transport, bitmap materialization, attempt/output refs, and persistence. Book Forge only validates the host-injected contained bitmap and returns a figure-authority receipt candidate or quality debt through `handler:obf.figure-asset-authority-evaluate`. Structural registry/source-closure proof is not live generation or visual acceptance evidence. |
| Revision entrypoint routing | `domain_refs_landed` | `agent/skills/revision-entrypoint-router.md`, `docs/references/opl-base-revision-routing-handoff.md` | Needs real manuscript meta-review route-back evidence. |
| OPL workspace artifact lifecycle | `handoff_contract_landed_apply_evidence_open` | OPL `workspace artifact-lifecycle` source/tests, `contracts/artifact_lifecycle_handoff.json`, direct OPL readback, and Book Forge handoff reference | Proves the OPL/Book Forge lifecycle authority split, required refs, readback command, and false-ready guard; still needs apply evidence against a real Book Forge workspace. |
| Temporal StageRun completion audit | `completion_audit_contract_landed_owner_gate_open` | `contracts/temporal_stage_run_consumption_policy.json#completion_audit`, `contracts/temporal_stage_run_consumption_policy.json#default_entry_routing`, `contracts/action_catalog.json`, focused policy test | Separates OPL provider completion, generated-surface readiness, and StageRun status from Book Forge `review_pdf`, `publication_proof`, `final_export`, and owner acceptance. Revision, export, and production-acceptance defaults route through the OPL StageRun account/current-owner boundary; evidence packages remain output refs only. It is a structural account boundary; live StageRun evidence, real book pilot owner receipt, human gate, and owner/export acceptance remain open. |
| Live StageRun progress evidence contract | `owner_evidence_required` | `contracts/live_stage_run_progress_evidence.json`, immutable historical pilot/OMA provenance, focused topology and policy tests | Uses the shared OPL contract without accepted live evidence refs. Old pilot evidence predates the active five-stage topology and remains provenance only; current-topology Live Evidence, readiness, final-export acceptance, owner acceptance, and runtime claims remain open. |
| Production acceptance tail contract | `domain_owned_typed_blocker_recorded_not_ready_claim` | `contracts/production_acceptance/bookforge-production-acceptance.json`, historical pilot typed-blocker refs, focused policy test, OPL conformance readback | Provides the production-specific domain-owned typed blocker surface expected by OPL conformance. It closes the missing-contract production tail only; owner acceptance, final export acceptance, production readiness, domain readiness, and quality/export readiness remain open. |
| Repo source byproduct hygiene | `source_structure_guard_landed` | `contracts/workspace_lifecycle_policy.json#byproduct_policy.repo_source_byproduct_guard`, OPL `workspace source-hygiene --source-root <repo> --json`, `scripts/verify.sh structural` | Proves ignored Python/cache/install residue is fail-closed at the structural readback boundary; does not prove workspace apply, book delivery, publication readiness, or owner acceptance. |
| Default-caller deletion structural gates | `structural_gate_landed_not_delete_ready` | `contracts/functional_privatization_audit.json`, OPL `agents default-callers --agent opl-bookforge=<repo> --json` | Generated wrapper/default-caller residue is classified as StageRun account dispatch metadata rather than a repo-local runner. No-forbidden-write proof and typed-blocker refs are structurally visible to OPL; physical delete and default-caller delete readiness remain false. |
| Private platform retirement matrix | `hygiene_deleted_image_handler_thinned` | `contracts/functional_privatization_audit.json#bookforge_private_platform_retirement_matrix`, `contracts/generated_surface_handoff.json#private_platform_retirement_projection`, focused policy test | The no-caller historical hygiene implementation is deleted. Publication/export helpers remain domain-specific; image validation is a read-only minimal authority handler; runtime/session/update surfaces remain absent. Hosted ABI binding and later owner/live evidence remain separate. |
| Non-live functional closure gate | `functional_structure_gate_landed_not_publication_or_owner_acceptance` | `contracts/temporal_stage_run_consumption_policy.json#functional_closure_gate`, `tests/test_temporal_stage_run_consumption_policy.py` | Scaffold/interface, golden path, revision route, PDF/proof helper plumbing, artifact lifecycle handoff, default-caller structural gate, private platform retirement matrix, and evidence package navigation are bound as non-live required refs; this does not prove publication readiness, final export, owner acceptance, domain readiness, production readiness, workspace apply, hosted parity, or physical delete authorization. |

## Functional / Structural Gaps

| Gap | Current state | Needed owner action |
| --- | --- | --- |
| Long-book structural workflow | Historical pilot evidence remains package payload; long-form rules, chapter-sharded Markdown package shape, chapter QC expectations, merged-manuscript handoff refs, and active production queue semantics must stay represented as Book Forge-owned structure without becoming a production-ready claim. | Keep chapter-sharded package, QC, merge, and handoff contracts/docs aligned; route real long-book run evidence to the later evidence lane. |
| Publication-proof plumbing | Proof helper and proof rules exist; active plan only tracks helper plumbing, project-local proof-ref requirements, and false-ready boundaries. | Keep proof/profile/helper contracts and docs aligned; route visual inspection, final export acceptance, and owner decision evidence to the later evidence lane. |
| Completion account split | Completion accounts are contractually split between OPL provider/generated/StageRun accounts and Book Forge `review_pdf`, `publication_proof`, `final_export`, and owner acceptance accounts. | Keep the split visible in contracts/docs and prevent provider completion, generated descriptors, docs, rendered pages, or helper proof plumbing from closing Book Forge domain completion. |
| Live StageRun progress evidence tail | Book Forge exposes a refs-only contract that marks old two-stage pilot evidence as topology-superseded provenance. It intentionally records no current-topology blocker or receipt and keeps the Live Evidence tail open. | Route actual five-stage progress closure to future StageRun receipts, owner route-back, no-regression, long-soak, or owner acceptance evidence; do not remap old evidence or synthesize current evidence. |
| Production acceptance evidence tail | Book Forge now exposes a production-specific acceptance contract for OPL conformance, with domain-owned typed blockers for owner acceptance / final export / production-ready claim still open. | Keep `contracts/production_acceptance/bookforge-production-acceptance.json` bound to domain-owned refs and false-ready flags; route actual production readiness to future owner receipt, human gate, route-back, or no-regression evidence. |
| Revision route-back structure | Router refs exist and should stay as Book Forge-owned decision refs rather than a generic OPL repair router. | Keep `revision-entrypoint-router` and OPL handoff docs aligned; route real manuscript meta-review route-back evidence to the later evidence lane. |
| OPL artifact lifecycle boundary | OPL refs-only transport exists as local source/test evidence; Book Forge has a machine-readable handoff contract while direct OPL readback owns projection refs, owner split, readback command, and false-ready boundaries. | Maintain `contracts/artifact_lifecycle_handoff.json`, direct OPL readback, and docs as structural boundary; route real workspace apply receipts to the later evidence lane. |
| Active portfolio coverage | Core current docs are aligned enough for the current baton; evidence package role now has a single index, evidence leaves remain package payloads rather than active truth owners, and default-caller structural delete gates are recorded without authorizing deletion. | Keep historical evidence under `docs/evidence/**` and `docs/history/**`; route evidence-package navigation through `docs/evidence/README.md`; do not convert evidence leaves into current status, active process logs, physical delete authorization, or ready claims. |
| Default path functional closure guard | The non-live gate now binds standard scaffold/interface validation, golden path default route, revision entrypoint routing, PDF/proof helper plumbing, artifact lifecycle handoff refs, default-caller structural gates, private platform retirement matrix, and evidence package navigation in one contract readback. | Maintain `contracts/temporal_stage_run_consumption_policy.json#functional_closure_gate` and its focused test; route real long-book, publication-proof visual acceptance, final export, owner acceptance, hosted artifact handoff parity, workspace apply receipt, and physical delete authorization to later evidence lanes. |
| Private platform tail retirement | Publication/export helpers remain legitimate domain operations; image validation is a closed-registry read-only authority handler; the no-caller project-hygiene implementation is deleted; runtime/session/update/workbench surfaces remain absent. | Keep the registry closed, keep the exact source/effect closure at zero private generic effects, and route owner acceptance, live hosted parity, final export, and publication readiness to later evidence lanes. |
| Hosted stage-action entry closure | Revision routing, publication/final-export, and production acceptance share `contracts/temporal_stage_run_consumption_policy.json#default_entry_routing`; `contracts/action_catalog.json` is a closed `family-action-catalog.v2` object using only the stage-manifest binding, with no `source_command`, action handler id/ref, per-surface command copy, or duplicated completion/default-entry policy. OPL generates `opl agents run --domain opl-bookforge --action <action_id> --workspace <absolute_path>` and hosted surface kinds. The image handler remains a separate closed-registry callable. | Keep every mutating action bound to `agent/stages/manifest.json`, keep its entry/required refs in `stage_route`, keep public actions separate from minimal authority handlers, and route live hosted execution/parity to later evidence lanes. |

本轮按 source/import、package payload、verification、generated/default caller 与 `launcher|wrapper|alias|compat|legacy|status|sidecar|product-entry|helper|facade` 关键词复核后，确认历史 project-hygiene 实现只有自引用和声明式保留说明，没有 active/package/default caller，已连同 parts 物理删除。其余命中的 publication helper、projection 与 default-entry surfaces 分别归为合法 domain-specific helper、refs-only projection 或 StageRun account dispatch metadata；不得据此扩张删除到 Pandoc/XeLaTeX/PDF 领域交付能力、owner authority 或 hosted ABI 尚未替换的表面。

## Ready / Export Claim Boundary

This active plan does not carry owner acceptance, final export acceptance, publication-proof visual acceptance, live OPL StageRun / hosted artifact-handoff parity, real long-book project evidence, lifecycle/currentness apply evidence, physical delete authorization, or production-ready worklists. Those belong to owner / release / runtime evidence owners. This plan may mention them only as false-ready boundaries and must not list run ids, owner receipts, human gates, screenshot paths, pilot counters, or ready-claim work items.

## Next-Round Agent Prompt

Use this prompt for the next OPL Book Forge development tranche:

```text
Task: govern OPL Book Forge from the current active truth plan.
Cwd: /Users/gaofeng/workspace/opl-bookforge
Write scope: choose exactly one narrow lane and state the allowed write set before editing. Default writable docs are docs/active/bookforge-ideal-state-gap-plan.md plus the lane's direct evidence/reference doc. Contract/schema/authority changes require scripts/verify.sh.
Non-goals: do not implement generic OPL runtime, queue, scheduler, app shell, hosted transport, default entrypoints, manuscript acceptance, publication approval, owner acceptance, production readiness, or final export readiness in this repo.
Live truth inputs: contracts, agent pack files, scripts/verify.sh, docs/status.md, docs/invariants.md, docs/architecture.md, docs/decisions.md, docs/references/opl-base-revision-routing-handoff.md, OPL validator output, runtime/native helper output, project-local structural proof refs, and this active plan. Use owner receipts, typed blockers, and live evidence refs only to prevent false-ready claims or to route the work to the later evidence lane.
Claim boundary: structural scaffold/interface proof is not book delivery proof; helper proof plumbing is not visual acceptance; generated descriptors are not hosted runtime parity; docs are not owner acceptance.

Pick one high-confidence lane only:
1. artifact-lifecycle handoff contract / direct OPL readback boundary cleanup;
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
- For proof/export helper-plumbing lanes that need backend compile/render behavior: ./scripts/verify.sh pdf-smoke plus the relevant runtime/native helper or project-local proof verifier; do not claim publication/export/owner acceptance from helper proof.

Completion gate: stop only after fresh verification passes, changes are committed and pushed to main, post-push parity is checked, and remaining stale/retire candidates are folded back into this plan or recorded as blocked with owner/evidence needs.
Foldback target: docs/active/bookforge-ideal-state-gap-plan.md is the active truth owner for progress, gaps, next prompt, and remaining candidate state.
```

## Portfolio Coverage State

- Covered by this active owner: current progress, functional/structural gaps, later-evidence routing, and next executable prompt.
- Current-status SSOT remains `docs/status.md`; this file should not duplicate evidence package lists or dated run transcripts.
- Support/reference docs remain `docs/references/**`; history/provenance remains `docs/history/**`; evidence-package navigation remains `docs/evidence/README.md`, with evidence payloads under `docs/evidence/**`.
- Remaining stale/retire candidates need fresh no-active-caller or replacement-owner proof before physical deletion. Current scans mainly show history/provenance or contract-backed no-resurrection contexts, not safe delete authority.
