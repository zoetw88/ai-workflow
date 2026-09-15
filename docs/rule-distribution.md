# Rule sources and local installation

This repository is the maintained source for shareable workflow guidance. A local
installation is a reviewed snapshot, not a second independently edited canonical
repository. Repository-specific contracts and explicit user decisions retain
their authority; installation does not waive approval or verification gates.

## Updating shareable guidance

1. Start from the current integration branch in an isolated checkout.
2. Change the canonical prompt or workflow and each declared adapter mirror in
   the same reviewable change. Update the plugin version from the current version.
3. Review the complete diff, run the repository checks, and record the source
   revision and validation results. Do not copy an entire personal configuration
   directory into this repository.
4. After the change is approved and merged, update local installations using an
   explicit file list. Compare local differences first and preserve intentional
   private overrides separately. Record the installed source revision and any
   exceptions. A prepared branch is not a published or installed release.

## Local state and privacy

Keep personal inventories, machine paths, credentials, and company notes outside
the shareable repository. Existing ignore rules are a guard, not proof that a
previous commit or remote copy contains no private data. Check tracked files and
the staged diff before each publication; do not use bulk staging to synchronize
a personal directory.

Do not use `skip-worktree` or `assume-unchanged` to hide edits to maintained agent
rules. Keep portable rules tracked, and place deliberately private overrides in
the tool's local configuration. When removing a hidden-file flag, preserve the
working file first and verify its contents afterward. Do not force-add ignored
company rules merely to make status look complete.

Historical removal is separate from ordinary file deletion and rule delivery.
Rewriting published history needs a scoped plan, a verified recovery copy, and
explicit approval; it cannot guarantee removal from forks or third-party copies.
