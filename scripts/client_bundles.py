#!/usr/bin/env python3
"""Build Antigravity, Claude Desktop and Copilot plugins from shared content."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/launa"
CLIENTS = ("antigravity", "claude-desktop", "copilot")


def json_bytes(value: dict) -> bytes:
    return (json.dumps(value, indent=2) + "\n").encode()


def bundle_files(client: str, environment: str = "production") -> dict[str, bytes]:
    if client not in CLIENTS or environment not in {"production", "staging"}:
        raise ValueError("Unknown client or service environment")
    source = json.loads((PLUGIN / "plugin.json").read_text())
    rules = (PLUGIN / "rules/launa.mdc").read_text().split("---", 2)[2].strip()
    files = {"LICENSE": (ROOT / "LICENSE").read_bytes()}
    for folder in ("assets", "references"):
        for path in sorted((PLUGIN / folder).rglob("*")):
            if path.is_file():
                files[path.relative_to(PLUGIN).as_posix()] = path.read_bytes()
    for path in sorted((PLUGIN / "skills").glob("*/SKILL.md")):
        content = path.read_text()
        # Claude does not automatically load Cursor .mdc rules. Keep the shared
        # safety contract in each workflow, independent of client rules support.
        content += "\n## Launa operation rules\n\n" + rules + "\n"
        files[path.relative_to(PLUGIN).as_posix()] = content.encode()
    files["README.md"] = (ROOT / "docs" / f"{client}.md").read_bytes()
    url = "https://mcp.launa.io/mcp"
    if environment == "staging":
        url = "https://mcp.staging.launa.io/mcp"
    if client == "antigravity":
        manifest = {key: source[key] for key in (
            "name", "version", "description", "author", "homepage", "repository", "license", "keywords"
        )}
        manifest.update({
            "$schema": "https://antigravity.google/schemas/v1/plugin.json",
            "displayName": "Launa",
            "logo": "assets/icon.svg",
            "suggestedPrompts": [
                "List my Launa APIs and their priced endpoints.",
                "Show my API usage and income for the last seven days.",
                "Help me set up a Sandbox API. Ask for any required information I haven't provided.",
            ],
        })
        files["plugin.json"] = json_bytes(manifest)
        # Native Antigravity manifests use mcp_config.json on both IDE and CLI.
        # agy 1.4.11 strict validation rejects mcp.json for this schema.
        config = json_bytes({"mcpServers": {"launa": {"serverUrl": url}}})
        files["mcp_config.json"] = config
        files["rules/AGENTS.md"] = (rules + "\n").encode()
    elif client == "copilot":
        manifest = {key: value for key, value in source.items() if key != "extensions"}
        files["plugin.json"] = json_bytes(manifest)
        files["mcp.json"] = json_bytes({
            "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
            "mcpServers": {"launa": {"type": "streamable-http", "url": url}},
        })
    else:
        manifest = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text())
        # A single .mcp.json definition works for Desktop, Cowork and Code.
        manifest.pop("mcpServers", None)
        files[".claude-plugin/plugin.json"] = json_bytes(manifest)
        files[".mcp.json"] = json_bytes({"mcpServers": {"launa": {"type": "http", "url": url}}})
        for path in sorted((PLUGIN / "commands").glob("*.md")):
            files[path.relative_to(PLUGIN).as_posix()] = (
                path.read_text() + "\n## Launa operation rules\n\n" + rules + "\n"
            ).encode()
    return files


def check_bundles() -> list[str]:
    errors = []
    for client in CLIENTS:
        directory = ROOT / "bundles" / client / "launa"
        expected = bundle_files(client)
        for name, data in expected.items():
            path = directory / name
            if not path.is_file() or path.read_bytes() != data:
                errors.append(f"Missing or stale {client} bundle file: {name}")
        actual = {p.relative_to(directory).as_posix() for p in directory.rglob("*") if p.is_file()}
        errors.extend(f"Unexpected {client} bundle file: {name}" for name in sorted(actual - expected.keys()))
    return errors


def write_bundle(directory: Path, files: dict[str, bytes]) -> None:
    # Refuse to silently ship leftovers or overwrite files outside the output via symlinks.
    if directory.is_symlink() or any(p.is_symlink() for p in directory.rglob("*")):
        raise ValueError(f"Symlinks are not supported in bundle output: {directory}")
    actual = {p.relative_to(directory).as_posix() for p in directory.rglob("*") if p.is_file()}
    if actual - files.keys():
        raise ValueError(f"Unexpected files in {directory}: {sorted(actual - files.keys())}")
    for name, data in files.items():
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def write_archive(path: Path, files: dict[str, bytes]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path, "w", compression=ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            info = ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check committed production bundles for drift")
    parser.add_argument("--environment", choices=("production", "staging"), default="production")
    args = parser.parse_args()
    if args.check:
        if args.environment != "production":
            parser.error("--check applies to the committed production bundles")
        errors = check_bundles()
        print("\n".join(errors) if errors else "Client bundles match shared plugin content")
        return bool(errors)
    version = json.loads((PLUGIN / "plugin.json").read_text())["version"]
    for client in CLIENTS:
        files = bundle_files(client, args.environment)
        if args.environment == "production":
            write_bundle(ROOT / "bundles" / client / "launa", files)
        else:
            write_bundle(ROOT / "dist/staging" / client / "launa", files)
        suffix = "-staging" if args.environment == "staging" else ""
        path = ROOT / "dist" / f"launa-{client}-{version}{suffix}.zip"
        write_archive(path, files)
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
