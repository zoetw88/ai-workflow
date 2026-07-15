# Glossary

Plain-English definitions for terms used throughout this repository.

## Acceptance criteria

An explicit checklist describing what must be true before a task can be called
complete. It is written before implementation and verified with evidence.

## AGENTS.md

The repository-level source of truth read by Codex and other compatible agents:
project boundaries, commands, risks, and what "done" requires. Tool-specific
files should import or point to it instead of maintaining conflicting rules.

## AI development map

The per-ticket handoff file at `.spec/<ticket>/ai-development-map.md`. It tells
the next agent what to read, what changed, what remains, and which traps matter.

## Canonical source

The one file that owns a rule. Other copies are adapters or mirrors and must
declare where the canonical version lives.

## Close the loop

The Ship-stage discipline of updating current task state, handoff documents,
project history, and affected maps in the same change as the implementation.

## Evidence block

A completion report containing exact criteria, commands, results, file
references, and unverified boundaries. It replaces "I think this is done."

## Historical tier

Append-only context such as audits and architecture decision records. It
explains what was known or decided at a point in time; it is not current truth.

## Living tier

Documents that must match the current state, including the active spec, task
checklist, development log, and work queue.

## Pitfall / gotcha

A recurring failure pattern worth preventing. `pitfalls/` holds reusable
technical checklists; repo- and ticket-specific gotchas stay closer to their
boundary.

## Portfolio map

A human-facing cross-project status view: what is active, paused, next, or
overlapping. It answers "what should I work on?"

## Review

An independent judgment pass asking whether the implementation is correct,
safe, maintainable, and aligned with the spec. Review is not a substitute for
running tests.

## Spec map

A generated index of the specification areas inside one repository. It helps
navigation once a project has enough `.spec/` areas to justify another index.

## System map

An agent-facing cross-repository context cache: locations, entry points, public
surfaces, dependencies, and integration edges. It answers "where does this
change travel?"

## Verify

The stage that runs the relevant checks and gathers proof that acceptance
criteria are met. Verify asks "does it work?"

## Worktree

An isolated Git working directory attached to its own branch. The workflow uses
one worktree per ticket so concurrent tasks do not overwrite each other.
