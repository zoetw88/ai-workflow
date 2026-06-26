# Prompt: Debug AI-generated bug

Use when AI-generated code has a bug and you don't know where.

---

```
The code at <path> has a bug. AI wrote it. Walk through this SOP:

1. **Reproduce.** Show me the exact command that triggers the bug
   and the exact output you get vs. what you expect.

2. **Bisect.** If the AI wrote multiple files, find which file is
   the culprit by reverting them one at a time.

3. **Match to spec.** Read the spec (.spec/current.md or what I
   told you to build). For each acceptance criterion, verify the
   code actually implements it. Anything not matched → that's the
   bug source.

4. **Isolate the function.** Find the single function where the
   bug lives. Write a unit test that reproduces the bug at that
   function level (red).

5. **Decide: fix or regenerate?**
   - If the function is < 30 lines: fix in place
   - If > 30 lines or you've been "fixing" it for 3 turns:
     delete the function and regenerate with better spec

6. **Verify.** Run the test. Show me green.

DO NOT skip step 1. "I think it's because..." without a
reproduction is guessing.
```
