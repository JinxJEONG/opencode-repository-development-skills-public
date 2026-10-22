#!/usr/bin/env python3
"""Synchronize the maintained `standard/` source into each distributable skill package.

Usage: python3 tools/sync_standard.py [--check] [--repo <path>]

`standard/` at the repository root is the only authored copy. Each package keeps a complete copy at
`skills/<package>/standard/` so an installed package never depends on a sibling at runtime.
`--check` reports drift and writes nothing; exit 1 on drift, 0 when synchronized.
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

PACKAGES = ("jinx-bootstrap", "jinx-context-maintenance", "jinx-verify-change")
SKIP_DIR_NAMES = {"__pycache__"}
EXIT_OK = 0
EXIT_DRIFT = 1
EXIT_USAGE = 64


def source_files(source: Path) -> list[Path]:
    files = [
        path
        for path in source.rglob("*")
        if path.is_file() and not any(part in SKIP_DIR_NAMES for part in path.relative_to(source).parts)
    ]
    return sorted(files)


def drift(source: Path, destination: Path) -> list[str]:
    """Return human-readable drift entries between the source and one package copy."""
    expected = {str(path.relative_to(source)) for path in source_files(source)}
    found = (
        {str(path.relative_to(destination)) for path in source_files(destination)}
        if destination.is_dir()
        else set()
    )
    entries = [f"missing: {name}" for name in sorted(expected - found)]
    entries += [f"unexpected: {name}" for name in sorted(found - expected)]
    entries += [
        f"differs: {name}"
        for name in sorted(expected & found)
        if not filecmp.cmp(source / name, destination / name, shallow=False)
    ]
    return entries


def sync(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns(*SKIP_DIR_NAMES),
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="sync_standard.py",
        description="Copy the maintained standard/ into every skill package, or check for drift.",
        epilog="exit codes: 0 synchronized, 1 drift found with --check, 64 usage error",
    )
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parent.parent))
    try:
        args = parser.parse_args(argv)
    except SystemExit as error:
        return EXIT_USAGE if error.code not in (0, None) else EXIT_OK

    repo = Path(args.repo)
    source = repo / "standard"
    if not source.is_dir():
        parser.print_usage()
        print(f"error: no maintained standard at {source}")
        return EXIT_USAGE

    drifted = False
    for package in PACKAGES:
        package_dir = repo / "skills" / package
        if not package_dir.is_dir():
            parser.print_usage()
            print(f"error: missing package directory: {package_dir}")
            return EXIT_USAGE
        destination = package_dir / "standard"
        entries = drift(source, destination)
        if not entries:
            print(f"in-sync  {package}")
            continue
        drifted = True
        if args.check:
            for entry in entries:
                print(f"drift    {package}: {entry}")
        else:
            sync(source, destination)
            print(f"synced   {package} ({len(entries)} change(s))")

    if args.check:
        print("summary: drift found" if drifted else "summary: all packages in sync")
        return EXIT_DRIFT if drifted else EXIT_OK
    print("summary: all packages synchronized")
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
