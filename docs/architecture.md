# OPL Book Forge Architecture

Owner: `opl-bookforge`
Purpose: `architecture`
State: `active_truth`
Machine boundary: Human-readable architecture boundary. Machine truth remains in contracts, agent pack files, OPL validator output, runtime receipts, OMA evidence, pilot evidence, owner receipts, and typed blockers.

## Ownership Split

This repo owns book-domain truth, manuscript quality rules, style policy, figure/table planning, export/publication verdict boundaries, artifact authority, memory body, and owner receipts.

OPL owns generated interfaces, generic runtime, queue, attempt ledger, transition runner, memory locator transport, artifact lifecycle shell, workbench, Agent Lab, work-order execution, registry/discovery, promotion gates, and observability projection.

Temporal-backed StageRun execution belongs to that OPL-owned runtime layer. Book Forge consumes StageRun, Temporal workflow, provider attempt, attempt ledger, current pointer, owner receipt, typed blocker, human gate, and route-back refs through `contracts/temporal_stage_run_consumption_policy.json`; it must not create a private Temporal runtime, StageRun wrapper, queue, provider completion store, scheduler, session store, or attempt ledger.

The same policy is also the positive export boundary for OPL generated surfaces: Book Forge exposes book-domain action contracts, chapter task card refs, manuscript/style/artifact authority refs, owner-gated publication/export decision refs, typed blocker refs, and owner receipt refs. It does not expose runtime status read models, private Temporal wrappers, private StageRun wrappers, private queues, private schedulers, private session stores, private provider completion stores, or private attempt ledgers.

## Stage Model

Book Forge uses a storyline default stage plus focused materialization stages:

- `storyline-architecture`: build the premise, reader promise, argument arc, source map, chapter thesis chain, style contract, and owner handoff.
- `chapter-production-planning`: direct `materialize-book` entry; admit the approved storyline closeout, route ordinary gaps back or keep them in progress, then produce target extent, chapter budgets, production queue, chapter task cards, context plan, and memory refs.
- `chapter-materialization`: produce chapter context packs, reader-entry plans, per-chapter Markdown draft refs, chapter QC, and repair back-propagation refs.
- `source-style-integrity-review`: run source/claim integrity, style consistency, AI-flavor/internal-language scan, meta-review routing, and repair entrypoint judgment.
- `publication-proof-handoff`: package review/proof/export handoff refs, figure/table readiness, rendered-page QA refs when claimed, owner decisions, blockers, and artifact-role boundaries.

The sequence is `storyline-architecture` -> `chapter-production-planning` -> `chapter-materialization` -> `source-style-integrity-review` -> `publication-proof-handoff`. Planning owns storyline-ref admission and route-back. Ordinary planning gaps stay in progress or route back with exact repair refs; an independent review receipt is not a blanket transition prerequisite.

The stage split follows the OMA-derived sizing rule: one top-level stage should own one major open judgment. Deterministic file generation, validators, helper receipts, and professional-skill method work remain inside the relevant stage; independent judgments such as planning, drafting, integrity review, and proof/export handoff are separated.

## Prompt / Professional Skill / Tool Split

The repo-owned rich primary skill lives at `agent/primary_skill/SKILL.md`. It is the standard default Codex entry for OPL Book Forge: it carries the book-level operating contract, routes to stage prompts and professional skills, and keeps the authority boundary visible to Codex users. `plugins/opl-bookforge/skills/opl-bookforge/SKILL.md` is the materialized Codex plugin carrier full copy; the carrier is transport, not the Book Forge truth owner.

Stage prompts define the goal, required refs, accepted handoff shape, and claim boundary for `storyline-architecture`, `chapter-production-planning`, `chapter-materialization`, `source-style-integrity-review`, and `publication-proof-handoff`.

Repo-local Codex professional skills under `agent/professional_skills/*/SKILL.md` carry workflow-level book-writing methods: storyline/style architecture, chapter authoring, source/reference review, meta-review, and publication/memory curation. They absorb and route the existing `agent/skills/*.md` policy refs without creating a private runtime, memory-body authority, owner acceptance, or readiness verdict. Legacy fine-grained skill entries are contract-only redirects in `contracts/capability_map.json#legacy_professional_skill_redirects`; no legacy physical `SKILL.md` or `TOMBSTONE.md` is retained for them.

Tool catalogs under `agent/tools/` describe affordances, write scope, side effects, credentials, and forbidden authority. Tools do not prescribe executor strategy, own manuscript truth, or grant readiness verdicts.

Image generation follows the same framework/domain split. Book Forge builds the figure prompt and declares the project-local output ref, then calls `opl executor run` with `required_capabilities: ["image_generation"]`. OPL Runway owns Codex discovery, capability activation, process transport, and the executor receipt. Book Forge only accepts the result after validating the declared bitmap bytes, then writes the figure receipt and asset-manifest projection; publication, final-export, and owner-acceptance authority remain in Book Forge.

## Revision Architecture

Book Forge treats serious critique and independent meta-review as a routed repair system, not a local prose queue. After a full-manuscript meta-review, complete-version comparison, or serious owner/reviewer critique, the domain pack first records a revision entrypoint decision.

The repair hierarchy is:

- artifact target: decide whether the manuscript is a concise review edition, internal trial reading edition, formal publication manuscript, or another owner-approved target.
- storyline architecture: repair reader promise, primary audience, central thesis, argument arc, source map, author/source stance, or evidence burden.
- outline sequence: repair chapter order, split/merge, part structure, front matter, conclusion path, and handoffs.
- chapter function: repair a chapter's primary job, new movement, adjacent handoff, and non-repeat claims.
- evidence/model: repair claim ledgers, source locators, case evidence ladder, concept map, core model map, figures, and tables.
- publication design: repair proof target, TOC/front matter, figure stance, page profile, and rendered-page inspection plan.
- local prose: repair sentence rhythm, paragraph movement, terminology clarity, transitions, and AI-flavor residue.
- owner/source blocker: return a typed blocker when source material, authorization, owner decision, outcome evidence, publication acceptance, or final export acceptance is missing.

This hierarchy preserves owner routing while using the focused stage graph. Structural route-back goes to the owning Book Forge refs, especially `storyline-architecture` when top-level design changes; chapter-package issues route to `chapter-production-planning` or `chapter-materialization`; source/style/meta-review issues route to `source-style-integrity-review`; proof/export issues route to `publication-proof-handoff`. OPL only transports opaque route refs, blockers, receipts, and current-owner projections; it does not decide manuscript semantics or quality.

## Generated Surface Boundary

The action catalog exposes `shape-storyline` and `materialize-book`. Generated MCP/OpenAI/AI SDK descriptors are interface descriptors unless a runtime surface provides execution evidence.

Scaffold validation and generated interface readiness prove the domain pack can be read by OPL. They do not prove manuscript quality, export acceptance, publication readiness, owner acceptance, or hosted runtime parity.

Generated status/readback surfaces may project the Temporal StageRun policy flags, including `provider_completion_is_domain_completion=false` and `generated_surface_ready_counts_as_domain_ready=false`. Domain completion still requires a Book Forge owner receipt, typed blocker, human gate, or route-back ref; provider completion and StageRun readiness are transport evidence only.

## Evidence Flow

OMA / Agent Lab evidence evaluates the agent baseline and improvement loop. Pilot evidence evaluates a real short-book project. Owner receipts and runtime receipts remain separate gates.
