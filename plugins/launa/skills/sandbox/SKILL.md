---
name: sandbox
description: >
  Use Launa Sandbox / Test mode for APIs and x402 payments without real funds.
  Use when the user mentions launa_sandbox keys, development mode, the Anvil
  fork, test payments, or the Sandbox wallet.
---

# Sandbox

For the hosted Cursor connection, select **Test mode** during OAuth consent.
The grant fixes its environment; reconnect to change it. Environment variables
and local wallet configuration do not change a hosted connection. Do not set up
a wallet for developer control-plane operations.

## Local stdio environment

Sandbox is the `development` control-plane environment and uses an
`launa_sandbox_...` key.
The key prefix selects Sandbox; `LAUNA_ENVIRONMENT` / `LAUNA_SANDBOX` are optional.

```bash
export LAUNA_ENVIRONMENT=development
# or
export LAUNA_SANDBOX=1
```

The hosted fork network is `eip155:845320402`. Do not substitute public Base
or Base Sepolia. Obtain the current token, RPC, and gateway details from
`launa_supported_networks` and `launa_platform_config`; do not hardcode them
into mutations.

Sandbox endpoint defaults support `exact` only, not `batch-settlement`.

## Funded test wallet (local buyer workflow only)

Sandbox wallet retrieval is JWT-only and intentionally not exposed over MCP:

```bash
export LAUNA_JWT="$(launa auth login --email ... --password ...)"
launa --sandbox sandbox-wallet get --json --wait
```

The JSON output contains a private key. The user must run this locally and
place it in `LAUNA_EVM_PRIVATE_KEY`; never request or display it in chat.

Fork state is ephemeral and can be wiped by restarts. Do not treat Sandbox
transactions or balances as production state.
