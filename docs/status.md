# OPL Book Forge Status

Owner: `opl-bookforge`
Purpose: `current_status_and_evidence_boundary`
State: `active_truth`
Machine boundary: Source and retained evidence summary; installed, published, runtime, and domain acceptance require their own fresh readback.

## Source State

`package.json` and `contracts/opl_agent_package_manifest.json` declare source
version `0.3.12` and Package identity `obf`. Version metadata is not a release or
installed-state receipt.

The action catalog exposes `shape-storyline` and `materialize-book`. The current
five-stage graph, isolated Review adoption, refs-only handoffs, PDF helper, and
read-only figure authority handler are represented in contracts and source;
their ownership and mechanisms are described in [Architecture](./architecture.md).

The manifest declares
`ghcr.io/gaofeng21cn/one-person-lab-packages/obf:latest-stable` as the configured
carrier publication locator. Shared tooling may generate refs, digests, and
channels without taking Book Forge's publication decision or Package authority.
The locator and source metadata alone do not establish published or installed
currentness; neither the namespace nor the absence of a repo-local publishing
workflow establishes a migration requirement.

## Live Stage Progress Evidence

`contracts/live_stage_run_progress_evidence.json` is `owner_evidence_required`
with no accepted current-topology live refs. The short-book pilot used the older
two-stage topology; its artifacts cannot be remapped into five-stage evidence.

## Production Acceptance Tail

`contracts/production_acceptance/bookforge-production-acceptance.json` exposes
the historical pilot's typed owner blockers to conformance. It closes the
required contract surface, not the acceptance it describes.

| Evidence still required | Owner and closure evidence |
| --- | --- |
| Current five-stage execution | Framework runtime and Book Forge: actual StageRun/Attempt, review, route-back, and closeout refs |
| Real long-book workflow | Book project owner: a chapter-sharded run and inspectable manuscript/review artifacts |
| Publication-proof visual acceptance | Publication reviewer: inspection of exact proof bytes with required design, asset, and page refs |
| Final export and owner acceptance | Book/export owner: explicit acceptance receipts or a specific unresolved decision |
| Hosted artifact-handoff parity | Runtime/release owner: fresh hosted execution and artifact/receipt parity |

The [evidence index](./evidence/README.md) locates retained OMA Agent Lab material
and the historical owner-blocked pilot. They remain evidence of their original
scope, not a continuously refreshed test result.

## Claim Boundary

Repository validation establishes only the contract, helper, or structural
surface actually checked. It does not establish book quality, publication
approval, final-export readiness, owner acceptance, current live execution,
hosted parity, workspace lifecycle apply, physical deletion authority, or
production readiness. Run the [verification commands](../README.md#verification)
for new changes and read the relevant owner receipts for wider claims.
