---
name: verify-done
description: Use before claiming any task, feature, or fix is complete. Produces an evidence block mapping every acceptance criterion to file:line references or a same-session test run. Never round up.
---

<!-- Canonical source: ~/.ai-workflow/prompts/verify-done.md — if that file exists on this
     machine, read it instead; it may be newer than this embedded copy. -->

Before you say "done", produce this evidence block. If you cannot fill a line with a file
path, line number, or a test run from THIS session, the honest status is "not verified" —
go check, then report.

```
Verified:
  ✅ <criterion> → <file:line> (commit <hash>)
  ✅ <criterion> → <test name> passed: <pasted summary line from the run>
  ❌ <criterion> → not found / not implemented
Unverified:
  - <criterion> — <why it wasn't checked>
```

Rules:

1. Walk EVERY acceptance criterion in `.spec/<ticket>/tasks.md` (or the task list you were
   given). Unchecked items are reported as ❌ or Unverified — never silently dropped.
2. "Tests pass" means you ran them after your last edit and paste the summary line.
   A green run from before the last change proves nothing.
3. Kafka / DB-transaction / auth work: an integration test must pass before claiming done.
   Unit tests alone don't count for these categories.
4. If an agent (including you) claims it edited files, check `git diff --stat` before
   reporting the work as done. Claims describe intent, not always reality.
5. Partial is a valid answer. "4 of 6 criteria verified, 2 open" beats a "done" that
   unravels in review.
