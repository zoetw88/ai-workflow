# AI Workflow — AI × backend reality

> **AI is a capable coworker who overstates its progress. Ask for evidence.**

This started with more than 20,000 lines of AI-assisted code and one missing
critical path: the Kafka integration the AI had already called "done."

The files were there. The code looked clean. The system still did not work.

So I stopped treating AI development as a better prompt and started treating
it as a system:

`messy request → explicit contract → isolated work → evidence → independent review → durable handoff`

This repository is that system. It is the tool-agnostic layer I share between
Claude Code, Codex, and whatever comes next. Tool-specific configuration is
glue; the rules that matter live in files.

## The operating loop

| Stage | The question | Evidence it leaves behind |
|---|---|---|
| **Define** | What are we actually solving? | scope, constraints, acceptance criteria |
| **Plan** | What are the smallest verifiable steps? | atomic task list |
| **Build** | Can the change be made in isolation? | focused diff in a dedicated worktree |
| **Verify** | Does it work? | commands, tests, output, file references |
| **Review** | Is it good and does it match the spec? | independent findings and decisions |
| **Ship** | Can the next person recover the truth? | commit, PR, updated handoff docs |

Two distinctions carry most of the weight:

- **A claim is not evidence.** "Done" means the acceptance criteria have proof.
- **Verify is not Review.** Tests ask whether it works; review asks whether it
  is the right, safe, maintainable thing.

The complete process lives in [`workflow.md`](workflow.md).

## Start with the problem you have

| If you need to… | Start here |
|---|---|
| understand the principles behind the workflow | [`PHILOSOPHY.md`](PHILOSOPHY.md) |
| run the full Define → Ship process | [`workflow.md`](workflow.md) |
| avoid the mistakes that shaped these rules | [`GOTCHAS.md`](GOTCHAS.md) |
| decode terms such as evidence block, living tier, or system map | [`GLOSSARY.md`](GLOSSARY.md) |
| clarify a vague request | [`prompts/grill-me.md`](prompts/grill-me.md) |
| prove a task is actually complete | [`prompts/verify-done.md`](prompts/verify-done.md) |
| review AI-generated code adversarially | [`prompts/review-checklist.md`](prompts/review-checklist.md) |
| start a ticket with the right files | [`scripts/start-task.ps1`](scripts/start-task.ps1) |
| avoid Go, Python, or production-LLM traps | [`pitfalls/`](pitfalls) |

## What lives here

| Area | Job |
|---|---|
| [`prompts/`](prompts) | reusable actions: clarify, review, debug, audit, verify |
| [`pitfalls/`](pitfalls) | pre-write checklists for mistakes AI repeats |
| [`templates/`](templates) | project rules, specs, tasks, ADRs, maps, and hooks |
| [`claude-code/plugin/`](claude-code/plugin) | Claude Code skills and planner/builder/reviewer agents |
| [`scripts/`](scripts) | task bootstrap, spec-map generation, close-the-loop guard |
| [`shell/aliases.sh`](shell/aliases.sh) | small worktree and context helpers |

The canonical documents stay tool-agnostic. Adapter copies under
`claude-code/plugin/skills/` carry a `Canonical source` header so drift is
visible and reviewable.

## Install

Clone the shared layer:

```bash
git clone https://github.com/zoetw88/ai-workflow.git ~/.ai-workflow
```

Optional shell helpers:

```bash
source ~/.ai-workflow/shell/aliases.sh
```

### Claude Code

Inside Claude Code:

```text
/plugin marketplace add zoetw88/ai-workflow
/plugin install ai-workflow@zoetw88
```

This installs the workflow, clarification, verification, pitfall, system-map,
and portfolio skills plus the planner, builder, and reviewer agents.

For global rules, start from
[`claude-code/CLAUDE.md.example`](claude-code/CLAUDE.md.example).

### Codex and other agents

Codex reads project `AGENTS.md` files directly. Other tools can consume the
same Markdown sources without adopting the Claude plugin format.

For a new project, copy:

```text
templates/AGENTS.md.template  → AGENTS.md
templates/CLAUDE.md.template  → CLAUDE.md
```

For a new ticket:

```powershell
pwsh ./scripts/start-task.ps1
```

## When something new is learned

Every durable rule should have one home:

| What changed | Put it here |
|---|---|
| a reusable prompt pattern | `prompts/` |
| a language or library trap AI repeats | `pitfalls/<language>.md` |
| a repo-specific gotcha | that repo's `AGENTS.md` |
| a ticket-specific workaround | `.spec/<ticket>/ai-development-map.md` |
| a process change | `workflow.md` |
| a principle change | `PHILOSOPHY.md` — rarely |
| a public entry point or integration edge | patch `system-map.md` in the same PR |

This is how the workflow improves: not from collecting more instructions, but
from turning real failures into rules at the correct boundary.

## Built with this workflow

- [job-tracker-skill](https://github.com/zoetw88/job-tracker-skill) — a Claude
  Code skill for funnel metrics, interview logs, follow-up cadence, and
  rejection-stage analysis.

## The longer story

Read [AI Is a Coworker Who Overstates Its Progress: How I Build With It](https://zoe-builds.com/en/articles/my-ai-workflow/)
for the failure behind these rules and why acceptance criteria changed the way
I work with agents.

More from [Zoe](https://zoe-builds.com): practical notes on AI products,
backend systems, and engineering judgment without the hype.
