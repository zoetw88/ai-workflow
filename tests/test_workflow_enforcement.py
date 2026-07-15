import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_workflow_docs.py"
CLOSE_LOOP = ROOT / "scripts" / "check_close_the_loop.py"

VALID_CURRENT = """
# Fixture feature

## Goal

Create a report.

## Acceptance criteria

- [ ] Observable: `report.json` contains the normalized result.
  - Environment: local fixture repository.
  - Verify: `python verify_report.py`.

## Non-goals

- Change production data.
"""

VALID_TASKS = """
# Tasks

- [ ] task-1: Build the report
  - Files: `report.py`
  - Test / validation: report schema contract
  - Verify: `python verify_report.py`

## Acceptance

- [ ] All acceptance criteria have evidence.
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def create_docs(root: Path, ticket: str = "fixture", complete: bool = False) -> None:
    current = VALID_CURRENT
    tasks = VALID_TASKS
    if complete:
        current = current.replace("- [ ]", "- [x]")
        tasks = tasks.replace("- [ ]", "- [x]")
    write(root / ".spec" / ticket / "current.md", current)
    write(root / ".spec" / ticket / "tasks.md", tasks)
    write(root / "AGENTS.md", "# Rules\n\n**Project type: personal**\n")
    write(root / "devlog.md", "# Devlog\n")
    write(root / "todo.md", "# Todo\n")
    write(root / "app.py", "print('fixture')\n")


def run_validator(
    root: Path,
    mode: str,
    changed_files: list[str],
    env: dict[str, str] | None = None,
    project_type: str | None = None,
) -> subprocess.CompletedProcess:
    command = [
        sys.executable,
        str(VALIDATOR),
        "--root",
        str(root),
        "--mode",
        mode,
    ]
    if project_type:
        command.extend(["--project-type", project_type])
    for changed_file in changed_files:
        command.extend(["--changed-file", changed_file])
    return subprocess.run(command, capture_output=True, text=True, timeout=20, env=env)


class WorkflowDocumentValidatorTests(unittest.TestCase):
    def test_wip_accepts_unchecked_but_structurally_complete_ticket_docs(self):
        with tempfile.TemporaryDirectory(prefix="workflow-wip-") as fixture:
            root = Path(fixture)
            create_docs(root)

            result = run_validator(
                root,
                "wip",
                ["app.py", ".spec/fixture/current.md", ".spec/fixture/tasks.md"],
            )

        self.assertEqual(0, result.returncode, result.stderr)

    def test_ship_rejects_unchecked_acceptance_and_task_items(self):
        with tempfile.TemporaryDirectory(prefix="workflow-ship-") as fixture:
            root = Path(fixture)
            create_docs(root)

            result = run_validator(
                root,
                "ship",
                [
                    "app.py",
                    ".spec/fixture/current.md",
                    ".spec/fixture/tasks.md",
                    "devlog.md",
                    "todo.md",
                ],
            )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("unchecked", (result.stdout + result.stderr).lower())

    def test_ship_rejects_a_substantive_docs_only_change_without_living_docs(self):
        with tempfile.TemporaryDirectory(prefix="workflow-docs-only-") as fixture:
            root = Path(fixture)
            create_docs(root, complete=True)
            write(root / "workflow.md", "# Changed canonical policy\n")

            result = run_validator(root, "ship", ["workflow.md"])

        self.assertNotEqual(0, result.returncode)
        self.assertIn("living document", (result.stdout + result.stderr).lower())

    def test_ship_accepts_docs_only_when_the_complete_living_tier_is_changed(self):
        with tempfile.TemporaryDirectory(prefix="workflow-docs-complete-") as fixture:
            root = Path(fixture)
            create_docs(root, complete=True)
            write(root / "workflow.md", "# Changed canonical policy\n")

            result = run_validator(
                root,
                "ship",
                [
                    "workflow.md",
                    ".spec/fixture/current.md",
                    ".spec/fixture/tasks.md",
                    "devlog.md",
                    "todo.md",
                ],
            )

        self.assertEqual(0, result.returncode, result.stderr)

    def test_explicit_personal_project_type_cannot_be_disabled_by_the_pr(self):
        with tempfile.TemporaryDirectory(prefix="workflow-project-type-") as fixture:
            root = Path(fixture)
            create_docs(root, complete=True)
            write(root / "AGENTS.md", "# Rules changed by this PR\n")

            result = run_validator(
                root,
                "ship",
                ["app.py", ".spec/fixture/current.md", ".spec/fixture/tasks.md"],
                project_type="personal",
            )

        output = (result.stdout + result.stderr).lower()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("devlog.md", output)
        self.assertIn("todo.md", output)

    def test_ship_warns_but_passes_for_weak_acceptance_wording(self):
        with tempfile.TemporaryDirectory(prefix="workflow-warning-") as fixture:
            root = Path(fixture)
            create_docs(root, complete=True)
            weak = """
            # Fixture feature

            ## Goal

            Create a report.

            ## Acceptance criteria

            - [x] The report works well.

            ## Non-goals

            - Change production data.
            """
            write(root / ".spec" / "fixture" / "current.md", weak)

            result = run_validator(
                root,
                "ship",
                [
                    "app.py",
                    ".spec/fixture/current.md",
                    ".spec/fixture/tasks.md",
                    "devlog.md",
                    "todo.md",
                ],
            )

        output = (result.stdout + result.stderr).lower()
        self.assertEqual(0, result.returncode, output)
        self.assertIn("warning", output)
        self.assertIn("observable", output)
        self.assertIn("environment", output)
        self.assertIn("verify", output)

    def test_github_actions_emits_a_warning_annotation_without_failing(self):
        with tempfile.TemporaryDirectory(prefix="workflow-annotation-") as fixture:
            root = Path(fixture)
            create_docs(root, complete=True)
            weak = """
            # Fixture feature

            ## Goal

            Create a report.

            ## Acceptance criteria

            - [x] The report works well.

            ## Non-goals

            - Change production data.
            """
            write(root / ".spec" / "fixture" / "current.md", weak)
            env = os.environ.copy()
            env["GITHUB_ACTIONS"] = "true"

            result = run_validator(
                root,
                "ship",
                [
                    "app.py",
                    ".spec/fixture/current.md",
                    ".spec/fixture/tasks.md",
                    "devlog.md",
                    "todo.md",
                ],
                env=env,
            )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("::warning file=.spec/fixture/current.md::", result.stdout)

    def test_ship_rejects_current_and_tasks_from_different_tickets(self):
        with tempfile.TemporaryDirectory(prefix="workflow-mismatch-") as fixture:
            root = Path(fixture)
            create_docs(root, ticket="alpha", complete=True)
            create_docs(root, ticket="beta", complete=True)

            result = run_validator(
                root,
                "ship",
                [
                    "app.py",
                    ".spec/alpha/current.md",
                    ".spec/beta/tasks.md",
                    "devlog.md",
                    "todo.md",
                ],
            )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("same ticket", (result.stdout + result.stderr).lower())

    def test_ship_rejects_placeholders_in_living_docs(self):
        with tempfile.TemporaryDirectory(prefix="workflow-placeholder-") as fixture:
            root = Path(fixture)
            create_docs(root, complete=True)
            tasks = (root / ".spec" / "fixture" / "tasks.md").read_text(encoding="utf-8")
            write(root / ".spec" / "fixture" / "tasks.md", tasks + "\n- <TBD>\n")

            result = run_validator(
                root,
                "ship",
                [
                    "app.py",
                    ".spec/fixture/current.md",
                    ".spec/fixture/tasks.md",
                    "devlog.md",
                    "todo.md",
                ],
            )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("placeholder", (result.stdout + result.stderr).lower())

    def test_ship_rejects_checked_template_placeholders_and_ellipses(self):
        with tempfile.TemporaryDirectory(prefix="workflow-template-placeholder-") as fixture:
            root = Path(fixture)
            create_docs(root, complete=True)
            current = """
            # <Feature name>

            ## Goal

            <Why this exists. Business motivation. Link to ticket.>

            ## Acceptance criteria

            - [x] Observable: <result a reviewer can see or measure>
              - Environment: <local, CI, staging, production, or named device>
              - Verify: <exact command or numbered manual steps>

            ## Non-goals

            - ...
            """
            tasks = """
            # Tasks

            - [x] task-1: <small atomic change>
              - Files: <exact paths this task touches>
              - Test / validation: <test case or validator this covers>
              - Verify: <command that proves it>

            ## Acceptance

            - [x] All acceptance criteria have evidence.
            """
            write(root / ".spec" / "fixture" / "current.md", current)
            write(root / ".spec" / "fixture" / "tasks.md", tasks)

            result = run_validator(
                root,
                "ship",
                [
                    "app.py",
                    ".spec/fixture/current.md",
                    ".spec/fixture/tasks.md",
                    "devlog.md",
                    "todo.md",
                ],
            )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("placeholder", (result.stdout + result.stderr).lower())

    def test_ship_rejects_bare_todo_values_in_completed_living_docs(self):
        with tempfile.TemporaryDirectory(prefix="workflow-bare-todo-") as fixture:
            root = Path(fixture)
            create_docs(root, complete=True)
            current_path = root / ".spec" / "fixture" / "current.md"
            tasks_path = root / ".spec" / "fixture" / "tasks.md"
            current = current_path.read_text(encoding="utf-8")
            tasks = tasks_path.read_text(encoding="utf-8")
            write(current_path, current.replace("Create a report.", "TODO"))
            write(tasks_path, tasks.replace("task-1: Build the report", "task-1: TODO"))

            result = run_validator(
                root,
                "ship",
                [
                    "app.py",
                    ".spec/fixture/current.md",
                    ".spec/fixture/tasks.md",
                    "devlog.md",
                    "todo.md",
                ],
            )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("placeholder", (result.stdout + result.stderr).lower())

    def test_ship_allows_real_angle_bracket_markup_inside_fenced_code(self):
        with tempfile.TemporaryDirectory(prefix="workflow-fenced-markup-") as fixture:
            root = Path(fixture)
            create_docs(root, complete=True)
            current_path = root / ".spec" / "fixture" / "current.md"
            current = current_path.read_text(encoding="utf-8")
            write(
                current_path,
                current
                + """

                ## Interface example

                ```html
                <div>
                  <span>Verified result</span>
                </div>
                ```
                """,
            )

            result = run_validator(
                root,
                "ship",
                [
                    "app.py",
                    ".spec/fixture/current.md",
                    ".spec/fixture/tasks.md",
                    "devlog.md",
                    "todo.md",
                ],
            )

        self.assertEqual(0, result.returncode, result.stderr)

    def test_ship_allows_branch_metadata_html_comment(self):
        with tempfile.TemporaryDirectory(prefix="workflow-branch-comment-") as fixture:
            root = Path(fixture)
            create_docs(root, complete=True)
            tasks_path = root / ".spec" / "fixture" / "tasks.md"
            tasks = tasks_path.read_text(encoding="utf-8")
            write(tasks_path, "<!-- branch: codex/fixture -->\n" + tasks)

            result = run_validator(
                root,
                "ship",
                [
                    "app.py",
                    ".spec/fixture/current.md",
                    ".spec/fixture/tasks.md",
                    "devlog.md",
                    "todo.md",
                ],
            )

        self.assertEqual(0, result.returncode, result.stderr)

    def test_ship_ignores_checkbox_examples_inside_fenced_code(self):
        with tempfile.TemporaryDirectory(prefix="workflow-fenced-checkbox-") as fixture:
            root = Path(fixture)
            create_docs(root, complete=True)
            current_path = root / ".spec" / "fixture" / "current.md"
            current = current_path.read_text(encoding="utf-8")
            write(
                current_path,
                current
                + """

                ## UI example

                ```markdown
                - [ ] unchecked UI state
                ```
                """,
            )

            result = run_validator(
                root,
                "ship",
                [
                    "app.py",
                    ".spec/fixture/current.md",
                    ".spec/fixture/tasks.md",
                    "devlog.md",
                    "todo.md",
                ],
            )

        self.assertEqual(0, result.returncode, result.stderr)

    def test_ship_rejects_an_acceptance_heading_without_checklist_criteria(self):
        with tempfile.TemporaryDirectory(prefix="workflow-empty-acceptance-") as fixture:
            root = Path(fixture)
            create_docs(root, complete=True)
            empty = """
            # Fixture feature

            ## Goal

            Create a report.

            ## Acceptance criteria

            Evidence will be added later.

            ## Non-goals

            - Change production data.
            """
            write(root / ".spec" / "fixture" / "current.md", empty)

            result = run_validator(
                root,
                "ship",
                [
                    "app.py",
                    ".spec/fixture/current.md",
                    ".spec/fixture/tasks.md",
                    "devlog.md",
                    "todo.md",
                ],
            )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("at least one checklist", (result.stdout + result.stderr).lower())

    def test_ship_rejects_tasks_without_exact_headings_or_checklists(self):
        with tempfile.TemporaryDirectory(prefix="workflow-empty-tasks-") as fixture:
            root = Path(fixture)
            create_docs(root, complete=True)
            malformed = """
            This prose mentions # Tasks but is not a heading.

            ## Acceptance

            Evidence will be added later.
            """
            write(root / ".spec" / "fixture" / "tasks.md", malformed)

            result = run_validator(
                root,
                "ship",
                [
                    "app.py",
                    ".spec/fixture/current.md",
                    ".spec/fixture/tasks.md",
                    "devlog.md",
                    "todo.md",
                ],
            )

        output = (result.stdout + result.stderr).lower()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("missing required heading: # tasks", output)
        self.assertIn("at least one task checklist", output)
        self.assertIn("at least one acceptance checklist", output)

    def test_ship_does_not_count_an_acceptance_checkbox_as_a_task(self):
        with tempfile.TemporaryDirectory(prefix="workflow-task-in-acceptance-") as fixture:
            root = Path(fixture)
            create_docs(root, complete=True)
            malformed = """
            # Tasks

            ## Acceptance

            - [x] task-1: This is in the wrong section.
            """
            write(root / ".spec" / "fixture" / "tasks.md", malformed)

            result = run_validator(
                root,
                "ship",
                [
                    "app.py",
                    ".spec/fixture/current.md",
                    ".spec/fixture/tasks.md",
                    "devlog.md",
                    "todo.md",
                ],
            )

        output = (result.stdout + result.stderr).lower()
        self.assertNotEqual(0, result.returncode)
        self.assertIn("at least one task checklist", output)


@unittest.skipUnless(shutil.which("git"), "git required")
class CloseLoopIntegrationTests(unittest.TestCase):
    def test_pre_push_guard_runs_wip_structure_validation(self):
        with tempfile.TemporaryDirectory(prefix="workflow-close-loop-") as fixture:
            root = Path(fixture)
            create_docs(root)
            subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, capture_output=True)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Test",
                    "-c",
                    "user.email=test@example.com",
                    "commit",
                    "-m",
                    "initial",
                ],
                cwd=root,
                check=True,
                capture_output=True,
            )
            base = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True
            ).stdout.strip()
            write(root / "app.py", "print('changed')\n")
            current = (root / ".spec" / "fixture" / "current.md").read_text(encoding="utf-8")
            write(root / ".spec" / "fixture" / "current.md", current + "\n<TBD>\n")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Test",
                    "-c",
                    "user.email=test@example.com",
                    "commit",
                    "-m",
                    "changed",
                ],
                cwd=root,
                check=True,
                capture_output=True,
            )
            head = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True
            ).stdout.strip()
            env = os.environ.copy()
            env["PRE_COMMIT_FROM_REF"] = base
            env["PRE_COMMIT_TO_REF"] = head

            result = subprocess.run(
                [sys.executable, str(CLOSE_LOOP)],
                cwd=root,
                env=env,
                capture_output=True,
                text=True,
                timeout=20,
            )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("placeholder", (result.stdout + result.stderr).lower())


if __name__ == "__main__":
    unittest.main()
