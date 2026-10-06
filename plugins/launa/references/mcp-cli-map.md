# MCP and CLI coverage

Use MCP for API-key seller automation and basic buyer inspect/pay.

| Area | MCP | CLI-only additions |
|------|-----|--------------------|
| APIs | list/get/create/update/delete, slug check, upstream probe, webhook deliveries | none |
| Endpoints | list/create/update/delete, schemas, OpenAPI parse/import | discovery checker command |
| Domains / CORS | suggest/list/add/verify/delete, get/set/add/remove CORS | none |
| Batch | overview and timing settings | none |
| Analytics | stats, settlement list/batch/history/export, income summary/ledger/payout-request list | facilitator events, billing packages/invoices, exchange rates |
| Identity | none | auth login/me, API-key list/create/revoke, scope presets |
| Sandbox wallet | none | get/reset with JWT + `--sandbox` |
| Buyer | inspect/pay URL | same via `launa inspect url` / `launa pay url` |

Install the CLI with `npm install -g @launa/cli`. Add `--json` for
machine-readable output. Never pass secrets on the command line when an
environment variable or secure prompt is available.
