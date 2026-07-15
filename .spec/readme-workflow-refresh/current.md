# README and workflow foundation refresh

## Goal

Make the public README easy to scan and adopt, then correct the canonical
workflow so its guarantees match the repository's actual tooling and a
cost-conscious, risk-based agent practice.

## Acceptance criteria

- [x] README presents a copy-ready Quick start before reference material.
- [x] README uses no more than two tables and keeps Claude-specific setup
      visually secondary to the generic agent path.
- [x] Quick start never overwrites an existing `AGENTS.md`; the interactive
      PowerShell bootstrap is optional rather than a minimum requirement.
- [x] The six stages use `.spec/<ticket>/...` consistently.
- [x] Isolation and test-first rules scale with change risk instead of forcing
      a worktree, TDD, and one commit per task for every change.
- [x] Verify distinguishes local evidence from production evidence; Review
      findings are resolved or explicitly accepted before Ship.
- [x] Merge, migration, deployment, payment, and production user-data actions
      have an explicit human approval gate.
- [x] Model routing defaults to a general coding model and escalates for risk,
      ambiguity, conflicting evidence, or repeated bounded failure.
- [x] Review selects relevant risk lenses instead of always spawning a fixed
      security-and-performance panel.
- [x] The close-loop documentation accurately states what
      `scripts/check_close_the_loop.py` does and does not enforce.
- [x] The close-loop guard counts only true living-tier documents and fails
      visibly when it cannot resolve the outgoing comparison range.
- [x] `start-task.ps1` persists `current.md`, creates or reuses only the ticket
      worktree from a shared branch, and creates a feature branch when the user
      declines a worktree.
- [x] Claude adapter copies, related prompts, and plugin metadata stay aligned
      with the canonical workflow; plugin version is at least `0.4.0`.
- [x] Targeted docs-contract tests, Markdown links, GitHub rendering,
      `git diff --check`, and the close-loop guard pass.

## Non-goals

- Add native adapters for more agent products.
- Install or deploy an agent runtime.
- Replace the repository's evidence-first six-stage structure.
- Add decorative badges, screenshots, or marketing claims.
