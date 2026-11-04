# Using Claude at a Nonprofit: a one-hour workshop

A ready-to-run, one-hour workshop that teaches non-technical nonprofit staff to use Claude
carefully: how to ask well, how to check an answer before using it, what never to paste in,
and when not to use it at all.

**Live site:** https://nathanaelhub.github.io/nonprofit-ai-workshop/

**Status:** being built from the approved [spec](docs/spec.md). Not yet run with real staff.

Not affiliated with Anthropic.

## Stack

- Static HTML and CSS, published with GitHub Pages (no build step for readers)
- Python 3.11+ with uv, for tests and for re-checking the exercises against Claude

## Run

```bash
uv sync
uv run pytest            # links resolve, attendee pages read at grade 8 or below, ...
uv run workshop build    # -> _site/, open _site/index.html
```

Pages are Markdown files in `content/`; GitHub Pages rebuilds the site from `main` after the
tests pass.
