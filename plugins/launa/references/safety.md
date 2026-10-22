# Safety rules

- Do not invent x402 headers, payload fields, chain IDs, token addresses,
  decimals, facilitator URLs, DNS records, or payout recipients.
- Read supported networks and assets with `launa_supported_networks`.
- Buyer requests target gateway hosts. Seller operations target the Launa
  control plane through MCP.
- Never ask for secrets in chat or echo them into chat, logs, command arguments,
  or committed files. `launa_sandbox_wallet` deliberately returns the prepared
  fork-only private key to the AI with `sandbox:wallet` consent. This authorized
  tool use is allowed; it does not grant payment, reset, or Live-wallet authority.
- Ask for required information that neither the user nor authorized reads supply.
  Do not guess pricing, resources, public contact details, or Live payout addresses.
  Reuse existing answers and keep optional fields omitted unless needed.
- Inspect before paying. Confirm URL, method, amount, asset, network, recipient,
  and scheme before one payment attempt.
- Ask for explicit confirmation before deleting an API, endpoint, domain, or
  CORS origin.
- Do not automatically retry payment or destructive calls.
- Sandbox uses `launa_sandbox_...` and development mode. Live keys move real value.
- The gateway, not the buyer, selects and calls its facilitator.
