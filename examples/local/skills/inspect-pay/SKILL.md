---
name: inspect-pay
description: >
  Inspect or pay an HTTP 402 / x402 gateway URL. Use when diagnosing Payment
  Required, choosing a payment accept, or explicitly paying an Launa resource.
---

# Inspect and pay

These tools are available only in the local stdio runtime. Cursor's hosted
developer connection does not expose buyer inspection or payments. If the tools
are absent, explain that limitation; do not request wallet credentials or switch
authentication modes automatically.


Buyer calls target gateway hostnames, not the Launa control-plane API.

## Inspect first

Call `launa_inspect_url` with the exact URL and HTTP method. Summarize each
accept:

- scheme
- network
- asset and atomic amount
- `payTo`
- timeout and transfer method when present

Inspection is read-only and needs no wallet.

## Pay

Call `launa_pay_url` only when:

1. The user explicitly asks to pay.
2. The user confirms the selected amount, asset, network, recipient, URL,
   method, and scheme.
3. Signing credentials are already configured securely for the MCP process
   (Claude plugin settings or the other client's host environment).

Never ask the user to paste a private key into chat. Never print keys. Do not
blindly retry a failed payment because a retry can create another authorization.

`launa_pay_url` supports the SDK's EVM and Hedera wallet env. For Solana,
Permit2 approval, ERC-7710 grants, or advanced batch-channel management, use
the Simple Agent Wallet (`saw`) instead:

```bash
saw inspect URL
saw pay URL --confirm
```

The gateway handles facilitator verification and settlement; do not configure
or call a facilitator directly.

## Card offers and MPP

A card-capable inspect build also reports `cardPayment` terms independently of
x402 accepts. Check runtime availability; the pinned 0.0.7 example may lack this
feature. Report the USD amount and hosted Checkout path without calling it an
x402 scheme. `launa_pay_url` remains x402-only. Use the browser checkout path or
an implemented SDK card helper when the buyer explicitly chooses cards; retain
the original purchase for recovery and never fall back to x402 after an uncertain
card charge. MPP is planned, not an available Launa payment option. Actual ChatGPT
Wallet acceptance is unverified. See the shared
[card capability reference](../../../../plugins/launa/references/card-payments.md).
