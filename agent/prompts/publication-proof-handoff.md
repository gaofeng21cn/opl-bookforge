# Publication Proof Handoff Prompt

Goal: package honest review/proof/export handoff refs after source/style integrity review.

Primary open judgment: which artifact role is currently supportable: `review_pdf`, `publication_proof`, `final_export`, or blocked/human-gated.

Use the professional method layer when needed:

- `bookforge-publication-memory-curator` for review PDF, publication proof, final export handoff, design tokens, figure/table manifest readiness, memory refs, and rendered-page QA.

Produce these refs:

- publication design profile when the target is `publication_proof` or `final_export`.
- figure asset manifest and table plan readiness refs.
- PDF export receipt with explicit `artifact_role` of `review_pdf`, `publication_proof`, or `final_export`.
- Markdown image-ref and resource-path resolution refs.
- rendered-page QA refs and machine-baseline inspection refs when proof evidence is claimed.
- pre-ship proof review refs for publication proof.
- owner handoff packet naming remaining decisions, blockers, evidence refs, and artifact-role boundary.
- typed blocker, human gate, or route-back refs when backend, design profile, figure assets, rendered-page inspection, owner/export acceptance, or upstream integrity evidence is missing.

Keep `review_pdf`, `publication_proof`, and `final_export` separate. A successful PDF compile or readable review PDF does not imply publication proof, final export readiness, owner acceptance, publication approval, or book quality acceptance.
