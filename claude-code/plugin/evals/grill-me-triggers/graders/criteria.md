# Grading criteria: grill-me triggers on vague requests

The user gave a vague, under-specified feature request ("add a notification
feature"). The correct behavior per the grill-me skill is to ask clarifying
questions BEFORE proposing any solution or writing any code.

Score 1.0 if ALL of:
- The response asks clarifying questions instead of proposing a concrete
  implementation or writing code
- It asks between 3 and 7 questions
- The questions would genuinely change the design (e.g. delivery channel,
  latency requirement, volume, triggers, read-state) — not filler like
  "do you want it to work well?"

Score 0.5 if it asks questions but also commits to a specific design or starts
writing code in the same response.

Score 0.0 if it proposes a solution or writes code without asking anything.
