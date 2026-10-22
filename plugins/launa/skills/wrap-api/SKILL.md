---
name: wrap-api
description: >
  Wrap an upstream HTTP API with an Launa payment gateway. Use when creating,
  updating, inspecting, or deleting an Launa API or configuring its payout,
  webhook, default subdomain, or unmatched-route proxying.
---

# Wrap an API

Use Launa MCP tools. Do not construct control-plane HTTP requests manually.

## Create

Collect:

- `name`, lowercase `slug`, and HTTPS `upstream_base_url`
- payout recipient when the account uses `user_wallet`
- optional webhook and discovery fields only when requested

Ask for missing required inputs before creating anything; reuse supplied answers
and authorized existing configuration. Never invent an upstream, Live recipient,
or account choice. For Sandbox setup with no recipient, use
`launa_sandbox_wallet` and its returned public address for the verified fork
network. The prepared private key may be retrieved by that tool; never echo it.
If the tool is unavailable or permission is missing, explain how to reconnect.

Then:

1. Call `launa_platform_config` for the current gateway hostname format.
2. Call `launa_apis_slug_check`.
3. Create with `launa_create_api`.
4. Call `launa_apis_probe_upstream` using the returned API id.
5. Call `launa_discovery_urls` and report the primary gateway and discovery URLs.

`pay_to_addresses` is a CAIP-2 network-to-recipient map. Obtain supported
networks from `launa_supported_networks`; never invent chain IDs, assets, or
addresses.

## Update

Read current state with `launa_get_api`, then pass only changed fields to
`launa_update_api`. An empty `pay_to_addresses` object replaces and clears the
map; omission leaves it unchanged. `clear_webhook` removes webhook settings.

## Delete

Show the API name, id, gateway hosts, and affected endpoint count. Call
`launa_delete_api` only after explicit user confirmation.

## CLI-only fallback

Authentication and API-key management require the CLI:

```bash
launa auth login ...
launa keys create ...
```

Never request passwords, JWTs, API keys, webhook secrets, or wallet keys in chat.
