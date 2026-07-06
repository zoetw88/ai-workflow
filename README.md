# ~/.ai-workflow — tool-agnostic AI development layer

The single source of truth shared between Claude Code, Codex, and any future agent tool.

## Why this exists

Tool-specific configs (`~/.claude/`, `~/.codex/`) hold tool-specific glue.
**Anything that should outlive a tool change lives here.**

## Start here

Read in this order:

1. [`PHILOSOPHY.md`](PHILOSOPHY.md) — the six principles behind everything else (evidence over memory, acceptance criteria first, never round up, capture lessons, don't pad).
2. [`workflow.md`](workflow.md) — the canonical 6-stage workflow (Define → Plan → Build → Verify → Review → Ship), per-ticket worktree isolation, the two-tier doc discipline, risk-tiered review, parallel-agent patterns, and model assignment per stage.
3. `templates/` — grab what the workflow tells you to grab.

The index hierarchy, from widest zoom to narrowest — each level answers one question:

| File | Question it answers | For |
|---|---|---|
| `system-map.md` | Where does everything live, what talks to what? | agents (context cache) |
| `portfolio.md` | What is every project doing, what's next? | humans (status) |
| `<repo>/spec-map.md` | What spec areas exist in this repo? | both |
| `.spec/<ticket>/ai-development-map.md` | What do I read to pick up this ticket? | agents (handoff) |

## Layout

```
~/.ai-workflow/
├── README.md                    (this file)
├── PHILOSOPHY.md                Six principles for working with AI agents
├── workflow.md                  The canonical 6-stage workflow + context discipline
│
├── prompts/                     Reusable prompt fragments
│   ├── grill-me.md              Interactive requirement clarification (Define stage)
│   ├── code-review.md           Adversarial review of freshly written code
│   ├── review-checklist.md      Priority-ordered review checklist (Review stage)
│   ├── refactor.md              Behavior-preserving cleanup
│   ├── debug-ai-bug.md          Locating bugs in AI-generated code
│   ├── parallel-audit.md        Fan-out read-only audits across repos/modules
│   ├── portfolio-scan.md        gh-CLI scan of ALL repos → regenerates portfolio.md
│   ├── system-map-scan.md       One-time parallel scan → system-map.md, then patch-only
│   └── verify-done.md           Evidence block required before claiming "done" (Verify stage)
│
├── pitfalls/                    Language/library traps AI repeatedly misses
│   ├── go.md                    Pre-write checklist for Go (context, goroutines, …)
│   ├── python.md                Python/Django traps (mutable defaults, …)
│   └── (add more as you encounter them)
│
├── templates/                   Drop-in files for projects and tickets
│   ├── spec.md                  .spec/<ticket>/current.md starter   (living tier)
│   ├── tasks.md                 .spec/<ticket>/tasks.md starter     (living tier)
│   ├── adr.md                   Architecture Decision Record        (historical tier)
│   ├── devlog.md                Project-level rolling devlog        (historical tier)
│   ├── todo.md                  Project-level rolling work queue    (living tier)
│   ├── ai-development-map.md    Per-ticket handoff read-order for agents
│   ├── portfolio.md             Cross-project STATUS: what every repo is doing (living tier)
│   ├── system-map.md            Cross-repo STRUCTURE: agent context cache — entry points,
│   │                            public surfaces, integration edges (living tier)
│   ├── AGENTS.md.template       Project agent rules — the single source of truth
│   ├── CLAUDE.md.template       Thin shim that imports AGENTS.md (@AGENTS.md)
│   └── pre-commit.template.yaml Pre-commit hooks: tests, lint, secret scan
│
├── .claude-plugin/
│   └── marketplace.json         Makes this repo a Claude Code plugin marketplace
│
├── claude-code/                 Claude Code-specific glue (references the layers above)
│   ├── CLAUDE.md.example        Global rules — drop into ~/.claude/CLAUDE.md
│   └── plugin/                  Installable plugin (see Setup below)
│       ├── .claude-plugin/plugin.json
│       ├── skills/              grill-me, six-stage-workflow, verify-done,
│       │                        go-pitfalls, python-pitfalls,
│       │                        build-system-map, portfolio-scan
│       └── agents/              planner (Define/Plan), builder (Build), reviewer (Review)
│
├── scripts/                     Automation (PowerShell, cross-platform via pwsh)
│   ├── start-task.ps1           Bootstrap a ticket: .spec/<ticket>/ scaffolding
│   └── build-spec-map.ps1       Generate/diff spec-map.md so the index never drifts
│
└── shell/
    └── aliases.sh               cc/ccr/ccp aliases, wt/wtrm worktree helpers, ctx, sprint, init-claude-md
```

## How tools consume this

- **Claude Code** — global rules live in `~/.claude/CLAUDE.md` (start from
  `claude-code/CLAUDE.md.example`); skills and subagents install as a plugin from
  `claude-code/plugin/` (see Setup). Plugin skills that mirror tool-agnostic files
  (workflow, verify-done, pitfalls) embed a copy with a `Canonical source` header —
  when you change one side, update the other.
- **Codex** — `~/.codex/AGENTS.md` mirrors the same global rules; per-project
  `AGENTS.md` files reference these files.
- **Project-level** — each repo has an `AGENTS.md` (from
  `templates/AGENTS.md.template`) as its single source of truth, plus a thin
  `CLAUDE.md` that imports it via `@AGENTS.md`. Both point back here for global
  process. Each project declares `Project type: personal | team` at the top —
  see `workflow.md` for what that toggles.

## Setup on a new machine

```bash
git clone <your-private-remote> ~/.ai-workflow

# shell helpers (add to ~/.zshrc or ~/.bashrc)
source ~/.ai-workflow/shell/aliases.sh

# Claude Code global rules
cp ~/.ai-workflow/claude-code/CLAUDE.md.example ~/.claude/CLAUDE.md   # then personalize
```

Claude Code skills + subagents install as a plugin — inside Claude Code run:

```
/plugin marketplace add zoetw88/ai-workflow
/plugin install ai-workflow@zoetw88
```

This gives you the `six-stage-workflow`, `grill-me`, `verify-done`, `go-pitfalls`,
`python-pitfalls`, `build-system-map`, and `portfolio-scan` skills plus the
`planner` / `builder` / `reviewer` subagents, with one-command updates — no manual
copying into `~/.claude/`.

Per new project: copy `templates/AGENTS.md.template` → `AGENTS.md`,
`templates/CLAUDE.md.template` → `CLAUDE.md`, and optionally
`templates/pre-commit.template.yaml` → `.pre-commit-config.yaml`.

Per new ticket: run `scripts/start-task.ps1` (or copy `templates/spec.md` and
`templates/tasks.md` into `.spec/<ticket>/` by hand).

One-time, once your repos are cloned: run the `prompts/system-map-scan.md` procedure to
build `~/.ai-workflow/system-map.md` (agents read it instead of re-exploring every repo
each session — close-the-loop keeps it patched), and `prompts/portfolio-scan.md` for
`portfolio.md` (refresh monthly or when deciding what to work on).

## Where new content goes

| You learned / built | Put it in |
|---|---|
| A reusable prompt pattern | `prompts/` |
| A language/library trap AI keeps hitting | `pitfalls/<lang>.md` |
| A repo-specific gotcha | that repo's `AGENTS.md`, not here |
| A ticket-specific workaround | that ticket's `.spec/<ticket>/ai-development-map.md` |
| A new/changed entry point, endpoint, event, or cross-repo edge | patch `system-map.md` in the same PR (close-the-loop step 4) |
| A project changed status (paused, archived, new) | rerun `prompts/portfolio-scan.md` |
| A new doc/file every project needs | `templates/` |
| A Claude Code skill or subagent | `claude-code/plugin/skills/` or `agents/` — bump `plugin.json` version; mirrored skills carry a `Canonical source` header, keep both sides in sync |
| A process change | `workflow.md` |
| A principle change | `PHILOSOPHY.md` (rare) |

## Built with this workflow

- [job-tracker-skill](https://github.com/zoetw88/job-tracker-skill) — Claude Code skill for systematic job search tracking: funnel metrics, interview logs, follow-up cadence, rejection-stage analysis.

## Versioning

This directory is a git repo. Commit and push every change — when you change
machines, clone it and you're back.
