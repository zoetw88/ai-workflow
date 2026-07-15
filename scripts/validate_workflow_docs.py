#!/usr/bin/env python3
"""Validate living workflow documents without claiming semantic correctness."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


SPEC_PATH = re.compile(r"^\.spec/(.+)/(current|tasks)\.md$", re.IGNORECASE)
CHECKBOX = re.compile(r"(?m)^\s*- \[([ xX])\]")
TASK_CHECKBOX = re.compile(r"(?mi)^\s*-\s+\[[ x]\]\s+task-\d+\s*:")
PLACEHOLDER = re.compile(r"<\s*(?:TBD|TODO|\.\.\.)\s*>|\bTBD\b", re.IGNORECASE)
REQUIRED_CURRENT_HEADINGS = ("## Goal", "## Acceptance criteria")
REQUIRED_TASK_HEADINGS = ("# Tasks", "## Acceptance")
QUALITY_FIELDS = ("Observable:", "Environment:", "Verify:")


@dataclass
class Finding:
    path: str
    message: str


@dataclass
class Report:
    errors: list[Finding] = field(default_factory=list)
    warnings: list[Finding] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def normalize(path: str) -> str:
    normalized = path.replace("\\", "/")
    return normalized[2:] if normalized.startswith("./") else normalized


def is_document(path: str) -> bool:
    return normalize(path).lower().endswith(".md")


def is_living_document(path: str) -> bool:
    normalized = normalize(path)
    return bool(SPEC_PATH.match(normalized)) or normalized.lower() in {
        "devlog.md",
        "todo.md",
    }


def ticket_docs(changed_files: list[str]) -> tuple[set[str], set[str]]:
    current: set[str] = set()
    tasks: set[str] = set()
    for changed_file in changed_files:
        match = SPEC_PATH.match(normalize(changed_file))
        if not match:
            continue
        ticket, kind = match.groups()
        (current if kind.lower() == "current" else tasks).add(ticket)
    return current, tasks


def is_personal_project(root: Path) -> bool:
    agents = root / "AGENTS.md"
    if not agents.exists():
        return False
    return bool(
        re.search(
            r"Project type:\s*personal",
            agents.read_text(encoding="utf-8"),
            re.IGNORECASE,
        )
    )


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ims)^{re.escape(heading)}\s*$\n(.*?)(?=^##\s|\Z)",
        text,
    )
    return match.group(1) if match else ""


def has_heading(text: str, heading: str) -> bool:
    return bool(re.search(rf"(?mi)^{re.escape(heading)}\s*$", text))


def without_fenced_code(text: str) -> str:
    outside: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if re.match(r"^\s*(?:```|~~~)", line):
            in_fence = not in_fence
            continue
        if not in_fence:
            outside.append(line)
    prose = "\n".join(outside)
    return re.sub(r"<!--.*?-->", "", prose, flags=re.DOTALL)


def contains_living_placeholder(text: str) -> bool:
    prose = without_fenced_code(text)
    if PLACEHOLDER.search(prose):
        return True
    angle = r"<[^>\r\n]+>"
    field_names = r"(?:Observable|Environment|Verify|Files|Test / validation)"
    patterns = (
        r"^TODO(?:\s*:.*)?$",
        rf"^#{{1,6}}\s+{angle}\s*$",
        rf"^{angle}\s*$",
        rf"^-\s+{angle}(?:\s+→.*)?$",
        rf"^-\s+(?:\[[ xX]\]\s+)?{field_names}:\s*{angle}\s*$",
        rf"^-\s+(?:\[[ xX]\]\s+)?(?:{field_names}|task-\d+):\s*TODO(?:\s*:.*)?$",
        r"^-\s+\[[ xX]\]\s+TODO(?:\s*:.*)?$",
        rf"^-\s+\[[ xX]\]\s+task-\d+\s*:\s*(?:{angle}|\.\.\.)\s*$",
        r"^-\s*\.\.\.\s*$",
    )
    return any(
        re.match(pattern, line.strip(), re.IGNORECASE)
        for line in prose.splitlines()
        for pattern in patterns
    )


def acceptance_blocks(text: str) -> list[str]:
    body = section(text, "## Acceptance criteria")
    starts = list(re.finditer(r"(?m)^\s*- \[[ xX]\]\s+", body))
    blocks: list[str] = []
    for index, start in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(body)
        blocks.append(body[start.start() : end])
    return blocks


def validate_file_structure(report: Report, path: Path, relative: str, kind: str, mode: str) -> None:
    if not path.exists():
        report.errors.append(Finding(relative, f"required {kind}.md does not exist"))
        return

    text = path.read_text(encoding="utf-8")
    prose = without_fenced_code(text)
    headings = REQUIRED_CURRENT_HEADINGS if kind == "current" else REQUIRED_TASK_HEADINGS
    for heading in headings:
        if not has_heading(prose, heading):
            report.errors.append(Finding(relative, f"missing required heading: {heading}"))

    if contains_living_placeholder(text):
        report.errors.append(Finding(relative, "living document contains a placeholder"))

    if mode == "ship":
        unchecked = sum(1 for state in CHECKBOX.findall(prose) if state == " ")
        if unchecked:
            report.errors.append(
                Finding(relative, f"Ship mode found {unchecked} unchecked checklist item(s)")
            )

    if kind == "current":
        blocks = acceptance_blocks(prose)
        if not blocks:
            report.errors.append(
                Finding(relative, "Acceptance criteria requires at least one checklist item")
            )
        for index, block in enumerate(blocks, start=1):
            missing = [field for field in QUALITY_FIELDS if field.lower() not in block.lower()]
            if missing:
                report.warnings.append(
                    Finding(
                        relative,
                        "acceptance criterion "
                        f"{index} is weak; add observable result, environment, and verify "
                        f"command/manual step (missing: {', '.join(missing)})",
                    )
                )
    else:
        acceptance_heading = re.search(r"(?mi)^## Acceptance\s*$", prose)
        task_body = prose[: acceptance_heading.start()] if acceptance_heading else prose
        if not TASK_CHECKBOX.search(task_body):
            report.errors.append(Finding(relative, "Tasks requires at least one task checklist item"))
        acceptance = section(prose, "## Acceptance")
        if not CHECKBOX.search(acceptance):
            report.errors.append(
                Finding(relative, "Tasks requires at least one Acceptance checklist item")
            )


def validate_workflow_documents(
    root: Path,
    changed_files: list[str],
    mode: str,
    project_type: str = "auto",
) -> Report:
    root = Path(root).resolve()
    changed = [normalize(path) for path in changed_files]
    report = Report()
    current_tickets, task_tickets = ticket_docs(changed)
    touched_tickets = current_tickets | task_tickets
    code_changed = any(not is_document(path) for path in changed)
    substantive_changed = any(not is_living_document(path) for path in changed)

    requires_ticket = code_changed if mode == "wip" else substantive_changed
    if requires_ticket and not touched_tickets:
        report.errors.append(
            Finding(
                ".spec/",
                "substantive change without a ticket living document; update "
                ".spec/<ticket>/{current.md,tasks.md}",
            )
        )
        return report

    if mode == "ship" and substantive_changed:
        if not current_tickets or current_tickets != task_tickets:
            report.errors.append(
                Finding(
                    ".spec/",
                    "Ship mode requires changed current.md and tasks.md from the same ticket",
                )
            )
        personal_project = project_type == "personal" or (
            project_type == "auto" and is_personal_project(root)
        )
        if personal_project:
            for required in ("devlog.md", "todo.md"):
                if required not in {path.lower() for path in changed}:
                    report.errors.append(
                        Finding(required, f"Ship mode requires changed {required} for a personal project")
                    )

    for ticket in sorted(touched_tickets):
        spec_root = root / ".spec" / Path(ticket)
        validate_file_structure(
            report,
            spec_root / "current.md",
            f".spec/{ticket}/current.md",
            "current",
            mode,
        )
        validate_file_structure(
            report,
            spec_root / "tasks.md",
            f".spec/{ticket}/tasks.md",
            "tasks",
            mode,
        )

    return report


def changed_from_git(root: Path, base: str, head: str) -> list[str] | None:
    result = subprocess.run(
        ["git", "-C", str(root), "diff", "--name-only", f"{base}...{head}"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        return None
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def emit_report(report: Report) -> None:
    for finding in report.warnings:
        if os.environ.get("GITHUB_ACTIONS", "").lower() == "true":
            path = finding.path.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
            path = path.replace(":", "%3A").replace(",", "%2C")
            message = finding.message.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
            print(f"::warning file={path}::{message}")
        else:
            print(f"WARNING: {finding.path}: {finding.message}")
    for finding in report.errors:
        print(f"ERROR: {finding.path}: {finding.message}", file=sys.stderr)
    if report.ok:
        print(f"workflow-docs: pass with {len(report.warnings)} warning(s)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--mode", choices=("wip", "ship"), default="wip")
    parser.add_argument(
        "--project-type",
        choices=("auto", "personal", "team"),
        default="auto",
        help="Pin project policy so a pull request cannot weaken its own checks.",
    )
    parser.add_argument("--changed-file", action="append", default=[])
    parser.add_argument("--base")
    parser.add_argument("--head")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    changed_files = args.changed_file
    if not changed_files:
        if not args.base or not args.head:
            sys.stderr.write("workflow-docs: provide --changed-file or both --base and --head\n")
            return 2
        changed_files = changed_from_git(args.root, args.base, args.head)
        if changed_files is None:
            return 2

    report = validate_workflow_documents(
        args.root,
        changed_files,
        args.mode,
        project_type=args.project_type,
    )
    emit_report(report)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
