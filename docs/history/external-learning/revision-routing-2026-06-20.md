# External Learning: Revision Routing

Owner: `opl-bookforge`
Purpose: `external_learning_landing`
State: `history_provenance_landed_domain_contract`
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
- Martin Fowler, Scaling the Practice of Architecture, Conversationally: https://martinfowler.com/articles/scaling-architecture-conversationally.html
- Google SRE Workbook, Postmortem Practices for Incident Management: https://sre.google/workbook/postmortem-culture/
- NASA Systems Engineering Handbook: https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf

## Patterns Adopted

| External pattern | Local interpretation | Classification | Owner surface | Landing |
| --- | --- | --- | --- | --- |
| Higher-order concerns before lower-order concerns | Repair reader promise, thesis, audience, organization, and development before local prose | adopt | Book Forge domain skills and gates | `agent/skills/revision-entrypoint-router.md`, meta-review and quality-gate updates |
| Reverse outline after draft | Extract actual manuscript structure before deciding whether outline/storyline repair is needed | adopt | Book Forge materialization refs | `reverse-outline-ref:book-materialization/{decision_id}` |
| Developmental/structural editing before copyediting | Separate storyline/outline/chapter-function repair from local prose polish | adapt | Book Forge materialization quality gate | repair entrypoint hierarchy |
| Architecture risk/tradeoff review | Classify risks and topmost affected layer before changing design | adapt | Book Forge revision route decision | finding-to-level table and route-back refs |
| Hierarchical architecture views | Keep repair levels named and bounded so maintainers can reason by zoom level | adapt | Book Forge docs/contracts | artifact target -> storyline -> outline -> chapter -> evidence/model -> publication design -> local prose |
| Decision record discipline | Keep context, decision, and consequences inspectable near the artifact | adapt | Book Forge revision route decision and docs | durable entrypoint decision refs and handoff reference |
| Postmortem/action-item discipline | Classify root cause and preventive action instead of only fixing the visible symptom | adapt | Meta Review repair plan | finding-to-level table, owner, next action, and freshness obligations |
| Systems traceability | Preserve requirement/design/verification links across major changes | adapt | Book Forge + OPL refs-only transport | route-back refs, downstream freshness refs, and projection health |

## Rejected Patterns

- Importing an external writing-agent runtime, review queue, vector store, scheduler, or multi-agent controller.
- Letting OPL decide manuscript repair semantics.
- Treating a generated descriptor, review report, or route ref as quality approval.

## Local Design

The new `revision-entrypoint-router` sits between Meta Review and repair. It produces an owner-inspectable decision ref before edits:

- selected topmost repair level;
- reverse-outline evidence when organization is implicated;
- affected Book Forge refs;
- allowed and forbidden lower-level edits;
- route-back refs and typed blockers;
- downstream freshness obligations.

The router preserves the existing two-stage model. If repair begins at storyline, the route goes back to `storyline-architecture`; if repair stays in materialization, it updates the relevant chapter, evidence/model, publication-design, or prose refs.

## OPL Base Handoff

OPL now has an initial local refs-only workspace transport for opaque review-repair refs through `opl workspace artifact-lifecycle`. It projects `revision_entrypoint_decision_ref`, `route_back_ref`, `repair_plan_ref`, `typed_blocker_ref`, `owner_decision_ref`, freshness gates, iteration caps, and current-owner shape without inspecting manuscript semantics or owning quality/export verdicts.

The handoff reference is `docs/references/opl-base-revision-routing-handoff.md`.

## Learning Landing Audit

This table is dated landing provenance. Completion values describe whether the external learning pattern landed into local Book Forge / OPL refs at the time of the audit; they are not current hosted-runtime parity, publication readiness, repair acceptance, final export acceptance, or owner acceptance claims.

| Item | Pattern | Local owner surface | Target landing | Status | Completion | Fresh evidence | Missing refs | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Higher-order repair before prose | HOC/LOC and structural editing | Book Forge skills/gates | Revision router skill and gate refs | done | 100% | `agent/skills/revision-entrypoint-router.md`, `agent/quality_gates/book-materialization-quality-gate.md` | none for domain contract | Exercise on real manuscript |
| Reverse-outline diagnostic | Reverse outlining | Book Forge materialization refs | `reverse-outline-ref` in stage contract | done | 100% | `contracts/stage_control_plane.json` | no runtime artifact yet | Exercise on real manuscript |
| Architecture-style risk routing | ATAM risk/theme classification | Book Forge route decision | finding-to-level table and topmost entrypoint | done | 100% | `agent/skills/revision-entrypoint-router.md` | none for domain contract | Add OPL transport when base owner accepts |
| Hierarchical repair model | C4-style named abstraction levels | Docs/contracts | repair hierarchy in architecture and invariants | done | 100% | `docs/architecture.md`, `docs/invariants.md` | none for domain contract | Use in future review reports |
| OPL base optimization | generic opaque transport | OPL base source/test surface | local OPL `workspace artifact-lifecycle` transport | dated_local_transport_landed | local source/test transport provenance recorded; hosted/runtime adoption remains open | `/Users/gaofeng/workspace/one-person-lab/src/workspace-artifact-lifecycle.ts`, `tests/src/cli/cases/workspace-domain.initializer.test.ts`, `docs/references/opl-base-revision-routing-handoff.md` | real Book Forge workspace runtime evidence and owner acceptance remain separate | Exercise on real manuscript workspace |
