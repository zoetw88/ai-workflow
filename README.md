# ai-workflow

> How a senior backend engineer actually works with AI agents.

This is not a "vibe coding" repo. It's the opposite — the discipline
that makes AI useful in production engineering work.

What's inside:

- **[PHILOSOPHY.md](./PHILOSOPHY.md)** — the principles that shape everything else
- **claude-code/** — `CLAUDE.md` template, subagent definitions, custom skills
- **prompts/** — reusable prompts for refactor / debug / review tasks
- **shell/** — aliases and functions that make AI workflows fast

Steal whatever's useful. Fork, adapt, ignore the rest.

---

## Why this exists

I've watched too many talented engineers either:

1. **Refuse to use AI** — and slowly fall behind
2. **Let AI run wild** — and ship plausible-but-wrong code

Neither is the answer. The answer is **AI as a peer**, not a tool or
a magic wand. That means you set the rules. You require evidence.
You verify before trusting.

These files are how I set those rules.

---

## Quick start

If you're using Claude Code:

```bash
# 1. Drop the template instructions into your global CLAUDE.md
cp claude-code/CLAUDE.md.example ~/.claude/CLAUDE.md

# 2. Copy a subagent that fits your workflow
cp claude-code/subagents/builder.md ~/.claude/agents/builder.md

# 3. Add a useful skill
cp claude-code/skills/grill-me.md ~/.claude/skills/grill-me.md
```

Then read [PHILOSOPHY.md](./PHILOSOPHY.md) to understand why each rule is there.

---

## License

MIT. Use freely, attribution appreciated but not required.
