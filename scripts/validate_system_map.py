#!/usr/bin/env python3
"""Validate private local system-map repository and entrypoint claims."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


REPO_SECTION = re.compile(
    r"(?ms)^###\s+([^\r\n—]+?)(?:\s+—[^\r\n]*)?\r?\n(.*?)(?=^###\s|^##\s|\Z)"
)
FIELD = re.compile(r"(?m)^-\s+([^:]+):\s*(.*)$")
HEADING_PLACEHOLDER = re.compile(r"^###\s+<[^>]+>", re.IGNORECASE)
FIELD_PLACEHOLDER = re.compile(r"^-\s+[^:]+:\s*<[^>]+>\s*$", re.IGNORECASE)
LIST_PLACEHOLDER = re.compile(r"^-\s+<[^>]+>", re.IGNORECASE)
TABLE_PLACEHOLDER = re.compile(r"\|\s*<[^>]+>\s*\|", re.IGNORECASE)


def clean_value(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return value


def resolve_local_path(value: str) -> Path:
    expanded = os.path.expandvars(os.path.expanduser(clean_value(value)))
    return Path(expanded).resolve()


def contains_template_placeholder(text: str) -> bool:
    for line in text.splitlines():
        stripped = line.strip()
        if "TBD" in stripped.upper():
            return True
        if any(
            pattern.search(stripped)
            for pattern in (
                HEADING_PLACEHOLDER,
                FIELD_PLACEHOLDER,
                LIST_PLACEHOLDER,
                TABLE_PLACEHOLDER,
            )
        ):
            return True
    return False


def git_root(path: Path) -> Path | None:
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip()).resolve()


def validate(map_path: Path, if_present: bool = False) -> list[str]:
    if not map_path.exists():
        if if_present:
            print(f"system-map: {map_path} not found; skipped")
            return []
        return [f"map does not exist: {map_path}"]

    text = map_path.read_text(encoding="utf-8")
    if contains_template_placeholder(text):
        return ["system map contains a placeholder"]

    sections = list(REPO_SECTION.finditer(text))
    if not sections:
        return ["system map has no repository sections"]

    errors: list[str] = []
    for section in sections:
        name = section.group(1).strip()
        fields = {key.strip().lower(): value.strip() for key, value in FIELD.findall(section.group(2))}
        local_value = fields.get("local path")
        if not local_value:
            errors.append(f"{name}: missing Local path")
            continue
        repo_path = resolve_local_path(local_value)
        if not repo_path.exists():
            errors.append(f"{name}: repository path does not exist: {repo_path}")
            continue
        if not repo_path.is_dir():
            errors.append(f"{name}: repository path is not a directory: {repo_path}")
            continue
        actual_root = git_root(repo_path)
        if actual_root is None or actual_root != repo_path:
            errors.append(f"{name}: Local path is not a Git repository root: {repo_path}")
            continue

        entry_value = fields.get("entry points", "")
        if not entry_value:
            errors.append(f"{name}: missing Entry points; use none when intentionally empty")
            continue
        if entry_value.strip().lower() in {"none", "n/a"}:
            continue
        entries = re.findall(r"`([^`]+)`", entry_value)
        if not entries:
            errors.append(f"{name}: Entry points must be backticked paths or none")
            continue
        for entry in entries:
            relative_entry = Path(entry.replace("/", os.sep))
            if relative_entry.is_absolute() or ".." in relative_entry.parts:
                errors.append(f"{name}: entry point must stay inside the repository: {entry}")
                continue
            entry_path = (repo_path / relative_entry).resolve()
            try:
                entry_path.relative_to(repo_path)
            except ValueError:
                errors.append(f"{name}: entry point must stay inside the repository: {entry}")
                continue
            if not entry_path.exists():
                errors.append(f"{name}: entry point does not exist: {entry}")

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", dest="map_path", type=Path, required=True)
    parser.add_argument("--if-present", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate(args.map_path, args.if_present)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    if args.map_path.exists():
        print("system-map: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
