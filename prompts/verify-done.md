# Prompt: Verify done

Use before claiming ANY task or feature is complete. This is the operational form of
PHILOSOPHY.md #1 (evidence over memory) and #3 (never round up).

---

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

1. Walk EVERY acceptance criterion in `.spec/<ticket>/tasks.md`. Unchecked items are
   reported as ❌ or Unverified — never silently dropped.
2. "Tests pass" means you ran them after your last edit and paste the summary line.
   A green run from before the last change proves nothing.
3. Kafka / DB-transaction / auth work: an integration test must pass before claiming done.
   Unit tests alone don't count for these categories.
4. If an agent (including you) claims it edited files, check `git diff --stat` before
   reporting the work as done. Claims describe intent, not always reality.
5. Partial is a valid answer. "4 of 6 criteria verified, 2 open" beats a "done" that
   unravels in review.
