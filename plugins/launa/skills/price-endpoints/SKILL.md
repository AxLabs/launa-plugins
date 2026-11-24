---
name: price-endpoints
description: >
  Create, update, delete, or bulk-import paid Launa endpoints. Use for route
  pricing, payment schemes, token accepts, TTL endpoints, request/response
  schemas, or importing OpenAPI.
---

# Price endpoints

Read the API and existing routes with `launa_get_api` and
`launa_list_endpoints` before mutating them.

Ask for missing API/route selection, method, path, price and payment terms before
writing. Discover supported networks/assets and decimals, but never interpret
support as the user's choice. Do not apply a default price. Use prior answers or
an unambiguous existing configuration; ask when multiple choices remain.

## Add or update

- Use `launa_add_endpoint` for a new method + path.
- Use `launa_update_endpoint` for enabled state, route metadata, pricing,
  accepts, or schemas.
- `price_usdc` uses the platform's default USDC accept.
- For another token, first call `launa_supported_networks`; pass `network`,
  `asset`, and either decimal `price` + `decimals` or atomic `amount`.
- Pass a complete `accepts` array when preserving multiple payment options.
- `ttl` is create-only and makes the endpoint ephemeral. It disappears after
  first settlement or expiry and is excluded from discovery documents.
- Use `request_schema` and `response_schema` so agents can understand inputs
  and outputs. `clear_schemas` clears and re-infers defaults.

Sandbox supports `exact` only. Do not select `batch-settlement` when
`LAUNA_ENVIRONMENT=development`.

## OpenAPI

1. Call `launa_parse_openapi` with YAML or JSON.
2. Review operations and the suggested upstream with the user.
3. Call `launa_import_openapi` with API id, spec, and user-approved default USDC price.
4. List endpoints and report created/skipped operations.

Import skips existing method + path keys.

## Delete

Show method, path, price accepts, and endpoint id. Call
`launa_delete_endpoint` only after explicit user confirmation.

Never hardcode chain IDs, token addresses, or decimals. Derive them from
`launa_supported_networks` or existing endpoint accepts.

## Card acceptance (requires a card-capable deployment)

Card support is merged and tested on staging; the
published 0.0.7 local runtime does not contain these additions. Read
[card payment capabilities](../../references/card-payments.md) and check the
connected server's tool schemas before using them; do not guess unsupported
arguments. A build with card support exposes `launa_stripe_connection` and
`launa_card_payments`, and adds `card_payment` to endpoint create/update.

For an authorized seller configuration, first verify their Stripe connection in
the selected environment. Linking an existing Stripe account is performed in
**Account → Card payments** in the seller dashboard; do not request their Stripe
secret key. Accept cards only on permanent, side-effect-free GET endpoints.
Use an explicit final USD price, e.g. `card_payment: {enabled:true,
currency:"usd",amount_minor:"100"}` for $1.00. Minimum is 50 cents. Preserve
existing `accepts` to offer both rails; use `accepts:[]` only when cards alone
are intended. Omission preserves card pricing; null removes it.

These operations configure receipt of buyer payments in the seller's account.
They do not authorize a buyer payment. The hosted card buyer completes Stripe
Checkout explicitly; existing `launa_pay_url` remains x402-only. Keep uncertain
purchases on the same token and payment rail. MPP is an opt-in public GET path; card commerce fulfillment is not implemented. Browser Checkout is the
documented route for ChatGPT Wallet, but actual Wallet compatibility is unverified.


For MPP-capable feature builds, read [card capabilities](../../references/card-payments.md)
before setting `card_payment.mpp`. Reuse the linked seller account, verify separate
MPP readiness, and opt in only explicitly public read-only GET resources. Existing
x402 accepts and hosted Checkout remain independent. Enabling acceptance does not
authorize a buyer payment.


MPP authentication recovery requires the `feat/mpp-3ds` backend and gateway build.
A 402 `payment_requires_action` means the buyer's token issuer must complete 3DS;
keep the original credential and exact request. Do not create a replacement token
or switch to Checkout/x402 until the original outcome is resolved. The local SDK
card lab supports sandbox fixtures and redacted debugging; issuer-backed 3DS needs
a separate sandbox issuer business profile. Seller linking is not buyer wallet setup.
