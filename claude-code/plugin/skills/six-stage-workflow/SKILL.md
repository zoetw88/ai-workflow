---
name: six-stage-workflow
description: Use for non-trivial features, bug fixes, or refactors. Enforces Define → Plan → Build → Verify → Review → Ship with proportional isolation, test-first behavior changes, evidence, risk-based review, and approval gates.
---

<!-- Canonical source: ~/.ai-workflow/workflow.md — if that file exists on this machine,
     read it instead; it is the full version and may be newer than this embedded copy. -->

# The six stages

1. **Define** — Turn the request into accepted scope, constraints, non-goals,
   and criteria in `.spec/<ticket>/current.md`. Each criterion should name an
   Observable result, Environment, and exact Verify command or manual step.
2. **Plan** — Write dependency-ordered, independently verifiable slices in
   `.spec/<ticket>/tasks.md`, with paths and exact checks.
3. **Build** — Implement one accepted slice on a feature branch. Use test-first
   development for behavior when a test harness exists; use the relevant
   validator for docs, configuration, and generated data.
4. **Verify** — Run checks and report exact commands, output, and environment.
   Local evidence is not production evidence.
5. **Review** — Use fresh context for spec conformance and the risks the diff
   actually introduces. Fix and reverify findings or record their acceptance.
6. **Ship** — Close the loop, prepare a cohesive commit and PR, and state what
   was not verified. Ship does not grant merge or deployment authority.

**Verify ≠ Review.** Verify answers "does it work?"; review answers "is it the
right, safe, maintainable thing?" Never collapse them.

## Proportional isolation

Every write belongs on a feature branch. Use a dedicated worktree for
non-trivial work, parallel writers, or when the shared checkout must stay
stable. A clean feature branch is enough for a bounded documentation or
low-risk single-file change.

Before editing, inspect `git status`, preserve unrelated changes, and run the
narrow relevant baseline for a behavior change. Parallel writers never share
a working directory.

## Context and close-loop discipline

- **Living tier:** `.spec/<ticket>/current.md`, `tasks.md`, and, when the
  project's convention requires them, `devlog.md` and `todo.md`.
- **Historical tier:** append-only `audit.md` and `adr-*.md`. Supersede an ADR
  with a new ADR; do not rewrite its body.

Before Plan, read current truth and settled decisions. **WIP mode** checks the
available ticket pair, required headings, and placeholders while allowing open
checkboxes. **Ship mode** treats every change outside the living tier, including canonical Markdown,
as substantive and requires the same ticket's changed
`current.md` and `tasks.md`, completed checklists, and personal-project
`devlog.md` plus `todo.md`; CI pins project type so a PR cannot disable that
policy. Missing Observable, Environment, or Verify fields
emit warnings only. These are structural evidence checks; they cannot prove the
documents are accurate or the private system map is current.

## Review depth scales with risk

Default to one fresh reviewer. Add only relevant specialist lenses:

- security for auth, trust boundaries, secrets, crypto, or untrusted input
- data integrity for transactions, migrations, retries, and idempotency
- performance for queries, hot paths, capacity, and material cost
- compatibility for public APIs, events, clients, and rollout behavior
- operability for production availability and recovery paths

Reviewers report before they fix. The orchestrator or authorized builder owns
changes; affected verification runs again afterward.

## Model routing: one workflow, different autonomy

Use a general coding model by default for bounded Define, Plan, Build, and
Review work. Prefer deterministic tools for Verify and fast models for narrow
classification, search, or evidence formatting.

Escalate to the strongest reasoning tier when requirements remain ambiguous,
scope crosses boundaries, risk is high, evidence conflicts, or the current tier
fails twice on the same bounded task. If a preferred model is unavailable, use
the next capable tier without waiving any gate.

## Delegation contract

Delegate only when the work is independent and the benefit exceeds context
reconstruction and integration cost. Every worker brief states its role,
allowed scope, ownership, done criteria, evidence format, budget or stop
condition, and permissions. A fresh verifier tries to refute non-trivial claims
and does not silently become the fixer.

## Approval gates

Obtain explicit human authorization before merging a default or integration
branch; applying migrations or destructive data changes; deploying or cutting
over production; performing payment or production user-data writes; or sending
external messages. Also stop before source writes when the user requested
plan-first work or the plan introduces a material decision outside the original
authorization. Approval is scoped to the named action and environment; record
it in the ticket handoff or PR.

## What humans always own

Humans make the final architecture and risk decisions, accept or reject review
findings, authorize sensitive external state changes, and decide whether the
available evidence is sufficient. AI proposes; humans dispose.
