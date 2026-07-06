# Prompt: System-map scan

Use ONCE to build `~/.ai-workflow/system-map.md` (from `templates/system-map.md`), and
again only after large architectural changes. Day-to-day the map is kept fresh by the
close-the-loop patch rule, not by rescanning.

The point: pay the cross-repo exploration cost ONE time. Afterwards agents read the map
and verify only what their ticket touches — they do not re-explore N repos every session.

---

## Build procedure (one time)

1. In ONE message, spawn one read-only `Explore` agent per repo. Each prompt is
   self-contained and asks for exactly the template fields, under 200 words:

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

2. Synthesize into `system-map.md`. Integration edges: only record an edge after seeing
   BOTH sides (the caller's client code AND the callee's handler/contract). One-sided
   claims go to a `## Unconfirmed` section for the human.

3. Stamp the scan date.

## Consume rule (Define / Plan — this is what kills re-querying)

- Cross-repo task → read `system-map.md` FIRST, before any Explore fan-out.
- Only spot-verify what the ticket touches: the specific entry points and edges you're
  about to change (paths still exist, signatures still match). Do NOT re-explore repos
  the ticket doesn't touch.
- Map contradicts reality → the map is stale: fix the map line in the same PR, and note
  it in the devlog. Don't silently work around it — that's how caches rot.

## Patch rule (close-the-loop)

Before opening a PR, if the change added/removed/renamed anything the map records —
an entry point, a public endpoint, an event, an integration edge, a shared lib — patch
`system-map.md` in the SAME PR. Same discipline as `current.md`.

## Scope

- The map records STRUCTURE (what talks to what, where things live), not status or
  progress — status lives in `portfolio.md`, progress in each repo's devlog/todo.
- Keep each repo section under ~15 lines. This is a cache for orientation, not
  documentation — an agent needing more detail goes to the repo AFTER orienting.
