---
title: Answer key: Exercise 2, Check before using
audience: facilitator
---

# Answer key: Exercise 2, Check before using

**Time:** 12 minutes (3 to ask, 4 to check, 5 to discuss the conflict).
**Handout:** [Exercise 2](../handouts/2-check.md).

## The official answer

From the USDA Food and Nutrition Service's FY 2027 cost-of-living page (checked 2026-11-03):
the gross monthly income limit for a household of 4 in the 48 states and DC is **$3,575**,
130% of the poverty line, **effective October 1, 2026, through September 30, 2027**.

Printed copy of the row, for when there's no internet:

| Household size | 48 states, DC, Guam, Virgin Islands | Alaska | Hawaii |
|---|---|---|---|
| 4 | $3,575 | $4,469 | $4,112 |

**Update this every October 1**, when the USDA publishes new numbers. The RUNBOOK has the steps,
and a test fails if the cached source no longer has this row.

## What usually happens

Claude's training stops at a date, so it often gives the figure from an earlier year (the
FY 2026 figure was lower) without saying which year it's for. Sometimes it gets the current figure.
Either way, the lesson is the same: you found the source and its dates, and now you know. If
Claude says it isn't sure and points to the USDA, praise that; it's the right behavior.

The facilitator guide shows what Claude said on the most recent check run.

## The Tennessee conflict

This is real, found while building a benefits screener in October 2026:

- A June 2026 news story (Hoodline) says Tennessee adopted "broad-based categorical eligibility",
  raising the gross limit from 130% to 200% of poverty. For four people, 200% is about $5,500 a
  month.
- The USDA's own BBCE state chart (checked 2026-11-03) does not list Tennessee.
- No official Tennessee document we could find confirms the change or its start date.

So the honest answer is "we don't know yet." Good answers from the room:

1. Tell the client she might qualify, and to apply anyway; only the agency decides.
2. Call the Tennessee Department of Human Services or 211 to ask.
3. Don't tell her she doesn't qualify based on a number from Claude, or from one website.

## If something goes wrong

- **The USDA page has moved or changed:** use the printed row above and say so. Then tell the
  kit's maintainer (see the RUNBOOK).
- **Someone outside Tennessee:** the federal figure applies in most states, but many states use
  BBCE with a higher limit. The lesson holds: check your state agency.
