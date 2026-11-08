# Chapter Materialization Stage

Stage id: `chapter-materialization`
Action ref: `materialize-book`

This stage writes or repairs chapter packages from approved task cards and context packs. It owns the chapter drafting judgment and returns per-chapter Markdown refs, chapter QC refs, repair refs, in-progress states, route-back refs, or typed blockers.

The stage does not own source/style integrity verdicts, independent meta-review pass, review-PDF generation, publication proof, final export, or owner acceptance.
