---
name: analytics
description: >
  Analyze Launa traffic, settlements, batch activity, seller income, billing,
  webhook deliveries, or payout-request status.
---

# Analytics and operations

Ask for the target environment, API, or reporting period when the requested answer depends on missing or ambiguous details. Reuse prior answers and distinguish account-wide data from API-specific data.

Prefer narrow date ranges and API filters. State whether results are
production or Sandbox.

| Need | Tool |
|------|------|
| Account traffic | `launa_stats_overview` |
| One API's traffic | `launa_stats_api` |
| API settlements | `launa_settlements_list` |
| Batch settlements | `launa_settlements_batch` |
| Paginated cross-API history | `launa_settlements_history` |
| CSV/JSON history | `launa_settlements_export` |
| Income totals | `launa_income_summary` |
| Paginated income entries | `launa_income_ledger` |
| Existing payout requests | `launa_income_payout_requests` |
| Billing state | `launa_billing_overview` |
| Facilitator aggregate stats | `launa_facilitator_stats` |
| API webhook attempts | `launa_webhook_deliveries` |
| Batch channel state | `launa_batch_overview` |

For pagination, preserve `limit`, `offset`, API id, network, and date range in
the summary. Do not present atomic token amounts as decimal amounts unless
token decimals are known from returned metadata.

Facilitator event logs, billing invoices, and exchange-rate lookup are
CLI-only in this plugin. Creating/cancelling payouts is not exposed by the
published MCP server or CLI; only listing payout requests is available.
Do not synthesize calls for unsupported operations.
