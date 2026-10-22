"""Argument parsing and dispatch for the read-only standard checker."""

from __future__ import annotations

import argparse
from pathlib import Path

from .package_checks import check_package
from .project_checks import ALL_TARGETS, check_project
from .result import EXIT_USAGE, exit_code, render_json, render_text
from .spec import read_text

USAGE_EPILOG = (
    "exit codes: 0 all PASS/NOT_APPLICABLE, 1 any FAIL, 2 any BLOCKED without FAIL, 64 usage error"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jinx_context_check.py",
        description=(
            "Read-only deterministic checks for the jinx context standard. "
            "Reports PASS/FAIL/BLOCKED/NOT_APPLICABLE per check and writes nothing."
        ),
        epilog=USAGE_EPILOG,
    )
    parser.add_argument(
        "--mode",
        choices=("project", "package"),
        default="project",
        help="project: a target repository's context standard. package: a distributable skill directory.",
    )
    parser.add_argument("--root", default=".", help="repository root (project mode) or parent of --package")
    parser.add_argument(
        "--package",
        action="append",
        default=[],
        help="package directory to check; repeatable. Required in package mode.",
    )
    parser.add_argument(
        "--targets",
        default=",".join(ALL_TARGETS),
        help=f"comma-separated agent targets to check: {', '.join(ALL_TARGETS)}",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text", help="output format")
    return parser


def standard_version(tools_dir: Path) -> str:
    return (read_text(tools_dir.parent / "VERSION") or "").strip()


def main(argv: list[str], tools_dir: Path) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as error:
        return EXIT_USAGE if error.code not in (0, None) else 0

    version = standard_version(tools_dir)
    if not version:
        parser.print_usage()
        print(f"error: cannot read standard version from {tools_dir.parent / 'VERSION'}")
        return EXIT_USAGE

    targets = tuple(part.strip() for part in args.targets.split(",") if part.strip())
    unknown = sorted(set(targets) - set(ALL_TARGETS))
    if unknown:
        parser.print_usage()
        print(f"error: unknown --targets values: {', '.join(unknown)}")
        return EXIT_USAGE

    root = Path(args.root)
    if not root.is_dir():
        parser.print_usage()
        print(f"error: --root is not a directory: {root}")
        return EXIT_USAGE

    if args.mode == "package":
        if not args.package:
            parser.print_usage()
            print("error: package mode requires at least one --package")
            return EXIT_USAGE
        results = []
        for name in args.package:
            package = Path(name) if Path(name).is_absolute() else root / name
            if not package.is_dir():
                parser.print_usage()
                print(f"error: --package is not a directory: {package}")
                return EXIT_USAGE
            results.extend(check_package(package, version))
    else:
        if args.package:
            parser.print_usage()
            print("error: --package is only valid with --mode package")
            return EXIT_USAGE
        results = check_project(root, targets, version)

    output = render_json(results) if args.format == "json" else render_text(results)
    print(output)
    return exit_code(results)
