#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import tempfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO / "runtime/native_helpers/bookforge_imagegen_asset.py"


def load_helper():
    spec = importlib.util.spec_from_file_location("bookforge_imagegen_asset", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def helper_args(opl_bin: str) -> argparse.Namespace:
    return argparse.Namespace(
        artifact_role="book_manuscript_figure",
        figure_id="figure-1",
        title="Figure 1",
        style_reference="",
        size="1536x1024",
        quality="high",
        timeout=120,
        model="",
        reasoning_effort="",
        opl_bin=opl_bin,
    )


def write_fake_opl(path: Path) -> None:
    path.write_text(
        """#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

request_path = Path(sys.argv[sys.argv.index('--request') + 1])
request = json.loads(request_path.read_text(encoding='utf-8'))
Path(os.environ['FAKE_OPL_CAPTURE']).write_text(json.dumps(request), encoding='utf-8')
mode = os.environ.get('FAKE_OPL_MODE', 'success')
activated = [] if mode == 'missing-capability' else ['image_generation']
if mode == 'success':
    output = Path(request['cwd']) / request['domain_payload']['output_ref']
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(b'\\x89PNG\\r\\n\\x1a\\n' + b'\\x00' * 8 + (4).to_bytes(4, 'big') + (3).to_bytes(4, 'big'))
print(json.dumps({
    'version': 'g2',
    'agent_execution_receipt': {
        'surface_kind': 'opl_agent_execution_receipt',
        'executor_kind': 'codex_cli',
        'session_id': 'fake-session',
        'exit_code': 0,
        'requested_capabilities': ['image_generation'],
        'activated_capabilities': activated,
    },
}))
""",
        encoding="utf-8",
    )
    path.chmod(0o755)


def main() -> int:
    helper = load_helper()
    source = MODULE_PATH.read_text(encoding="utf-8")
    for forbidden in (
        "parse_codex_command",
        "build_codex_args",
        "parse_jsonl",
        "generated_images_dir",
        "recent_generated_images",
        "codex exec",
        "--enable",
    ):
        assert forbidden not in source, forbidden

    with tempfile.TemporaryDirectory(prefix="bookforge-opl-adapter-test-") as tmp:
        root = Path(tmp)
        fake_opl = root / "fake-opl"
        capture = root / "captured-request.json"
        output = root / "artifacts/figures/figure-1.png"
        write_fake_opl(fake_opl)
        os.environ["FAKE_OPL_CAPTURE"] = str(capture)
        os.environ.pop("FAKE_OPL_MODE", None)

        payload = helper.generate_live(
            helper_args(str(fake_opl)),
            root,
            output,
            "A book-specific explanatory figure.",
        )
        request = json.loads(capture.read_text(encoding="utf-8"))
        assert request["executor_kind"] == "codex_cli", request
        assert request["required_capabilities"] == ["image_generation"], request
        assert request["timeout_ms"] == 120000, request
        assert request["domain_payload"]["output_ref"] == "artifacts/figures/figure-1.png", request
        assert payload["status"] == "asset_ready", payload
        assert payload["asset"]["sha256"], payload
        assert payload["generation_runtime"]["requested_capabilities"] == ["image_generation"], payload
        assert payload["generation_runtime"]["activated_capabilities"] == ["image_generation"], payload

        output.unlink()
        os.environ["FAKE_OPL_MODE"] = "missing-capability"
        blocked = helper.generate_live(
            helper_args(str(fake_opl)),
            root,
            output,
            "A second book-specific explanatory figure.",
        )
        assert blocked["status"] == "blocked_opl_capability_not_activated", blocked
        assert blocked["blocker_kind"] == "opl_executor_image_generation_capability_not_activated", blocked
        assert not output.exists(), output

    print(json.dumps({"status": "passed", "surface": "bookforge_imagegen_opl_executor_adapter"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
