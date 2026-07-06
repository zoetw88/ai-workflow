#!/usr/bin/env python3
"""Pre-push guard: refuse to push code without the living-tier docs.

Enforces workflow.md's close-the-loop rule mechanically: if the commits being
pushed change code but touch neither `.spec/**` nor `devlog.md` / `todo.md`,
the push is rejected with a reminder.

Scope rules:
- Only enforces in repos that follow the discipline (a `.spec/` dir exists).
- Doc-only pushes always pass.
- Escape hatches: `git push --no-verify`, or `CLOSE_THE_LOOP=skip git push`.

Wire-up (pre-commit framework, pre-push stage) — see pre-commit.template.yaml.
"""

import os
import subprocess
import sys

ZEROS = "0" * 40
LIVING_BASENAMES = {"devlog.md", "todo.md"}


def git(*args):
    return subprocess.run(
        ["git", *args], capture_output=True, text=True
    )


def resolve_range():
    """Return (from_ref, to_ref) for the outgoing commits, or None to skip."""
    from_ref = os.environ.get("PRE_COMMIT_FROM_REF") or ""
    to_ref = os.environ.get("PRE_COMMIT_TO_REF") or "HEAD"

    if not from_ref or from_ref == ZEROS:
        # New branch: compare against the default branch if we can find one.
        for candidate in ("origin/HEAD", "origin/main", "origin/master"):
            base = git("merge-base", candidate, to_ref)
            if base.returncode == 0 and base.stdout.strip():
                return base.stdout.strip(), to_ref
        return None  # nothing to compare against — stay silent

    return from_ref, to_ref


def changed_files(from_ref, to_ref):
    diff = git("diff", "--name-only", f"{from_ref}..{to_ref}")
    if diff.returncode != 0:
        return None
    return [line.strip() for line in diff.stdout.splitlines() if line.strip()]


def is_living_doc(path):
    p = path.replace("\\", "/")
    return p.startswith(".spec/") or p.rsplit("/", 1)[-1].lower() in LIVING_BASENAMES


def is_doc(path):
    return is_living_doc(path) or path.lower().endswith(".md")


def main():
    if os.environ.get("CLOSE_THE_LOOP", "").lower() == "skip":
        return 0
    if not os.path.isdir(".spec"):
        return 0

    resolved = resolve_range()
    if resolved is None:
        return 0
    files = changed_files(*resolved)
    if files is None or not files:
        return 0

    code = [f for f in files if not is_doc(f)]
    if not code:
        return 0
    if any(is_living_doc(f) for f in files):
        return 0

    sys.stderr.write(
        "close-the-loop: this push changes code but no living-tier doc.\n"
        "workflow.md requires updating, in the SAME PR:\n"
        "  .spec/<ticket>/{current.md,tasks.md,ai-development-map.md}\n"
        "  devlog.md (newest-on-top entry) and todo.md\n"
        f"Code files pushed without docs ({len(code)}): {', '.join(code[:5])}"
        f"{' …' if len(code) > 5 else ''}\n"
        "Intentional? CLOSE_THE_LOOP=skip git push   (or git push --no-verify)\n"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
