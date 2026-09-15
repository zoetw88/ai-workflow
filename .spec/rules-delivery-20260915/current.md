# Rule delivery

## Goal

Align rule distribution, clarification, debugging and private-map handling; retain the current plugin baseline and increment it to 0.5.1.

## Acceptance criteria

- [x] Observable: only rule documentation, task records, and the applicable plugin version change. Environment: isolated branch from the current remote integration baseline. Verify: inspect the complete diff and file list.
- [x] Observable: corrected rules preserve product behavior and explicit approval gates. Environment: document review against the recorded implementation and global contracts. Verify: targeted readback and diff checks.

## Non-goals

No application behavior, remote history rewrite, merge, deployment, or publication.
