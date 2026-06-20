# OPL BookForge Architecture

Owner: `opl-bookforge`
Purpose: `architecture`
State: `active_truth`
Machine boundary: Human-readable architecture boundary. Machine truth remains in contracts, agent pack files, OPL validator output, runtime receipts, OMA evidence, pilot evidence, owner receipts, and typed blockers.

## Ownership Split

This repo owns book-domain truth, manuscript quality rules, style policy, figure/table planning, export/publication verdict boundaries, artifact authority, memory body, and owner receipts.

OPL owns generated interfaces, generic runtime, queue, attempt ledger, transition runner, memory locator transport, artifact lifecycle shell, workbench, Agent Lab, work-order execution, registry/discovery, promotion gates, and observability projection.

## Stage Model

BookForge uses two primary stages:

- `storyline-architecture`: build the premise, reader promise, argument arc, source map, chapter thesis chain, style contract, and owner handoff.
- `book-materialization`: produce the chapter draft bundle, manuscript body, figure plan, table plan, style consistency report, AI-flavor revision report, layout QC report, exports, and owner handoff.

The stage split is intentionally coarse. Each stage should produce a reviewable handoff package rather than a chain of small status updates.

## Revision Architecture

BookForge treats serious critique and independent meta-review as a routed repair system, not a local prose queue. After a full-manuscript meta-review, complete-version comparison, or serious owner/reviewer critique, the domain pack first records a revision entrypoint decision.

The repair hierarchy is:

- artifact target: decide whether the manuscript is a concise review edition, internal trial reading edition, formal publication manuscript, or another owner-approved target.
- storyline architecture: repair reader promise, primary audience, central thesis, argument arc, source map, author/source stance, or evidence burden.
- outline sequence: repair chapter order, split/merge, part structure, front matter, conclusion path, and handoffs.
- chapter function: repair a chapter's primary job, new movement, adjacent handoff, and non-repeat claims.
- evidence/model: repair claim ledgers, source locators, case evidence ladder, concept map, core model map, figures, and tables.
- publication design: repair proof target, TOC/front matter, figure stance, page profile, and rendered-page inspection plan.
- local prose: repair sentence rhythm, paragraph movement, terminology clarity, transitions, and AI-flavor residue.
- owner/source blocker: return a typed blocker when source material, authorization, owner decision, outcome evidence, publication acceptance, or final export acceptance is missing.

This hierarchy preserves the two-stage model. Structural route-back goes to the owning BookForge refs, especially `storyline-architecture` when top-level design changes. OPL only transports opaque route refs, blockers, receipts, and current-owner projections; it does not decide manuscript semantics or quality.

## Generated Surface Boundary

The action catalog exposes `shape-storyline` and `materialize-book`. Generated MCP/OpenAI/AI SDK descriptors are interface descriptors unless a runtime surface provides execution evidence.

Scaffold validation and generated interface readiness prove the domain pack can be read by OPL. They do not prove manuscript quality, export acceptance, publication readiness, owner acceptance, or hosted runtime parity.

## Evidence Flow

OMA / Agent Lab evidence evaluates the agent baseline and improvement loop. Pilot evidence evaluates a real short-book project. Owner receipts and runtime receipts remain separate gates.
