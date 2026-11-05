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
    html = re.sub(r"\s+", " ", html)  # line breaks inside a paragraph aren't sentence ends
    html = re.sub(r"</(p|li|h[1-6]|td|th|tr|dt|dd|blockquote)>", "\n", html)
    return re.sub(r"[ \t]+", " ", re.sub(r"<[^>]+>", " ", html))


def grade(text: str) -> float | None:
    sentences = [s for s in re.split(r"[.!?]+\s|\n+", text) if re.search(r"[A-Za-z]{2}", s)]
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", text)
    if len(words) < 30 or not sentences:
        return None
    return round(0.39 * len(words) / len(sentences) + 11.8 * sum(map(syllables, words)) / len(words) - 15.59, 1)


# Spanish: the Szigriszt-Pazos perspicuity index, read on the INFLESZ scale
# (above 80 very easy, 65-80 fairly easy, 55-65 normal, 40-55 somewhat hard, below 40 very hard).
_STRONG = set("aeoáéó")
_ACCENTED_WEAK = set("íú")


def silabas(word: str) -> int:
    """Approximate Spanish syllables: vowel groups, split where two strong vowels meet (hiatus)
    or an accented i/u sits next to another vowel. A final y after a vowel is a vowel sound."""
    w = word.lower()
    groups = re.findall(r"[aeiouáéíóúü]+", w)
    n = len(groups)
    for g in groups:
        for a, b in zip(g, g[1:]):
            if (a in _STRONG and b in _STRONG) or a in _ACCENTED_WEAK or b in _ACCENTED_WEAK:
                n += 1
    return max(1, n)


def inflesz(text: str) -> float | None:
    sentences = [s for s in re.split(r"[.!?¡¿]+\s|\n+", text) if re.search(r"[A-Za-zÁÉÍÓÚáéíóúÑñ]{2}", s)]
    words = re.findall(r"[A-Za-zÁÉÍÓÚÜáéíóúüÑñ][A-Za-zÁÉÍÓÚÜáéíóúüÑñ'-]*", text)
    if len(words) < 30 or not sentences:
        return None
    return round(206.835 - 62.3 * sum(map(silabas, words)) / len(words) - len(words) / len(sentences), 1)
