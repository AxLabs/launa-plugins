---
name: discovery
description: >
  Publish and validate Launa API discovery metadata. Use for gateway
  openapi.json, /.well-known/x402.json, AgentCash discovery, guidance,
  contact email, OpenAPI version, or endpoint schemas.
---

# API discovery

Discovery documents are public, unpaid gateway routes generated from live API
and endpoint configuration:

- `https://{gateway-host}/openapi.json`
- `https://{gateway-host}/.well-known/x402.json`

Use `launa_discovery_urls` to obtain exact URLs. Never derive the hostname by
guessing.

## Improve discovery

1. Read the API and endpoints.
2. Set API-level guidance, contact email, or version with
   `launa_set_discovery_guidance`.
3. Set meaningful endpoint request/response schemas with
   `launa_update_endpoint_schemas` or `launa_update_endpoint`.
4. Fetch fresh URLs with `launa_discovery_urls`.

Disabled and ephemeral endpoints are omitted from discovery.

## Validate

The AgentCash checker is CLI-only and requires Node.js 20+:

```bash
npx -y @agentcash/discovery@1.7.5 check "https://gateway.example/"
npx -y @agentcash/discovery@1.7.5 discover "https://gateway.example/"
```

Run it only against a URL returned by `launa_discovery_urls`. Report validation
failures without silently rewriting schemas or guidance.
