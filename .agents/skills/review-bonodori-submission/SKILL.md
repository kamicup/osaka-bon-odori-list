---
name: review-bonodori-submission
description: "Review anonymous Osaka Bon-Odori calendar submissions that arrive as GitHub issues. Use when Antigravity is asked to inspect issues created by the public submission form, verify festival data against official sources, decide whether to update `2026/bonodori_report_2026.md`, regenerate `docs/events.json` and `docs/index.html`, and comment on or close the GitHub issue."
---

# Review Bon-Odori Submission

## Core Workflow

1. Confirm the repository context is `kamicup/osaka-bon-odori-list` or a checkout containing `2026/bonodori_report_2026.md`, `2026/build.py`, and `workers/submissions/`.
2. Inspect relevant open issues with `gh issue list --label submission --state open --limit 20 --json number,title,labels,url,createdAt,body`. If the user names an issue number, use `gh issue view <number> --json number,title,labels,url,createdAt,body,comments`.
3. Parse the fixed anonymous-form section:

```text
## 投稿内容
- イベント名:
- 開催日:
- 開催時間:
- 会場:
- 住所:
- 区:
- 公式情報URL:
- 補足:
```

4. Classify the submission before editing files:
   - **Reject / no data change**: obvious test data, spam, unrelated event, missing official source, top-page-only source with no event details, impossible date, or duplicate of an existing entry.
   - **Needs clarification**: plausible event but official source does not confirm date, time, venue, ward, organizer, rain policy, or the submitted URL is insufficient.
   - **Accept**: official or organizer source confirms enough details to update the 2026 schedule.
5. Verify accepted or borderline submissions against the official URL first. Use web browsing when needed because festival pages and municipal notices change. Prefer primary sources: organizer pages, city/ward pages, venue pages, official flyers or PDFs.
6. Search existing data before adding anything:

```bash
rg -n "イベント名|会場|公式情報URLのドメイン|開催日" 2026/bonodori_report_2026.md docs/events.json
```

7. For accepted submissions, update `2026/bonodori_report_2026.md` in the existing report style, preserving Japanese names and source text. Include the official source URL. Add uncertainty notes only if the surrounding report already uses that style.
8. Regenerate outputs with `uv`:

```bash
uv run python 2026/build.py
```

Use `uv run python 2026/generate_calendar_html.py` only when the user specifically wants the calendar generator instead of the full build.
9. Validate generated files:
   - `docs/events.json` parses as JSON.
   - The new or changed event appears with the expected date, venue, ward, source URL, and modal details.
   - `git diff -- 2026/bonodori_report_2026.md docs/events.json docs/index.html` contains only expected changes.
10. If the change affects the final public display or cached data (`docs/index.html`, `docs/events.json`, icons, manifest, or other user-visible assets), bump `CACHE_NAME` in `docs/sw.js` (for example `bonodori-cache-v5` to `bonodori-cache-v6`) so deployed users receive the update.
11. For any accepted submission or issue-driven code/data fix, commit the changes, push a branch, create a PR, and merge the PR before closing the issue. Include the PR link in the issue comment. If the user explicitly asks not to merge, leave the issue open and explain the pending PR.
12. Comment on the issue with the action taken, evidence checked, generated command run, cache-version change if applicable, and PR link. Close the issue only after the PR has been merged, or when the submission was clearly invalid/test data and required no repository change. Leave it open with `needs-review` when human confirmation is still required.

## Issue Response Policy

Use concise Japanese comments.

For accepted submissions:

```markdown
確認しました。公式情報で日付・会場・区を確認できたため、`2026/bonodori_report_2026.md` に反映し、`uv run python 2026/build.py` で `docs/events.json` と `docs/index.html` を再生成しました。

確認元: <URL>
```

For rejected test submissions:

```markdown
テスト投稿として確認しました。実在イベントとして反映できる公式開催情報ではないため、予定表への変更は行いません。
```

For insufficient sources:

```markdown
投稿内容を確認しましたが、提示 URL から開催日・時間・会場を確認できませんでした。公式告知、主催者ページ、またはチラシ PDF など確認可能な URL が必要です。
```

## Safety Rules

- Do not add an event from user-submitted text alone. Require an official or organizer source.
- Do not infer dates from compact strings such as `20260701` without confirming the intended date and display format from the source.
- Do not treat generic venue top pages as evidence unless the event is visible there.
- Do not edit generated files by hand. Edit the report, then run the generator.
- Do not forget the PWA cache: when final display output changes, include the `docs/sw.js` cache-version bump in the same PR.
- Do not close non-test issues if verification failed for temporary network or source availability reasons; comment with the blocker instead.
- Preserve unrelated local changes. Check `git status --short` before editing and inspect relevant diffs before finalizing.

## Useful Commands

```bash
gh issue list --label submission --state open --limit 20 --json number,title,labels,url,createdAt,body
gh issue view <number> --json number,title,labels,url,createdAt,body,comments
gh issue comment <number> --body "<Japanese review comment>"
gh issue close <number> --reason completed
gh pr create --base main --head <branch> --title "<title>" --body "<body>"
gh pr merge <number-or-url> --merge --delete-branch
uv run python 2026/build.py
uv run python -m json.tool docs/events.json >/tmp/events.json.validated
git diff -- 2026/bonodori_report_2026.md docs/events.json docs/index.html
```
