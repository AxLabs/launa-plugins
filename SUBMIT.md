# Marketplace publication

Release candidate: **Launa 0.1.2**. Production hosted MCP and consent are deployed.
The public repository is Apache-2.0 licensed. Native production acceptance and
marketplace submission remain pending. This candidate is on staging; main still
contains the older local-server plugin until promotion.

## Cursor

1. Run `python3 scripts/validate.py` and complete the
   [native production test](docs/cursor-production-test.md).
2. Review the tested candidate, promote it to main, and record the full public
   commit SHA. Confirm main contains version 0.1.2 and the production MCP URL.
3. Use the [reviewer pack](docs/release-review.md) for listing text, support,
   privacy and terms links, and sanitized test evidence. Prepare private
   reviewer access if requested; do not commit credentials.
4. Sign in to [Cursor's publisher form](https://cursor.com/marketplace/publish)
   using the AxLabs publisher account and submit:
   https://github.com/AxLabs/launa-plugins
5. Cursor reviews the submission. Respond to concrete feedback and verify the
   published installation before announcing availability. A Git push is not a
   store listing or proof an update has been approved.

The root `.cursor-plugin/marketplace.json` identifies `plugins/launa`.
Its manifest uses hosted OAuth, the square icon and https://launa.io as Website.
This is a developer control-plane plugin; buyer inspection/payment tools are
not bundled. Do not use historical buyer-payment demo instructions for review.

Official requirements checked 2026-10-22:
[manifest/submission reference](https://cursor.com/docs/reference/plugins) and
[installation and review](https://cursor.com/docs/plugins).

## Other marketplaces

Claude Code, Grok Build and Codex / ChatGPT formats remain in the repository,
but Cursor acceptance does not establish their native compatibility or listing.
Each needs its own current submission requirements, native OAuth evidence and
separate submission authorization.

Earlier multi-market research is preserved in
[historical notes](docs/archive/submission-research-2026-10-20.md).
Those notes describe superseded packaging and must not be used as current
release instructions. The [hosted rollout](docs/hosted-mcp.md) describes the
current authentication and tool surface.
