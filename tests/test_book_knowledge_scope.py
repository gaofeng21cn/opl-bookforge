#!/usr/bin/env python3
"""Exercise Book Forge's v2 knowledge permissions, book_id schema containment, and workspace isolation."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile

from stage_topology_cases.hosted_runtime_and_schema import ContractShapeError, _validate_node


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    manifest = json.loads((repo / "opl-package.json").read_text(encoding="utf-8"))
    catalog = json.loads((repo / "contracts/action_catalog.json").read_text(encoding="utf-8"))

    # Verify v2 manifest declares personal/topic/project read-only knowledge scopes.
    scopes = {item["scope"]: item["access"] for item in manifest["permissions"]["knowledge"]}
    assert scopes == {
        "personal_profile": "read",
        "long_term_topic": "read",
        "project_local": "read",
    }, scopes

    # Verify input schemas reject missing/traversing book_id values.
    checks = 0
    for action in catalog["actions"]:
        schema = json.loads((repo / action["input_schema_ref"]).read_text(encoding="utf-8"))
        for bad in ({"workspace_root": "/tmp/ws"}, {"workspace_root": "/tmp/ws", "book_id": "../book-a"}):
            try:
                _validate_node(schema, schema, bad, action["action_id"])
            except ContractShapeError:
                checks += 1
            else:
                raise AssertionError(f"Expected validation rejection for {bad}")
        _validate_node(schema, schema, {"workspace_root": "/tmp/ws", "book_id": "book-a"}, action["action_id"])
        checks += 1

    # Verify runtime contribution reader enforces strict book containment across books.
    spec = importlib.util.spec_from_file_location("book_review", repo / "runtime/native_helpers/bookforge_app_review.py")
    assert spec and spec.loader
    review = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(review)

    with tempfile.TemporaryDirectory(prefix="obf-book-knowledge-") as directory:
        ws = Path(directory).resolve()
        (ws / "projects/book-a").mkdir(parents=True)
        (ws / "projects/book-b").mkdir(parents=True)
        (ws / "workspace_index.json").write_text(json.dumps({
            "projects": [
                {"project_id": "book-a", "project_root": "projects/book-a"},
                {"project_id": "book-b", "project_root": "projects/book-b"},
            ]
        }), encoding="utf-8")
        (ws / "projects/book-a/a.md").write_text("# Book A\n", encoding="utf-8")
        (ws / "projects/book-b/b.md").write_text("# Book B\n", encoding="utf-8")

        ready = review.read_review({"book_id": "book-a", "artifact_path": "projects/book-a/a.md"}, str(ws))
        assert ready["state"] == "ready"
        try:
            review.read_review({"book_id": "book-a", "artifact_path": "projects/book-b/b.md"}, str(ws))
        except ValueError as err:
            assert "selected book" in str(err)
        else:
            raise AssertionError("Cross-book manuscript read was not rejected")
        checks += 2

    print(json.dumps({"status": "passed", "action_scope_checks": checks}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
