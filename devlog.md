# Devlog

## 2026-07-15 — readme-storytelling — make the workflow portable across agents and model tiers

- **What**: Make the canonical workflow usable by any coding agent, move
  Claude Code and Codex into optional adapter guidance, and replace brittle
  provider-version routing with capability- and risk-based routing.
- **Why**: The public README and repository metadata still implied that Claude
  was required, while hard-coded model names and prices had already drifted.
- **Spec/Plan**: `.spec/readme-storytelling/current.md`
- **Commit**: `2a181ae`
- **Continues**: README storytelling work in PR #15
- **Notes**: Strong and weaker models keep the same acceptance criteria and
  evidence gates; task size, autonomy, permissions, and escalation differ.
  Claude plugin validation remains blocked because the CLI is not installed.

## 2026-07-15 — readme-storytelling — make the public entry point sound like Zoe

- **What**: Reframe the README around the failure and evidence loop that
  created the workflow; add dedicated Gotchas and Glossary entry points.
- **Why**: The existing README is complete but reads like a directory manual,
  and the two concepts Zoe expected are missing as discoverable documents.
- **Spec/Plan**: `.spec/readme-storytelling/current.md`
- **Commits**: `e351bd6`, plus the close-the-loop follow-up in PR #15
- **Continues**: public-profile and repository-brand cleanup from 2026-07-13
- **Notes**: Canonical workflow and pitfall content remains in its existing
  files; the new public docs route to it instead of copying it wholesale. The
  repository About homepage was also updated to `https://zoe-builds.com`.
