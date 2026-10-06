# Safety rules

- Do not invent x402 headers, payload fields, chain IDs, token addresses,
  decimals, facilitator URLs, DNS records, or payout recipients.
- Read supported networks and assets with `launa_supported_networks`.
- Buyer requests target gateway hosts. Seller operations target the Launa
  control plane through MCP.
- Never expose `LAUNA_API_KEY`, JWTs, passwords, webhook secrets, wallet private
  keys, seed phrases, or signed payment payloads.
- Inspect before paying. Confirm URL, method, amount, asset, network, recipient,
  and scheme before one payment attempt.
- Ask for explicit confirmation before deleting an API, endpoint, domain, or
  CORS origin.
- Do not automatically retry payment or destructive calls.
- Sandbox uses `launa_sandbox_...` and development mode. Live keys move real value.
- The gateway, not the buyer, selects and calls its facilitator.
