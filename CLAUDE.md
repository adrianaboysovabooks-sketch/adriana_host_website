# Adriana Boysová — author website

Static rebuild of Adriana's Wix author site (adrianaboysova.eu). Plain HTML/CSS/JS, no framework, served by GitHub Pages from the repo root.

Read `README.md` (what each file does) and `HANDOVER.md` (preview, publishing, launch steps) before changing anything. Background notes are in `notes/`.

## Rules

- Faithful rebuild, not a redesign. Keep the existing look, layout and page order unless Adriana asks for a change.
- Keep the Slovak copy and diacritics exactly as supplied. Don't rewrite or translate text unless asked.
- Interior pages are generated. Edit `content/pages.json` (copy) or `content/links.json` (links), then run `python3 scripts/build_pages.py`. Edit `index.html` directly for the homepage. All styling lives in `assets/styles.css`.
- Keep local paths relative so the site works both at `*.github.io/<repo>/` and at a custom domain.
- The pages carry `noindex` and `robots.txt` blocks crawlers until launch. Don't change that, the domain/DNS or anything on Wix without Adriana's explicit go-ahead.

## Preview and checks

```sh
python3 -m http.server 8876 --bind 127.0.0.1   # then open http://127.0.0.1:8876/
python3 scripts/check_assets.py
python3 scripts/check_structure.py
```
