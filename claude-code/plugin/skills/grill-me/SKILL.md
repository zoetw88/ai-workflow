---
name: grill-me
description: Clarify consequential unresolved requirements after checking existing context; ask only necessary questions and continue independent work.
---

When a request is under-specified, first inspect available context and contracts.
Ask about consequential gaps without reopening settled decisions or imposing a
question quota. A vague request alone does not require stopping all useful work.

## Process

1. Read the request, prior decisions, repository contracts, and relevant task docs.
2. Identify consequential unknowns that cannot be resolved from those sources.
3. Ask the minimum necessary questions using the available question tool; do not repeat answers or approvals already given.
4. Continue independent work while waiting. Defer work that depends on a required answer; elapsed time is not an answer or approval.
5. If no consequential unknown remains, proceed. Use established contracts for routine choices and state material assumptions; do not invent product or data-loss guarantees.

## What makes a good clarifying question

- It has at least 2 plausible answers
- Each answer would lead to different code
- It's not asking the user to do your design work for you

## Question categories to consider

- **Scale**: How many users / requests / records? p99 latency budget?
- **Failure modes**: What happens when upstream fails? Partial data?
- **Boundaries**: Who calls this? Who can call this? Auth model?
- **Lifecycle**: How is data created / updated / deleted / archived?
- **Concurrency**: Multiple writers? What conflict resolution?
- **Constraints**: Existing tech you must use? Things you must NOT use?
- **Definition of done**: What does "working" mean to you?

## Example

User: "I want to add notifications"

Bad response: "I'll add a notification system using websockets."

Good response:

> Before I build this, a few things will change the design a lot:
>
> 1. **What triggers a notification?** Specific events (order placed)
>    or arbitrary admin push?
> 2. **Where should it land?** In-app only, or also email / SMS / push?
> 3. **Latency requirement?** Within seconds (websocket), or "next time
>    they open the app" is fine (poll)?
> 4. **Volume?** 10/day per user or 10k/day?
> 5. **Read state?** Does "read vs unread" matter, or fire-and-forget?
>
> Once I know these, I can propose something concrete.

## When to skip this skill

- The request is genuinely simple (one-line change)
- The user has already provided a clear spec
- The user explicitly says "just do X" with full context
