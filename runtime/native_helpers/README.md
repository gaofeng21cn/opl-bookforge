# OPL BookForge Native Helpers

Place domain-specific helper implementations here only when they cannot be represented as declarative pack inputs. OPL owns the generic helper envelope and execution contract.

## PDF Export Helper

`bookforge_pdf_export.py` is the BookForge-owned Markdown-to-PDF export helper for owner-review PDFs and publication-layout candidates. It keeps manuscript prose in Markdown and delegates PDF layout to a real publication/typesetting backend.

Current backend:

- `pandoc-xelatex`: Pandoc standalone Markdown input, XeLaTeX PDF engine, optional Poppler page rendering through `pdftoppm`.
- Optional Pandoc profile controls: `--metadata-file` plus repeatable `-V/--variable`, so review and publication design profiles can control page geometry, fonts, document class, and related PDF variables without project-local renderer code.

Boundary:

- The helper may compile PDFs, render pages for inspection, and write a JSON manifest.
- It does not authorize publication readiness, owner acceptance, or final export approval.
- It must not be replaced by project-local raster text drawing, Pillow/canvas page painting, or bespoke layout engines as the normal path.

## Imagegen Asset Helper

`bookforge_imagegen_asset.py` is the BookForge-owned project-local bitmap materialization helper for final manuscript figures.

Default backend:

- `codex-native-imagegen`: launches a child Codex executor with `--enable image_generation`, requires the child executor to use the built-in `imagegen` / `image_generation` capability, and copies the final bitmap into the book project path.
- The helper records a JSON receipt with prompt hash, output path, image hash/dimensions, runtime surface, and token boundary.
- The helper does not read OpenAI Base URL, `OPENAI_API_KEY`, Codex provider tokens, or project secrets. Provider credentials remain owned by the Codex executor/native imagegen surface.

Boundary:

- Project-bound book figures must end as project-local PNG/WebP/JPEG assets and be tracked by the figure asset manifest.
- Chat previews and default `$CODEX_HOME/generated_images` files are not final book assets until copied into the book project and recorded.
- The `--mock` / `--self-test` paths only verify helper structure. Mock images must not be counted as final manuscript illustrations.
- API fallback is an explicit operator/owner route for large batches or unavailable built-in imagegen, not the default BookForge route.
