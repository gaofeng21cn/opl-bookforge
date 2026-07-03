# OPL Book Forge Principles

Owner: `opl-bookforge`
Purpose: book-authoring specialization of the OPL standard-agent AI-first principle pack.
State: `active_domain_specialization`
Machine boundary: this is a human-readable domain specialization. Machine-readable adoption is in `contracts/standard-agent-principles-adoption.json`; book artifacts, quality gates, publication decisions, memory bodies, receipts, and verification outputs remain the authority surfaces.

OPL Book Forge adopts the OPL principles as a book authoring Foundry Agent:

- Intake is the `domain_intake` stage/prompt policy and starter handoff into `storyline-architecture`, not a standalone Skill. It should produce source refs, storyline work refs, route-back refs, human gates, owner receipts, or typed blockers.
- Storyline architecture and book materialization are AI-first stages. They own narrative structure, chapter planning, source-claim integrity, style consistency, figure/table plans, draft materialization, and revision loop semantics.
- Book quality, export/publication readiness, memory body, artifact body, and owner acceptance remain Book Forge authority. OPL scaffold or interface validation proves structure only, not production readiness or book delivery readiness.
- `agent/stages/`, `agent/prompts/`, `agent/skills/`, `agent/quality_gates/`, `agent/knowledge/`, and `agent/tools/domain_affordances.md` are the declarative book pack. Native helpers may materialize refs and run doctors, but cannot replace book judgment.
- Publication design, source-claim integrity, style calibration, and meta-review are domain strategies and gates. Mechanical checks return evidence or blockers; they do not issue book-ready or publish-ready verdicts.

This specialization keeps book creation AI-first while preserving the owner gate for real publication and delivery decisions.
