# OPL BookForge Native Helpers

Place domain-specific helper implementations here only when they cannot be represented as declarative pack inputs. OPL owns the generic helper envelope and execution contract.

## PDF Export Helper

`bookforge_pdf_export.py` is the BookForge-owned Markdown-to-PDF export helper for owner-review PDFs and publication-layout candidates. It keeps manuscript prose in Markdown and delegates PDF layout to a real publication/typesetting backend.

Current backend:

- `pandoc-xelatex`: Pandoc standalone Markdown input, XeLaTeX PDF engine, optional Poppler page rendering through `pdftoppm`.
- Optional Pandoc profile controls: `--metadata-file` plus repeatable `-V/--variable`, so review and publication design profiles can control page geometry, fonts, document class, and related PDF variables without project-local renderer code.
- Resource path controls: repeatable `--resource-path`, defaulting to the source Markdown directory plus project root, so relative figure paths in chapter Markdown can resolve in generated PDFs.
- Section numbering controls: `--number-sections` is the default for Markdown without pre-numbered chapter titles; pass `--no-number-sections` for cumulative review PDFs or manuscripts that already carry Chinese chapter/figure numbering, to avoid doubled headings such as `第七章 第五章`.
- Publication profile controls: `--publication-profile bookforge-zh-publication-proof` is the default bundled proof profile for Chinese nonfiction e-books. It applies an A5 electronic-book page, Chinese body/head fonts, running heads, footer page numbers, chapter-title hierarchy, caption styling, table/callout treatment, and visual-rhythm expectations. Pass `--publication-profile none` only for diagnostics or owner-approved custom styling.
- Asset and page checks: the helper scans Markdown image refs against the effective resource paths, checks required `figure_asset_manifest` items for `asset_ready` project-local bitmap files, and can write a machine-baseline rendered-page inspection JSON through `--write-rendered-page-inspection`.

Artifact roles:

- `review_pdf`: cumulative owner/editor reading checkpoint. A generated review PDF can pass its helper gate when the PDF compiles; rendered pages are strongly preferred for visual review, but it remains review-only.
- `publication_proof`: publication-layout candidate. It requires a publication design profile JSON, rendered page refs, and rendered-page inspection JSON in addition to PDF compilation.
- `final_export`: owner-gated export. It requires publication-proof evidence plus an owner/export acceptance receipt.

The helper records `artifact_gate.status` and blocker details separately from PDF compile status. A PDF can compile successfully and still return `generated_with_artifact_gate_blocker` when proof or final-export evidence is missing.

Publication-proof quality:

- Review PDFs may use simple styling for fast reading.
- Publication proofs should use the bundled `bookforge-zh-publication-proof` profile or an owner-approved equivalent. Unstyled Pandoc defaults are review-output quality, not publication-proof quality.
- Rendered-page inspection should sample front matter, chapter openings, dense body pages, figure/table pages, callouts, and closing pages for nonblank content, clipped glyphs, caption proximity, image rendering, header/footer/page-number presence, and monotony.
- Helper-generated rendered-page inspection is a machine baseline for nonblank pages, profile plumbing, and asset resolution. It is useful for continuous review PDFs and proof gates, but it is not a substitute for human publication-design review or owner final-export acceptance.

Boundary:

- The helper may compile PDFs, render pages for inspection, and write a JSON manifest.
- It does not authorize publication readiness, owner acceptance, or final export approval.
- It must not be replaced by project-local raster text drawing, Pillow/canvas page painting, or bespoke layout engines as the normal path.

Examples:

```bash
python3 runtime/native_helpers/bookforge_pdf_export.py \
  --root "$BOOK_PROJECT" \
  --source-md "$BOOK_PROJECT/artifacts/manuscript/book.preview.md" \
  --output-pdf "$BOOK_PROJECT/exports/book-review.pdf" \
  --render-dir "$BOOK_PROJECT/exports/rendered-pages" \
  --artifact-role review_pdf \
  --no-number-sections \
  --manifest "$BOOK_PROJECT/receipts/book-review-pdf.json"
```

```bash
python3 runtime/native_helpers/bookforge_pdf_export.py \
  --root "$BOOK_PROJECT" \
  --source-md "$BOOK_PROJECT/artifacts/manuscript/book.md" \
  --output-pdf "$BOOK_PROJECT/exports/book-publication-proof.pdf" \
  --render-dir "$BOOK_PROJECT/exports/rendered-pages" \
  --artifact-role publication_proof \
  --publication-profile bookforge-zh-publication-proof \
  --publication-design-profile "$BOOK_PROJECT/publication-design/profile.json" \
  --write-rendered-page-inspection "$BOOK_PROJECT/quality/rendered-page-inspection.machine.json" \
  --figure-asset-manifest "$BOOK_PROJECT/artifacts/figures/figure-asset-manifest.json" \
  --manifest "$BOOK_PROJECT/receipts/book-publication-proof.json"
```

## Imagegen Asset Helper

`bookforge_imagegen_asset.py` is the BookForge-owned project-local bitmap materialization helper for final manuscript figures.

Default backend:

- `codex-native-imagegen`: launches a child Codex executor with `--enable image_generation`, requires the child executor to use the built-in `imagegen` / `image_generation` capability, and copies the final bitmap into the book project path.
- The helper records a JSON receipt with prompt hash, output path, image hash/dimensions, runtime surface, and token boundary.
- Project-relative `--prompt-file`, `--output-file`, `--manifest`, `--receipt-file`, and `--asset-manifest` paths are resolved against `--root`, not the caller's current directory.
- Pass `--asset-manifest` during generation to update the figure asset manifest by `figure_id` after receipt creation. Pass `--update-asset-manifest --receipt-file <receipt>` to backfill a manifest from an existing helper receipt without generating a new image.
- The helper does not read OpenAI Base URL, `OPENAI_API_KEY`, Codex provider tokens, or project secrets. Provider credentials remain owned by the Codex executor/native imagegen surface.

Boundary:

- Project-bound book figures must end as project-local PNG/WebP/JPEG assets and be tracked by the figure asset manifest.
- Chat previews and default `$CODEX_HOME/generated_images` files are not final book assets until copied into the book project and recorded.
- The `--mock` / `--self-test` paths only verify helper structure. Mock images must not be counted as final manuscript illustrations.
- API fallback is an explicit operator/owner route for large batches or unavailable built-in imagegen, not the default BookForge route.
