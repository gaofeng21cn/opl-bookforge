# Style Engine Skill

Use this skill when BookForge needs a durable writing style asset rather than one-off prompt wording.

Working policy:

- The style engine is a domain artifact contract, not a private model router or runtime control plane.
- Build the style engine from the reader-style contract, owner examples, comparable works, source constraints, and chapter QC findings.
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
- Store the style engine as a ref that chapter prompts, chapter QC, wording repair, and publication proof can cite. Do not bury it only in a long prompt.
- Let style evolve through reviewed deltas. When a chapter repair reveals a recurring style defect, update the style engine with the defect, replacement pattern, and evidence ref.
- Keep style quality tied to the declared readers. A passage is not "natural" in the abstract; it is natural for a reader group, reading situation, and book promise.
- For nonfiction, prefer specific claims, concrete transitions, precise verbs, and argument movement. Avoid filler summaries, formulaic contrasts, generic urgency, empty metaphors, and repetitive "not only...but also..." structures unless they are genuinely needed.
- Keep owner voice and authorial responsibility visible. The style engine may guide prose, but it cannot authorize final editorial acceptance.

Required style refs for book-length work:

- `style-engine/style-contract.md` or equivalent durable style ref.
- `style-engine/anti-ai-flavor-rules.md` or equivalent repair rule ref.
- `style-engine/terminology.md` or equivalent term and naming map.
- `style-engine/style-qc.md` or equivalent chapter/whole-book style consistency report.

This skill does not replace `reader-style-contract`; it materializes it into reusable production rules.
