---
name: cors
description: >
  Manage allowed browser origins for an Launa API. Use when a browser,
  React paywall, or frontend request is blocked by CORS or when reviewing
  gateway origin access.
---

# CORS

1. Read current origins with `launa_get_cors`.
2. Identify the exact browser origin: scheme, host, and port only.
3. Use `launa_add_cors_origin` for one origin or `launa_set_cors` to replace
   the full list.
4. Read again and report the resulting list.

Use `launa_remove_cors_origin` only after confirming the exact origin with the
user. Replacing the list can remove working applications; show old and new
lists before calling `launa_set_cors`.

Do not add paths, wildcards, trailing slashes, or credentials unless the Launa
API explicitly supports them.
