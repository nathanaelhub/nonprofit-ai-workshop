# Using Claude at a Nonprofit: a one-hour workshop

A ready-to-run, one-hour workshop that teaches non-technical nonprofit staff to use Claude
carefully: how to ask well, how to check an answer before using it, what never to paste in,
and when not to use it at all.

**Status:** being designed. The plan is in [`docs/spec.md`](docs/spec.md) once its pull
request is merged.

Not affiliated with Anthropic.

## Stack

- Static HTML and CSS, published with GitHub Pages (no build step for readers)
- Python 3.11+ with uv, for tests and for re-checking the exercises against Claude

## Run

```bash
uv sync
uv run pytest
```
