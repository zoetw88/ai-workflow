---
name: grill-me
description: Use when a feature request is vague or under-specified. Ask 3-7 targeted clarifying questions before proposing any solution or writing any code.
---

The user has given you a vague or under-specified request. **Do not
propose a solution yet.** First, grill them with targeted questions.

## Process

1. Read the request. Identify the ambiguities.
2. Pick 3-7 questions that, when answered, would change the design.
3. Ask them, structured as a numbered list.
4. Wait for answers.
5. THEN propose.

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
