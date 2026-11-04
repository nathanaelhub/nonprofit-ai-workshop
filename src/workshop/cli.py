"""workshop build | refresh-sources | check"""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="workshop", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="build the site into _site/")
    b.add_argument("--out", default="_site")
    r = sub.add_parser("refresh-sources", help="re-download the cached sources; then run the tests")
    r.add_argument("ids", nargs="*", help="source ids (default: all)")
    c = sub.add_parser("check", help="run the exercise prompts through Claude and record what happened")
    c.add_argument("--model", default="sonnet")
    c.add_argument("--repeats", type=int, default=3)
    c.add_argument("--concurrency", type=int, default=2)
    c.add_argument("--rescore", metavar="DIR", help="score a saved run again instead of asking Claude")
    a = p.parse_args(argv)
    if a.cmd == "build":
        from .build import build
        print(build(a.out))
    elif a.cmd == "refresh-sources":
        from .sources import refresh
        changed = refresh(a.ids or None)
        print(f"{len(changed)} changed. Now run: uv run pytest")
    elif a.cmd == "check":
        import asyncio

        from pathlib import Path

        from .check import rescore, run
        out = rescore(Path(a.rescore)) if a.rescore else asyncio.run(run(a.model, a.repeats, a.concurrency))
        print((out / "summary.md").read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
