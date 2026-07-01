# 大阪市盆踊りカレンダー HTML版 の手軽な公開方法ガイド

本プロジェクトで生成された [docs/index.html](file:///Users/yoshikazuhashimoto/tmp/docs/index.html) は、**HTML/CSS/Javascriptがすべて1つのファイルに完結している（単一の静的HTML）**ため、サーバーのバックエンドやデータベースを設定することなく、完全無料で即座に一般公開することができます。

一般ユーザーがスマホやPCから簡単にアクセスできるようにするための、GitHub Pagesを使った公開手順を解説します。

---

## 1. GitHub Pages を使った公開手順 (推奨・無料)

本プロジェクトはすでに `docs/index.html` にカレンダーHTMLを出力する構成に変更されています。リポジトリをGitHubにプッシュするだけで簡単に公開できます。

### ステップ 1: GitHubへプッシュ
1. `docs/index.html` が生成されていることを確認します。
2. Gitでコミットし、GitHub上の公開リポジトリ（Public）へプッシュします。
   ```bash
   git add docs/index.html README.md 2026/generate_calendar_html.py
   git commit -m "Configure docs/index.html for GitHub Pages"
   git push origin main
   ```

### ステップ 2: GitHub上でホスティング設定を有効にする
1. ブラウザでGitHubにログインし、対象リポジトリのページを開きます。
2. 上部メニューから **Settings (設定)** をクリックします。
3. 左サイドバーにある **Pages** をクリックします。
4. **Build and deployment** セクションにある以下の項目を設定します。
   * **Source**: `Deploy from a branch` (デフォルトのまま)
   * **Branch**: `main` (または `master`) を選択し、その右側のフォルダ選択で **`/docs`** を選択します。
5. **Save (保存)** ボタンをクリックします。

### ステップ 3. **一般公開URLの確認**
   * 設定保存後、1〜2分ほどで自動ビルドが走り公開されます。
   * 公開されたWebサイトのURL: [https://kamicup.github.io/osaka-bon-odori-list/](https://kamicup.github.io/osaka-bon-odori-list/)
   * このURLをコピーし、一般のユーザー（SNS、LINEなど）に共有すれば、誰でもスマホやPCからカレンダーを開くことができます。

---

## 2. 運用・更新手順
盆踊りのデータソース（`bonodori_report_2026.md`）にイベント情報が追加・修正された際は、以下のコマンドでHTMLを再生成してプッシュするだけで、Web上のカレンダーも自動で最新にアップデートされます。

```bash
# HTMLの再生成 (自動で docs/index.html が上書き更新されます)
./.venv/bin/python 2026/generate_calendar_html.py

# 変更をコミットしてプッシュ
git add docs/index.html
git commit -m "Update bonodori calendar data"
git push origin main
```

---

## 3. PWA機能（スマホへのホーム画面・アプリ追加）について

本カレンダーは **PWA (Progressive Web App)** に対応しています。これにより、一般ユーザーが手元のスマートフォンにネイティブアプリと同じようにインストールして、全画面で起動できるようになります。

### インストール方法（ユーザー側の手順）
* **iPhone (Safari)**:
  1. 公開URL [https://kamicup.github.io/osaka-bon-odori-list/](https://kamicup.github.io/osaka-bon-odori-list/) をSafariで開きます。
  2. 画面下部中央の **「共有ボタン（上矢印のアイコン）」** をタップします。
  3. メニューをスクロールし、**「ホーム画面に追加」** をタップして登録します。
* **Android (Chrome)**:
  1. Chromeで公開URLを開きます。
  2. 画面下部やメニュー内に表示される **「アプリをインストール」** または **「ホーム画面に追加」** をタップして登録します。

### インストール後のメリット
* ホーム画面に、お祭りの提灯をデザインした**美しいアプリアイコン（「大阪盆踊り」）**が追加されます。
* アプリを起動すると、ブラウザの上部アドレスバーや下部メニューバーが一切表示されない **「全画面モード（スタンドアロン）」** で立ち上がり、完全に独立したスマートフォンのアプリとして快適に盆踊りカレンダーを利用できます。
