# Style Engine Skill

Use this skill when BookForge needs a durable writing style asset rather than one-off prompt wording.

Working policy:

- The style engine is a domain artifact contract, not a private model router or runtime control plane.
- Build the style engine from the reader-style contract, owner examples, comparable works, source constraints, and chapter QC findings.
- When the owner supplies a stronger prior version or reference draft, create a `reference-draft-absorption` ref and fold transferable craft patterns into the style engine before drafting or rewriting more chapters.
- Keep the style engine explicit and reusable across chapters:
  - audience stance
  - vocabulary boundary
  - sentence rhythm
  - paragraph movement
  - example density
  - theory-to-practice ratio
  - permitted metaphors
  - forbidden voice patterns
  - anti-AI-flavor repair rules
  - terminology and naming rules
  - reference-derived book-prose rules, including chapter-opening patterns, paragraph movement, example density, transition rhythm, case treatment, figure/table prose integration, and reader-facing completion cues
- Store the style engine as a ref that chapter prompts, chapter QC, wording repair, and publication proof can cite. Do not bury it only in a long prompt.
- Let style evolve through reviewed deltas. When a chapter repair reveals a recurring style defect, update the style engine with the defect, replacement pattern, and evidence ref.
- Let reference comparisons evolve style through reviewed deltas. Record what the reference does better, why it fits the declared primary readers, how BookForge will adopt it, and which patterns are explicitly not adopted.
- Keep style quality tied to the declared readers. A passage is not "natural" in the abstract; it is natural for a reader group, reading situation, and book promise.
- For nonfiction, prefer specific claims, concrete transitions, precise verbs, and argument movement. Avoid filler summaries, formulaic contrasts, generic urgency, empty metaphors, and repetitive "not only...but also..." structures unless they are genuinely needed.
- Make affirmative, concrete prose the default repair pattern. Prefer a named subject doing a clear action with a consequence over symmetric negation pairs such as `不是...而是...`, `不只是...更是...`, `并非...而是...`, and `不仅...还...` when the contrast does not carry real conceptual work.
- Prefer reader-action openings for education and practice-oriented nonfiction. Convert abstract topic setup into the question a primary reader would actually use, then answer it through scene, case, process, or design choice.
- Use relationship sentences instead of binary slogans when both sides remain valuable. For example, explain how knowledge supplies language and practice supplies problem conditions, rather than implying one replaces the other.
- Keep chapter prose scoped to its assigned job. Move adjacent-chapter exposition into brief transitions or task-card updates so the visible chapter gains focus without becoming thin.
- Convert repetition into movement. When a paragraph repeats the book's central claim, ask what new work it does in this chapter: evidence, mechanism, boundary, model application, case consequence, institutional implication, or transition. Delete or relocate repetitions that do none of these.
- Keep recurring concept names stable and reader-facing. Define or preview heavily used terms early, then reuse the same names instead of drifting across synonyms that make the model feel improvised.
- Treat whole-book core models as prose obligations. The style engine should include how each selected model is introduced, how captions name it, how later chapters refer back to it, and how the conclusion recovers it without sounding like a summary table.
- Match case language to evidence level. A constructed scene should read as a typicalized scene, process material as documented operation, authorized material as participant detail, and outcome evidence as measured impact. Style must not blur these levels for narrative smoothness.
- When editing for rhythm, preserve density that matters to the primary reader: why the claim holds, what evidence or case shows, where the boundary sits, and what action follows. Do not optimize only for lower counts of flagged phrases.
- Flag high-risk AI-flavor scaffolds during style QC: generic intensifiers such as `真正`, `本质上`, `关键在于`, `更准确地说`, `其实`, `显然`, `毋庸置疑`; outline echoes such as `本章将讨论`, `这一部分`, `从三个方面`; and empty summarizers such as `综上所述` when they only restate the obvious. Replace them with reader-visible movement, concrete examples, or direct claims.
- Require style QC to scan for known forbidden or high-risk patterns before handoff. The report should either record counts/locations and accepted exceptions, or state that the scan found no active manuscript occurrences. Do not rely on impressionistic "去 AI 味" review when concrete regressions have already been observed.
- Run a sentence-integrity pass after every merge or large rewrite. Broken clauses, duplicated transitional fragments, dangling "also can..." continuations, and repeated headings are style failures even when the passage otherwise sounds polished.
- Keep owner voice and authorial responsibility visible. The style engine may guide prose, but it cannot authorize final editorial acceptance.

Required style refs for book-length work:

- `style-engine/style-contract.md` or equivalent durable style ref.
- `style-engine/anti-ai-flavor-rules.md` or equivalent repair rule ref.
- `style-engine/terminology.md` or equivalent term and naming map.
- `style-engine/style-qc.md` or equivalent chapter/whole-book style consistency report.
- `style-engine/reference-draft-absorption.md` or equivalent report when owner/reference drafts are used to improve the workflow.

This skill does not replace `reader-style-contract`; it materializes it into reusable production rules.
