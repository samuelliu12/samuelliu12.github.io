# Portfolio — conventions

## Stack
Vanilla HTML + CSS + JS. No dependencies, no package.json. One stdlib-only Python generator (`build.py`) pre-renders the JSON data into static HTML so link previews, scrapers and crawlers see real content without running JavaScript.
Deploy by pushing to `main` on `samuelliu12.github.io`; GitHub Pages serves the root directly. Generated files are committed.

## Adding / editing projects or experience
Edit `data/projects.json` or `data/experience.json`, then run `python3 build.py` and commit the regenerated files.
Never hand-edit between the `<!-- BUILD:... -->` markers in `projects.html` / `experience.html`, or anything in `projects/`, or `project.html`, `sitemap.xml`, `robots.txt`; the next build overwrites them.
Project page chrome (head, nav, footer) lives in `templates/project.html`.
Each entry supports: `title`, `tags` (array), `description`, `image` (path or `""`), `image_position` (optional CSS `object-position`, e.g. `"left center"`, to control the crop), `detail_image` (optional; replaces `image` on the project detail page, and `image_position` is not applied to it), `links` (array of `{label, url}`; an empty `url` renders as a non-clickable "coming soon" label).
Valid tag values: `"hardware"`, `"firmware"`, `"software"`.

## File roles
- `css/style.css` — all styles, one file
- `js/main.js` — active-nav detection + filter tabs (hides/shows pre-rendered `.card-entry` elements by `data-tags`)
- `build.py` — generates card HTML, `projects/<slug>.html` detail pages, the `project.html?id=` redirect, `sitemap.xml`, `robots.txt`
- `templates/project.html` — template for project detail pages
- `data/projects.json` — single source of truth for project cards and detail pages
- `data/experience.json` — single source of truth for experience cards
- `assets/images/` — project photos and headshot

## Design tokens
Light, minimal academic style (white background, blue links, thin dividers, no cards).

| Token | Value |
|---|---|
| Background | `#ffffff` |
| Surface (tags, placeholders) | `#f7f7f7` |
| Border | `#e5e5e5` |
| Text | `#1f1f1f` |
| Muted | `#6b6b6b` |
| Accent (links) | `#1a5fb4` (blue) |
| Font | Lato (Google Fonts), all text |
| Max content width | 780px |

## Local preview
```
python3 build.py && python3 -m http.server 8080
```
Pages are static, so opening them as `file://` URLs also works.
