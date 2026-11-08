# OPL Book Forge Invariants

Owner: `opl-bookforge`
Purpose: `cross_cutting_domain_constraints`
State: `active_truth`
Machine boundary: Maintainer constraints and policy navigation; contracts, agent policy inputs, artifact bytes, and owner/runtime receipts remain authoritative.

## Identity And Authority

Canonical Agent and Package identity is `obf`; repository/domain/carrier locators
do not create another Package identity. Book Forge owns manuscript, source and
memory bodies, book quality, publication/export decisions, and owner receipts.
Framework owns generic execution, generated interfaces, and refs-only lifecycle
projection. Carrier installation, generated descriptors, provider completion,
StageRun status, hashes, and validator success cannot substitute for domain
judgment or owner acceptance.

Use the [declared stage graph](../agent/stages/manifest.json) and
[public action catalog](../contracts/action_catalog.json). Do not add private
runtime, scheduler, queue, attempt ledger, session store, lifecycle page,
provider discovery, OS package manager, TeX installer, or per-surface entry wrapper.
Source byproducts stay outside the checkout under the
[workspace policy](../contracts/workspace_lifecycle_policy.json).

## Writing And Evidence

Substantial book prose lives in chapter Markdown; scripts assemble, measure,
validate, and export it. Preserve owner-declared extent and reader priority.
Below-target chapters stay in progress and assemblies stay clearly labeled
previews. Primary-reader, author/source stance, and claim-evidence boundaries
cannot be weakened to make a draft look complete. Retired full-text drafts
must not remain searchable as current manuscript source.

| Constraint owner | Scope |
| --- | --- |
| [Book production](../agent/skills/book-production.md) | Chapter packages, budgets, contiguous review output, and production hygiene |
| [Reader style](../agent/skills/reader-style-contract.md) | Reader priority, inference, owner review, and author/source stance |
| [Reader-facing draft](../agent/skills/reader-facing-draft.md) | Separate manuscript prose from production metadata |
| [Claim integrity](../agent/skills/source-claim-integrity.md) | Locators, evidence classes, unsupported outcomes, and anti-leakage |
| [Context compiler](../agent/skills/chapter-context-compiler.md) | Inspectable selected refs, budgets, protected context, and next action |
| [Book memory](../agent/skills/book-memory.md) | Domain-owned working, episodic, and semantic memory |
| [Style calibration](../agent/skills/style-calibration.md) and [style engine](../agent/skills/style-engine.md) | Evidence-backed style assets, source preservation, and accepted exceptions |
| [Reference absorption](../agent/skills/reference-draft-absorption.md) | Reusable editorial improvements without copying authority or losing reasoning |

## Review And Handoff

The decisive Codex Attempt owns semantic routing; Framework validates and
materializes the transition. Formal Review uses new isolated StageAttempts.
Producer/repairer recommendations do not replace decisive reviewer/re-reviewer
decisions. Whole-book Meta Review diagnoses and routes without inline repair.
Only affected semantic dimensions and their dependencies lose review currentness;
hash or governance-only changes do not invalidate epistemic review.

Use [Review policy](../contracts/stage_quality_cycle_policy.json),
[epistemic dependencies](../contracts/epistemic_review_adoption.json), and
[revision routing](../agent/skills/revision-entrypoint-router.md) for exact rules.
Budgets belong to OPL StageAttempts, never a parallel domain counter. Exhaustion
preserves readable work and quality debt; real authority, safety, identity,
executor, irreversible-action, or explicit human-decision boundaries still stop
the affected action.

## Publication And Assets

`review_pdf`, `publication_proof`, and `final_export` remain distinct.
[Publication design](../agent/skills/publication-design.md) owns proof evidence;
[the proof gate](../agent/quality_gates/publication-proof-handoff-quality-gate.md)
owns acceptance requirements. Successful compilation or a machine nonblank-page
check cannot replace human visual review or final-export owner acceptance.
Proof-only gaps must not block narrower truthful writing or review work.

Final figures default to host-generated, project-bound bitmap assets unless the
owner chooses deterministic vectors. Chat previews and placeholders cannot prove
figure readiness. The [image handoff](../contracts/image_asset_host_handoff.json)
allows Book Forge to read and validate only the injected contained bitmap and
return receipt/manifest candidates; it cannot generate, copy, or persist assets,
discover providers, or spawn executors. Framework persists candidates.

Use [artifact-lifecycle handoff](../contracts/artifact_lifecycle_handoff.json)
and [Temporal consumption](../contracts/temporal_stage_run_consumption_policy.json)
for refs-only currentness and default entry. Evidence packages are output refs,
never execution shortcuts. Current claim limits belong to [Status](./status.md).
