# Submit to marketplaces

This repo is the source. Listing is a separate step per catalog. Plugin path: `plugins/launa`.

## Cursor Marketplace (curated)

1. `python3 scripts/validate.py`
2. Test: `ln -s $(pwd)/plugins/launa ~/.cursor/plugins/local/launa` then reload
3. Submit the GitHub URL at https://cursor.com/marketplace/publish
4. Target category: Payments

Community listing (faster): https://cursor.directory/plugins/new — paste `https://github.com/AxLabs/launa-plugins` (root `.mcp.json` is for auto-detect).

## Grok Build Plugin Marketplace

Users can add this repo today:

```bash
grok plugin marketplace add AxLabs/launa-plugins
grok plugin install launa --trust
```

Official catalog is a PR against https://github.com/xai-org/plugin-marketplace. Add one remote entry (pin a full 40-char SHA after this repo is pushed):

```json
{
  "name": "launa",
  "description": "Manage Launa paid APIs from the agent: wrap endpoints, set x402 prices, inspect 402s, and review settlements.",
  "category": "development",
  "source": {
    "source": "url",
    "url": "https://github.com/AxLabs/launa-plugins.git",
    "sha": "REPLACE_WITH_FULL_COMMIT_SHA",
    "path": "plugins/launa"
  },
  "homepage": "https://launa.io",
  "keywords": ["launa", "x402", "payments", "mcp", "launa mcp"],
  "domains": ["launa.io", "api.launa.io"]
}
```

Then in that fork:

```bash
python3 scripts/generate-plugin-index.py
python3 scripts/validate-catalog.py
```

## Claude plugin directory

This repo is already a Claude marketplace (`.claude-plugin/marketplace.json`).

```bash
claude plugin marketplace add AxLabs/launa-plugins
claude plugin install launa@launa-plugins
claude plugin validate ./plugins/launa
```

Official directory (Cowork + Claude Code):

- https://claude.ai/admin-settings/directory/submissions/plugins/new
- https://platform.claude.com/plugins/submit

Claude **Connectors** directory is a different path: it wants a public Streamable HTTP MCP, not stdio `npx`. Skip until Launa hosts one.

## ChatGPT / Codex

- **Codex / ChatGPT desktop:** `codex plugin marketplace add AxLabs/launa-plugins` (stdio MCP).
- **Public ChatGPT plugin directory:** submit a remote HTTPS MCP through OpenAI's plugin flow. This package does not include a hosted endpoint or a `plugin_asdk_app...` mapping in `.app.json`.

## Official MCP Registry

Separate from plugins. Publish `server.json` from `launa-sdks/tools/mcp-server` with `mcpName` on the npm package, then `mcp-publisher publish`.
