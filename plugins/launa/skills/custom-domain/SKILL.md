---
name: custom-domain
description: >
  Configure an Launa custom gateway domain. Use when planning a hostname,
  adding DNS CNAME/TXT records, checking verification, listing domains, or
  removing a custom domain.
---

# Custom domains

## Add and verify

1. Call `launa_domain_suggest` with the apex and optional prefix/path.
2. Confirm the intended gateway hostname with the user.
3. Call `launa_add_domain`.
4. Present the returned CNAME target and TXT verification record exactly.
5. Wait for the user to add DNS records.
6. Call `launa_verify_domain`.
7. Call `launa_discovery_urls` and report discovery URLs for the verified host.

Do not invent DNS names, targets, tokens, or records. Use the tool response.
DNS propagation can delay verification; report pending status without repeatedly
changing records.

## Remove

Call `launa_list_domains`, show the hostname and domain id, then call
`launa_delete_domain` only after explicit user confirmation. Removing a domain
does not delete the API or its default Launa subdomain.
