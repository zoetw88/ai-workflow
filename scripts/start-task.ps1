param(
    [string]$RepoPath,
    [string]$Ticket,
    [switch]$LaunchCodex
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Normalize-Digits {
    param([string]$Value)

    if ($null -eq $Value) {
        return ""
    }

    $normalized = $Value.Trim()
    for ($i = 0; $i -le 9; $i++) {
        $fullWidthDigit = [string][char](0xFF10 + $i)
        $normalized = $normalized.Replace($fullWidthDigit, [string]$i)
    }

    return $normalized
}

function Prompt-Choice {
    param(
        [string]$Title,
        [string[]]$Options,
        [int]$DefaultIndex = 0
    )

    Write-Host ""
    Write-Host $Title
    for ($i = 0; $i -lt $Options.Count; $i++) {
        $defaultMark = if ($i -eq $DefaultIndex) { " (default)" } else { "" }
        Write-Host ("[{0}] {1}{2}" -f ($i + 1), $Options[$i], $defaultMark)
    }

    $raw = Read-Host "Choose 1-$($Options.Count)"
    if ([string]::IsNullOrWhiteSpace($raw)) {
        return $Options[$DefaultIndex]
    }

    $normalized = Normalize-Digits -Value $raw
    if ($normalized -notmatch '^\d+$') {
        throw "Invalid choice: $raw"
    }

    $index = [int]$normalized - 1
    if ($index -lt 0 -or $index -ge $Options.Count) {
        throw "Invalid choice: $raw"
    }

    return $Options[$index]
}

function Prompt-OptionalText {
    param(
        [string]$Title,
        [string]$Default = ""
    )

    $prompt = if ($Default) { "$Title [$Default]" } else { $Title }
    $raw = Read-Host $prompt
    if ([string]::IsNullOrWhiteSpace($raw)) {
        return $Default
    }

    return $raw.Trim()
}

function Prompt-RequiredText {
    param(
        [string]$Title,
        [string]$Hint = ""
    )

    while ($true) {
        $label = if ($Hint) { "$Title ($Hint)" } else { $Title }
        $value = Prompt-OptionalText -Title $label
        if (-not [string]::IsNullOrWhiteSpace($value)) {
            return $value
        }

        Write-Host "This field is required."
    }
}

function Prompt-Ticket {
    param([string]$Default = "")

    while ($true) {
        $value = Prompt-OptionalText -Title "Ticket / task id" -Default $Default
        if ($value.Length -lt 4) {
            Write-Host "Ticket is too short. Use something like MVP-8000 or bugfix/profile-ios."
            continue
        }

        if ($value -match '^\d+$') {
            Write-Host "Pure numeric tickets are too weak. Include system or context, for example MVP-8000 or DES-3333."
            continue
        }

        if ($value -match '^[A-Za-z0-9][A-Za-z0-9._/-]*$') {
            return $value
        }

        Write-Host "Ticket contains unsupported characters. Use letters, numbers, dot, underscore, slash, or dash."
    }
}

function Prompt-Notes {
    param([string]$Title = "Notes (optional, blank to finish)")

    $notes = New-Object System.Collections.Generic.List[string]
    while ($true) {
        $line = Prompt-OptionalText -Title $Title
        if ([string]::IsNullOrWhiteSpace($line)) {
            break
        }

        $notes.Add($line)
    }

    return ($notes -join " | ")
}

function Ensure-SpecScaffold {
    param(
        [string]$RepoPath,
        [string]$Ticket
    )

    if ([string]::IsNullOrWhiteSpace($Ticket)) {
        return
    }

    $taskDir = Join-Path $RepoPath ".spec\$Ticket"
    $null = New-Item -ItemType Directory -Path $taskDir -Force

    $templatesDir = Join-Path $HOME ".ai-workflow\templates"
    $copies = @(
        @{ Source = (Join-Path $templatesDir "tasks.md"); Target = (Join-Path $taskDir "tasks.md") }
        @{ Source = (Join-Path $templatesDir "ai-development-map.md"); Target = (Join-Path $taskDir "ai-development-map.md") }
    )

    foreach ($copy in $copies) {
        if ((Test-Path $copy.Source) -and -not (Test-Path $copy.Target)) {
            Copy-Item -LiteralPath $copy.Source -Destination $copy.Target
        }
    }

    $auditPath = Join-Path $taskDir "audit.md"
    if (-not (Test-Path $auditPath)) {
        @"
# $Ticket audit

## Findings

- 

## Deferred

- 
"@ | Set-Content -LiteralPath $auditPath
    }
}

function Ensure-Worktree {
    param(
        [string]$RepoPath,
        [string]$Ticket
    )

    $branch = $Ticket
    $repoName = Split-Path $RepoPath -Leaf
    $parent = Split-Path $RepoPath -Parent
    $worktreePath = Join-Path $parent ("$repoName-" + ($branch -replace '/', '-'))

    if (Test-Path $worktreePath) {
        Write-Host "Worktree already exists: $worktreePath"
        return $worktreePath
    }

    git -C $RepoPath worktree add $worktreePath -b $branch
    if ($LASTEXITCODE -ne 0) {
        # branch may already exist — reuse it instead of creating one
        git -C $RepoPath worktree add $worktreePath $branch
        if ($LASTEXITCODE -ne 0) {
            throw "git worktree add failed for $worktreePath (branch $branch)"
        }
    }

    Write-Host "Worktree created: $worktreePath"
    Write-Host "Verify the test baseline is GREEN there before building (workflow.md, Workspace isolation)."
    return $worktreePath
}

function Get-RepoChoices {
    # Personal/company repo paths live in the gitignored repos.local.json
    # (see repos.local.json.example) so they never enter version control.
    $choices = [ordered]@{
        "current" = (Get-Location).Path
    }

    $localMapPath = Join-Path $PSScriptRoot "repos.local.json"
    if (Test-Path $localMapPath) {
        $localMap = Get-Content -LiteralPath $localMapPath -Raw | ConvertFrom-Json
        foreach ($prop in $localMap.PSObject.Properties) {
            $choices[$prop.Name] = [string]$prop.Value
        }
    }

    $choices["custom"] = ""
    return $choices
}

function Get-TaskTypeChoices {
    return @("debug", "create", "change", "review", "investigate", "docs", "test-only", "refactor")
}

function Get-WorkflowChoices {
    return @("workflow", "build", "test", "review", "ship")
}

function Get-CommitChoices {
    return @("no-commit", "commit-when-ready")
}

function Get-ScopeChoices {
    return @("none", "resolve conflict", "do not touch migrations", "tests first", "docs only", "api only", "ui only", "custom")
}

function Get-SourceChoices {
    return @("jira", "slack", "sentry", "spec", "bug-report", "verbal", "custom")
}

function Get-PriorityChoices {
    return @("critical", "high", "medium", "low")
}

function Get-PitfallCaptureChoices {
    return @("ask-me", "yes", "no")
}

function Get-TypeSpecificFieldDefinitions {
    param([string]$TaskType)

    switch ($TaskType) {
        "debug" {
            return @(
                @{ Name = "symptom"; Hint = "What is breaking?" }
                @{ Name = "reproduction_steps"; Hint = "How do you trigger it?" }
                @{ Name = "expected_behavior"; Hint = "What should happen?" }
                @{ Name = "actual_behavior"; Hint = "What happens now?" }
                @{ Name = "error_message"; Hint = "Paste exact error, or 'none'" }
                @{ Name = "affected_scope"; Hint = "Env / users / platform / tenant scope" }
                @{ Name = "entrypoints"; Hint = "Endpoints, jobs, commands, handlers; use 'none' if unknown" }
                @{ Name = "suspected_files"; Hint = "Likely files or modules; use 'none' if unknown" }
                @{ Name = "related_tests"; Hint = "Relevant tests; use 'none' if unknown" }
                @{ Name = "search_hints"; Hint = "Strings, symbols, flags, log text, or keywords" }
            )
        }
        "create" {
            return @(
                @{ Name = "target_user_or_flow"; Hint = "Who uses it or where in the flow?" }
                @{ Name = "acceptance_criteria"; Hint = "What must be true at the end?" }
                @{ Name = "dependencies"; Hint = "Needed systems, APIs, or teams; use 'none' if none" }
                @{ Name = "existing_pattern_files"; Hint = "Similar implementations to follow; use 'none' if unknown" }
                @{ Name = "target_files"; Hint = "Planned files or modules; use 'none' if unknown" }
            )
        }
        "change" {
            return @(
                @{ Name = "requested_change"; Hint = "What should change?" }
                @{ Name = "acceptance_criteria"; Hint = "What must be true at the end?" }
                @{ Name = "affected_area"; Hint = "Files, modules, endpoints, or flows" }
                @{ Name = "entrypoints"; Hint = "Endpoints, jobs, commands, handlers; use 'none' if unknown" }
                @{ Name = "suspected_files"; Hint = "Files or modules expected to change; use 'none' if unknown" }
                @{ Name = "related_tests"; Hint = "Relevant tests; use 'none' if unknown" }
                @{ Name = "search_hints"; Hint = "Strings, symbols, flags, or keywords" }
            )
        }
        "review" {
            return @(
                @{ Name = "review_target"; Hint = "Branch, commit, PR, or files" }
                @{ Name = "review_focus"; Hint = "Bugs, regressions, security, tests, design" }
                @{ Name = "changed_files"; Hint = "Known changed files; use 'none' if unknown" }
                @{ Name = "related_tests"; Hint = "Relevant tests or suites; use 'none' if unknown" }
            )
        }
        "investigate" {
            return @(
                @{ Name = "question_to_answer"; Hint = "What are we trying to learn?" }
                @{ Name = "evidence_available"; Hint = "Logs, traces, docs, screenshots, or links" }
                @{ Name = "entrypoints"; Hint = "Endpoints, jobs, commands, handlers; use 'none' if unknown" }
                @{ Name = "suspected_files"; Hint = "Likely files or modules; use 'none' if unknown" }
                @{ Name = "search_hints"; Hint = "Strings, symbols, flags, or keywords" }
            )
        }
        "docs" {
            return @(
                @{ Name = "target_audience"; Hint = "Who is this for?" }
                @{ Name = "deliverable"; Hint = "ADR, README, runbook, audit doc, spec" }
                @{ Name = "reference_files"; Hint = "Source files or docs to read first; use 'none' if unknown" }
            )
        }
        "test-only" {
            return @(
                @{ Name = "test_target"; Hint = "What code or flow needs tests?" }
                @{ Name = "test_goal"; Hint = "What behavior do the tests need to prove?" }
                @{ Name = "related_tests"; Hint = "Target test files or suites; use 'none' if unknown" }
                @{ Name = "suspected_files"; Hint = "Code under test; use 'none' if unknown" }
            )
        }
        "refactor" {
            return @(
                @{ Name = "refactor_target"; Hint = "What area is being cleaned up?" }
                @{ Name = "guardrails"; Hint = "What behavior must not change?" }
                @{ Name = "suspected_files"; Hint = "Files or modules to refactor; use 'none' if unknown" }
                @{ Name = "related_tests"; Hint = "Tests that should stay green; use 'none' if unknown" }
                @{ Name = "search_hints"; Hint = "Symbols, patterns, duplication markers, or keywords" }
            )
        }
        default {
            return @()
        }
    }
}

function Build-Prompt {
    param(
        [string]$Ticket,
        [string]$TaskType,
        [string]$WorkflowMode,
        [string]$RepoName,
        [string]$RepoPath,
        [string]$Scope,
        [string]$CommitMode,
        [bool]$UseGrillMe
    )

    $parts = New-Object System.Collections.Generic.List[string]
    $parts.Add($Ticket)
    $parts.Add("task type $TaskType")

    switch ($WorkflowMode) {
        "workflow" { $parts.Add("start with workflow") }
        "build" { $parts.Add("go straight to build") }
        "test" { $parts.Add("go straight to verify") }
        "review" { $parts.Add("review only") }
        "ship" { $parts.Add("go straight to ship") }
    }

    if ($UseGrillMe) {
        $parts.Add("run grill-me first")
    }

    $parts.Add("only change $RepoName")
    $parts.Add("project path $RepoPath")

    if ($Scope) {
        $parts.Add($Scope)
    }

    switch ($CommitMode) {
        "no-commit" { $parts.Add("do not commit") }
        "commit-when-ready" { $parts.Add("commit when ready") }
    }

    return ($parts -join ", ") + "."
}

function Build-IntakeBlock {
    param(
        [System.Collections.IDictionary]$Intake,
        [string]$KickoffPrompt
    )

    $lines = New-Object System.Collections.Generic.List[string]
    $lines.Add("Task intake")

    $preferredOrder = @(
        "ticket",
        "task_type",
        "repo",
        "project_path",
        "mode",
        "use_grill_me",
        "commit_mode",
        "create_spec_scaffold",
        "use_worktree",
        "source_type",
        "source_link",
        "priority",
        "capture_as_pitfall",
        "scope_constraints",
        "task_description",
        "goal",
        "non_scope",
        "done_definition",
        "requested_change",
        "acceptance_criteria",
        "affected_area",
        "existing_pattern_files",
        "target_files",
        "target_user_or_flow",
        "dependencies",
        "symptom",
        "reproduction_steps",
        "expected_behavior",
        "actual_behavior",
        "error_message",
        "affected_scope",
        "entrypoints",
        "suspected_files",
        "changed_files",
        "related_tests",
        "search_hints",
        "review_target",
        "review_focus",
        "question_to_answer",
        "evidence_available",
        "target_audience",
        "deliverable",
        "reference_files",
        "test_target",
        "test_goal",
        "refactor_target",
        "guardrails",
        "notes"
    )

    foreach ($key in $preferredOrder) {
        if (-not $Intake.Contains($key)) {
            continue
        }

        $value = [string]$Intake[$key]
        if ([string]::IsNullOrWhiteSpace($value)) {
            $value = "none"
        }
        $lines.Add("${key}: $value")
    }

    $lines.Add("kickoff_prompt: $KickoffPrompt")
    return ($lines -join [Environment]::NewLine)
}

function Maybe-CopyToClipboard {
    param([string]$Text)

    try {
        if (Get-Command Set-Clipboard -ErrorAction SilentlyContinue) {
            $Text | Set-Clipboard
            return $true
        }
    }
    catch {
    }

    return $false
}

$repoMap = Get-RepoChoices
if (-not $RepoPath) {
    $repoChoice = Prompt-Choice -Title "Select repo" -Options @($repoMap.Keys) -DefaultIndex 0
    if ($repoChoice -eq "custom") {
        $RepoPath = Prompt-RequiredText -Title "Repo path"
    }
    else {
        $RepoPath = $repoMap[$repoChoice]
    }
}

if (-not (Test-Path $RepoPath)) {
    throw "Repo path does not exist: $RepoPath"
}

if (-not $Ticket) {
    $Ticket = Prompt-Ticket
}

$taskType = Prompt-Choice -Title "Task type" -Options (Get-TaskTypeChoices) -DefaultIndex 2
$workflowMode = Prompt-Choice -Title "Select mode" -Options (Get-WorkflowChoices) -DefaultIndex 0
$useGrillMe = (Prompt-Choice -Title "Use grill-me?" -Options @("yes", "no") -DefaultIndex 0) -eq "yes"
$commitMode = Prompt-Choice -Title "Commit mode" -Options (Get-CommitChoices) -DefaultIndex 0

$scopeChoice = Prompt-Choice -Title "Extra scope / constraints" -Options (Get-ScopeChoices) -DefaultIndex 0
$scope = switch ($scopeChoice) {
    "none" { "" }
    "custom" { Prompt-OptionalText -Title "Custom scope / constraints" }
    default { $scopeChoice }
}

$createSpec = (Prompt-Choice -Title "Create .spec scaffold?" -Options @("yes", "no") -DefaultIndex 0) -eq "yes"
$useWorktree = (Prompt-Choice -Title "Create git worktree for this ticket?" -Options @("yes", "no") -DefaultIndex 0) -eq "yes"
$sourceType = Prompt-Choice -Title "Source type" -Options (Get-SourceChoices) -DefaultIndex 0
if ($sourceType -eq "custom") {
    $sourceType = Prompt-RequiredText -Title "Custom source type"
}

$sourceLinkHint = if ($sourceType -eq "verbal") { "Optional for verbal tasks" } else { "Paste link, or 'none' if unavailable" }
$sourceLink = Prompt-RequiredText -Title "Source link" -Hint $sourceLinkHint
$priority = Prompt-Choice -Title "Priority" -Options (Get-PriorityChoices) -DefaultIndex 2
$captureAsPitfall = Prompt-Choice -Title "If we hit and solve a reusable blocker, ask to add pitfall?" -Options (Get-PitfallCaptureChoices) -DefaultIndex 0
$taskDescription = Prompt-RequiredText -Title "Task description" -Hint "One-sentence summary"
$goal = Prompt-RequiredText -Title "Goal" -Hint "What outcome do you want?"
$nonScope = Prompt-RequiredText -Title "Non-scope" -Hint "What should not be touched? Use 'none' if none"
$doneDefinition = Prompt-RequiredText -Title "Done definition" -Hint "How do we know this is done?"

$typeSpecificFields = Get-TypeSpecificFieldDefinitions -TaskType $taskType
$typeSpecificValues = [ordered]@{}
foreach ($field in $typeSpecificFields) {
    $typeSpecificValues[$field.Name] = Prompt-RequiredText -Title $field.Name -Hint $field.Hint
}

$notes = Prompt-Notes

$repoName = Split-Path $RepoPath -Leaf
if ($workflowMode -eq "ship" -and $commitMode -eq "no-commit") {
    $guardChoice = Prompt-Choice -Title "Ship mode usually implies a commit. Continue anyway?" -Options @("switch to commit-when-ready", "continue with no-commit") -DefaultIndex 0
    if ($guardChoice -eq "switch to commit-when-ready") {
        $commitMode = "commit-when-ready"
    }
}

if ($useWorktree) {
    $RepoPath = Ensure-Worktree -RepoPath $RepoPath -Ticket $Ticket
}

if ($createSpec) {
    Ensure-SpecScaffold -RepoPath $RepoPath -Ticket $Ticket
}

$kickoffPrompt = Build-Prompt `
    -Ticket $Ticket `
    -TaskType $taskType `
    -WorkflowMode $workflowMode `
    -RepoName $repoName `
    -RepoPath $RepoPath `
    -Scope $scope `
    -CommitMode $commitMode `
    -UseGrillMe:$useGrillMe

$intake = [ordered]@{
    ticket = $Ticket
    task_type = $taskType
    repo = $repoName
    project_path = $RepoPath
    mode = $workflowMode
    use_grill_me = $(if ($useGrillMe) { "yes" } else { "no" })
    commit_mode = $commitMode
    create_spec_scaffold = $(if ($createSpec) { "yes" } else { "no" })
    use_worktree = $(if ($useWorktree) { "yes" } else { "no" })
    source_type = $sourceType
    source_link = $sourceLink
    priority = $priority
    capture_as_pitfall = $captureAsPitfall
    scope_constraints = $(if ($scope) { $scope } else { "none" })
    task_description = $taskDescription
    goal = $goal
    non_scope = $nonScope
    done_definition = $doneDefinition
}

foreach ($entry in $typeSpecificValues.GetEnumerator()) {
    $intake[$entry.Key] = $entry.Value
}

if ($notes) {
    $intake["notes"] = $notes
}

$intakeBlock = Build-IntakeBlock -Intake $intake -KickoffPrompt $kickoffPrompt
$copied = Maybe-CopyToClipboard -Text $intakeBlock

Write-Host ""
Write-Host "Kickoff prompt:"
Write-Host $kickoffPrompt
Write-Host ""
Write-Host "Paste this block into Codex/Claude:"
Write-Host "----------------------------------------"
Write-Host $intakeBlock
Write-Host "----------------------------------------"
if ($copied) {
    Write-Host "Copied to clipboard."
}
Write-Host ""

if ($LaunchCodex) {
    $profile = switch ($workflowMode) {
        "workflow" { "plan" }
        "build" { "build" }
        "test" { "test" }
        "review" { "review" }
        "ship" { "ship" }
    }

    if (-not (Get-Command codex -ErrorAction SilentlyContinue)) {
        throw "codex CLI not found in PATH"
    }

    Write-Host "Launching Codex in $RepoPath with profile '$profile'..."
    Start-Process -FilePath "codex" -ArgumentList @("--profile", $profile) -WorkingDirectory $RepoPath
}
