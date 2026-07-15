# Zoe site workflow article alignment

## Goal

Align both public workflow articles to the canonical enforced behavior while
preserving the existing article design and voice.

## Acceptance criteria

- [x] Observable: Traditional Chinese and English sources carry equivalent
      claims about durable rules, ticket truth, evidence, adapters, and loops.
  - Environment: coordinated `zoe-site` feature worktree.
  - Verify: `node --test tests/ai-workflow-article-contract.test.mjs`.
- [x] Observable: both routes build and render without page-level overflow.
  - Environment: local Astro server and in-app browser at desktop/mobile widths.
  - Verify: Astro check/build and manual inspection of both article routes.
- [x] Observable: `zoe-site` pull-request CI runs the bilingual contract before
      either article can merge independently.
  - Environment: read-only GitHub-hosted `Build check`.
  - Verify: inspect the coordinated article PR check before merge.

## Non-goals

- Deploy the site.
- Change unrelated Cloudflare migration or design work.
