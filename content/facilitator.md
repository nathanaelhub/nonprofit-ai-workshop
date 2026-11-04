---
title: Facilitator guide
---

# Facilitator guide

You don't need to be technical to run this. You need to have used Claude a few times, and to be
comfortable saying "I don't know, let's check." That's the whole workshop in one sentence.

## The hour

| Min | Block | Materials |
|---|---|---|
| 0–5 | Welcome and pre-quiz | [Slides](slides.md), [quiz](quiz.md) |
| 5–12 | What Claude is and isn't | [Slides](slides.md) |
| 12–24 | Exercise 1: Ask well | [Handout](handouts/1-ask-well.md), [key](keys/1-ask-well.md) |
| 24–36 | Exercise 2: Check before using | [Handout](handouts/2-check.md), [key](keys/2-check.md) |
| 36–46 | Exercise 3: Protect clients | [Handout](handouts/3-protect.md), [key](keys/3-protect.md) |
| 46–55 | Exercise 4: When not to use it | [Handout](handouts/4-when-not.md), [key](keys/4-when-not.md) |
| 55–60 | Post-quiz, takeaway, feedback | [Quiz](quiz.md), [takeaway](takeaway.md), [feedback](feedback.md) |

## A week before

1. **Ask about the organization's AI policy.** If there is one, read it and bring it. If it
   conflicts with anything here, the policy wins; say so in the room.
2. **Check accounts.** Each pair needs one laptop signed in to Claude (a free account works). If
   people can't sign in, pairs can share yours, or use the printed sample answers.
3. **Run the check** (or ask the kit's maintainer to): `uv run workshop check`. It takes a few
   minutes and costs about ten cents. Read the summary, and print a few answers from
   `checks/results/<date>/answers.jsonl` as paper backups for Exercises 1 and 2.
4. **Check the SNAP number** in the [Exercise 2 key](keys/2-check.md) is still current (it changes
   every October 1; see the RUNBOOK).
5. **Print**, for 10 people (5 pairs):

| What | Copies |
|---|---|
| Handouts 1, 2 and 3 | 5 each (one per pair) |
| Handout 4 | 3 (one per group) |
| Quiz | 20 (before and after) |
| Privacy sheet and takeaway | 10 each |
| Feedback form | 10 |
| Answer keys and this guide | 1 each, for you |

## Block by block

### 0–5: Welcome and pre-quiz

Say: "This hour is about four habits for using Claude at work: asking well, checking, keeping
clients safe, and knowing when not to use it. It's not about becoming an expert."

Hand out the quiz. "This isn't graded and has no names. We'll take it again at the end, so we can
tell if the hour was worth it." Give 3 minutes. Collect them face down.

### 5–12: What Claude is and isn't

Use slides 4 to 6. The points to land:

- Claude writes by predicting likely words. That's why it's fluent, and why it can be fluent and
  wrong at the same time.
- It learned from text up to a date. It doesn't know this month's rules, your organization, or
  your clients, unless you tell it, and you shouldn't tell it about clients.
- It's good at drafts, rewording, summaries and ideas. It's not a source of facts.

Ask: "Who has used it already? What for?" Take two or three answers; don't let this run long.

### 12–24: Exercise 1, Ask well

Pairs, one handout each. Keep time: round 1 at minute 15, round 2 at minute 19, compare at 24.
Use the [key](keys/1-ask-well.md) for what to expect and the discussion prompts.

### 24–36: Exercise 2, Check before using

The SNAP number is real and current; the Tennessee conflict is real too. Spend the last 5 minutes
on step 3. The answer you want from the room: "We don't know, so we tell her to apply and we call
the agency or 211." [Key](keys/2-check.md).

### 36–46: Exercise 3, Protect clients

Start by saying nobody pastes the emails into Claude. When pairs try their de-identified
request, point out the reply is nearly as useful. Hand out the privacy sheet at the end.
[Key](keys/3-protect.md).

On the check run, a reply to the pasted email used the client's name and her child's name and
mentioned the breathing machine; the de-identified request got a template with none of that.
That's the trade: a more personal draft, for a client's details sitting in a chat.

### 46–55: Exercise 4, When not to use it

Groups of three or four. Five minutes to sort, four to discuss. Ask each group for the card they
argued about most. [Key](keys/4-when-not.md).

### 55–60: Close

Post-quiz (3 minutes), then hand out the takeaway and feedback form. Thank them. Tell them who to
ask about the organization's AI policy.

## If you're running behind

- Cut Exercise 4's discussion to the two hardest cards (3 and 8).
- Don't cut Exercise 3 or the post-quiz.

## After

1. Tally the quizzes with the [tally sheet](tally.md): count correct answers per question,
   before and after.
2. Read the feedback forms.
3. Send the tallies and a summary of the feedback (no names) to the kit's maintainer, or add them
   to the repo under `pilots/`. That's how this kit gets evidence that it works.

## What people ask

- **"Is Claude listening to everything?"** Point to the privacy sheet: it quotes what Anthropic
  says, with dates and links. Don't add to it from memory.
- **"Is it going to take my job?"** Be honest that you don't know. Today's point is narrower:
  if you use it, use it carefully.
- **"Which is better, Claude or another AI tool?"** Out of scope today. The four habits apply to
  all of them.
