---
name: setup
description: >
  Configure the Launa plugin MCP server (Cursor OAuth or local API keys, test vs live).
  Use on first install, when tools fail with LAUNA_API_KEY required, or when
  switching Sandbox and production.
---

# Launa plugin setup

## Cursor hosted connection

Cursor's vendor manifest uses the hosted developer MCP at `https://mcp.launa.io/mcp`
with public OAuth client `launa-cursor`. Complete the client's sign-in flow, log
in to Launa, review permissions, and choose Test or Live mode. No API key or
wallet credential is entered into Cursor. Default to Test unless the user asks
for live operations. Reconnect to choose a different environment. Revoke access
using the named `MCP: Cursor (...)` API key in that environment's dashboard.

This source configuration requires deployment of the hosted MCP and seller
consent page before use; do not interpret a connection failure as a request for
credentials. The hosted service exposes the 42 control-plane tools only.
`launa_inspect_url` and `launa_pay_url` remain local-runtime capabilities.

## Local runtime (other clients or explicit fallback)

The local MCP server is `npx -y @launaio/mcp-server@0.0.7` (stdio). It reads env vars;
this plugin does not ship secrets. Requires Node.js 18+ and npm.
Keep npm optional dependencies enabled: the SDK needs `@x402/fetch` even
for wallet-free inspection of HTTP 402 responses.

## Required

1. Create a scoped API key in the [Launa dashboard](https://launa.io).
2. Configure `LAUNA_API_KEY` using the client's settings below (`launa_live_...` or `launa_sandbox_...`).
   An `launa_sandbox_...` key selects Sandbox automatically; `LAUNA_ENVIRONMENT` is optional.

Optional:

| Variable | Default | When |
|----------|---------|------|
| `LAUNA_BASE_URL` | `https://api.launa.io` | Staging / self-host |
| `LAUNA_ENVIRONMENT` | unset | `development` for Sandbox / Test mode |
| `LAUNA_SANDBOX` | unset | `1` / `true` — alias for development |

## Per client

- **Cursor local fallback:** explicitly configure the stdio example in `examples/cursor-local.mcp.json` from the repository. This is a separate API-key connection; do not silently replace an OAuth connection.
- **Grok Build:** export the vars in the environment Grok inherits, or set them on the `launa` MCP server (`grok mcp` / `/mcps`).
- **Claude Code:** enter `LAUNA_API_KEY` in secure plugin configuration, then `/reload-plugins`. The Claude manifest maps `userConfig` into the MCP process; it overrides the shared environment configuration. Empty credentials allow inspection; seller calls require an API key. Use a current Claude Code release; native onboarding still needs verification.
- **Codex / ChatGPT desktop:** set `LAUNA_API_KEY` in the host environment before enabling the plugin. Public directory submission has a local MCP route for approved partners and a hosted MCP route; the portable manifest retains stdio; Cursor has its own hosted OAuth configuration.

Restart / reload the client after changing env.

## Local wallet pay (optional; not hosted)

`launa_pay_url` also needs `LAUNA_EVM_PRIVATE_KEY` and/or `HEDERA_ACCOUNT_ID` + `HEDERA_PRIVATE_KEY`. In Claude, use secure plugin configuration; in other clients, use the user's MCP host environment. Do not put those in the plugin repo, chat, or git. Leave them unset unless the user is explicitly paying.

Sandbox wallet private keys are CLI + JWT only (`launa --sandbox sandbox-wallet get`).

## Check

Call `launa_list_apis` or `launa_platform_config`. For hosted OAuth, reconnect if authorization expired or the account key was revoked. For local stdio, check the scoped key and `LAUNA_BASE_URL`. Never print tokens or keys.
