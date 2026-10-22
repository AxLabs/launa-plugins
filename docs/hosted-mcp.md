# Hosted MCP rollout

Production was deployed on 2026-10-21 at https://mcp.launa.io/mcp, with browser
sign-in and consent on https://launa.io. Health and OAuth metadata were checked
again on 2026-10-22. Marketplace submission and native production acceptance
remain pending. Use the [Cursor checklist](cursor-production-test.md).

Deployment checks covered TLS, health, OAuth discovery, PKCE authorization
handoff to the production consent page, invalid OAuth/API-key rejection, and
registration edge rate limiting. SDK/MCP regressions covered OAuth behavior and
Mongo persistence. These checks do not establish successful native Cursor login
or authenticated tool execution.

## Authentication

All plugin formats default to hosted OAuth. Cursor uses public client ID
`launa-cursor` with these registered callbacks:

- `http://localhost:8787/callback`
- `https://www.cursor.com/agents/mcp/oauth/callback`

Other clients use restricted dynamic registration: reviewed web callbacks or
native loopback callbacks. No client secret is shipped. Consent binds each grant
to Sandbox or Live. Production Sandbox uses the production account's sandbox
resources, not the staging account/database.

Hosted MCP exposes 43 developer control-plane tools. Permissions include API,
endpoint and domain configuration and analytics, billing, income and settlement
reads. Configuration writes can change API payout destinations and webhooks;
they do not authorize sending funds. Buyer inspection/payment tools are excluded.
Local stdio retains buyer tools as an explicit alternative; published version
0.0.7 predates the new Sandbox wallet tool.

Clients without OAuth can use scoped API keys on the same hosted endpoint;
see [setup](https://launa.io/ai#other-clients). Never commit credentials.

## Runtime and release gates

The runtime lives in `launa-sdks/tools/mcp-server`; its `HOSTED.md` documents
configuration. The seller frontend supplies `/mcp/connect` and
`/api/mcp/consent` using the existing login. OAuth grants use separate durable
Mongo storage, encryption credentials and a consent-bridge secret shared with
the seller frontend. Production and staging secrets and grant databases stay
separate.

Staging remains at https://mcp.staging.launa.io/mcp, with sign-in on
https://staging.launa.io. Generate its test copy using
`python3 scripts/prepare-staging.py /tmp/launa-plugin-staging`.
The unmodified source manifests target production.

Before Cursor submission, complete the native production checklist, review the
exact public release commit, and prepare [reviewer evidence](release-review.md).
Other marketplaces require their own native client checks. Deployment alone
does not mean the plugin is listed.

The explicit `sandbox:wallet` permission adds `launa_sandbox_wallet`: it returns
the prepared Sandbox wallet, including its private key, to the AI client for
authorized fork-only testing. Live access and wallet reset are denied. Existing
connections must reconnect to grant the permission. No buyer payment is implied;
optional payment tests can use [saw](https://saw.axlabs.com/agents.md).
