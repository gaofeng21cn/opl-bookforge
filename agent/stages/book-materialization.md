# Book Materialization Stage

Stage id: `book-materialization`
Action ref: `materialize-book`

This stage owns the second half of the workflow. It turns the storyline into book deliverable refs: chapter briefs, per-chapter Markdown drafts, a merged manuscript, illustration plan, tables, style pass, wording pass, layout checks, and handoff.

Quality control covers Markdown-first chapter sharding, target extent, content consistency, writing style consistency, terminology, source grounding, illustration/table fit, typography, pacing, and owner decisions. The stage returns typed blockers when manuscript body refs, target extent evidence, data refs, project-local image assets, image rights, layout target, or owner gate evidence is missing.
