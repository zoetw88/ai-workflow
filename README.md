# ~/.ai-workflow — tool-agnostic AI development layer

The single source of truth shared between Claude Code, Codex, and any future agent tool.

## Why this exists

Tool-specific configs (`~/.claude/`, `~/.codex/`) hold tool-specific glue.
**Anything that should outlive a tool change lives here.**

## Layout

```
~/.ai-workflow/
├── README.md              (this file)
├── pitfalls/              Language- and library-specific traps AI repeatedly misses
│   ├── go.md
│   └── (add more as you encounter them)
├── prompts/               Reusable prompt fragments — grill, review checklist, etc.
│   ├── grill-me.md
│   └── review-checklist.md
├── templates/             Spec / task / ADR templates
│   ├── spec.md
│   ├── tasks.md
│   └── adr.md
└── workflow.md            The canonical 6-stage workflow (Define → Ship)
```

## How tools consume this

- **Claude Code** — skills in `~/.claude/skills/*/SKILL.md` reference these files
- **Codex** — `AGENTS.md` in each project references these files
- **Project-level** — each repo has a `CLAUDE.md` + `AGENTS.md` (often symlinked to the same content) that point here

## Versioning

This directory should be a git repo. Push it. When you change machines, clone it.

```bash
cd ~/.ai-workflow && git init && git add . && git commit -m "init"
# then push to a private repo
```
