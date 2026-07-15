---
name: six-stage-workflow
description: Use when starting any non-trivial feature, bugfix, or refactor. Enforces the Define → Plan → Build → Verify → Review → Ship discipline with per-ticket worktrees, TDD, evidence-based verification, and risk-tiered review.
---

<!-- Canonical source: ~/.ai-workflow/workflow.md — if that file exists on this machine,
     read it instead; it is the full version and may be newer than this embedded copy. -->

# The six stages

1. **Define** — Grill the user (see the `grill-me` skill). Produce `.spec/<ticket>/current.md`.
2. **Plan** — Break the spec into atomic tasks in `.spec/<ticket>/tasks.md`. Each task:
   2–5 minutes of focused work, ≤ 1 commit, with exact file paths and a `Verify:` command.
3. **Build** — One task at a time, in an isolated worktree. TDD. One commit per task.
4. **Verify** — Run tests. Tests are proof. Before claiming done, produce the evidence
   block from the `verify-done` skill.
5. **Review** — Independent reviewer with FRESH context (spawn the `reviewer` agent).
   Check spec conformance + AI smells.
6. **Ship** — Commit message, PR description, ADR if architectural. Close the loop first
   (see below).

**Verify ≠ Review.** Verify answers "does it work?"; review answers "is it good?".
Never collapse them.

## Workspace isolation

Build happens on a dedicated branch in a dedicated worktree — never on the main checkout:

```bash
git worktree add ../<repo>-<ticket> -b <ticket>
```

Run the test suite in the fresh worktree BEFORE writing anything. If the baseline is
already red, report it as a blocker — do not "fix it along the way". Remove the worktree
at Ship, after the PR is opened.

## Review depth scales with risk

Default: ONE reviewer. Escalate to a 3-lens panel (spec conformance + security + performance,
three parallel agents) only when the diff touches:

- auth / permissions / session handling
- money, transactions, or data migrations
- concurrency or caching
- public API contracts

These categories also require a passing integration test before "done".

## Context discipline (two-tier docs)

- **Living tier** — must always reflect current state: `.spec/<ticket>/current.md`,
  `tasks.md`, project-level `devlog.md` + `todo.md`.
- **Historical tier** — append-only: `audit.md`, `adr-*.md`. To overturn a decision,
  write a NEW ADR marked `Supersedes ADR-NNNN` — never edit the old one's body.

Before proposing an approach (Define/Plan): read `current.md` + every settled ADR for the
ticket, and state which docs you consulted. Conflict with a recorded decision → STOP and
flag it; the user decides.

Before opening a PR (close the loop): update every living-tier doc the change touched,
append a newest-on-top `devlog.md` entry, refresh `todo.md`, and commit the doc updates
in the SAME PR.

## Model routing: one workflow, different autonomy

Every model follows the same six stages and evidence gates. Change the task
shape, not the definition of done:

- **Fast / lower-cost:** exact files, one bounded question, structured output,
  and read-only permissions by default.
- **General coding:** one accepted implementation slice, a constrained change
  surface, and an exact verification command.
- **Strongest reasoning:** ambiguous requirements, architecture, conflicting
  evidence, and high-risk review — with the same tests and independent review.

Escalate when risk or uncertainty grows, when evidence conflicts, or after two
failures on the same bounded task. Do not hard-code provider model versions in
the workflow; choose the current model matching the required capability.

## What humans always own

Architectural decisions, security-sensitive code, performance/cost trade-offs, production
deployments, and the final accept/reject on review findings. AI proposes. Humans dispose.
