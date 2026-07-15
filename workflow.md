# The 6-stage workflow

Influenced by [Addy Osmani's agent-skills](https://github.com/addyosmani/agent-skills),
then adapted around evidence, proportional controls, and durable handoffs.
Role contracts and fresh-context refutation also draw on the MIT-licensed
[pilotfish design](https://github.com/Nanako0129/pilotfish/blob/main/docs/design.md).

## Stages

1. **Define** — Turn the request into scope, constraints, non-goals, and
   acceptance criteria in `.spec/<ticket>/current.md`. Each criterion should
   name an **Observable** result, **Environment**, and exact **Verify** command
   or manual step. Ask only questions that change the result or authorization.
2. **Plan** — Break the accepted spec into atomic, dependency-ordered tasks in
   `.spec/<ticket>/tasks.md`. Each task names its change surface and verification.
3. **Build** — Implement one accepted slice at a time on a feature branch. Use
   test-first development for new or fixed behavior when a test harness exists;
   use the relevant validator for documentation, configuration, and generated data.
4. **Verify** — Run the relevant checks and record exact commands, output, and
   environment. A local pass is local evidence; it is not production-derived proof.
5. **Review** — Use fresh context to check spec conformance, correctness, and the
   risks the diff actually introduces. Fix and reverify findings, or record the
   human decision that explicitly accepts them.
6. **Ship** — Close the loop, create a cohesive commit and PR, and report what was
   and was not verified. Ship prepares integration; it does not authorize merge,
   migration, deployment, or another external state change.

## Proportional workspace isolation

Every write belongs on a feature branch. Add a dedicated worktree when the task
is non-trivial, parallel work is active, or the shared checkout must stay stable:

```bash
git worktree add ../<repo>-<ticket> -b <ticket>    # or: wt <ticket> (shell/aliases.sh)
```

- Before editing, inspect `git status` and preserve unrelated user changes.
- For a behavior change, run the narrow relevant baseline before writing. If it
  is already red, classify the failure instead of fixing it incidentally.
- A clean feature branch is enough for a bounded documentation or low-risk
  single-file change. Do not create process overhead that adds no isolation.
- Parallel writers never share a working directory; give each one a worktree.
- Remove a task worktree after its PR is opened and its state is recoverable:
  `git worktree remove ../<repo>-<ticket>`.

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

1. Update the ticket's `current.md` and `tasks.md`.
2. For personal projects, update newest-on-top `devlog.md` and `todo.md`.
3. Patch `~/.ai-workflow/system-map.md` when a recorded entry point, public surface, integration edge, or shared library changed.
4. Commit repository doc updates in the same PR as the change.

`scripts/check_close_the_loop.py` can be wired at pre-push through `templates/pre-commit.template.yaml`. In **WIP mode**, it rejects code without a
touched ticket document and checks the ticket pair, required headings, and placeholders;
unchecked work remains valid. In **Ship mode**, any change outside the living tier,
including canonical Markdown, requires changed `current.md` and `tasks.md` from the same
ticket, no unchecked items, and personal-project `devlog.md` plus `todo.md`; CI pins project type so a PR cannot disable that policy. Weak acceptance wording emits a warning when Observable,
Environment, or Verify fields are missing; the warning does not fail either mode.
The guard is intentionally narrow: it validates structure, not truth. It cannot prove
that evidence is sufficient, prose is accurate, or the private system map is current.
Review those obligations before Ship. Escape hatch: `CLOSE_THE_LOOP=skip git push`.

### Project type

Each project declares `Project type: personal | team` at the top of its
`AGENTS.md` or thin tool-specific shim:

- `personal` → `devlog.md` + `todo.md` are required for non-trivial tracked
  tasks; a trivial doc correction does not need synthetic history.
- `team` → they follow the team's convention; skip until the team has adopted them.

Templates: `~/.ai-workflow/templates/{devlog.md,todo.md,CLAUDE.md.template,AGENTS.md.template}`.

Detailed rules for `spec-map.md`, `system-map.md`, `portfolio.md`, and their
generators live in [context-management.md](context-management.md). Keep this
file focused on the execution loop.

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
- `last_successful_command`
- `working_directory`
- `required_environment_or_input`

If a blocker is solved and the workaround is likely reusable, ask the user whether to capture it as a pitfall. If they say yes, record it in the appropriate layer:

- global reusable pitfall -> `~/.ai-workflow/pitfalls/`
- repo-specific pitfall -> local repo workflow notes
- ticket-specific pitfall -> `.spec/<ticket>/ai-development-map.md`

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
| **Review** | fresh reviewer + risk-specific specialist lenses | Different contexts do not share the same blind spots |
| Investigation / spec gap-finding | one read-only worker per repo or concern | Independent context produces independent conclusions |
| Verifying a non-trivial claim | second-opinion worker while the main agent continues unrelated work | Cheap insurance when the claim matters |

### Do NOT use parallel agents for

- A sequential test-first cycle (red → green → refactor needs the same context)
- Multiple writers touching the same files or depending on uncommitted output
- Anything requiring a user decision mid-stream
- Single-file edits where main session is faster anyway
- One deterministic verification command; independent verification surfaces may
  run in parallel when their outputs stay separate
- Ship (linear: commit → PR → ADR)

### How to call them well

- **Dispatch independent calls concurrently.** Use the tool's actual parallel mechanism; sequential calls do not become parallel because the prompts look similar.
- **Each prompt is a bounded role contract.** Include the phase and role,
  allowed scope, exclusive ownership, constraints, done criteria, evidence
  format, permissions, and budget or stop condition. A fresh worker does not
  inherit the main conversation unless the tool explicitly says it does.
- **Cap each agent's report length.** Long reports refill main context — defeats the purpose. "Report in under 200 words" is a fair default.
- **Pick the right role and permissions, not a product-specific agent name.**
  - read-only explorer — file discovery and bounded code search
  - research / planning worker — multi-step investigation with no writes
  - builder — one specified implementation slice in an isolated worktree
  - tester / reviewer — deterministic verification or a fresh judgment context
- **Trust but verify.** Agent summaries describe intent, not always reality. If an agent claimed to edit files, check the diff yourself before reporting work as done.
- **Do not repeat the whole delegated exploration.** Continue independent work
  during the wait, then spot-check load-bearing claims, the final diff, and the
  evidence before using the report.
- **Keep verification independent.** A verifier tries to refute the claim and
  reports before fixing anything. The orchestrator or an authorized builder
  owns the patch and reruns affected verification.

For a concrete fan-out and synthesis template, use
[`prompts/parallel-audit.md`](prompts/parallel-audit.md).

### Review depth scales with risk

Default is **one reviewer** with fresh context
(`prompts/review-checklist.md`). Multiple reviewers on every diff burn tokens
without reliably adding findings on low-risk changes.

Add only the relevant review lenses when the diff touches:

- auth / permissions / session handling
- money, transactions, or data migrations
- concurrency or caching
- public API contracts
- production operations, availability, or material cost

Same list as PHILOSOPHY.md's "half-done is worse than not-done" categories — the ones that
already demand integration tests get deeper review; everything else gets one reviewer.

### Review pattern (risk-specific, high-risk diffs only)

After Build, select the smallest useful panel. For example:

```
Worker A (fresh reviewer): spec conformance against .spec/<ticket>/current.md
Worker B (security, when relevant): trust boundaries, auth, injection, secrets
Worker C (data integrity, when relevant): transactions, retries, migrations
Worker D (performance, when relevant): queries, N+1, hot paths, cost
Worker E (compatibility, when relevant): public API and rollout behavior
```

The human reads the reports, rejects or accepts each finding, and requires
reverification after any fix. Do not spawn a specialist whose risk is absent.

## Model routing: one workflow, different autonomy

Do not maintain separate strong-model and weak-model workflows. Every model
must meet the same acceptance criteria, verification, review, and evidence
gates. Model capability changes task shape and autonomy, not the definition of
done.

Use a **general coding model by default** for bounded Define, Plan, Build, and
Review work. Prefer deterministic tools over a model for Verify; use a fast
model only to classify or summarize exact output. A fast model can also prepare
routine Ship metadata, but it cannot grant approval.

Escalate to the strongest reasoning tier only when ambiguity, risk, scope, or
conflicting evidence requires broader judgment. These are capability profiles,
not brand mappings: provider names and prices change faster than this workflow.

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

If the preferred model is unavailable, use the next capable tier, shrink the
task if necessary, and preserve every acceptance and evidence gate. Bind model
names in tool adapters or role definitions, not in this canonical policy.

## Approval gates

An agent may prepare plans, diffs, migration commands, release notes, or a PR,
but it must obtain explicit human authorization before it performs:

- a merge into the repository's default or integration branch
- a database migration, destructive operation, or irreversible data change
- a production deployment, traffic cutover, or infrastructure mutation
- a payment action or a write involving production user data
- an external message, publication, or other action on the user's behalf

Also stop before source writes when the user explicitly requested plan-first
work, or when the proposed plan introduces a material architecture, scope, or
risk decision that the original request did not authorize.

Approval is scoped to the named action and environment. Permission to open a PR
does not imply permission to merge it; permission to deploy staging does not
imply permission to deploy production. Record the approved action, environment,
and approver in the ticket handoff or PR.

## What humans always own

- Architectural decisions
- Security-sensitive code
- Performance / cost trade-offs
- Production deployments
- Final accept/reject on review findings

AI proposes. Humans dispose.
