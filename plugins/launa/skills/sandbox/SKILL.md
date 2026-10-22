---
name: sandbox
description: >
  Use Launa Sandbox for APIs and x402 payments without real funds.
  Use when the user mentions launa_sandbox keys, development mode, the Anvil
  fork, test payments, or the Sandbox wallet.
---

# Sandbox

For the hosted connection, select **Sandbox** during OAuth consent.
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

Fork state is ephemeral. Do not treat Sandbox as production state.
