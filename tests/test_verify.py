import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
VERIFY = ROOT / "verify.py"


def write_project(root: pathlib.Path, skill_body: str, state_count: int, *, state_gate: str = "OPEN", red: str = "OPEN", green: str = "OPEN", ablation: str = "OPEN", holdout: str = "OPEN") -> None:
    skill = f"---\nname: verified-delta\ndescription: Use when scope drift or false completion can corrupt a task.\n---\n\n# Verified Delta\n\n{skill_body}\n"
    (root / "SKILL.md").write_text(skill, encoding="utf-8")
    (root / "CONSTITUTION.md").write_text("# Constitution\n", encoding="utf-8")
    (root / "README.md").write_text("# Readme\n", encoding="utf-8")
    (root / "STATE.md").write_text(
        f"# STATE\n\n**Behavioral verification gate:** {state_gate}\n**Core skill word count:** {state_count}\n",
        encoding="utf-8",
    )
    (root / "EVALS.md").write_text(
        "# Evals\n\n"
        f"**RED baseline:** {red}\n"
        f"**GREEN comparison:** {green}\n"
        f"**Ablation:** {ablation}\n"
        f"**Cross-domain holdout:** {holdout}\n",
        encoding="utf-8",
    )


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

    def test_accepts_consistent_open_project(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            body = "Ground current truth. Preserve invariants. Verify reality. Stop."
            skill = f"---\nname: verified-delta\ndescription: Use when scope drift or false completion can corrupt a task.\n---\n\n# Verified Delta\n\n{body}\n"
            write_project(root, body, count_words(skill))
            result = self.run_verify(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("PASS", result.stdout)

    def test_rejects_more_than_500_skill_words(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            body = "word " * 510
            skill = f"---\nname: verified-delta\ndescription: Use when scope drift or false completion can corrupt a task.\n---\n\n# Verified Delta\n\n{body}\n"
            write_project(root, body, count_words(skill))
            result = self.run_verify(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("500", result.stdout)

    def test_rejects_state_word_count_drift(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            body = "Ground current truth."
            write_project(root, body, 999)
            result = self.run_verify(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("word count", result.stdout.lower())

    def test_rejects_invalid_skill_frontmatter(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            write_project(root, "Ground truth.", 1)
            (root / "SKILL.md").write_text("# Missing frontmatter\n", encoding="utf-8")
            result = self.run_verify(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("frontmatter", result.stdout.lower())

    def test_closed_behavioral_gate_requires_all_eval_gates_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            body = "Ground current truth."
            skill = f"---\nname: verified-delta\ndescription: Use when scope drift or false completion can corrupt a task.\n---\n\n# Verified Delta\n\n{body}\n"
            write_project(root, body, count_words(skill), state_gate="CLOSED", red="CLOSED", green="OPEN", ablation="CLOSED", holdout="CLOSED")
            result = self.run_verify(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("behavioral verification gate", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
