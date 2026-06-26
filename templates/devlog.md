# Devlog

> Project-level. One rolling file spanning ALL tickets. **Newest entry on top.**
> Historical tier: append-only, never rewrite past entries.
> Updated at close-the-loop (before each PR). Personal projects: mandatory.
>
> Purpose:縱向歷史 — answer "what shipped when, why, and which decision it ties to",
> so a future session can trace a bug back to the version/spec/ADR that introduced it.

<!-- Copy the block below to the TOP for each session. Keep entries short. -->

## YYYY-MM-DD — <ticket> <one-line what>

- **What**: <what changed, in behavior terms>
- **Why**: <the driver — requirement, bug, decision>
- **Spec/Plan**: [.spec/<ticket>/current.md](.spec/<ticket>/current.md) (<which section / AD-n>)
- **ADR**: [.spec/<ticket>/adr-NNNN.md](.spec/<ticket>/adr-NNNN.md) (if any)
- **Commits**: <short SHAs>
- **Continues**: <prior session/date this builds on, or "new">
- **Notes**: <gotchas, deferred items, follow-ups>

---

## 2026-01-01 — EXAMPLE-1 set up project skeleton

- **What**: initial CLAUDE.md / AGENTS.md, `.spec/` layout, devlog + todo
- **Why**: adopt the read-first / close-the-loop workflow
- **Spec/Plan**: [.spec/EXAMPLE-1/current.md](.spec/EXAMPLE-1/current.md)
- **ADR**: —
- **Commits**: abc1234
- **Continues**: new
- **Notes**: delete this example entry once real work starts
