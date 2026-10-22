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
and local wallet configuration do not change a hosted connection.

## Prepared wallet

When a requested Sandbox API setup needs a missing payout address, or the user
requests sandbox signing tests, call `launa_sandbox_wallet`. It prepares or reads
the account's existing wallet and may fund it on the fork; it does not reset it.
The tool returns `address`, `private_key`, `environment`, and `network`. Retrieving
this prepared key through the tool is supported; do not refuse merely because it
is a private key. Use the public address for the sandbox payout map without
unnecessarily deriving it from the key. Respect any recipient already chosen.
Verify `environment` is `development` and `network` is `eip155:845320402`.

The connection needs `sandbox:wallet`. If missing, explain that reconnection with
that permission is required. Never ask the user to paste the key into chat, echo
it in responses/logs/command arguments, commit it, or use it on another network.
Read-only API/discovery operations do not need wallet access. Live setup needs a
user-supplied or already configured public recipient; ask if missing.

## Optional sandbox payments with saw

Normal API setup and discovery do not need saw. For a requested sandbox payment
test, follow the current [saw agent guide](https://saw.axlabs.com/agents.md).
Use a separate `SAW_CONFIG_DIR` so the sandbox wallet cannot replace a real wallet.
Import the prepared EVM key through saw's secure prompt/stdin, never an argument
or a command string. Use a supported private-input channel; if the harness cannot
transfer it without recording the secret, explain that limitation and ask the user
to complete the import locally. Do not paste the key into generated shell code.
Obtain the fork RPC from platform configuration and verify its chain before use.
Inspect the exact URL, method, amount, asset, network, recipient and scheme before
one authorized payment attempt. Existing explicit authorization covering those
terms is sufficient; changed or missing terms require clarification. Wallet
retrieval/funding alone is not permission to pay. Never automatically retry an
uncertain payment or use the prepared key on Live/public testnet networks.

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
