# Control-plane scopes

Hosted plugin access uses OAuth consent. Its selected scopes are enforced by a
server-held API key; the user does not paste that key into the plugin. Its default
permissions cover developer configuration and reporting, excluding billing
mutations and payouts. The table below also applies to explicit local API keys.

Use the smallest preset that supports the task:

| Preset | Scopes |
|--------|--------|
| `readonly` | `apis:read`, `endpoints:read`, `domains:read`, `stats:read`, `settlements:read`, `openapi:read`, `billing:read`, `income:read` |
| `apiManager` | `apis:read`, `apis:write`, `endpoints:read`, `endpoints:write`, `domains:read`, `domains:write`, `openapi:read` |
| `analytics` | `stats:read`, `settlements:read`, `billing:read`, `income:read` |

API keys are created in the dashboard or with JWT-authenticated CLI commands:

```bash
launa scopes presets --json
launa keys create --name agent --scopes apis:read,endpoints:read --json
```

The key value is shown once. Never request, echo, log, or commit it.

`sandbox:wallet` is a separate, sensitive permission outside the presets above.
It allows preparing/funding and retrieving the account's Sandbox wallet, including
its private key, through `launa_sandbox_wallet`. It cannot access Live wallets or
reset a wallet. The AI client receives the key; review that permission at consent.
Existing OAuth connections need to reconnect to grant it. API-key connections
need an explicitly scoped Sandbox key. Do not silently widen an existing key.
