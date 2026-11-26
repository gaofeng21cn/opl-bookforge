# OPL Book Forge Status

Owner: `opl-bookforge`
Purpose: `current_status_and_evidence_boundary`
State: `active_truth`
Machine boundary: Source and retained evidence summary; installed, published, runtime, and domain acceptance require their own fresh readback.

## Source State

[`package.json`](../package.json) and [`opl-package.json`](../opl-package.json) (`opl.package.v2`) declare Package identity `obf` and the current source version. Version metadata is not a release or installed-state receipt.

Knowledge catalogs use the shared v2 scope/content model. Both public actions
require an inventory-bound book identity, and the primary Skill consumes
Framework-bound sources and snapshots. Personal-library and local-workspace
knowledge use the same source model; source migration and live book acceptance
still require their own readback.

The isolated knowledge-scope test uses the real Framework action resolver and
source consumer: both public actions resolve registered books, shared owner/topic
knowledge is selected, and book-specific knowledge remains isolated across books.
Missing or unknown book identities are rejected. These checks run in the default
verification lane with temporary sources and state; they do not migrate a user's
library or establish manuscript acceptance.

The manuscript review contribution reads exact book-local Markdown versions,
shows headings and an optional same-book comparison, and returns source hashes
with the current task's review context. Isolated owner/adapter tests cover book
selection, cross-book rejection, stale versions, bounded previews, reopening,
carrier parity, and zero writes. This evidence does not establish a hosted
StageRun continuation or a human editorial decision.

The source includes a standard dual-format Word/PDF publication helper and a
bundled Chinese A4 profile (`review_pdf`, `publication_proof`, `final_export`),
reusing Framework file hashing, font/footnote checks, and rendered-page
inspection. Domain editorial, planning, and layout rules remain in
[Book production](../agent/skills/book-production.md) and
[Publication design](../agent/skills/publication-design.md); helper usage lives
in [Native helpers](../runtime/native_helpers/README.md). Package publication
and installed carrier currentness are verified through their own receipts.

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
