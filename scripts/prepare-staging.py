#!/usr/bin/env python3
"""Create a clean, credential-free staging plugin copy for native client testing."""
import json
import shutil
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
destination = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else None
if destination is None or destination.exists() or destination.is_relative_to(root):
    raise SystemExit("Usage: prepare-staging.py NEW_DIRECTORY_OUTSIDE_REPOSITORY")
shutil.copytree(root / "plugins/launa", destination)
for path in destination.rglob("*.json"):
    data = path.read_text()
    if "https://mcp.launa.io" in data:
        data = data.replace("https://mcp.launa.io", "https://mcp.staging.launa.io")
        json.loads(data)
        path.write_text(data)
print(f"Staging plugin prepared at {destination}")
