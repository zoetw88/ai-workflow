<!-- branch: codex/workflow-enforcement-article -->

# Tasks

Repository: zoe-site

- [x] task-1: Capture outdated bilingual workflow claims with failing tests
  - Files: `tests/ai-workflow-article-contract.test.mjs`
  - Test / validation: Chinese and English sources reject the single-source AGENTS claim, commit-hash-only evidence, Claude-primary positioning, and one-clean-pass wording
  - Verify: `node --test tests/ai-workflow-article-contract.test.mjs`

- [x] task-2: Align the Chinese and English article with the canonical workflow
  - Files: `content/articles/my-ai-workflow.md`, `content/articles/en/my-ai-workflow.md`
  - Test / validation: durable rules versus ticket truth, evidence types, model routing, local-versus-production boundary, approval gates, optional Claude adapter, and iterative review remain semantically equivalent
  - Verify: `node --test tests/ai-workflow-article-contract.test.mjs`

- [x] task-3: Verify the rendered article and close the zoe-site handoff
  - Files: `.spec/workflow-enforcement/` and generated build output only for local inspection
  - Test / validation: Astro build/check pass; both language routes render with readable hierarchy and stable URLs at desktop and mobile widths
  - Verify: `$env:NODE_OPTIONS='--use-system-ca'; npm run check; npm run build`

- [x] task-4: Wire bilingual synchronization into the existing site PR check
  - Files: coordinated `zoe-site/.github/workflows/build.yml`
  - Test / validation: read-only workflow runs article tests, Astro check, build
  - Verify: inspect the hosted `Build check` before merge

## Acceptance

- [x] Chinese and English workflow claims are semantically aligned.
- [x] Article contract test, Astro check, build, and browser QA pass.
- [x] Existing site PR CI is configured to rerun the bilingual contract.
- [x] Coordinated PR description contract links the canonical ai-workflow change.
