#!/usr/bin/env python3
"""Validate an Agent-produced one-line Python file; optionally fix only line endings.

Designed for a disposable, explicitly selected workspace. No third-party packages.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import sys
from pathlib import Path


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Existing isolated workspace")
    parser.add_argument("--file", required=True, help="File to verify inside --root")
    expected_args = parser.add_mutually_exclusive_group(required=True)
    expected_args.add_argument("--expected-line", help="One exact Python source line")
    expected_args.add_argument("--expected-print", help="Exact one-line print output; avoids Windows command quoting issues")
    parser.add_argument(
        "--normalize-newline",
        action="store_true",
        help="Repair BOM/final newline only if existing code body exactly matches",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve(strict=True)
    target = Path(args.file).expanduser().resolve(strict=True)
    if not root.is_dir() or not target.is_file() or target.suffix.lower() != ".py":
        parser.error("root must be a directory and file must be an existing .py file")
    if target != root and root not in target.parents:
        parser.error("refusing to access a file outside the isolated root")
    expected_line = (
        "print(" + json.dumps(args.expected_print, ensure_ascii=False) + ")"
        if args.expected_print is not None else args.expected_line
    )
    if "\r" in expected_line or "\n" in expected_line:
        parser.error("expected source must contain exactly one line")
    try:
        ast.parse(expected_line + "\n")
    except SyntaxError as exc:
        parser.error(f"expected Python line is invalid: {exc}")

    expected = (expected_line + "\n").encode("utf-8")
    actual = target.read_bytes()
    was_exact = actual == expected
    before_sha = sha256(actual)
    repaired = False
    failure = None

    if not was_exact and args.normalize_newline:
        try:
            decoded = actual.decode("utf-8-sig")
        except UnicodeDecodeError:
            failure = "not valid UTF-8"
        else:
            if decoded.rstrip("\r\n") != expected_line:
                failure = "source code differs; refusing to overwrite content"
            else:
                target.write_bytes(expected)
                repaired = True

    after = target.read_bytes()
    result = {
        "file": str(target),
        "before_exact": was_exact,
        "before_size": len(actual),
        "before_sha256": before_sha,
        "repaired_newline_only": repaired,
        "after_exact": after == expected,
        "after_size": len(after),
        "after_sha256": sha256(after),
        "expected_size": len(expected),
        "error": failure,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["after_exact"] else 1


if __name__ == "__main__":
    sys.exit(main())
