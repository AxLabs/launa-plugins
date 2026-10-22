---
name: discovery
description: >
  Publish and validate Launa API discovery metadata. Use for gateway
  openapi.json, /.well-known/x402.json, discovery validation, guidance,
  contact email, OpenAPI version, or endpoint schemas.
---

# API discovery

Ask for the target API and any requested public metadata that is missing. Read existing configuration first, reuse supplied information, and do not invent contact details or schemas.

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

Fetch the exact public OpenAPI and x402 discovery URLs returned by
`launa_discovery_urls`. Compare methods, paths, schemas, and payment terms with
`launa_get_api` and `launa_list_endpoints`. No external checker or wallet is required.
Report discrepancies without silently rewriting schemas or guidance. Ask for
missing public contact details or guidance if requested; never substitute the
account email or publish private information without the user's direction.
