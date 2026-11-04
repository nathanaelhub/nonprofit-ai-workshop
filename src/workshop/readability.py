"""Flesch-Kincaid grade level, computed in code so the reading-level claim can be tested."""

from __future__ import annotations

import re


def syllables(word: str) -> int:
    w = word.lower().strip(".,;:!?")
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups) - (1 if w.endswith("e") and not w.endswith("le") and len(groups) > 1 else 0)
    return max(1, n)


def plain_text(html: str) -> str:
    """Visible text of rendered HTML, one block per line, so headings and list items count as sentences."""
    html = re.sub(r"(?s)<(script|style|aside)\b.*?</\1>", " ", html)
    html = re.sub(r"</(p|li|h[1-6]|td|th|tr|dt|dd|blockquote)>", "\n", html)
    return re.sub(r"[ \t]+", " ", re.sub(r"<[^>]+>", " ", html))


def grade(text: str) -> float | None:
    sentences = [s for s in re.split(r"[.!?]+\s|\n+", text) if re.search(r"[A-Za-z]{2}", s)]
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", text)
    if len(words) < 30 or not sentences:
        return None
    return round(0.39 * len(words) / len(sentences) + 11.8 * sum(map(syllables, words)) / len(words) - 15.59, 1)
