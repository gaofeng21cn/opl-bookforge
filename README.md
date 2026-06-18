# OPL BookForge

OPL BookForge is an OPL-standard Foundry Agent domain pack for writing books. It keeps the OPL series naming style in the repo slug `opl-bookforge`, while using `OPL BookForge` as the product name.

The workflow has two primary stages:

- `storyline-architecture`: shape the premise, reader promise, argument arc, source map, chapter thesis chain, and writing style contract.
- `book-materialization`: materialize the book as chapters, illustration plans, table plans, style pass, layout checks, and owner-gated handoff refs.

This repo is a declarative domain pack plus minimal authority-function surface. OPL owns generated interfaces and framework runtime projection. OPL BookForge owns domain truth, book quality/export decisions, artifact authority, memory body, and owner receipts.

## Verification

Run:

```bash
scripts/verify.sh
```

The script validates the OPL standard scaffold and generated interfaces through the local OPL CLI.

Current baseline evidence:

- `opl agents scaffold --validate . --json`: passed
- `opl agents interfaces --repo-dir . --json`: ready

These checks prove the structural baseline and generated interface descriptors. They do not prove production readiness, book-delivery quality, publication readiness, or owner acceptance.
