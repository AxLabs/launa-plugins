# MCP and CLI coverage

Use hosted MCP for OAuth-authenticated developer control-plane automation (43 tools).
Local stdio additionally supports API-key authentication and basic buyer inspect/pay.

| Area | MCP | CLI-only additions |
|------|-----|--------------------|
| APIs | list/get/create/update/delete, slug check, upstream probe, webhook deliveries | none |
| Endpoints | list/create/update/delete, schemas, OpenAPI parse/import | none |
| Domains / CORS | suggest/list/add/verify/delete, get/set/add/remove CORS | none |
| Batch | overview and timing settings | none |
| Analytics | stats, settlement list/batch/history/export, income summary/ledger/payout-request list, billing overview/catalog, facilitator stats | facilitator events, billing invoices, exchange rates |
| Identity | none | auth login/me, API-key list/create/revoke, scope presets |
| Sandbox wallet | `launa_sandbox_wallet`: prepare/get address and private key, `sandbox:wallet`, Sandbox only | reset remains JWT-only; get also supports scoped Sandbox keys |
| Buyer | inspect/pay URL (local stdio only) | same via `launa inspect url` / `launa pay url` |

Install the CLI with `npm install -g @launaio/cli@0.0.7`. Add `--json` for
machine-readable output. Never pass secrets on the command line when an
environment variable or secure prompt is available.

## Upcoming card-payments release

After upgrading to a build containing card support, MCP adds
`launa_stripe_connection` (`payment_accounts:read`) and `launa_card_payments`
(`payments:read`). CLI equivalents are `cards connection` and `cards list`.
Endpoint create/update accepts `card_payment`; CLI uses `--card-payment` JSON.
Linking Stripe remains an interactive seller-dashboard action. Existing grants
must explicitly consent to the added read scopes. The current published 0.0.7
launch configuration is unchanged; discover tool availability before use.
