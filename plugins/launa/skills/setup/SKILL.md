---
name: setup
description: >
  Configure the Launa plugin MCP server (API key, base URL, sandbox vs live).
  Use on first install, when tools fail with LAUNA_API_KEY required, or when
  switching Sandbox and production.
---

# Launa plugin setup

The MCP server is `npx -y @launa/mcp-server` (stdio). It reads env vars;
this plugin does not ship secrets.

## Required

1. Create a scoped API key in the [Launa dashboard](https://launa.io).
2. Set `LAUNA_API_KEY` to that value (`launa_live_...` or `launa_sandbox_...`).
   An `launa_sandbox_...` key selects Sandbox automatically; `LAUNA_ENVIRONMENT` is optional.

Optional:

| Variable | Default | When |
|----------|---------|------|
| `LAUNA_BASE_URL` | `https://api.launa.io` | Staging / self-host |
| `LAUNA_ENVIRONMENT` | unset | `development` for Sandbox / Test mode |
| `LAUNA_SANDBOX` | unset | `1` / `true` — alias for development |

## Per client

- **Cursor:** Customize → plugin → Configure. Fill `LAUNA_API_KEY` (and optional base URL). Reload if tools stay missing.
- **Grok Build:** export the vars in the environment Grok inherits, or set them on the `launa` MCP server (`grok mcp` / `/mcps`).
- **Claude Code:** export `LAUNA_API_KEY` in the shell that launches `claude`, then `/reload-plugins`.
- **Codex / ChatGPT desktop:** set `LAUNA_API_KEY` in the host environment before enabling the plugin. Public ChatGPT directory listing needs a hosted Streamable HTTP MCP (not this stdio package).

Restart / reload the client after changing env.

## Wallet pay (optional)

`launa_pay_url` also needs `LAUNA_EVM_PRIVATE_KEY` and/or `HEDERA_ACCOUNT_ID` + `HEDERA_PRIVATE_KEY`. Do not put those in the plugin repo, chat, or git. Leave them unset unless the user is explicitly paying.

Sandbox wallet private keys are CLI + JWT only (`launa --sandbox sandbox-wallet get`).

## Check

Call `launa_list_apis` or `launa_platform_config`. Auth errors mean a bad key or the wrong `LAUNA_BASE_URL`.
