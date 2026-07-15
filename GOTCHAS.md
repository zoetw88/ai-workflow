# Gotchas — the scars behind the workflow

These are not theoretical best practices. They are the failure patterns that
made the workflow necessary.

## "Done" is only a claim

AI can produce a plausible completion narrative before the work is complete. A
clean diff, confident summary, or successful startup is not proof that the
acceptance criteria are satisfied.

**Do instead:** require the evidence block in
[`prompts/verify-done.md`](prompts/verify-done.md): exact commands, results,
paths, and anything that remains unverified.

## Critical paths fail quietly

Messaging, database transactions, authentication, authorization, and payments
can be half-built without crashing immediately. Half-done is worse than
not-done because it looks shippable.

**Do instead:** require integration or smoke evidence through the real
boundary before making a production claim.

## Verify and Review catch different failures

Passing tests can still prove the wrong behavior. A good-looking review can
still miss a broken runtime path.

**Do instead:** Verify first against acceptance criteria, then Review from a
fresh context for correctness, safety, maintainability, and spec alignment.

## Instructions are not enforcement

An instruction that says "always update the handoff" will eventually be
forgotten. The same is true for schemas, security rules, and release steps.

**Do instead:** turn non-negotiable rules into hooks, schemas, tests, permission
boundaries, or CI gates. This repository's
[`scripts/check_close_the_loop.py`](scripts/check_close_the_loop.py) is one
example.

## Parallel writers need isolation

Parallel read-only investigation is useful. Parallel agents editing the same
working tree create races, overwritten changes, and misleading summaries.

**Do instead:** one ticket, one branch, one worktree. Treat every agent report
as a claim until the main session checks the diff.

## Canonical copies drift

Some Claude plugin skills embed tool-agnostic content so the plugin can travel
on its own. Editing only the source or only the embedded copy creates two
different workflows with the same name.

**Do instead:** follow the `Canonical source` header, update both sides, and
bump the plugin version in the same change.

## More documentation can create less context

Hand-written indexes and copied summaries look helpful until they disagree
with reality. Then the agent spends its context deciding which document to
trust.

**Do instead:** give every document one job. Generate maps that are purely
indexes; preserve curated maps; keep current truth in living documents and
decisions in append-only historical documents.

## Where a new gotcha belongs

| Scope | Home |
|---|---|
| reusable across projects | [`pitfalls/`](pitfalls) |
| specific to one repository | that repository's `AGENTS.md` |
| specific to one ticket | `.spec/<ticket>/ai-development-map.md` |
| changes the whole process | [`workflow.md`](workflow.md) |

Detailed pre-write checklists:

- [`pitfalls/go.md`](pitfalls/go.md)
- [`pitfalls/python.md`](pitfalls/python.md)
- [`pitfalls/llm.md`](pitfalls/llm.md)
