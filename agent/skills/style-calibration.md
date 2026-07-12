# Style Calibration Skill

Use this skill when Book Forge needs to calibrate a reusable writing style
profile from owner-inspectable evidence before drafting, revising, or checking
book prose.

Boundary:

- Style calibration is a Book Forge domain ref, not a model router, detector
  evasion layer, or generic humanizer.
- The calibrated style must obey the reader-style contract, source stance map,
  evidence map, chapter job, and house style.
- Reference material is used to extract transferable craft rules. Do not copy
  reference prose, examples, claims, or voice targets without source authority
  and owner permission.
- Style calibration can support first-draft naturalness and style QC, but it
  cannot authorize final editorial acceptance, publication readiness, export
  readiness, or owner approval.

External lesson mapping:

- InkOS style analyze/import: analyze reference style before importing rules;
  keep adoption and rejection explicit; scan fatigue words, repeated patterns,
  and anti-AI-flavor issues with evidence instead of impressionistic polish.
- Novel-OS writing standards: separate global writing standards,
  project-specific standards, manuscript-local continuity, and accepted
  exceptions so a house style does not override the current book contract.
- Academic Research Skills style calibration and writing quality check:
  calibrate against a target corpus, then run quality checks for clarity, claim
  restraint, source fit, style currentness, and overstatement risk.

Inputs:

- owner samples and owner edits;
- reference drafts, edited chapters, or prior versions;
- comparable works or target-market style references;
- house style and publisher/editor rules;
- prior chapters, chapter task cards, and book memory;
- critique, meta-review, QC, and owner findings.

Outputs:

- style profile with audience stance, source stance, house-style scope, and
  owner-review status;
- sentence rhythm rules;
- paragraph movement rules;
- terminology and naming map;
- forbidden patterns and non-transferable reference patterns;
- fatigue list with scan terms, contexts, counts or locations, and repair
  guidance;
- reference-derived adoption and rejection list;
- scan evidence for active manuscript refs;
- accepted exceptions with reason, scope, owner/editor basis, and expiry or
  review trigger.

Workflow:

1. Confirm the reader-style contract and source stance map exist. If they
   conflict or are missing but a readable draft exists, preserve a provisional
   style assumption, record `completed_with_quality_debt`, and continue. Stop
   with a typed blocker only when no consumable artifact can be produced or the
   conflict requires protected-source, owner-authority, or human resolution.
2. Classify each input as owner voice, reference draft, comparable work, house
   style, prior chapter, critique, or QC finding.
3. Extract style signals: sentence length, cadence, paragraph entry and exit,
   transition shape, example density, theory-to-practice ratio, term reuse, case
   voice, claim restraint, and visual/table prose integration.
4. Build the style profile as an owner-inspectable ref. Include what to adopt,
   what to reject, and why each rule fits the primary readers.
5. Build the fatigue list from repeated empty turns, generic intensifiers,
   formulaic negation, outline scaffolds, status language, and project-specific
   phrases that make prose sound generated or workflow-facing.
6. Run a scan over the active chapter or manuscript refs. Record locations,
   counts, repair actions, and accepted exceptions.
7. Back-propagate reusable findings into the style engine, terminology map,
   chapter task cards, reader-entry plans, QC reports, or semantic memory. Do
   not only patch local prose when the defect is systemic.

Progress priority:

- Use the style gate to make first drafts more natural for the declared primary
  readers.
- Do not block every chapter in endless polish. Normal local style issues
  should be recorded and repaired in the chapter pass.
- Update the style pattern before continuing only when a serious systemic defect
  appears, such as repeated memo-like openings, generic AI-flavor scaffolds,
  copied reference rhythm, weakened primary-reader density, or recurring
  source-stance drift.
- Preserve chapter budget, evidence density, and argument movement when
  improving rhythm. Smoother prose is not an excuse to remove the reasoning the
  primary reader needs.

Fail-closed conditions:

- The style profile conflicts with the reader-style contract or silently
  changes the primary reader.
- Calibration copies reference prose, examples, claims, or protected voice
  instead of extracting transferable rules.
- A reference or house style weakens primary-reader density, lowers required
  argument depth, or turns secondary-reader accessibility into the main voice.
- Style repair hides unsupported claims, source gaps, owner-decision gaps, or
  evidence limits.
- The style profile claims final editorial acceptance, publication readiness,
  export readiness, or owner approval.
- The active manuscript keeps known forbidden or fatigue patterns while the
  report claims style pass without scan evidence or accepted exceptions.
