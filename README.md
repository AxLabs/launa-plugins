# launa-plugins

Developer plugins for [Launa](https://launa.io): manage APIs, endpoint pricing,
domains, discovery, analytics, and settlements from your AI tool.

All four client formats use the hosted MCP with **OAuth browser sign-in**.
No API key, local Node.js runtime, or wallet is needed. Review permissions and
choose Test or Live mode before granting access. The hosted server exposes the
same 42 control-plane tools as the local server.

**Marketplace release candidate 0.1.2:** production MCP is deployed at
`https://mcp.launa.io/mcp`, with sign-in and consent on `https://launa.io`.
Native production client acceptance and marketplace review remain pending.
Nothing has been submitted to marketplaces. Start with the
[Cursor production test](docs/cursor-production-test.md), then follow
[submission](SUBMIT.md).

## Install from source

| Client | Plugin definition | Sign-in |
| --- | --- | --- |
| Cursor | `.cursor-plugin/plugin.json` | Tools & MCP → connect Launa |
| Claude Code | `.claude-plugin/plugin.json` | `/mcp` → authenticate Launa |
| Grok Build | `.grok-plugin/plugin.json` + `.mcp.json` | `/mcps` → Launa → `i` |
| Codex / ChatGPT desktop | `plugin.json` + `mcp.json`; `.codex-plugin/` fallback | Authenticate the plugin in the host |

Cursor uses public client `launa-cursor`. The other clients discover the OAuth
registration endpoint. The portable OpenAI manifest explicitly declares OAuth
with dynamic client registration. Client IDs are public; no client secret is
shipped. Browser consent is required for every new grant.

For production testing, copy `plugins/launa/`, including hidden files, into
`~/.cursor/plugins/local/launa/`. Back up an existing copy outside that directory
first. Reload Cursor and follow the [production checklist](docs/cursor-production-test.md).
Use the reviewed `staging` checkout until this candidate is promoted to `main`.

For staging-service testing, build a separate environment-specific copy:

```bash
python3 scripts/prepare-staging.py /tmp/launa-plugin-staging
```

Load that directory in your client. For Cursor, copy its contents into
`~/.cursor/plugins/local/launa/` and reload the plugin. The source generator
changes every MCP manifest to staging together; Website remains `https://launa.io`.
Use the `staging` branch if adding this repository as a marketplace for testing;
the default branch may contain older packaging.

After this candidate is promoted to the public default branch, repository-based
installation (separate from acceptance into a curated marketplace):

```bash
claude plugin marketplace add AxLabs/launa-plugins
claude plugin install launa@launa-plugins

grok plugin marketplace add AxLabs/launa-plugins
grok plugin install launa --trust
```

Cursor and OpenAI directory submission instructions are in [SUBMIT.md](SUBMIT.md).

## Workflows and access

Eight skills cover setup, API wrapping, endpoint pricing, discovery, custom
domains, CORS, Test mode, and analytics. Five commands provide `/wrap`, `/price`,
`/discover`, `/domain`, and `/cors`.

Access expires after 30 days. Revoke the named `MCP: <client> (...)` key in the
selected environment's API key settings to stop backend access. Reconnect to
change environments. Never put credentials in prompts, manifests, or Git.

## Advanced local server

The local `@launaio/mcp-server@0.0.7` remains available with a scoped API key.
Use `examples/cursor-local.mcp.json` explicitly; it is a separate connection.
The local server also exposes two buyer tools that are not included in hosted
OAuth. Their legacy instructions are retained under `examples/local/` and are
not loaded by the developer plugins.

The optional discovery checker uses `@agentcash/discovery@1.7.5` and needs Node.js
20+. Connecting to hosted MCP does not require it.

## Validate

```bash
python3 scripts/validate.py
```

Checks all client formats, matching versions, hosted URLs, OAuth metadata, icons,
required workflows, and absence of credential-based onboarding.

Apache-2.0. Server implementation: [AxLabs/launa-sdks](https://github.com/AxLabs/launa-sdks/tree/main/tools/mcp-server).
