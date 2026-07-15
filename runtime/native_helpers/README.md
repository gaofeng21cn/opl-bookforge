# OPL Book Forge Native Helpers

Place domain-specific helper implementations here only when they cannot be represented as declarative pack inputs. OPL owns no-authority helper entrypoint and executable probes; Book Forge retains only domain execution and receipt behavior.

`scripts/verify.sh full-local` runs the complete repo-owned policy/helper/PDF/handler suite without OPL scaffold, generated-interface, or source-closure validation. It is useful while a cross-repo OPL contract/parser release is in flight, but it cannot replace `scripts/verify.sh structural` or `scripts/verify.sh full` for final framework conformance.

## PDF Export Helper

`bookforge_pdf_export.py` is the Book Forge-owned Markdown-to-PDF export helper for owner-review PDFs and publication-layout candidates. It keeps manuscript prose in Markdown and delegates PDF layout to a real publication/typesetting backend.

Current backend:

- `pandoc-xelatex`: Pandoc standalone Markdown input, XeLaTeX PDF engine, optional Poppler page rendering through `pdftoppm`.
- Optional Pandoc profile controls: `--metadata-file` plus repeatable `-V/--variable`, so review and publication design profiles can control page geometry, fonts, document class, and related PDF variables without project-local renderer code.
- Resource path controls: repeatable `--resource-path`, defaulting to the source Markdown directory plus project root, so relative figure paths in chapter Markdown can resolve in generated PDFs.
- Section numbering controls: `--number-sections` is the default for Markdown without pre-numbered chapter titles; pass `--no-number-sections` for cumulative review PDFs or manuscripts that already carry Chinese chapter/figure numbering, to avoid doubled headings such as `第七章 第五章`.
- Publication profile controls: `--publication-profile bookforge-zh-publication-proof` is the default bundled proof profile for Chinese nonfiction e-books. It applies an A5 electronic-book page, CTEX-distributed Fandol Chinese body/head fonts, running heads, footer page numbers, chapter-title hierarchy, caption styling, table/callout treatment, and visual-rhythm expectations. The profile selects `fontset=fandol` explicitly so proof compilation does not depend on macOS font auto-detection or user-only fonts. Pass `--publication-profile none` only for diagnostics or owner-approved custom styling.
- Asset and page checks: the helper scans Markdown image refs against the effective resource paths, checks required `figure_asset_manifest` items for `asset_ready` project-local bitmap files, and can write a machine-baseline rendered-page inspection JSON through `--write-rendered-page-inspection`.

Dependency route:

- OPL owns local helper dependency diagnosis and maintenance for this profile through `opl system dependency-doctor --profile bookforge-publication-proof --json` and `opl system dependency-maintenance --profile bookforge-publication-proof --json`.
- Book Forge owns the proof helper, proof profile, artifact gates, manuscript evidence, and owner/export boundaries; it does not implement a system package manager or TeX installer.
- Missing required dependencies block `publication_proof` and `final_export` claims, but they do not block unrelated storyline, chapter drafting, context compilation, claim integrity, or style calibration progress when a narrower honest writing action remains available.
- The bundled `bookforge-zh-publication-proof` header no longer requires `titling.sty` or `tocloft.sty`; OPL may report those packages as legacy diagnostics, but they are not current proof blockers.

Artifact roles:

- `review_pdf`: cumulative owner/editor reading checkpoint. A generated review PDF can pass its helper gate when the PDF compiles; rendered pages are strongly preferred for visual review, but it remains review-only.
- `publication_proof`: publication-layout candidate. It requires a publication design profile JSON, rendered page refs, and rendered-page inspection JSON in addition to PDF compilation.
- `final_export`: owner-gated export. It requires publication-proof evidence plus an owner/export acceptance receipt.

The helper records `artifact_gate.status` and quality-debt details separately from PDF compile status. A readable PDF returns `generated_with_quality_debt` when proof or final-export evidence is missing; that debt blocks publication/final-export/readiness claims but does not block stage transition.

Publication-proof quality:

- Review PDFs may use simple styling for fast reading.
- Publication proofs should use the bundled `bookforge-zh-publication-proof` profile or an owner-approved equivalent. Unstyled Pandoc defaults are review-output quality, not publication-proof quality.
- Rendered-page inspection should sample front matter, chapter openings, dense body pages, figure/table pages, callouts, and closing pages for nonblank content, clipped glyphs, caption proximity, image rendering, header/footer/page-number presence, and monotony.
- Helper-generated rendered-page inspection is a machine baseline for nonblank pages, profile plumbing, and asset resolution. It is useful for continuous review PDFs and proof gates, but it is not a substitute for human publication-design review or owner final-export acceptance.

Boundary:

- The helper may compile PDFs, render pages for inspection, and write a JSON manifest.
- Its probe binds every process and artifact-write slot to the exact helper bytes. Process targets are limited to the probe's declared publication commands, while artifact writes use only carrier-provided artifact slots; neither surface grants route, lifecycle, executor, receipt, verdict, or readiness authority.
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

## Image Asset Authority Handler

`bookforge_imagegen_asset.py` is the Book Forge-owned read-only authority handler for final manuscript figures. It does not generate assets. OPL first materializes a bitmap into a host-allocated workspace output and injects immutable attempt/output refs, the workspace-relative bitmap ref, SHA-256, and figure metadata.

Handler contract:

- `contracts/domain_handler_registry.json` is the closed OPL registry ABI: top level contains only `surface_kind`, `version`, and `handlers`; the single entry contains only `handler_id` and a `python_callable` binding. It exposes no shell command or stage/action entry.
- `contracts/schemas/imagegen-host-bitmap.input.schema.json` defines host input; `contracts/schemas/imagegen-host-bitmap.output.schema.json` defines the authority-candidate / quality-debt result.
- The handler rejects absolute/escaping refs, symlink traversal, non-regular files, empty or malformed bitmaps, unsupported or mismatched formats, missing/invalid dimensions, digest mismatch, and optional media-type/minimum-dimension mismatch.
- Validation reads at most 64 MiB from the single host-injected bitmap ref; larger files return image quality debt before their body is read. PNG IDAT validation is streamed with a 256 MiB decompressed-payload ceiling, so compressed input cannot trigger unbounded memory expansion.
- Valid PNG/JPEG/WebP bytes produce a `bookforge_figure_authority_receipt_candidate.v1` plus an asset-manifest entry candidate. OPL owns persistence of both candidates.
- Ordinary missing/invalid output produces `completed_with_quality_debt`, does not block later stage work, and closes figure-ready/publication/export claims.

Boundary:

- Project-bound book figures must be workspace-contained regular PNG/WebP/JPEG files with matching host-provided SHA-256 and inspectable figure metadata.
- The handler cannot create an execution request, spawn OPL/Codex, discover providers/tokens, generate or copy bitmap bytes, or write receipt/manifest/workspace state.
- The registered callable is reached only through `handler:obf.figure-asset-authority-evaluate`. The richer host handoff contract preserves schema validation, immutable attempt/output/ref/SHA binding, read-only containment, and OPL-owned persistence without expanding the closed registry ABI.
- A candidate is not visual review, publication proof, final export, owner acceptance, domain readiness, or production readiness.
- `--self-test` is an in-memory parser check only and creates no bitmap or other file.
