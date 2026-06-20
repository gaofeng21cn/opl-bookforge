# External Learning: Revision Routing

Owner: `opl-bookforge`
Purpose: `external_learning_landing`
State: `landed_domain_contract`
Machine boundary: Human-readable learning record. Machine truth remains in contracts, agent pack files, OPL validator output, runtime receipts, owner receipts, and typed blockers.

## Sources Inspected

- Purdue OWL, Higher Order Concerns and Lower Order Concerns: https://owl.purdue.edu/owl/general_writing/mechanics/hocs_and_locs.html
- Purdue OWL, Higher Order Concerns for business writing: https://owl.purdue.edu/owl/subject_specific_writing/professional_technical_writing/prioritizing_your_concerns_for_effective_business_writing/index.html
- UNC Writing Center, Reorganizing Drafts: https://writingcenter.unc.edu/tips-and-tools/reorganizing-drafts/
- UNC Writing Center, Flow / reverse outlining: https://writingcenter.unc.edu/tips-and-tools/flow/
- Institute of Professional Editors, Types of editing: https://www.iped-editors.org/about-editing/types-of-editing/
- CMU SEI, Architecture Tradeoff Analysis Method collection: https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/
- C4 model official site: https://c4model.com/
- C4 model abstractions: https://c4model.com/abstractions

## Patterns Adopted

| External pattern | Local interpretation | Classification | Owner surface | Landing |
| --- | --- | --- | --- | --- |
| Higher-order concerns before lower-order concerns | Repair reader promise, thesis, audience, organization, and development before local prose | adopt | BookForge domain skills and gates | `agent/skills/revision-entrypoint-router.md`, meta-review and quality-gate updates |
| Reverse outline after draft | Extract actual manuscript structure before deciding whether outline/storyline repair is needed | adopt | BookForge materialization refs | `reverse-outline-ref:book-materialization/{decision_id}` |
| Developmental/structural editing before copyediting | Separate storyline/outline/chapter-function repair from local prose polish | adapt | BookForge materialization quality gate | repair entrypoint hierarchy |
| Architecture risk/tradeoff review | Classify risks and topmost affected layer before changing design | adapt | BookForge revision route decision | finding-to-level table and route-back refs |
| Hierarchical architecture views | Keep repair levels named and bounded so maintainers can reason by zoom level | adapt | BookForge docs/contracts | artifact target -> storyline -> outline -> chapter -> evidence/model -> publication design -> local prose |

## Rejected Patterns

- Importing an external writing-agent runtime, review queue, vector store, scheduler, or multi-agent controller.
- Letting OPL decide manuscript repair semantics.
- Treating a generated descriptor, review report, or route ref as quality approval.

## Local Design

The new `revision-entrypoint-router` sits between Meta Review and repair. It produces an owner-inspectable decision ref before edits:

- selected topmost repair level;
- reverse-outline evidence when organization is implicated;
- affected BookForge refs;
- allowed and forbidden lower-level edits;
- route-back refs and typed blockers;
- downstream freshness obligations.

The router preserves the existing two-stage model. If repair begins at storyline, the route goes back to `storyline-architecture`; if repair stays in materialization, it updates the relevant chapter, evidence/model, publication-design, or prose refs.

## OPL Base Handoff

OPL should support generic review-repair transport for opaque refs: `revision-entrypoint-decision-ref`, `route-back-ref`, `repair-plan-ref`, `typed-blocker-ref`, `owner-decision-ref`, freshness gates, iteration caps, and current-owner projection. OPL should not inspect manuscript semantics or own quality/export verdicts.

The handoff proposal is `docs/opl-base-revision-routing-handoff.md`.

## Learning Landing Audit

| Item | Pattern | Local owner surface | Target landing | Status | Completion | Fresh evidence | Missing refs | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Higher-order repair before prose | HOC/LOC and structural editing | BookForge skills/gates | Revision router skill and gate refs | done | 100% | `agent/skills/revision-entrypoint-router.md`, `agent/quality_gates/book-materialization-quality-gate.md` | none for domain contract | Exercise on real manuscript |
| Reverse-outline diagnostic | Reverse outlining | BookForge materialization refs | `reverse-outline-ref` in stage contract | done | 100% | `contracts/stage_control_plane.json` | no runtime artifact yet | Exercise on real manuscript |
| Architecture-style risk routing | ATAM risk/theme classification | BookForge route decision | finding-to-level table and topmost entrypoint | done | 100% | `agent/skills/revision-entrypoint-router.md` | none for domain contract | Add OPL transport when base owner accepts |
| Hierarchical repair model | C4-style named abstraction levels | Docs/contracts | repair hierarchy in architecture and invariants | done | 100% | `docs/architecture.md`, `docs/invariants.md` | none for domain contract | Use in future review reports |
| OPL base optimization | generic opaque transport | OPL owner handoff | proposal doc only | partial | 60% | `docs/opl-base-revision-routing-handoff.md` | OPL repo implementation and runtime evidence | Land in OPL base repo separately |
