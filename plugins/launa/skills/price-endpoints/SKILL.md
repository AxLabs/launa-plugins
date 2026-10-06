---
name: price-endpoints
description: >
  Create, update, delete, or bulk-import paid Launa endpoints. Use for route
  pricing, payment schemes, token accepts, TTL endpoints, request/response
  schemas, or importing OpenAPI.
---

# Price endpoints

Read the API and existing routes with `launa_get_api` and
`launa_list_endpoints` before mutating them.

## Add or update

- Use `launa_add_endpoint` for a new method + path.
- Use `launa_update_endpoint` for enabled state, route metadata, pricing,
  accepts, or schemas.
- `price_usdc` uses the platform's default USDC accept.
- For another token, first call `launa_supported_networks`; pass `network`,
  `asset`, and either decimal `price` + `decimals` or atomic `amount`.
- Pass a complete `accepts` array when preserving multiple payment options.
- `ttl` is create-only and makes the endpoint ephemeral. It disappears after
  first settlement or expiry and is excluded from discovery documents.
- Use `request_schema` and `response_schema` so agents can understand inputs
  and outputs. `clear_schemas` clears and re-infers defaults.

Sandbox supports `exact` only. Do not select `batch-settlement` when
`LAUNA_ENVIRONMENT=development`.

## OpenAPI

1. Call `launa_parse_openapi` with YAML or JSON.
2. Review operations and the suggested upstream with the user.
3. Call `launa_import_openapi` with API id, spec, and default USDC price.
4. List endpoints and report created/skipped operations.

Import skips existing method + path keys.

## Delete

Show method, path, price accepts, and endpoint id. Call
`launa_delete_endpoint` only after explicit user confirmation.

Never hardcode chain IDs, token addresses, or decimals. Derive them from
`launa_supported_networks` or existing endpoint accepts.
