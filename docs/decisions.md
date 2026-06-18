# OPL BookForge Decisions

Owner: `opl-bookforge`
Purpose: `decisions`
State: `active_truth`
Machine boundary: Human-readable decision log. Machine truth remains in contracts, agent pack files, OPL validator output, OMA evidence, pilot evidence, runtime receipts, owner receipts, and typed blockers.

- Adopt `OPL BookForge` as the product name and `opl-bookforge` as the repo slug, `domain_id`, and `foundry_agent_id`.
- Follow the OPL series repo naming style used by `opl-meta-agent`, `opl-flow`, `opl-hermes-shell`, `opl-aion-shell`, and `opl-doc`.
- Adopt OPL standard domain-agent scaffold v1 and standard stage pack v2.
- Keep this repo as a declarative domain pack plus minimal authority functions.
- Model the book-writing workflow as two primary stages: `storyline-architecture` and `book-materialization`.
- Treat structural validation as L4 baseline evidence only; do not use it as book quality, production readiness, publication readiness, or owner acceptance evidence.
- Use OMA Agent Lab takeover, independent AI reviewer evaluation, and external-suite self-evolution as required new-agent baseline evidence. Scaffold/interface readiness alone is not a delivered-agent claim.
- Treat the 2026-06-18 real short-book pilot as evidence for two-stage workflow execution, manuscript/export generation, quality checks, and owner-gate blocker handling. It does not authorize a production-ready claim.
- Keep App/default product exposure separate until a product owner decision and App-owned contracts add BookForge to visible default routes.
