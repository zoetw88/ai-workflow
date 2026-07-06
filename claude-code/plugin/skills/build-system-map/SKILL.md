---
name: build-system-map
description: Use when the user wants a cross-repo system map, or when agents keep re-exploring the same repos every session. Scans locally cloned repos in parallel and builds/refreshes a system-map.md recording structure — entry points, public surfaces, integration edges.
---

<!-- Canonical source: ~/.ai-workflow/prompts/system-map-scan.md — if that file exists on
     this machine, read it instead; it may be newer than this embedded copy. -->

The point: pay the cross-repo exploration cost ONCE. Afterwards agents read the map and
verify only what their ticket touches — they do not re-explore N repos every session.

The map records STRUCTURE (what talks to what, where things live), never status, progress,
code, or secrets. It describes the user's own locally cloned repos — ask which repo paths
to scan if not obvious.

## Build procedure (one time, then patch-only)

1. In ONE message, spawn one read-only Explore agent per repo. Each prompt is
   self-contained, asks for exactly the fields below, under 200 words:

   ```
   Explore <path-to-repo>. Report, under 200 words:
   1. One-line purpose (from README + main entry point)
   2. Stack: language, framework, datastore
   3. Entry points: services/jobs/handlers with file paths
   4. Public surface: REST routes / events published / packages exported — where defined
   5. What it consumes: outbound HTTP clients, topics subscribed, shared libs imported
   6. Whether .spec/, devlog.md, todo.md exist
   7. One or two gotchas a new agent must know before editing
   ```

2. Synthesize into `system-map.md` (default location `~/.ai-workflow/system-map.md`,
   or where the user keeps it) using this skeleton:

   ```markdown
   # System map — cross-repo context cache for agents
   > Last full scan: <date>

   ## Repos
   ### <repo> — <one-line purpose>
   - Local path / Stack / Entry points / Public surface / Consumes / Workflow docs / Gotchas

   ## Integration edges
   | From | To | How | Contract lives at |

   ## Unconfirmed
   (one-sided integration claims, for human confirmation)

   ## Shared libraries & conventions
   ```

3. Integration edges: record an edge ONLY after seeing BOTH sides (the caller's client
   code AND the callee's handler/contract). One-sided claims go to `## Unconfirmed`.

4. Keep each repo section under ~15 lines. This is an orientation cache, not documentation.

## Consume rule (what kills re-querying)

Cross-repo task → read the map FIRST, before any Explore fan-out. Spot-verify only the
entry points and edges the ticket touches. Do NOT re-explore repos the ticket doesn't touch.

## Patch rule (keeps the cache honest)

If a change adds/removes/renames anything the map records — an entry point, endpoint,
event, integration edge, shared lib — patch the map in the SAME PR. Map contradicts
reality → the map is stale: fix it in the same PR, never silently work around it.

## Privacy

The finished map is an architecture diagram of the user's systems. It belongs in a
private repo or local disk only — never commit it to anything public.
