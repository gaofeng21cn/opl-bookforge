# Chapter Materialization Prompt

Goal: produce reader-facing chapter Markdown packages from approved chapter task cards and context packs.

Primary open judgment: whether each active chapter unit has enough task-card, context, source, style, target extent, and memory refs to become honest book prose or must remain in-progress/blocked.

Use the professional method layer when needed:

- `bookforge-chapter-author` for reader-entry plans, chapter drafting, repair, chapter QC, and review-PDF eligibility.
- `bookforge-source-reference-reviewer` only to classify a claim-level blocker that prevents drafting the affected passage.
- `bookforge-story-style-architect` only when chapter function, reader-style, or stance gaps must route back.

Produce these refs:

- chapter context pack and trace for each active production chapter.
- reader-entry plan in chapter brief or drafting notes, not visible manuscript prose.
- per-chapter Markdown draft refs or explicit `seed_in_progress` / `draft_in_progress` refs when below target.
- chapter QC refs covering function, reader-facing prose, extent, figure/table obligations, internal-language leakage, and repair needs.
- chapter repair back-propagation refs to task cards, style engine, glossary, evidence map, or semantic memory when the finding is reusable.
- completed-contiguous review-PDF eligibility marker, without generating or claiming proof/export readiness.
- handoff to `source-style-integrity-review`, route-back refs, or typed blockers.

Keep substantial manuscript body in per-chapter Markdown or equivalent author-facing refs. Do not store book prose in scripts or JSON literals, do not claim source/style/meta-review pass, and do not claim review PDF, publication proof, final export, quality acceptance, or owner acceptance.
