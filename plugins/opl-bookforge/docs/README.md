# OPL Book Forge Documentation

Owner: `opl-bookforge`
Purpose: `docs_index_and_lifecycle`
State: `active_index`
Machine boundary: Navigation and editorial lifecycle only. Contracts, executable agent inputs, source, validators, and owner/runtime receipts establish their own facts.

## Document Responsibilities

| Document | Its sole responsibility |
| --- | --- |
| [Repository entry](../README.md) / [中文](../README.zh-CN.md) | Product introduction, installation, commands, and developer starting point; both languages describe the same entry |
| [Project](./project.md) | Product scope and intended users |
| [Status](./status.md) | What current source and retained evidence can establish |
| [Architecture](./architecture.md) | Components, ownership, and data/control flow |
| [Invariants](./invariants.md) | Cross-cutting constraints and links to their domain policy owners |
| [Decisions](./decisions.md) | Rationale and consequences of durable design choices |
| [Revision handoff](./references/opl-base-revision-routing-handoff.md) | Cross-repository revision-ref transport boundary |
| [Evidence](./evidence/README.md) | Retained evidence packages and their scope |
| [Source attribution](./history/README.md) | Original external source identities supporting current design rationale |

The [agent pack](../agent/README.md) owns executable domain guidance. Its primary
Skill routes work, professional Skills carry methods, policy refs carry focused
domain rules, stage prompts specify requested results, and quality gates judge
those results. Developer docs link to those inputs instead of restating them.

## Lifecycle

Before creating or extending a document, identify its reader, question, and
existing topic owner. Extend that owner when the responsibility is the same;
create a separate document only for a distinct durable responsibility. There is
no required template or document quota.

Update source-backed claims with the owning code or contract change. Rewrite
the affected section from the current state; do not append dated progress,
next-agent prompts, verification transcripts, or cumulative coverage ledgers.
Keep accepted targets distinct from implementation and published/installed state.

Remove completed gaps after their facts have reached the current owner. Retain
history only for unique rationale, provenance, or a concrete risk of restoring a
retired design. Delete superseded prose once its useful content and incoming
references have moved; Git retains the edit history. Retired entrypoints do not
receive permanent aliases or compatibility navigation.

Create a scoped plan only for a confirmed unfinished implementation change.
Its owner and observable closure condition must be clear; remove it when closed.
Evidence still required for a claim belongs to Status, not an empty recurring
audit plan. No active implementation plan is currently retained.

Evidence payloads are frozen observations, including obsolete paths and topology.
Correct their interpretation in the evidence index or current status; never
rewrite artifact bytes or signed/hash-bound receipts to make old runs look current.

Before closing a docs change, inspect incoming references, resolve local links,
run the relevant repository checks, and compare claims with their code/receipt
owners. Mechanical checks cover paths, schemas, generated copies, and integrity;
they must not turn wording, headings, or text counts into semantic truth.
