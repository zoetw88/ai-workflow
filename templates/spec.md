# <Feature name>

## Goal
<Why this exists, the observable outcome, and the ticket link.>

## Scope

### In
- ...

### Out
- ...

## Acceptance criteria

Use one block per criterion. Missing fields produce a warning so old or draft
specs stay workable; Ship still requires every checkbox to be complete.

- [ ] Observable: <result a reviewer can see or measure>
  - Environment: <local, CI, staging, production, or named device>
  - Verify: <exact command or numbered manual steps>

## Interface

### Input
<shape, validation rules>

### Output (success)
<shape>

### Output (errors)
| Condition | HTTP / error code | Body |
|-----------|-------------------|------|
|           |                   |      |

## Invariants
- <thing that must always hold true>

## Test cases (exhaustive, natural language)

### Happy path
- ...

### Edge cases
- Empty input → ...
- Oversized input → ...
- Malformed input → ...

### Failure modes
- Downstream returns 5xx → ...
- Network timeout → ...

### Concurrency
- Two concurrent identical calls → ...

## Non-goals
<What this explicitly does NOT do>

## Dependencies
- Internal services: ...
- External APIs: ...
- DB tables: ...

## Risks
- <risk> → mitigation

## Self-review (30 seconds, before handing off to Plan)

Each "no" goes back into the spec above — not into a mental note.

- [ ] Every test case is falsifiable (a command or observable behavior can prove it)
- [ ] Every acceptance criterion names Observable, Environment, and Verify evidence
- [ ] Scope Out + Non-goals actually exclude something (empty = scope not thought through)
- [ ] No conflict with settled ADRs for this area (checked, not assumed)
- [ ] Error table covers every external dependency listed under Dependencies
- [ ] Invariants are checkable in a test, not aspirational
