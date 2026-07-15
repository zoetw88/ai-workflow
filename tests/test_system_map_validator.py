import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_system_map.py"


def run_validator(map_path: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--map", str(map_path), *extra],
        capture_output=True,
        text=True,
        timeout=20,
    )


def write_map(path: Path, repo_path: Path, entrypoint: str = "src/main.py") -> None:
    path.write_text(
        "\n".join(
            [
                "# System map",
                "",
                "## Repos",
                "",
                "### owner/repo — fixture",
                "",
                f"- Local path: `{repo_path.as_posix()}`",
                "- Stack: Python",
                f"- Entry points: `{entrypoint}`",
                "- Public surface: none",
                "- Consumes: none",
                "- Workflow docs: `.spec/`",
                "- Gotchas: none",
                "",
            ]
        ),
        encoding="utf-8",
    )


class SystemMapValidatorTests(unittest.TestCase):
    def test_validates_existing_git_repo_and_entrypoint(self):
        with tempfile.TemporaryDirectory(prefix="system-map-valid-") as fixture:
            root = Path(fixture)
            repo = root / "repo"
            (repo / "src").mkdir(parents=True)
            (repo / "src" / "main.py").write_text("print('ok')\n", encoding="utf-8")
            subprocess.run(["git", "init", "-b", "main"], cwd=repo, check=True, capture_output=True)
            map_path = root / "system-map.md"
            write_map(map_path, repo)

            result = run_validator(map_path)

        self.assertEqual(0, result.returncode, result.stderr)

    def test_if_present_skips_a_missing_private_map(self):
        with tempfile.TemporaryDirectory(prefix="system-map-skip-") as fixture:
            map_path = Path(fixture) / "missing.md"

            result = run_validator(map_path, "--if-present")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("skipped", (result.stdout + result.stderr).lower())

    def test_allows_angle_bracket_route_parameters_that_are_not_template_fields(self):
        with tempfile.TemporaryDirectory(prefix="system-map-route-") as fixture:
            root = Path(fixture)
            repo = root / "repo"
            (repo / "src").mkdir(parents=True)
            (repo / "src" / "main.py").write_text("print('ok')\n", encoding="utf-8")
            subprocess.run(["git", "init", "-b", "main"], cwd=repo, check=True, capture_output=True)
            map_path = root / "system-map.md"
            write_map(map_path, repo)
            source = map_path.read_text(encoding="utf-8")
            map_path.write_text(
                source.replace("- Public surface: none", "- Public surface: `GET /users/<id>`"),
                encoding="utf-8",
            )

            result = run_validator(map_path)

        self.assertEqual(0, result.returncode, result.stderr)

    def test_rejects_unbackticked_entrypoints_instead_of_silently_skipping_them(self):
        with tempfile.TemporaryDirectory(prefix="system-map-unbackticked-") as fixture:
            root = Path(fixture)
            repo = root / "repo"
            (repo / "src").mkdir(parents=True)
            subprocess.run(["git", "init", "-b", "main"], cwd=repo, check=True, capture_output=True)
            map_path = root / "system-map.md"
            write_map(map_path, repo)
            source = map_path.read_text(encoding="utf-8")
            map_path.write_text(
                source.replace("`src/main.py`", "src/main.py"),
                encoding="utf-8",
            )

            result = run_validator(map_path)

        self.assertNotEqual(0, result.returncode)
        self.assertIn("backtick", (result.stdout + result.stderr).lower())

    def test_rejects_entrypoints_that_escape_the_repository_root(self):
        with tempfile.TemporaryDirectory(prefix="system-map-traversal-") as fixture:
            root = Path(fixture)
            repo = root / "repo"
            repo.mkdir()
            (root / "outside.txt").write_text("outside\n", encoding="utf-8")
            subprocess.run(["git", "init", "-b", "main"], cwd=repo, check=True, capture_output=True)
            map_path = root / "system-map.md"
            write_map(map_path, repo, "../outside.txt")

            result = run_validator(map_path)

        self.assertNotEqual(0, result.returncode)
        self.assertIn("inside the repository", (result.stdout + result.stderr).lower())

    def test_rejects_missing_repo_non_git_root_missing_entrypoint_and_placeholder(self):
        cases = ("missing-repo", "non-git", "missing-entrypoint", "placeholder")
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory(prefix=f"system-map-{case}-") as fixture:
                root = Path(fixture)
                repo = root / "repo"
                repo.mkdir()
                map_path = root / "system-map.md"

                if case == "missing-repo":
                    repo = root / "does-not-exist"
                    write_map(map_path, repo)
                elif case == "placeholder":
                    write_map(map_path, repo)
                    source = map_path.read_text(encoding="utf-8")
                    map_path.write_text(source.replace("Python", "<language>"), encoding="utf-8")
                else:
                    if case == "missing-entrypoint":
                        subprocess.run(["git", "init", "-b", "main"], cwd=repo, check=True, capture_output=True)
                    write_map(map_path, repo, "src/missing.py")

                result = run_validator(map_path)

            output = (result.stdout + result.stderr).lower()
            self.assertNotEqual(0, result.returncode, output)
            expected = {
                "missing-repo": "does not exist",
                "non-git": "git repository",
                "missing-entrypoint": "entry point",
                "placeholder": "placeholder",
            }[case]
            self.assertIn(expected, output)


if __name__ == "__main__":
    unittest.main()
