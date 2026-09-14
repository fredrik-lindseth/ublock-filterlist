#!/usr/bin/env python3
"""Small, dependency-free checks for this uBlock Origin filter list."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
import sys


def audit(lines: list[str]) -> tuple[list[str], list[str]]:
    """Return errors and useful, non-failing maintenance notices."""
    errors: list[str] = []
    notices: list[str] = []
    exact = Counter()
    selector_domains: dict[tuple[str, str], set[str]] = defaultdict(set)

    for number, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        if not line or line.lstrip().startswith("!"):
            continue
        if line != line.lstrip():
            errors.append(f"{number}: active filter has leading whitespace")
            continue

        exact[line] += 1
        if "##" in line and not line.startswith("||"):
            domains, selector = line.split("##", 1)
            if not selector:
                errors.append(f"{number}: cosmetic filter has an empty selector")
                continue
            if "/" in domains:
                errors.append(f"{number}: cosmetic filter hostname contains '/'")
            if selector.startswith("#body,html:style("):
                errors.append(
                    f"{number}: use ##body,html:style(...), not ###body,html:style(...)"
                )
            if domains:
                for domain in domains.split(","):
                    selector_domains[(selector, "cosmetic")].add(domain)
            else:
                notices.append(f"{number}: global cosmetic filter: ##{selector}")
        elif line.startswith("||") and "$subdocument" in line and "domain=" not in line:
            notices.append(f"{number}: unscoped subdocument network filter: {line}")

    for rule, count in sorted(exact.items()):
        if count > 1:
            notices.append(f"duplicate ({count}x): {rule}")
    for (selector, _), domains in sorted(selector_domains.items()):
        if len(domains) > 1:
            notices.append(
                "can group %d domains: %s" % (len(domains), selector)
            )
    return errors, notices


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filterlist", type=Path)
    args = parser.parse_args()
    errors, notices = audit(args.filterlist.read_text(encoding="utf-8").splitlines(True))
    for notice in notices:
        print(f"NOTICE: {notice}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
