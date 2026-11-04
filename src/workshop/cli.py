"""workshop build"""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="workshop", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="build the site into _site/")
    b.add_argument("--out", default="_site")
    a = p.parse_args(argv)
    if a.cmd == "build":
        from .build import build
        print(build(a.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
