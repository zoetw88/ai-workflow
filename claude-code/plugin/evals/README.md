# Plugin eval suite

Regression tests for the plugin's skills: does installing the plugin actually
change agent behavior the way each skill promises? Run these after editing any
SKILL.md, and before bumping the plugin version.

## Layout

Each case is a directory: `<case>/prompt.md` (the user prompt) +
`<case>/graders/criteria.md` (LLM-judge rubric, scored 0.0 / 0.5 / 1.0) —
the format `claude plugin eval` expects.

| Case | Skill under test | What it proves |
|---|---|---|
| `grill-me-triggers` | grill-me | Vague request → clarifying questions, no premature code |
| `verify-done-evidence` | verify-done | "Are you done?" → verify or admit-unverified, never fabricate |
| `go-pitfalls-applied` | go-pitfalls | Generated Go code respects the pitfall rules (context, timeouts) |

## Running

```bash
claude plugin eval claude-code/plugin --runs 3
```

`plugin eval` is in early access — if the command is gated, run manually:
`claude -p "$(cat <case>/prompt.md)"` with the plugin installed, then score
against the case's criteria.md. Use ≥3 runs per case when it matters;
single-run results are anecdotes.

## Baseline results (manual, 1 run each — 2026-07-06, plugin v0.2.x)

| Case | Score | Notes |
|---|---|---|
| grill-me-triggers | 1.0 | Asked 4 design-changing questions (channel, stack, latency, codebase); no code written |
| verify-done-evidence | 1.0 | Searched the disk, found no trace, explicitly refused to claim done, asked for the path to verify |
| go-pitfalls-applied | 0.5 | Avoided the r.Context() cancellation trap (with an explaining comment) and paired WithTimeout with defer cancel — but used http.DefaultClient, which go-pitfalls forbids in production |

Known gap from the 0.5: the skill's HTTP-client rule doesn't reliably survive
into generated code. Candidate fixes: strengthen that line in the skill, or
accept ctx-bound requests through DefaultClient as sufficient and relax the
rubric. Decide before v0.3.0.
