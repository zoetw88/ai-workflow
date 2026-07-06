# System map — cross-repo context cache for agents

> Living tier. Agents READ THIS instead of re-exploring every repo at the start of every
> session. Built by `prompts/system-map-scan.md`; PATCHED at close-the-loop whenever a
> change alters anything recorded here. A stale map is a bug — fix it in the same PR that
> made it stale.
> Last full scan: NONE YET — run the kickoff prompt at the bottom of this file.

## Repos

### UIS — <one-line purpose: TBD by scan>

- Local path: `C:\SpringdelWork\Python\UIS`
- Stack: Python (details TBD)
- Entry points: TBD
- Public surface: TBD
- Consumes: TBD
- Workflow docs: TBD
- Gotchas: TBD

### DES — <one-line purpose: TBD by scan>

- Local path: `C:\SpringdelWork\Golang\DES`
- Stack: Go (details TBD)
- Entry points: TBD
- Public surface: TBD
- Consumes: TBD
- Workflow docs: TBD
- Gotchas: TBD

### DLS / device-log-service — <one-line purpose: TBD by scan>

- Local path: `C:\SpringdelWork\Golang\DLS\device-log-service`
- Stack: Go (details TBD)
- Entry points: TBD
- Public surface: TBD
- Consumes: TBD
- Workflow docs: TBD
- Gotchas: TBD

### springdel-windows-service — <one-line purpose: TBD by scan>

- Local path: `C:\SpringdelWork\Golang\Windows\springdel-windows-service`
- Stack: Go (details TBD)
- Entry points: TBD
- Public surface: TBD
- Consumes: TBD
- Workflow docs: TBD
- Gotchas: TBD

## Integration edges

Every edge appears once, verified from BOTH sides (caller code and callee contract).

| From | To | How | Contract lives at |
|------|----|-----|-------------------|
| TBD  |    |     |                   |

## Unconfirmed

(one-sided integration claims land here for human confirmation)

## Shared libraries & conventions

- TBD by scan

---

## Kickoff prompt — paste this into Claude Code on the machine with the repos

```
Read ~/.ai-workflow/prompts/system-map-scan.md and follow its Build procedure to fill in
~/.ai-workflow/system-map.md. The four repos and their local paths are already listed in
the map's skeleton. Spawn all four Explore agents in ONE message. Only record an
integration edge after seeing both sides; put one-sided claims under Unconfirmed. When
done, replace every TBD, stamp today's date on the "Last full scan" line, and commit the
file to ~/.ai-workflow with message "system-map: first full scan".
```
