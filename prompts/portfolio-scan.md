# Prompt: Portfolio scan

Use monthly, before starting a new project (overlap check), or whenever "what should I
work on?" comes up. Produces or refreshes `~/.ai-workflow/portfolio.md` from
`templates/portfolio.md`.

---

## Procedure

1. **List everything (cheap, one call):**

   ```bash
   gh repo list "$(gh api user --jq .login)" --limit 200 \
     --json name,description,pushedAt,isArchived,primaryLanguage \
     --jq 'sort_by(.pushedAt) | reverse'
   ```

   (The `mine` alias in `shell/aliases.sh` is the short form.)

2. **Bucket by recency before reading anything:**
   - pushed < 30 days → candidate `active`
   - pushed 30–180 days → candidate `maintenance` / `paused`
   - pushed > 180 days, not archived → candidate `archive-candidate`
   - `isArchived` → drop from the table entirely

3. **Deep-read ONLY the active bucket** (metadata is enough for the rest):
   - README first paragraph → the "what it does" line
   - last 5 commit subjects + open PR titles → the "current focus" line
   - if the repo follows this workflow: top entry of `devlog.md`, top items of `todo.md`
     → the "next milestone" line

   For many repos, fan out parallel read-only agents — one per repo, report < 100 words
   each (see workflow.md, Parallel agents).

4. **Diff against the existing `portfolio.md`** before overwriting: report rows added,
   rows removed, and status changes. Status downgrades (active → paused,
   anything → archive-candidate) are DECISIONS — surface them, let the human confirm,
   record confirmed ones under "Decisions from recent scans".

5. Write the file, stamp the scan date.

## Rules

- Metadata first. Reading every repo's code on every scan is how the scan stops happening.
- The scan flags archive candidates; it NEVER archives. Archiving is a human decision.
- A `paused` row without a wake-up condition is a lie — either write the condition or
  call it `archive-candidate`.
- Same anti-drift rule as spec-map: regenerate, don't hand-edit.
