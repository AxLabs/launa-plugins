# Launa for Antigravity IDE and CLI

Launa by **AxLabs GmbH** includes eight developer skills, Launa's square logo,
shared operation rules, and hosted MCP access with browser OAuth. No local server,
runtime dependency, API key, hook, or automatic payment is installed.

## Install

From the repository root, build and validate:

```bash
python3 scripts/client_bundles.py
agy plugin validate --strict ./bundles/antigravity/launa
agy plugin install ./bundles/antigravity/launa
agy plugin list --json
```

For the standalone IDE, copy `bundles/antigravity/launa` into your project's
`.agents/plugins/launa` directory, or into `~/.gemini/config/plugins/launa` for
all projects. Back up an existing Launa directory first. Reload the IDE and
inspect Customizations. The `.gemini` directory is Antigravity's documented
storage location; this package does not require Gemini CLI.

The build also creates `dist/launa-antigravity-0.1.4.zip`. Extract it into a
directory named `launa` to use the same installation steps without the repository.

## Connect and test

Authenticate the `launa_launa` MCP connection in Antigravity's MCP/Customizations
settings. Follow browser sign-in at `https://launa.io` and choose **Sandbox**.
If the host asks you to copy an authorization code back, use its authentication
dialog, never the chat. The server is `https://mcp.launa.io/mcp`.

Ask: “List my Launa APIs and their environments. Do not change anything.”
Then try `/setup`, `/analytics`, or `/wrap-api`. The eight bundled skills are
setup, wrap-api, price-endpoints, discovery, custom-domain, cors, sandbox, and
analytics. Antigravity uses skill invocations, not the other clients' five command files.

Test the IDE and CLI separately: confirm one MCP connection, all eight skills,
AxLabs attribution, and the Launa icon. Ask to configure an API without a price
or upstream URL; the agent must ask for missing details before creating it.
Do not send a payment as a connection test. Deletions need explicit authorization.

## OAuth rollout prerequisite

The hosted MCP must include the Antigravity callback allowlist change in
`launa-sdks/tools/mcp-server/src/hosted/registration.ts` before browser OAuth can
finish: `https://antigravity.google/oauth-callback`. PKCE, user consent, and
exact callback matching remain required. An `invalid_redirect_uri` error means
the server rollout needs checking; do not change to an arbitrary redirect URL.

For staging-service tests run `python3 scripts/client_bundles.py --environment staging`
and install `dist/staging/antigravity/launa`. This uses the staging MCP and account;
Sandbox on production is a separate environment from staging.

Review consent: `sandbox:wallet` permits the AI to retrieve the prepared fork-only
private key. It grants neither Live-wallet access nor payment authority. Revoke
the named MCP key in Launa's API key settings to stop access.

## Publication

Local packaging is separate from marketplace approval. Complete native OAuth and
read-only acceptance in both clients, then use Google's marketplace submission
process. The plugin is not claimed to be marketplace-listed.

References: [plugin format](https://antigravity.google/docs/build-plugins),
[IDE and CLI installation](https://antigravity.google/docs/plugins),
[OAuth configuration](https://antigravity.google/docs/mcp),
[marketplace](https://antigravity.google/docs/marketplace).
