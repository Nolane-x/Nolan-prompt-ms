#!/usr/bin/env bash
set -euo pipefail
python - <<'PY'
import json
from pathlib import Path
path = Path('rollout.json')
state = json.loads(path.read_text(encoding='utf-8'))
state['channel'] = 'stable'
path.write_text(json.dumps(state, sort_keys=True) + '\n', encoding='utf-8')
PY
