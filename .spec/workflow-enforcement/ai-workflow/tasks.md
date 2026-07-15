<!-- branch: codex/workflow-enforcement -->

# Tasks

Repository: ai-workflow

- [x] task-1: Specify workflow-document and acceptance-warning behavior with failing tests
  - Files: `tests/test_workflow_enforcement.py`
  - Test / validation: WIP versus Ship, missing/mismatched living docs, placeholders, incomplete checkboxes, and warning-only acceptance quality
  - Verify: `python -m unittest tests.test_workflow_enforcement -v`

- [x] task-2: Implement structural living-doc validation and integrate it with close-loop
  - Files: `scripts/validate_workflow_docs.py`, `scripts/check_close_the_loop.py`
  - Test / validation: local WIP allows unchecked items; Ship mode fails incomplete/missing document contracts; semantic truth remains explicitly unprovable
  - Verify: `python -m unittest tests.test_workflow_enforcement.WorkflowDocumentValidatorTests tests.test_workflow_enforcement.CloseLoopIntegrationTests -v`

- [x] task-3: Specify and implement the private local system-map validator
  - Files: `tests/test_system_map_validator.py`, `scripts/validate_system_map.py`, `templates/system-map.md`
  - Test / validation: fixture repos cover valid maps, missing repos, invalid Git roots, missing entrypoints, placeholders, and if-present behavior
  - Verify: `python -m unittest tests.test_system_map_validator -v`

- [x] task-4: Add the pull-request CI workflow and contract tests
  - Files: `.github/workflows/validate.yml`, `tests/test_ci_workflow_contract.py`
  - Test / validation: CI has read-only permissions, pinned actions, full Git history, Python tests, Ship validation, and two pinned Claude strict validators
  - Verify: `python -m unittest tests.test_ci_workflow_contract -v`

- [x] task-5: Align canonical docs, templates, README, and the Claude mirror
  - Files: `workflow.md`, `context-management.md`, `README.md`, `templates/`, `claude-code/plugin/`
  - Test / validation: public claims match implemented local/CI behavior; mirror drift and plugin version contracts pass
  - Verify: `python -m unittest discover -s tests -v`

- [x] task-6: Prepare the ai-workflow handoff and hosted validation trigger
  - Files: `.spec/workflow-enforcement/`, `devlog.md`, `todo.md`
  - Test / validation: all local checks and strict Claude validation pass;
    evidence boundaries are recorded; the opened PR supplies hosted evidence
  - Verify: `python -m unittest discover -s tests -v` and `python scripts/check_close_the_loop.py`

## Acceptance

- [x] All acceptance criteria in `../current.md` have evidence or an explicit hosted-check boundary.
- [x] Independent findings are fixed and reverified or explicitly accepted.
- [x] PR description contract records local versus GitHub-hosted evidence.
