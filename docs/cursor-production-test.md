# Cursor production acceptance — 0.1.2

Status: awaiting native Cursor testing. Record Cursor version, plugin version,
source commit, date and pass/fail for each step. Do not record credentials or
OAuth callback query strings. This checklist does not submit or publish anything.

## 1. Load the production copy

Use a real copy of `plugins/launa/`, including hidden files, at
`~/.cursor/plugins/local/launa/`. Back up the old copy outside that directory.
The installed `.cursor-plugin/plugin.json` must show version `0.1.2` and
`mcpServers.launa.url` equal to `https://mcp.launa.io/mcp`.

Run **Developer: Reload Window** from Cursor's command palette. Open the plugin
page and MCP settings (labels vary by version). Confirm the square Launa icon,
Website link to https://launa.io, eight skills and five commands.
Disable other Launa MCP connections in this workspace for the test so tools
cannot silently use staging or local stdio. A marketplace plugin of the same
name takes precedence over a local copy; disable/remove that duplicate for this
test if necessary. Organization restrictions can also block local imports.

## 2. Authenticate

Connect/authenticate Launa. The browser must open https://launa.io, not staging.
Use the normal login and MFA/passkey if configured. Review client, return address,
permissions and environment. Deny once: Cursor must remain unauthenticated.
Start a fresh connection and approve **Test mode**.

Production Test mode is distinct from staging, so the older staging smoke-test
APIs need not appear here. No API key, wallet key or Node.js should be required.
Expect 42 developer tools and no `launa_pay_url` or `launa_inspect_url`.

## 3. Read-only smoke test

In a fresh chat:

> Use only the Launa plugin connection. List my APIs and supported networks.
> If an API exists, show its endpoints and prices. Do not create or change anything.

Compare with Test mode in the production dashboard. Empty results are valid for
an empty test account. No Live-mode or another account's private resources should
appear. Check that tool output contains no credentials.

## 4. Disposable API

Only after confirming Test mode, send:

> In Test mode only, create a disposable API named Cursor marketplace test with
> a unique cursor-review slug and upstream https://postman-echo.com. Use my
> existing test payout address if available; otherwise stop and explain what is
> missing. Add GET /get at 0.001 USDC using the supported exact scheme and test
> network. List the API and endpoint afterward. Do not make any payment.

Do not invent a payout address. If none is configured, record the actionable
validation error and configure the test payout through the dashboard before
retrying. Check the new API/route in the production dashboard's Test mode.

> For only the test API we just created, update GET /get to 0.002 USDC, list its
> endpoints and show its request statistics. Do not change any other API.

The listed price must match the dashboard. Stats include method/path when
endpoint rows exist; a new API may have no traffic. Income is account-level:
unavailable fiat valuation is not a zero valuation.

Before revocation, explicitly authorize deletion of this exact disposable API
and endpoint using their returned IDs, then verify they disappear. Do not delete
pre-existing resources.

## 5. Reload, revoke, reconnect

Reload Cursor and list APIs again. The connection should work or clearly request
authentication. A quick reload is not proof of refresh-token expiry/rotation.

In the production dashboard's **Test mode**, revoke only the
`MCP: <client> (...)` API key created for this test. Ask Cursor to list APIs
again: the backend operation must fail rather than present cached data as a new
success. Disconnect/re-authenticate, approve Test mode and confirm access returns.
Remove the test connection/key afterward if no longer needed.

## Results

Report pass/fail for appearance, deny/approve, read-only calls, create/update/
delete, reload, and revoke/reconnect. Include Cursor version and redacted errors.
Never send keys, passwords, cookies or callback query strings.

Separate account-isolation and Live-mode tests need distinct authorized
accounts/grants; do not mark those passed from this single-account test.
After acceptance, promote the reviewed plugin commit to main and submit the
repository through Cursor's publisher form.
