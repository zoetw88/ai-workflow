# Prompt: Refactor

Use when you want to clean up code without changing behavior.

---

```
Refactor the code in <path> with these rules:

1. **Behavior must not change.** If existing tests pass before, they
   pass after. If no tests exist, write characterization tests first.

2. **No new features.** No "while I'm here" additions.

3. **No new dependencies** unless you ask first.

4. **One refactor pattern at a time.** Don't mix "extract method" +
   "rename" + "move file" into one diff. Separate commits.

5. **Output a plan first.** Don't write code until I approve the plan:
   - What pattern (extract, rename, move, inline, etc.)
   - Why (concrete benefit, not "cleaner")
   - Risk (what might break)

6. **After each step, verify.** Run tests. Show me the output.

Anti-patterns to avoid:
- ❌ Splitting a 50-line function into 10 micro-functions
- ❌ Adding interfaces "for testability" when nothing else implements them
- ❌ Reformatting whitespace mixed into a semantic refactor
```
