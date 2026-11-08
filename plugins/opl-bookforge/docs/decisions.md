# OPL Book Forge Design Decisions

Owner: `opl-bookforge`
Purpose: `durable_design_rationale`
State: `active_truth`
Machine boundary: Accepted design choices and their reasons; contracts/source establish implementation and receipts establish acceptance.

## Package Composition

Book Forge owns one executor-neutral `obf` Package identity, descriptor, version,
and publication decisions. Shared tooling can publish complete bytes and generate
refs/digests without acquiring Package currentness authority. Carrier and executor
are separate replaceable routes, so changing either must preserve book work,
preferences, and dependency state. Ordinary dependencies use identity presence
and required capability callability. Exact checksums remain appropriate for
release integrity and reproducible offline/QA snapshots, not a cross-Package
version solver, lock, or ordinary readiness gate. Registry namespace does not
determine publication ownership or require a separate per-repository publisher.

## Stages Follow Independent Judgments

Storyline, production planning, chapter drafting, whole-book integrity review,
and proof/export handoff require different inputs and decisions. The five-stage
graph makes those responsibilities inspectable. Planning owns storyline-ref
admission; an extra routing-only stage would add no domain judgment. The graph
expresses dependencies and claim boundaries, not a mandatory recipe for every
model thought: current accepted refs may be reused and findings may route back.

## Manuscript Body Stays In Chapter Markdown

Chapter packages preserve target extent, chapter function, evidence, memory,
and local review without making generator code the authoring source. Assembly
and export consume those packages. A thin all-chapter sample is a preview; it
cannot silently replace a requested full book. Cumulative contiguous review
PDFs expose progress without hiding unfinished earlier chapters. Detailed
production policy belongs to [Book production](../agent/skills/book-production.md).

## Revision Changes Its Owning Layer

Higher-order defects must update storyline, chapter function, evidence, style,
or design refs before repair is claimed. Sentence polish cannot repair a wrong
book target or argument. Stronger references and serious critique become
reusable domain constraints while preserving evidence classes, primary readers,
reasoning density, and the author's stance. The [revision method](../agent/skills/revision-entrypoint-router.md)
owns the hierarchy; [source attribution](./history/README.md) preserves
its provenance. Methods, examples, model counts, and rhetorical techniques are
editorial judgments rather than universal numeric or phrase rules.

## Review Has Bounded, Specific Effects

Independent Stage Review checks new judgments or artifact bytes; the separate
whole-book Meta Review does not recursively review itself or edit the manuscript.
Fresh attempts review explicit refs without author conversation inheritance.
Review currentness follows semantic dependencies, so layout/export regeneration
does not invalidate unrelated content judgments. Quality budgets preserve the
best readable artifact with debt; they cannot grant publication or acceptance.
The [architecture](./architecture.md#independent-stage-review-and-whole-book-meta-review)
explains role and transition mechanics; machine policy lives in
`contracts/stage_quality_cycle_policy.json` and `contracts/epistemic_review_adoption.json`.

## Proof And Acceptance Are Separate

Review PDF, publication proof, final export, and owner acceptance answer different
questions. A real typesetting backend and inspected asset/page evidence improve
proof reliability, while human visual judgment and owner/export receipts retain
their own authority. Missing proof dependencies block that claim, not unrelated
writing. [Publication design](../agent/skills/publication-design.md) owns the
rules and [Native helpers](../runtime/native_helpers/README.md) owns operator detail.
The [source attribution](./history/README.md) preserves the exact Kami source
for proof discipline; its branding and private runtime were not adopted.

## Reuse Framework Execution And Lifecycle

Book Forge keeps manuscript, source, memory, quality, and acceptance bodies.
Framework executes attempts and transports opaque refs, including lifecycle and
revision handoff. This avoids a private scheduler, package manager, hidden
memory store, or second currentness system. Figure generation/materialization
is Framework work; Book Forge's contained-bitmap handler only evaluates the
injected asset and returns candidates. The former repo-local image executor and
project-hygiene implementation were removed; their source is available in Git
history, with no compatibility or resume path.
