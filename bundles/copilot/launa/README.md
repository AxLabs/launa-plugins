# Launa for GitHub Copilot

This bundle packages eight Launa skills and the hosted developer MCP for Copilot
CLI, VS Code and the Copilot app. It uses Agent Plugins 1.0. Skills include the
shared Launa operation rules, so they ask for missing required information and
keep Sandbox and Live actions separate. It has no local server or bundled secrets.

## Test the local bundle

From the repository root, build and install in Copilot CLI:

```bash
python3 scripts/client_bundles.py
copilot plugin marketplace add .
copilot plugin install launa@launa-plugins
copilot plugin list
```

In VS Code, run **Chat: Install Plugin from Source** and select the absolute path
to `bundles/copilot/launa`. You can also find plugins installed by Copilot CLI in
**Chat: Open Customizations → Plugins**. Use a current VS Code with agent plugins
enabled and the Copilot harness selected.

For the Copilot app, open **Customize** and add this repository as a marketplace
after the bundle has been pushed. Install Launa from that marketplace. Availability
can be restricted by organization policies. This package does not promise support
for every IDE containing a Copilot extension.

## Install after these files are published

The repository's `.github/plugin/marketplace.json` points to the Copilot bundle:

```bash
copilot plugin marketplace add AxLabs/launa-plugins
copilot plugin install launa@launa-plugins
```

Use the marketplace commands above: Copilot CLI 1.0.105 warns that direct
repository and local-folder installs are deprecated.

These remote commands require the files on the repository's default branch.
Adding our repository is separate from being listed in GitHub's built-in marketplace.

## Connect and verify

Enable Launa's MCP connection and complete the client's browser authentication
prompt. Review the permissions at Launa and select **Sandbox** for this test.
The connection URL is `https://mcp.launa.io/mcp`; no API key is embedded or required
for OAuth. A client that offers API-key authentication can instead use its own
secure credential settings with a scoped Launa key; never put a key in this bundle.

1. Confirm Launa's eight skills and developer tools are available.
2. Ask: **“List my Launa APIs and their priced endpoints. Do not change anything.”**
3. Ask: **“Help me create a Sandbox API. Ask for required information I haven't
   supplied before creating it.”** The agent must obtain missing inputs rather
   than invent an upstream, payout address, slug or price.
4. If testing the prepared wallet, explicitly grant `sandbox:wallet` and authorize
   fork-only wallet access. The key must not be echoed, logged or committed.
   Wallet access does not authorize a payment or a reset.
5. Revoke the connection in Launa and verify that subsequent protected tool calls fail.

For staging-service tests, run `python3 scripts/client_bundles.py --environment staging`
and install `dist/staging/copilot/launa` instead. Do not install both environments
under the same plugin name at once.

Packaging checks do not verify browser sign-in, tool execution or account policies.
Complete those checks in each intended client before requesting a marketplace listing.

References: [GitHub plugin support](https://docs.github.com/en/copilot/concepts/customizations/plugins),
[CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference),
and [VS Code plugin installation](https://code.visualstudio.com/docs/agent-customization/agent-plugins).
