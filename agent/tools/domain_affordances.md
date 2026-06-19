# OPL BookForge Domain Tool Affordances

This catalog lists domain-available tools as affordances. It defines only capability, permission scope, credential boundary, write scope, side-effect risk, and forbidden authority refs. The executor chooses, skips, substitutes, combines, parallelizes, or asks for missing context within those boundaries during the attempt.

## PDF Export

- Capability: `runtime/native_helpers/bookforge_pdf_export.py` compiles Markdown sources to PDF through a BookForge-owned publication/typesetting backend adapter and can render PDF pages for inspection.
- Current backend: `pandoc-xelatex`, requiring Pandoc and XeLaTeX; page rendering uses `pdftoppm` when available.
- Write scope: caller-provided PDF, rendered page directory, and JSON manifest paths.
- Forbidden authority: this helper cannot create owner acceptance, publication approval, production readiness, or final export readiness claims.
- Forbidden implementation path: project-local Pillow/canvas/raster text drawing or bespoke page layout code as the normal PDF renderer.
