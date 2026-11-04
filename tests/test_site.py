import re
from pathlib import Path

from workshop.build import CONTENT, Page, pages, slides_html
from workshop.readability import grade, plain_text

MAX_GRADE = 8.0


def test_every_page_builds_with_a_title(site):
    for page in pages():
        out = site / page.out
        assert out.exists(), page.path
        assert "title" in page.meta, page.path


def test_internal_links_resolve(site):
    for html in site.rglob("*.html"):
        for ref in re.findall(r'(?:href|src)="([^"]+)"', html.read_text(encoding="utf-8")):
            if re.match(r"[a-z]+:|#|//", ref):
                continue
            target = (html.parent / ref.split("#")[0]).resolve()
            assert target.exists(), f"{html.relative_to(site)} links to missing {ref}"


def test_attendee_pages_read_at_grade_8_or_below(site):
    for page in pages():
        if page.audience != "attendee":
            continue
        g = grade(plain_text((site / page.out).read_text(encoding="utf-8")))
        assert g is not None and g <= MAX_GRADE, f"{page.path}: grade {g}"


def test_readability_tells_easy_from_hard():
    easy = "Read the report. Use only the numbers in it. Ask a friend to check your work. " * 3
    hard = ("Organizational accountability necessitates comprehensive verification of quantitative "
            "representations prior to dissemination to institutional stakeholders. ") * 3
    assert grade(easy) < 4 < 14 < grade(hard)


def test_slides_split_on_rules_and_keep_notes_out_of_the_slide():
    page = Page(Path("slides.md"), {"title": "t"}, "# One\n\nHello\nNotes:\nSay hi\n---\n## Two\n\nBye\n")
    out = slides_html(page)
    assert out.count('<section class="slide"') == 2
    assert '<aside class="notes"><p>Say hi</p></aside>' in out
    assert "Notes:" not in out


def test_relative_md_links_become_html_links(site):
    for h in site.rglob("*.html"):
        assert not re.findall(r'href="(?![a-z]+:)[^"]*\.md[#"]', h.read_text(encoding="utf-8")), h.name


def test_content_dir_exists():
    assert (CONTENT / "index.md").exists()


def test_a_wrapped_paragraph_is_one_sentence():
    one_line = "<p>" + "The volunteers at the pantry gave many hours of their time this quarter " * 3 + "today.</p>"
    wrapped = one_line.replace(" of ", "\nof ")
    assert grade(plain_text(wrapped)) == grade(plain_text(one_line))
