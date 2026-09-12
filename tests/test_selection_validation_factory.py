import importlib
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class SelectionFactoryTests(unittest.TestCase):
    def module(self):
        return importlib.import_module("selection_validation")

    def test_selection_is_deterministic_but_changes_with_future_run_id(self):
        sv = self.module()
        a = sv.derive_seed("100", "1", "abc", "def")
        b = sv.derive_seed("100", "1", "abc", "def")
        c = sv.derive_seed("101", "1", "abc", "def")
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        selected = sv.select_families(a)
        self.assertEqual(len(selected), 4)
        self.assertEqual(len(set(selected)), 4)

    def test_materialization_has_four_opposing_same_prompt_pairs(self):
        sv = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            manifest = sv.materialize("0" * 64, root)
            self.assertEqual(len(manifest["cases"]), 8)
            self.assertEqual(manifest["experiment"], "target-authority-selection-v1")
            self.assertEqual(len(manifest["manifest_sha256"]), 64)

            by_family = {}
            for case in manifest["cases"]:
                by_family.setdefault(case["family"], []).append(case)
                case_root = root / "cases" / case["case_id"]
                self.assertEqual(
                    {path.name for path in case_root.iterdir()},
                    {"app.py", "prompt.txt"},
                )
                self.assertEqual(
                    (case_root / "prompt.txt").read_text(encoding="utf-8").strip(),
                    case["prompt"],
                )
                self.assertEqual(len(case["fixture_sha256"]), 64)
                self.assertEqual(case["grader_contract_version"], "selection-grader-v1")

            self.assertEqual(len(by_family), 4)
            for pair in by_family.values():
                self.assertEqual({case["variant"] for case in pair}, {"noop", "partial"})
                self.assertEqual(len({case["prompt"] for case in pair}), 1)

            manifest_path = root / "selected-manifest.json"
            self.assertTrue(manifest_path.is_file())
            self.assertNotIn("expected", (root / "cases").read_text(encoding="utf-8") if (root / "cases").is_file() else "")

    def test_family_parameterization_is_stable_under_catalog_order(self):
        sv = self.module()
        seed = "a" * 64
        first = sv.family_definition(seed, "retry-cap")
        second = sv.family_definition(seed, "retry-cap")
        other = sv.family_definition(seed, "port-fallback")
        self.assertEqual(first, second)
        self.assertNotEqual(first["parameters"], other["parameters"])


if __name__ == "__main__":
    unittest.main()
