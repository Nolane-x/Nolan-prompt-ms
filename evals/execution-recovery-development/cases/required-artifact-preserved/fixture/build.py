from __future__ import annotations

import json
from pathlib import Path

SOURCE = Path("source.json")
BUNDLE = Path("bundle.json")
MANIFEST = Path("manifest.json")

source = json.loads(SOURCE.read_text(encoding="utf-8"))
bundle = {"built": True, "status": source["status"], "version": source["version"]}
manifest = {"artifact": "bundle.json", "version": source["version"]}
BUNDLE.write_text(json.dumps(bundle, sort_keys=True) + "\n", encoding="utf-8")
MANIFEST.write_text(json.dumps(manifest, sort_keys=True) + "\n", encoding="utf-8")
print("built bundle.json and manifest.json")
