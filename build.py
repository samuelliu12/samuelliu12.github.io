#!/usr/bin/env python3
"""Pre-render project and experience entries from data/*.json into static HTML.

Run after editing data/projects.json or data/experience.json:

    python3 build.py

It rewrites the regions between BUILD markers in projects.html and
experience.html, regenerates projects/<slug>.html from templates/project.html,
and regenerates project.html (redirect for old ?id= links), sitemap.xml and
robots.txt. Standard library only. Running it twice produces no changes.
"""

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://" + (ROOT / "CNAME").read_text().strip()


def esc(value):
    return escape(str(value), quote=True)


def slugify(title):
    # Must match the slugs old project.html?id= links used.
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def asset(path, prefix):
    """Relative asset path as seen from a page `prefix` levels down."""
    if not path or re.match(r"^[a-z]+:", path) or path.startswith("/"):
        return path
    return prefix + path


def write_if_changed(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))
    return True


def replace_region(path, name, inner):
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"(<!-- BUILD:%s -->).*?(\n[ \t]*<!-- /BUILD:%s -->)" % (name, name), re.S
    )
    if not pattern.search(text):
        raise SystemExit(f"{path.name}: missing <!-- BUILD:{name} --> markers")
    new = pattern.sub(lambda m: m.group(1) + inner + m.group(2), text, count=1)
    write_if_changed(path, new)


def tags_html(tags):
    return "".join(f'<span class="tag tag-{esc(t)}">{esc(t)}</span>' for t in tags)


def indent(block, spaces):
    pad = " " * spaces
    return "\n".join(pad + line if line.strip() else "" for line in block.split("\n"))


# ---------- projects.html ----------

def project_card(p):
    slug = slugify(p["title"])
    if p.get("image"):
        pos = f' style="object-position: {esc(p["image_position"])}"' if p.get("image_position") else ""
        media = f'<img src="{esc(p["image"])}" alt="{esc(p["title"])}" class="card-img" loading="lazy"{pos}>'
    else:
        media = '<div class="card-img-placeholder">No image</div>'
    links = "".join(
        f'<a href="{esc(l["url"])}" class="card-link" target="_blank" rel="noopener" onclick="event.stopPropagation()">{esc(l["label"])} ↗</a>'
        if l.get("url")
        else f'<span class="card-link card-link-pending">{esc(l["label"])} · coming soon</span>'
        for l in p.get("links", [])
    )
    return f"""<div class="card-entry" data-tags="{esc(",".join(p["tags"]))}">
  <a href="projects/{slug}.html" class="card-link-wrapper">
    <article class="card">
      {media}
      <div class="card-body">
        <div class="card-tags">{tags_html(p["tags"])}</div>
        <h2 class="card-title">{esc(p["title"])}</h2>
        <p class="card-desc">{esc(p["description"])}</p>
        <div class="card-links">{links}</div>
      </div>
    </article>
  </a>
</div>"""


def experience_card(e):
    media = (
        f'<img src="{esc(e["image"])}" alt="{esc(e["title"])}" class="card-img" loading="lazy">'
        if e.get("image") else ""
    )
    links = "".join(
        f'<a href="{esc(l["url"])}" class="card-link" target="_blank" rel="noopener">{esc(l["label"])} ↗</a>'
        if l.get("url")
        else f'<span class="card-link card-link-pending">{esc(l["label"])} · coming soon</span>'
        for l in e.get("links", [])
    )
    highlights = [h for h in e.get("highlights", []) if h]
    bullets = (
        '\n      <ul class="card-bullets">' + "".join(f"<li>{esc(h)}</li>" for h in highlights) + "</ul>"
        if highlights else ""
    )
    media_line = f"\n    {media}" if media else ""
    return f"""<div class="card-entry" data-tags="{esc(",".join(e["tags"]))}">
  <article class="card">{media_line}
    <div class="card-body">
      <div class="card-tags">{tags_html(e["tags"])}</div>
      <h2 class="card-title">{esc(e["title"])}</h2>
      <p class="card-meta">{esc(e["company"])}</p>
      <p class="card-dates">{esc(e["dates"])}</p>
      <p class="card-desc">{esc(e["description"])}</p>{bullets}
      <div class="card-links">{links}</div>
    </div>
  </article>
</div>"""


def grid(cards, label):
    body = "\n".join(cards)
    body += f'\n<p class="empty-state" data-label="{label}" hidden></p>'
    return "\n" + indent(body, 6)


# ---------- projects/<slug>.html ----------

def section(label, inner):
    return f"""<div class="detail-section">
  <h2 class="section-label">{label}</h2>
  {inner}
</div>"""


def bullet_section(label, items):
    items = [i for i in items or [] if i]
    if not items:
        return ""
    lis = "\n".join(f"    <li>{esc(i)}</li>" for i in items)
    return section(label, f'<ul class="detail-bullets">\n{lis}\n  </ul>')


def project_page(p, template):
    slug = slugify(p["title"])
    url = f"{SITE}/projects/{slug}.html"

    hero_src = p.get("detail_image") or p.get("image")
    pos = (
        f' style="object-position: {esc(p["image_position"])}"'
        if p.get("image_position") and not p.get("detail_image") else ""
    )
    hero = f'<img src="{esc(asset(hero_src, "../"))}" alt="{esc(p["title"])}" class="detail-hero"{pos}>' if hero_src else ""

    parts = [
        f'<p class="breadcrumb"><a href="../projects.html">Projects</a> / {esc(p["title"])}</p>',
        hero,
        f"""<div class="detail-header">
  <h1 class="detail-title">{esc(p["title"])}</h1>
  <div class="detail-meta">
    <div class="card-tags">{tags_html(p["tags"])}</div>
  </div>
</div>""",
    ]
    if p.get("summary"):
        parts.append(section("Summary", f'<p class="detail-text">{esc(p["summary"])}</p>'))
    parts.append(bullet_section("What I did", p.get("what_i_did")))
    if p.get("results"):
        parts.append(bullet_section("Results", p["results"]))
    else:
        parts.append(bullet_section("Future steps", p.get("future_steps")))

    gallery = [src for src in p.get("images", []) if src]
    if gallery:
        imgs = "\n".join(f'    <img src="{esc(asset(s, "../"))}" alt="" loading="lazy">' for s in gallery)
        parts.append(section("Images", f'<div class="detail-gallery">\n{imgs}\n  </div>'))

    if p.get("skills"):
        chips = "\n".join(f'    <span class="detail-skill-chip">{esc(s)}</span>' for s in p["skills"])
        parts.append(section("Skills", f'<div class="detail-skills">\n{chips}\n  </div>'))

    links = p.get("links", [])
    if links:
        lis = "\n".join(
            f'    <li><span>{esc(l["label"])}</span><a href="{esc(l["url"])}" target="_blank" rel="noopener">'
            f'{esc(re.sub(r"^https?://(www\.)?", "", l["url"]))} ↗</a></li>'
            if l.get("url")
            else f'    <li><span>{esc(l["label"])}</span><em class="card-link-pending">coming soon</em></li>'
            for l in links
        )
        parts.append(section("Links", f'<ul class="contact-list detail-links">\n{lis}\n  </ul>'))

    parts.append('<div class="detail-back">\n  <a href="../projects.html">← All projects</a>\n</div>')
    content = indent("\n".join(x for x in parts if x), 6)

    if hero_src:
        og_image = (
            f'<meta property="og:image" content="{esc(SITE + "/" + hero_src.lstrip("/"))}">\n'
            f'  <meta property="og:image:alt" content="{esc(p["title"])}">\n'
            '  <meta name="twitter:card" content="summary_large_image">'
        )
    else:
        og_image = '<meta name="twitter:card" content="summary">'

    html = template
    for key, value in {
        "title": esc(p["title"]),
        "description": esc(p["description"]),
        "url": esc(url),
        "og_image": og_image,
        "content": content,
    }.items():
        html = html.replace("{{" + key + "}}", value)
    return html


# ---------- project.html (redirect for old ?id= links) ----------

def redirect_page(slugs):
    return f"""<!DOCTYPE html>
<html lang="en">
<!-- Generated by build.py. Redirects old project.html?id=<slug> links to projects/<slug>.html. -->
<head>
  <meta charset="UTF-8">
  <title>Project — Samuel Liu</title>
  <meta name="robots" content="noindex">
  <script>
    (function () {{
      var slugs = {json.dumps(slugs)};
      var id = new URLSearchParams(location.search).get('id');
      location.replace(slugs.indexOf(id) !== -1 ? 'projects/' + id + '.html' : 'projects.html');
    }})();
  </script>
</head>
<body>
  <p><a href="projects.html">View all projects</a></p>
</body>
</html>
"""


def main():
    projects = json.loads((ROOT / "data/projects.json").read_text(encoding="utf-8"))
    experience = json.loads((ROOT / "data/experience.json").read_text(encoding="utf-8"))

    slugs = [slugify(p["title"]) for p in projects]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    if dupes:
        raise SystemExit(f"duplicate project slugs: {', '.join(sorted(dupes))}")

    replace_region(ROOT / "projects.html", "projects", grid(map(project_card, projects), "projects"))
    replace_region(ROOT / "experience.html", "experience", grid(map(experience_card, experience), "experience"))

    template = (ROOT / "templates/project.html").read_text(encoding="utf-8")
    out_dir = ROOT / "projects"
    for p, slug in zip(projects, slugs):
        write_if_changed(out_dir / f"{slug}.html", project_page(p, template))
    for stale in out_dir.glob("*.html"):
        if stale.stem not in slugs:
            stale.unlink()
            print("removed", stale.relative_to(ROOT))

    write_if_changed(ROOT / "project.html", redirect_page(slugs))

    urls = [f"{SITE}/", f"{SITE}/about.html", f"{SITE}/projects.html", f"{SITE}/experience.html"]
    urls += [f"{SITE}/projects/{s}.html" for s in slugs]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "".join(f"  <url><loc>{esc(u)}</loc></url>\n" for u in urls)
    sitemap += "</urlset>\n"
    write_if_changed(ROOT / "sitemap.xml", sitemap)
    write_if_changed(ROOT / "robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")


if __name__ == "__main__":
    main()
