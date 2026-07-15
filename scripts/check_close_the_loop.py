#!/usr/bin/env python3
"""Pre-push guard: refuse to push code without the living-tier docs.

Enforces workflow.md's close-the-loop rule mechanically: if the commits being
pushed change code but touch neither `.spec/**` nor `devlog.md` / `todo.md`,
the push is rejected with a reminder.

Scope rules:
- Only enforces in repos that follow the discipline (a `.spec/` dir exists).
- Doc-only pushes always pass.
- Only `.spec/**/current.md`, `.spec/**/tasks.md`, `devlog.md`, and `todo.md`
  count as living-tier evidence; historical audit/ADR files do not.
- An unresolved comparison range fails visibly instead of silently passing.
- Escape hatches: `git push --no-verify`, or `CLOSE_THE_LOOP=skip git push`.

Wire-up (pre-commit framework, pre-push stage) — see pre-commit.template.yaml.
"""

import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from validate_workflow_docs import emit_report, validate_workflow_documents

ZEROS = "0" * 40
PROJECT_LIVING_PATHS = {"devlog.md", "todo.md"}
SPEC_LIVING_BASENAMES = {"current.md", "tasks.md"}


def git(*args):
    return subprocess.run(
        ["git", *args], capture_output=True, text=True
    )


def resolve_range():
    """Return the outgoing comparison range, or None so the guard fails closed."""
    from_ref = os.environ.get("PRE_COMMIT_FROM_REF") or ""
    to_ref = os.environ.get("PRE_COMMIT_TO_REF") or "HEAD"

    if not from_ref or from_ref == ZEROS:
        # New branch: compare against the default branch if we can find one.
        for candidate in ("origin/HEAD", "origin/main", "origin/master"):
            base = git("merge-base", candidate, to_ref)
            if base.returncode == 0 and base.stdout.strip():
                return base.stdout.strip(), to_ref
        return None  # caller reports the unresolved range and refuses the push

    return from_ref, to_ref


def changed_files(from_ref, to_ref):
    diff = git("diff", "--name-only", f"{from_ref}..{to_ref}")
    if diff.returncode != 0:
        return None
    return [line.strip() for line in diff.stdout.splitlines() if line.strip()]


def is_living_doc(path):
    p = path.replace("\\", "/")
    basename = p.rsplit("/", 1)[-1].lower()
    return (
        (p.startswith(".spec/") and basename in SPEC_LIVING_BASENAMES)
        or p.lower() in PROJECT_LIVING_PATHS
    )


def is_doc(path):
    return is_living_doc(path) or path.lower().endswith(".md")


def main():
    if os.environ.get("CLOSE_THE_LOOP", "").lower() == "skip":
        return 0
    if not os.path.isdir(".spec"):
        return 0

    resolved = resolve_range()
    if resolved is None:
        sys.stderr.write(
            "close-the-loop: unable to resolve the outgoing comparison range; "
            "refusing to treat this push as verified.\n"
            "Set PRE_COMMIT_FROM_REF/PRE_COMMIT_TO_REF or fetch origin/HEAD, "
            "then retry. Intentional exception: CLOSE_THE_LOOP=skip git push\n"
        )
        return 1
    files = changed_files(*resolved)
    if files is None:
        sys.stderr.write(
            "close-the-loop: git diff failed for the outgoing comparison "
            "range; refusing to pass silently.\n"
        )
        return 1
    if not files:
        return 0

    code = [f for f in files if not is_doc(f)]
    if not code:
        return 0
    if not any(is_living_doc(f) for f in files):
        sys.stderr.write(
            "close-the-loop: this push changes code but no living-tier doc.\n"
            "workflow.md requires updating, in the SAME PR:\n"
            "  .spec/<ticket>/{current.md,tasks.md}\n"
            "  devlog.md (newest-on-top entry) and todo.md\n"
            f"Code files pushed without docs ({len(code)}): {', '.join(code[:5])}"
            f"{' …' if len(code) > 5 else ''}\n"
            "Intentional? CLOSE_THE_LOOP=skip git push   (or git push --no-verify)\n"
        )
        return 1

    report = validate_workflow_documents(os.getcwd(), files, "wip")
    emit_report(report)
    if not report.ok:
        sys.stderr.write(
            "close-the-loop: living-doc structure is invalid. This guard still "
            "cannot prove semantic correctness.\n"
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
