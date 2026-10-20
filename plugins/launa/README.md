# Launa plugin

Agent plugin for the [Launa](https://launa.io) platform. Cursor uses the hosted developer MCP with OAuth. Other client manifests retain `@launaio/mcp-server@0.0.7` (stdio via `npx`) with `@launaio/sdk@0.0.7`. Local stdio requires Node.js 18+ and npm.

One package, four clients:

| Client | How it loads this folder |
|--------|--------------------------|
| Cursor | `.cursor-plugin/plugin.json` (inline hosted OAuth config) |
| Grok Build | `.grok-plugin/plugin.json` + `.mcp.json` |
| Claude Code / Cowork | `.claude-plugin/plugin.json` + `.mcp.json` |
| Codex / ChatGPT desktop | root `plugin.json` (Agent Plugins) + optional `.codex-plugin/` |

Public OpenAI directory submission supports a hosted MCP route and a desktop-only local route for approved partners. The portable/OpenAI manifest uses local stdio; directory eligibility and packaging still need verification. See the repository's [publication guide](https://github.com/AxLabs/launa-plugins/blob/main/SUBMIT.md).

## Configure

**Cursor:** connect the Launa MCP server and complete browser sign-in. Review the
permissions and explicitly select Test or Live mode. The hosted service exposes
42 developer control-plane tools; it does not require a manually entered API
key or a wallet. Access expires after 30 days; revoke the named `MCP: Cursor (...)`
key in the selected environment's dashboard to cut off backend access.

**Deployment pending:** the Cursor source points to `https://mcp.launa.io/mcp`.
The service and seller consent page must be deployed and tested before distributing
this configuration. The local installed plugin has not been switched automatically.
See [hosted rollout](https://github.com/AxLabs/launa-plugins/blob/main/docs/hosted-mcp.md).

**Other clients / local stdio:** set `LAUNA_API_KEY` from the
[Launa dashboard](https://launa.io). Optional `LAUNA_BASE_URL` defaults to
`https://api.launa.io`. An explicit Cursor local fallback is in
`examples/cursor-local.mcp.json` in the repository.

Do not commit keys or put their values in manifests.

In Claude Code, use the plugin's configuration dialog. API keys and optional
signing keys are declared as sensitive `userConfig` fields and mapped into the
local MCP process. Never put their values in chat. Empty credentials permit
inspection; seller operations need a scoped API key. Native Claude Code and
Cowork onboarding must be verified separately.

## Paid API access (local runtime only)

Launa connects APIs to agent commerce: sellers configure endpoints and prices,
and buyers can inspect a resource's payment requirements and explicitly
authorize its purchase. `launa_pay_url` accepts a URL and optional HTTP method.
It does not expose an arbitrary-address transfer operation or wallet-management
interface. For a paid request, the local SDK uses the user's configured signer
to authorize x402 payment, then retries the resource request. The gateway and
facilitator perform verification and settlement.

Always inspect and agree the resource, method, amount, asset, network, recipient,
and scheme before paying. The current MCP tool's arguments are URL and method;
the tool schema itself does not carry an amount ceiling or a consent token.
Never retry an uncertain payment outcome automatically.

## Processes, destinations, and data

- Local stdio installation/startup uses npm's registry to resolve and run
  `@launaio/mcp-server@0.0.7` through `npx`. The server depends on
  `@launaio/sdk@0.0.7`; transitive dependencies are resolved at installation.
- Cursor connects to `https://mcp.launa.io/mcp` with OAuth tokens. The hosted service
  stores an encrypted, scoped backend key after consent and forwards control-plane
  requests to Launa. The plugin never receives the frontend session or backend key.
- Local seller tools send the API key and requested configuration or query data to
  `https://api.launa.io`, or the base URL explicitly configured by the user.
- Buyer inspection and purchase contact the resource URL selected by the user.
  Paid requests submit a signed x402 authorization to that gateway. The SDK may
  contact the selected chain's RPC services; those destinations depend on the
  network and the user's configuration.
- The optional discovery command runs `@agentcash/discovery@1.7.5` and fetches
  discovery documents and probes from the selected origin. It needs Node.js 20+.
- MCP results return resource responses and seller data to the host client.
  Private signing keys are local inputs to signing and must never be included
  in prompts, results, logs, screenshots, or support reports.
- The plugin contains no telemetry hooks or analytics scripts. Service-side
  retention and processing are governed by the
  [Launa privacy policy](https://launa.io/privacy); this statement does not
  assert that the backend or package dependencies collect no operational data.

## Support

Report plugin installation and configuration issues in
[GitHub Issues](https://github.com/AxLabs/launa-plugins/issues).
Include client and plugin versions and a redacted error. Public issues must
not contain credentials, signed payment payloads, or private account data.
See also [terms](https://launa.io/terms) and [privacy](https://launa.io/privacy).

## Workflows

The plugin includes focused skills for setup, API wrapping, endpoint pricing,
OpenAPI discovery, custom domains, CORS, Sandbox, buyer inspect/pay, and
analytics. Cursor omits the local buyer skill and `/inspect` command. Local slash commands: `/wrap`, `/price`, `/discover`, `/domain`,
`/inspect`, `/cors`.

## Local test

```bash
# Cursor
mkdir -p ~/.cursor/plugins/local/launa
cp -R . ~/.cursor/plugins/local/launa/

# Grok
grok plugin install . --trust

# Claude
claude plugin validate .
```

After hosted deployment (or an explicitly configured local fallback), reload the client and call `launa_list_apis`.
