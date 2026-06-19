# OPL BookForge Invariants

Owner: `opl-bookforge`
Purpose: `invariants`
State: `active_truth`
Machine boundary: Human-readable hard constraints. Machine truth remains in contracts, agent pack files, OPL validator output, runtime receipts, owner receipts, and typed blockers.

- Do not store runtime artifacts in repo source.
- Do not implement generic OPL runtime primitives in this domain repo.
- Do not let OPL write domain truth, memory body, or quality/export verdicts.
- Do not claim production-ready book writing, publication approval, owner acceptance, or export acceptance from scaffold validation, interface descriptors, OMA evidence, pilot exports, or rendered pages alone.
- Keep `storyline-architecture` and `book-materialization` as the two primary stages unless a future decision records a stronger owner-reviewed stage model.
- Keep writing-quality checks focused on style consistency, concrete language, affirmative editorial phrasing, evidence grounding, figure/table completeness, layout, and handoff readiness.
- Keep book prose Markdown-first: per-chapter Markdown refs own manuscript body for book-length work; scripts may assemble, count, validate, export, and report but must not be the source of truth for substantial prose.
- Keep book-length drafting chapter-sharded by default: chapter brief, chapter draft, chapter QC, merged manuscript, whole-book pass. A monolithic creative source file requires explicit owner approval.
- Retire invalid compact/sample drafts when the owner requires a book-length restart; do not expand an invalid compact draft in place as the active workflow.
- Keep long-form materialization auditable with a pipeline contract that names chapter packages, chapter QC refs, figure asset manifest, table plan, whole-book review, export refs, blockers, and retired drafts.
- Preserve owner/source-declared target extent during materialization; compact/sample drafts require explicit owner approval or a typed extent blocker.
- Treat final book-bound artwork as `imagegen`-generated bitmap assets by default; SVG, local-script diagrams, and placeholders are planning aids only unless the owner explicitly requests deterministic vector output.
- Treat chat previews or generated artwork without an exposed, project-local file path as image-asset blockers, not as completed figure evidence.
- Route missing human acceptance as owner receipt blockers or typed blockers, not as silent success.
- Treat generated MCP/OpenAI/AI SDK surfaces as descriptors until direct runtime execution evidence exists.
