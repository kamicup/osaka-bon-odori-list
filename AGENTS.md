# Repository Guidelines

## Project Structure & Module Organization

This repository maintains the Osaka Bon-Odori festival schedule and public calendar. The main research source is `2026/bonodori_report_2026.md`. Python generator scripts live in `2026/`, including `build.py` and `generate_calendar_html.py` for the web calendar data/view. Public GitHub Pages output lives in `docs/`: `index.html`, `events.json`, `manifest.json`, `sw.js`, and PWA icons. Keep temporary source downloads in `downloads/`; its contents are ignored.

## Build, Test, and Development Commands

Use the repo-local virtual environment when available:

```bash
./.venv/bin/python 2026/build.py
```

Runs the full build, regenerating `docs/index.html` and `docs/events.json`.

```bash
./.venv/bin/python 2026/generate_calendar_html.py
```

Regenerates the interactive GitHub Pages calendar and JSON data after report edits.

## Coding Style & Naming Conventions

Python scripts use straightforward procedural code, 4-space indentation, UTF-8 text handling, and descriptive snake_case names. Keep generated filenames stable because README links and GitHub Pages depend on them. For web assets, keep `docs/index.html` static, and treat `docs/events.json` as the separate data source. Preserve Japanese event names, venue names, and source text exactly.

## Testing Guidelines

There is no formal automated test suite. Validate changes by running the relevant generator command and checking that expected files are updated. For calendar data changes, inspect `docs/events.json` for valid JSON and open `docs/index.html` locally to confirm event dates, modal content, and PWA assets still load.

## Commit & Pull Request Guidelines

Recent commits use concise imperative messages such as `Add Kawarayamachi festival...`, `Configure docs/index.html...`, and `Decouple HTML View...`. Follow that style: describe the user-visible change and mention affected outputs when useful. Pull requests should summarize data sources changed, generated files updated, verification commands run, and include screenshots when the calendar UI changes.

## Security & Configuration Tips

Use official sources for festival data and retain source URLs in the report. Do not commit private downloads, credentials, or local-only cache files. Before publishing, verify that `docs/` contains only files intended for GitHub Pages.
