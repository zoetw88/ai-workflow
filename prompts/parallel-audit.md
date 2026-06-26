# Parallel Audit Pattern

Use when scope discovery requires inspecting multiple independent areas (repos, modules, concerns) and the results are read-only.

## When to invoke

- Cross-repo gap analysis (e.g. "Does feature X exist in services A, B, C?")
- Wide codebase audit (find all references / usages / patterns)
- Multi-concern investigation (security + perf + correctness on the same diff)
- Spec gap-finding before Plan stage

## When NOT to invoke

- Single-file work
- Sequential dependencies (each agent needs the prior agent's output)
- Anything that writes files (use the builder subagent, not parallel agents)
- TDD cycle (red → green → refactor needs single context)

## The recipe

1. Identify N independent areas. Typical N = 3–6.
2. In ONE message, spawn N `Agent` tool calls.
3. Each prompt must:
   - Be self-contained (no reference to "above" or "the conversation")
   - Specify the exact question
   - Cap output length: "Report in under 200 words"
   - Choose agent type: `Explore` for read-only lookups, `general-purpose` for open-ended research
4. While agents run, the main session prepares the synthesis target (the audit doc skeleton, headings, criteria).
5. When all agents return, synthesize into one structured artifact (`.spec/<ticket>/audit.md`).
6. Verify any specific claims an agent made before treating them as facts (especially file paths, line numbers, function existence).

## Anti-patterns

- **Duplicating agent work** — running greps yourself while an agent is doing the same. Pick one.
- **Sequential agent calls** — writing four `Agent` calls across four messages instead of one. That serializes them.
- **Open-ended prompts** — "look at this codebase and tell me what's wrong" produces unfocused reports.
- **Letting agents return full file contents** — that pulls raw text into main context. Always cap word count.

## Template prompt

```
You are auditing <area> for <specific question>.

Context: <repo path, what this code does, why I care>.

Tasks:
1. <specific check 1>
2. <specific check 2>
3. <specific check 3>

Return a structured report under 200 words with:
- Findings (one bullet per concrete observation, include file:line)
- Categorization: <e.g. A/B/C/D per audit doc convention>
- Anything surprising

Do not edit files. Do not run code beyond grep / read.
```

## Example: 3-repo audit

For MVP-NNNN spanning UIS / SAS / scep-server:

```
Agent 1 (Explore): UIS — find all ProfileType.android references, classify each
Agent 2 (Explore): SAS — verify config is env-driven; find brand string literals
Agent 3 (Explore): scep-server — verify no brand-specific code paths
```

All three in one message. Main session waits for all three reports, then writes audit.md.

Estimated wall-clock saving vs serial: 3–5×. Main session context saved: large (raw grep results never enter main context).
