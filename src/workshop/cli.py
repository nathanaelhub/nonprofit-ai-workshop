"""workshop build | refresh-sources"""

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
    a = p.parse_args(argv)
    if a.cmd == "build":
        from .build import build
        print(build(a.out))
    elif a.cmd == "refresh-sources":
        from .sources import refresh
        changed = refresh(a.ids or None)
        print(f"{len(changed)} changed. Now run: uv run pytest")
    return 0


if __name__ == "__main__":
    sys.exit(main())
