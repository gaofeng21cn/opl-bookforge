# Source Claim Integrity Skill

Use this skill when BookForge drafts, reviews, repairs, or packages nonfiction
material whose claims depend on source refs, owner material, cases, interviews,
process evidence, or impact evidence.

Working policy:

- Treat claim integrity as a BookForge domain gate. OPL may project source-map,
  claim-ledger, claim-locator, blocker, and receipt refs, but the truth body
  stays in BookForge-owned book workspace refs.
- Do not create a second truth source, generic vector store, generic retrieval
  runtime, private source database, or hidden attempt ledger for integrity work.
- Adapt external lessons as patterns only:
  - Academic Research Skills: claim/source support, material passport,
    source locator, provenance, anti-leakage, and fail-closed integrity gates.
  - InkOS: schema-validated truth delta for claim changes, source changes,
    boundary changes, and audit repairs.
  - LibriScribe: local retrieval and cross-reference discipline for finding
    source slices and neighboring claims before drafting or repair.
- Keep local retrieval BookForge-scoped: retrieve from declared book workspace
  refs, owner-supplied material, source maps, chapter packages, and approved
  local reference packs. Do not import a general retrieval service as the gate.
- Record source provenance before using a source: who supplied it, where it
  lives, what scope it authorizes, what it may support, and what must not leak
  into reader-facing prose or generated public interface descriptors.
- Run claim checks at chapter-package boundaries and again after assembly,
  reference absorption, owner/source updates, or any rewrite that changes the
  strength, scope, actor, time, result, or evidence class of a claim.

Evidence classes:

- `constructed_scene`: invented or composite scene used to orient the reader.
  It may support typical tension or explanation, not factual event claims.
- `typical_scenario`: generalized scenario grounded in domain experience or
  repeated source patterns. It may support common-pattern language, not a
  specific documented event or measured result.
- `documented_process_material`: source-backed process artifact, record,
  workflow note, transcript excerpt, policy, log, or operational material. It
  may support process, sequence, decision, and mechanism claims within scope.
- `authorized_material/interview`: owner-authorized material, interview, or
  participant detail. It may support attributed detail within its permission,
  confidentiality, and stance boundary.
- `owner-supplied_source`: owner-provided source package, draft, note, dataset,
  image, table, or private context. It must carry owner scope, allowed usage,
  privacy boundary, and whether it can appear in manuscript, appendix, or only
  internal refs.
- `outcome/impact_evidence`: measured or documented result, impact, effect,
  adoption, feedback, validation, or comparison. It is required before outcome,
  impact, learning-effect, success, scale, or performance claims.
- `unsupported_gap`: a claim candidate or desired narrative move whose source
  support is missing, stale, too weak, unauthorized, or outside the declared
  boundary.

Required chapter/package refs:

- Claim ledger: every material claim has a stable `claim_id`, manuscript
  locator, claim text or digest, claim type, evidence class, support status,
  source locator, source provenance, freshness stamp, and reviewer/audit note.
- Source locator: every source has a local path or owner-supplied identifier,
  section/page/time locator when available, source owner, access boundary,
  allowed use, privacy rule, and cross-references to claims it supports.
- Evidence boundary: each chapter states what evidence level is available for
  major cases, examples, tables, figures, and outcomes; weaker classes must not
  be written in stronger language for narrative smoothness.
- Unsupported gaps: each gap records `gap_id`, affected claim locator,
  missing evidence class, typed blocker or `next-source-action`, owner decision
  need when any, and whether the chapter can proceed without that claim.
- Truth delta: any claim repair records previous claim locator, revised claim
  locator, evidence delta, source delta, boundary delta, and audit reason in a
  structured form that can be schema-validated when the workspace provides a
  schema.
- Anti-leakage note: private owner material, interview detail, draft comments,
  or unpublished source slices stay in internal refs unless the source boundary
  explicitly allows reader-facing use.

Drafting and repair rules:

- Before drafting a major section, retrieve the relevant local source slices,
  neighboring chapter claims, evidence ladder entries, reader-style stance, and
  unresolved gaps.
- Match language to evidence. A constructed scene reads as a constructed or
  typical scene; documented process material reads as documented process;
  owner practice involvement reads as practice-involved design/reflection;
  outcome language requires outcome/impact evidence.
- For practice-involved cases, active author-team voice may explain design
  judgment, operational choice, and reflective limits. It must not claim
  unprovided outcomes, user validation, interviews, authorization, learning
  effects, impact metrics, or full process proof.
- Keep claim locators out of reader-facing prose unless the house style or
  owner explicitly wants visible citations. Locators belong in chapter packages,
  source maps, comments, review packets, footnotes, appendices, or handoff refs
  according to the book style and source boundary.
- When local retrieval finds contradictory, stale, or duplicate support, repair
  the claim ledger and source boundary before strengthening manuscript prose.
- Tables, figures, captions, callouts, and case boxes are claims too. They need
  the same source locator, evidence class, rights boundary, and unsupported-gap
  handling as paragraphs.

Fail-closed conditions:

- An outcome, impact, success, validation, learning-effect, adoption, scale, or
  performance claim appears without `outcome/impact_evidence`.
- A source is fabricated, unlocatable, outside the declared source map, or cited
  with a locator/provenance that cannot be inspected.
- A chapter or package uses source-dependent claims while the source map or
  source locator is missing.
- A constructed scene, typical scenario, or documented process material is
  upgraded into authorized participant detail or measured outcome language.
- A practice-involved stance claims results, user feedback, authorization,
  interviews, impact, or complete operational proof beyond the available
  evidence boundary.
- Private owner material, interview detail, draft notes, or unpublished source
  slices leak into public generated interfaces or reader-facing prose beyond
  the allowed boundary.
- A reference draft supplies prose, examples, source-specific facts, or claims
  that are not independently supported by the BookForge source map.
- Claim audit evidence is stale after source updates, chapter rewrites,
  reference absorption, assembly, or owner-material changes.
- Unsupported gaps are hidden by softer wording, generic hedging, or final
  readiness labels instead of being recorded as typed blockers or
  next-source-actions.

Progress policy:

- Integrity gates should fail closed on the affected claim, section, table,
  figure, chapter package, or handoff claim, not freeze unrelated drafting by
  default.
- If a chapter can proceed without an unsupported claim, remove or bracket that
  claim, record `unsupported_gap`, assign a `next-source-action`, and continue
  with source-supported material.
- If the chapter's central movement depends on the unsupported claim, return a
  typed blocker such as `missing_outcome_evidence`, `source_locator_missing`,
  `owner_authorization_needed`, `stale_claim_audit`, or
  `practice_stance_overclaim`.
- Do not turn source integrity into infinite preflight. Each audit pass must
  end with supported claims, explicit claim repairs, typed blockers, or
  concrete next-source-actions.

This skill strengthens BookForge source and claim discipline. It does not
authorize publication readiness, final export, owner acceptance, or generic OPL
runtime behavior.
