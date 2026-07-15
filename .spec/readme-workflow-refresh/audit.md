# Audit — README and workflow foundation refresh

Date: 2026-07-15

## Public README

- GitHub's rendered page presents five dense tables before the reader reaches
  installation, making the entry point read like a reference manual.
- `Use it with any coding agent` starts after the operating loop, model table,
  routing table, and repository map, so adoption is visually secondary.
- Claude Code receives the only copy-ready adapter commands; Codex and other
  agents receive prose only.

## Canonical workflow

- Stage 1 still writes `.spec/current.md`, while repository rules, scripts, and
  newer docs use `.spec/<ticket>/current.md`.
- Build mandates a worktree, TDD, and one commit per task for every change,
  including documentation and low-risk edits where those controls add churn
  without improving evidence.
- Define, Plan, and Review always select the strongest model, which defeats
  capability-based cost control even for bounded work.
- High-risk review always selects security and performance lenses, whether or
  not those are the risks the diff introduces.
- The workflow says close-loop steps 1–4 are mechanically enforced. The script
  only rejects code pushes that touch no living-tier document; it cannot prove
  the documents are correct or that every required file was updated.
- Merge/deployment and other irreversible actions have no explicit approval
  gate in the six-stage canonical document.

## External evidence

- OpenAI recommends a short instruction map pointing to deeper sources rather
  than one large manual:
  https://openai.com/index/harness-engineering/
- OpenAI's Codex guidance keeps human review and permission for dangerous
  actions as explicit controls:
  https://openai.com/index/introducing-upgrades-to-codex/
- Claude Code supports task-specific permissions, model selection, and optional
  worktree isolation, supporting proportional routing rather than one fixed
  worker shape:
  https://code.claude.com/docs/en/sub-agents
- Addy Osmani's current `agent-skills` entry point puts a generic Quick Start
  before tool-specific adapters:
  https://github.com/addyosmani/agent-skills

## Decision

Keep the same evidence-first six stages, but make controls proportional to
risk. Put a three-step generic Quick start near the top of README, reduce table
density, default to a general coding model, and escalate isolation, model
capability, reviewer lenses, and human approval when the change warrants it.

## Independent review extension

- README review found that copy commands could overwrite an existing
  `AGENTS.md`, and that a PowerShell-only interactive script should not be part
  of the minimum any-agent path.
- Local-workflow review found that `start-task.ps1` creates no `current.md`,
  does not create a feature branch when worktree creation is declined, and
  trusts an existing worktree path without checking Git registration.
- Enforcement review confirmed that any `.spec/**` file currently satisfies
  `is_living_doc`, including historical `audit.md`, and unresolved Git ranges
  silently pass.
- Second-pass workflow review found that nested `docs/devlog.md` could satisfy
  the project-level living-doc requirement and worktree creation could inherit
  an unrelated feature branch. Both now have explicit guards and regression
  coverage.

## Pilotfish reference review

[`Nanako0129/pilotfish`](https://github.com/Nanako0129/pilotfish) is MIT
licensed and provides useful prior art for role-based policy, fresh read-only
verification, bounded escalation, explicit approval, and exact-context handoff.
This task adopts those generic concepts, with attribution, but not its
Claude-global installation, fixed role catalog, provider aliases, quota claims,
or wording.

## Verification before publish

- `python -m unittest discover -s tests -v` — 15 tests passed, including real
  temporary-repository branch, `current.md`, and worktree smoke tests.
- PowerShell parser — `scripts/start-task.ps1` parsed with zero errors.
- Plugin manifests — both JSON files parsed; Claude mirror version is `0.4.0`.
- `workflow.md` — 278 lines, within the 280-line map contract.
- Relative Markdown validator — passed; three documented template placeholders
  were skipped deliberately.
- GitHub Markdown API — rendered 8 headings, 1 table, and 3 details blocks.
- `git diff --check` — passed (Git only reported expected LF/CRLF checkout
  notices).
- Official Claude Code CLI `2.1.210` was installed at
  `C:\Users\Zoe\.local\bin\claude.exe`. Both strict validators passed:
  `claude plugin validate --strict .` and
  `claude plugin validate --strict .\claude-code\plugin`.

## Published handoff

- Core commit: `c4ae17e`
- Ready PR: [#17](https://github.com/zoetw88/ai-workflow/pull/17)
- Integration is intentionally pending Zoe's explicit merge approval.
