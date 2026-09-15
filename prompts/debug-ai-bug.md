# Prompt: Debug AI-generated bug

Use when a regression may involve AI-generated code; confirm its cause rather than assuming authorship proves it.

---

```
Investigate the reported bug at <path> using this SOP:

1. **Reproduce.** Show me the exact command that triggers the bug
   and the exact output you get vs. what you expect.

2. **Protect the working state and narrow the cause.** Inspect the branch,
   working-tree changes, callers, and relevant history. Use a separate disposable
   worktree or test copy for historical comparisons, bisecting, or controlled
   mutations. Preserve uncommitted and unrelated work; do not revert files in
   the user's checkout to experiment. Record the exact revision and patch tested.

3. **Match to spec.** Read the resolved task spec (.spec/<ticket>/current.md, the repository's established path, or what I
   told you to build). For each acceptance criterion, verify the
   code actually implements it. A mismatch is a candidate cause; demonstrate
   its connection to the reported failure before calling it the root cause.

4. **Choose the reproducing boundary.** Use the smallest test that reproduces
   the observed defect with an independent expected result. The defect may span
   functions, configuration, or services; do not force it into a mocked unit test
   if the real boundary is what fails. Record missing reproduction evidence when
   the environment blocks it, and distinguish hypotheses from verified causes.

5. **Make the smallest evidence-backed repair.** Preserve established behavior
   and compatibility. Function length and the number of attempts do not justify
   deletion or regeneration. If attempts fail, revisit the reproduction and
   causal hypothesis; explain any broader change with evidence and keep it
   within the authorized scope.

6. **Verify.** Follow the applicable global and repository gates. Record relevant
   fail-to-pass or controlled-mutation evidence without weakening assertions,
   plus affected integration/E2E and failure/recovery results. State the revision,
   environment, discovered tests, actual outcomes, and remaining gaps. A green
   unit test alone does not prove a service workflow or deployed fix.

DO NOT skip step 1. "I think it's because..." without a
reproduction is guessing.
```
