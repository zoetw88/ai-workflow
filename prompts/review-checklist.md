# Review Checklist

Priority order — stop at the first level that finds blocking issues.

## 1. Spec conformance (highest)

- [ ] Implements every required test case in `.spec/current.md`?
- [ ] Stays inside scope (no scope creep)?
- [ ] Respects stated invariants?
- [ ] If deviates from spec, is the deviation documented?

## 2. Correctness

- [ ] nil / empty handling on all inputs
- [ ] Error paths covered
- [ ] Off-by-one, boundary conditions
- [ ] Type assertions / conversions that could panic

## 3. Concurrency (if applicable)

- [ ] Goroutine ownership clear (who cancels, who waits)
- [ ] Shared state protected
- [ ] Context propagated
- [ ] `-race` clean

## 4. Security

- [ ] Input validation at trust boundaries
- [ ] No SQL / command injection vectors
- [ ] No secrets in logs / error returns
- [ ] Auth checks on protected paths

## 5. Maintainability

- [ ] Names match spec vocabulary
- [ ] No over-abstraction (interface for 1 impl, factory for 1 type)
- [ ] No hallucinated APIs (verify external calls exist)
- [ ] Comments explain WHY where non-obvious

## Output format

```
## Review

### MUST FIX (blocking)
- [file:line] <issue>

### SHOULD FIX
- ...

### CONSIDER
- ...

### Spec conformance: PASS / PARTIAL / FAIL
```
