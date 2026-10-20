# launa-plugins

Installable agent plugins for [Launa](https://launa.io). One plugin directory is loaded by Cursor, Grok Build, Claude Code, and Codex / ChatGPT desktop.

Cursor is configured for the hosted developer MCP with OAuth; its deployment is pending. Other clients use the published npm package [`@launaio/mcp-server`](https://www.npmjs.com/package/@launaio/mcp-server) (stdio). See [hosted rollout](docs/hosted-mcp.md). This repo is packaging + marketplace indexes, not a fork of the server.

The local manifests in plugin `0.1.1` launch `@launaio/mcp-server@0.0.7`, which depends on
`@launaio/sdk@0.0.7`. The matching CLI is `@launaio/cli@0.0.7`.
Node.js 18+ and npm are required for local stdio. Its four launch configurations
pin the same MCP release; Cursor uses the separately deployed hosted service.

```
plugins/launa/          portable plugin (Agent Plugins 1.0 + client shims)
.cursor-plugin/         Cursor marketplace index
.claude-plugin/         Claude marketplace index
.grok-plugin/           Grok marketplace index
.agents/plugins/        ChatGPT / Codex marketplace index
```

## Install

For local stdio clients, set `LAUNA_API_KEY` from the [Launa dashboard](https://launa.io) first. Cursor uses browser OAuth sign-in after hosted deployment.

**Cursor** — submit/install from this repo, or locally:

```bash
mkdir -p ~/.cursor/plugins/local/launa
cp -R /path/to/launa-plugins/plugins/launa/. ~/.cursor/plugins/local/launa/
```

After deploying the hosted service and consent page, connect the Launa MCP in Cursor and complete browser sign-in. Choose Test or Live on the consent screen. Do not install this source configuration against an undeployed endpoint. Official listing: [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish) (see [SUBMIT.md](SUBMIT.md)).

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

**Codex / ChatGPT desktop** — add this repo (`codex plugin marketplace add AxLabs/launa-plugins`) or point `.agents/plugins/marketplace.json` at `./plugins/launa`. Public OpenAI directory submission has a hosted MCP route and a desktop-only local route for approved partners. This package uses local stdio; see [SUBMIT.md](SUBMIT.md) for eligibility and packaging requirements.

**cursor.directory** — repo-root `.mcp.json` is for auto-detect. Submit at [cursor.directory/plugins/new](https://cursor.directory/plugins/new).

## Configure local stdio

| Variable | Required | Purpose |
|----------|----------|---------|
| `LAUNA_API_KEY` | Yes | `launa_live_...` or `launa_sandbox_...` |
| `LAUNA_BASE_URL` | No | Default `https://api.launa.io` |
| `LAUNA_ENVIRONMENT` | No | `development` for Sandbox / Test mode |

Signing keys for `launa_pay_url` stay in the user's MCP host environment or
Claude's secure plugin configuration. See the
[plugin configuration and data flow](plugins/launa/README.md).
The optional discovery checker requires Node.js 20+.

## One plugin, several manifests

Control-plane skills and commands are shared. Cursor selects the developer workflows and hosted OAuth; local manifests also expose buyer inspection/payment:

| File | Who |
|------|-----|
| `plugin.json` + `mcp.json` | Agent Plugins 1.0 (Cursor, Codex, others) |
| `.cursor-plugin/plugin.json` | Cursor hosted OAuth config |
| `.grok-plugin/plugin.json` + `.mcp.json` | Grok Build |
| `.claude-plugin/plugin.json` + `.mcp.json` | Claude (with an inline credential override) |
| `.codex-plugin/plugin.json` | Codex compatibility fallback |

Portable `mcp.json` does not embed API keys (Agent Plugins leaves unknown `${VAR}` placeholders literal). Grok configs use environment substitution; Cursor uses its inline hosted OAuth definition; Claude uses its declared secure `userConfig` values.

## Validate

```bash
python3 scripts/validate.py
```

The validator checks manifest and marketplace versions, required files, and
the MCP package/command in four local launch configurations plus Cursor OAuth
URL, client ID, scopes, and developer-only workflows. When upgrading the
published MCP package, update all four local launch configurations, setup and CLI
references, and `MCP_PACKAGE` in `scripts/validate.py`; verify the published
tool schemas against the skills before bumping the plugin release.

## License

Apache-2.0. MCP server: [AxLabs/launa-sdks](https://github.com/AxLabs/launa-sdks) (`tools/mcp-server`).
