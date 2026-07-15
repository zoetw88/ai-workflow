# Context management

Deep guidance for keeping ticket, repository, and cross-project context useful
without turning `AGENTS.md` or `workflow.md` into a monolithic manual.

The canonical six-stage process remains in [`workflow.md`](workflow.md). This
file owns optional index hierarchy and anti-drift rules.

## Spec map (optional, threshold and generated)

A `spec-map.md` indexes the `.spec/` areas. It earns its place only when there
are many areas:

- Add it only when `.spec/` has more than eight areas. Below that,
  `current.md` and `tasks.md` are enough.
- Generate it with `scripts/build-spec-map.ps1`; do not hand-maintain a plain
  index that will drift.
- Keep the roles distinct: `current.md` is current truth, `spec-map.md` is
  repository navigation, and `ai-development-map.md` is ticket handoff order.

For an existing curated map, run `build-spec-map.ps1 -DryRun` and compare the
result. Never overwrite a map that contains policy, release state, or other
hand-maintained sections; update those maps deliberately.

## Cross-project maps

Above each repository sit two optional views:

- `~/.ai-workflow/system-map.md` — structure across repositories: entry points,
  public surfaces, integration edges, and shared libraries. Build it with
  `prompts/system-map-scan.md`; spot-check only the edges a ticket touches. Run
  `python scripts/validate_system_map.py --map ~/.ai-workflow/system-map.md`
  after edits, or add `--if-present` when the private map is optional.
- `~/.ai-workflow/portfolio.md` — project status, current focus, and next
  milestone. Generate it with `prompts/portfolio-scan.md`; status downgrade and
  archival remain human decisions.

The index hierarchy is:

1. `system-map.md` — cross-repository structure
2. `portfolio.md` — cross-project status
3. `<repo>/spec-map.md` — one repository's spec areas
4. `.spec/<ticket>/ai-development-map.md` — one ticket's read order

Use GitHub Projects or the team's adopted tracker when several humans need a
shared roadmap. Generated local Markdown is the lightweight option for a solo
developer whose agents need file-based context.

## Anti-drift rule

Generators are drift detectors and initializers, not replacement tools:

- New large project: generate the first map, then add deliberate grouping.
- Existing plain map: generate in dry-run mode and compare.
- Curated map: never overwrite; patch only the stale entries.
- When reality contradicts a map, reality wins. Correct the affected line in
  the same PR when it is inside the authorized change surface.

The validator checks declared local paths, Git roots, entrypoint paths, and
template placeholders. It never uploads the map and cannot prove integration
semantics; CI exercises only public fixtures.
