# OPL Book Forge Professional Skills

Repo-local professional skills are workflow-level method entries. They stay internal to OPL Book Forge and are invoked from the primary skill or stage runtime; they are not global Codex default skills.

Canonical workflow skills:

- `bookforge-story-style-architect`: storyline, reader contract, chapter function, author/source stance, and reusable prose style.
- `bookforge-chapter-author`: chapter context pack, task card, reader-entry plan, chapter Markdown drafting/repair, QC, and review-PDF eligibility.
- `bookforge-source-reference-reviewer`: source locators, claim ledger, evidence classes, unsupported gaps, anti-leakage, and stronger reference absorption.
- `bookforge-meta-reviewer`: independent meta-review, revision entrypoint routing, reviewer-comment absorption, and fast-track eligibility.
- `bookforge-publication-memory-curator`: working/episodic/semantic memory, review PDF, publication proof, final export boundaries, figures/tables, and rendered-page QA.

Legacy entries are retained only as tombstone redirects for older prompts or operator habits. Their machine-readable coverage lives in `contracts/capability_map.json#legacy_professional_skill_redirects`. Do not add them to `contracts/capability_map.json` or `contracts/pack_compiler_input.json` as independent canonical capabilities.

| Legacy entry | Canonical coverage |
| --- | --- |
| `bookforge-story-architect` | `bookforge-story-style-architect` |
| `bookforge-reader-style-designer` | `bookforge-story-style-architect` |
| `bookforge-style-editor` | `bookforge-story-style-architect` |
| `bookforge-reference-absorber` | `bookforge-source-reference-reviewer` |
| `bookforge-source-claim-reviewer` | `bookforge-source-reference-reviewer` |
| `bookforge-book-memory-curator` | `bookforge-publication-memory-curator` |
| `bookforge-publication-designer` | `bookforge-publication-memory-curator` |

None of these skills can authorize manuscript quality, publication readiness, final export readiness, production readiness, memory acceptance, owner acceptance, runtime queues, provider attempts, owner receipts, or typed blockers.
