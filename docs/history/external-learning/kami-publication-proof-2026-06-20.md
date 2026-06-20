# External Learning: Kami Publication Proof

Owner: `opl-bookforge`
Purpose: `external_learning_landing`
State: `history_provenance_landed_domain_contract_and_runtime_helper`
Machine boundary: Human-readable learning record. Machine truth remains in contracts, agent pack files, OPL validator output, runtime receipts, owner receipts, and typed blockers.

## Source Evidence

- External source: `tw93/kami`.
- Commit inspected: `818dfb431c19156bbe2245577cc66478b72baed9` (`docs: tighten agent maintenance guidance`).
- Local read path used for this landing slice: `/tmp/kami-818dfb`, detached at the commit above.
- Inspected files:
  - `plugins/kami/skills/kami/SKILL.md`
  - `plugins/kami/skills/kami/references/design.md`
  - `plugins/kami/skills/kami/references/production.md`
  - `plugins/kami/skills/kami/references/tokens.json`
  - `plugins/kami/skills/kami/references/checks_thresholds.json`
  - `plugins/kami/skills/kami/references/anti-patterns.md`
  - `plugins/kami/skills/kami/scripts/checks.py`
  - `plugins/kami/skills/kami/scripts/ensure-fonts.sh`

## Classification

| Kami pattern | Classification | Book Forge adaptation | Local owner surface |
| --- | --- | --- | --- |
| Tokenized print design system | adapt | Use publication design tokens for page geometry, font stack, hierarchy, line height, captions, callouts, tables, headers/footers, color restraint, density thresholds, and rendered-page expectations. Do not copy Kami's palette or visual identity. | `agent/skills/publication-design.md`, `agent/prompts/book-materialization.md` |
| Template and component inventory | adopt | Require a proof inventory for title/front matter, TOC, chapter opener, dense body, figures, tables, callouts/case boxes, captions, and closing matter before proof claims. | `agent/skills/publication-design.md` |
| Font availability and actual-load discipline | adapt | Record intended font stack, backend/profile, actual loaded fonts or fallback evidence when available, and rerender/reinspect after fallback. Keep this as proof/export evidence, not a drafting blocker. | `agent/skills/publication-design.md`, `agent/prompts/book-materialization.md`, `runtime/native_helpers/bookforge_pdf_export.py` |
| Rendered-page checks for orphans, density, rhythm, and sparse pages | adapt | Add rendered-page QA checklist for nonblank pages, glyph coverage, overflow, density, orphan/widow risk, captions, figure/table placement, headers/footers, page numbers, and adjacent-page rhythm. The helper can now write a machine-baseline rendered-page inspection with embedded-font, density, trailing-whitespace, page-size, sample-role, and checklist readbacks. | `agent/quality_gates/book-materialization-quality-gate.md`, `runtime/native_helpers/bookforge_pdf_export.py`, `scripts/verify.sh` |
| Production runbook around HTML to PDF and WeasyPrint | reject | Book Forge keeps its current real-typesetting backend boundary through Book Forge/OPL-owned export helpers and accepts Pandoc/XeLaTeX, Quarto, Typst, or Paged.js style backends. Do not import Kami's WeasyPrint runtime route. | N/A |
| Warm parchment / ink-blue / serif visual language | reject | Visual branding is Kami-specific. Book Forge can learn restraint and token discipline, but each book needs its own owner-approved publication design profile. | N/A |
| Update check, package refresh, plugin distribution workflow | watch_only | Useful for Kami as a shipped skill package, but not relevant to this OBF domain-docs lane. | N/A |
| AI document anti-pattern catalog | adapt | Reinforce Book Forge's existing AI-flavor/internal-language scans and caption/content checks where they affect manuscript and proof quality. | `agent/skills/book-production.md`, existing style gates |

## Local Design

The landed Book Forge rule is: progress-first writing continues, proof claims fail closed.

`review_pdf` remains an owner reading checkpoint. It should be cumulative, contiguous, clearly labeled review-only, and honest about missing assets or incomplete earlier units. It does not need full publication tokens, component inventory, font readback, pre-ship proof review, or owner export receipt.

`publication_proof` is a design evidence artifact. It requires publication design tokens, a template/component inventory, real backend receipt, resource-path-backed assets, Markdown image-ref and figure-manifest checks, font actual-load/readback where available, rendered-page refs, rendered-page QA, front matter/TOC cleanliness checks, page rhythm/density/orphan checks, material/asset coverage, and pre-ship proof review.

The current helper landing implements the machine-baseline part of that rule for the bundled Book Forge profile. It does not replace book-specific human visual review, pre-ship proof review, or owner/export acceptance.

`final_export` remains owner-gated. It requires publication proof evidence plus owner/export acceptance receipts and any target-specific packaging checks.

## Adopt / Adapt / Watch / Reject Summary

- Adopt: component inventory before proof, proof sampling across representative page types, pre-ship proof review as a named handoff gate.
- Adapt: design tokens, font actual-load/readback, density/orphan/rhythm checks, and material coverage as Book Forge-owned proof refs rather than Kami-specific templates.
- Watch: packaging/update-check discipline for future plugin shipping, if OPL owner surfaces need it.
- Reject: Kami visual identity, WeasyPrint runtime dependency, private font downloader route, and any second truth source for Book Forge export readiness.

## Learning Landing Audit

| Item | Pattern | Local owner surface | Target landing | Status | Completion | Fresh evidence | Missing refs | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Publication design tokens | Tokenized print design | Book Forge publication design skill and materialization prompt | Token refs required for publication proof | done | 100% | `agent/skills/publication-design.md`, `agent/prompts/book-materialization.md` | Runtime proof artifacts not part of this docs lane | Exercise on a real book proof |
| Component inventory | Template/component map | Book Forge publication design skill | Inventory ref required before proof claims | done | 100% | `agent/skills/publication-design.md` | Runtime proof artifact not part of this docs lane | Use in next publication proof |
| Font actual-load/readback | Font availability and fallback discipline | Book Forge proof refs and PDF helper | Font readback evidence gates proof/export only | done | 100% | `agent/skills/publication-design.md`, `agent/prompts/book-materialization.md`, `runtime/native_helpers/bookforge_pdf_export.py`, `scripts/verify.sh` | Book-specific final visual judgment still needs human review | Use receipt in the next real book proof |
| Rendered-page QA | Density, orphan, rhythm, nonblank page checks | Book Forge quality gate and PDF helper | Rendered-page QA checklist, machine baseline, and fail-closed conditions | done | 100% | `agent/quality_gates/book-materialization-quality-gate.md`, `runtime/native_helpers/bookforge_pdf_export.py`, `scripts/verify.sh` | Human proof review remains required for final visual judgment | Exercise on a real book proof |
| Progress-first boundary | Missing proof evidence blocks only proof/export claims | Book Forge skills, prompt, quality gate, docs, and PDF helper | Ordinary drafting/review PDF remains available | done | 100% | `agent/skills/book-production.md`, `agent/prompts/book-materialization.md`, `docs/invariants.md`, `runtime/native_helpers/bookforge_pdf_export.py`, `scripts/verify.sh` | none for landed repo behavior | Preserve in future runtime helpers |
| Executable machine proof QA | Kami-style rendered proof checks | Book Forge PDF helper and bundled profile | `publication_proof` can fail-close unchecked machine QA and pass complete machine-baseline evidence | done | 100% | `runtime/native_helpers/bookforge_pdf_export.py`, `runtime/native_helpers/pdf_profiles/bookforge-zh-publication-proof.json`, `scripts/verify.sh` | Owner/export acceptance still external to helper | Run on real manuscript proof |
| Reject foreign runtime/visual identity | Kami is pattern source only | Book Forge docs | No WeasyPrint or Kami visual import | done | 100% | `docs/decisions.md`, this learning record | none | Keep OBF/OPL authority boundary |
