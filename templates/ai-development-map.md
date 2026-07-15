# <ticket> AI development map

This file is the handoff entry point for Codex, Claude, and helper agents working on the same ticket.

## Authoritative sources

Read these in order before changing code:

1. `<master spec path>`
2. `<repo task list path>`
3. `<repo audit path>`
4. `<deferred or sub-task path if any>`

## Current scope

Summarize the current parent-ticket or task scope:

1. 
2. 
3. 

## Implementation files

### Production

- 

### Tests

- 

### Call sites or integration points

- 

## Verification checkpoints

1. For new or fixed behavior, confirm a narrow test exists and capture the
   correct failure before implementation when a test harness is available.
2. For docs, configuration, or generated data, name the relevant validator.
3. Implement the smallest accepted change.
4. Re-run the narrow test or validator.
5. Run broader verification proportional to the touched area and risk.

## Verification commands

```text
ruff check ...
pytest <narrow target>
pytest <broader target>
```

## Known blockers

- 

## Pitfall capture

- ask_to_capture_as_pitfall:
- pitfall_status:
- pitfall_target:
- pitfall_note:

## Out of scope

- 

## Git hygiene

Do not stage:

- local worktrees
- cache files
- unrelated untracked files

## Handoff notes

- 
