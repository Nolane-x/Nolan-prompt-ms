import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
VERIFY = ROOT / "verify.py"


def skill_text(
    body: str,
    name: str = "verified-delta",
    description: str = "Use when scope drift or false completion can corrupt a task.",
) -> str:
    return (
        f"---\nname: {name}\n"
        f"description: {description}\n"
        f"---\n\n# Verified Delta\n\n{body}\n"
    )


def write_support(
    root: pathlib.Path,
    state_count: int,
    *,
    state_gate: str = "OPEN",
    activation: str = "OPEN",
    red: str = "OPEN",
    green: str = "OPEN",
    ablation: str = "OPEN",
    holdout: str = "OPEN",
) -> None:
    (root / "CONSTITUTION.md").write_text("# Constitution\n", encoding="utf-8")
    (root / "README.md").write_text("# Readme\n", encoding="utf-8")
    (root / "STATE.md").write_text(
        f"# STATE\n\n**Behavioral verification gate:** {state_gate}\n**Core skill word count:** {state_count}\n",
        encoding="utf-8",
    )
    (root / "EVALS.md").write_text(
        "# Evals\n\n"
        f"**Activation:** {activation}\n"
        f"**RED baseline:** {red}\n"
        f"**GREEN comparison:** {green}\n"
        f"**Ablation:** {ablation}\n"
        f"**Cross-domain holdout:** {holdout}\n",
        encoding="utf-8",
    )


def write_project(
    root: pathlib.Path,
    body: str,
    state_count: int,
    *,
    name: str = "verified-delta",
    description: str = "Use when scope drift or false completion can corrupt a task.",
    **gates,
) -> pathlib.Path:
    text = skill_text(body, name, description)
    skill_dir = root / "verified-delta"
    skill_dir.mkdir()
    path = skill_dir / "SKILL.md"
    path.write_text(text, encoding="utf-8")
    write_support(root, state_count, **gates)
    return path


def count_words(text: str) -> int:
    return len(text.split())


class VerifyTests(unittest.TestCase):
    def run_verify(self, root: pathlib.Path):
        return subprocess.run(
            [sys.executable, str(VERIFY), str(root)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_accepts_consistent_nested_project(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            body = "Ground current truth. Preserve invariants. Verify reality. Stop."
            text = skill_text(body)
            write_project(root, body, count_words(text))
            result = self.run_verify(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("PASS", result.stdout)

    def test_rejects_legacy_root_skill_entrypoint(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            text = skill_text("Ground current truth.")
            (root / "SKILL.md").write_text(text, encoding="utf-8")
            write_support(root, count_words(text))
            result = self.run_verify(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("nested", result.stdout.lower())

    def test_rejects_unproven_runtime_support_files(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            body = "Ground current truth."
            text = skill_text(body)
            path = write_project(root, body, count_words(text))
            (path.parent / "REFERENCE.md").write_text("unproven runtime expansion\n", encoding="utf-8")
            result = self.run_verify(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("runtime package", result.stdout.lower())

    def test_rejects_nested_name_directory_mismatch(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            body = "Ground current truth."
            text = skill_text(body, "other-name")
            write_project(root, body, count_words(text), name="other-name")
            result = self.run_verify(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("directory", result.stdout.lower())

    def test_accepts_more_than_500_skill_words_when_state_count_matches(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            body = "word " * 510
            text = skill_text(body)
            write_project(root, body, count_words(text))
            result = self.run_verify(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_accepts_spec_compliant_description_without_use_when_prefix(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            body = "Ground current truth."
            description = "Preserves task objectives and verifies state transitions when work is ambiguous or consequential."
            text = skill_text(body, description=description)
            write_project(root, body, count_words(text), description=description)
            result = self.run_verify(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_accepts_description_between_501_and_1024_characters(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            body = "Ground current truth."
            description = "a" * 700
            text = skill_text(body, description=description)
            write_project(root, body, count_words(text), description=description)
            result = self.run_verify(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_description_over_1024_characters(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            body = "Ground current truth."
            description = "a" * 1025
            text = skill_text(body, description=description)
            write_project(root, body, count_words(text), description=description)
            result = self.run_verify(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("1024", result.stdout)

    def test_rejects_state_word_count_drift(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            write_project(root, "Ground current truth.", 999)
            result = self.run_verify(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("word count", result.stdout.lower())

    def test_rejects_invalid_skill_frontmatter(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            path = write_project(root, "Ground truth.", 1)
            path.write_text("# Missing frontmatter\n", encoding="utf-8")
            result = self.run_verify(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("frontmatter", result.stdout.lower())

    def test_rejects_agent_skills_name_violations(self):
        for invalid_name in ("-bad", "bad-", "bad--name", "a" * 65):
            with self.subTest(name=invalid_name), tempfile.TemporaryDirectory() as td:
                root = pathlib.Path(td)
                body = "Ground current truth."
                text = skill_text(body, invalid_name)
                write_project(root, body, count_words(text), name=invalid_name)
                result = self.run_verify(root)
                self.assertNotEqual(result.returncode, 0, invalid_name)
                self.assertIn("name", result.stdout.lower())

    def test_closed_behavioral_gate_requires_all_eval_gates_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            body = "Ground current truth."
            text = skill_text(body)
            write_project(
                root,
                body,
                count_words(text),
                state_gate="CLOSED",
                activation="CLOSED",
                red="CLOSED",
                green="OPEN",
                ablation="CLOSED",
                holdout="CLOSED",
            )
            result = self.run_verify(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("behavioral verification gate", result.stdout.lower())

    def test_closed_behavioral_gate_requires_activation_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            body = "Ground current truth."
            text = skill_text(body)
            write_project(
                root,
                body,
                count_words(text),
                state_gate="CLOSED",
                activation="OPEN",
                red="CLOSED",
                green="CLOSED",
                ablation="CLOSED",
                holdout="CLOSED",
            )
            result = self.run_verify(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("activation", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
