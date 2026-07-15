import json
import importlib.util
import io
import re
import shutil
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class PublicReadmeContractTests(unittest.TestCase):
    def test_quick_start_precedes_reference_sections(self):
        readme = read("README.md")

        self.assertLess(readme.index("## Quick start"), readme.index("## The operating loop"))
        self.assertIn("templates/AGENTS.md.template", readme)
        self.assertIn("scripts/start-task.ps1", readme)

    def test_quick_start_preserves_existing_project_rules(self):
        readme = read("README.md")

        self.assertIn("If `AGENTS.md` already exists", readme)
        self.assertIn("<summary>Optional task bootstrap", readme)

    def test_public_entry_point_avoids_table_wall_and_adapter_bias(self):
        readme = read("README.md")
        table_separators = re.findall(r"^\|(?:\s*:?-+:?\s*\|)+$", readme, re.MULTILINE)

        self.assertLessEqual(len(table_separators), 2)
        self.assertIn("<details>", readme)
        self.assertIn("<summary>Claude Code plugin", readme)


class CanonicalWorkflowContractTests(unittest.TestCase):
    def test_workflow_uses_ticket_scoped_specs_and_proportional_controls(self):
        workflow = read("workflow.md")

        self.assertNotIn(".spec/current.md", workflow)
        self.assertNotIn("never on the main checkout", workflow)
        self.assertNotIn("TDD. One commit per task", workflow)
        self.assertIn("test-first", workflow)
        self.assertIn("Approval gates", workflow)
        self.assertIn("production-derived", workflow)

    def test_routing_is_risk_based_instead_of_fixed_to_the_strongest_model(self):
        workflow = read("workflow.md")

        self.assertNotIn("strongest reasoning available", workflow)
        self.assertNotIn("3-lens panel", workflow)
        self.assertIn("general coding model", workflow)
        self.assertIn("relevant review lenses", workflow)

    def test_close_loop_claim_matches_the_guard_scope(self):
        workflow = read("workflow.md")

        self.assertIn("The guard is intentionally narrow", workflow)
        self.assertIn("cannot prove", workflow)

    def test_core_workflow_stays_a_map_instead_of_a_monolithic_manual(self):
        workflow = read("workflow.md")

        self.assertLessEqual(len(workflow.splitlines()), 280)
        self.assertIn("[context-management.md](context-management.md)", workflow)


class AdapterConsistencyContractTests(unittest.TestCase):
    def test_active_agent_and_prompt_docs_use_ticket_scoped_specs(self):
        paths = [
            "claude-code/plugin/agents/builder.md",
            "claude-code/plugin/agents/planner.md",
            "claude-code/plugin/skills/six-stage-workflow/SKILL.md",
            "prompts/debug-ai-bug.md",
            "prompts/review-checklist.md",
        ]

        for path in paths:
            with self.subTest(path=path):
                self.assertNotIn(".spec/current.md", read(path))

    def test_claude_mirror_and_plugin_version_follow_the_canonical_change(self):
        mirror = read("claude-code/plugin/skills/six-stage-workflow/SKILL.md")
        manifest = json.loads(read("claude-code/plugin/.claude-plugin/plugin.json"))
        version = tuple(int(part) for part in manifest["version"].split("."))

        self.assertIn("proportional", mirror)
        self.assertIn("Approval gates", mirror)
        self.assertGreaterEqual(version, (0, 4, 0))

    def test_mirror_does_not_retain_superseded_mandates(self):
        mirror = read("claude-code/plugin/skills/six-stage-workflow/SKILL.md")

        for stale_rule in (
            "never on the main checkout",
            "TDD. One commit per task",
            "3-lens panel",
            "strongest reasoning available",
        ):
            with self.subTest(stale_rule=stale_rule):
                self.assertNotIn(stale_rule, mirror)


class LocalWorkflowToolContractTests(unittest.TestCase):
    def test_close_loop_only_accepts_true_living_documents(self):
        module = self._load_close_loop_module()

        self.assertTrue(module.is_living_doc(".spec/TICKET/current.md"))
        self.assertTrue(module.is_living_doc(".spec/TICKET/tasks.md"))
        self.assertTrue(module.is_living_doc("devlog.md"))
        self.assertTrue(module.is_living_doc("todo.md"))
        self.assertFalse(module.is_living_doc(".spec/TICKET/audit.md"))
        self.assertFalse(module.is_living_doc(".spec/TICKET/adr-001.md"))
        self.assertFalse(module.is_living_doc("docs/devlog.md"))
        self.assertFalse(module.is_living_doc("notes/todo.md"))

    def test_close_loop_fails_visibly_when_the_range_is_unknown(self):
        module = self._load_close_loop_module()
        stderr = io.StringIO()

        with mock.patch.object(module, "resolve_range", return_value=None):
            with redirect_stderr(stderr):
                result = module.main()

        self.assertEqual(1, result)
        self.assertIn("unable to resolve", stderr.getvalue())

    def test_task_bootstrap_persists_truth_and_guards_branch_isolation(self):
        script = read("scripts/start-task.ps1")

        self.assertIn("function Write-CurrentSpec", script)
        self.assertIn("function Ensure-FeatureBranch", script)
        self.assertIn("git -C $RepoPath worktree list --porcelain", script)
        self.assertIn('$workflowRoot = Split-Path $PSScriptRoot -Parent', script)
        self.assertNotIn('Join-Path $HOME ".ai-workflow\\templates"', script)

    @unittest.skipUnless(shutil.which("pwsh") and shutil.which("git"), "pwsh and git required")
    def test_task_bootstrap_creates_branch_and_persists_current_spec(self):
        answers = [
            "", "", "", "", "", "", "2", "", "none", "", "",
            "Docs contract smoke",
            "Persist spec and branch safely",
            "none",
            "current.md exists and branch is smoke/task",
            "persist the task intake",
            "spec exists",
            "docs",
            "none",
            "scripts/start-task.ps1",
            "none",
            "start-task",
            "",
        ]

        with tempfile.TemporaryDirectory(prefix="ai-workflow-start-task-") as fixture:
            subprocess.run(
                ["git", "-C", fixture, "init", "-b", "main"],
                check=True,
                capture_output=True,
                text=True,
            )
            result = subprocess.run(
                [
                    "pwsh",
                    "-NoProfile",
                    "-File",
                    str(ROOT / "scripts/start-task.ps1"),
                    "-RepoPath",
                    fixture,
                    "-Ticket",
                    "smoke/task",
                ],
                input="\n".join(answers) + "\n",
                capture_output=True,
                text=True,
                timeout=30,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            branch = subprocess.run(
                ["git", "-C", fixture, "branch", "--show-current"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            current = Path(fixture, ".spec", "smoke", "task", "current.md")

            self.assertEqual("smoke/task", branch)
            self.assertTrue(current.exists())
            self.assertIn("Persist spec and branch safely", current.read_text(encoding="utf-8"))

    @unittest.skipUnless(shutil.which("pwsh") and shutil.which("git"), "pwsh and git required")
    def test_task_bootstrap_creates_ticket_worktree_from_shared_branch(self):
        answers = [
            "", "", "", "", "", "", "", "", "none", "", "",
            "Worktree contract smoke",
            "Create the ticket worktree from main",
            "none",
            "current.md exists in the ticket worktree",
            "create an isolated worktree",
            "worktree and spec exist",
            "docs",
            "none",
            "scripts/start-task.ps1",
            "none",
            "start-task worktree",
            "",
        ]

        with tempfile.TemporaryDirectory(prefix="ai-workflow-worktree-") as root:
            fixture = Path(root, "repo")
            fixture.mkdir()
            subprocess.run(
                ["git", "-C", str(fixture), "init", "-b", "main"],
                check=True,
                capture_output=True,
                text=True,
            )
            Path(fixture, "README.md").write_text("# fixture\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(fixture), "add", "README.md"], check=True)
            subprocess.run(
                [
                    "git", "-C", str(fixture), "-c", "user.name=Test",
                    "-c", "user.email=test@example.com", "commit", "-m", "initial",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            result = subprocess.run(
                [
                    "pwsh",
                    "-NoProfile",
                    "-File",
                    str(ROOT / "scripts/start-task.ps1"),
                    "-RepoPath",
                    str(fixture),
                    "-Ticket",
                    "smoke/worktree",
                ],
                input="\n".join(answers) + "\n",
                capture_output=True,
                text=True,
                timeout=30,
            )

            worktree = Path(root, "repo-smoke-worktree")
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue(worktree.exists())
            branch = subprocess.run(
                ["git", "-C", str(worktree), "branch", "--show-current"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            current = worktree / ".spec" / "smoke" / "worktree" / "current.md"

            self.assertEqual("smoke/worktree", branch)
            self.assertTrue(current.exists())
            self.assertIn("Create the ticket worktree from main", current.read_text(encoding="utf-8"))

    @staticmethod
    def _load_close_loop_module():
        script_path = ROOT / "scripts/check_close_the_loop.py"
        spec = importlib.util.spec_from_file_location("close_loop", script_path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        return module


if __name__ == "__main__":
    unittest.main()
