#!/usr/bin/env python3
"""Validate an OPL-hosted bitmap and return a Book Forge authority candidate."""

from __future__ import annotations

import argparse
import json
import sys
import zlib
from pathlib import Path
from typing import Any

from opl_framework.artifact_inspection import (
    ContainedFileReadError,
    read_contained_regular_file as framework_read_contained_regular_file,
    sha256_bytes,
)


VERSION = "bookforge-imagegen-asset.v3"
REQUEST_KIND = "opl_bookforge_host_bitmap_validation_request"
RESULT_KIND = "opl_bookforge_figure_asset_evaluation"
RECEIPT_KIND = "bookforge_figure_authority_receipt_candidate.v1"
MAX_BITMAP_BYTES = 64 * 1024 * 1024
MAX_PNG_DECOMPRESSED_BYTES = 256 * 1024 * 1024
PNG_DECOMPRESS_CHUNK_BYTES = 1024 * 1024
ALLOWED_FORMATS = {"png", "jpeg", "jpg", "webp"}
ALLOWED_MEDIA_TYPES = {"image/png", "image/jpeg", "image/webp"}


class RequestShapeError(ValueError):
    pass


class AssetValidationError(ValueError):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


def record(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise RequestShapeError(f"{field} must be an object")
    return value


def required_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RequestShapeError(f"{field} must be a non-empty string")
    return value.strip()


def optional_text(value: Any, field: str) -> str | None:
    if value is None:
        return None
    return required_text(value, field)


def reject_unknown_fields(value: dict[str, Any], allowed: set[str], field: str) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise RequestShapeError(f"{field} contains unsupported fields: {', '.join(unknown)}")


def normalize_sha256(value: Any, field: str) -> str:
    digest = required_text(value, field).lower()
    if digest.startswith("sha256:"):
        digest = digest[7:]
    if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
        raise RequestShapeError(f"{field} must be a SHA-256 digest")
    return f"sha256:{digest}"


def normalize_format(value: str) -> str:
    normalized = value.lower().lstrip(".")
    return "jpeg" if normalized == "jpg" else normalized


def validate_png_idat_stream(payloads: list[bytes]) -> None:
    decompressor = zlib.decompressobj()
    decoded_bytes = 0
    try:
        for payload in payloads:
            pending = payload
            while pending:
                remaining = MAX_PNG_DECOMPRESSED_BYTES - decoded_bytes
                if remaining <= 0:
                    raise AssetValidationError(
                        "bitmap_decoded_size_exceeded",
                        f"PNG decompressed payload exceeds {MAX_PNG_DECOMPRESSED_BYTES} bytes",
                    )
                chunk = decompressor.decompress(
                    pending,
                    min(PNG_DECOMPRESS_CHUNK_BYTES, remaining + 1),
                )
                decoded_bytes += len(chunk)
                if decoded_bytes > MAX_PNG_DECOMPRESSED_BYTES:
                    raise AssetValidationError(
                        "bitmap_decoded_size_exceeded",
                        f"PNG decompressed payload exceeds {MAX_PNG_DECOMPRESSED_BYTES} bytes",
                    )
                pending = decompressor.unconsumed_tail
        if not decompressor.eof or decompressor.unused_data:
            raise AssetValidationError("bitmap_structure_invalid", "PNG IDAT stream is incomplete or has trailing data")
    except zlib.error as error:
        raise AssetValidationError("bitmap_structure_invalid", f"PNG IDAT payload is invalid: {error}") from error


def png_info(data: bytes) -> tuple[int, int] | None:
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return None
    if len(data) < 33 or data[8:12] != b"\x00\x00\x00\x0d" or data[12:16] != b"IHDR":
        raise AssetValidationError("bitmap_structure_invalid", "PNG has no valid IHDR chunk")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    offset = 8
    idat_payloads: list[bytes] = []
    saw_idat = False
    saw_iend = False
    while offset + 12 <= len(data):
        chunk_size = int.from_bytes(data[offset:offset + 4], "big")
        chunk_end = offset + 12 + chunk_size
        if chunk_end > len(data):
            raise AssetValidationError("bitmap_structure_invalid", "PNG contains a truncated chunk")
        kind = data[offset + 4:offset + 8]
        payload = data[offset + 8:offset + 8 + chunk_size]
        expected_crc = int.from_bytes(data[offset + 8 + chunk_size:chunk_end], "big")
        observed_crc = zlib.crc32(kind + payload) & 0xFFFFFFFF
        if expected_crc != observed_crc:
            raise AssetValidationError("bitmap_structure_invalid", f"PNG {kind!r} chunk CRC mismatch")
        saw_idat = saw_idat or kind == b"IDAT"
        if kind == b"IDAT":
            idat_payloads.append(payload)
        saw_iend = saw_iend or kind == b"IEND"
        offset = chunk_end
        if saw_iend:
            break
    if not saw_idat or not saw_iend:
        raise AssetValidationError("bitmap_structure_invalid", "PNG must contain IDAT and IEND chunks")
    validate_png_idat_stream(idat_payloads)
    return width, height


def jpeg_info(data: bytes) -> tuple[int, int] | None:
    if not data.startswith(b"\xff\xd8"):
        return None
    offset = 2
    start_of_frame = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while offset < len(data):
        while offset < len(data) and data[offset] != 0xFF:
            offset += 1
        while offset < len(data) and data[offset] == 0xFF:
            offset += 1
        if offset >= len(data):
            break
        marker = data[offset]
        offset += 1
        if marker in {0x01, *range(0xD0, 0xD8)}:
            continue
        if marker in {0xD9, 0xDA}:
            break
        if offset + 2 > len(data):
            break
        segment_length = int.from_bytes(data[offset:offset + 2], "big")
        if segment_length < 2 or offset + segment_length > len(data):
            raise AssetValidationError("bitmap_structure_invalid", "JPEG contains a truncated segment")
        if marker in start_of_frame:
            if segment_length < 7:
                raise AssetValidationError("bitmap_structure_invalid", "JPEG SOF segment is too short")
            height = int.from_bytes(data[offset + 3:offset + 5], "big")
            width = int.from_bytes(data[offset + 5:offset + 7], "big")
            remainder = data[offset + segment_length:]
            if b"\xff\xda" not in remainder:
                raise AssetValidationError("bitmap_structure_invalid", "JPEG has no SOS marker")
            if b"\xff\xd9" not in remainder:
                raise AssetValidationError("bitmap_structure_invalid", "JPEG has no EOI marker")
            return width, height
        offset += segment_length
    raise AssetValidationError("bitmap_dimensions_missing", "JPEG has no supported SOF dimensions")


def webp_info(data: bytes) -> tuple[int, int] | None:
    if len(data) < 12 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    declared_size = int.from_bytes(data[4:8], "little") + 8
    if declared_size > len(data):
        raise AssetValidationError("bitmap_structure_invalid", "WebP RIFF payload is truncated")
    offset = 12
    while offset + 8 <= len(data):
        chunk_kind = data[offset:offset + 4]
        chunk_size = int.from_bytes(data[offset + 4:offset + 8], "little")
        payload_start = offset + 8
        payload_end = payload_start + chunk_size
        if payload_end > len(data):
            raise AssetValidationError("bitmap_structure_invalid", "WebP contains a truncated chunk")
        payload = data[payload_start:payload_end]
        if chunk_kind == b"VP8X" and len(payload) >= 10:
            width = 1 + int.from_bytes(payload[4:7], "little")
            height = 1 + int.from_bytes(payload[7:10], "little")
            return width, height
        if chunk_kind == b"VP8L" and len(payload) >= 5 and payload[0] == 0x2F:
            dimensions = int.from_bytes(payload[1:5], "little")
            return 1 + (dimensions & 0x3FFF), 1 + ((dimensions >> 14) & 0x3FFF)
        if chunk_kind == b"VP8 " and len(payload) >= 10 and payload[3:6] == b"\x9d\x01\x2a":
            width = int.from_bytes(payload[6:8], "little") & 0x3FFF
            height = int.from_bytes(payload[8:10], "little") & 0x3FFF
            return width, height
        offset = payload_end + (chunk_size % 2)
    raise AssetValidationError("bitmap_dimensions_missing", "WebP has no supported dimension chunk")


def image_info(data: bytes, path: Path) -> dict[str, Any]:
    if not data:
        raise AssetValidationError("bitmap_empty", "bitmap is empty")
    detected: tuple[str, str, tuple[int, int] | None] = (
        "png",
        "image/png",
        png_info(data),
    )
    if detected[2] is None:
        detected = ("jpeg", "image/jpeg", jpeg_info(data))
    if detected[2] is None:
        detected = ("webp", "image/webp", webp_info(data))
    if detected[2] is None:
        raise AssetValidationError("bitmap_format_unsupported", "asset is not PNG, JPEG, or WebP")
    kind, media_type, dimensions = detected
    if dimensions is None or dimensions[0] <= 0 or dimensions[1] <= 0:
        raise AssetValidationError("bitmap_dimensions_invalid", "bitmap dimensions must be positive")
    suffix = normalize_format(path.suffix)
    if suffix != kind:
        raise AssetValidationError(
            "bitmap_extension_mismatch",
            f"bitmap bytes are {kind} but the file extension is {path.suffix or '<none>'}",
        )
    return {
        "format": kind,
        "media_type": media_type,
        "width": dimensions[0],
        "height": dimensions[1],
        "bytes": len(data),
        "sha256": sha256_bytes(data),
    }


def read_contained_regular_file(root_value: str, ref_value: str) -> tuple[Path, Path, bytes]:
    try:
        return framework_read_contained_regular_file(
            root_value,
            ref_value,
            max_bytes=MAX_BITMAP_BYTES,
        )
    except ContainedFileReadError as error:
        code = {
            "root_not_absolute": "workspace_root_not_absolute",
            "root_unavailable": "workspace_root_unavailable",
            "root_not_directory": "workspace_root_not_directory",
            "ref_not_contained": "bitmap_ref_not_contained",
            "ref_symlink": "bitmap_ref_symlink",
            "ref_not_directory": "bitmap_ref_not_contained",
            "not_regular_file": "bitmap_not_regular_file",
            "file_too_large": "bitmap_too_large",
            "identity_changed": "bitmap_identity_changed",
        }.get(error.code, "bitmap_unavailable")
        raise AssetValidationError(code, error.detail) from error


def request_parts(request: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    reject_unknown_fields(
        request,
        {"surface_kind", "schema_version", "host_context", "bitmap", "figure"},
        "request",
    )
    if request.get("surface_kind") != REQUEST_KIND:
        raise RequestShapeError(f"surface_kind must be {REQUEST_KIND}")
    if request.get("schema_version") != 1:
        raise RequestShapeError("schema_version must be 1")
    host = record(request.get("host_context"), "host_context")
    bitmap = record(request.get("bitmap"), "bitmap")
    figure = record(request.get("figure"), "figure")
    reject_unknown_fields(host, {"workspace_root", "attempt_ref", "output_ref"}, "host_context")
    reject_unknown_fields(bitmap, {"bitmap_ref", "sha256", "format", "media_type"}, "bitmap")
    reject_unknown_fields(
        figure,
        {
            "figure_id",
            "title",
            "artifact_role",
            "prompt_sha256",
            "style_reference",
            "placement_ref",
            "caption_intent",
            "claim_boundary",
            "source_refs",
            "review_criteria",
            "minimum_width",
            "minimum_height",
        },
        "figure",
    )
    required_text(host.get("workspace_root"), "host_context.workspace_root")
    required_text(host.get("attempt_ref"), "host_context.attempt_ref")
    required_text(host.get("output_ref"), "host_context.output_ref")
    required_text(bitmap.get("bitmap_ref"), "bitmap.bitmap_ref")
    normalize_sha256(bitmap.get("sha256"), "bitmap.sha256")
    if bitmap.get("format") is not None:
        bitmap_format = required_text(bitmap["format"], "bitmap.format")
        if bitmap_format not in ALLOWED_FORMATS:
            raise RequestShapeError(f"bitmap.format must be one of: {', '.join(sorted(ALLOWED_FORMATS))}")
    if bitmap.get("media_type") is not None:
        media_type = required_text(bitmap["media_type"], "bitmap.media_type")
        if media_type not in ALLOWED_MEDIA_TYPES:
            raise RequestShapeError(f"bitmap.media_type must be one of: {', '.join(sorted(ALLOWED_MEDIA_TYPES))}")
    required_text(figure.get("figure_id"), "figure.figure_id")
    required_text(figure.get("title"), "figure.title")
    required_text(figure.get("artifact_role"), "figure.artifact_role")
    if figure.get("prompt_sha256") is not None:
        normalize_sha256(figure.get("prompt_sha256"), "figure.prompt_sha256")
    for field in ("style_reference", "placement_ref", "caption_intent", "claim_boundary"):
        if field in figure:
            optional_text(figure[field], f"figure.{field}")
    for field in ("source_refs", "review_criteria"):
        if field not in figure:
            continue
        values = figure[field]
        if not isinstance(values, list) or not values or any(not isinstance(item, str) or not item.strip() for item in values):
            raise RequestShapeError(f"figure.{field} must be a non-empty array of non-empty strings")
        if len(values) != len(set(values)):
            raise RequestShapeError(f"figure.{field} must not contain duplicates")
    for field in ("minimum_width", "minimum_height"):
        if field in figure and (not isinstance(figure[field], int) or isinstance(figure[field], bool) or figure[field] <= 0):
            raise RequestShapeError(f"figure.{field} must be a positive integer")
    return host, bitmap, figure


def authority_boundary() -> dict[str, bool]:
    return {
        "candidate_requires_opl_persistence": True,
        "visual_review_still_required": True,
        "authorizes_publication_proof": False,
        "authorizes_final_export": False,
        "counts_as_owner_acceptance": False,
        "counts_as_domain_ready": False,
        "counts_as_production_ready": False,
    }


def invalid_host_input(detail: str) -> dict[str, Any]:
    return {
        "surface_kind": RESULT_KIND,
        "schema_version": 1,
        "status": "invalid_host_input",
        "figure_authority_receipt_candidate": None,
        "quality_debt": None,
        "error": {"code": "host_input_schema_invalid", "detail": detail},
        "authority_boundary": authority_boundary(),
    }


def quality_debt(
    host: dict[str, Any],
    bitmap: dict[str, Any],
    figure: dict[str, Any],
    error: AssetValidationError,
) -> dict[str, Any]:
    return {
        "surface_kind": RESULT_KIND,
        "schema_version": 1,
        "status": "completed_with_quality_debt",
        "figure_id": figure["figure_id"],
        "host_refs": {
            "attempt_ref": host["attempt_ref"],
            "output_ref": host["output_ref"],
        },
        "figure_authority_receipt_candidate": None,
        "quality_debt": {
            "code": error.code,
            "detail": error.detail,
            "bitmap_ref": bitmap["bitmap_ref"],
            "blocks_stage_transition": False,
            "blocks_figure_ready_or_export_claims": True,
            "next_stage_may_start": True,
        },
        "error": None,
        "authority_boundary": authority_boundary(),
    }


def evaluate_host_bitmap(request: dict[str, Any]) -> dict[str, Any]:
    """Evaluate a host-injected bitmap ref without spawning or writing files."""
    if not isinstance(request, dict):
        return invalid_host_input("request document must be an object")
    try:
        host, bitmap, figure = request_parts(request)
    except RequestShapeError as error:
        return invalid_host_input(str(error))

    bitmap_ref = required_text(bitmap["bitmap_ref"], "bitmap.bitmap_ref")
    expected_sha256 = normalize_sha256(bitmap["sha256"], "bitmap.sha256")
    try:
        root, asset_path, data = read_contained_regular_file(host["workspace_root"], bitmap_ref)
        observed_sha256 = sha256_bytes(data)
        if observed_sha256 != expected_sha256:
            raise AssetValidationError(
                "bitmap_sha256_mismatch",
                f"expected {expected_sha256}, observed {observed_sha256}",
            )
        info = image_info(data, asset_path)
        expected_media_type = optional_text(bitmap.get("media_type"), "bitmap.media_type")
        if expected_media_type and expected_media_type != info["media_type"]:
            raise AssetValidationError(
                "bitmap_media_type_mismatch",
                f"expected {expected_media_type}, observed {info['media_type']}",
            )
        expected_format = optional_text(bitmap.get("format"), "bitmap.format")
        if expected_format and normalize_format(expected_format) != info["format"]:
            raise AssetValidationError(
                "bitmap_format_mismatch",
                f"expected {expected_format}, observed {info['format']}",
            )
        minimum_width = figure.get("minimum_width", 1)
        minimum_height = figure.get("minimum_height", 1)
        if info["width"] < minimum_width or info["height"] < minimum_height:
            raise AssetValidationError(
                "bitmap_dimensions_below_minimum",
                f"expected at least {minimum_width}x{minimum_height}, observed {info['width']}x{info['height']}",
            )
    except (AssetValidationError, OSError) as error:
        normalized = error if isinstance(error, AssetValidationError) else AssetValidationError("bitmap_unavailable", str(error))
        return quality_debt(host, bitmap, figure, normalized)

    prompt_sha256 = figure.get("prompt_sha256")
    candidate = {
        "receipt_kind": RECEIPT_KIND,
        "candidate_only": True,
        "owner": "OPL Book Forge",
        "figure_id": figure["figure_id"],
        "title": figure["title"],
        "artifact_role": figure["artifact_role"],
        "prompt_sha256": normalize_sha256(prompt_sha256, "figure.prompt_sha256") if prompt_sha256 else None,
        "asset": {
            "path": str(asset_path.relative_to(root)),
            **info,
        },
        "host_refs": {
            "attempt_ref": host["attempt_ref"],
            "output_ref": host["output_ref"],
        },
        "figure_metadata": {
            key: figure[key]
            for key in (
                "style_reference",
                "placement_ref",
                "caption_intent",
                "claim_boundary",
                "source_refs",
                "review_criteria",
            )
            if key in figure
        },
        "asset_manifest_entry_candidate": {
            "id": figure["figure_id"],
            "title": figure["title"],
            "artifact_role": figure["artifact_role"],
            "asset_status": "bitmap_validated_pending_visual_review",
            "project_local_path": str(asset_path.relative_to(root)),
            "asset": info,
            "source_attempt_ref": host["attempt_ref"],
            "source_output_ref": host["output_ref"],
        },
        "authority_boundary": authority_boundary(),
    }
    return {
        "surface_kind": RESULT_KIND,
        "schema_version": 1,
        "status": "figure_authority_receipt_candidate",
        "figure_id": figure["figure_id"],
        "host_refs": candidate["host_refs"],
        "figure_authority_receipt_candidate": candidate,
        "quality_debt": None,
        "error": None,
        "authority_boundary": authority_boundary(),
    }


def run_self_test() -> dict[str, Any]:
    def chunk(kind: bytes, payload: bytes) -> bytes:
        checksum = zlib.crc32(kind + payload) & 0xFFFFFFFF
        return len(payload).to_bytes(4, "big") + kind + payload + checksum.to_bytes(4, "big")

    header = (2).to_bytes(4, "big") + (3).to_bytes(4, "big") + b"\x08\x06\x00\x00\x00"
    rows = b"".join(b"\x00" + b"\x00\x00\x00\xff" * 2 for _ in range(3))
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b"")
    info = image_info(png, Path("self-test.png"))
    return {
        "surface_kind": "bookforge_imagegen_asset_self_test",
        "version": VERSION,
        "status": "passed" if info["width"] == 2 and info["height"] == 3 else "failed",
        "writes_files": False,
        "spawns_processes": False,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="Run an in-memory parser self-test.")
    parser.add_argument("--request-file", type=Path, help="Host-generated validation request JSON.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.self_test:
        payload = run_self_test()
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if payload["status"] == "passed" else 1
    if args.request_file is None:
        payload = invalid_host_input("--request-file is required")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 2
    try:
        request = json.loads(args.request_file.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        payload = invalid_host_input(str(error))
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 2
    if not isinstance(request, dict):
        payload = invalid_host_input("request document must be an object")
    else:
        payload = evaluate_host_bitmap(request)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 2 if payload["status"] == "invalid_host_input" else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
