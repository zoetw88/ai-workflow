# AI Workflow — evidence-first engineering with coding agents

> **AI is a capable coworker who overstates its progress. Ask for evidence.**

This started with more than 20,000 lines of AI-assisted code and one missing
critical path: the Kafka integration the AI had already called "done."

The files were there. The code looked clean. The system still did not work.

So I stopped treating AI development as a better prompt and started treating
it as a system:

`messy request → explicit contract → isolated work → evidence → independent review → durable handoff`

This repository is that system: portable Markdown contracts, prompts,
templates, and checks that any coding agent can follow. Claude Code and Codex
have convenient adapters here, but neither is required. Tool-specific
configuration is glue; the rules that matter live in files.

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

## One workflow, different model budgets

There is no separate "smart model workflow" and "cheap model workflow." The
same acceptance criteria, verification, review, and evidence gates apply to
both. What changes is how much judgment and autonomy the model receives.

| Capability profile | Good fit | Operating boundary |
|---|---|---|
| **Fast / low-cost** | search, classification, formatting, deterministic checks | exact files, narrow output, read-only by default |
| **General coding** | a well-specified implementation slice, test repair, routine refactors | one atomic task, focused diff, required test command |
| **Strongest reasoning** | ambiguous requirements, architecture, conflicting evidence, high-risk review | broader context and judgment, but no skipped gates |

Use a weaker model by making the task smaller and the contract more explicit,
not by lowering the definition of done. Escalate when risk or uncertainty
increases, not merely because the workflow reached a particular stage. The
full routing and escalation policy lives in [`workflow.md`](workflow.md).

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
| [`claude-code/plugin/`](claude-code/plugin) | optional Claude Code adapter: skills and planner/builder/reviewer agents |
| [`scripts/`](scripts) | task bootstrap, spec-map generation, close-the-loop guard |
| [`shell/aliases.sh`](shell/aliases.sh) | small worktree and context helpers |

The canonical documents stay tool-agnostic. Adapter copies under
`claude-code/plugin/skills/` carry a `Canonical source` header so drift is
visible and reviewable.

## Use it with any coding agent

Clone the shared layer; that is enough to use the canonical documents:

```bash
git clone https://github.com/zoetw88/ai-workflow.git ~/.ai-workflow
```

Optional shell helpers:

```bash
source ~/.ai-workflow/shell/aliases.sh
```

For a new project, copy the portable source of truth:

```text
templates/AGENTS.md.template  → AGENTS.md
```

Then configure your coding agent to read `AGENTS.md` and the canonical
`workflow.md`. For a new ticket:

```powershell
pwsh ~/.ai-workflow/scripts/start-task.ps1
```

### Codex

Codex reads project `AGENTS.md` files directly. Keep repo-specific context in
that file and link back to this repository for the global process.

### Claude Code

Use [`templates/CLAUDE.md.template`](templates/CLAUDE.md.template) as a thin
shim that imports `AGENTS.md`. The plugin is optional; it packages the same
workflow as native skills and subagents.

Inside Claude Code:

```text
/plugin marketplace add zoetw88/ai-workflow
/plugin install ai-workflow@zoetw88
```

This installs the workflow, clarification, verification, pitfall, system-map,
and portfolio skills plus the planner, builder, and reviewer agents.

For global rules, start from
[`claude-code/CLAUDE.md.example`](claude-code/CLAUDE.md.example).

### Other coding agents

Point the tool's project-instruction mechanism at `AGENTS.md`. If it cannot
import another file, keep a thin tool-specific shim that tells the agent to
read `AGENTS.md`; do not maintain two copies of the rules. Parallel-agent and
automatic model routing features are optional optimizations, not prerequisites
for the six-stage workflow.

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

- [job-tracker-skill](https://github.com/zoetw88/job-tracker-skill) — a
  Claude Code adapter for funnel metrics, interview logs, follow-up cadence,
  and rejection-stage analysis, built with the same tool-agnostic process.

## The longer story

Read [AI Is a Coworker Who Overstates Its Progress: How I Build With It](https://zoe-builds.com/en/articles/my-ai-workflow/)
for the failure behind these rules and why acceptance criteria changed the way
I work with agents.

More from [Zoe](https://zoe-builds.com): practical notes on AI products,
backend systems, and engineering judgment without the hype.
