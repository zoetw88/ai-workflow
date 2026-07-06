# Tasks

Each task: 2–5 minutes of focused agent work, ≤ 1 commit. If it looks bigger, split it —
coarse tasks are where agents start improvising. Done = Verify command passes + reviewed.

- [ ] task-1: <small atomic change>
  - Files: <exact paths this task touches>
  - Test: <test case from spec this covers>
  - Verify: <command that proves it, e.g. `go test ./pkg/x -run TestY`>

- [ ] task-2: ...

## Acceptance

When all tasks are done:
- [ ] All test cases in spec pass
- [ ] Independent reviewer approved
- [ ] PR description written
- [ ] ADR written (if architectural decision involved)
