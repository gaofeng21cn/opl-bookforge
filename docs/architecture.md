# OPL Book Forge Architecture

Owner: `opl-bookforge`
Purpose: `architecture`
State: `active_truth`
Machine boundary: Human-readable architecture boundary. Machine truth remains in contracts, agent pack files, OPL validator output, runtime receipts, OMA evidence, pilot evidence, owner receipts, and typed blockers.

## Ownership Split

This repo owns book-domain truth, manuscript quality rules, style policy, figure/table planning, export/publication verdict boundaries, artifact authority, memory body, and owner receipts.

OPL owns generated interfaces, generic runtime transport, queue, attempt ledger, memory locator transport, artifact lifecycle shell, workbench, Agent Lab, work-order execution, registry/discovery, promotion gates, and observability projection. Codex CLI alone selects semantic stage routes; OPL has no transition runner or route oracle.

## Implementation And Reference Boundary

`contracts/pack_compiler_input.json#/implementation_profile` is the machine-readable implementation boundary. Canonical Agent and OPL Package identity is `obf`, declared by `pack_compiler_input.canonical_agent_id` and package manifest `agent_id/package_id`. Repo, domain, Foundry consumer, npm package, Codex plugin, and existing distribution carrier locators remain `opl-bookforge`; they do not define a second package identity. Agent identity comes only from the Markdown/JSON Declarative Standard Agent Pack; Python is a replaceable publishing-helper implementation, not an Agent type, identity, runtime owner, or publication verdict authority.

The declared helper lane is:

| helper | language | allowed role | source refs |
| --- | --- | --- | --- |
| publishing helper family | Python | PDF/publication-proof materialization, rendered-page evidence, and project-local figure assets | `runtime/native_helpers/` |

`implementation_profile.helpers` keeps the helper optional, language-neutral at the Agent identity layer, and excludes Rust from domain-agent implementations. OPL owns helper execution transport, executor discovery, generated surfaces, and generic runtime. `generic_runtime`, `generic_cli`, and `generic_workbench` remain forbidden through the existing functional privatization/source-purity gates even if a checkout contains scripts or diagnostic residue. The top-level `reference_implementation` contract marks Book Forge as a golden-fixture/reference role only: it is not the standard owner, cannot define Framework identity/contracts, and cannot become a second standard source.

Temporal-backed StageRun execution belongs to that OPL-owned runtime layer. Book Forge consumes StageRun, Temporal workflow, provider attempt, attempt ledger, current pointer, owner receipt, typed blocker, human gate, and route-back refs through `contracts/temporal_stage_run_consumption_policy.json`; it must not create a private Temporal runtime, StageRun wrapper, queue, provider completion store, scheduler, session store, or attempt ledger.

The same policy is also the positive export boundary for OPL generated surfaces: Book Forge exposes book-domain action contracts, chapter task card refs, manuscript/style/artifact authority refs, owner-gated publication/export decision refs, typed blocker refs, and owner receipt refs. It does not expose runtime status read models, private Temporal wrappers, private StageRun wrappers, private queues, private schedulers, private session stores, private provider completion stores, or private attempt ledgers.

## Stage Model

Book Forge uses a storyline default stage plus focused materialization stages:

- `storyline-architecture`: build the premise, reader promise, argument arc, source map, chapter thesis chain, style contract, and owner handoff.
- `chapter-production-planning`: direct `materialize-book` entry; admit the approved storyline closeout, route ordinary gaps back or keep them in progress, then produce target extent, chapter budgets, production queue, chapter task cards, context plan, and memory refs.
- `chapter-materialization`: produce chapter context packs, reader-entry plans, per-chapter Markdown draft refs, chapter QC, and repair back-propagation refs.
- `source-style-integrity-review`: run source/claim integrity, style consistency, AI-flavor/internal-language scan, meta-review routing, and repair entrypoint judgment.
- `publication-proof-handoff`: package review/proof/export handoff refs, figure/table readiness, rendered-page QA refs when claimed, owner decisions, blockers, and artifact-role boundaries.

The sequence is `storyline-architecture` -> `chapter-production-planning` -> `chapter-materialization` -> `source-style-integrity-review` -> `publication-proof-handoff`. Planning owns storyline-ref admission and route-back. The planning StageRun launches an independent reviewer Attempt, but a reviewer `pass` is not a hard transition prerequisite: ordinary gaps may route back or close as explicit quality debt when a readable plan exists.

The stage split follows the OMA-derived sizing rule: one top-level stage should own one major open judgment. Deterministic file generation, validators, helper receipts, and professional-skill method work remain inside the relevant stage; independent judgments such as planning, drafting, integrity review, and proof/export handoff are separated.

## Prompt / Professional Skill / Tool Split

The repo-owned rich primary skill lives at `agent/primary_skill/SKILL.md`. It is the standard default Codex entry for OPL Book Forge: it carries the book-level operating contract, routes to stage prompts and professional skills, and keeps the authority boundary visible to Codex users. `plugins/opl-bookforge/skills/opl-bookforge/SKILL.md` is the materialized Codex plugin carrier full copy; the carrier is transport, not the Book Forge truth owner.

Stage prompts define the goal, required refs, accepted handoff shape, and claim boundary for `storyline-architecture`, `chapter-production-planning`, `chapter-materialization`, `source-style-integrity-review`, and `publication-proof-handoff`.

Repo-local Codex professional skills under `agent/professional_skills/*/SKILL.md` carry workflow-level book-writing methods: storyline/style architecture, chapter authoring, source/reference review, meta-review, and publication/memory curation. They absorb and route the existing `agent/skills/*.md` policy refs without creating a private runtime, memory-body authority, owner acceptance, or readiness verdict. Legacy fine-grained skill entries are contract-only redirects in `contracts/capability_map.json#legacy_professional_skill_redirects`; no legacy physical `SKILL.md` or `TOMBSTONE.md` is retained for them.

Tool catalogs under `agent/tools/` describe affordances, write scope, side effects, credentials, and forbidden authority. Tools do not prescribe executor strategy, own manuscript truth, or grant readiness verdicts.

Image generation follows the same framework/domain split. OPL owns capability activation, executor selection and transport, the workspace output slot, bitmap materialization, attempt/output refs, and candidate persistence. The Book Forge handler registered as `handler:obf.figure-asset-authority-evaluate` consumes only the host-injected relative bitmap ref, SHA-256 digest, attempt/output refs, and figure metadata. It validates containment, regular-file identity, bitmap structure, format, dimensions, and digest, then returns either a figure-authority receipt candidate or quality debt. It does not create execution requests, spawn OPL/Codex, generate or copy bitmap bytes, or persist receipts/manifests. Publication, final-export, and owner-acceptance authority remain in Book Forge.

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
- owner/source gap: preserve any manuscript or diagnostic, record quality debt, and let Codex continue or route back when source material, outcome evidence, publication acceptance, final export acceptance, or readable bytes are missing. Use a typed blocker only for protected-material authorization, real authority/safety/permission, wrong-target identity/currentness, irreversible action, executor unavailability, or an explicit owner decision that must occur before the requested action.

This hierarchy preserves owner routing while using the focused stage graph. Structural route-back goes to the owning Book Forge refs, especially `storyline-architecture` when top-level design changes; chapter-package issues route to `chapter-production-planning` or `chapter-materialization`; source/style/meta-review issues route to `source-style-integrity-review`; proof/export issues route to `publication-proof-handoff`. OPL only transports opaque route refs, blockers, receipts, and current-owner projections; it does not decide manuscript semantics or quality.

## Generated Surface Boundary

The `family-action-catalog.v2` catalog exposes `shape-storyline` and `materialize-book` as public stage actions. Each action declares only `execution_binding={kind: stage_binding, stage_manifest_ref: agent/stages/manifest.json}`; the action's own `stage_route` keeps its entry and required stage refs. The domain pack does not carry a `source_command`, action-level handler id/ref, or surface-specific command; OPL generates the canonical `opl agents run --domain opl-bookforge --action <action_id> --workspace <absolute_path>` entry and hosted surface kinds. Generated MCP/OpenAI/AI SDK descriptors remain interface descriptors unless a runtime surface provides execution evidence.

Scaffold validation and generated interface readiness prove the domain pack can be read by OPL. They do not prove manuscript quality, export acceptance, publication readiness, owner acceptance, or hosted runtime parity.

Generated status/readback surfaces may project the Temporal StageRun policy flags, including `provider_completion_is_domain_completion=false` and `generated_surface_ready_counts_as_domain_ready=false`. Domain completion still requires a Book Forge owner receipt, typed blocker, human gate, or route-back ref; provider completion and StageRun readiness are transport evidence only.

## Evidence Flow

OMA / Agent Lab evidence evaluates the agent baseline and improvement loop. Pilot evidence evaluates a real short-book project. Owner receipts and runtime receipts remain separate gates.

## Independent Stage Review And Whole-Book Meta Review

Book Forge binds `official_high_value_knowledge_deliverable.v1`, while formal Review is an explicit per-Stage risk decision rather than a blanket rule. `storyline-architecture`, `chapter-production-planning`, and `chapter-materialization` use isolated producer, reviewer, repairer, and re-reviewer Attempts because they create open judgments or manuscript bytes. `source-style-integrity-review` is already the independent Meta Review StageRun and does not recursively review itself. `publication-proof-handoff` retains the full Review loop because it generates or transforms final PDF/export bytes, freezes their canonical identity, and can support publication/export/ready claims. Same-thread checking is only `in_thread_refinement`; a protocol closeout resume cannot produce a Review receipt.

Within `publication-proof-handoff`, producer and repairer outputs remain `review_pending` candidates. Any regeneration invalidates the prior receipt. Only a controller-materialized Review receipt bound to a fresh reviewer Attempt for unchanged producer bytes or a fresh re-reviewer Attempt for repaired bytes can close Review against the exact current hashes; downstream owner/export acceptance remains a separate Book Forge authority.

Cross-Stage routing remains a Codex domain judgment. The semantic owner is the
single `decisive_codex_attempt`: the producer for a primary-only StageRun,
otherwise the terminal reviewer or re-reviewer. Producer and repairer Attempts
inside formal Review can only recommend a route. A reviewer or re-reviewer with
`repair_required` continues the local loop while budget remains when the current
Stage is the narrowest repair owner. If a different declared Stage is the
narrowest owner, it may instead decisively route back to that Stage before
budget exhaustion; this is the only permitted pre-exhaustion terminal route for
`repair_required`. A final-budget reviewer or re-reviewer with consumable bytes
remains decisive while preserving outcome `repair_required`.
Machine output is `route_impact.stage_route_decision` or
`stage_route_recommendation`. The OPL StageRun controller owns only transition
validation and materialization; it does not rewrite Book Forge editorial or
publication semantics.

`source-style-integrity-review` keeps its stable ID and acts as the independent whole-book Meta Review and integrity gate. It consumes exact manuscript/artifact hashes, Stage Review receipts, source/reader-style/rubric refs, and necessary lineage only. It routes defects to the earliest owning storyline, planning, or materialization Stage and never edits manuscript artifacts inside the Meta Review Stage. Three exhausted repair/route-back rounds with a readable manuscript produce quality debt, which still closes publication/export/ready claims.

Within a formal Stage Review cycle, the initial reviewer creates stable findings and repair expectations but does not create the repair map. The repairer returns the per-finding repair map and changed artifact refs. A fresh re-reviewer closes each prior finding against the changed bytes; only an unclosed required finding, repair regression, or critical new finding can consume another repair round. Ordinary new suggestions remain optional observations or quality debt and cannot restart the loop.
