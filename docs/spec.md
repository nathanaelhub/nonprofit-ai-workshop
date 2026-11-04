# Spec: Using Claude at a Nonprofit, a one-hour workshop

Status: proposed, 2026-11-03. Approve by merging this pull request; nothing else gets built first.

## Why

Small nonprofits are adopting AI tools without training. Staff paste client emails into chat
windows, copy numbers from answers into grant reports, and either trust everything or nothing.
A one-hour session, run by someone who isn't a technologist, can change four habits that matter
most. The kit is also the "explain technical work to non-technical people" and "hand it off"
piece of the Claude Corps portfolio, and it reuses what the other projects found: Claude's
numbers need checking against a source (tn-benefits-screener), and a check by code catches
made-up facts but not misplaced ones (nashville-council-digest).

## Who it's for

- **Attendees:** nonprofit staff who use email and documents daily but don't code: program
  coordinators, development staff, front-desk and intake workers, volunteers. 4 to 20 people.
- **Facilitator:** anyone comfortable in front of a group who has used Claude a few times. The
  kit must work without me in the room, so everything a facilitator says or needs is written down.

## Goals: by the end, attendees can

1. **Ask well:** give Claude the context, the audience and the facts it should use.
2. **Check before using:** find the source for a number or claim in an answer, and spot one that
   isn't supported.
3. **Protect clients:** say what never goes into Claude (names, dates of birth, case details,
   anything identifying), and rewrite a request so Claude can help without it.
4. **Know when not to use it:** decisions about a person's eligibility, safety or legal standing,
   crisis responses, and anything they couldn't check.

## Non-goals

- Not a prompt-engineering course, and no coding or API use.
- Not a legal or compliance policy. The privacy sheet points staff to their own organization's
  policy and to Anthropic's published terms; it doesn't replace either.
- Not a comparison of AI products.
- English only in this version.

## Anti-goals (failure even if it "works")

- Hype, or leaving people more trusting of answers than when they came in.
- Any exercise that has attendees paste real client information, even "just to see".
- Any statement about how Anthropic stores or uses data that isn't quoted from Anthropic's own
  pages, with the page and the date it was checked.
- Exercises whose point depends on Claude making a mistake on cue. If Claude gets it right, the
  lesson still holds: you checked, and now you know.

## The hour

| Min | Block | Materials |
|---|---|---|
| 0–5 | Welcome, why we're here, pre-quiz (3 min) | slides, quiz |
| 5–12 | What Claude is and isn't: it predicts text, it can be confidently wrong, it doesn't know your clients or this month's rules | slides |
| 12–24 | **Exercise 1, Ask well:** draft a grant-report paragraph from a short program report, first with a vague request, then with context and facts | handout 1 |
| 24–36 | **Exercise 2, Check before using:** ask Claude the SNAP income limit for a family of four, then look it up in the official source | handout 2 |
| 36–46 | **Exercise 3, Protect clients:** three made-up intake emails full of personal details; rewrite the request so Claude can draft a reply without any of them | handout 3 |
| 46–55 | **Exercise 4, When not to use it:** sort ten task cards into "good use", "use with a check", "don't use" and discuss the hard ones | cards |
| 55–60 | Post-quiz, one-page takeaway, feedback | quiz, takeaway, feedback form |

Attendees work in pairs on one laptop, so the session works with a few devices. Each exercise has a
paper fallback (printed sample outputs) if the internet or Claude is unavailable.

### Exercise details

- **1, Ask well.** A fictional food pantry's one-page quarterly report (households served,
  pounds distributed, volunteer hours). Pairs ask for "a paragraph for our grant report", then ask
  again with audience, length and "use only the numbers in this report". They compare the two and
  circle any number not in the report. Teaching point: context in, fewer surprises out; and still
  check every number.
- **2, Check before using.** The real federal SNAP gross income limit changed on October 1, 2026
  ($3,575 a month for four, 130% of poverty). Claude may give an older figure, or the current one.
  Pairs then find the figure in the USDA source on the handout. Then the twist found while building
  the benefits screener: guides say Tennessee uses a higher limit, and no official state document
  confirms it. Teaching point: check the source; when sources disagree, call the agency or 211.
- **3, Protect clients.** Three intake emails, clearly marked fictional, with names, birthdays,
  diagnoses and addresses. Pairs highlight every identifying detail, then write a request for a
  reply template that contains none of them. Teaching point: Claude can help with the shape of the
  work without the person's details.
- **4, When not to use it.** Ten cards, e.g. "thank-you note to a volunteer" (good use),
  "translate a lease notice for a client" (use with a check by a qualified person), "decide whether
  this family qualifies for help" (don't), "reply to someone who says they're in crisis" (don't).
  The facilitator guide gives the reasoning for each card and the questions that come up.

## Deliverables

All published as a GitHub Pages site and printable on letter paper:

- **Facilitator guide:** the agenda, what to say in each block, timings, what to do when things go
  wrong, and answer keys.
- **Slides:** about 15, readable from the back of a room, with speaker notes.
- **Four handouts and the card set,** each with a facilitator answer key.
- **Privacy sheet (one page):** what never goes in, how to remove identifying details, and what
  Anthropic says it does with chats on each kind of plan, quoted and dated, with links.
- **Pre/post quiz** (the same 8 questions), a tally sheet, and a feedback form.
- **One-page takeaway** for attendees.
- **RUNBOOK:** preparing a week before, the day of, after, and the yearly update (SNAP figures
  each October 1; Anthropic's policy pages whenever the check below fails).

## Keeping it accurate (tests, `uv run pytest`)

- The agenda adds up to 60 minutes and every block's materials exist.
- Every exercise has a handout, facilitator notes and an answer key.
- Attendee-facing pages read at grade 8 or below (Flesch–Kincaid, computed in code).
- Every factual claim on the privacy sheet and in Exercise 2 carries a source URL and a retrieved
  date, and its quoted text is found in a cached copy of that source (the same rule as the council
  digest's zoning glossary). Re-fetching the sources is a separate command; if a quote disappears,
  the test fails and the RUNBOOK says what to do.
- Internal links resolve.
- Every person's name in the exercises is on the list of fictional names, so no real person
  ends up in the materials.

## Re-checking the exercises against Claude (`workshop check`)

Models change, so before each workshop the facilitator, or I, run each exercise's prompts through
the `claude` CLI three times and save the transcripts. Code then records what happened: the SNAP
figure Claude gave against the official one, any number in an Exercise 1 draft that isn't in the
report, and whether a reply to an un-redacted Exercise 3 email repeats personal details. The
facilitator guide shows real outputs from a dated run, so the facilitator knows what to expect.
Cost: a few dollars per run on a Claude login.

## Evidence, and what's not known yet

- The kit hasn't been run with real staff. The README will say so until it has. The pre/post quiz
  and feedback form are how a first run produces evidence; results get added to the repo,
  anonymized.
- Open: a group to pilot it with (a church, a campus group, a local nonprofit). That's for you to
  find; the kit is built either way.

## Stack (my call)

- Content is written in Markdown (`content/`), built into a static site with print styles by a
  small Python script using the `markdown` package. GitHub Pages deploys it after the tests pass.
- Slides are one Markdown file split into slides, shown with a few lines of JavaScript (arrow
  keys, speaker notes on a second screen), no framework.
- Python 3.11+, uv, pytest; CI on 3.11–3.14. The changes reach `main` through pull requests.
