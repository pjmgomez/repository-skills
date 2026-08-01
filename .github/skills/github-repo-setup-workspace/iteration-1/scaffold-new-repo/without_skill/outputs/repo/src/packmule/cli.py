"""Command-line interface for packmule."""

from __future__ import annotations

import argparse
from typing import Optional, Sequence

from packmule import __version__


def build_parser() -> argparse.ArgumentParser:
    """Create the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="packmule",
        description="Pack and haul your files around from the command line.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Entry point for the ``packmule`` command."""
    parser = build_parser()
    args = parser.parse_args(argv)
    # No subcommands implemented yet; print help as a friendly default.
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
