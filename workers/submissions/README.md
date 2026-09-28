# 盆踊り情報投稿 Worker

この Worker は、公開カレンダーから匿名で投稿された祭り情報を受け取り、確認用の GitHub Issue を作成します。

## 設定

プロジェクトの依存関係をインストールし、ローカルの Wrangler CLI を確認します。

```bash
cd workers/submissions
npm ci
npx wrangler --version
```

必要に応じて Cloudflare にログインします。

```bash
npx wrangler login
```

GitHub トークンを Worker のシークレットとして設定します。このトークンには、`kamicup/osaka-bon-odori-list` に Issue を作成する権限が必要です。

```bash
cd workers/submissions
npx wrangler secret put GITHUB_TOKEN
```

必要に応じて Turnstile による保護を設定します。

```bash
npx wrangler secret put TURNSTILE_SECRET_KEY
```

`wrangler.jsonc` で `ALLOWED_ORIGIN`、`GITHUB_OWNER`、`GITHUB_REPO`、`ISSUE_LABELS` を設定してください。

## GitHub トークンの更新

`GITHUB_TOKEN` の有効期限は発行から 90 日間です。次の祭りシーズンを公開する前に、新しい Fine-grained personal access token を作成し、Worker のシークレットを更新してください。

1. GitHub の `Settings` → `Developer settings` → `Personal access tokens` → `Fine-grained tokens` を開きます。
2. 対象リポジトリを `kamicup/osaka-bon-odori-list` のみに限定して、新しいトークンを作成します。
3. リポジトリ権限の `Issues: Read and write` を付与します。
4. Worker のシークレットを更新してデプロイします。

```bash
cd workers/submissions
npx wrangler secret put GITHUB_TOKEN
npx wrangler deploy
```

トークンの有効期限が切れた場合、公開フォームは引き続き表示されますが、Issue の作成に失敗します。

## デプロイ

```bash
cd workers/submissions
npx wrangler deploy --dry-run
npx wrangler deploy
```

デプロイ後、`docs/submission-config.js` を更新します。

```js
window.BONODORI_SUBMISSION_API_URL = "https://osaka-bon-odori-submissions.<your-subdomain>.workers.dev/submit";
window.BONODORI_TURNSTILE_SITE_KEY = "";
```

Turnstile を有効にする場合は、公開用のサイトキーを `BONODORI_TURNSTILE_SITE_KEY` に設定してください。
