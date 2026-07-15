# AI Workflow Repository Rules

**Project type: personal**

This repository is the tool-agnostic source of truth for Zoe's AI-development
workflow. It contains documentation, reusable prompts, templates, scripts, and
Claude Code plugin adapters; it is not an application runtime.

## Canonical sources

- Process changes belong in `workflow.md`.
- Principle changes belong in `PHILOSOPHY.md`.
- Reusable technical traps belong in `pitfalls/`.
- `README.md`, `GOTCHAS.md`, and `GLOSSARY.md` are public entry points. Keep
  them concise and link to canonical details instead of duplicating them.
- Files under `claude-code/plugin/skills/` that declare a `Canonical source`
  are mirrors. When the canonical source changes, update the mirror and plugin
  version in the same change.

## Workflow

For non-trivial work, use `.spec/<ticket>/` for acceptance criteria, audit
evidence, and handoff state. Update `devlog.md` and `todo.md` before shipping.

## Verification

- `git diff --check`
- `python scripts/check_close_the_loop.py`
- Validate changed Markdown links and render the README through GitHub's
  Markdown API before changing its public structure.

Do not commit credentials, local repository inventories, private project data,
or generated personal maps.
