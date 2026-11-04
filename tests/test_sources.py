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
