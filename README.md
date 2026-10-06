# launa-plugins

Installable agent plugins for [Launa](https://launa.io). One plugin directory is loaded by Cursor, Grok Build, Claude Code, and Codex / ChatGPT desktop.

The MCP server is the published npm package [`@launa/mcp-server`](https://www.npmjs.com/package/@launa/mcp-server) (stdio). This repo is packaging + marketplace indexes, not a fork of the server.

```
plugins/launa/          portable plugin (Agent Plugins 1.0 + client shims)
.cursor-plugin/         Cursor marketplace index
.claude-plugin/         Claude marketplace index
.grok-plugin/           Grok marketplace index
.agents/plugins/        ChatGPT / Codex marketplace index
```

## Install

Set `LAUNA_API_KEY` from the [Launa dashboard](https://launa.io) first.

**Cursor** — submit/install from this repo, or locally:

```bash
ln -s /path/to/launa-plugins/plugins/launa ~/.cursor/plugins/local/launa
```

Then Customize → Configure the `LAUNA_API_KEY` variable. Official listing: [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish) (see [SUBMIT.md](SUBMIT.md)).

**Grok Build** — add this repo as a marketplace, then install:

```bash
grok plugin marketplace add AxLabs/launa-plugins
grok plugin install launa --trust
```

**Claude Code**

```bash
claude plugin marketplace add AxLabs/launa-plugins
claude plugin install launa@launa-plugins
```

**Codex / ChatGPT desktop** — add this repo (`codex plugin marketplace add AxLabs/launa-plugins`) or point `.agents/plugins/marketplace.json` at `./plugins/launa`. Public ChatGPT directory listing needs a hosted Streamable HTTP MCP; this package is local stdio.

**cursor.directory** — repo-root `.mcp.json` is for auto-detect. Submit at [cursor.directory/plugins/new](https://cursor.directory/plugins/new).

## Configure

| Variable | Required | Purpose |
|----------|----------|---------|
| `LAUNA_API_KEY` | Yes | `launa_live_...` or `launa_sandbox_...` |
| `LAUNA_BASE_URL` | No | Default `https://api.launa.io` |
| `LAUNA_ENVIRONMENT` | No | `development` for Sandbox / Test mode |

Wallet keys for `launa_pay_url` stay in the user's environment, not in this plugin.

## One plugin, several manifests

Yes — skills, commands, and the MCP command are shared. Each client still wants its own tiny manifest:

| File | Who |
|------|-----|
| `plugin.json` + `mcp.json` | Agent Plugins 1.0 (Cursor, Codex, others) |
| `.cursor-plugin/plugin.json` | Cursor variables UI |
| `.grok-plugin/plugin.json` + `.mcp.json` | Grok Build |
| `.claude-plugin/plugin.json` + `.mcp.json` | Claude |
| `.codex-plugin/plugin.json` | Codex compatibility fallback |

Portable `mcp.json` does not embed API keys (Agent Plugins leaves unknown `${VAR}` placeholders literal). Cursor / Grok / Claude configs pass `LAUNA_API_KEY` through client-specific substitution.

## Validate

```bash
python3 scripts/validate.py
```

## License

Apache-2.0. MCP server: [AxLabs/launa-sdks](https://github.com/AxLabs/launa-sdks) (`tools/mcp-server`).
