# Using Claude at a Nonprofit: a one-hour workshop

A ready-to-run, one-hour workshop that teaches nonprofit staff who don't write code to use Claude
carefully: how to ask well, how to check an answer before using it, what never to paste in, and
when not to use it at all.

**Live site:** https://nathanaelhub.github.io/nonprofit-ai-workshop/

**Status:** complete, and **not yet run with real staff.** The quiz and feedback form are how a
first run will produce evidence; results will go in `pilots/`.

Not affiliated with Anthropic.

## What's in it

| For the facilitator | For attendees |
|---|---|
| [Facilitator guide](content/facilitator.md): the hour minute by minute, prep, what to do when things go wrong | Four [handouts](content/handouts/index.md), each 9 to 12 minutes, in pairs |
| [Slides](content/slides.md) with speaker notes | A one-page [privacy sheet](content/privacy.md) |
| Four [answer keys](content/keys/) | A [quiz](content/quiz.md), before and after |
| [Quiz answers and tally sheet](content/tally.md) | A one-page [takeaway](content/takeaway.md) and a [feedback form](content/feedback.md) |

The four exercises:

1. **Ask well.** A grant-report paragraph from a (fictional) food pantry's report, asked for
   vaguely and then with context. Pairs circle every number and find it in the report.
2. **Check before using.** "What's the SNAP income limit for a family of four?" Then the official
   USDA table. Then a real conflict: a news story says Tennessee raised its limit to 200% of poverty;
   the USDA's own list of states using that rule doesn't include Tennessee.
3. **Protect clients.** Three fictional intake emails full of private details. Pairs find every
   detail, then write a request with none of them.
4. **When not to use it.** Ten task cards sorted into "good use", "use with a check" and "don't
   use", from a volunteer thank-you note to a reply to someone in crisis.

The design and its reasons are in the [spec](docs/spec.md). To find a group to host it: a
one-page [host flyer](content/host.md) and an [outreach email](docs/outreach-email.md).

## How it stays accurate

| What | How it's checked (`uv run pytest`) |
|---|---|
| What Anthropic says it does with chats | Quoted from Anthropic's Privacy Center; every quoted passage must be in a cached copy of its page, and the date the sheet says it was checked must match the cache |
| The SNAP figure and the Tennessee conflict | Each fact is tied to a quote in a cached USDA or news source; "Tennessee isn't on the USDA list" is tested as an absence |
| Reading level | Attendee pages must read at grade 8 or below (Flesch–Kincaid, in code; cross-checked against the textstat library). They currently read at grade 2.6 to 5.8 |
| Timings | The hour adds up to 60 minutes, and each exercise's time agrees across the guide, handout, key and index |
| Fictional people | Every email sender is on a list of made-up names, and every address uses `example.org` |
| What Claude does with the exercises | `workshop check` (below); Claude output quoted in the answer keys must be in a saved run |

`workshop refresh-sources` re-downloads every cached source, so a policy page or USDA table that
changes makes a test fail instead of leaving the kit quietly out of date.

## What Claude actually does with the exercises

Models change, so before each workshop `workshop check` sends every exercise prompt to Claude
three times and scores the answers in code. The first run (November 3, 2026, Claude Sonnet, $0.10,
[summary](checks/results/2026-11-03/summary.md)):

- **The vague request didn't produce made-up numbers.** All three answers were paragraphs full
  of blanks like "[X] households" and example values like "a 20% increase," plus a request for real
  details. I had predicted invented numbers; the spec said so. The keys now say what happened, and
  the risk the exercise teaches moves to the person filling in the blanks.
- **The request with context used only the report's numbers,** 3 of 3. One added a reason the
  report doesn't give.
- **On SNAP, Claude was careful:** every answer gave last year's limit ($3,483) labeled as such,
  two called the current $3,575 an estimate, one declined to give a new figure, and all three said
  to check the USDA or the state agency. Pairs still end up with two numbers and only the source
  settles it.
- **Pasting the client's email** got a warmer, more personal reply, using her name and her
  child's, 3 of 3. The de-identified request got a usable template with no private details, 3 of 3.
  That trade is the discussion in Exercise 3.

The first scoring counted the "20%" inside a placeholder as an invented number. Reading the
answers caught it; the RUNBOOK says to read them every time.

These runs use the `claude` CLI with no tools and a plain system prompt. claude.ai has its own
settings and may search the web, so attendees can see different answers.

## Run

```bash
uv sync
uv run pytest                                # all the checks above, offline
uv run workshop build                        # -> _site/, open _site/index.html
uv run workshop refresh-sources              # re-download cached sources, then run pytest
WORKSHOP_USE_LOGIN=1 uv run workshop check   # run the exercises through Claude (~$0.10)
```

Pages are Markdown in `content/`; GitHub Pages rebuilds the site from `main` once the tests pass.
Keeping it current (SNAP figures every October 1, privacy pages, adding pilot results) is in the
[RUNBOOK](RUNBOOK.md).

## Stack

- Markdown content built to a static site by a small Python script (`markdown` package); print
  styles for letter paper; slides in a few lines of JavaScript. Hosted on GitHub Pages.
- Python 3.11+, uv, pytest; CI on 3.11 to 3.14; `main` protected, changes by pull request.

## Layout

```
content/                pages: guide, slides, handouts, keys, privacy, quiz, tally, feedback, takeaway
sources/                cached source texts, the claims that quote them, the fictional names list
checks/results/         saved runs of the exercises against Claude
src/workshop/build.py   Markdown -> site
src/workshop/check.py   run and score the exercises against Claude
src/workshop/sources.py cached sources and refresh
docs/spec.md            the approved design
```

## Limits

- Not run with real staff yet; nothing here shows it changes behavior.
- English only, US-focused (SNAP, 988).
- The privacy sheet quotes Anthropic's policies; it isn't legal advice and doesn't replace an
  organization's own policy.

MIT license.
