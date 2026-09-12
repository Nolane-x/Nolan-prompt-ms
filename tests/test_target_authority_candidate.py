import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "verified-delta" / "SKILL.md"
CANDIDATE = ROOT / "evals" / "candidates" / "r1-target-authority.md"
TARGET_RULE = (
    "**Hold the target boundary.** If observable behavior already satisfies the user-stated "
    "target under a discriminating probe and no evidence establishes another required defect, "
    "preserve the implementation; do not widen `S*` to justify a change."
)


class TargetAuthorityCandidateTests(unittest.TestCase):
    def test_candidate_is_exact_r1_plus_one_target_authority_rule(self):
        self.assertTrue(CANDIDATE.is_file(), "experimental target-authority candidate must exist")
        skill_lines = SKILL.read_text(encoding="utf-8").splitlines()
        candidate_lines = CANDIDATE.read_text(encoding="utf-8").splitlines()

        extras = []
        skill_index = 0
        for line in candidate_lines:
            if skill_index < len(skill_lines) and line == skill_lines[skill_index]:
                skill_index += 1
            else:
                extras.append(line)

        self.assertEqual(skill_index, len(skill_lines), "candidate must preserve every R1 line in order")
        self.assertEqual(extras, [TARGET_RULE], "candidate may add exactly one semantic rule")
        self.assertEqual(candidate_lines.count(TARGET_RULE), 1)


if __name__ == "__main__":
    unittest.main()
