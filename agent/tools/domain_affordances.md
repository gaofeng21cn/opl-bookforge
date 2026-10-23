# OPL Book Forge Domain Tool Affordances

This catalog lists domain-available tools as affordances. It defines only capability, permission scope, credential boundary, write scope, side-effect risk, and forbidden authority refs. The executor chooses, skips, substitutes, combines, parallelizes, or asks for missing context within those boundaries during the attempt.

## PDF Export

- Capability: `runtime/native_helpers/bookforge_pdf_export.py` compiles Markdown sources to PDF through a Book Forge-owned publication/typesetting backend adapter and can render PDF pages for inspection.
- Current backend: `pandoc-xelatex`, requiring Pandoc and XeLaTeX; page rendering uses `pdftoppm` when available.
- OPL dependency route: use `opl system dependency-doctor --profile bookforge-publication-proof --json` for local dependency diagnosis and `opl system dependency-maintenance --profile bookforge-publication-proof --json` for the OPL-owned maintenance plan. Do not add Book Forge-private OS/TeX package installation logic.
- Write scope: caller-provided PDF, rendered page directory, and JSON manifest paths.
- Forbidden authority: this helper cannot create owner acceptance, publication approval, production readiness, or final export readiness claims.
- Forbidden implementation path: project-local Pillow/canvas/raster text drawing or bespoke page layout code as the normal PDF renderer.

## Paired Word And PDF Export

- Capability: `runtime/native_helpers/bookforge_publication_bundle.py` materializes an editable DOCX and typeset PDF from the same manuscript, identity metadata and assets under `materialize-book` / `publication-proof-handoff`.
- Contract: `contracts/publication_bundle_contract.json`. Select the book's reference DOCX and publication design profile from its accepted sample/style contract. There is no universal book layout or mandatory teaching-scene component.
- Invocation: `python3 runtime/native_helpers/bookforge_publication_bundle.py --root BOOK_ROOT --source-md CHAPTER.md --output-dir OUTPUT --basename NAME --title TITLE --author AUTHOR --date DATE --reference-doc REFERENCE.docx --publication-profile PROFILE.json`. Repeat `--resource-path` for figure locations. Set `--soffice` to the host bundled LibreOffice executable when available.
- The helper resolves assets, renders both formats, checks source-token coverage, title/byline/date, table and figure counts, and embedded PDF fonts. It retains build inputs, PDF receipt, rendered pages and a SHA-256-bound bundle manifest. Text-order equality is diagnostic because PDF table extraction can reorder cells.
- Write scope: caller-provided output and QA directories. Review every rendered page before delivery; a machine-ready bundle is a candidate for owner review, not a publication or final-export acceptance receipt.
- Dependencies: the OPL-owned `bookforge-publication-proof` profile covers Pandoc, XeLaTeX, LibreOffice and Poppler. Book Forge does not install private system runtimes.
