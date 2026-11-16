# Launa for Claude Desktop

Launa by **AxLabs GmbH** packages eight skills, five commands, shared operation
rules, the Launa logo asset, and a remote MCP connector. It uses browser OAuth at
`https://mcp.launa.io/mcp`; no local Node server or wallet is needed.

## Build and install

From the repository root:

```bash
python3 scripts/client_bundles.py
```

Upload `dist/launa-claude-desktop-0.1.4.zip` through Claude Desktop's
**Customize → Plugins** custom-plugin upload option. The ZIP contains
`.claude-plugin/plugin.json` at its root; do not upload a ZIP of the entire
repository. In Cowork, open the Cowork tab before Customize.

Claude currently requires a paid plan for plugins. Building the bundle does not
require a subscription. Organization policies may restrict installation.

This is a Claude plugin for Desktop Chat/Cowork, not an `.mcpb` local-server
extension. The remote connector also works independently of the workflow bundle.

## Connect and test

Connect Launa when Claude prompts for connector authentication. Sign in in the
browser and choose **Sandbox**. Then ask: “List my Launa APIs. Do not change
anything.” Check that the result comes from the Launa MCP tools.

Skills cover setup, API wrapping, pricing, discovery, domains, CORS, Sandbox,
and analytics. Select them through Claude's skill picker. In Cowork, commands
include `/launa:wrap`, `/launa:price`, `/launa:discover`, `/launa:domain`, and
`/launa:cors`. The same instruction and consent boundaries apply to every workflow.

Confirm that missing upstream URLs, prices, or Live payout addresses lead to
questions before a mutation. Do not make payments to test installation. Shared
operation rules are embedded into skills and commands because Claude does not
load Cursor's `.mdc` rule file.

The default connection targets production Launa; Sandbox is selected during
consent. For staging-service testing, run
`python3 scripts/client_bundles.py --environment staging` and upload
`dist/launa-claude-desktop-0.1.4-staging.zip` instead.

`sandbox:wallet` explicitly permits retrieving the prepared private key only for
the dedicated Sandbox fork. Do not paste secrets into chat. This permission does
not authorize a payment. Revoke the named MCP key in Launa's API key settings to
stop access; removing the plugin alone is not the account-side revocation step.

Public marketplace approval is separate from uploading a custom plugin. Native
Desktop installation and authenticated acceptance must be completed before submission.

References: [Claude plugins and installation](https://support.claude.com/en/articles/13837440-use-plugins-in-claude),
[plugin manifest reference](https://code.claude.com/docs/en/plugins-reference),
[Launa](https://launa.io), [support](https://github.com/AxLabs/launa-plugins/issues).
