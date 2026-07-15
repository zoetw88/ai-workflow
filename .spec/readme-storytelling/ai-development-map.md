# AI development map — README storytelling refresh

## Read order

1. `.spec/readme-storytelling/current.md`
2. `.spec/readme-storytelling/audit.md`
3. Zoe's published article: `https://zoe-builds.com/en/articles/my-ai-workflow/`
4. `README.md`
5. `PHILOSOPHY.md`
6. `workflow.md`
7. `pitfalls/{go,python,llm}.md`

## Change surface

- Public entry point: `README.md`
- New navigation documents: `GOTCHAS.md`, `GLOSSARY.md`
- Repository rules: `AGENTS.md`
- Living notes: `devlog.md`, `todo.md`

## Verification

- Resolve every relative Markdown link in changed public documents.
- Render `README.md` with GitHub's Markdown API.
- Run `git diff --check`.
- Run `python scripts/check_close_the_loop.py`.

## Out of scope

- Plugin code, versions, prompt contents, scripts, and workflow semantics.
