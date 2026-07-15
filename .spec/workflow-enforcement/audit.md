# Workflow enforcement audit

## Test-first evidence

- Red: 12 Python enforcement/CI tests failed because the validators and workflow
  did not exist or the old pre-push guard accepted a placeholder.
- Red: 2 Node article tests failed on the four known bilingual drift claims.
- Green: the full Python suite passes after implementation; the article contract
  and existing reading-system tests pass after the bilingual edit.

## Verification evidence

- `python -m unittest discover -s tests -v`
- `claude plugin validate --strict .`
- `claude plugin validate --strict claude-code/plugin`
- GitHub Markdown API render and README relative-link validation
- `python scripts/validate_system_map.py --map ~/.ai-workflow/system-map.md`
- `npm run check` and `npm run build` in the coordinated `zoe-site` worktree
- In-app browser inspection of both language routes at desktop and mobile widths

## Findings and decisions

- The private system-map file existed but was empty. It was populated locally
  with the two canonical clones and validated; it remains outside Git.
- Acceptance-quality findings are warnings by Zoe's decision. Missing documents,
  mismatched ticket pairs, placeholders, and incomplete Ship checklists fail.
- GitHub actions use full commit SHAs, the token is read-only, and Claude CLI is
  fixed at `2.1.210`.
- Fresh review found and closed Ship fail-open paths for docs-only changes,
  imprecise headings, empty checklists, bare `TODO`, path traversal, and a PR
  attempting to reclassify the repository. It also removed false positives for
  fenced examples and HTML comments. Each case has regression coverage.
- The bilingual articles now describe model routing and the optional Claude
  adapter without implying that Codex installs the Claude plugin.
- The English checklist code block scrolls horizontally on mobile by design;
  it does not create page-level overflow.

## Evidence boundary

- GitHub-hosted evidence does not exist until the PR is opened. The PR checks
  are required evidence before merge in both repositories, but branch-protection
  configuration is out of scope.
- The article was built and inspected locally; this change does not deploy or
  prove the live `zoe-builds.com` routes.
- `npm ci` reported six existing dependency audit findings in `zoe-site`
  (two low, two moderate, two high). No dependency was changed in this task.
