"""Build the workshop kit into a static site.

Every page is a Markdown file in content/ with a short header:

    ---
    title: Exercise 1: Ask well
    audience: attendee        # attendee pages must read at grade 8 or below
    ---

Links between pages are written to the .md files (so they work on GitHub too) and
rewritten to .html here. content/slides.md is special: slides are separated by a
line holding only `---`, and anything after a line `Notes:` is a speaker note.
"""

from __future__ import annotations

import html
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "content"
ASSETS = ROOT / "site"

NAV = [("index.md", "Home"), ("facilitator.md", "Facilitator guide"), ("slides.md", "Slides"),
       ("handouts/index.md", "Handouts"), ("privacy.md", "Privacy sheet")]


@dataclass
class Page:
    path: Path      # relative to content/
    meta: dict
    body: str       # Markdown, header removed

    @property
    def title(self) -> str:
        return self.meta.get("title", self.path.stem)

    @property
    def audience(self) -> str:
        return self.meta.get("audience", "facilitator")

    @property
    def out(self) -> Path:
        return self.path.with_suffix(".html")


def parse(path: Path) -> Page:
    text = path.read_text(encoding="utf-8")
    meta = {}
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
        text = text[m.end():]
    return Page(path.relative_to(CONTENT), meta, text)


def pages() -> list[Page]:
    return [parse(p) for p in sorted(CONTENT.rglob("*.md"))]


def md_to_html(text: str) -> str:
    out = markdown.markdown(text, extensions=["tables", "attr_list", "sane_lists"])
    return re.sub(r'href="([^":#]+)\.md(#[^"]*)?"', lambda m: f'href="{m.group(1)}.html{m.group(2) or ""}"', out)


def slides_html(page: Page) -> str:
    parts = []
    for i, chunk in enumerate(re.split(r"\n---\n", page.body.strip()), 1):
        slide, _, notes = chunk.partition("\nNotes:")
        note = f'<aside class="notes">{md_to_html(notes.strip())}</aside>' if notes.strip() else ""
        parts.append(f'<section class="slide" id="s{i}">{md_to_html(slide.strip())}{note}</section>')
    return '<div class="deck">' + "".join(parts) + "</div>"


def render(page: Page) -> str:
    up = "../" * (len(page.path.parts) - 1)
    nav = " ".join(f'<a href="{up}{p[:-3]}.html"{" aria-current=page" if Path(p) == page.path else ""}>{label}</a>'
                   for p, label in NAV if (CONTENT / p).exists())
    is_slides = page.path == Path("slides.md")
    body = slides_html(page) if is_slides else md_to_html(page.body)
    script = f'<script src="{up}slides.js"></script>' if is_slides else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(page.title)} · Using Claude at a Nonprofit</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&display=swap">
<link rel="stylesheet" href="{up}style.css">
</head>
<body class="{'slides' if is_slides else page.audience}">
<header class="site"><a class="brand" href="{up}index.html">Using Claude at a Nonprofit</a><nav>{nav}</nav></header>
<main>
{body}
</main>
<footer class="site">A one-hour workshop kit. Not affiliated with Anthropic. MIT license.
<a href="https://github.com/nathanaelhub/nonprofit-ai-workshop">Source</a></footer>
{script}
</body>
</html>
"""


def build(out: str | Path = "_site") -> Path:
    out = Path(out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for page in pages():
        dest = out / page.out
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(render(page), encoding="utf-8")
    for asset in ASSETS.iterdir():
        shutil.copy(asset, out / asset.name)
    return out
