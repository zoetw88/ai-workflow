# AI development map — workflow enforcement

## Read order

1. `current.md` — accepted cross-repository behavior and evidence boundaries
2. `build-order.md` — canonical policy before public article wording
3. `ai-workflow/tasks.md` — enforcement implementation and verification
4. `zoe-site/tasks.md` — bilingual article and visual QA
5. `audit.md` — exact evidence and remaining hosted/live boundaries

## Change surfaces

- Workflow policy and adapters: `workflow.md`, `context-management.md`,
  `README.md`, `templates/`, `claude-code/plugin/`
- Deterministic enforcement: `scripts/validate_workflow_docs.py`,
  `scripts/validate_system_map.py`, `scripts/check_close_the_loop.py`
- Hosted gate: `.github/workflows/validate.yml`
- Public explanation: coordinated `zoe-site` bilingual article PR

## Handoff

- Merge remains Zoe's decision.
- Check GitHub-hosted `Workflow contracts` before merging `ai-workflow`.
- A local article build is not evidence that the live site changed.
