# AI development map — README and workflow foundation refresh

## Read order

1. `.spec/readme-workflow-refresh/current.md`
2. `.spec/readme-workflow-refresh/audit.md`
3. `AGENTS.md`
4. `README.md`
5. `workflow.md`
6. `context-management.md`
7. `scripts/check_close_the_loop.py`
8. `claude-code/plugin/skills/six-stage-workflow/SKILL.md`

## Change surface

- Public entry point: `README.md`
- Canonical process: `workflow.md`
- Deep context/index guidance: `context-management.md`
- Repository rules/template: `AGENTS.md`, `templates/AGENTS.md.template`
- Claude mirror/agents: `claude-code/plugin/`
- Related reusable prompts: `prompts/`
- Local bootstrap and enforcement: `scripts/start-task.ps1`,
  `scripts/check_close_the_loop.py`
- Drift guard: `tests/test_docs_contracts.py`
- Living history: `devlog.md`, `todo.md`

## Boundaries

- Keep close-loop enforcement narrow: reject code pushes without a true
  living-tier document, but do not claim that it validates document accuracy.
- Do not add provider-specific model names to canonical routing.
- Do not merge without Zoe's explicit approval.
