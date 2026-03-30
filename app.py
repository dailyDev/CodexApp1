#!/usr/bin/env python3
"""Basic application to read a 3-column test file."""

from __future__ import annotations

import argparse
from pathlib import Path


def detect_file_type(file_path: Path) -> str:
    """Detect file type from extension, defaulting to generic text."""
    return file_path.suffix.lstrip(".").lower() or "text"


def log_file_processing(file_path: Path, row_count: int, log_file: Path) -> None:
    """Write file processing details to a log file."""
    file_size = file_path.stat().st_size
    file_type = detect_file_type(file_path)
    log_line = (
        f"file={file_path} | rows={row_count} | size_bytes={file_size} | type={file_type}\n"
    )
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(log_line)


def parse_three_column_file(file_path: Path, log_file: Path = Path("file_processing.log")) -> list[tuple[str, str, str]]:
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

    log_file_processing(file_path=file_path, row_count=len(rows), log_file=log_file)

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
    parser.add_argument(
        "--log-file",
        type=Path,
        default=Path("file_processing.log"),
        help="Path to the output log file (default: file_processing.log)",
    )
    args = parser.parse_args()

    rows = parse_three_column_file(args.file, log_file=args.log_file)

    print(f"Read {len(rows)} row(s) from {args.file}:")
    for idx, (col1, col2, col3) in enumerate(rows, start=1):
        print(f"{idx:>3}: col1={col1!r}, col2={col2!r}, col3={col3!r}")


if __name__ == "__main__":
    main()
