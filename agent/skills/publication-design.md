# Publication Design Skill

Use this skill when a manuscript needs to move beyond readable review output toward a publication-grade book proof.

Working policy:

- Keep a strict distinction between `review_pdf`, `publication_proof_pdf`, and `final_export`.
- A review PDF is a cumulative owner reading checkpoint. It can use a simpler layout profile, but it must render text, tables, captions, and any ready figures correctly, and it must label itself as review-only.
- A publication proof PDF is the first artifact that should be judged for book-like visual quality. It requires a publication design profile, not just a default PDF backend.
- A final export is owner-gated and cannot be implied by review PDF generation or a successful PDF compile.
- Define a publication design profile before final proof: page size, page geometry, body font, heading scale, line length, table style, caption style, figure placement, case-box/callout style, page headers/footers, numbering, and rendered-page inspection plan.
- Use real publication/typesetting systems such as Pandoc with XeLaTeX/LuaLaTeX templates, Quarto book rendering, or Typst. Do not hand-roll publication layout through ad-hoc raster text drawing.
- Treat image placement as part of publication design. If a figure is referenced in prose but the project-local bitmap asset is missing, keep the PDF as a text-review checkpoint and return an image-asset blocker.
- Use rendered-page checks before owner handoff. Inspect sampled pages for page rhythm, heading hierarchy, table readability, caption proximity, figure sharpness, missing images, overfull lines, and visually monotonous spreads.
- A high-quality nonfiction book should use visual rhythm intentionally: meaningful figures, tables, case boxes, pull quotes, and section breaks. Do not add decorative noise to compensate for weak structure.
- Do not mark the publication proof ready while required figures are `planned`, `preview_only`, or `blocked_missing_project_bitmap`.

External practice notes:

- Pandoc can compile Markdown to PDF with a configured PDF engine, fonts, metadata, section numbering, table of contents, variables, and templates.
- Quarto book projects support multi-chapter rendering, cross-references, figure/table numbering, callouts, and multiple output formats.
- Typst makes page setup, margins, headers, footers, numbering, and reusable layout rules first-class document concerns.
