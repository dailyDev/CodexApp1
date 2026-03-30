#!/usr/bin/env python3
"""Basic application to read a 3-column test file."""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_three_column_file(file_path: Path) -> list[tuple[str, str, str]]:
    """Parse a text file where each non-empty line has exactly three columns."""
    rows: list[tuple[str, str, str]] = []

    with file_path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()

            # Skip blank lines and comments.
            if not line or line.startswith("#"):
                continue

            # Split on any amount of whitespace.
            columns = line.split()
            if len(columns) != 3:
                raise ValueError(
                    f"Line {line_number} must contain exactly 3 columns, found {len(columns)}: {line!r}"
                )

            rows.append((columns[0], columns[1], columns[2]))

    return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read and display rows from a text file with exactly three columns per line."
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Path to the input text file",
    )
    args = parser.parse_args()

    rows = parse_three_column_file(args.file)

    print(f"Read {len(rows)} row(s) from {args.file}:")
    for idx, (col1, col2, col3) in enumerate(rows, start=1):
        print(f"{idx:>3}: col1={col1!r}, col2={col2!r}, col3={col3!r}")


if __name__ == "__main__":
    main()
