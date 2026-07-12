# OPL Standard Agent Principles Projection

Owner: `one-person-lab`
Purpose: repo-local projection of the OPL standard-agent AI-first principle pack.
State: `active_projection`
Machine boundary: this file projects the principle ids consumed by `contracts/standard-agent-principles-adoption.json`. Canonical OPL policy remains in `contracts/opl-framework/standard-agent-principles.json` and `human_doc:one-person-lab/docs/policies/standard-agent-ai-first-principles.md`.

This projection does not create a second truth source. OPL owns the shared principle vocabulary; OPL BookForge owns book truth, book quality, export/publication decisions, book memory bodies, and owner receipts.

| Principle id | Principle | Domain adoption meaning |
| --- | --- | --- |
| `ai_first_execution` | AI-first execution | AI performs open-ended book planning, comparison, drafting, review, diagnosis, and revision inside bounded stage attempts. |
| `contract_backed_boundary` | Contract-backed boundary | Contracts, schemas, tests, and readbacks guard identity, authority, inputs, outputs, evidence, and recovery. |
| `domain_truth_authority` | Domain truth authority | Book truth, quality/export verdicts, artifact authority, memory body, owner receipts, and typed blockers stay with BookForge. |
| `stage_prompt_skill_tool_separation` | Prompt / Skill / Tool separation | Stage prompts define goals and accepted answer shapes; professional skills carry book methods; tool catalogs describe affordances and limits. |
| `domain_intake_mapping` | Domain intake mapping | Domain intake is handled by the active `storyline-architecture` entry stage, not by an orphan intake stage or independent Skill. |
| `workspace_source_intake_shell` | Workspace/source shell | OPL owns generic locator and refs-only source intake transport; BookForge owns book source semantics, storyline acceptance, and owner route decisions. |
| `owner_delta_progress` | Owner-delta progress | Progress is measured by manuscript/storyline deltas, owner receipts, route-back refs, typed blockers, human gates, or handoff packets. |
| `quality_budget_progress_first` | Quality-budget progress first | A readable book artifact advances with `completed_with_quality_debt`; unresolved review/proof debt blocks quality/publication/export claims, not stage transition. |
| `parallel_executor_autonomy` | Bounded executor autonomy | Executors choose tools, iteration, and safe parallelism inside declared authority while preserving source, chapter-ready, integrity-review, and proof/export dependencies. |
| `module_organization` | Module organization | OPL brand modules hold framework primitives; BookForge is a declarative domain pack plus minimal authority functions. |

For BookForge, these ids are adopted through the book-authoring specialization in `agent/principles/domain-specialization.md` and the mapping contract in `contracts/standard-agent-principles-adoption.json`.
