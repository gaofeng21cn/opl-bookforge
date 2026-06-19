# OPL BookForge Status

Current state: OPL standard structural baseline plus one real short-book pilot run with owner-gated production-readiness blocker.

Fresh local evidence:

- `opl agents scaffold --validate /Users/gaofeng/workspace/opl-bookforge --json`: passed.
- `opl agents interfaces --repo-dir /Users/gaofeng/workspace/opl-bookforge --json`: ready.
- `npm --prefix /Users/gaofeng/workspace/opl-meta-agent run --silent takeover:test -- --agent-dir /Users/gaofeng/workspace/opl-bookforge --output-dir /Users/gaofeng/workspace/opl-bookforge/docs/evidence/oma-agent-lab --opl-bin /Users/gaofeng/workspace/one-person-lab/bin/opl`: passed.
- `npm --prefix /Users/gaofeng/workspace/opl-meta-agent run --silent improve:external-suite -- --suite /Users/gaofeng/workspace/opl-bookforge/docs/evidence/oma-agent-lab/agent-lab-takeover-suite.json --target-agent-dir /Users/gaofeng/workspace/opl-bookforge --output-dir /Users/gaofeng/workspace/opl-bookforge/docs/evidence/oma-agent-lab/external-suite-improvement --opl-bin /Users/gaofeng/workspace/one-person-lab/bin/opl --ai-reviewer-evaluation /Users/gaofeng/workspace/opl-bookforge/docs/evidence/oma-agent-lab/bookforge-ai-reviewer-evaluation.json --feedback-ref user-request:2026-06-18/oma-agent-lab-quality-loop-required`: passed.
- `python3 docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/tools/generate_pilot.py && python3 docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/tools/export_pilot.py && python3 docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/tools/verify_pilot.py`: passed with owner-gate blocker.
- `npm --prefix /Users/gaofeng/workspace/opl-meta-agent run --silent takeover:test -- --agent-dir /Users/gaofeng/workspace/opl-bookforge --output-dir /Users/gaofeng/workspace/opl-bookforge/docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/oma-takeover-after-pilot --opl-bin /Users/gaofeng/workspace/one-person-lab/bin/opl`: passed.
- `npm --prefix /Users/gaofeng/workspace/opl-meta-agent run --silent improve:external-suite -- --suite /Users/gaofeng/workspace/opl-bookforge/docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/oma-takeover-after-pilot/agent-lab-takeover-suite.json --target-agent-dir /Users/gaofeng/workspace/opl-bookforge --output-dir /Users/gaofeng/workspace/opl-bookforge/docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/oma-external-suite-after-pilot --opl-bin /Users/gaofeng/workspace/one-person-lab/bin/opl --ai-reviewer-evaluation /Users/gaofeng/workspace/opl-bookforge/docs/evidence/oma-agent-lab/bookforge-ai-reviewer-evaluation.json --feedback-ref user-request:2026-06-18/bookforge-production-readiness-pilot`: passed.

Scope of the claim:

- This proves the repo has a valid OPL standard scaffold, stage pack v2 fields, domain pack refs, foundry series contract, generated interface descriptors, OMA Agent Lab takeover evidence, independent AI reviewer evidence, and external-suite self-evolution evidence.
- This also proves a real pilot book project produced inputs, `storyline-architecture` artifacts, `book-materialization` artifacts, manuscript body, figure/table plans, style and AI-flavor checks, layout QC, DOCX/HTML/PDF exports, PDF page renders, independent gate receipts, and typed blockers.
- This does not prove final production readiness, publication approval, owner acceptance, direct `opl-bookforge` runtime CLI availability, or OPL-hosted artifact-handoff parity.
- The 2026-06-18 pilot generator is historical evidence only. Its prose-in-code generation pattern is superseded by the current Markdown-first, chapter-sharded materialization invariant.
- The 2026-06-19 200-page manuscript incident exposed additional rules now recorded in the domain pack: target readers, reader priority, and natural expression must be fixed as a reader-style contract before drafting; secondary readers must not become hidden co-primary writing targets without owner approval; reader-facing prose is a first-draft target driven by chapter-local reader-entry plans, and production scaffolding must not leak into manuscript body; routine late reader-facing rewrite is not the normal quality path; target extent must be converted to chapter budgets and an active production queue before body drafting; chapter target budgets are production gates; invalid compact drafts must be retired rather than expanded in place; all-chapter short coverage remains seed material rather than completed materialization; cumulative completed-contiguous review PDFs should refresh after chapter text-readiness or full readiness changes through the BookForge PDF export helper or an equivalent real publication/typesetting backend and must not skip unfinished earlier book units; review PDF / publication proof PDF / final export are distinct artifact levels requiring a publication design profile before publication-grade proof; book-bound `imagegen` figures need project-local bitmap paths recorded in a figure asset manifest; and final figure generation should use the BookForge native imagegen asset helper / Codex executor route by default rather than direct Base URL or API-key provider calls.

OMA / Agent Lab evidence:

- Takeover suite: `docs/evidence/oma-agent-lab/agent-lab-takeover-suite.json`.
- Takeover receipt: `docs/evidence/oma-agent-lab/takeover-receipt.json`, status `testing_takeover_recorded`.
- Takeover learning candidate: `docs/evidence/oma-agent-lab/takeover-online-learning-candidate.json`, status `candidate_recorded_requires_explicit_gate`.
- Takeover mechanism patch proposal: `docs/evidence/oma-agent-lab/takeover-mechanism-patch-proposal.json`, status `proposal_recorded_requires_explicit_gate`.
- AI reviewer evaluation: `docs/evidence/oma-agent-lab/bookforge-ai-reviewer-evaluation.json`, verdict `baseline_ready_with_agent_lab_takeover_and_owner_gate`.
- External-suite improvement receipt: `docs/evidence/oma-agent-lab/external-suite-improvement/meta-agent-improvement-receipt.json`, status `external_suite_passed_no_mechanism_patch_required`.
- Target capability candidate: `docs/evidence/oma-agent-lab/external-suite-improvement/target-capability-improvement-candidate.json`, status `candidate_recorded_requires_target_owner_gate`.
- Developer patch work order: `docs/evidence/oma-agent-lab/external-suite-improvement/developer-patch-work-order.json`, status `no_patch_required`.

Real book pilot production-readiness evidence:

- Evidence root: `docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/`.
- Boundary: this pilot remains historical short-book evidence; it is not the current implementation pattern for book-length manuscript source management.
- Source corpus and owner brief: `inputs/`.
- Stage 1 outputs: `artifacts/stage_outputs/storyline-architecture/`, including storyline map, chapter thesis chain, style contract, stage manifest, and owner handoff.
- Stage 2 outputs: `artifacts/stage_outputs/book-materialization/`, including chapter draft bundle, illustration plan, table plan, style consistency report, AI-flavor revision report, layout QC report, stage manifest, and owner handoff.
- Manuscript and assets: `artifacts/manuscript/book.md`, `artifacts/figures/figure-01-storyline-arc.png`, and `artifacts/figures/figure-02-two-stage-route.png`.
- Exports: `exports/bookforge-pilot-book.html`, `exports/bookforge-pilot-book.docx`, `exports/bookforge-pilot-book.pdf`, and rendered page PNGs under `exports/rendered-pages/`.
- Local verification receipt: `quality/local-verification-receipt.json`, status `passed_with_owner_gate_blocker`; all required files present and nonempty, DOCX schema validation passed, DOCX has two media files, PDF rendered to five nonblank pages, AI-flavor scan is clean, style terms are present, and production-ready claim remains fail-closed.
- Visual inspection note: `quality/visual-render-inspection.md`.
- Owner blockers: `receipts/storyline-owner-blocker.json` and `receipts/book-owner-blocker.json`, both status `blocked_owner_acceptance_missing`.
- After-pilot OMA takeover receipt: `oma-takeover-after-pilot/takeover-receipt.json`, status `testing_takeover_recorded`.
- After-pilot OMA external-suite improvement receipt: `oma-external-suite-after-pilot/meta-agent-improvement-receipt.json`, status `external_suite_passed_no_mechanism_patch_required`.
- After-pilot developer patch work order: `oma-external-suite-after-pilot/developer-patch-work-order.json`, status `no_patch_required`.

Next evidence required for stronger claims:

- Human owner receipt accepting the pilot topic, reader promise, manuscript quality, figure/table plan, DOCX/PDF layout, and publication intent.
- Direct `opl-bookforge` runtime CLI or hosted OPL artifact-handoff parity evidence.
