import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = ROOT / "selection_validation.py"
CASE_KEYS = {
    "config-noop",
    "config-required",
    "writing-noop",
    "writing-required",
    "data-noop",
    "data-required",
}


class SelectionValidationHarnessTests(unittest.TestCase):
    def run_harness(self, *args):
        return subprocess.run(
            [sys.executable, str(HARNESS), *map(str, args)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def generate(self, root, name="pack.json"):
        path = pathlib.Path(root) / name
        result = self.run_harness("generate", path, "--seed", "fixed-selection-seed", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        return path, json.loads(path.read_text(encoding="utf-8"))

    def test_generate_is_deterministic_balanced_and_cross_domain(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, first = self.generate(tmp)
            _, second = self.generate(tmp, "pack-2.json")
            self.assertEqual(first, second)
            self.assertEqual(first["schema_version"], 1)
            self.assertEqual(set(first["cases"]), CASE_KEYS)
            self.assertEqual(
                {case["domain"] for case in first["cases"].values()},
                {"config", "writing", "data"},
            )
            self.assertEqual(
                {case["mode"] for case in first["cases"].values()},
                {"noop", "required"},
            )

    def test_redacted_agent_pack_contains_no_seed_or_expected_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack_path, _ = self.generate(tmp)
            agent_pack = pathlib.Path(tmp) / "agent-pack.json"
            result = self.run_harness("redact", pack_path, agent_pack, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            raw = agent_pack.read_text(encoding="utf-8")
            payload = json.loads(raw)
            self.assertNotIn("seed", raw.lower())
            self.assertNotIn("expected", raw.lower())
            self.assertEqual(set(payload["cases"]), CASE_KEYS)
            self.assertIn("source_pack_sha256", payload)

            workspace = pathlib.Path(tmp) / "agent-workspace"
            result = self.run_harness("prepare-agent", agent_pack, "writing-noop", workspace, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            prepared = json.loads(result.stdout)
            self.assertEqual(set(prepared), {"case_id", "workspace", "prompt"})

    def test_prepare_hides_expected_state_and_grade_enforces_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack_path, pack = self.generate(tmp)

            noop = pathlib.Path(tmp) / "noop"
            result = self.run_harness("prepare", pack_path, "config-noop", noop, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            prepared = json.loads(result.stdout)
            self.assertEqual(set(prepared), {"case_id", "workspace", "prompt"})
            self.assertNotIn("expected", json.dumps(prepared).lower())
            grade = self.run_harness("grade", pack_path, "config-noop", noop, "--json")
            self.assertEqual(grade.returncode, 0, grade.stderr)
            self.assertTrue(json.loads(grade.stdout)["passed"])

            required = pathlib.Path(tmp) / "required"
            result = self.run_harness("prepare", pack_path, "config-required", required, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            grade = self.run_harness("grade", pack_path, "config-required", required, "--json")
            self.assertEqual(grade.returncode, 0, grade.stderr)
            self.assertFalse(json.loads(grade.stdout)["passed"])

            expected = pack["cases"]["config-required"]["expected_files"]
            for relative, content in expected.items():
                target = required / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
            grade = self.run_harness("grade", pack_path, "config-required", required, "--json")
            self.assertEqual(grade.returncode, 0, grade.stderr)
            self.assertTrue(json.loads(grade.stdout)["passed"])

            (required / "unrequested.txt").write_text("scope drift\n", encoding="utf-8")
            grade = self.run_harness("grade", pack_path, "config-required", required, "--json")
            self.assertEqual(grade.returncode, 0, grade.stderr)
            self.assertFalse(json.loads(grade.stdout)["passed"])


if __name__ == "__main__":
    unittest.main()
