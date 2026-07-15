# AI Workflow

**Evidence-first engineering with coding agents.**

> **AI is a capable coworker who overstates its progress. Ask for evidence.**

This started with more than 20,000 lines of AI-assisted code and one missing
critical path: the Kafka integration the AI had already called "done."

The files were there. The code looked clean. The system still did not work.

So I stopped treating AI development as a better prompt and started treating
it as a system:

`messy request → explicit contract → isolated work → evidence → independent review → durable handoff`

This repository contains the portable Markdown contracts, prompts, templates,
and checks behind that system. Any coding agent can use the canonical files;
tool-specific configuration is optional glue.

## Quick start

The minimum setup is clone, merge one instruction file, and give the agent a
clear starting command.

1. Clone the shared workflow.

   ```bash
   git clone https://github.com/zoetw88/ai-workflow.git ~/.ai-workflow
   ```

2. Add the project-instruction template without overwriting local rules.

   If `AGENTS.md` already exists, merge the relevant sections from
   [`templates/AGENTS.md.template`](templates/AGENTS.md.template) into it. If it
   does not exist, use the guarded copy command for your shell:

   ```bash
   # macOS / Linux
   test -e ./AGENTS.md && echo "AGENTS.md exists; merge it manually" || \
     cp ~/.ai-workflow/templates/AGENTS.md.template ./AGENTS.md
   ```

   ```powershell
   # PowerShell
   if (Test-Path ./AGENTS.md) {
     Write-Host "AGENTS.md exists; merge it manually"
   } else {
     Copy-Item "$HOME/.ai-workflow/templates/AGENTS.md.template" ./AGENTS.md
   }
   ```

3. Give your coding agent one instruction:

```text
Read AGENTS.md and ~/.ai-workflow/workflow.md, then follow the six-stage
workflow for this task. Do not claim completion without verification evidence.
```

Optional shell helpers live in [`shell/aliases.sh`](shell/aliases.sh).

<details>
<summary>Optional task bootstrap</summary>

For a guided intake that can create ticket files and an isolated workspace:

```powershell
# Run inside the target repository:
pwsh ~/.ai-workflow/scripts/start-task.ps1

# Or name the repository explicitly:
pwsh ~/.ai-workflow/scripts/start-task.ps1 -RepoPath C:\path\to\repo
```

</details>

Local pre-push uses **WIP mode**: draft checkboxes may remain open, but ticket
documents must be structurally valid. Pull requests use **Ship mode** in
GitHub-hosted CI: changes outside the living tier, including substantive
Markdown, require completed living docs; repository tests and both strict
Claude adapter validators must pass. CI pins the project type so a PR cannot
disable its own personal-project policy. Acceptance criteria should name an
observable result, environment, and verification step; weak wording warns
without blocking. These checks validate evidence structure, not factual truth.

## The operating loop

| Stage | The question | Evidence it leaves behind |
|---|---|---|
| **Define** | What are we actually solving? | scope, constraints, acceptance criteria |
| **Plan** | What are the smallest verifiable steps? | atomic task list |
| **Build** | Can the change be made safely and in scope? | focused diff on an isolated branch or worktree |
| **Verify** | Does it work in the environment tested? | commands, tests, output, file references |
| **Review** | Is it right, safe, and maintainable? | independent findings and decisions |
| **Ship** | Can the next person recover the truth? | commit, PR, updated handoff docs |

Two distinctions carry most of the weight:

- **A claim is not evidence.** "Done" means the acceptance criteria have proof.
- **Verify is not Review.** Tests ask whether it works; review asks whether it
  is the right, safe, maintainable thing.

The complete process lives in [`workflow.md`](workflow.md).

## Choose the model; keep the gates

There is no separate smart-model and cheap-model workflow. Every model keeps
the same acceptance criteria, verification, review, and evidence gates.

- **Fast / low-cost** — search, classification, formatting, and deterministic
  checks. Give exact files, narrow output, and read-only access by default.
- **General coding** — the default for accepted, well-bounded implementation
  and review work. Give one slice, one allowed change surface, and exact checks.
- **Strongest reasoning** — escalate for ambiguity, architecture, conflicting
  evidence, high-risk changes, or repeated failure on the same bounded task.

Use a weaker model by shrinking the task and making the contract explicit, not
by lowering the definition of done. See the full routing policy in
[`workflow.md`](workflow.md#model-routing-one-workflow-different-autonomy).

## Find what you need

- **Understand the principles** — [`PHILOSOPHY.md`](PHILOSOPHY.md)
- **Run Define → Ship** — [`workflow.md`](workflow.md)
- **Recognize recurring failure patterns** — [`GOTCHAS.md`](GOTCHAS.md)
- **Decode workflow terminology** — [`GLOSSARY.md`](GLOSSARY.md)
- **Manage ticket and cross-project context** — [`context-management.md`](context-management.md)
- **Clarify a vague request** — [`prompts/grill-me.md`](prompts/grill-me.md)
- **Prove completion** — [`prompts/verify-done.md`](prompts/verify-done.md)
- **Review adversarially** — [`prompts/review-checklist.md`](prompts/review-checklist.md)
- **Avoid technical traps** — [`pitfalls/`](pitfalls)

<details>
<summary>Repository map</summary>

- [`prompts/`](prompts) — reusable clarification, debugging, review, audit, and
  verification actions.
- [`pitfalls/`](pitfalls) — pre-write checklists for mistakes agents repeat.
- [`templates/`](templates) — project rules, specs, tasks, ADRs, maps, and hooks.
- [`scripts/`](scripts) — task bootstrap, map validation, and WIP/Ship close-loop guards.
- [`claude-code/plugin/`](claude-code/plugin) — optional Claude Code adapter.

Canonical documents stay tool-agnostic. Adapter copies that declare a
`Canonical source` must be updated with their source so drift stays visible.

</details>

## Tool adapters

**Codex** reads project `AGENTS.md` files directly. Other coding agents should
use their project-instruction mechanism to read the same file. If a tool cannot
import it, keep a thin shim that points to `AGENTS.md`; do not duplicate rules.

Parallel agents and automatic model routing are optional optimizations, not
prerequisites for the six-stage workflow.

<details>
<summary>Claude Code plugin (optional)</summary>

Use [`templates/CLAUDE.md.template`](templates/CLAUDE.md.template) as a thin
shim that imports `AGENTS.md`, or install the packaged skills and agents:

```text
/plugin marketplace add zoetw88/ai-workflow
/plugin install ai-workflow@zoetw88
```

For global rules, start from
[`claude-code/CLAUDE.md.example`](claude-code/CLAUDE.md.example).

</details>

## Keep lessons durable

Every reusable lesson should have one home:

- reusable prompt pattern → `prompts/`
- language or library trap → `pitfalls/<language>.md`
- repo-specific rule → that repository's `AGENTS.md`
- ticket-specific workaround → `.spec/<ticket>/ai-development-map.md`
- process change → `workflow.md`
- principle change → `PHILOSOPHY.md` — rarely

This is how the workflow improves: turn real failures into rules at the correct
boundary instead of collecting more instructions everywhere.

## The longer story

Read [AI Is a Coworker Who Overstates Its Progress: How I Build With It](https://zoe-builds.com/en/articles/my-ai-workflow/)
for the failure behind these rules and why acceptance criteria changed the way
I work with agents.

More from [Zoe](https://zoe-builds.com): practical notes on AI products,
backend systems, and engineering judgment without the hype.
