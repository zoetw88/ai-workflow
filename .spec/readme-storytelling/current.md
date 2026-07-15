# README storytelling refresh

## Goal

Make the public repository explain Zoe's real AI-development philosophy before
presenting its file layout, and make clear that the workflow is usable by any
coding agent that can read project instructions and produce verifiable work.

## Acceptance criteria

- [x] README opens with the failure that shaped the workflow and states the
      core evidence-first loop in Zoe's article voice.
- [x] README provides a short route to principles, workflow, gotchas,
      glossary, templates, and installation without the current directory wall.
- [x] `GOTCHAS.md` exists and distinguishes workflow gotchas from the detailed
      language/application checklists in `pitfalls/`.
- [x] `GLOSSARY.md` defines the repository's recurring terms in plain English.
- [x] Existing Claude Code installation commands and Codex/tool-agnostic usage
      remain documented.
- [x] Public links use `zoe-builds.com`; local Markdown links resolve.
- [x] GitHub Markdown rendering and repository verification pass.
- [ ] README presents the generic agent path first; Claude Code and Codex are
      adapters, not prerequisites.
- [ ] README explains that strong and weaker models use one workflow with
      different task granularity, autonomy, and escalation rules.
- [ ] `workflow.md` describes parallel agents and model routing by capability,
      without assuming Claude-specific agent types or hard-coding provider
      versions and prices.
- [ ] The Claude plugin mirror and version stay aligned with the canonical
      workflow change.
- [ ] GitHub's public repository description no longer frames the project as a
      Claude-only template collection.

## Non-goals

- Build native plugin adapters for every agent product.
- Claim that every tool natively reads `AGENTS.md` or supports subagents.
- Change scripts or project templates beyond wording needed for tool-agnostic
  instructions.
- Duplicate every canonical document inside the README.
