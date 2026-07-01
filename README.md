# 大阪市盆踊り開催状況状況調査プロジェクト (Osaka Bon-Odori Festival List)

本プロジェクトは、大阪市内で開催される盆踊り・夏祭りイベントのスケジュールや会場、出演者などの情報を公式情報源（自治体の広報誌、主催者のウェブサイトやSNS、出演者本人の発表等）から厳密に調査し、カレンダーおよび一覧レポートとして整理・管理するためのリポジトリです。

---

## 1. 成果物一覧へのアクセス

現在、2026年（令和8年）夏の調査レポートおよび各種カレンダーが以下に整理されています。

*   **2026年調査レポート (Markdown)**:
    [2026/bonodori_report_2026.md](file:///Users/yoshikazuhashimoto/tmp/2026/bonodori_report_2026.md)
    *   開催日順にソートされた詳細一覧表（盆踊り名称、日時、場所、出演者、公式ソースリンク、特記事項）。
    *   市と区は別の列で整理され、重点調査地域（東成・城東・中央・天王寺・浪速・都島・北・西・港）の広報誌7月号から最新の夏祭りスケジュールをすべて網羅しています。

*   **HTML版インタラクティブカレンダー (GitHub Pages公開・PC/スマホ両対応)**:
    *   **一般公開用URL (Webで直接開く)**: [https://kamicup.github.io/osaka-bon-odori-list/](https://kamicup.github.io/osaka-bon-odori-list/)
    *   **ローカルファイル**: [docs/index.html](file:///Users/yoshikazuhashimoto/tmp/docs/index.html)
    *   **データソースJSON**: [docs/events.json](file:///Users/yoshikazuhashimoto/tmp/docs/events.json) (※HTMLビューと完全に分離されたデータソース。このファイルをメンテすることで将来的にシステム化可能です)
    *   **GitHub Pages公開**: 本ファイルは GitHub Pages にホスティングされ、上記URLで全世界に公開されています。
    *   **PWA（アプリ化）対応**: スマホで開いた際、ブラウザの「ホーム画面に追加」（iOS Safari）や「アプリをインストール」（Android Chrome）を押すことで、スマホ上に独立したアプリとして登録できます。登録後は、ブラウザのツールバー等が隠れたネイティブアプリ同様の「全画面表示（スタンドアロン）」で快適に起動します。
    *   **インタラクティブ仕様**: カレンダーの日付マスをクリックすると、その日に開催されるすべての盆踊りの詳細（お祭り名称、会場場所、特記事項、情報ソースURLへの直接リンク）がポップアップモーダルで綺麗に表示されます。
    *   **テーマ切り替え**: 画面右上から「ライトモード（白基調）」と「ダークモード（お祭り夜空風の深紺）」をワンクリックで切り替え可能です。
    *   **スマホ表示最適化**: スマホでは横スクロールを発生させず、画面幅にすっぽりとカレンダーがスケールダウンして収まります。予定がある日はバッジで件数が示され、タップして詳細が開きます。
    *   **匿名情報提供フォーム**: 一般ユーザーがログインなしで盆踊り情報を投稿できます。投稿内容はCloudflare Worker経由でGitHub Issueとして作成され、管理者が公式情報を確認してから取り込みます。

---

## 2. ディレクトリ構成

```text
├── README.md               # 本ファイル（プロジェクト説明書）
├── docs/                   # GitHub Pages公開用フォルダ
│   ├── index.html          # ★HTMLビュー（events.json を非同期ロードして動的にカレンダーを描画）
│   ├── events.json         # ★カレンダーの純粋なデータソース（JSON形式）
│   ├── submission-config.js # 匿名投稿フォームのAPI URL設定
│   ├── manifest.json       # PWAウェブアプリ設定マニフェスト
│   ├── sw.js               # PWA用サービスワーカー（events.json を含む静的キャッシュ制御）
│   ├── icon-192.png        # PWAアプリアイコン (192px)
│   └── icon-512.png        # PWAアプリアイコン (512px)
├── 2026/                   # 2026年度（令和8年）調査成果物
│   ├── bonodori_report_2026.md    # 調査レポート（開催日時、場所、出演者等の詳細一覧）
│   ├── reproduction_prompt.md     # 調査およびレポート生成を最初から完全再現するAI用プロンプト
│   ├── build.py                    # HTMLカレンダーとJSONデータを一括生成するPythonスクリプト
│   └── generate_calendar_html.py   # インタラクティブHTMLカレンダーを自動生成するPythonスクリプト
├── workers/submissions/    # 匿名投稿をGitHub Issueへ変換するCloudflare Worker
│   ├── wrangler.jsonc      # Worker設定
│   ├── src/index.js        # 投稿API実装
│   └── README.md           # デプロイとシークレット設定手順
└── downloads/              # 一時ダウンロードデータの格納先（Git追跡対象外）
    └── .gitignore          # 内部ファイルをGit無視する設定
```

---

## 3. 再現・アップデート手順

### AIアシスタントによる調査の再現
本プロジェクトに格納されている [2026/reproduction_prompt.md](file:///Users/yoshikazuhashimoto/tmp/2026/reproduction_prompt.md) のプロンプトテキストをAIアシスタントにインプットすることで、同様の調査・パース要件に基づく成果物の作成をゼロから再現して実行させることができます。

### HTMLカレンダーの更新・再生成
HTMLカレンダーをデータソース（`bonodori_report_2026.md`）の更新に合わせて再生成したい場合は、`uv` を使って以下のスクリプトを実行してください。

```bash
# HTMLカレンダー（docs/index.html）とJSONデータ（docs/events.json）を更新
uv run python 2026/generate_calendar_html.py
```

### 匿名情報提供フォームの設定
投稿フォームを有効にするには、Cloudflare Workerをデプロイし、発行された `/submit` エンドポイントを `docs/submission-config.js` に設定します。

```bash
cd workers/submissions
wrangler secret put GITHUB_TOKEN
wrangler deploy
```

詳細は [workers/submissions/README.md](workers/submissions/README.md) を参照してください。

### 次シーズン公開前のGitHubトークン更新
匿名投稿フォームで使う `GITHUB_TOKEN` は90日期限で発行しています。次シーズンの公開前には、新しいFine-grained personal access tokenを発行し、Cloudflare Workerのsecretを再設定してください。

1. GitHubの `Settings` → `Developer settings` → `Personal access tokens` → `Fine-grained tokens` で新規トークンを作成します。
2. 対象リポジトリは `kamicup/osaka-bon-odori-list` のみに限定します。
3. Repository permissions は `Issues: Read and write` を付与します。
4. 生成されたトークンを以下でWorker secretに再設定します。

```bash
cd workers/submissions
wrangler secret put GITHUB_TOKEN
wrangler deploy
```

期限切れのままだと投稿フォームからGitHub Issueを作成できません。
