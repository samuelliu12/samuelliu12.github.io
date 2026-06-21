# Portfolio — conventions

## Stack
Vanilla HTML + CSS + JS. No build step, no dependencies, no package.json.
Deploy by pushing to `main` on `samuelliu1202.github.io`; GitHub Pages serves the root directly.

## Adding / editing projects
Edit `data/projects.json` only — never touch the card HTML in `projects.html`.
Each entry supports: `title`, `tags` (array), `description`, `image` (path or `""`), `github`, `demo`, `paper`.
Valid tag values: `"hardware"`, `"firmware"`, `"software"`.

## File roles
- `css/style.css` — all styles, one file
- `js/main.js` — active-nav detection + card renderer + filter logic
- `data/projects.json` — single source of truth for project cards
- `assets/images/` — project photos and headshot

## Design tokens
| Token | Value |
|---|---|
| Background | `#0d0d0d` |
| Surface (cards) | `#161616` |
| Border | `#262626` |
| Text | `#e2e2e2` |
| Muted | `#737373` |
| Accent | `#4ade80` (green) |
| Heading font | Space Mono (Google Fonts) |
| Body font | Inter (Google Fonts) |
| Max content width | 900px |

## Local preview
```
python3 -m http.server 8080
```
`fetch()` for `projects.json` requires HTTP — opening `index.html` directly as a `file://` URL will not render cards.
