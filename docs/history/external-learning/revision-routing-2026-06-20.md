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

At the time of this learning record, the router was landed against the then-current two-stage model. That topology is historical. The current five-stage route and repair owners are defined by `agent/stages/manifest.json`, current skills, contracts, architecture, and the active handoff reference.

## OPL Base Handoff

OPL now has an initial local refs-only workspace transport for opaque review-repair refs through `opl workspace artifact-lifecycle`. It projects `revision_entrypoint_decision_ref`, `route_back_ref`, `repair_plan_ref`, `typed_blocker_ref`, `owner_decision_ref`, freshness gates, iteration caps, and current-owner shape without inspecting manuscript semantics or owning quality/export verdicts.

The handoff reference is `docs/references/opl-base-revision-routing-handoff.md`.

## Landing Provenance

This record only preserves the external-learning decision: higher-order repair before prose, reverse-outline diagnostic, architecture-style risk routing, hierarchical repair naming, and opaque OPL transport refs were adopted or adapted into Book Forge owner surfaces. Current rules now live in `agent/skills/revision-entrypoint-router.md`, the five current stage quality gates, `agent/stages/manifest.json`, `contracts/artifact_lifecycle_handoff.json`, `docs/architecture.md`, `docs/invariants.md`, and `docs/references/opl-base-revision-routing-handoff.md`.

The old row-by-row landing audit is intentionally not kept here. It was dated provenance and must not be read as current hosted-runtime parity, publication readiness, repair acceptance, final export acceptance, or owner acceptance. Real manuscript workspace evidence and owner acceptance remain later evidence lanes under the active gap plan.
