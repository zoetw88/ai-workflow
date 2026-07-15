# AI workflow enforcement

## Goal

Implement deterministic WIP/Ship workflow-document checks, private system-map
validation, and a read-only GitHub-hosted pull-request gate.

## Acceptance criteria

- [x] Observable: WIP/Ship, warning, system-map, and CI contracts pass locally.
  - Environment: `ai-workflow` feature worktree.
  - Verify: `python -m unittest discover -s tests -v`.
- [x] Observable: canonical docs and the optional Claude mirror agree, and both
      Claude plugin surfaces pass strict validation at version `0.5.0`.
  - Environment: official Claude CLI `2.1.210`.
  - Verify: run `claude plugin validate --strict .` and
    `claude plugin validate --strict claude-code/plugin`.

## Non-goals

- Change GitHub branch protection or rulesets.
- Publish the private system map.
- Claim structural validation proves semantic correctness.
