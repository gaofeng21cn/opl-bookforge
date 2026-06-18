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
- Route missing human acceptance as owner receipt blockers or typed blockers, not as silent success.
- Treat generated MCP/OpenAI/AI SDK surfaces as descriptors until direct runtime execution evidence exists.
