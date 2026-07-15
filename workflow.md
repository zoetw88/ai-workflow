# The 6-stage workflow

Based on Addy Osmani's agent-skills, simplified.

## Stages

1. **Define** — Grill the user. Produce `.spec/current.md`.
2. **Plan** — Break the spec into atomic tasks. Produce `.spec/tasks.md`.
3. **Build** — Implement one task at a time, in an isolated worktree (see Workspace isolation). TDD. One commit per task.
4. **Verify** — Run tests. Tests are proof. Verify is NOT review. Before claiming done, produce the evidence block from `prompts/verify-done.md`.
5. **Review** — Independent reviewer (fresh context). Check spec conformance + AI smells.
6. **Ship** — Commit message, PR description, ADR if architectural. Run the close-the-loop checklist (see Context discipline) before opening the PR.

## Workspace isolation (git worktrees)

Build happens on a dedicated branch in a dedicated worktree — never on the main checkout:

```bash
git worktree add ../<repo>-<ticket> -b <ticket>    # or: wt <ticket> (shell/aliases.sh)
```

- **Verify the baseline is green BEFORE writing anything.** Run the test suite in the fresh
  worktree first. If it's already red, that's an `environment blocker` or `test defect` to
  report (see Blockers) — not something to "fix along the way". A red baseline blamed on new
  code is a classic time sink.
- One ticket = one branch = one worktree. Parallel tickets never share a working directory.
- Remove the worktree at Ship, after the PR is opened: `git worktree remove ../<repo>-<ticket>`.

`scripts/start-task.ps1` offers to create the worktree during ticket intake.

## Context discipline (two-tier docs)

Docs split into two tiers. The split is what keeps a coding agent aligned across sessions
without anyone having to remember to update things.

- **Living tier** — must always reflect the current state:
  - `.spec/<ticket>/current.md` (the spec / current truth), `.spec/<ticket>/tasks.md`
  - project-level `devlog.md` + `todo.md` (one rolling file each, spanning all tickets)
- **Historical tier** — append-only, may diverge from reality, used to trace context:
  - `.spec/<ticket>/audit.md`, `.spec/<ticket>/adr-*.md`
  - To overturn a decision, write a NEW ADR and mark the old one `Superseded by ADR-NNNN` — never edit its body.

`current.md` IS the spec: a behavior-affecting change updates it; an implementation-only
decision goes to an ADR only.

### Read first (Define / Plan)

Before proposing an approach: read `current.md` + every settled ADR for the ticket (and the
latest `devlog.md` entries), and state which docs you consulted. If the approach conflicts
with a recorded decision, STOP and flag it immediately — do not defer to Review. The user
decides: honor the past decision, or update the docs because the new requirement supersedes it.

Cross-repo task → also read `~/.ai-workflow/system-map.md` FIRST, before any Explore
fan-out. Spot-verify only the entry points and edges the ticket touches; do NOT re-explore
repos the ticket doesn't touch. If the map contradicts reality, the map is stale — fix that
line in the same PR (see `prompts/system-map-scan.md`).

### Close the loop (before opening a PR)

1. Update every living-tier doc the change touched (`current.md`, `tasks.md`).
2. Append a newest-on-top entry to project `devlog.md`, linking back to the ticket's spec/ADR.
3. Refresh `todo.md`.
4. If the change added/removed/renamed an entry point, public endpoint, event, integration
   edge, or shared lib, patch `~/.ai-workflow/system-map.md` too.
5. Commit the doc updates into the SAME PR as the change.

Steps 1–4 are mechanically enforced at push time by
`scripts/check_close_the_loop.py` (wired via `templates/pre-commit.template.yaml`,
pre-push stage): a push that changes code without touching any living-tier doc is
rejected. Escape hatch for intentional exceptions: `CLOSE_THE_LOOP=skip git push`.

### Project type

Each project declares `Project type: personal | team` at the top of its `CLAUDE.md` / `AGENTS.md`:

- `personal` → `devlog.md` + `todo.md` are mandatory every session.
- `team` → they follow the team's convention; skip until the team has adopted them.

Templates: `~/.ai-workflow/templates/{devlog.md,todo.md,CLAUDE.md.template,AGENTS.md.template}`.

### Spec map (optional, threshold + generated)

A `spec-map.md` indexes the `.spec/` areas. It earns its place only when there are many areas:

- **Add it only when `.spec/` has > 8 areas.** Below that, `current.md` + `tasks.md` are enough;
  a small project does not need a third index that can drift.
- **Generate it, do not hand-maintain it.** A hand-written index goes stale — the exact problem
  the two-tier model exists to prevent. Run `~/.ai-workflow/scripts/build-spec-map.ps1` and
  re-run it as part of close-the-loop so the map never drifts from the folders on disk.
- Keep the three index roles distinct: `current.md` = current truth/spec; `spec-map.md` =
  navigation index of all areas; `ai-development-map.md` = per-ticket handoff read-order.

### Portfolio (cross-project, generated)

Above the per-repo indexes sit two more zoom levels — the index hierarchy is:

- `~/.ai-workflow/system-map.md` — STRUCTURE across all repos: what each repo does, entry
  points, public surfaces, integration edges. The agent-facing context cache — built once
  by `prompts/system-map-scan.md`, patched at close-the-loop, so agents stop re-exploring
  every repo every session (template: `templates/system-map.md`)
- `~/.ai-workflow/portfolio.md` — STATUS across all projects: what's active, current focus,
  next milestone. Human-facing (template: `templates/portfolio.md`)
- `<repo>/spec-map.md` — areas within one repo
- `.spec/<ticket>/ai-development-map.md` — read-order within one ticket

`portfolio.md` is generated by the gh-CLI scan in `prompts/portfolio-scan.md` — same
anti-drift rule as spec-map: regenerate, don't hand-edit. Refresh monthly, before starting
a new project (overlap check), or when deciding what to work on next. Status downgrades and
archiving are human decisions; the scan only flags them.

Team-scale alternative: a GitHub Projects (v2) org-level board pulls issues from many repos
into one roadmap/timeline view — the right tool when several humans need the same picture.
For a solo dev working with agents, a generated markdown file wins: agents read files, not UIs.

The generator is a **drift detector and a new-project starter, not a replacement tool**:

- **New large project** (no map yet): generate the first `spec-map.md`, then hand-add grouping.
- **Existing curated map**: do NOT overwrite it. Run `build-spec-map.ps1 -DryRun` and diff the
  output against the current map to catch areas added/removed on disk but missing from the map.
- **Never regenerate a `spec-map.md` that carries more than a Spec Areas table** (extra sections
  like release state / policies, or one referenced by tests) — the script would destroy those
  sections and can break CI. Update such maps by hand.

## Blockers and pitfalls

When execution is blocked, classify the blocker before concluding anything:

- `code defect`
- `test defect`
- `environment blocker`
- `dependency blocker`

For any non-code blocker, report:

- `blocker_type`
- `blocker_area`
- `observed_error`
- `impact`
- `next_action_needed`
- `fallback_path`

If a blocker is solved and the workaround is likely reusable, ask the user whether to capture it as a pitfall. If they say yes, record it in the appropriate layer:

- global reusable pitfall -> `~/.ai-workflow/pitfalls/`
- repo-specific pitfall -> local repo workflow notes
- ticket-specific pitfall -> `.spec/<ticket>/ai-development-map.md`

## The rule

**Verify ≠ Review.** Verify answers "does it work?"; review answers "is it good?".
Most teams collapse them. Don't.

## Parallel agents

If the current tool supports subagents, use them as isolated workers with
self-contained prompts and independent context. The orchestrator should receive
short final reports rather than every raw search result. Claude Code, Codex, and
other agent tools expose different APIs for this; parallelism is an optimization,
not a requirement for the workflow.

### Use parallel agents for

| Stage | Parallel pattern | Why |
|---|---|---|
| **Define** (audit-heavy) | N × read-only explorers, each on a different code area | Reduces wall-clock time without mixing raw context |
| **Review** | fresh reviewer + separate security / performance lenses | Different contexts do not share the same blind spots |
| Investigation / spec gap-finding | one read-only worker per repo or concern | Independent context produces independent conclusions |
| Verifying a non-trivial claim | second-opinion worker while the main agent continues unrelated work | Cheap insurance when the claim matters |

### Do NOT use parallel agents for

- Sequential TDD (red → green → refactor — needs same context)
- One-task-one-commit Build cycles (single builder, no fan-out)
- Anything requiring a user decision mid-stream
- Single-file edits where main session is faster anyway
- Verify (one test runner, deterministic)
- Ship (linear: commit → PR → ADR)

### How to call them well

- **Dispatch independent calls concurrently.** Use the tool's actual parallel mechanism; sequential calls do not become parallel because the prompts look similar.
- **Each prompt is self-contained.** The agent has no view of main-session history. Include file paths, the question, and what form the answer should take.
- **Cap each agent's report length.** Long reports refill main context — defeats the purpose. "Report in under 200 words" is a fair default.
- **Pick the right role and permissions, not a product-specific agent name.**
  - read-only explorer — file discovery and bounded code search
  - research / planning worker — multi-step investigation with no writes
  - builder — one specified implementation slice in an isolated worktree
  - tester / reviewer — deterministic verification or a fresh judgment context
- **Trust but verify.** Agent summaries describe intent, not always reality. If an agent claimed to edit files, check the diff yourself before reporting work as done.
- **Don't duplicate work.** If you delegated research to an agent, do NOT also grep / read the same files — your job during the wait is something else (write the next test, draft the spec, prep the review checklist).

### Audit pattern (concrete example)

For a wide cross-repo audit, dispatch concurrently:

```
Worker 1 (read-only): audit Repo-A for <pattern> — under 200 words
Worker 2 (read-only): audit Repo-B for <pattern> — under 200 words
Worker 3 (read-only): audit Repo-C for <pattern> — under 200 words
Worker 4 (read-only): cross-reference shared library usage — under 200 words
```

Then synthesize the four reports into `.spec/<ticket>/audit.md`.

This is the move I should have made on a real cross-repo audit ticket — instead I serially grepped each repo, which worked but took ~4× longer and pulled raw results into main context.

### Review depth scales with risk

Default is **one reviewer** (fresh context, `prompts/review-checklist.md`). A full multi-lens
panel on every diff burns tokens without reliably adding findings on low-risk changes.

Escalate to the 3-lens panel below only when the diff touches:

- auth / permissions / session handling
- money, transactions, or data migrations
- concurrency or caching
- public API contracts

Same list as PHILOSOPHY.md's "half-done is worse than not-done" categories — the ones that
already demand integration tests get the panel; everything else gets one reviewer.

### Review pattern (3-lens panel, high-risk diffs only)

After Build is complete, in one message spawn:

```
Worker A (fresh reviewer): spec-conformance review against .spec/current.md
Worker B (security lens): OWASP top-10 review of the diff
Worker C (performance lens): DB queries, N+1, hot paths
```

Three independent reports = three independent blind spots covered.
Human reads all three, decides what to accept.

## Model routing: one workflow, different autonomy

Do not maintain separate strong-model and weak-model workflows. Every model must
meet the same acceptance criteria, verification, review, and evidence gates. Model
capability changes task shape and autonomy, not the definition of done.

| Stage | Default capability | Why |
|---|---|---|
| **Define** | strongest reasoning available | resolve ambiguity, constraints, and failure modes |
| **Plan** | strongest reasoning available | make architecture and dependency order explicit |
| **Build** | general coding model | the spec should reduce the work to one atomic slice |
| **Verify** | fast / low-cost model or deterministic runner | execute known commands and report exact output |
| **Review** | strongest reasoning available, fresh context | challenge the implementation and reconcile evidence |
| **Ship** | fast / low-cost model | assemble status, commit, and PR evidence; human owns release approval |

These are defaults, not brand mappings. Provider model names, prices, and aliases
change faster than this workflow should. Choose the current model that matches the
capability profile in the provider you are actually using.

### How the operating style changes

- **Fast / lower-capability model:** give exact files, one bounded question, an
  output schema, and read-only permissions by default. Do not delegate architecture,
  security decisions, or cross-cutting writes.
- **General coding model:** give one accepted task, the relevant spec slice, the
  allowed change surface, and the exact verification command.
- **Strongest reasoning model:** give the broader decision context for ambiguous or
  high-risk work, but still require tests, independent review, and evidence.

Escalate one tier when requirements remain ambiguous, a decision crosses system
boundaries, the diff touches auth / money / migrations / concurrency / public APIs,
evidence conflicts, or the current model fails twice on the same bounded task. A
stronger model may inspect a wider context; it may never waive a gate.

## What humans always own

- Architectural decisions
- Security-sensitive code
- Performance / cost trade-offs
- Production deployments
- Final accept/reject on review findings

AI proposes. Humans dispose.
