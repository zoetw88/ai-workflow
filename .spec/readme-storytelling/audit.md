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
