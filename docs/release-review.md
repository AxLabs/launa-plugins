# Launa 0.1.2 reviewer preparation

Status: production service deployed; native Cursor production acceptance and
marketplace submission pending. These are proposed cases, not completed tests.

## Listing copy

- Name: Launa
- Publisher: AxLabs
- Website: https://launa.io
- Repository: https://github.com/AxLabs/launa-plugins
- Support: https://github.com/AxLabs/launa-plugins/issues
- Privacy: https://launa.io/privacy
- Terms: https://launa.io/terms

Connect Launa to Cursor to manage APIs, endpoint pricing, domains, discovery,
analytics and settlements. Sign in through your browser, review permissions,
and choose Test or Live mode. The hosted developer plugin includes 42
control-plane tools, eight skills and five commands. No local Node.js runtime
or wallet is needed for the connection.

The plugin configures APIs that use x402 payments; it does not expose buyer
payment, wallet signing, arbitrary transfers or payout-execution tools. Write
permissions include deleting resources and changing API payout destinations and
webhooks. Do not describe these permissions as read-only access.

## Reviewer access and evidence

Use a dedicated reviewer account with Test-mode fixtures. Supply access details
only through a private reviewer channel if requested; never commit them or put
them in a demo. Reviewers need no wallet credentials or mainnet funds. Disclose
service-account requirements and applicable service charges accurately.

Record release commit, Cursor version, plugin version, test date and results
from [production acceptance](cursor-production-test.md). A sanitized demo should
show installation, logo/links, browser consent, Test-mode inventory, disposable
API creation/update/deletion and revocation/reconnect. Exclude login entry,
cookies, API keys, OAuth callback parameters and private customer data.

## Expected behavior

| Case | Expected outcome |
| --- | --- |
| Deny consent | No authenticated control-plane access. |
| Approve Test mode | Only the account's Test-mode configuration is visible. |
| List APIs/endpoints | Matches the Test dashboard, without mutation or credential disclosure. |
| Create without a required payout address | Actionable validation error; no partial API creation. |
| Create/update/delete a disposable API | Only explicitly selected test resources change. |
| Reload Cursor | Connection works or clearly requests authentication. |
| Revoke the connection's backend key | The next backend operation fails; reconnect can establish a new grant. |
| Request buyer payment | No buyer payment tool is exposed by this plugin. |

Token expiry/replay, callback validation, scopes and storage concurrency belong
to the runtime's regression tests. Native client and runtime tests provide
different evidence; record both honestly.
