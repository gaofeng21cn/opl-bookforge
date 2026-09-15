<p align="center">
  <img src="assets/branding/opl-bookforge-logo.png" alt="OPL Book Forge logo" width="132" />
</p>

<p align="center">
  <a href="./README.md"><strong>English</strong></a> | <a href="./README.zh-CN.md">中文</a>
</p>

# OPL Book Forge

An OPL book-authoring domain package for storyline design, chapter production,
source/style review, figures and tables, publication proof, and export handoff.
Book Forge owns book meaning, artifacts, quality, memory, and acceptance boundaries;
OPL Framework provides shared execution and generated interfaces.

The canonical Agent and Package id is `obf`. Repository, domain, and Codex
Plugin locators use `opl-bookforge`.

![OPL Book Forge overview](assets/branding/opl-bookforge-overview-v2.png)

## Start A Book

Provide the book brief, intended readers, source material, voice requirements,
target extent, and desired handoff. For example:

- "Shape a storyline from these sources, define the reader promise and chapter thesis chain, and return it for owner review."
- "Materialize this approved storyline into chapter Markdown, with figures/tables, source/style review, and a review PDF."
- "Review this manuscript and identify whether repair belongs in its storyline, chapter function, evidence, publication design, or local prose."

`shape-storyline` ends at storyline handoff. With accepted storyline refs,
`materialize-book` enters production planning and proceeds through chapter
materialization, source/style integrity review, and publication-proof handoff.
Review PDF, publication proof, and final export have separate evidence and owner
requirements. See [Architecture](docs/architecture.md) for the stage model and
[Status](docs/status.md) for current evidence limits. The retained short-book
pilot is historical and owner-blocked; it does not prove current five-stage
execution, independent Package publication, or production readiness.

## Installation

Install through the standard OPL Package entry:

```bash
opl packages install obf --json
opl packages status --package-id obf --json
```

The publication channel is `ghcr.io/gaofeng21cn/one-person-lab-packages/obf`. Immutable versions identify exact releases; `latest-stable` selects the current version. OPL and the native plugin manager handle installation and updates. Separate GitHub Release pages and attachments are not used for distribution.

Start a new task after installation to load the professional skills. Package installation, runtime callability, and domain acceptance remain separate; see [Current Status](./docs/status.md).

## Verification

Read [AGENTS.md](AGENTS.md) before editing and use the
[documentation guide](docs/README.md) to locate the topic owner. Cloning this
repository does not install Framework or a hosted runtime. The verification
script defaults to the sibling Framework checkout; set `OPL_BIN` and
`OPL_FRAMEWORK_ROOT` when using another checkout.

| Command | Executed checks |
| --- | --- |
| `scripts/verify.sh` | Fast local policy and contract checks |
| `scripts/verify.sh structural` | Policy plus Framework agent check and source-hygiene readback |
| `scripts/verify.sh helpers` | Native-helper probes, adapters, and image authority handler |
| `scripts/verify.sh pdf` | Real review-PDF and publication-proof compile/render paths |
| `scripts/verify.sh full-local` | Local policy/helper/PDF/handler union |
| `scripts/verify.sh full` | Local union plus Framework structural readback |

PDF execution requires Pandoc, XeLaTeX, the declared rendering tools, and Pillow
in the Python environment for machine page inspection. For an isolated local
verification environment, `uv run --with pillow scripts/verify.sh full-local`
supplies Pillow without adding source-checkout dependencies.
[Native helpers](runtime/native_helpers/README.md) documents dependency diagnosis,
arguments, artifact roles, and handler limits. Negative PDF gate variants run
against the canonical gate without redundant recompilation.

The historical pilot can be checked independently:

```bash
python3 docs/evidence/production-readiness/bookforge-real-book-pilot-2026-06-18/tools/verify_pilot.py
```

Each command proves only its checked surface. Book/publication/export acceptance
still requires the corresponding domain artifacts and owner receipts.

## Reference

- [Documentation responsibilities and lifecycle](docs/README.md)
- [Agent entry and methods](agent/README.md)
- [Contracts](contracts/)
- [Evidence packages](docs/evidence/README.md)
