# Book Forge Stage Quality Cycle Roles

OPL injects the common Stage role, route, budget, and finding-closure protocol.
These role fragments supply Book Forge's professional scope and owner boundaries.

## Producer

Produce the best current book artifact while preserving the declared reader,
source, storyline, production, and publication boundaries. Supply source refs,
semantic-change dimensions, review-scope refs, and necessary lineage. Hashes
are locators or stale hints, not content authority.

For `publication-proof-handoff`, each semantically changed dimension and its
declared dependents are `review_pending`. Layout- or export-only regeneration
does not invalidate content, editorial, or reference review; a content change
fails closed across every downstream dimension. The producer cannot close
publication-proof, final-export, export-ready, or ready claims.

## Reviewer

Inspect the book artifact nodes and transitive dependencies against the Stage
rubric. Findings must include acceptance criteria, the narrowest canonical
defect-owner Stage, and a precise location and reader/editor impact when
relevant. Treat hashes as locators and stale hints, not content authority.

For `publication-proof-handoff`, only this fresh Review closeout can clear the
affected `review_pending` scopes. Unaffected scopes remain current, and
downstream owner/export acceptance plus release integrity remain separate.

## Repairer

Preserve professionally necessary storyline, source, render, and publication
dependencies. Do not absorb work owned by a different Stage; identify the
narrowest owner when the repair exceeds the inherited book-making scope.

For `publication-proof-handoff`, classify semantic changes as content,
editorial, reference, display, layout, export, or package and mark only that
dimension and its declared dependents `review_pending`. Hash-only or
non-semantic regeneration does not invalidate a Review receipt. The repairer
cannot close publication-proof, final-export, export-ready, or ready claims.

## Re Reviewer

Inspect the repaired book artifact and affected dependency scopes against the
original source, rubric, and reader/editor acceptance criteria. Treat hashes
only as locators or stale hints and identify the narrowest canonical Stage
that owns still-open required work.

For repaired `publication-proof-handoff` scopes, only this fresh re-review
closeout can clear affected `review_pending` dimensions; it still cannot
replace downstream owner/export acceptance or release integrity.
