# Philosophy

Six principles that shape how I work with AI agents.

---

## 1. Never trust "done" from memory — produce evidence

When you (or the AI) claim something is implemented or fixed, the
honest answer is one of these:

```
Verified via grep/Read:
  ✅ <criterion> → <file:line> (commit <hash> if known)
  ❌ <criterion> → not found
```

If you can't produce file paths and line numbers, the answer is
"I don't know yet, let me check" — then go check.

**Why this rule exists.** Conversations drift. Recent tool calls
dominate attention. Older work fades. Without evidence, "I think
I did that" becomes "I definitely did that" within five turns.

---

## 2. Multi-part tasks → write acceptance criteria *first*

The moment a task has more than one moving piece, before any code
gets written, draft a checklist:

```markdown
## Task: <name>
- [ ] <atomic criterion 1>
- [ ] <atomic criterion 2>
- [ ] <atomic criterion 3>
```

Then tick items off with commit hashes as you go. When someone asks
"done?" — read the file. Your memory is a guess.

---

## 3. Before saying "done" on a full task

Walk through every unchecked item. Anything unchecked → say so.
**Never round up.**

For Kafka / DB-transaction / auth work specifically: an integration
test must pass before claiming done. These are the
"half-done is worse than not-done" categories.

---

## 4. Update the working file before the conversation ends

When you stop for the day:
1. Update the progress doc (tick what's done, note what's blocked, what's next)
2. Commit it

So next session — even from a fresh context — you can read the file
and resume without re-explaining everything.

---

## 5. When the AI is corrected, capture the lesson

If the AI drifts, forgets, or gets something wrong:
1. Fix the immediate issue
2. Ask: is this a one-off, or a recurring pattern?
3. If recurring → add a rule to your `CLAUDE.md` or a project-level
   `gotchas.md`. Don't let the same mistake bite twice.

This is how `CLAUDE.md` grows over time. It's not written in one
sitting — it's curated over months from real mistakes.

---

## 6. Don't pad

Direct, dense answers. No "great question!", no recap of what was
just said, no "let me know if you need anything else". Get to the
point. Structure with headings or lists when it actually helps
scanning, not because the LLM defaults to it.

---

## The meta-principle

> **AI is a peer, not a tool or a magic wand.**

A peer you can over-trust and get burned. A peer you can under-trust
and waste. The right relationship is: set clear expectations,
require evidence, give honest feedback, and **expect the same back**.

That's the whole game.
