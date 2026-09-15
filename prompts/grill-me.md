# Grill Me — interactive requirement clarification

Inspired by Matt Pocock's pattern. Resolve consequential unknowns using existing context first, then ask only what remains necessary.

## How to use

Read the request, prior decisions, repository contracts, and relevant task docs before asking. Use the dimensions below to identify consequential gaps, not as a mandatory questionnaire. Ask the minimum needed questions; continue independent work while waiting and defer only work that depends on a required answer.

### Dimensions to consider (skip irrelevant or already resolved items)

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

- ONE question per dimension — don't sprawl
- Phrase as "Do you want X or Y?" when possible, not open-ended
- For routine implementation choices, use existing contracts and state any material assumption. Do not guess consequential product, authorization, or data-loss decisions.
- Summarize resolved decisions when useful; do not add a mandatory confirmation round or repeat an approval already given.
- If no consequential unknown remains, proceed. There is no question quota or mandatory interview phase.

## When NOT to grill

- Trivial requests ("rename this variable")
- Bug fixes with clear reproduction (the spec is "make this test pass")
- Tasks already broken down by a planner
