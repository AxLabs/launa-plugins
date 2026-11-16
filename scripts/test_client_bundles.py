import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile

import client_bundles as bundles


class ClientBundleTests(unittest.TestCase):
    def test_workflows_assets_and_rules_are_self_contained(self):
        rules = (bundles.PLUGIN / "rules/launa.mdc").read_text().split("---", 2)[2].strip()
        for client in bundles.CLIENTS:
            with self.subTest(client=client):
                files = bundles.bundle_files(client)
                skills = [name for name in files if name.endswith("/SKILL.md")]
                self.assertEqual(len(skills), 8)
                for name in skills:
                    text = files[name].decode()
                    self.assertIn(rules, text)
                    self.assertIn(f"name: {Path(name).parent.name}\n", text)
                self.assertEqual(files["assets/icon.svg"], (bundles.PLUGIN / "assets/icon.svg").read_bytes())
                self.assertIn("LICENSE", files)
                self.assertIn("references/safety.md", files)
                self.assertFalse(any("gemini-extension" in name or name.endswith(".toml") for name in files))

    def test_native_manifests_and_single_remote_server(self):
        files = bundles.bundle_files("antigravity")
        manifest = json.loads(files["plugin.json"])
        self.assertEqual(manifest["author"]["name"], "AxLabs GmbH")
        self.assertEqual(manifest["displayName"], "Launa")
        self.assertEqual(manifest["homepage"], "https://launa.io")
        self.assertIn(manifest["logo"], files)
        self.assertNotIn("mcp.json", files)
        self.assertEqual(json.loads(files["mcp_config.json"]), {
            "mcpServers": {"launa": {"serverUrl": "https://mcp.launa.io/mcp"}}
        })
        files = bundles.bundle_files("claude-desktop")
        manifest = json.loads(files[".claude-plugin/plugin.json"])
        self.assertNotIn("mcpServers", manifest)
        self.assertEqual(json.loads(files[".mcp.json"]), {
            "mcpServers": {"launa": {"type": "http", "url": "https://mcp.launa.io/mcp"}}
        })
        commands = [name for name in files if name.startswith("commands/")]
        self.assertEqual(len(commands), 5)
        for name in commands:
            self.assertIn(b"## Launa operation rules", files[name])

    def test_copilot_uses_portable_skills_and_mcp_without_other_client_extensions(self):
        files = bundles.bundle_files("copilot")
        manifest = json.loads(files["plugin.json"])
        self.assertEqual(manifest["$schema"], "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json")
        self.assertNotIn("extensions", manifest)
        self.assertEqual(manifest["author"]["name"], "AxLabs GmbH")
        self.assertEqual(json.loads(files["mcp.json"]), {
            "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
            "mcpServers": {"launa": {"type": "streamable-http", "url": "https://mcp.launa.io/mcp"}},
        })
        self.assertNotIn(".mcp.json", files)
        self.assertNotIn(".claude-plugin/plugin.json", files)
        marketplace = json.loads((bundles.ROOT / ".github/plugin/marketplace.json").read_text())
        entry = marketplace["plugins"][0]
        self.assertEqual(entry["source"], "./bundles/copilot/launa")
        self.assertEqual(entry["version"], manifest["version"])

    def test_staging_changes_only_mcp_endpoints(self):
        for client in bundles.CLIENTS:
            production = bundles.bundle_files(client)
            staging = bundles.bundle_files(client, "staging")
            changed = {name for name in production if production[name] != staging[name]}
            expected = {
                "antigravity": {"mcp_config.json"},
                "claude-desktop": {".mcp.json"},
                "copilot": {"mcp.json"},
            }[client]
            self.assertEqual(changed, expected)
            for name in changed:
                self.assertIn(b"https://mcp.staging.launa.io/mcp", staging[name])
                self.assertNotIn(b"https://mcp.launa.io/mcp", staging[name])

    def test_archives_are_reproducible_with_plugin_at_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            for client in bundles.CLIENTS:
                files = bundles.bundle_files(client)
                archive = Path(tmp) / f"{client}.zip"
                bundles.write_archive(archive, files)
                first = archive.read_bytes()
                bundles.write_archive(archive, files)
                self.assertEqual(first, archive.read_bytes())
                with ZipFile(archive) as z:
                    self.assertIsNone(z.testzip())
                    self.assertEqual(set(z.namelist()), set(files))
                    for name in z.namelist():
                        self.assertFalse(Path(name).is_absolute())
                        self.assertNotIn("..", Path(name).parts)
                        self.assertEqual(z.read(name), files[name])

    def test_missing_stale_and_extra_files_fail_validation(self):
        # Keep the real source files, but point only bundle validation at fixtures.
        expected = {client: bundles.bundle_files(client) for client in bundles.CLIENTS}
        with tempfile.TemporaryDirectory() as tmp, patch.object(bundles, "ROOT", Path(tmp)), patch.object(
            bundles, "bundle_files", side_effect=lambda client: expected[client]
        ):
            self.assertTrue(bundles.check_bundles())
            for client, files in expected.items():
                bundles.write_bundle(Path(tmp) / "bundles" / client / "launa", files)
            self.assertEqual(bundles.check_bundles(), [])
            directory = Path(tmp) / "bundles/antigravity/launa"
            (directory / "mcp_config.json").write_text('{}')
            self.assertTrue(any("stale" in e for e in bundles.check_bundles()))
            (directory / "leftover.txt").write_text("must not ship")
            self.assertTrue(any("Unexpected" in e for e in bundles.check_bundles()))
            with self.assertRaisesRegex(ValueError, "Unexpected"):
                bundles.write_bundle(directory, expected["antigravity"])

    def test_build_rejects_symlinks_in_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "untouched"
            target.mkdir()
            output = Path(tmp) / "output"
            output.symlink_to(target, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "Symlinks"):
                bundles.write_bundle(output, {"plugin.json": b"{}"})
            self.assertEqual(list(target.iterdir()), [])

    def test_invalid_environment_is_not_silently_production(self):
        with self.assertRaises(ValueError):
            bundles.bundle_files("antigravity", "typo")


if __name__ == "__main__":
    unittest.main()
