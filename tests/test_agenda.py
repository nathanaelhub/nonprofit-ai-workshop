import re

from workshop.build import CONTENT, parse


def read(path):
    return (CONTENT / path).read_text(encoding="utf-8")


def agenda():
    rows = re.findall(r"^\| (\d+)–(\d+) \| ([^|]+) \|", read("facilitator.md"), re.M)
    return [(int(a), int(b), title.strip()) for a, b, title in rows]


def test_the_hour_runs_0_to_60_without_gaps():
    rows = agenda()
    assert rows[0][0] == 0 and rows[-1][1] == 60
    for (_, end, _), (start, _, _) in zip(rows, rows[1:]):
        assert end == start


def test_exercise_minutes_agree_across_guide_handouts_and_index():
    index = read("handouts/index.md")
    for n, path in enumerate(["1-ask-well", "2-check", "3-protect", "4-when-not"], 1):
        start, end, _ = next(r for r in agenda() if r[2].startswith(f"Exercise {n}"))
        minutes = end - start
        assert f"**{minutes} minutes." in read(f"handouts/{path}.md"), path
        assert f"**Time:** {minutes} minutes" in read(f"keys/{path}.md"), path
        assert re.search(rf"\[Handout\]\({path}\.md\) \| \[Key\][^|]*\| {minutes} \|", index), path


def test_quiz_matches_its_answer_key():
    quiz = read("quiz.md")
    blocks = re.split(r"^\*\*\d\. ", quiz, flags=re.M)[1:9]
    assert len(blocks) == 8
    for block in blocks:
        assert re.findall(r"^- ([A-D])\. ", block, re.M) == ["A", "B", "C", "D"]
    key = dict(re.findall(r"^\| (\d) \| ([A-D]) \|", read("tally.md"), re.M))
    assert sorted(key) == [str(i) for i in range(1, 9)]


def test_slides_the_guide_points_to_are_the_right_ones():
    slides = parse(CONTENT / "slides.md").body.split("\n---\n")
    assert "What Claude is" in slides[3] and "What it's good at" in slides[5]
    assert "slides 4 to 6" in read("facilitator.md")
