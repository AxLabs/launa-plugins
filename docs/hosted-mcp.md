# Hosted OAuth rollout — all plugins

The Cursor manifest now targets `https://mcp.launa.io/mcp`, using the static public
OAuth client `launa-cursor`. It no longer requests an API key in plugin variables.
The square icon remains the same improved asset for the listing and plugin page.
This is **unreleased source**. The production endpoint is not deployed; do not
distribute it until production service/consent deployment and the complete native
connection have been tested.

Staging was deployed on 2026-10-20 at `https://mcp.staging.launa.io/mcp`, with
consent on `https://staging.launa.io`. HTTPS, OAuth discovery, Mongo-backed
authorization requests, the frontend bridge, invalid-session rejection, callback
validation, and consent origin checks passed. The existing staging login page
and backend health checks also passed. Interactive Cursor account sign-in and
authenticated tool operations remain to be verified by the tester.

Implementation lives in `launa-sdks/tools/mcp-server`; its `HOSTED.md` contains
runtime configuration and the deployment procedure. The existing seller frontend
in `launa-clients/apps/seller` supplies `/mcp/connect` and `/api/mcp/consent`. Backend
frontend-session authentication is unchanged. Configure a dedicated Mongo database,
encryption key, consent-bridge secret, and the exact seller/MCP origins.

Register these exact callbacks for `launa-cursor`, as documented by
[Cursor](https://cursor.com/docs/mcp):

- `http://localhost:8787/callback`
- `https://www.cursor.com/agents/mcp/oauth/callback`

The plugin requests control-plane read/write scopes and analytics/billing/income
reads. The consent screen selects test or live mode. It does not grant wallet,
payment, payout, or billing-mutation authority. Hosted and local share the same
42 control-plane tool definitions; local stdio retains its two additional buyer
tools. All other client manifests now use hosted OAuth with dynamic client registration.
Native onboarding remains a release verification step for every client.
Registration permits loopback redirects and reviewed web callbacks only; it does
not fetch arbitrary metadata URLs. See the server HOSTED.md for the policy.

Before release:

1. Keep staging's hosted runtime, consent routes, dedicated database, secret, and
   origins configured together. Use the staging URL for local plugin testing.
2. Connect in Cursor, use existing Launa login/MFA/passkeys, deny once, then allow
   Test access. Check all 42 tools and exercise test API/endpoint CRUD.
3. Confirm a second account and a separately authorized live connection cannot
   see or mutate each other's resources. Revoke the named API key and confirm
   backend operations fail. Test refresh and expired/replayed tokens.
4. Deploy the reviewed runtime to the intended public hostname; verify TLS,
   metadata, callback roundtrip and edge rate limits. No marketplace release is
   part of deployment testing.
5. Refresh the source ZIP/checksum and reviewer evidence, then request the user's
   authorization to publish or submit. Keep earlier local-runtime evidence labeled
   as local; it is not proof of hosted OAuth onboarding.

The installed local Cursor copy now points to the deployed staging endpoint.
To keep using local stdio, use `examples/cursor-local.mcp.json` explicitly
and supply a scoped key through Cursor's environment substitution. Do not put
credentials in chat or Git. OAuth sign-in does not require Node/npm locally.

For staging tests, use `examples/cursor-staging.mcp.json`, or install the plugin
locally and set its Cursor manifest's `mcpServers.launa.url` to
`https://mcp.staging.launa.io/mcp`. Sign-in and consent must stay on
`https://staging.launa.io`; this endpoint uses the staging control plane. The
Website link remains `https://launa.io`. Staging deployment does not publish the
plugin to any marketplace.

Use `python3 scripts/prepare-staging.py /tmp/launa-plugin-staging` to generate all
client manifests against staging together. Public directory submission remains pending.
