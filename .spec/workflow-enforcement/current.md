# Workflow enforcement

## Intake

- Ticket: `workflow-enforcement`
- Type: feature
- Description: Turn four evidence-process gaps into explicit, testable local
  and GitHub contracts without claiming that automation can judge semantic
  truth.
- Affected repositories:
  - `ai-workflow`
  - `zoe-site`
- Device type: developer tooling and GitHub-hosted CI
- Payload shape: not applicable

## Goal

Strengthen workflow-document checks, add GitHub-hosted validation, make the
private local system map verifiable, and warn when acceptance criteria are not
independently testable.

## Acceptance criteria

- [x] Observable: WIP accepts open checkboxes while rejecting invalid ticket
      structure and placeholders without claiming semantic correctness.
  - Environment: Windows fixture repositories and pre-push integration fixture.
  - Verify: `python -m unittest tests.test_workflow_enforcement -v`.
- [x] Observable: pull requests have a read-only GitHub-hosted workflow for
      repository tests, Ship validation, and both strict Claude validators.
      CI pins `--project-type personal`, so the PR cannot disable its own policy.
  - Environment: `.github/workflows/validate.yml`; hosted execution occurs when
    the PR is opened and is reported by GitHub checks.
  - Verify: `python -m unittest tests.test_ci_workflow_contract -v` and inspect
    the PR's `Workflow contracts` check before merge.
- [x] Observable: weak acceptance criteria create visible log warnings and
      GitHub annotations but do not change a successful exit code.
  - Environment: local CLI and simulated `GITHUB_ACTIONS=true`.
  - Verify: `python -m unittest tests.test_workflow_enforcement.WorkflowDocumentValidatorTests.test_github_actions_emits_a_warning_annotation_without_failing -v`.
- [x] Observable: `~/.ai-workflow/system-map.md` remains private and its declared
      repositories, Git roots, entrypoints, and placeholders are validated.
  - Environment: public fixture maps in tests plus Zoe's local private map.
  - Verify: `python -m unittest tests.test_system_map_validator -v` and
    `python scripts/validate_system_map.py --map ~/.ai-workflow/system-map.md`.
- [x] Observable: regression tests cover WIP/Ship, mismatch, placeholders,
      warnings, invalid map claims, and immutable CI dependencies.
  - Environment: Python 3.11 locally and Python 3.12 in configured PR CI.
  - Verify: `python -m unittest discover -s tests -v`.
- [x] Observable: canonical workflow, templates, README, and Claude mirror state
      the same enforcement and evidence boundaries; plugin version is `0.5.0`.
  - Environment: repository source and official Claude CLI `2.1.210`.
  - Verify: full Python suite plus both `claude plugin validate --strict` commands.
- [x] Observable: both `my-ai-workflow` articles distinguish durable rules from
      ticket truth, evidence from hashes, optional adapters, and iterative loops.
  - Environment: bilingual Markdown sources in `zoe-site`.
  - Verify: `node --test tests/ai-workflow-article-contract.test.mjs`.
- [x] Observable: both article routes build and render readably without page-level
      horizontal overflow at desktop and mobile widths.
  - Environment: local Astro development server and Codex in-app browser.
  - Verify: `npm run check`, `npm run build`, and manual browser inspection of
    `/articles/my-ai-workflow/` and `/en/articles/my-ai-workflow/`.

## Key invariants

- Automation validates structure and evidence contracts; it does not decide
  whether prose is factually correct.
- No personal repository path or private system-map content is committed.
- Chinese and English article claims stay semantically equivalent.
- WIP remains pushable; completion is enforced by PR CI.
- Acceptance-criteria quality findings are warnings, not blocking errors.
- The GitHub workflow is added, but branch protection and required-check rules
  are not changed.

## Non-goals

- Publish a shared system map.
- Change GitHub branch protection or repository rulesets.
- Prevent every possible intentional bypass of local hooks.
- Use an LLM as a correctness gate.
- Merge or deploy without Zoe's explicit approval.
- Change unrelated `zoe-site` runtime, Cloudflare migration, or article content.

## Verification environments

- Local Windows worktree for Python and PowerShell contract tests.
- GitHub-hosted runner for the pull-request workflow.
- Fixture repositories and maps for system-map validation.
- Isolated `zoe-site` worktree for Astro build/check and bilingual visual QA.

## Open questions

- None. Zoe confirmed all four gaps are in scope, WIP is allowed, acceptance
  quality is warning-only, the system map stays local, and only the CI workflow
  should be added.
