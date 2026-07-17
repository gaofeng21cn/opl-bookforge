# OPL Book Forge Ideal State Gap Plan

Owner: `opl-bookforge`
Purpose: `single_active_truth_plan`
State: `active_truth_owner`
Machine boundary: Human-readable development baton. Machine truth remains in contracts, agent pack files, source, tests, OPL validator/readback output, runtime receipts, owner receipts, and typed blockers.

This is Book Forge's only Active Truth owner. It is rewritten from current repository truth and contains no execution log, closeout ledger, release claim, owner verdict, or evidence-package transcript.

## Ideal-State Reference

Book Forge is an OPL-standard domain package for long-form book authoring. It keeps book semantics and artifact authority local while consuming OPL-owned runtime and generated surfaces. Its durable target is:

- storyline-first planning followed by chapter-sharded Markdown production, independent source/style review, and publication-proof handoff;
- reader/style, source/claim, figure/table, book-memory, revision, proof, export, and owner-gate refs that stay inspectable;
- a clear split between review PDF, publication proof, final export, and owner acceptance;
- no private generic runtime, scheduler, queue, attempt ledger, workspace lifecycle, package manager, hosted shell, or second truth source.

The durable target and hard boundaries live in [Project](../project.md), [Architecture](../architecture.md), [Invariants](../invariants.md), and [Decisions](../decisions.md). This plan derives only current state, current gaps, and the next prompt.

<a id="current-completion-progress"></a>
## Current State Summary

| Theme | Current state | Truth owner |
| --- | --- | --- |
| Identity and public actions | `obf`; `shape-storyline` and `materialize-book` | package/action contracts |
| Stage topology | Five-stage graph with storyline as the ordinary default and materialization entering planning | stage manifest and golden-path contract |
| Domain/runtime split | Book Forge owns book truth and verdict refs; OPL owns generic runtime, transport, generated surfaces, and lifecycle projection | architecture and boundary contracts |
| Long-book structure | Chapter-sharded Markdown, task/context/QC/memory refs, merge and handoff rules are represented | invariants, skills, gates, and contracts |
| Revision routing | Book Forge owns repair-level decisions; OPL transports opaque refs | revision skill and handoff contract |
| Proof/export plumbing | Review/proof/final-export accounts and real PDF helper lanes are separated | proof skills, helper, profiles, and tests |
| Evidence packages | OMA material and one historical two-stage short-book pilot are retained as evidence, not current topology truth | evidence index and package manifests |
| Documentation lifecycle | One status owner, one Active Truth owner, one docs index, one history index, and one evidence index | `docs/README.md` and this plan |

## Current State vs Ideal Gaps

No confirmed functional or structural gap is open in the current repository snapshot. The previous active list mostly repeated landed contracts or maintenance invariants; those facts now live in their canonical owners instead of remaining as perpetual gaps.

The following evidence accounts remain open but are not repo-structure gaps:

| Open evidence account | Current blocker owner | What would close it |
| --- | --- | --- |
| Current five-stage Live StageRun | OPL runtime plus Book Forge/owner receipts | accepted current-topology run, review, route-back, and closeout refs |
| Real long-book evidence | Book Forge project owner | a real chapter-sharded book run with bounded claims and reviewable artifacts |
| Publication-proof visual acceptance | Book Forge publication reviewer/owner | human visual review over exact proof bytes and required proof refs |
| Final export and owner acceptance | Book/export owner | explicit acceptance receipt or a precise route-back/blocker |
| Hosted artifact-handoff parity | OPL runtime/release owner | live hosted readback and exact artifact/receipt parity evidence |
| Physical delete authorization | owning runtime/default-caller surfaces | fresh replacement and no-active-caller evidence plus owner authorization |

These accounts must remain fail-closed. Docs, contract validation, helper output, rendered pages, historical pilot artifacts, OMA evidence, or a clean doctor result cannot close them.

## Next-Round Agent Prompt

```text
Task: run the next OPL Book Forge development audit from the single Active Truth plan.
Cwd: /Users/gaofeng/workspace/opl-bookforge
Goal: preserve Book Forge's domain authority and identify only fresh, evidence-backed functional or structural gaps; do not turn later evidence accounts into perpetual repo TODOs.
Write scope: contracts/**, agent/**, runtime/native_helpers/**, tests/**, scripts/verify.sh, README*.md, and docs/** only when the selected gap requires them.
Non-goals: do not add generic OPL runtime, scheduler, queue, provider-attempt ledger, hosted shell, private workspace lifecycle, OS/TeX package manager, manuscript or memory authority outside Book Forge, retired public surfaces, or owner/publication/production claims without receipts.
Live truth inputs: AGENTS.md, contracts/**, agent/**, runtime/native_helpers/**, tests/**, scripts/verify.sh, OPL validator/readback output, owner receipts or typed blockers when present, docs/status.md, and this plan.
Required actions: fresh-check branch, remote, dirty worktrees, and owner write sets; build an authority-aware matrix; select a 3-7 item safe batch or return no_safe_batch_matrix; implement against the semantic owner; remove closed gaps from this plan; route live-run, long-book, visual, export, hosted-parity, and owner evidence to their evidence owners.
Verification commands: scripts/verify.sh full for contract/source changes; the narrowest repo-native lane for docs-only changes; git diff --check; OPL Doc doctor as a read-only risk map; relative Markdown link scan.
Completion gate: land verified bytes on main, push and read back the remote ref, remove task worktrees/branches, and keep runtime/release/owner/publication/production claims fail-closed without their own evidence.
Foldback target: docs/active/bookforge-ideal-state-gap-plan.md
```

## Coverage Ledger

- Current governed owners: both root READMEs; every canonical, index, active, and reference Markdown surface.
- Historical/provenance coverage: the history index, two external-learning records, and the image-execution retirement tombstone.
- Evidence coverage: both evidence manifests and every pilot input, manuscript, stage-output, and visual-inspection Markdown payload; their old topology and paths remain historical evidence content.
- Redundant current lifecycle or process indexes: none; navigation and lifecycle roles have one docs index and one history index.
- Uncovered `README*` or `docs/**/*.md`: none.
- Remaining stale or retirement candidates: none established by current live truth.
