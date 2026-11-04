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
