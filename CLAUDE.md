# Portfolio — conventions

## Stack
Vanilla HTML + CSS + JS. No build step, no dependencies, no package.json.
Deploy by pushing to `main` on `samuelliu12.github.io`; GitHub Pages serves the root directly.

## Adding / editing projects
Edit `data/projects.json` only — never touch the card HTML in `projects.html`.
Each entry supports: `title`, `tags` (array), `description`, `image` (path or `""`), `image_position` (optional CSS `object-position`, e.g. `"left center"`, to control the crop), `detail_image` (optional; replaces `image` on the project detail page, and `image_position` is not applied to it), `links` (array of `{label, url}`; an empty `url` renders as a non-clickable "coming soon" label).
Valid tag values: `"hardware"`, `"firmware"`, `"software"`.

## File roles
- `css/style.css` — all styles, one file
- `js/main.js` — active-nav detection + card renderer + filter logic
- `data/projects.json` — single source of truth for project cards
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
python3 -m http.server 8080
```
`fetch()` for `projects.json` requires HTTP — opening `index.html` directly as a `file://` URL will not render cards.
