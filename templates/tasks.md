# Tasks

Each task is one independently verifiable slice with explicit ownership and an
exact check. Split when scope or dependencies would make the builder guess;
combine tiny adjacent steps when they form one cohesive commit.

- [ ] task-1: <small atomic change>
  - Files: <exact paths this task touches>
  - Test / validation: <test case or validator this covers>
  - Verify: <command that proves it, e.g. `go test ./pkg/x -run TestY`>

- [ ] task-2: ...

## Acceptance

When all tasks are done:
- [ ] All test cases in spec pass
- [ ] Independent findings fixed and reverified, or explicitly accepted
- [ ] PR description written
- [ ] ADR written (if architectural decision involved)
