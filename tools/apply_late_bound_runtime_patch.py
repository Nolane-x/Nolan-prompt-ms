#!/usr/bin/env python3
from pathlib import Path

WORKFLOW = Path('.github/workflows/execution-recovery-development.yml')
TESTS = Path('tests/test_execution_recovery_development_cases.py')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly one match, found {count}')
    return text.replace(old, new, 1)


workflow = WORKFLOW.read_text(encoding='utf-8')

old_gate = '''          python - \\
            "$TRIAL_ROOT/seed-attestation.json" \\
            "$TRIAL_ROOT/runtime-attestation.json" <<'PY'\n          import json\n          import pathlib\n          import sys\n\n          seed = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))\n          attestation = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))\n          if seed["model"] != attestation["model"]:\n              raise SystemExit("session fork runtime mismatch: model")\n          if seed["reasoning_effort"] != attestation["reasoning_effort"]:\n              raise SystemExit("session fork runtime mismatch: reasoning effort")\n          if seed["tool_set"] != attestation["tool_set"]:\n              raise SystemExit("session fork runtime mismatch: tool set")\n          PY\n\n'''
workflow = replace_once(workflow, old_gate, '', 'seed-vs-resume runtime gate')

workflow = replace_once(
    workflow,
    'HARNESS_ID: github-copilot-execution-recovery-dev-v3-tar-session-fork',
    'HARNESS_ID: github-copilot-execution-recovery-dev-v4-late-bound-runtime',
    'harness identity',
)

old_args = '''            "$TRIAL_ROOT/run-config.json" \\
            "$CONDITION" \\
            "$TRIAL_ROOT/runtime-attestation.json" \\
            "$MODEL_ID" \\
'''
new_args = '''            "$TRIAL_ROOT/run-config.json" \\
            "$CONDITION" \\
            "$TRIAL_ROOT/runtime-attestation.json" \\
            "$TRIAL_ROOT/seed-attestation.json" \\
            "$MODEL_ID" \\
'''
workflow = replace_once(workflow, old_args, new_args, 'run-config arguments')

old_unpack = '''              output,\n              condition,\n              attestation_path,\n              requested_model_id,\n'''
new_unpack = '''              output,\n              condition,\n              attestation_path,\n              seed_attestation_path,\n              requested_model_id,\n'''
workflow = replace_once(workflow, old_unpack, new_unpack, 'run-config unpack')

old_load = '''          attestation = json.loads(pathlib.Path(attestation_path).read_text(encoding="utf-8"))\n          is_u1 = condition == "U1"\n'''
new_load = '''          attestation = json.loads(pathlib.Path(attestation_path).read_text(encoding="utf-8"))\n          seed_attestation = json.loads(pathlib.Path(seed_attestation_path).read_text(encoding="utf-8"))\n          is_u1 = condition == "U1"\n'''
workflow = replace_once(workflow, old_load, new_load, 'seed attestation load')

old_fork = '''                  "session_fork": {\n                      "protocol": "copilot-local-session-resume-v2-tar",\n                      "session_id": session_id,\n                      "pre_treatment_state_sha256": pre_treatment_state_sha256,\n                      "transport_archive_sha256": transport_archive_sha256,\n                  },\n'''
new_fork = '''                  "session_fork": {\n                      "protocol": "copilot-local-session-resume-v3-late-bound-runtime",\n                      "session_id": session_id,\n                      "pre_treatment_state_sha256": pre_treatment_state_sha256,\n                      "transport_archive_sha256": transport_archive_sha256,\n                      "seed_runtime": {\n                          "model": seed_attestation["model"],\n                          "reasoning_effort": seed_attestation["reasoning_effort"],\n                          "tool_set": seed_attestation["tool_set"],\n                      },\n                  },\n'''
workflow = replace_once(workflow, old_fork, new_fork, 'session-fork provenance')
WORKFLOW.write_text(workflow, encoding='utf-8', newline='\n')

tests = TESTS.read_text(encoding='utf-8')
old_test = '''        for needle in [\n            '\"remoteExport\": false',\n            'PRE_TREATMENT_STATE_SHA256',\n            'seed[\"model\"] != attestation[\"model\"]',\n            'seed[\"reasoning_effort\"] != attestation[\"reasoning_effort\"]',\n            'seed[\"tool_set\"] != attestation[\"tool_set\"]',\n            '\"session_fork\": {',\n            '\"session_id\": session_id',\n            '\"pre_treatment_state_sha256\": pre_treatment_state_sha256',\n        ]:\n            self.assertIn(needle, workflow)\n        self.assertIn(\"session fork runtime mismatch\", workflow)\n        self.assertIn(\"session fork state hash mismatch\", workflow)\n        self.assertIn(\"if: always()\", workflow)\n'''
new_test = '''        for needle in [\n            '\"remoteExport\": false',\n            'PRE_TREATMENT_STATE_SHA256',\n            '\"session_fork\": {',\n            '\"session_id\": session_id',\n            '\"pre_treatment_state_sha256\": pre_treatment_state_sha256',\n            '\"seed_runtime\": {',\n            '\"model\": seed_attestation[\"model\"]',\n            '\"reasoning_effort\": seed_attestation[\"reasoning_effort\"]',\n            '\"tool_set\": seed_attestation[\"tool_set\"]',\n        ]:\n            self.assertIn(needle, workflow)\n        self.assertNotIn('seed[\"model\"] != attestation[\"model\"]', workflow)\n        self.assertNotIn('seed[\"reasoning_effort\"] != attestation[\"reasoning_effort\"]', workflow)\n        self.assertNotIn('seed[\"tool_set\"] != attestation[\"tool_set\"]', workflow)\n        self.assertNotIn(\"session fork runtime mismatch\", workflow)\n        self.assertIn(\"session fork state hash mismatch\", workflow)\n        self.assertIn(\"if: always()\", workflow)\n'''
tests = replace_once(tests, old_test, new_test, 'session-fork contract test')
TESTS.write_text(tests, encoding='utf-8', newline='\n')
