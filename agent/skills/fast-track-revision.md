# Fast-Track Revision Skill

Use this skill inside `book-materialization` when the owner or reviewer supplies small, well-bounded revision suggestions after a manuscript, chapter package, or review PDF already exists.

Fast-track revision is a controlled editing lane. It lets Codex CLI repair local prose, model naming, chapter boundary notes, small action lists, wording rhythm, or evidence-label clarity without starting a full independent meta-review cycle.

Eligibility:

- The suggestion preserves the approved reader-style contract, author/source stance map, core thesis, chapter thesis chain, target extent, evidence ladder, figure/table obligations, and export artifact role.
- The repair is local and auditable: affected chapter Markdown refs, style refs, model refs, or handoff refs can be named before editing.
- The repair does not introduce new factual claims, Red Bird outcome claims, interviews, authorization, user feedback, learning-effect claims, metrics, publication-proof claims, or final-export acceptance.
- The latest meta-review result is not invalidated. If the suggestion reveals a whole-book logic problem, repeated chapter-function defect, or missing evidence class that changes the review verdict, route back to the meta-review loop.
- Owner taste choices such as title, subtitle, house style, publication design preference, or source-material completion can be recorded as deferred owner decisions when they are not required for manuscript coherence.

Workflow:

1. Classify every suggestion as `accepted_fast_track`, `deferred_owner_decision`, `deferred_source_material`, `rejected_with_reason`, or `escalate_full_revision`.
2. For accepted suggestions, map the repair to manuscript chapter refs and any reusable production refs, such as chapter task cards, style engine rules, concept map, core model map, case evidence ladder, figure/table plan, or quality gate notes.
3. Edit the author-facing Markdown chapter refs or domain refs first. Regenerate assembled `book.md`, metrics, review PDF, hygiene reports, image-resolution receipts, and owner handoff refs after source changes.
4. Record a durable fast-track audit, preferably `quality/fast-track-revision-audit.md` or `quality/fast-track/round-N.md`, containing:
   - trigger and date;
   - reviewed suggestion source;
   - classification of each suggestion;
   - accepted repairs and touched refs;
   - evidence boundaries and unsupported case gaps;
   - deferred owner/source-material decisions;
   - validation commands and refreshed artifact refs.
5. Run internal-language, AI-flavor, forbidden case-stance, stale-status, figure-resolution, and freshness checks appropriate to the touched refs.

Escalate instead of fast-tracking when:

- The suggestion changes the book's central claim, chapter order, reader priority, target extent, or author/source stance.
- The repair needs new true Red Bird process cases, participant materials, interviews, enterprise feedback, learning outcomes, or authorization not already present.
- The suggestion would rewrite substantial portions of several chapters or alter the chapter function contract.
- The latest independent meta-review verdict would no longer be reliable.
- The issue concerns publication proof quality, final export acceptance, or owner publication approval.
- The executor cannot state the evidence boundary before editing.

Fast-track revision is still BookForge materialization work. It does not approve manuscript quality, publication proof, final export, or owner acceptance by itself.
