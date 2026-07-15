# Grill Me — interactive requirement clarification

Inspired by Matt Pocock's pattern. AI does not propose a solution. AI only asks until requirements are clear.

## How to use

When a vague request leaves material product, risk, or authorization decisions
unresolved, ask only the questions needed to settle them. First inspect the
repository, ticket, and existing decisions for answers; do not ask the user to
repeat discoverable context.

### Required dimensions (skip only if explicit in the request)

1. **Scope boundary**
   - What is in scope vs. out of scope?
   - What's the smallest version that delivers value?

2. **Inputs & validation**
   - What inputs are accepted? Format, size, character set?
   - Empty input behavior?
   - Oversized input behavior?
   - Malformed input behavior?

3. **Outputs & failure modes**
   - Success response shape?
   - Error response shape? Which error codes?
   - What does the caller see when downstream fails?

4. **State & persistence**
   - Stateless or stateful?
   - If stateful: where, retention policy, consistency requirements?

5. **Concurrency**
   - Is this called concurrently? From how many sources?
   - Idempotent on retry?
   - Rate limit considerations?

6. **Auth & authorization**
   - Who can call this? How are they authenticated?
   - Are there permission checks beyond authentication?

7. **Observability**
   - What should be logged? At what level?
   - What metrics should this emit?
   - What alerts should fire on failure?

8. **Downstream dependencies**
   - What external services / DBs does this hit?
   - What are their SLAs and failure modes?
   - Circuit breaker / retry strategy?

## Rules

- Ask only questions whose answers change scope, behavior, risk, or authority
- Prefer one question at a time; group only when the answers are independent
- Phrase as "Do you want X or Y?" when possible, not open-ended
- If user can't answer, propose a sensible default and call out the assumption
- Stop when the remaining uncertainty no longer changes the result
- DO NOT propose implementation details until grill is done

## When NOT to grill

- Trivial requests ("rename this variable")
- Bug fixes with clear reproduction (the spec is "make this test pass")
- Tasks already broken down by a planner
