<!-- branch: codex/workflow-enforcement -->

# Tasks

Ticket: workflow enforcement orchestrator

- [x] task-1: Define the cross-repository contract and build order
  - Files: `current.md`, `build-order.md`
  - Test / validation: scope, approval boundaries, and evidence environments are explicit
  - Verify: review both documents against Zoe's confirmed decisions

- [x] task-2: Complete the canonical enforcement implementation
  - Files: `ai-workflow/tasks.md`
  - Test / validation: WIP/Ship, warning, map, CI, docs, and adapter contracts
  - Verify: `python -m unittest discover -s tests -v`

- [x] task-3: Complete the bilingual public explanation
  - Files: `zoe-site/tasks.md` and the coordinated `zoe-site` branch
  - Test / validation: bilingual contract, Astro check/build, and browser QA
  - Verify: see `audit.md` and `zoe-site/tasks.md`

- [x] task-4: Prepare coordinated PR handoff without merging or deploying
  - Files: `audit.md`, `ai-development-map.md`, `devlog.md`, `todo.md`
  - Test / validation: local versus hosted/live evidence boundaries are explicit
  - Verify: inspect both PR descriptions and GitHub-hosted checks before merge

## Acceptance

- [x] Canonical enforcement is complete and locally verified.
- [x] Bilingual article claims and rendered routes are locally verified.
- [x] Merge, branch protection, and deployment remain outside agent authority.
