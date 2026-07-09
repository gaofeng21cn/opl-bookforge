# Source And Style Integrity Review Stage

Stage id: `source-style-integrity-review`
Action ref: `materialize-book`

This stage reviews materialized chapter packages for source/claim safety, style consistency, internal-language leakage, sentence integrity, and meta-review routing. It owns the integrity judgment before proof/export handoff.

The stage returns an integrity handoff to `publication-proof-handoff`, route-back refs to storyline or chapter stages, repair plans, typed blockers, or human gates.
