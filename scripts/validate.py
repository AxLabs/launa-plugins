#!/usr/bin/env python3
"""Validate JSON manifests in this repo."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "launa"

REQUIRED = [
    ROOT / ".cursor-plugin" / "marketplace.json",
    ROOT / ".claude-plugin" / "marketplace.json",
    ROOT / ".grok-plugin" / "marketplace.json",
    ROOT / ".agents" / "plugins" / "marketplace.json",
    ROOT / ".mcp.json",
    PLUGIN / "plugin.json",
    PLUGIN / "mcp.json",
    PLUGIN / ".mcp.json",
    PLUGIN / ".cursor-plugin" / "plugin.json",
    PLUGIN / ".claude-plugin" / "plugin.json",
    PLUGIN / ".grok-plugin" / "plugin.json",
    PLUGIN / ".codex-plugin" / "plugin.json",
]

SKILLS = {
    "setup",
    "wrap-api",
    "price-endpoints",
    "discovery",
    "custom-domain",
    "cors",
    "inspect-pay",
    "sandbox",
    "analytics",
}

COMMANDS = {"wrap", "price", "discover", "domain", "inspect", "cors"}


def validate_json_files() -> tuple[int, set[str]]:
    errors = 0
    versions: set[str] = set()
    for path in REQUIRED:
        if not path.is_file():
            print(f"missing {path.relative_to(ROOT)}", file=sys.stderr)
            errors += 1
            continue
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            print(f"invalid JSON {path.relative_to(ROOT)}: {exc}", file=sys.stderr)
            errors += 1
            continue
        if not isinstance(data, dict):
            print(f"not an object {path.relative_to(ROOT)}", file=sys.stderr)
            errors += 1
        if path.name == "plugin.json" and isinstance(data, dict) and "version" in data:
            versions.add(data["version"])
    return errors, versions


def report_missing(paths: list[Path]) -> int:
    errors = 0
    for path in paths:
        if not path.is_file():
            print(f"missing {path.relative_to(ROOT)}", file=sys.stderr)
            errors += 1
    return errors


def main() -> int:
    errors, versions = validate_json_files()
    expected_files = [
        *(PLUGIN / "skills" / name / "SKILL.md" for name in sorted(SKILLS)),
        *(PLUGIN / "commands" / f"{name}.md" for name in sorted(COMMANDS)),
        *(PLUGIN / "references" / name for name in ("mcp-cli-map.md", "scopes.md", "safety.md")),
        PLUGIN / "rules" / "launa.mdc",
        PLUGIN / "assets" / "logo.svg",
    ]
    errors += report_missing(expected_files)

    if versions != {"0.1.0"}:
        print(f"plugin manifest versions do not match 0.1.0: {sorted(versions)}", file=sys.stderr)
        errors += 1

    if errors:
        print(f"{errors} error(s)", file=sys.stderr)
        return 1
    print(f"ok ({len(REQUIRED)} json files, {len(SKILLS)} skills, {len(COMMANDS)} commands)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
