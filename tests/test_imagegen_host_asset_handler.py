#!/usr/bin/env python3
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO / "runtime/native_helpers/bookforge_imagegen_asset.py"


def load_helper():
    spec = importlib.util.spec_from_file_location("bookforge_imagegen_asset", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def png_chunk(kind: bytes, payload: bytes) -> bytes:
    checksum = zlib.crc32(kind + payload) & 0xFFFFFFFF
    return len(payload).to_bytes(4, "big") + kind + payload + checksum.to_bytes(4, "big")


def png_bytes(width: int = 16, height: int = 12) -> bytes:
    header = width.to_bytes(4, "big") + height.to_bytes(4, "big") + b"\x08\x06\x00\x00\x00"
    rows = b"".join(b"\x00" + b"\x00\x00\x00\xff" * width for _ in range(height))
    return (
        b"\x89PNG\r\n\x1a\n"
        + png_chunk(b"IHDR", header)
        + png_chunk(b"IDAT", zlib.compress(rows))
        + png_chunk(b"IEND", b"")
    )


def jpeg_bytes(width: int = 19, height: int = 13) -> bytes:
    components = b"\x01\x11\x00\x02\x11\x00\x03\x11\x00"
    sof = b"\x08" + height.to_bytes(2, "big") + width.to_bytes(2, "big") + b"\x03" + components
    return b"\xff\xd8\xff\xc0" + (len(sof) + 2).to_bytes(2, "big") + sof + b"\xff\xda\x00\x02\xff\xd9"


def webp_bytes(width: int = 23, height: int = 17) -> bytes:
    payload = b"\x00\x00\x00\x00" + (width - 1).to_bytes(3, "little") + (height - 1).to_bytes(3, "little")
    chunk = b"VP8X" + len(payload).to_bytes(4, "little") + payload
    body = b"WEBP" + chunk
    return b"RIFF" + len(body).to_bytes(4, "little") + body


def request(root: Path, bitmap_ref: str, data: bytes) -> dict[str, object]:
    return {
        "surface_kind": "opl_bookforge_host_bitmap_validation_request",
        "schema_version": 1,
        "host_context": {
            "workspace_root": str(root),
            "attempt_ref": "stage-run://obf/attempt-1",
            "output_ref": "stage-run://obf/attempt-1/output/figure-1",
        },
        "bitmap": {
            "bitmap_ref": bitmap_ref,
            "sha256": f"sha256:{hashlib.sha256(data).hexdigest()}",
            "format": "png",
            "media_type": "image/png",
        },
        "figure": {
            "figure_id": "figure-1",
            "title": "Figure 1",
            "artifact_role": "book_manuscript_figure",
            "prompt_sha256": "sha256:" + "1" * 64,
            "caption_intent": "Explain the chapter model.",
            "review_criteria": ["labels are legible"],
            "minimum_width": 8,
            "minimum_height": 8,
        },
    }


def assert_read_only_handler_source(source: str) -> None:
    tree = ast.parse(source)
    forbidden_imports = {
        "asyncio",
        "http",
        "httpx",
        "multiprocessing",
        "openai",
        "requests",
        "shutil",
        "socket",
        "sqlite3",
        "subprocess",
        "tempfile",
        "urllib",
    }
    imported_roots: set[str] = set()
    forbidden_calls = {
        "call",
        "check_call",
        "check_output",
        "chmod",
        "connect",
        "copy",
        "copy2",
        "copyfile",
        "exec",
        "eval",
        "hardlink_to",
        "makedirs",
        "mkdir",
        "open_connection",
        "popen",
        "putenv",
        "remove",
        "rename",
        "replace",
        "request",
        "rmdir",
        "run",
        "send",
        "sendall",
        "spawn",
        "symlink_to",
        "system",
        "touch",
        "unlink",
        "urlopen",
        "write",
        "write_bytes",
        "write_text",
    }
    observed_forbidden_calls: set[str] = set()
    framework_primitives: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".", 1)[0])
            if node.module == "opl_framework.artifact_inspection":
                framework_primitives.update(alias.name for alias in node.names)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {"__import__", "compile", "eval", "exec"}:
                observed_forbidden_calls.add(node.func.id)
            elif isinstance(node.func, ast.Attribute) and node.func.attr in forbidden_calls:
                observed_forbidden_calls.add(node.func.attr)
    assert imported_roots.isdisjoint(forbidden_imports), imported_roots & forbidden_imports
    assert not observed_forbidden_calls, observed_forbidden_calls
    assert source.count('.open("rb")') == 0, "handler must delegate binary reads to Framework"
    assert {
        "ContainedFileReadError",
        "read_contained_regular_file",
        "sha256_bytes",
    } <= framework_primitives, framework_primitives


def main() -> int:
    helper = load_helper()
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert_read_only_handler_source(source)

    registry = json.loads((REPO / "contracts/domain_handler_registry.json").read_text(encoding="utf-8"))
    descriptor = json.loads((REPO / "contracts/domain_descriptor.json").read_text(encoding="utf-8"))
    compiler_input = json.loads((REPO / "contracts/pack_compiler_input.json").read_text(encoding="utf-8"))
    source_closure_audit = json.loads((REPO / "contracts/source_closure_audit.json").read_text(encoding="utf-8"))
    action_catalog = json.loads((REPO / "contracts/action_catalog.json").read_text(encoding="utf-8"))
    assert descriptor["standard_contract_refs"]["domain_handler_registry"] == "contracts/domain_handler_registry.json"
    assert descriptor["standard_contract_refs"]["source_closure_audit"] == "contracts/source_closure_audit.json"
    assert compiler_input["source_refs"]["domain_handler_registry_source_ref"] == "contracts/domain_handler_registry.json"
    assert compiler_input["source_refs"]["source_closure_audit_source_ref"] == "contracts/source_closure_audit.json"
    assert source_closure_audit == {
        "surface_kind": "standard_agent_source_closure_audit",
        "version": "standard-agent-source-closure-audit.v1",
        "entries": [],
    }
    assert set(registry) == {"surface_kind", "version", "handlers"}, registry
    handler = registry["handlers"][0]
    assert set(handler) == {"handler_id", "binding"}, handler
    assert handler["handler_id"] == "obf.figure-asset-authority-evaluate", handler
    assert handler["binding"] == {
        "kind": "python_callable",
        "module": "runtime.native_helpers.bookforge_imagegen_asset",
        "callable": "evaluate_host_bitmap",
    }, handler
    for schema_ref in (
        "contracts/schemas/imagegen-host-bitmap.input.schema.json",
        "contracts/schemas/imagegen-host-bitmap.output.schema.json",
    ):
        schema = json.loads((REPO / schema_ref).read_text(encoding="utf-8"))
        assert schema["$schema"].endswith("2020-12/schema"), schema_ref
    input_schema = json.loads((REPO / "contracts/schemas/imagegen-host-bitmap.input.schema.json").read_text(encoding="utf-8"))
    assert input_schema["properties"]["figure"]["properties"]["source_refs"]["minItems"] == 1
    output_schema = json.loads((REPO / "contracts/schemas/imagegen-host-bitmap.output.schema.json").read_text(encoding="utf-8"))
    assert len(output_schema["oneOf"]) == 3
    assert output_schema["$defs"]["authority_candidate"]["additionalProperties"] is False
    assert output_schema["$defs"]["quality_debt"]["additionalProperties"] is False
    assert output_schema["$defs"]["asset"]["properties"]["bytes"]["maximum"] == helper.MAX_BITMAP_BYTES
    handoff = json.loads((REPO / "contracts/image_asset_host_handoff.json").read_text(encoding="utf-8"))
    assert handoff["state"] == "domain_handler_registered"
    assert handoff["host_binding_status"] == "bound_to_domain_handler_registry_v1"
    assert handoff["domain_handler"]["maximum_bitmap_bytes"] == helper.MAX_BITMAP_BYTES
    assert handoff["domain_handler"]["maximum_png_decompressed_bytes"] == helper.MAX_PNG_DECOMPRESSED_BYTES
    assert handoff["domain_handler"]["handler_ref"] == f"handler:{handler['handler_id']}"
    assert handoff["domain_handler"]["registry_entry_ref"] == "contracts/domain_handler_registry.json#/handlers/0"
    assert {action["action_id"] for action in action_catalog["actions"]} == {"shape-storyline", "materialize-book"}
    assert all("handler_id" not in action and "handler_ref" not in action for action in action_catalog["actions"])

    assert helper.image_info(jpeg_bytes(), Path("figure.jpg"))["width"] == 19
    assert helper.image_info(webp_bytes(), Path("figure.webp"))["height"] == 17
    original_png_limit = helper.MAX_PNG_DECOMPRESSED_BYTES
    helper.MAX_PNG_DECOMPRESSED_BYTES = 128
    try:
        helper.image_info(png_bytes(width=16, height=12), Path("bounded.png"))
    except helper.AssetValidationError as error:
        assert error.code == "bitmap_decoded_size_exceeded", error.code
    else:
        raise AssertionError("PNG decompression limit did not reject expanded payload")
    finally:
        helper.MAX_PNG_DECOMPRESSED_BYTES = original_png_limit

    with tempfile.TemporaryDirectory(prefix="bookforge-host-asset-test-") as tmp:
        root = Path(tmp)
        asset = root / "artifacts/figures/figure-1.png"
        asset.parent.mkdir(parents=True)
        data = png_bytes()
        asset.write_bytes(data)

        before = {path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()}
        payload = helper.evaluate_host_bitmap(request(root, "artifacts/figures/figure-1.png", data))
        after = {path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()}
        assert after == before, "authority callable mutated workspace bytes"
        assert payload["status"] == "figure_authority_receipt_candidate", payload
        candidate = payload["figure_authority_receipt_candidate"]
        assert candidate["receipt_kind"] == "bookforge_figure_authority_receipt_candidate.v1", candidate
        assert candidate["candidate_only"] is True, candidate
        assert candidate["asset"]["width"] == 16, candidate
        assert candidate["asset"]["height"] == 12, candidate
        assert candidate["asset_manifest_entry_candidate"]["asset_status"] == "bitmap_validated_pending_visual_review", candidate
        assert candidate["authority_boundary"]["visual_review_still_required"] is True, candidate
        assert candidate["authority_boundary"]["authorizes_publication_proof"] is False, candidate

        mismatch = request(root, "artifacts/figures/figure-1.png", data)
        mismatch["bitmap"]["sha256"] = "sha256:" + "0" * 64
        debt = helper.evaluate_host_bitmap(mismatch)
        assert debt["status"] == "completed_with_quality_debt", debt
        assert debt["quality_debt"]["code"] == "bitmap_sha256_mismatch", debt
        assert debt["quality_debt"]["blocks_stage_transition"] is False, debt
        assert debt["quality_debt"]["blocks_figure_ready_or_export_claims"] is True, debt

        escaped = helper.evaluate_host_bitmap(request(root, "../outside.png", data))
        assert escaped["quality_debt"]["code"] == "bitmap_ref_not_contained", escaped

        non_normalized = helper.evaluate_host_bitmap(request(root, "artifacts//figures/figure-1.png", data))
        assert non_normalized["quality_debt"]["code"] == "bitmap_ref_not_contained", non_normalized

        link = root / "artifacts/figures/linked.png"
        link.symlink_to(asset)
        symlinked = helper.evaluate_host_bitmap(request(root, "artifacts/figures/linked.png", data))
        assert symlinked["quality_debt"]["code"] == "bitmap_ref_symlink", symlinked

        bad_extension = root / "artifacts/figures/wrong.webp"
        bad_extension.write_bytes(data)
        extension_request = request(root, "artifacts/figures/wrong.webp", data)
        extension_request["bitmap"].pop("format")
        extension_request["bitmap"].pop("media_type")
        wrong = helper.evaluate_host_bitmap(extension_request)
        assert wrong["quality_debt"]["code"] == "bitmap_extension_mismatch", wrong

        oversized = root / "artifacts/figures/oversized.png"
        with oversized.open("wb") as stream:
            stream.truncate(helper.MAX_BITMAP_BYTES + 1)
        oversized_result = helper.evaluate_host_bitmap(
            request(root, "artifacts/figures/oversized.png", b"not-read")
        )
        assert oversized_result["quality_debt"]["code"] == "bitmap_too_large", oversized_result

        request_file = root / "host-request.json"
        request_file.write_text(json.dumps(request(root, "artifacts/figures/figure-1.png", data)), encoding="utf-8")
        cli = subprocess.run(
            [sys.executable, str(MODULE_PATH), "--request-file", str(request_file)],
            text=True,
            capture_output=True,
            check=False,
        )
        assert cli.returncode == 0, cli.stderr or cli.stdout
        assert json.loads(cli.stdout)["status"] == "figure_authority_receipt_candidate", cli.stdout

    invalid = helper.evaluate_host_bitmap({})
    assert invalid["status"] == "invalid_host_input", invalid
    invalid_document = helper.evaluate_host_bitmap([])
    assert invalid_document["status"] == "invalid_host_input", invalid_document
    invalid_format = request(Path("/tmp"), "figure.bmp", b"bitmap")
    invalid_format["bitmap"]["format"] = "bmp"
    assert helper.evaluate_host_bitmap(invalid_format)["status"] == "invalid_host_input"
    self_test = subprocess.run(
        [sys.executable, str(MODULE_PATH), "--self-test"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert self_test.returncode == 0, self_test.stderr or self_test.stdout
    assert json.loads(self_test.stdout)["writes_files"] is False

    print(json.dumps({"status": "passed", "surface": "bookforge_imagegen_host_asset_handler"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
