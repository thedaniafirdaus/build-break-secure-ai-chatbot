"""Approve knowledge-base documents by recording their SHA-256 fingerprint.
In a real company, only a reviewer runs this after checking a document change."""
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).parent
APPROVED = ["faq.md", "policies.md"]   # internal_staff_notes.md is deliberately NOT approved

manifest = {name: hashlib.sha256((BASE / "kb" / name).read_bytes()).hexdigest() for name in APPROVED}
(BASE / "kb_manifest.json").write_text(json.dumps(manifest, indent=2))
print(json.dumps(manifest, indent=2))
