# OPL Book Forge Agent Pack

Owner: `opl-bookforge`
Purpose: `human_readable_agent_pack_index`
State: `active_support`
Machine boundary: 本文是人读入口。机器 locator 归 `contracts/capability_map.json` 与 `contracts/pack_compiler_input.json`；本文不作为 runtime、generated surface、owner receipt、typed blocker、publication verdict 或 manuscript authority。

Stable entrypoints:

- Primary Codex entry: `agent/primary_skill/SKILL.md`
- Workflow-level professional skills: `agent/professional_skills/README.md`
- Domain skill declarations: `agent/skills/README.md`
- Stage prompts: `agent/prompts/README.md`
- Knowledge, principles, quality gates, stages, tools, and policies: sibling README files under `agent/`

Boundary:

- `agent/primary_skill/SKILL.md` is the default Codex-facing Book Forge source entry.
- `agent/prompts/*.md` carries each Stage's complete task: objective, relevant
  context, substantive work, professional dependencies, accepted result, and
  continuation judgment.
- `agent/professional_skills/*/SKILL.md` contains reusable methods selected by
  that task. The chapter-author Skill supports both production planning and
  manuscript writing, with each method scoped to its calling Stage.
- `agent/skills/*.md` contains domain skill declarations and policy refs consumed by OPL-generated surfaces.
- No file under `agent/` authorizes manuscript quality, publication readiness, final export readiness, production readiness, memory acceptance, owner acceptance, runtime queues, provider attempts, owner receipts, or typed blockers.
