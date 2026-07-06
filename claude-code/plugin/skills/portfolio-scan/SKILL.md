---
name: portfolio-scan
description: Use monthly, before starting a new project, or when the user asks "what should I work on" / "what are all my projects doing". Scans the user's own GitHub repos via gh CLI and regenerates a portfolio.md status table.
---

<!-- Canonical source: ~/.ai-workflow/prompts/portfolio-scan.md — if that file exists on
     this machine, read it instead; it may be newer than this embedded copy. -->

Produces or refreshes `portfolio.md` (default `~/.ai-workflow/portfolio.md`) — a
cross-project STATUS table. The repo list comes from whoever is logged into `gh` on this
machine; nothing is hardcoded.

## Procedure

1. **List everything (cheap, one call):**

   ```bash
   gh repo list "$(gh api user --jq .login)" --limit 200 \
     --json name,description,pushedAt,isArchived,primaryLanguage \
     --jq 'sort_by(.pushedAt) | reverse'
   ```

2. **Bucket by recency BEFORE reading anything:**
   - pushed < 30 days → candidate `active`
   - 30–180 days → candidate `maintenance` / `paused`
   - > 180 days, not archived → candidate `archive-candidate`
   - `isArchived` → drop from the table

3. **Deep-read ONLY the active bucket** (metadata suffices for the rest): README first
   paragraph → "what it does"; last 5 commit subjects + open PR titles → "current focus";
   devlog.md / todo.md top entries if present → "next milestone". For many repos, fan out
   parallel read-only agents, one per repo, < 100 words each.

4. **Diff against the existing portfolio.md** before overwriting: report rows added,
   removed, and status changes. Status downgrades (active → paused, anything →
   archive-candidate) are DECISIONS — surface them, let the human confirm, log confirmed
   ones under "Decisions from recent scans".

5. Write the file with this skeleton, stamp the scan date:

   ```markdown
   # Portfolio — what every project is doing
   > Last scan: <date>

   | Repo | What it does (one line) | Status | Current focus | Next milestone | Last push |

   ## Paused projects — wake-up conditions
   ## Decisions from recent scans (newest on top)
   ```

## Rules

- Status vocabulary: `active` / `maintenance` / `paused` / `archive-candidate`.
- A `paused` row without a wake-up condition is a lie — write the condition or call it
  `archive-candidate`.
- The scan flags archive candidates; it NEVER archives. Archiving is a human decision.
- Regenerate, don't hand-edit — hand-edited generated files drift.
