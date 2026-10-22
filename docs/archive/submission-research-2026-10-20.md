# Historical submission research — superseded

Not current release instructions. See ../../SUBMIT.md and ../release-review.md.

# Marketplace publication guide

> **Current rollout supersedes the local-runtime instructions below:** all client
> manifests now use hosted OAuth and 42 developer control-plane tools. Buyer
> inspection/payment skills are excluded from every default plugin. The older
> local submission research below is historical, not the current configuration
> or evidence of native OAuth acceptance. Use [the rollout guide](https://github.com/AxLabs/launa-plugins/blob/staging/docs/hosted-mcp.md)
> and regenerate reviewer evidence before any submission. Production deployment,
> each native client sign-in, and marketplace publication remain release gates.


Requirements checked against official sources on 2026-10-20. This repository
contains one Launa plugin (`plugins/launa`) with manifests for several clients.
A repository marketplace and a curated public listing are separate channels.

**Release approach:** submit the full feature set, including buyer payments.
Keep payment capabilities accurately disclosed. Treat policy concerns as
marketplace-specific review risks and adapt only in response to concrete
feedback; do not preemptively remove tools. No submission or publication has
been performed. Prepare the complete submission and explain that Launa sells
API access rather than providing an arbitrary-address transfer interface; let
the marketplace assess that use case through its normal review. See the
[reviewer preparation pack](docs/release-review.md) for copy, cases, and a demo outline.

## Shared preparation and observed gaps

- Push the reviewed `0.1.1` release to the public
  [AxLabs/launa-plugins repository](https://github.com/AxLabs/launa-plugins).
  The previous public-source check found `@launa/mcp-server`; the local changes pin
  `@launaio/mcp-server@0.0.7`. Record the final remote commit for submissions.
  Locally, remote `launa` targets the new repository; `origin` still names
  `AxLabs/ax402-plugins`.
- Brand rules were read from Launa's Notion brand guide on 2026-10-20.
  The existing icon uses the specified lime `#B8E961` on ink `#0E1301`.
  OpenAI metadata now uses the square icon, ink for light-theme contrast and
  lime for dark-theme contrast. Asset geometry was not compared byte-for-byte
  with the downloadable brand master.
- `https://launa.io/docs/agents` still returned 404 on 2026-10-20. Manifest
  documentation links now use the repository README. The product homepage
  and GitHub Issues support URL returned HTTP 200.
- Prepare a sandbox reviewer account, sample data,
  configuration instructions, and a short demonstration. Reviewer credentials
  must stay outside the public repository.
- Test actual installation and onboarding in each client. Direct MCP smoke
  tests passed for all five configurations, including mocked seller requests
  and wallet-free 402 inspection; native client onboarding is still untested.

`python3 scripts/validate.py` passes (12 JSON files, 9 skills, 6 commands),
including OpenAI listing consistency and Claude credential-reference checks.
`claude plugin validate ./plugins/launa` passes. The installed Claude CLI does
not support `--strict`; current docs recommend that flag with a current CLI.
Local validation does not establish directory acceptance.

## Cursor Marketplace

**Current source uses hosted OAuth; deployment and native sign-in verification
are release blockers.** Follow [hosted rollout](docs/hosted-mcp.md) before
submitting this configuration. Other clients still use the local runtime.


Submit the public GitHub repository at
[Cursor's publisher form](https://cursor.com/marketplace/publish). Required
preparation includes valid manifests/frontmatter, relative component paths,
configuration documentation, local testing, and the root marketplace index
for a multi-plugin layout. Cursor reviews submissions before listing them.
Our repository has the expected basic structure; name availability and
publisher-account access still need confirmation.

Use a real copy of `plugins/launa` in `~/.cursor/plugins/local/` for testing.
Current Cursor ignores symlinks whose targets are outside that directory;
the README recipes use copies. Reload and check the
API-key variables UI, skills, rules, commands, and running MCP server.

There is direct wallet precedent: Cursor lists
[MetaMask Agent Wallet](https://prod.cursor.com/marketplace/metamask) with swaps,
bridges, and other wallet workflows. Its [marketplace](https://prod.cursor.com/marketplace)
also lists PayBox with x402 payments, providing a closer precedent for Launa.
This supports trying Launa's complete feature set here; it does not establish
another marketplace's policy.

Keep the plugin itself free and check how the publisher terms apply to the
paid API service behind it. The terms describe requesting re-indexing for
updates, so a Git push alone should not be treated as a completed listing
update.

Sources: [submission checklist](https://cursor.com/docs/reference/plugins),
[local testing](https://cursor.com/docs/plugins),
[publisher terms](https://cursor.com/marketplace-publisher-terms).

## Grok Build official catalog

Submit a PR to [xai-org/plugin-marketplace](https://github.com/xai-org/plugin-marketplace).
Add a remote entry to `.grok-plugin/marketplace.json`, using the public release
commit and `plugins/launa` subdirectory. The SHA must be the complete
40-character lowercase commit hash. The official index generator supports
`source.path` for remote subdirectories.

```json
{
  "name": "launa",
  "description": "Manage Launa APIs, configure x402 pricing, inspect and pay gateway URLs, and review settlements.",
  "category": "development",
  "source": {
    "source": "url",
    "url": "https://github.com/AxLabs/launa-plugins.git",
    "sha": "REPLACE_WITH_FULL_RELEASE_COMMIT_SHA",
    "path": "plugins/launa"
  },
  "homepage": "https://launa.io",
  "keywords": ["launa", "launa x402", "launa mcp"],
  "domains": ["launa.io", "api.launa.io"]
}
```

Replace the placeholder before validation. In the catalog checkout:

```bash
python3 scripts/generate-plugin-index.py
python3 scripts/validate-catalog.py
python3 scripts/generate-plugin-index.py --check
```

Commit the entry and generated index. CI and code-owner review are required.
Updates replace the SHA and regenerate the index. Use brand-specific keywords:
the contribution guide warns against generic discovery terms such as `api`
and `cli`. Document network destinations and credential needs in the README.
The existing own-repository Grok marketplace does not create an official
listing. No wallet/x402 entries matched the official catalog search during
this review; that is not evidence of a prohibition.

Sources: [catalog process](https://github.com/xai-org/plugin-marketplace/blob/main/README.md),
[contribution requirements](https://github.com/xai-org/plugin-marketplace/blob/main/CONTRIBUTING.md),
[subdirectory handling](https://github.com/xai-org/plugin-marketplace/blob/main/scripts/generate-plugin-index.py).

## Claude directory

Use [claude.ai/directory/manage](https://claude.ai/directory/manage), choose
**Plugin bundle**, and provide `AxLabs/launa-plugins` with path `plugins/launa`.
Connect a GitHub account with push permission. Select the tracked branch/tag,
validate that exact commit, complete listing/data-handling/contact details,
and submit. The repository must be public at publication. Updates track that
source; an optional GitHub webhook accelerates discovery. Passing checks is
not the same as publication: follow the review/publish mode assigned by
Anthropic.

A paid Claude plan and an eligible owner/delegated role are required. This
public directory differs from `claude-plugins-official`; the latter's listing
route is through an Anthropic partner contact.

Sources: [submission flow](https://claude.com/docs/plugins/submit),
[distribution routes](https://code.claude.com/docs/en/plugins/publish).

Pre-submission work for Launa:

- Claude credential onboarding now uses sensitive `userConfig` fields and a
  Claude-only inline `launa` MCP configuration. The same-name server overrides
  the default `.mcp.json` server, preserving the other clients' configuration.
  Optional empty defaults permit wallet-free inspection. Native prompting and
  secure storage still need client tests.
- Both package launchers are pinned: MCP `0.0.7` and discovery helper `1.7.5`.
  The latter needs Node.js 20+. Exact npm pins can still cause a reviewer hold
  because transitive dependencies resolve at installation time.
- The plugin README now documents subprocesses, destinations, credentials,
  payment behavior, support, and data handling.
- Add applicable MCP titles and read/destructive annotations in the SDK-owned
  server; its current registrations lack these hints. Prepare a standard
  test account and at least three working examples.

Sources: [automated checklist](https://claude.com/docs/plugins/pre-submission-checklist),
[developer/server policy](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy).

Local MCP is ignored in Claude chat, loads in Claude Code, and loads in
Cowork sessions running on the user's computer. Cowork does not prompt for
required `userConfig` options without defaults. Verify onboarding on the
claimed surfaces. A hosted server needs a separate connector submission if
bundled with the plugin. See [surface support](https://claude.com/docs/plugins/platform-support).

**Review risk:** Anthropic's directory policy excludes financial execution,
including crypto transfers, unless expressly permitted in writing. Present
`launa_pay_url` accurately, including user authorization and wallet handling,
as part of the normal full-feature submission review. A wallet-related listing
alone does not establish permission for every signing/transfer workflow.
[Policy source](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy).

## OpenAI directory: Codex and ChatGPT

Self-installation through `.agents/plugins/marketplace.json` is separate from
public directory submission. Choose one publication route:

- **Desktop-only:** local MCP submissions require approved-partner status and
  an allowlisted organization. The documented package includes the server and
  its dependencies; our npm-launch configuration is not yet that bundled
  artifact. Confirm eligibility and onboarding with the OpenAI representative.
  See [local submission requirements](https://developers.openai.com/plugins/deploy/desktop-only).
- **Remote:** build and deploy a stable HTTPS MCP service with OAuth for
  protected seller operations. The portal does not support API-key connection
  setup. Current stdio/API-key packaging needs adaptation, and a shared token
  embedded in headers is not a substitute. See
  [authentication](https://developers.openai.com/plugins/build/auth) and
  [package authentication](https://developers.openai.com/plugins/build/plugins).

Prepare a verified publishing identity, submission role, complete ZIP,
reviewer account, five positive and three negative cases, and demo video.
Complete checks, submit, then publish the approved version. The listing needs
website/support/privacy/terms links, a subtitle up to 30 characters, square
icons, and a light-theme brand color with at least 2:1 contrast against white.
See [submission requirements](https://developers.openai.com/plugins/deploy/submission).

Metadata preparation completed locally:

- `supportURL` points to the public GitHub Issues page.
- Subtitle is now “Paid APIs for agents” (20 characters).
- Primary `logo` uses the existing 256 × 256 square icon.
- Light-theme `brandColor` uses brand ink `#0E1301`; dark-theme color uses
  brand lime `#B8E961`.
- Root `extensions.com.openai.interface` and the compatibility manifest now
  carry identical listing metadata, with payment functionality disclosed.

These metadata changes do not bundle the local MCP server or establish
publisher eligibility. The local source ZIP remains a review artifact.

**Review risk:** published OpenAI guidelines prohibit money/crypto transfer
execution and selling digital products/services. Those provisions appear
relevant to buyer payments for APIs. Submit the full behavior transparently
and let the normal submission review assess API purchases; do not describe it as already
approved or remove features before feedback. Hosting the MCP remotely does
not itself settle this policy question.
[Guidelines](https://developers.openai.com/plugins/plugin-guidelines).

## cursor.directory community listing

[Submit a Plugin](https://cursor.directory/plugins/new) supports importing a
GitHub repository or creating a listing manually. It is independent of the
curated Cursor marketplace. Check the importer's selected plugin path, MCP
command, branding, and description. Account-only fields, listing-name
availability, and review timing were not established from the public page.

## Official MCP Registry

This publishes MCP metadata, not plugin skills/commands. The SDK repository
has no `tools/mcp-server/server.json` and no `mcpName` in the MCP package.

Choose an ownership-verifiable namespace, add matching `mcpName` package
metadata, and publish a new npm version containing it. Published `0.0.7`
cannot be edited in place. Create `server.json` for that version with stdio
transport and environment inputs. Authenticate, validate, and publish with
`mcp-publisher`. Verify organization namespace permissions for AxLabs rather
than assuming personal GitHub login covers them. Update the plugin package
pin if the chosen MCP version changes.

Source: [official publishing guide](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/quickstart.mdx).

## Execution order

1. Finish native client onboarding tests and verify the existing icon geometry
   against the brand master; listing URLs and metadata have been corrected.
2. Prepare reviewer accounts, example prompts, data-handling answers, and demo.
3. Commit/push the reviewed release and verify the public commit.
4. Submit Cursor, the Grok catalog PR, and cursor.directory.
5. Submit Claude with full capability disclosure; pursue OpenAI local partner
   eligibility or the hosted OAuth route with the same full-feature intent.
6. Publish the MCP Registry record through an SDK package release.
7. Track actual reviewer findings and make only the adaptations they require.

Publisher account permissions, name availability, partner eligibility, native
client onboarding, and marketplace decisions remain unverified. No marketplace
has been asserted to approve Launa.
