from workshop.build import CONTENT
from workshop.check import EMAIL_1, GOOD_REQUEST, PROMPTS, REPORT, numbers, score
from workshop.sources import norm


def page(path):
    return norm((CONTENT / path).read_text(encoding="utf-8"))


def test_check_prompts_are_the_ones_on_the_handouts():
    assert norm(PROMPTS["1-vague"]) in page("handouts/1-ask-well.md")
    for line in REPORT.splitlines()[1:]:
        assert norm(line) in page("handouts/1-ask-well.md"), line
    assert norm(PROMPTS["2-snap"]) in page("handouts/2-check.md")
    assert norm(EMAIL_1) in page("handouts/3-protect.md")
    assert norm(GOOD_REQUEST) in page("keys/3-protect.md")


def test_numbers_ignore_list_markers_and_commas():
    assert numbers("1. We served 1,284 households\n2. and 3,912 people") == {"1284", "3912"}


def test_scores():
    s = score("1-context", "We served 1,284 households and over 4,000 people, about 41 hours each.")
    assert s["numbers_not_in_report"] == ["41", "4000"]
    s = score("2-snap", "For FY 2026 the limit was $3,483 a month; confirm with the USDA.")
    assert s == {"dollar_figures": [3483], "gives_current_limit": False, "hedges": True, "names_a_year": True,
                 "points_to_official_source": True}
    s = score("1-vague", "We served [X] families, e.g. [a 20% increase], with 47 volunteers.")
    assert s["numbers_not_in_report"] == [] and s["example_numbers_in_placeholders"] == ["20"]
    s = score("3-pasted", "Dear Marisol, we're sorry Ana's asthma ...")
    assert s["private_details_repeated"] == ["Marisol", "Ana", "asthma"]


def test_private_details_match_whole_words_only():
    assert score("3-pasted", "Please send an analysis of Leonard's bill.")["private_details_repeated"] == []


def test_claude_output_quoted_in_the_keys_is_in_the_saved_run():
    import json
    from workshop.check import RESULTS
    answers = norm(" ".join(json.loads(line)["answer"]
                            for line in (RESULTS / "2026-11-03" / "answers.jsonl").read_text(encoding="utf-8").splitlines()))
    quoted = {
        "keys/1-ask-well.md": ["[measurable outcome, e.g., a 20% increase in households served]",
                               "for families who cannot visit during the week"],
        "keys/2-check.md": ["$3,483", "about $3,575"],
    }
    for path, quotes in quoted.items():
        for q in quotes:
            assert norm(q) in page(path) and norm(q) in answers, q


def test_check_uses_the_snap_figure_the_answer_key_cites():
    from workshop.check import SNAP_LIMIT_4
    from workshop.sources import claims
    says = next(c["says"] for c in claims() if c["id"] == "snap-gross-limit-4")
    assert says == f"${SNAP_LIMIT_4:,}"


def test_spanish_check_prompts_are_the_ones_on_the_spanish_handouts():
    from workshop.check import EMAIL_1_ES, REPORT_ES
    assert norm(PROMPTS["1-vague-es"]) in page("es/handouts/1-ask-well.md")
    for line in REPORT_ES.splitlines()[1:]:
        assert norm(line) in page("es/handouts/1-ask-well.md"), line
    assert norm(PROMPTS["2-snap-es"]) in page("es/handouts/2-check.md")
    assert norm(EMAIL_1_ES) in page("es/handouts/3-protect.md")
    s = score("3-pasted-es", "Hola Marisol, sentimos lo del asma de Ana.")
    assert s["private_details_repeated"] == ["Marisol", "Ana", "asma"]


def test_hedging_is_recognized_in_the_wording_claude_used():
    for text in ["I believe it's around $3,575, but check that against the current USDA table.",
                 "about $3,575/month. Please verify this figure, since I'm less sure of it.",
                 "calculo que rondan los $3,575 al mes, pero no estoy seguro de esa cifra.",
                 "about $3,483 ... Check the USDA or your state agency for the current number."]:
        assert score("2-snap", text)["hedges"], text
    assert not score("2-snap", "The limit is $3,575 a month for a household of four.")["hedges"]
