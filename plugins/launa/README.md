# Launa developer plugin

Connect your [Launa](https://launa.io) workspace to Cursor, Claude Code, Codex /
ChatGPT desktop, or Grok Build. All formats use hosted OAuth with 42 developer
control-plane tools.

## Connect

Authenticate Launa in your client's MCP settings. Your browser opens Launa's
existing login, then a consent page showing permissions and the return address.
Choose Sandbox (default) or Live. Each grant is bound to that environment; reconnect
to change it. No API key or wallet credential needs to be entered into the plugin.

Access expires after 30 days. Revoke the named `MCP: <client> (...)` key in the
corresponding environment's API key settings to stop backend access. Remove the
connection from your AI tool as well.

Production uses `https://mcp.launa.io/mcp` and sign-in on `https://launa.io`.
Version 0.1.2 is a marketplace release candidate; native production acceptance
and store submission are pending. Sandbox on production is separate from the
staging service. See the [Cursor test checklist](https://github.com/AxLabs/launa-plugins/blob/staging/docs/cursor-production-test.md).

Clients without OAuth can use a scoped API key on the same hosted endpoint;
see [API-key setup](https://launa.io/ai#other-clients). The default plugin uses
OAuth. Never paste keys into a conversation or commit them to configuration.

## Data flow

- The client sends OAuth tokens and tool requests to the hosted Launa MCP.
- After explicit consent, the service stores an encrypted, scoped backend API
  key and forwards control-plane operations to Launa. The plugin does not receive
  your frontend session, password, or backend API key.
- Tools return account configuration and analytics to the AI client. Read the
  requested permissions: write access includes deletion and changing API payout
  destinations and webhooks. Review changes before approving them.
- The optional discovery checker executes `@agentcash/discovery@1.7.5` and probes
  the selected origin. It requires Node.js 20+ separately from the hosted connection.
- No telemetry scripts or hooks are bundled. Service processing is covered by
  [privacy](https://launa.io/privacy) and [terms](https://launa.io/terms).

## Workflows

Setup, API wrapping, endpoint pricing, discovery, domains, CORS, Sandbox, and
analytics. Commands: `/wrap`, `/price`, `/discover`, `/domain`, `/cors`.
The hosted developer connection does not expose buyer inspection/payment tools.
The separate local server remains available for explicit API-key automation.

## Support

[GitHub Issues](https://github.com/AxLabs/launa-plugins/issues): include client and
plugin versions and a redacted error. Never post credentials or private account data.
