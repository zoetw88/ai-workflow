# AI workflow shell aliases
# Source from your ~/.zshrc or ~/.bashrc:
#   source ~/path/to/ai-workflow/shell/aliases.sh

# --- Claude Code ---
alias cc='claude'
alias ccr='claude --resume'                    # resume last session
alias ccp='claude --plan'                      # plan mode
alias ccc='claude --continue'                  # continue (skip permission prompts in dev)

# --- gh CLI helpers ---
alias prs='gh pr list --author "@me"'
alias mine='gh repo list "$(gh api user --jq .login)" --limit 100 --json name,isPrivate,pushedAt --jq "sort_by(.pushedAt) | reverse"'

# --- Quick git AI prep ---
# Run before asking AI to write a commit message
alias gd='git diff --staged'
alias gs='git status --short'

# Make a working sprint file for cross-session continuity
sprint() {
  local dir=".claude"
  local file="$dir/sprint.md"
  mkdir -p "$dir"
  if [ ! -f "$file" ]; then
    cat > "$file" <<EOF
# Sprint $(date +%Y-%m-%d)

## Current task

## Acceptance criteria
- [ ]

## Notes
EOF
  fi
  ${EDITOR:-vim} "$file"
}

# Quickly extract context for AI: recent diff + status + relevant files
ctx() {
  echo "=== git status ==="
  git status --short
  echo
  echo "=== last 5 commits ==="
  git log --oneline -5
  echo
  echo "=== staged diff ==="
  git diff --staged
}

# Drop in a project CLAUDE.md skeleton
init-claude-md() {
  if [ -f "CLAUDE.md" ]; then
    echo "CLAUDE.md already exists. Edit it instead."
    return 1
  fi
  cat > CLAUDE.md <<'EOF'
# CLAUDE.md

## What this repo does
<one paragraph>

## Important files
- <path> — <why it matters>

## Conventions
- <coding style / patterns this repo follows>

## Gotchas
- <non-obvious traps>

## Working rules
- Inherit global rules from ~/.claude/CLAUDE.md
EOF
  echo "Created CLAUDE.md skeleton. Edit it to fit this repo."
}
