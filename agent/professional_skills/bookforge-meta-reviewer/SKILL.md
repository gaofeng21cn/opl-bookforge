---
name: bookforge-meta-reviewer
description: Use when OPL Book Forge must independently review an assembled manuscript, route critique by repair layer, and control review-repair iteration.
---

# Book Forge Meta Reviewer

## Purpose

Run independent whole-manuscript review and route serious findings before prose edits. This skill combines `agent/skills/meta-review-loop.md`, `revision-entrypoint-router.md`, and `fast-track-revision.md`.

## Inputs

- Assembled manuscript, current metrics, hygiene refs, reader-style contract, chapter function contract, source/evidence boundaries, core model map, case evidence ladder, and publication/artifact target.
- Owner critique, reviewer critique, complete-version comparison refs, proof/visual QA findings, proof/design memory refs, source-memory route-back refs, asset/right/source freshness refs, or latest meta-review report.
- Reverse outline or enough manuscript structure to produce one.

## Outputs

- Independent `meta-review/round-N.md` or equivalent with verdict, ranked findings, locations, reader impact, repair suggestions, and required/optional/blocker split.
- Revision entrypoint decision or `revision-routing/decision-N.md` with topmost repair level.
- Reviewer-comment absorption map that classifies each finding as manuscript prose, source/claim, case material, style rule, memory update, publication design/proof QA, control-layer task, owner decision, or not adopted.
- Complete-version comparison report covering argument movement, chapter sequence, reader promise, evidence/memory deltas, proof/design implications, retained strengths, and non-transferable changes.
- Proof/design memory reuse and asset/right/source freshness obligations for findings that affect layout, visual assets, captions, notes, public-use boundaries, or artifact target.
- Repair plan, fast-track audit, typed blockers, route-back refs, and downstream freshness obligations.

## AI-First / Contract-Light Boundary

- This skill owns the flexible professional judgment: independent quality review, severity ranking, topmost repair-level selection, reviewer-comment absorption, source-memory route-back, freshness obligations, route-back choice, and owner handoff framing.
- Contracts, capability maps, metrics, hygiene refs, and stage refs only locate artifacts, declare boundaries, and preserve traceable return shapes. They must not become a second manuscript-quality verdict, publication readiness gate, owner acceptance surface, or revision decision engine.
- Route serious findings by professional diagnosis before editing. If the highest owning layer is source, memory, publication design, artifact target, or owner decision, return that route instead of polishing local prose.
- Treat the revision entrypoint as an AI routing decision. The decision must explain why the topmost owner is storyline/style, chapter authoring, source/reference, memory/publication proof, lifecycle/control, or owner decision before any local rewrite begins.

## Execution Rules

- Keep reviewer context isolated from drafting rationale as far as the environment allows.
- Use meta-review only after full draft reaches chapter and asset gates, unless the owner asks for critique of an incomplete artifact.
- For long books, inspect reverse outline, part arc, chapter sequence, recurring cases/models, target extent, and transition logic before sentence-level critique.
- Route before editing when findings may affect artifact target, storyline, outline, chapter function, evidence/model, publication design, or owner/source blockers.
- Do not paste reviewer comments straight into prose. Classify findings first, then route them to chapter Markdown, case/source collection, style rules, book memory, publication design/proof QA, control docs, or owner decision.
- Treat owner critique as absorption input: preserve owner intent, classify each point by owning repair layer, record adopted/not-adopted rationale, and keep owner/export readiness outside this skill.
- When comparing complete versions, preserve active-manuscript strengths while adopting only transferable structure, evidence, style, memory, or proof/design lessons.
- Treat proof visual QA findings as publication-design or artifact-route findings unless the defect is truly manuscript text; do not repair layout, asset, or rendered-page problems by polishing prose.
- Route source-memory, proof/design memory, asset/right/source freshness, and owner-decision defects back to their owning refs before manuscript edits when the defect changes durable truth, continuity, artifact target, or public-use boundary.
- A route-back decision must include the blocking diagnosis, target skill/ref, minimum input needed to continue, affected chapters/artifacts, and downstream freshness obligations. It is not a quality, proof, export, or owner-acceptance claim.
- Fast-track only local, evidence-bounded repairs that preserve reader-style, source stance, chapter chain, target extent, and latest review verdict.
- Cap independent review-repair at three rounds unless the owner changes policy.

## Stage Prompt Boundary

- Stage prompts can require meta-review refs and stop/pass/blocker decisions; this skill owns the review and routing method.
- `source-style-integrity-review` must not self-approve a full manuscript by summarizing the drafting stage's own quality claims.
- This skill does not replace owner review, source-material completion, publication-proof inspection, or final-export acceptance.

## Legacy Coverage

This workflow-level skill covers the retired `meta-review-loop`, `revision-entrypoint-router`, and `fast-track-revision` entries named in the purpose. Keep independent review, owner critique absorption, complete-version comparison, topmost repair routing, and iteration control together; do not restore the retired fine-grained skill directories.

## Blockers And Repair Targets

- `meta_review_missing`: run or explicitly waive independent review before full-draft handoff claim.
- `revision_entrypoint_missing`: route serious findings before manuscript edits.
- `revise_major_localized_incorrectly`: repair topmost route, not only prose.
- `reviewer_absorption_route_missing`: classify reviewer findings by repair layer before prose changes.
- `owner_critique_absorption_missing`: classify owner critique, adoption rationale, and owner-decision items before revision closure.
- `complete_version_comparison_missing`: compare supplied complete versions before broad revision closure.
- `source_memory_route_back_missing`: route durable source or memory defects before revision closure.
- `asset_rights_freshness_missing`: route asset, rights, source, caption, or note freshness defects before proof/export-facing closure.
- `proof_design_memory_stale`: refresh or route design memory before treating proof findings as closed.
- `meta_review_iteration_limit_reached`: preserve the best readable draft, unresolved findings, and owner options as quality debt after three rounds; advance or route back without a publication/export claim.
- `owner_source_blocker_only`: return owner/source decision path instead of polishing around the gap.
