#!/usr/bin/env python3
"""Exercise Book Forge's actual Framework action scope and knowledge consumer."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

from stage_topology_cases.hosted_runtime_and_schema import framework_candidate_roots


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    framework = next(
        root for root in framework_candidate_roots(repo)
        if (root / "src/adapters/execution/standard-agent-action-runtime-parts/action-context.ts").is_file()
        or (root / "dist/adapters/execution/standard-agent-action-runtime-parts/action-context.js").is_file()
    )
    tree, suffix = ("src", ".ts") if (framework / "src").is_dir() else ("dist", ".js")

    def module(ref: str) -> str:
        return json.dumps((framework / tree / f"{ref}{suffix}").as_uri())

    with tempfile.TemporaryDirectory(prefix="obf-book-knowledge-") as directory:
        temporary = Path(directory).resolve()
        state = temporary / "state"
        workspace = temporary / "workspace"
        state.mkdir()
        project_a, project_b = workspace / "projects/book-a", workspace / "projects/book-b"
        project_a.mkdir(parents=True)
        project_b.mkdir(parents=True)
        (workspace / "workspace_index.json").write_text(json.dumps({
            "projects": [
                {"project_id": "book-a", "project_root": "projects/book-a"},
                {"project_id": "book-b", "project_root": "projects/book-b"},
            ],
        }))
        (state / "workspace-registry.json").write_text(json.dumps({
            "version": "g2",
            "bindings": [{
                "binding_id": "bookforge-knowledge-fixture",
                "project_scope_id": "project:bookforge-knowledge-fixture",
                "project_id": "opl-bookforge",
                "project": "OPL Book Forge",
                "workspace_path": str(workspace),
                "label": None,
                "status": "active",
                "direct_entry": {},
                "created_at": "2026-11-09T00:00:00Z",
                "updated_at": "2026-11-09T00:00:00Z",
                "archived_at": None,
            }],
        }))
        source = temporary / "user-knowledge"
        source.mkdir()
        bindings_dir = workspace / "shared/memory"
        bindings_dir.mkdir(parents=True)
        items = []
        for kind, scope_id in [("owner", "author"), ("topic", "editing"),
                               ("project", "book-a"), ("project", "book-b")]:
            knowledge_id = f"bookforge-fixture.{scope_id}"
            body = f"# {scope_id}\nCanonical {kind} knowledge for {scope_id}.\n"
            ref = f"{scope_id}.md"
            (source / ref).write_text(body)
            items.append({
                "surface_kind": "opl_durable_knowledge_item",
                "version": "durable-knowledge-item.v2",
                "knowledge_id": knowledge_id,
                "title": scope_id,
                "scope": {"kind": kind, "id": scope_id},
                "content_kind": "policy",
                "requirement": "required",
                "owner": "fixture-author",
                "body_ref": {"kind": "source_path", "source_id": "author.notes", "ref": ref,
                             "sha256": "sha256:" + hashlib.sha256(body.encode()).hexdigest()},
                "applicability": {"domains": ["opl-bookforge"],
                                  "stages": ["storyline-architecture", "chapter-production-planning"]},
                "status": "active",
                "reviewed_at": "2026-11-09T00:00:00Z",
                "next_review_at": "2099-01-01T00:00:00Z",
                "authority_boundary": {"semantic_body_owner": "fixture-author",
                                       "opl_role": "catalog_recall_and_receipt_projection_only"},
            })
        registry_path = bindings_dir / "knowledge-sources.json"
        scope_ids = [item["scope"]["id"] for item in items]
        registry_path.write_text(json.dumps({
            "surface_kind": "opl_knowledge_source_registry", "version": "knowledge-source-registry.v2",
            "registry_id": "fixture-author.sources", "owner": "fixture-author",
            "sources": [{"source_id": "author.notes", "root": str(source), "status": "active",
                         "writable": False, "grants": [{"workspace_root": str(workspace),
                            "domains": ["opl-bookforge"], "scope_ids": scope_ids}]}],
            "items": items,
        }))
        (bindings_dir / "knowledge-bindings.json").write_text(json.dumps({
            "surface_kind": "opl_knowledge_source_bindings", "version": "knowledge-source-bindings.v2",
            "registries": [{"registry_ref": str(registry_path), "source_ids": ["author.notes"],
                            "scope_ids": scope_ids}],
            "required_knowledge_ids": [],
        }))
        script = f"""
import assert from 'node:assert/strict';
import {{ resolveActionExecutionScope }} from {module('adapters/execution/standard-agent-action-runtime-parts/action-context')};
import {{ readHostedAgentRuntimeActionContracts }} from {module('adapters/execution/hosted-agent-runtime-binding')};
import {{ assertRepoJsonSchemaPayload }} from {module('kernel/repo-json-schema')};
import {{ bindDurableKnowledgeContext, resolveKnowledgeSourceItem }} from {module('authority/packages/durable-knowledge-catalog')};
const repo = {json.dumps(str(repo))};
const workspace = {json.dumps(str(workspace))};
const {{ catalog }} = readHostedAgentRuntimeActionContracts(repo, ['opl-bookforge']);
let checks = 0;
let knowledgeChecks = 0;
for (const action of catalog.actions) {{
  const validate = (payload) => assertRepoJsonSchemaPayload({{
    repoRoot: repo, schemaRef: action.input_schema_ref, payload, label: action.action_id,
  }});
  assert.throws(() => validate({{workspace_root: workspace}}));
  assert.throws(() => validate({{workspace_root: workspace, book_id: '../book-a'}}));
  validate({{workspace_root: workspace, book_id: 'book-a'}});
  const resolve = (payload) => resolveActionExecutionScope({{
    action, payload, workspaceRoot: workspace, checkoutRoot: repo,
    runtimeDomainId: 'opl-bookforge', acceptedProjectIds: ['opl-bookforge'],
  }});
  assert.throws(() => resolve({{workspace_root: workspace}}));
  assert.throws(() => resolve({{workspace_root: workspace, book_id: 'unknown'}}));
  const a = resolve({{workspace_root: workspace, book_id: 'book-a'}});
  const b = resolve({{workspace_root: workspace, book_id: 'book-b'}});
  assert.equal(a.domain_work_item_id, 'book-a');
  assert.equal(a.canonical_work_item_root, {json.dumps(str(project_a))});
  assert.equal(b.canonical_work_item_root, {json.dumps(str(project_b))});
  assert.notEqual(a.work_item_scope_id, b.work_item_scope_id);
  checks += 9;
  const context = (projectRoot) => bindDurableKnowledgeContext({{
    repoDir: repo, domainPackRoot: repo, workspaceRoot: workspace, projectRoot,
    domainId: 'opl-bookforge', stageId: action.stage_route.entry_stage_ref,
    now: new Date('2026-11-09T12:00:00Z'),
  }});
  for (const [scope, expected, other] of [[a, 'book-a', 'book-b'], [b, 'book-b', 'book-a']]) {{
    const result = context(scope.canonical_work_item_root);
    const privateBodies = result.bodies.filter((body) => body.scope.kind !== 'product');
    assert.deepEqual(privateBodies.map((body) => body.scope.id).sort(), ['author', 'editing', expected].sort());
    assert.equal(privateBodies.find((body) => body.scope.id === expected).content,
      `# ${{expected}}\nCanonical project knowledge for ${{expected}}.\n`);
    assert.equal(result.receipt.quality_debt.length, 0);
    assert.throws(() => resolveKnowledgeSourceItem({{
      workspaceRoot: workspace, projectRoot: scope.canonical_work_item_root,
      domainId: 'opl-bookforge', knowledgeId: `bookforge-fixture.${{other}}`,
    }}), /knowledge_source_unavailable/);
    knowledgeChecks += 4;
  }}
  assert.deepEqual(context(null).bodies.filter((body) => body.scope.kind !== 'product')
    .map((body) => body.scope.id).sort(), ['author', 'editing']);
  knowledgeChecks += 1;
}}
console.log(JSON.stringify({{status: 'passed', action_scope_checks: checks, knowledge_isolation_checks: knowledgeChecks}}));
"""
        command = ["node", "--conditions=opl-source"]
        if suffix == ".ts":
            command.append("--experimental-strip-types")
        completed = subprocess.run(
            [*command, "--input-type=module", "-e", script],
            cwd=repo,
            env={**os.environ, "OPL_STATE_DIR": str(state)},
            text=True,
            capture_output=True,
            check=False,
        )
        assert completed.returncode == 0, {"stdout": completed.stdout, "stderr": completed.stderr}
        print(completed.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
