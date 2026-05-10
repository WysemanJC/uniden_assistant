#!/usr/bin/env python3
"""Roundtrip test for favourites import/export against SAMPLE_DATA/INPUT_FILES."""

from __future__ import annotations

import argparse
import difflib
import io
import json
import sys
import uuid
import zipfile
from pathlib import Path, PurePosixPath
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = "http://localhost:8001/api/uniden_manager/favourites"
DEFAULT_INPUT_ROOT = Path(__file__).resolve().parents[2] / "SAMPLE_DATA" / "INPUT_FILES"


def print_header(title: str) -> None:
    print(f"\n{'=' * 88}")
    print(title)
    print(f"{'=' * 88}")


def parse_json_bytes(raw: bytes) -> dict:
    try:
        return json.loads(raw.decode("utf-8", errors="replace"))
    except Exception:
        return {"raw": raw.decode("utf-8", errors="replace")}


def http_json_post(url: str, payload: dict | None = None, timeout: int = 120) -> tuple[int, dict]:
    data = json.dumps(payload or {}).encode("utf-8")
    req = Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        with urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            return resp.status, parse_json_bytes(body)
    except HTTPError as exc:
        body = exc.read()
        return exc.code, parse_json_bytes(body)
    except URLError as exc:
        return 0, {"error": str(exc)}


def build_multipart_body(files: list[Path], field_name: str = "files") -> tuple[bytes, str]:
    boundary = f"----UnidenBoundary{uuid.uuid4().hex}"
    boundary_bytes = boundary.encode("ascii")
    body = bytearray()

    for file_path in files:
        file_name = file_path.name
        content = file_path.read_bytes()
        body.extend(b"--" + boundary_bytes + b"\r\n")
        body.extend(
            f'Content-Disposition: form-data; name="{field_name}"; filename="{file_name}"\r\n'.encode(
                "utf-8"
            )
        )
        body.extend(b"Content-Type: application/octet-stream\r\n\r\n")
        body.extend(content)
        body.extend(b"\r\n")

    body.extend(b"--" + boundary_bytes + b"--\r\n")
    return bytes(body), boundary


def http_multipart_post(url: str, files: list[Path], timeout: int = 600) -> tuple[int, dict]:
    payload, boundary = build_multipart_body(files)
    req = Request(url, data=payload, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

    try:
        with urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            return resp.status, parse_json_bytes(body)
    except HTTPError as exc:
        body = exc.read()
        return exc.code, parse_json_bytes(body)
    except URLError as exc:
        return 0, {"error": str(exc)}


def http_get_bytes(url: str, timeout: int = 600) -> tuple[int, bytes | None, dict | None]:
    req = Request(url, method="GET")
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read(), None
    except HTTPError as exc:
        body = exc.read()
        return exc.code, None, parse_json_bytes(body)
    except URLError as exc:
        return 0, None, {"error": str(exc)}


def first_diff_offset(left: bytes, right: bytes) -> int:
    limit = min(len(left), len(right))
    for idx in range(limit):
        if left[idx] != right[idx]:
            return idx
    return limit


def unified_text_diff(expected: bytes, actual: bytes, name: str, max_lines: int = 120) -> list[str]:
    expected_text = expected.decode("latin-1")
    actual_text = actual.decode("latin-1")
    diff = list(
        difflib.unified_diff(
            expected_text.splitlines(keepends=True),
            actual_text.splitlines(keepends=True),
            fromfile=f"expected/{name}",
            tofile=f"actual/{name}",
            n=3,
            lineterm="",
        )
    )
    if len(diff) > max_lines:
        return diff[:max_lines] + [f"\n... diff truncated after {max_lines} lines ...\n"]
    return diff


def load_expected_files(input_folder: Path) -> dict[str, bytes]:
    favorites_dir = input_folder / "favorites_lists"
    if not favorites_dir.is_dir():
        raise FileNotFoundError(f"Missing favorites_lists directory in {input_folder}")

    expected = {}
    for path in sorted(p for p in favorites_dir.iterdir() if p.is_file()):
        expected[path.name] = path.read_bytes()
    return expected


def load_actual_files_from_zip(zip_bytes: bytes) -> dict[str, bytes]:
    actual = {}
    with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as archive:
        for member in archive.namelist():
            normalized = PurePosixPath(member)
            if normalized.is_absolute() or ".." in normalized.parts:
                continue
            if len(normalized.parts) != 2 or normalized.parts[0] != "favorites_lists":
                continue
            if member.endswith("/"):
                continue
            actual[normalized.parts[1]] = archive.read(member)
    return actual


def compare_maps(expected: dict[str, bytes], actual: dict[str, bytes]) -> list[str]:
    discrepancies: list[str] = []
    expected_names = set(expected.keys())
    actual_names = set(actual.keys())

    missing = sorted(expected_names - actual_names)
    extra = sorted(actual_names - expected_names)

    for name in missing:
        discrepancies.append(f"Missing exported file: {name}")
    for name in extra:
        discrepancies.append(f"Unexpected exported file: {name}")

    for name in sorted(expected_names & actual_names):
        expected_bytes = expected[name]
        actual_bytes = actual[name]
        if expected_bytes == actual_bytes:
            continue

        offset = first_diff_offset(expected_bytes, actual_bytes)
        discrepancies.append(
            f"Byte mismatch in {name}: expected {len(expected_bytes)} bytes, "
            f"actual {len(actual_bytes)} bytes, first difference at byte {offset}"
        )
        discrepancies.extend(unified_text_diff(expected_bytes, actual_bytes, name))

    return discrepancies


def run_folder_roundtrip(base_url: str, input_folder: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []

    clear_url = f"{base_url}/clear-data/"
    import_url = f"{base_url}/import-files/"
    export_url = f"{base_url}/export-favorites/"

    status, clear_payload = http_json_post(clear_url, {})
    if status != 200:
        errors.append(f"clear-data failed ({status}): {clear_payload}")
        return False, errors

    favorites_dir = input_folder / "favorites_lists"
    files_to_upload = sorted(p for p in favorites_dir.iterdir() if p.is_file())
    if not files_to_upload:
        errors.append(f"No files found in {favorites_dir}")
        return False, errors

    status, import_payload = http_multipart_post(import_url, files_to_upload)
    if status != 200:
        errors.append(f"import-files failed ({status}): {import_payload}")
        return False, errors

    import_errors = import_payload.get("errors") if isinstance(import_payload, dict) else None
    if import_errors:
        errors.append(f"import-files returned per-file errors: {import_errors}")
        return False, errors

    status, zip_bytes, export_error = http_get_bytes(export_url)
    if status != 200 or zip_bytes is None:
        errors.append(f"export-favorites failed ({status}): {export_error}")
        return False, errors

    expected_files = load_expected_files(input_folder)
    actual_files = load_actual_files_from_zip(zip_bytes)
    discrepancies = compare_maps(expected_files, actual_files)
    return len(discrepancies) == 0, discrepancies


def list_target_folders(input_root: Path, selected: list[str] | None = None) -> list[Path]:
    folders = sorted(p for p in input_root.iterdir() if p.is_dir())
    if not selected:
        return folders

    selected_set = {name.strip() for name in selected}
    return [p for p in folders if p.name in selected_set]


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Import each folder in SAMPLE_DATA/INPUT_FILES, export favourites, "
            "and compare output with exact byte-for-byte matching."
        )
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="Base API URL for favourites endpoints",
    )
    parser.add_argument(
        "--input-root",
        default=str(DEFAULT_INPUT_ROOT),
        help="Root folder containing per-region sample directories",
    )
    parser.add_argument(
        "--folders",
        nargs="*",
        help="Optional folder names to test (e.g. NSW VIC OZ)",
    )
    args = parser.parse_args()

    input_root = Path(args.input_root).resolve()
    if not input_root.is_dir():
        print(f"ERROR: input root does not exist: {input_root}")
        return 2

    folders = list_target_folders(input_root, args.folders)
    if not folders:
        print("ERROR: no matching input folders found to test")
        return 2

    print_header("Favourites Roundtrip Validation")
    print(f"API base URL : {args.base_url}")
    print(f"Input root   : {input_root}")
    print(f"Folders      : {', '.join(p.name for p in folders)}")

    failed = False
    for folder in folders:
        print_header(f"Testing folder: {folder.name}")
        ok, discrepancies = run_folder_roundtrip(args.base_url, folder)
        if ok:
            print(f"PASS: {folder.name} exported output is a 100% byte-for-byte match")
            continue

        failed = True
        print(f"FAIL: {folder.name} mismatches detected")
        for item in discrepancies:
            sys.stdout.write(item)
            if not item.endswith("\n"):
                sys.stdout.write("\n")

    print_header("Result")
    if failed:
        print("Roundtrip validation FAILED")
        return 1

    print("Roundtrip validation PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())