"""Cached copies of the sources the kit quotes, and the claims that quote them.

sources/manifest.json lists each source (title, publisher, URL, date retrieved);
sources/text/<id>.txt is the text as retrieved. sources/claims.json ties each fact
a page states to a quote in a source, and tests check both ends: the page says it,
and the source contains the quote (and doesn't contain anything marked absent).
"""

from __future__ import annotations

import json
import re
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "sources"


@cache
def manifest() -> dict:
    return json.loads((DIR / "manifest.json").read_text(encoding="utf-8"))


def claims() -> list[dict]:
    return json.loads((DIR / "claims.json").read_text(encoding="utf-8"))


def text(source: str) -> str:
    return (DIR / "text" / f"{source}.txt").read_text(encoding="utf-8")


def norm(s: str) -> str:
    """Letters, digits and $ only: pages and sources differ in dashes, hyphens, spacing and markup."""
    return re.sub(r"[^a-z0-9$]", "", s.lower())


def extract(page: str) -> str:
    """Readable text of an HTML page: the article or main element if there is one, one block per line."""
    import html as htmllib

    m = re.search(r"(?s)<article\b.*?</article>", page) or re.search(r"(?s)<main\b.*?</main>", page)
    body = m.group(0) if m else page
    body = re.sub(r"(?s)<(script|style|noscript)\b.*?</\1>", " ", body)
    body = re.sub(r"</t[dh]>", " | ", body)
    body = re.sub(r"<[^>]+>", "\n", body)
    body = re.sub(r"[ \t]+", " ", htmllib.unescape(body))
    return re.sub(r"\n\s*\n+", "\n", body).strip() + "\n"


def refresh(ids: list[str] | None = None, log=print) -> list[str]:
    """Re-download sources and overwrite their cached text. Returns the ids whose text changed.

    Run the tests afterward: a claim whose quote is gone fails, and the RUNBOOK says what to do."""
    import datetime
    import json
    import urllib.request

    m = manifest()
    changed = []
    for sid in ids or list(m):
        req = urllib.request.Request(m[sid]["url"], headers={"User-Agent": "Mozilla/5.0 (nonprofit-ai-workshop source check)"})
        with urllib.request.urlopen(req, timeout=60) as r:
            new = extract(r.read().decode("utf-8", errors="replace"))
        path = DIR / "text" / f"{sid}.txt"
        if norm(new) != norm(path.read_text(encoding="utf-8")):
            changed.append(sid)
        path.write_text(new, encoding="utf-8")
        m[sid]["retrieved"] = datetime.date.today().isoformat()
        log(f"{sid}: {'CHANGED' if sid in changed else 'same'}")
    (DIR / "manifest.json").write_text(json.dumps(m, indent=1) + "\n", encoding="utf-8")
    manifest.cache_clear()
    return changed
