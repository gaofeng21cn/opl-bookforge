# Source Corpus

## Source refs

| id | source-ref | role in this pilot |
|---|---|---|
| S1 | `AGENTS.md` | authority boundary and validation entry point |
| S2 | `TASTE.md` | book-first preference, two-stage workflow, AI-flavor quality rule |
| S3 | `contracts/stage_control_plane.json` | stage ids, required refs, handoff closure refs |
| S4 | `contracts/action_catalog.json` | action ids `shape-storyline` and `materialize-book` |
| S5 | `agent/prompts/storyline-architecture.md` | storyline output expectations |
| S6 | `agent/prompts/book-materialization.md` | materialization output expectations |
| S7 | `agent/quality_gates/storyline-architecture-quality-gate.md` | storyline pass and fail-closed conditions |
| S8 | `agent/quality_gates/book-materialization-quality-gate.md` | manuscript, figure, table, style, layout gate |
| S9 | `docs/status.md` | baseline, OMA takeover, external-suite evidence and remaining gaps |
| S10 | `docs/evidence/oma-agent-lab/bookforge-ai-reviewer-evaluation.json` | independent reviewer critique and predicted next maturity gate |

## Corpus notes

The book uses BookForge's own contracts as source material. The pilot therefore tests the agent on a real domain surface instead of a synthetic topic. The manuscript may explain the workflow, but it may not claim final publication approval, export approval, or owner acceptance without an owner receipt.
