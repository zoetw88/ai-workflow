# Audit — README storytelling refresh

Date: 2026-07-15

## Evidence

- `README.md` is 165 lines and leads with repository structure, a full file
  tree, and setup instructions.
- Zoe's source article is
  `zoe-site/content/articles/en/my-ai-workflow.md`. Its narrative starts with a
  20,000-line AI-assisted change whose critical Kafka integration was missing,
  then derives the evidence-first rules from that failure.
- No `GOTCHAS.md` or `GLOSSARY.md` exists on `main`.
- Gotcha-related guidance is split across `PHILOSOPHY.md`, `workflow.md`,
  `pitfalls/`, `templates/system-map.md`, and `shell/aliases.sh`.
- `README.md` still links to `zoe-site-ten.vercel.app`; Zoe's canonical domain
  is `zoe-builds.com`.
- All prior README/plugin PRs are merged; no open PR contains this work.

## Decision

Use README as the human entry point, not as a duplicate filesystem index.
Create focused Gotchas and Glossary entry documents that route readers to the
canonical files where details already live.

## Extension — cross-agent use and model routing

Date: 2026-07-15

### Evidence

- The branch README calls the repository tool-agnostic, but its only turnkey
  install is still the Claude Code plugin; the generic path is two sentences.
- GitHub's repository description still leads with `CLAUDE.md templates`.
- `workflow.md` describes parallel work in Claude-specific `Agent` / `Explore`
  terms even though Codex and other orchestrators expose equivalent roles with
  different names and scheduling APIs.
- The canonical model table hard-codes provider versions and prices. Anthropic's
  current catalog still matches its Claude rows, but OpenAI's current catalog
  has already moved beyond the GPT-5.4 names in the table.
- Provider documentation agrees on capability tiers: frontier models for
  complex reasoning, balanced models for general work, and fast models for
  cost-sensitive bounded work. The exact product names are the unstable part.

### Decision

Keep one evidence-gated six-stage workflow. Route work by capability and risk:
fast models get bounded deterministic tasks, general coding models get atomic
implementation slices, and the strongest available model handles ambiguity,
architecture, conflict, and high-risk review. Stronger models receive more
judgment-heavy work, never weaker verification requirements.

### Verification

- Validated 26 relative links across 13 Markdown files.
- Rendered `README.md` through GitHub's Markdown API: 12 headings, 22 links,
  and 5 tables were present in the rendered result.
- Parsed the Claude plugin manifest and confirmed version `0.3.0`.
- `git diff --check` and `python scripts/check_close_the_loop.py` passed.
- The local environment has no `claude` executable, so
  `claude plugin validate` could not be run; this is an environment blocker,
  not a passing plugin-CLI result.
