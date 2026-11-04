# RUNBOOK

How to keep this kit accurate, and what to do when something changes. Written for whoever
maintains it next; you need a terminal, [uv](https://docs.astral.sh/uv/), and for the Claude
check, the `claude` CLI signed in to a Claude account.

```bash
uv sync
uv run pytest     # everything below ends with this passing
```

## Before each workshop (15 minutes, about $0.10)

1. `uv run workshop refresh-sources`, then `uv run pytest`. If a test fails, a source changed;
   see the sections below before the workshop.
2. `WORKSHOP_USE_LOGIN=1 uv run workshop check`. It runs each exercise prompt through Claude three
   times and writes `checks/results/<today>/summary.md`. **Read the answers in `answers.jsonl`,
   not just the summary.** The first run's scoring was wrong until the answers were read.
3. If Claude's behavior changed (for example, it now invents numbers in Exercise 1, or gives the
   SNAP figure confidently), update "What usually happens" in the answer keys and the link to the
   new run. The tests check that Claude output quoted in a key is in the saved run, so update the
   test's run date and quotes too (`tests/test_check.py`).
4. Give the facilitator the guide's print list and the summary.

## Every October 1: the SNAP figure

The USDA publishes new SNAP income limits for each fiscal year, effective October 1.

1. `uv run workshop refresh-sources fns_snap_standards_fy27`, then `uv run pytest`.
   `snap-gross-limit-4` fails when the table changes.
2. Read the new "Gross Monthly Income Limit" table on the
   [USDA page](https://www.fns.usda.gov/snap/allotment/cola). If the page moved, find the new
   one and update its `url` in `sources/manifest.json` (rename the id if you like, and update
   `sources/claims.json` to match).
3. Update, together:
   - `content/keys/2-check.md`: the figure, the printed table row, the dates and fiscal year.
   - `sources/claims.json`: the `says` and `quote` of `snap-gross-limit-4` and `snap-fy27-dates`.
   - `src/workshop/check.py`: `SNAP_LIMIT_4` (a test keeps it equal to the claim).
4. `uv run pytest`, then run the check (above) so the key describes the new year.

## When an Anthropic privacy page changes

`refresh-sources` re-downloads Anthropic's Privacy Center pages. If a claim from
`privacy.md` fails:

1. Read the current page. Find what it says now about the same thing.
2. If the meaning is the same and only the wording changed, update the quote in
   `content/privacy.md` and in `sources/claims.json`.
3. If the meaning changed, rewrite that part of the sheet in plain words, quoting the new text.
   Don't paraphrase a policy without a quote; the tests require every quoted passage on the sheet
   to be in a cached source.
4. The sheet says the date it was checked. A test requires that date to match a retrieved date
   in `sources/manifest.json`, so update the sentence ("checked on ...") too.

If a page is gone entirely, take that bullet off the sheet rather than keep an unsourced claim.

## When the Tennessee question is answered

Exercise 2 presents Tennessee's SNAP limit as unresolved: a June 2026 news story says the state
moved to 200% of poverty, and the USDA's BBCE chart doesn't list Tennessee. The claim
`tn-not-in-usda-bbce-list` fails when the USDA chart starts mentioning Tennessee.

When an official source settles it (TDHS policy, or the USDA chart), keep the exercise. Rewrite
step 3 as a story ("in 2026, these two sources disagreed; here's how it was settled") or replace
it with a current conflict. The lesson is the habit, not this particular case.

## After a workshop: adding results

1. Make a file `pilots/<date>-<kind of organization>.md`, for example
   `pilots/2027-02-10-food-pantry.md`. **No names of people or the organization** unless it has
   agreed in writing.
2. Include: number of attendees, the tally sheet (right before and after for each question, Q9
   average), a summary of the feedback, and what the facilitator would change.
3. Update the README's status line. Until then it says the kit hasn't been run with real staff.

Be careful reading a small group: with 8 people, one person changing an answer is 12 points.
Report counts, not just percentages.

## Making changes

`main` is protected: every change goes through a pull request, and the tests must pass on Python
3.11 to 3.14 before it can merge. Open an issue, branch from `main`, open a PR using the template.
GitHub Pages rebuilds the site from `main` after the tests pass.

## Contacts

- SNAP questions for a real client: the state SNAP agency, or **211**.
- Anthropic's privacy questions: the [Privacy Center](https://privacy.claude.com/).
- This kit: open an issue on the repo.
