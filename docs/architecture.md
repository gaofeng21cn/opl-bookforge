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

## Generated Surface Boundary

The action catalog exposes `shape-storyline` and `materialize-book`. Generated MCP/OpenAI/AI SDK descriptors are interface descriptors unless a runtime surface provides execution evidence.

Scaffold validation and generated interface readiness prove the domain pack can be read by OPL. They do not prove manuscript quality, export acceptance, publication readiness, owner acceptance, or hosted runtime parity.

## Evidence Flow

OMA / Agent Lab evidence evaluates the agent baseline and improvement loop. Pilot evidence evaluates a real short-book project. Owner receipts and runtime receipts remain separate gates.
