#!/usr/bin/env python3
"""Validate JSON manifests in this repo."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "launa"
PLUGIN_VERSION = "0.1.2"
MCP_URL = "https://mcp.launa.io/mcp"
MCP_CONFIGS = {
    ROOT / ".mcp.json",
    PLUGIN / "mcp.json",
    PLUGIN / ".mcp.json",
    PLUGIN / ".claude-plugin" / "plugin.json",
}

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
    "sandbox",
    "analytics",
}

COMMANDS = {"wrap", "price", "discover", "domain", "cors"}


def manifest_errors(path: Path, data: dict) -> list[str]:
    errors = []
    if path.name == "plugin.json" and data.get("version") != PLUGIN_VERSION:
        errors.append(f"plugin version must be {PLUGIN_VERSION}")
    if "homepage" in data and data["homepage"] != "https://launa.io":
        errors.append("plugin Website/homepage must be https://launa.io")
    if path in MCP_CONFIGS:
        server = data.get("mcpServers", {}).get("launa", {})
        if server.get("url") != MCP_URL or server.get("type") not in {"http", "streamable-http"}:
            errors.append("MCP must use hosted Streamable HTTP")
        if any(key in server for key in ("command", "args", "env", "headers")):
            errors.append("Hosted MCP must not ship local launch settings or credentials")
    if path.parent.name in {".cursor-plugin", ".claude-plugin"} and path.name == "marketplace.json":
        entries = data.get("plugins", [])
        if not entries or any(entry.get("version") != PLUGIN_VERSION for entry in entries):
            errors.append(f"marketplace plugin versions must be {PLUGIN_VERSION}")
    return errors


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
            continue
        for error in manifest_errors(path, data):
            print(f"{path.relative_to(ROOT)}: {error}", file=sys.stderr)
            errors += 1
        if path.name == "plugin.json" and "version" in data:
            versions.add(data["version"])
    return errors, versions


def report_missing(paths: list[Path]) -> int:
    errors = 0
    for path in paths:
        if not path.is_file():
            print(f"missing {path.relative_to(ROOT)}", file=sys.stderr)
            errors += 1
    return errors


def validate_listing() -> int:
    portable = json.loads((PLUGIN / "plugin.json").read_text())
    fallback = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text())
    cursor = json.loads((PLUGIN / ".cursor-plugin" / "plugin.json").read_text())
    marketplace = json.loads((ROOT / ".cursor-plugin" / "marketplace.json").read_text())
    interface = portable["extensions"]["com.openai"]["interface"]
    discovery = (PLUGIN / "skills/discovery/SKILL.md").read_text()
    checks = {
        "Cursor must use the square icon": cursor["logo"] == "assets/icon.svg",
        "Cursor marketplace must use the square icon":
            marketplace["plugins"][0]["logo"] == "plugins/launa/assets/icon.svg",
        "Cursor must use the hosted OAuth endpoint":
            cursor["mcpServers"]["launa"].get("url") == "https://mcp.launa.io/mcp",
        "Cursor must declare the registered public OAuth client":
            cursor["mcpServers"]["launa"].get("auth", {}).get("CLIENT_ID") == "launa-cursor",
        "Cursor must not request API keys or ship credentials":
            "variables" not in cursor and "headers" not in cursor["mcpServers"]["launa"]
            and "env" not in cursor["mcpServers"]["launa"]
            and "CLIENT_SECRET" not in cursor["mcpServers"]["launa"].get("auth", {}),
        "Cursor must omit local buyer skills and commands":
            "skills/inspect-pay" not in cursor.get("skills", [])
            and "commands/inspect.md" not in cursor.get("commands", [])
            and len(cursor.get("skills", [])) == 8 and len(cursor.get("commands", [])) == 5,
        "Cursor OAuth scopes must match developer control-plane access":
            set(cursor["mcpServers"]["launa"]["auth"]["scopes"]) == {
                "apis:read", "apis:write", "endpoints:read", "endpoints:write",
                "domains:read", "domains:write", "stats:read", "settlements:read",
                "openapi:read", "billing:read", "income:read"
            },
        "OpenAI listing metadata differs between manifests": interface == fallback["interface"],
        "OpenAI subtitle must contain 1–30 characters": 0 < len(interface["shortDescription"]) <= 30,
        "OpenAI support URL must use HTTPS": interface.get("supportURL", "").startswith("https://"),
        "OpenAI primary icon must use the square asset": interface["logo"] == "./assets/icon.svg",
        "OpenAI light-theme color must use brand ink": interface["brandColor"] == "#0E1301",
        "OpenAI dark-theme color must use brand lime": interface["brandColorDark"] == "#B8E961",
        "discovery helper must use its reviewed pin":
            "@agentcash/discovery@1.7.5" in discovery and "@latest" not in discovery,
    }
    failures = [message for message, passed in checks.items() if not passed]
    for message in failures:
        print(message, file=sys.stderr)
    return len(failures)


def validate_oauth_config() -> int:
    claude = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text())
    portable = json.loads((PLUGIN / "mcp.json").read_text())
    checks = {
        "Claude must use browser OAuth without API-key onboarding": "userConfig" not in claude,
        "OpenAI portable MCP must declare OAuth DCR": portable["mcpServers"]["launa"].get("extensions", {}).get("com.openai", {}).get("auth") == {"type": "oauth", "client": {"mode": "dcr"}},
        "Hosted bundle must contain only developer skills": {x.name for x in (PLUGIN / "skills").iterdir() if (x / "SKILL.md").is_file()} == SKILLS,
        "Hosted bundle must contain only developer commands": {x.stem for x in (PLUGIN / "commands").glob("*.md")} == COMMANDS,
    }
    for message, passed in checks.items():
        if not passed:
            print(message, file=sys.stderr)
    return sum(not passed for passed in checks.values())


def main() -> int:
    errors, versions = validate_json_files()
    expected_files = [
        *(PLUGIN / "skills" / name / "SKILL.md" for name in sorted(SKILLS)),
        *(PLUGIN / "commands" / f"{name}.md" for name in sorted(COMMANDS)),
        *(PLUGIN / "references" / name for name in ("mcp-cli-map.md", "scopes.md", "safety.md")),
        PLUGIN / "rules" / "launa.mdc",
        PLUGIN / "assets" / "logo.svg",
        PLUGIN / "assets" / "icon.svg",
    ]
    errors += report_missing(expected_files)

    if versions != {PLUGIN_VERSION}:
        print(f"plugin manifest versions do not match {PLUGIN_VERSION}: {sorted(versions)}", file=sys.stderr)
        errors += 1

    if errors:
        print(f"{errors} error(s)", file=sys.stderr)
        return 1
    errors += validate_listing() + validate_oauth_config()
    if errors:
        print(f"{errors} listing/configuration error(s)", file=sys.stderr)
        return 1
    print(f"ok ({len(REQUIRED)} json files, {len(SKILLS)} skills, {len(COMMANDS)} commands)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
