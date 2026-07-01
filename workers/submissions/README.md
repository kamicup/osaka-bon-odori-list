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
