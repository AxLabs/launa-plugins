# Card payments: implemented capabilities and limits

Reviewed 2026-11-17. Card support is implemented on `feat/card-payments` and tested
on Launa staging. This does not mean every published package or hosted deployment
contains it. Inspect connected tool schemas and versions before using the additions;
the local example remains pinned to the published 0.0.7 runtime.

## Configure seller acceptance

On a card-capable server, `launa_stripe_connection` reads readiness with
`payment_accounts:read`; `launa_card_payments` reads the selected environment's
latest 100 purchases with `payments:read`. Endpoint tools accept `card_payment`.
CLI equivalents are `cards connection`, `cards list` and endpoint `--card-payment`
JSON. Existing grants are not silently widened.

Link Stripe in the seller dashboard's Account page, under **Accept card payments**.
OAuth requires a recent browser sign-in. Seller receipt of buyer payments uses
Connect direct charges in that seller's linked Stripe account. Launa's own plan
and settlement-package billing is a separate Stripe integration. Never request a
seller Stripe secret key or replace the recipient with Launa's account.

Use only permanent, side-effect-free GET endpoints with explicit fixed USD prices
between 50 and 99,999,999 cents. Example: `card_payment: {enabled:true,
currency:"usd",amount_minor:"100"}`. Preserve x402 `accepts` when offering both;
`accepts:[]` deliberately clears x402. On update, omission preserves card settings,
`card_payment:null` removes them and `enabled:false` disables the saved card price.
Do not invent a crypto payout address for a card-only configuration.

Distinguish deployment, Launa environment and Stripe mode. In the current staging
configuration, both Launa Live and Sandbox use Stripe sandbox; linking is still
separate in each Launa environment. This exception does not authorize real payment
or imply x402 Live is test money. Read the actual connection's Stripe mode and
dashboard sandbox indicator, not only the Launa API-key prefix.

## Buyer behavior

Card-enabled builds expose card terms through `Launa-Card-Payment`, `card_payment`
and OpenAPI `x-launa-card-payment`, separately from x402 accepts. Local inspect can
show these terms when that runtime includes the feature. Existing `launa_pay_url`
is x402-only; do not invent a card/MPP argument or imply hosted developer MCP has
buyer payment tools.

Feature-branch initial unpaid JSON responses include `payment_options` listing
crypto/x402, card/launa-checkout, or both according to endpoint configuration.
Card offers add versioned `card_payment_flow` instructions for generating and
persisting the token, checkout, status and resume. Inspect's raw `body` retains
these fields. They do not authorize spending or implement MPP. Existing x402
headers/legacy body requirements stay intact. Payment-attempt errors and recovery
responses do not invite a new payment with these discovery instructions. Check
the deployed version before assuming this metadata is present.

Eligible top-level browser navigation opens Stripe Checkout automatically. The
buyer completes payment there. Launa uses the same request-specific purchase on
return, cancellation/reopen and refresh. SDK card helpers use explicit
checkout/status/resume operations and a securely retained purchase token. A 202
status is not a delivered resource. Do not lose the token/browser session or start
a replacement payment to recover an uncertain outcome.

Checking, response and attention pages are Launa themed; Checkout retains the
seller's identity. Successful responses are safely rendered with a receipt/download.
Paid results are cached for recovery, while refunds (including partial refunds)
and disputes block future retrieval. Already-delivered content cannot be recalled.
Uncertain upstream execution needs reconciliation, not a blind replay.

## Reporting

Card-enabled overview/API statistics expose `card_payments`. Income displays card
activity separately from the on-chain ledger. Paid count/gross sales include later
refunds/disputes. Delivered count means completed upstream delivery once. Refunded
amount is actual confirmed refunded cents; disputes are separate, not refunds.
Unpaid checkouts can remain pending after a decline. Polls and cached retries are
not new sales. These figures are not the seller's net Stripe balance or funds
available for a Launa payout.

Use the same environment, API filter and time window when comparing aggregates.
The latest-100 purchase list is not proof of all-time completeness. Current
on-chain earnings series do not automatically include card revenue. Inspect Stripe
for dispute financial resolution rather than inferring won/lost from `disputed`.

## Planned agent payments

MPP is not implemented in this release. The plan adds `stripe.charge` alongside
native x402 and hosted Checkout, using a seller-specific Stripe profile and direct
PaymentIntent reconciliation. Do not advertise MPP, configure invented MPP fields,
or consume an SPT using current Checkout tools.

First independent card-client targets are Stripe Link CLI and `mppx`. An MPP
crypto wallet does not necessarily support Stripe cards. The documented x402
interop bridge covers compatible EVM exact payments, not all Launa schemes.
ChatGPT Wallet's documented path is browser checkout; actual Wallet acceptance is
unverified and must not be inferred from sandbox cards or MPP support.

Staging sandbox evidence covers browser success/cancel/refresh, declined payments,
partial/full and automatic refunds, and dispute detection/access revocation.
Dispute closure and MPP/Wallet interoperability remain unverified.

References: [Launa card guide](https://docs.staging.launa.io/guides/card-payments),
[MPP/x402](https://mpp.dev/guides/use-mpp-with-x402),
[MPP clients](https://mpp.dev/tools/wallet),
[OpenAI Wallet checkout](https://developers.openai.com/commerce/guides/accept-payments).
