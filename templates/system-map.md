# System map — cross-repo context cache for agents

> Living tier. The live copy belongs at `~/.ai-workflow/system-map.md`.
> Purpose: agents READ THIS instead of re-exploring every repo at the start of every
> session. Generated once by `prompts/system-map-scan.md`; PATCHED at close-the-loop
> whenever a change alters anything recorded here. A stale map is a bug — fix it in
> the same PR that made it stale.
> Last full scan: YYYY-MM-DD

## Repos

### <owner/repo> — <one-line purpose>

- Local path: <where it's cloned>
- Stack: <language / framework / datastore>
- Entry points: <services, jobs, handlers — file paths>
- Public surface: <REST endpoints / events published / packages exported — where defined>
- Consumes: <what it calls or subscribes to — which repo or external system, via what>
- Workflow docs: <.spec/ present? devlog.md / todo.md present?>
- Gotchas: <repo-specific traps an agent must know BEFORE touching this repo>

### <owner/repo-2> — ...

## Integration edges

Every edge appears once here, verified from BOTH sides (caller code and callee contract).

| From | To | How | Contract lives at |
|------|----|-----|-------------------|
| <repo-A> | <repo-B> | REST `POST /api/...` | <path to handler + path to client> |
| <repo-B> | <repo-C> | Kafka topic `<name>` | <producer path + consumer path> |

## Shared libraries & conventions

- <lib/module>: used by <repos>; source of truth at <repo/path>
- <convention>: <e.g. error envelope format, auth header, tenant id propagation>
