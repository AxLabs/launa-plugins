---
name: setup
description: >
  Connect the Launa developer plugin with hosted OAuth, choose Test or Live mode,
  and troubleshoot authorization or connection failures.
---

# Connect Launa

All plugin formats use hosted MCP at `https://mcp.launa.io/mcp`. Staging packages
use `https://mcp.staging.launa.io/mcp` and sign in at `https://staging.launa.io`.
The source production endpoint requires deployment before distribution.

1. Start authentication in the client's MCP settings: Cursor Tools & MCP,
   Claude Code `/mcp`, Grok Build `/mcps` then `i`, or the Codex plugin connection UI.
2. Sign in to Launa in the browser. Never ask for passwords or tokens in chat.
3. Review permissions and the return address. Choose Test mode unless the user
   explicitly wants Live operations. Approve only a connection the user initiated.
4. Call `launa_list_apis` to check the connection.

The client receives OAuth tokens, not the frontend session or backend key. No
API key, Node.js, or wallet is required for hosted control-plane access. The grant
fixes its environment; reconnect to change it. Access expires after 30 days.
Revoke the named `MCP: <client> (...)` key in the selected environment's API key
settings to stop access.

For expired or rejected authorization, reconnect. For unreachable service, check
the intended environment and service availability; do not request credentials or
silently switch to production/local access. Registration IDs inactive for 90 days
expire: remove and re-add the connection if the client keeps a stale ID.

The separate local runtime is an explicit advanced fallback, documented in the
repository's examples. Do not automatically replace a hosted OAuth connection
with local API-key authentication. Hosted tools cover 42 developer operations;
`launa_inspect_url` and `launa_pay_url` are not available here.
