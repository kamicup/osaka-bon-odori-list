# Bon Odori Submission Worker

This Worker receives anonymous festival information submissions from the public calendar and creates GitHub issues for review.

## Configure

Set the GitHub token as a Worker secret. The token needs permission to create issues in `kamicup/osaka-bon-odori-list`.

```bash
cd workers/submissions
wrangler secret put GITHUB_TOKEN
```

Optional Turnstile protection:

```bash
wrangler secret put TURNSTILE_SECRET_KEY
```

Set `ALLOWED_ORIGIN`, `GITHUB_OWNER`, `GITHUB_REPO`, and `ISSUE_LABELS` in `wrangler.jsonc`.

## Renew GitHub Token

`GITHUB_TOKEN` is issued with a 90-day expiration. Before publishing the next festival season, create a new fine-grained personal access token and update the Worker secret.

1. Open GitHub `Settings` -> `Developer settings` -> `Personal access tokens` -> `Fine-grained tokens`.
2. Generate a new token for `kamicup/osaka-bon-odori-list` only.
3. Grant repository permission `Issues: Read and write`.
4. Update the Worker secret and deploy:

```bash
cd workers/submissions
wrangler secret put GITHUB_TOKEN
wrangler deploy
```

If this token expires, the public form remains visible but issue creation fails.

## Deploy

```bash
cd workers/submissions
wrangler deploy
```

After deployment, update `docs/submission-config.js`:

```js
window.BONODORI_SUBMISSION_API_URL = "https://osaka-bon-odori-submissions.<your-subdomain>.workers.dev/submit";
window.BONODORI_TURNSTILE_SITE_KEY = "";
```

If Turnstile is enabled, set the public site key in `BONODORI_TURNSTILE_SITE_KEY`.
