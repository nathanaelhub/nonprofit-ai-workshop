import json
import re

from workshop.build import CONTENT
from workshop.sources import DIR, claims, manifest, norm, text


def test_every_claim_is_on_its_page_and_quoted_from_its_source():
    for c in claims():
        page = (CONTENT / c["page"]).read_text(encoding="utf-8")
        assert norm(c["says"]) in norm(page), f'{c["id"]}: {c["page"]} no longer says it'
        src = text(c["source"])
        assert norm(c["quote"]) in norm(src), f'{c["id"]}: quote not in {c["source"]}'
        if "absent" in c:
            assert c["absent"] not in src, f'{c["id"]}: {c["source"]} now mentions {c["absent"]}'


def test_every_source_is_listed_with_a_url_and_date():
    m = manifest()
    for c in claims():
        e = m[c["source"]]
        assert e["url"].startswith("https://") and re.fullmatch(r"\d{4}-\d{2}-\d{2}", e["retrieved"])


def test_every_email_sender_is_fictional_and_uses_example_org():
    fictional = json.loads((DIR / "fictional.json").read_text(encoding="utf-8"))
    all_text = "\n".join(p.read_text(encoding="utf-8") for p in CONTENT.rglob("*.md"))
    senders = re.findall(r"\*\*From:\*\* ([^&<]+?) &lt;", all_text)
    assert senders, "found no email senders; the pattern is broken"
    assert set(senders) <= set(fictional["people"])
    for addr in re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", all_text):
        assert addr.endswith("@example.org"), addr
    for name in fictional["people"] + fictional["organizations"]:
        assert name in all_text, f"{name} is listed as fictional but not used"


def test_every_quote_on_the_privacy_sheet_is_in_a_cached_source():
    page = (CONTENT / "privacy.md").read_text(encoding="utf-8")
    section = page.split("## What Anthropic says", 1)[1].split("\n## ", 1)[0]
    section = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", section))
    sources = [norm(text(s)) for s in manifest()]
    quotes = re.findall(r'"([^"]{20,})"', section)
    assert len(quotes) >= 6, "found too few quotes; the pattern is broken"
    for q in quotes:
        for part in q.split("..."):
            if part.strip():
                assert any(norm(part) in s for s in sources), part


def test_extract_keeps_table_rows_and_drops_scripts():
    from workshop.sources import extract
    page = "<html><script>x=1</script><main><h2>Limits</h2><table><tr><td>4</td><td>$3,575</td></tr></table></main></html>"
    out = extract(page)
    assert "x=1" not in out and norm("4 | $3,575") in norm(out)


def test_dates_the_pages_say_sources_were_checked_match_the_manifest():
    import datetime
    retrieved = {e["retrieved"] for e in manifest().values()}
    found = 0
    for p in CONTENT.rglob("*.md"):
        t = p.read_text(encoding="utf-8").replace("*", "")
        for d in re.findall(r"checked (?:on )?(\d{4}-\d{2}-\d{2})", t):
            found += 1
            assert d in retrieved, f"{p.name} says checked {d}"
        for d in re.findall(r"checked (?:on )?([A-Z][a-z]+ \d{1,2}, \d{4})", t):
            found += 1
            assert datetime.datetime.strptime(d, "%B %d, %Y").date().isoformat() in retrieved, f"{p.name} says checked {d}"
    assert found >= 3
