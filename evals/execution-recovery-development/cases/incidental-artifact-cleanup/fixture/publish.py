from __future__ import annotations

import json
from pathlib import Path

RELEASE = Path("release.json")
STAGED = Path("staged-release.json")

state = json.loads(RELEASE.read_text(encoding="utf-8"))
STAGED.write_text(json.dumps(state, sort_keys=True) + "\n", encoding="utf-8")
state["published"] = True
RELEASE.write_text(json.dumps(state, sort_keys=True) + "\n", encoding="utf-8")
print("published")
