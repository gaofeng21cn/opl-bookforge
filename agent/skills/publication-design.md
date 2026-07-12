# Publication Design Skill

Use this skill when a manuscript needs to move beyond readable review output toward a publication-grade book proof.

Working policy:

- Keep a strict distinction between `review_pdf`, `publication_proof_pdf`, and `final_export`.
- A review PDF is a cumulative owner reading checkpoint. It can use a simpler layout profile, but it must render text, tables, captions, and any ready figures correctly, and it must label itself as review-only.
- A publication proof PDF is the first artifact that should be judged for book-like visual quality. It requires a publication design profile, not just a default PDF backend.
- A final export is owner-gated and cannot be implied by review PDF generation or a successful PDF compile.
- Publication design tokens, Kami-inspired patterns, component inventory, font readback, rendered-page QA, and pre-ship proof review are hard gates only for `publication_proof` and `final_export` claims. They are advisory inputs for storyline shaping, chapter drafting, style calibration, claim integrity, chapter QC, and ordinary review-PDF refreshes.
- Define a publication design profile before final proof: page size, page geometry, body font, heading scale, line length, table style, caption style, figure placement, case-box/callout style, page headers/footers, numbering, and rendered-page inspection plan.
- Treat the publication design profile as a tokenized proof contract, not a visual mood board. Record concrete tokens for page size, margins, body and display fonts, font weights, line heights, text measure, heading scale, caption scale, table rules, callout rules, figure spacing, header/footer behavior, page numbering, color use, and density thresholds. External design systems such as Kami are pattern sources for token discipline and proof checks; do not copy their palette, font choices, HTML runtime, WeasyPrint route, or brand language into Book Forge.
- Maintain a template/component inventory before publication proof. The inventory should name the reusable book components that the proof will render: cover/title page, front matter, TOC, part opener, chapter opener, dense body page, figure page, table page, case box/callout, quote/pull-quote, caption, footnote/endnote style if used, bibliography/source note if used, and closing matter. Each component needs an owner surface, input refs, expected output role, and rendered-page sample plan.
- Record font actual-load/readback evidence for publication proof. The proof receipt should name the intended font stack, the backend command/profile that loads it, the actual fonts reported by the backend or PDF inspection path when available, and any fallback font used. Font fallback can change page count, density, glyph coverage, and orphan behavior; it blocks `publication_proof` and `final_export` claims until rerendered and reinspected, but it does not block ordinary chapter drafting or review-PDF text review.
- Define the reader-facing front matter and TOC policy before proof output. A book-like proof needs title, subtitle, author, proof/version label, clean chapter punctuation, running heads/feet, and a TOC that works as an argument map. Review metadata, production notes, blockers, case-box labels, table labels, figure labels, empty headings, and asset/status commentary must be excluded from the book TOC.
- Use real publication/typesetting systems such as Pandoc with XeLaTeX/LuaLaTeX templates, Quarto book rendering, or Typst. Do not hand-roll publication layout through ad-hoc raster text drawing.
- For Chinese nonfiction e-book proof output, prefer the bundled Book Forge `bookforge-zh-publication-proof` profile unless the owner supplies a stronger design profile. It provides A5 page geometry, Chinese body/head fonts, running heads, page numbers, chapter opening hierarchy, captions, table treatment, callout/quote treatment, resource-path-backed images, and rendered-page inspection expectations.
- Treat unstyled Pandoc defaults as review-output quality, not publication-proof quality.
- Treat a readable PDF with polluted front matter or TOC as review-output quality even when the body text is acceptable. Clean front matter and TOC are publication-design gates, not cosmetic afterthoughts.
- Treat image placement as part of publication design. If a figure is referenced in prose but the project-local bitmap asset is missing, keep the PDF as a text-review checkpoint, record image-asset quality debt, and advance without publication-proof or final-export claims.
- Use the Book Forge PDF helper's Markdown image-ref scan, figure-asset-manifest scan, and helper-generated rendered-page baseline inspection when available. A machine baseline can satisfy proof plumbing evidence for nonblank pages and asset resolution, but it does not replace human publication-design review or owner final-export acceptance.
- Use rendered-page checks before owner handoff. Inspect sampled pages for page rhythm, heading hierarchy, table readability, caption proximity, figure sharpness, missing images, overfull lines, and visually monotonous spreads.
- Use a rendered-page QA checklist for publication proof and final export. At minimum sample title/front matter, TOC, chapter opener, dense body page, figure/table page, callout/case-box page, and closing page. Check nonblank rendering, glyph coverage, font fallback, page rhythm, density, orphan/widow risk, overfull or clipped lines, heading hierarchy, caption proximity, figure/table placement, running heads/feet, page numbers, cross-references, and monotony across adjacent spreads.
- Run a pre-ship proof review before any `publication_proof` handoff. The review should compare the rendered pages against the publication design tokens, component inventory, front matter/TOC policy, asset coverage, and artifact role. It may conclude `proof_ready_for_owner_review`, `proof_blocked`, or `downgrade_to_review_pdf`; it cannot grant final export acceptance.
- A high-quality nonfiction book should use visual rhythm intentionally: meaningful figures, tables, case boxes, pull quotes, and section breaks. Do not add decorative noise to compensate for weak structure.
- Choose a whole-book figure stance before final proof when figure style is questioned or when multiple figure styles exist. Record whether the book uses `light_methodology_sketchnote`, `formal_framework_diagram`, or another owner-approved stance, and align figure prompts, captions, image placement, and rendered-page inspection with that choice.
- A light methodology sketchnote style is acceptable for education-method books when it improves reader entry, model memory, and classroom/project usability. Keep it disciplined: consistent handwritten Chinese typography, restrained color, clear model structure, readable captions, and no decorative clutter.
- A formal framework diagram style is preferable when the book is positioned as a policy report, institutional white paper, or strictly academic monograph. If selected, all figures should move toward formal layout and terminology rather than mixing casual sketchnotes with serious tables.
- Do not mark the publication proof ready while required figures are `planned`, `preview_only`, or `blocked_missing_project_bitmap`.

Advisory boundary:

- External design systems such as Kami are pattern sources for proof discipline, not Book Forge runtime, template, palette, font, or proof-truth owners.
- Missing publication-proof dependency, token, component, font-readback, rendered-page QA, or owner proof review must return a blocker for proof/export claims. It must not stop narrower honest actions that do not require those proof guarantees.
- Review PDFs may carry review-only evidence and known proof blockers. Do not describe them as publication proof, final export, book delivery ready, or owner accepted.

Artifact-role boundary:

- `review_pdf` is progress-first reading output. It should be cumulative, contiguous, clearly labeled review-only, and honest about missing assets or earlier incomplete units. It may proceed without full publication tokens, actual font readback, full component inventory, human proof review, or final-export owner receipt when the goal is ordinary chapter review.
- `publication_proof` is design evidence. It requires publication design tokens, template/component inventory, real backend receipt, resource-path-backed assets, Markdown image-ref and figure-manifest checks, font actual-load/readback when available, rendered-page refs, rendered-page QA checklist, front matter/TOC cleanliness, page rhythm/density/orphan checks, and pre-ship proof review.
- `final_export` is owner-gated export. It requires all publication-proof evidence plus owner/export acceptance receipts and any target-specific packaging or distribution checks. A clean review PDF, successful compile, or machine baseline page render is never enough by itself.

External practice notes:

- Pandoc can compile Markdown to PDF with a configured PDF engine, fonts, metadata, section numbering, table of contents, variables, and templates.
- Quarto book projects support multi-chapter rendering, cross-references, figure/table numbering, callouts, and multiple output formats.
- Typst makes page setup, margins, headers, footers, numbering, and reusable layout rules first-class document concerns.
