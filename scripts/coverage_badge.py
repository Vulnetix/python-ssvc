#!/usr/bin/env python3
"""
Coverage badge generator

Writes the coverage.svg badge from the .coverage data file that
`coverage run` leaves behind. It replaces the coverage-badge package, which
is unmaintained and imports pkg_resources: that module left setuptools in
v81, so keeping coverage-badge meant pinning setuptools below 81 and living
with the advisories fixed after it. The badge, colour bands and rounding are
the same as coverage-badge 1.1.2 produced (MIT, Danilo Bargen), so the
committed coverage.svg does not change.

Usage: uv run python scripts/coverage_badge.py -o coverage.svg
"""

import argparse
import io
import sys
from pathlib import Path

import coverage
from coverage.results import display_covered

COLORS = [
    (95, "#4c1"),
    (90, "#97CA00"),
    (75, "#a4a61d"),
    (60, "#dfb317"),
    (40, "#fe7d37"),
    (0, "#e05d44"),
]

TEMPLATE = """\
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="99" height="20">
    <linearGradient id="b" x2="0" y2="100%">
        <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
        <stop offset="1" stop-opacity=".1"/>
    </linearGradient>
    <mask id="a">
        <rect width="99" height="20" rx="3" fill="#fff"/>
    </mask>
    <g mask="url(#a)">
        <path fill="#555" d="M0 0h63v20H0z"/>
        <path fill="{color}" d="M63 0h36v20H63z"/>
        <path fill="url(#b)" d="M0 0h99v20H0z"/>
    </g>
    <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
        <text x="31.5" y="15" fill="#010101" fill-opacity=".3">coverage</text>
        <text x="31.5" y="14">coverage</text>
        <text x="80" y="15" fill="#010101" fill-opacity=".3">{total}%</text>
        <text x="80" y="14">{total}%</text>
    </g>
</svg>
"""


def total_covered() -> str:
    """Return the total percentage, rounded with the project's precision."""
    cov = coverage.Coverage()
    cov.load()
    total = cov.report(file=io.StringIO())
    return display_covered(total, cov.config.precision)


def color_for(total: str) -> str:
    """Pick the badge colour band for a percentage."""
    percent = int(float(total))
    return next(color for floor, color in COLORS if percent >= floor)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument(
        "-o", dest="output", required=True, help="Path of the SVG to write."
    )
    args = parser.parse_args()

    try:
        total = total_covered()
    except coverage.exceptions.NoDataError as e:
        print(f"Error: {e} Did you run coverage first?", file=sys.stderr)
        return 1

    Path(args.output).write_text(TEMPLATE.format(color=color_for(total), total=total))
    print(f"Saved badge to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
