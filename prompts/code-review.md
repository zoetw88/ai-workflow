# Prompt: Code review

Use this to get an adversarial review of code you just wrote.

---

```
You are reviewing the diff I just made. Your job is to find what's
wrong, not what's right. Don't approve to be polite.

Focus on:
1. Spec compliance — does this solve the stated problem?
2. Edge cases — empty/null/large inputs, timeouts, concurrent access
3. Error paths — anything silently swallowed?
4. Resource leaks — files/connections/goroutines closed?
5. Security — input validation, auth, no secrets in logs
6. Tests — do they actually exercise this code, or pass without it?

Output format:
- ✅ Correctly implemented: <criterion> → <file:line>
- ❌ Issues found: <severity> <description> <file:line> <suggested fix>
- ❓ Questions: <any ambiguity>

Severity: blocker / major / minor.

Skip style nits — assume the linter handles them.
Don't rewrite the code yourself.
```
