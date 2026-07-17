# OPL Book Forge Status

Owner: `opl-bookforge`
Purpose: `current_status`
State: `active_truth`
Machine boundary: Human-readable current summary. Machine truth remains in contracts, agent pack files, source, tests, OPL validator/readback output, runtime receipts, owner receipts, and typed blockers.

Book Forge is an OPL-standard book-authoring domain package with canonical `agent_id/package_id=obf`. The repo, npm package, plugin, carrier, and domain locators may use `opl-bookforge`; they do not create a second package identity.

## Current Implementation

- The public domain actions are `shape-storyline` and `materialize-book`. OPL owns generated CLI, MCP, skill, product-entry, StageRun, and hosted projections.
- The active stage graph is `storyline-architecture` -> `chapter-production-planning` -> `chapter-materialization` -> `source-style-integrity-review` -> `publication-proof-handoff`. `storyline-architecture` is the ordinary default route; `materialize-book` enters planning directly.
- Book Forge owns manuscript and book-memory bodies, book-domain truth, style and claim rules, figure/table authority, quality/export verdict boundaries, and owner receipt bodies.
- OPL owns generic runtime, provider attempts, queues, generated surfaces, workspace artifact-lifecycle projection, dependency maintenance, registry/discovery, and promotion mechanics.
- Revision repair starts from a Book Forge-owned entrypoint decision. OPL may transport opaque route-back and blocker refs but cannot decide manuscript meaning or acceptance.
- Review PDF, publication proof, and final export are separate accounts. Helper output and rendered-page machine checks are proof plumbing; final export remains owner-gated.
- The image authority handler is a closed, read-only domain callable. OPL generates and materializes bitmaps; Book Forge validates the injected asset and returns a receipt candidate or quality debt.
- OPL Ledger registration is refs-only. It may index artifact and receipt refs but cannot store manuscript bodies, sign owner receipts, or authorize publication/export verdicts.

## Verification Surface

- `scripts/verify.sh`: fast policy and contract lane.
- `scripts/verify.sh structural`: adds OPL scaffold, interface, and source-hygiene readback.
- `scripts/verify.sh helpers`: checks native-helper descriptors and adapters.
- `scripts/verify.sh pdf`: runs the two real review/proof compile-render paths.
- `scripts/verify.sh full-local`: runs the repo-owned policy, helper, PDF, and handler union.
- `scripts/verify.sh full`: adds current OPL structural readback to the local union.

These checks prove only the surfaces they execute. They do not establish a live StageRun, book quality, publication approval, final-export acceptance, owner acceptance, release, hosted parity, or production readiness.

<a id="live-stage-progress-evidence"></a>
## Live Stage Progress Evidence

`contracts/live_stage_run_progress_evidence.json` is `owner_evidence_required` and contains no accepted current-topology live evidence refs. The retained short-book pilot used the superseded two-stage topology and remains historical provenance. Current five-stage execution, a real long-book run, hosted parity, final-export acceptance, and owner acceptance remain unproven.

<a id="production-acceptance-tail"></a>
## Production Acceptance Tail

`contracts/production_acceptance/bookforge-production-acceptance.json` exposes the historical pilot's domain-owned typed blocker through the contract expected by OPL conformance. This closes the missing contract surface only. It does not close owner acceptance, final export, publication approval, domain readiness, or production readiness.

## Evidence Packages

[The evidence index](./evidence/README.md) owns package names, roles, and claim boundaries. OMA Agent Lab material and the historical short-book pilot are retained evidence packages. Payload Markdown under the pilot is evidence body, not current documentation truth, and is intentionally left in its historical topology and vocabulary.

## Claim Boundary

Current repository evidence supports the OPL-standard structural package, current action/stage contracts, generated-surface ownership boundaries, helper plumbing, OMA evidence, and a historical owner-blocked pilot. It does not support production-ready book writing, publication approval, final-export readiness, owner acceptance, live five-stage execution, hosted artifact-handoff parity, real workspace lifecycle apply, or physical delete authorization.

Current gaps and the next executable baton live only in [the Active Truth plan](./active/bookforge-ideal-state-gap-plan.md).
