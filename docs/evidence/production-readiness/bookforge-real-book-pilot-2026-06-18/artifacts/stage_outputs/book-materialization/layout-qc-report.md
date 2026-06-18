# Layout And Typography QC Report

Target exports:

- Markdown source: `artifacts/manuscript/book.md`
- HTML export: `exports/bookforge-pilot-book.html`
- DOCX export: `exports/bookforge-pilot-book.docx`
- PDF export: `exports/bookforge-pilot-book.pdf`

Checks planned:

- Heading hierarchy: title, preface, five chapters, conclusion.
- Page rhythm: chapters separated by headings, no placeholder pages.
- Tables: header rows, readable columns, short cell content.
- Figures: PNG files exist, are nonblank, and carry captions in the manuscript.
- Cross-references: figure and table mentions stay near their artifacts.
- Export chain: DOCX and PDF are created by local tools and PDF pages render to PNG for inspection.

Initial status before export: pending. Final render evidence is written by `tools/verify_pilot.py`.
