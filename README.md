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

*   **カレンダー画像 (PNGポスター)**:
    縦長高解像度のポスター形式で、すべてのイベントが日付のマスの中に直接テキストでプロットされています（重複日も文字が省略されず完全表示されます）。
    *   **7月通常版 (ダークテーマ)**: [大阪市盆踊りカレンダー2026_07.png](file:///Users/yoshikazuhashimoto/tmp/2026/大阪市盆踊りカレンダー2026_07.png)
    *   **7月印刷用 (背景純白)**: [大阪市盆踊りカレンダー2026_07_print.png](file:///Users/yoshikazuhashimoto/tmp/2026/大阪市盆踊りカレンダー2026_07_print.png)
    *   **8月通常版 (ダークテーマ)**: [大阪市盆踊りカレンダー2026_08.png](file:///Users/yoshikazuhashimoto/tmp/2026/大阪市盆踊りカレンダー2026_08.png)
    *   **8月印刷用 (背景純白)**: [大阪市盆踊りカレンダー2026_08_print.png](file:///Users/yoshikazuhashimoto/tmp/2026/大阪市盆踊りカレンダー2026_08_print.png)

---

## 2. ディレクトリ構成

```text
├── README.md               # 本ファイル（プロジェクト説明書）
├── docs/                   # GitHub Pages公開用フォルダ
│   ├── index.html          # ★HTMLビュー（events.json を非同期ロードして動的にカレンダーを描画）
│   ├── events.json         # ★カレンダーの純粋なデータソース（JSON形式）
│   ├── manifest.json       # PWAウェブアプリ設定マニフェスト
│   ├── sw.js               # PWA用サービスワーカー（events.json を含む静的キャッシュ制御）
│   ├── icon-192.png        # PWAアプリアイコン (192px)
│   └── icon-512.png        # PWAアプリアイコン (512px)
├── 2026/                   # 2026年度（令和8年）調査成果物
│   ├── bonodori_report_2026.md    # 調査レポート（開催日時、場所、出演者等の詳細一覧）
│   ├── reproduction_prompt.md     # 調査およびレポート生成を最初から完全再現するAI用プロンプト
│   ├── generate_calendar_ultra.py  # 高解像度PNGカレンダー画像を自動生成するPythonスクリプト
│   ├── generate_calendar_html.py   # インタラクティブHTMLカレンダーを自動生成するPythonスクリプト
│   ├── 大阪市盆踊りカレンダー2026_07.png       # 7月カレンダー（通常版）
│   ├── 大阪市盆踊りカレンダー2026_07_print.png # 7月カレンダー（印刷用・背景白）
│   ├── 大阪市盆踊りカレンダー2026_08.png       # 8月カレンダー（通常版）
│   └── 大阪市盆踊りカレンダー2026_08_print.png # 8月カレンダー（印刷用・背景白）
└── downloads/              # 一時ダウンロードデータの格納先（Git追跡対象外）
    └── .gitignore          # 内部ファイルをGit無視する設定
```

---

## 3. 再現・アップデート手順

### AIアシスタントによる調査の再現
本プロジェクトに格納されている [2026/reproduction_prompt.md](file:///Users/yoshikazuhashimoto/tmp/2026/reproduction_prompt.md) のプロンプトテキストをAIアシスタントにインプットすることで、同様の調査・パース要件に基づく成果物の作成をゼロから再現して実行させることができます。

### カレンダー画像＆HTMLの更新・再生成
カレンダー画像をデータソース（`bonodori_report_2026.md`）の更新に合わせて再生成したい場合は、仮想環境のPythonを使って以下のスクリプトを実行してください。

```bash
# 2026/ フォルダへ移動
cd 2026/

# PNG画像を更新
../.venv/bin/python generate_calendar_ultra.py

# HTMLカレンダー（docs/index.html）を更新
../.venv/bin/python generate_calendar_html.py
```
