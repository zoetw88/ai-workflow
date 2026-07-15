import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "validate.yml"


class PullRequestWorkflowContractTests(unittest.TestCase):
    def test_pull_request_workflow_enforces_ship_without_changing_repository_rules(self):
        self.assertTrue(WORKFLOW.exists(), "expected .github/workflows/validate.yml")
        source = WORKFLOW.read_text(encoding="utf-8")

        self.assertRegex(source, r"(?m)^\s*pull_request:\s*$")
        self.assertRegex(source, r"(?ms)^permissions:\s*\n\s*contents:\s*read\s*$")
        self.assertIn("fetch-depth: 0", source)
        self.assertIn("python -m unittest discover -s tests -v", source)
        self.assertIn("validate_workflow_docs.py", source)
        self.assertIn("--mode ship", source)
        self.assertIn("--project-type personal", source)
        self.assertNotIn("branches: write", source)

    def test_actions_and_claude_cli_are_immutably_pinned(self):
        self.assertTrue(WORKFLOW.exists(), "expected .github/workflows/validate.yml")
        source = WORKFLOW.read_text(encoding="utf-8")
        action_uses = re.findall(r"uses:\s*(actions/(?:checkout|setup-python|setup-node))@([^\s#]+)", source)

        self.assertEqual(3, len(action_uses), action_uses)
        for action, revision in action_uses:
            with self.subTest(action=action):
                self.assertRegex(revision, r"^[0-9a-f]{40}$")
        self.assertIn("@anthropic-ai/claude-code@2.1.210", source)

    def test_both_claude_plugin_surfaces_receive_strict_validation(self):
        self.assertTrue(WORKFLOW.exists(), "expected .github/workflows/validate.yml")
        source = WORKFLOW.read_text(encoding="utf-8")
        strict_commands = re.findall(r"claude plugin validate --strict ([^\r\n]+)", source)

        self.assertEqual(2, len(strict_commands), strict_commands)
        self.assertIn(".", [command.strip() for command in strict_commands])
        self.assertIn("claude-code/plugin", [command.strip() for command in strict_commands])


if __name__ == "__main__":
    unittest.main()
