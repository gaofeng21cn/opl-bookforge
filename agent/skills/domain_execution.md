# OPL Book Forge Domain Execution Skill Policy

The direct domain skill is the owner path for domain execution. OPL-generated CLI, MCP, product-entry, sidecar, status, and workbench surfaces route to declared domain handlers or refs-only adapters and require owner receipts for mutating or verdict-bearing outcomes.

Temporal-backed StageRun/provider attempts are OPL-owned execution refs, not Book Forge runtime state. Domain execution may consume those refs for provenance and handoff, but Book Forge stage closeout still requires an `owner_receipt_ref`, `typed_blocker_ref`, `human_gate_ref`, or `route_back_ref`; provider completion and generated surface readiness are not domain completion.
