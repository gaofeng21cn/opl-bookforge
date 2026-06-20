# Publication Design Skill

Use this skill when a manuscript needs to move beyond readable review output toward a publication-grade book proof.

Working policy:

- Keep a strict distinction between `review_pdf`, `publication_proof_pdf`, and `final_export`.
- A review PDF is a cumulative owner reading checkpoint. It can use a simpler layout profile, but it must render text, tables, captions, and any ready figures correctly, and it must label itself as review-only.
- A publication proof PDF is the first artifact that should be judged for book-like visual quality. It requires a publication design profile, not just a default PDF backend.
- A final export is owner-gated and cannot be implied by review PDF generation or a successful PDF compile.
- Define a publication design profile before final proof: page size, page geometry, body font, heading scale, line length, table style, caption style, figure placement, case-box/callout style, page headers/footers, numbering, and rendered-page inspection plan.
- Define the reader-facing front matter and TOC policy before proof output. A book-like proof needs title, subtitle, author, proof/version label, clean chapter punctuation, running heads/feet, and a TOC that works as an argument map. Review metadata, production notes, blockers, case-box labels, table labels, figure labels, empty headings, and asset/status commentary must be excluded from the book TOC.
- Use real publication/typesetting systems such as Pandoc with XeLaTeX/LuaLaTeX templates, Quarto book rendering, or Typst. Do not hand-roll publication layout through ad-hoc raster text drawing.
- For Chinese nonfiction e-book proof output, prefer the bundled BookForge `bookforge-zh-publication-proof` profile unless the owner supplies a stronger design profile. It provides A5 page geometry, Chinese body/head fonts, running heads, page numbers, chapter opening hierarchy, captions, table treatment, callout/quote treatment, resource-path-backed images, and rendered-page inspection expectations.
- Treat unstyled Pandoc defaults as review-output quality, not publication-proof quality.
- Treat a readable PDF with polluted front matter or TOC as review-output quality even when the body text is acceptable. Clean front matter and TOC are publication-design gates, not cosmetic afterthoughts.
- Treat image placement as part of publication design. If a figure is referenced in prose but the project-local bitmap asset is missing, keep the PDF as a text-review checkpoint and return an image-asset blocker.
- Use the BookForge PDF helper's Markdown image-ref scan, figure-asset-manifest scan, and helper-generated rendered-page baseline inspection when available. A machine baseline can satisfy proof plumbing evidence for nonblank pages and asset resolution, but it does not replace human publication-design review or owner final-export acceptance.
- Use rendered-page checks before owner handoff. Inspect sampled pages for page rhythm, heading hierarchy, table readability, caption proximity, figure sharpness, missing images, overfull lines, and visually monotonous spreads.
- A high-quality nonfiction book should use visual rhythm intentionally: meaningful figures, tables, case boxes, pull quotes, and section breaks. Do not add decorative noise to compensate for weak structure.
- Do not mark the publication proof ready while required figures are `planned`, `preview_only`, or `blocked_missing_project_bitmap`.

External practice notes:

- Pandoc can compile Markdown to PDF with a configured PDF engine, fonts, metadata, section numbering, table of contents, variables, and templates.
- Quarto book projects support multi-chapter rendering, cross-references, figure/table numbering, callouts, and multiple output formats.
- Typst makes page setup, margins, headers, footers, numbering, and reusable layout rules first-class document concerns.
