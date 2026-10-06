# Launa plugin

Agent plugin for the [Launa](https://launa.io) platform. Bundles `@launa/mcp-server` (stdio via `npx`) plus skills and slash commands.

One package, four clients:

| Client | How it loads this folder |
|--------|--------------------------|
| Cursor | `.cursor-plugin/plugin.json` + `mcp.json` |
| Grok Build | `.grok-plugin/plugin.json` + `.mcp.json` |
| Claude Code / Cowork | `.claude-plugin/plugin.json` + `.mcp.json` |
| Codex / ChatGPT desktop | root `plugin.json` (Agent Plugins) + optional `.codex-plugin/` |

ChatGPT's **public** plugin directory wants a hosted Streamable HTTP MCP. This package is local stdio. Codex and ChatGPT desktop can still install it from this repo.

## Configure

Set `LAUNA_API_KEY` from the [Launa dashboard](https://launa.io). Optional `LAUNA_BASE_URL` (default `https://api.launa.io`).

Do not commit keys. Do not put wallet private keys in plugin config.

## Workflows

The plugin includes focused skills for setup, API wrapping, endpoint pricing,
OpenAPI discovery, custom domains, CORS, Sandbox, buyer inspect/pay, and
analytics. Slash commands: `/wrap`, `/price`, `/discover`, `/domain`,
`/inspect`, `/cors`.

## Local test

```bash
# Cursor
ln -s "$(pwd)" ~/.cursor/plugins/local/launa

# Grok
grok plugin install . --trust

# Claude
claude plugin validate .
```

Then reload the client and call `launa_list_apis`.
