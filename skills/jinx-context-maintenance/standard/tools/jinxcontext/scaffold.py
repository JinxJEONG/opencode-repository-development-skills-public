"""CLI for the create-only scaffold. Never overwrites, merges, or deletes."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import NoReturn

from .project_checks import ALL_TARGETS
from .result import EXIT_BLOCKED, EXIT_OK, EXIT_USAGE
from .scaffold_plan import ScaffoldAction, ScaffoldRequest, blockers, content, plan
from .spec import read_text


def assert_never(action: NoReturn) -> NoReturn:
    """Check exhaustiveness without requiring Python 3.11's typing API."""
    raise AssertionError(action)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jinx_context_scaffold.py",
        description=(
            "Create the missing files and required directories of the fixed context standard. "
            "Existing files are kept untouched; re-running produces no diff. "
            "It fills no semantic content: the agent populates every placeholder from target evidence."
        ),
        epilog=(
            "exit codes: 0 every planned path created or already present, "
            "2 blocked before writing or a write failed after the preflight, 64 usage error"
        ),
    )
    parser.add_argument("--root", default=".", help="repository root to scaffold")
    parser.add_argument(
        "--targets",
        default=",".join(ALL_TARGETS),
        help=f"comma-separated agent targets to scaffold: {', '.join(ALL_TARGETS)}",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="report what would be created without writing"
    )
    return parser


def main(argv: list[str], tools_dir: Path) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as error:
        return EXIT_USAGE if error.code not in (0, None) else EXIT_OK

    request = _request(args, tools_dir)
    if request is None:
        parser.print_usage()
        return EXIT_USAGE

    found = blockers(request)
    if found:
        for blocker in found:
            print(f"BLOCKED  {blocker}")
        print("summary: blocked, nothing written; resolve the blocker or choose an authorized scope")
        return EXIT_BLOCKED

    actions = plan(request)
    for action, path in actions:
        print(f"{action}  {path}")
    if args.dry_run:
        created = sum(1 for action, _ in actions if action != "keep")
        print(f"summary: dry-run, {created} would be created")
        return EXIT_OK

    created, failures = _apply(request, actions)
    kept = sum(1 for action, _ in actions if action == "keep")
    for path, reason in failures:
        print(f"BLOCKED  {path}: {reason}")
    print(f"summary: created={len(created)} kept={kept} blocked={len(failures)}")
    if failures:
        print(f"created before blocking: {', '.join(created) if created else 'none'}")
        return EXIT_BLOCKED
    return EXIT_OK


def _request(args: argparse.Namespace, tools_dir: Path) -> ScaffoldRequest | None:
    standard_dir = tools_dir.parent
    templates = standard_dir / "templates"
    version = (read_text(standard_dir / "VERSION") or "").strip()
    if not version or not templates.is_dir():
        print(f"error: incomplete standard copy at {standard_dir}")
        return None

    targets = tuple(part.strip() for part in args.targets.split(",") if part.strip())
    unknown = sorted(set(targets) - set(ALL_TARGETS))
    if unknown:
        print(f"error: unknown --targets values: {', '.join(unknown)}")
        return None

    root = Path(args.root)
    if not root.is_dir():
        print(f"error: --root is not a directory: {root}")
        return None
    return ScaffoldRequest(root=root, templates=templates, targets=targets, version=version)


def _apply(
    request: ScaffoldRequest, actions: list[tuple[ScaffoldAction, str]]
) -> tuple[list[str], list[tuple[str, str]]]:
    """Create planned paths, reporting failures without overwriting existing content."""
    created: list[str] = []
    failures: list[tuple[str, str]] = []
    for action, path in actions:
        match action:
            case "keep":
                continue
            case "mkdir":
                try:
                    (request.root / path).mkdir(parents=True, exist_ok=True)
                except OSError as error:
                    failures.append((path, f"{type(error).__name__}: {error.strerror or error}"))
                    continue
                reason = None
            case "create":
                body = content(request, path)
                if body is None:
                    failures.append((path, "its template became unreadable after the preflight"))
                    continue
                reason = _create_exclusive(request.root / path, body)
            case unreachable:
                assert_never(unreachable)
        if reason is None:
            created.append(path)
        else:
            failures.append((path, reason))
    return created, failures


def _create_exclusive(target: Path, body: str) -> str | None:
    """Write only when absent — `x` makes the check and the write atomic. Returns a failure reason."""
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("x", encoding="utf-8") as handle:
            handle.write(body)
    except FileExistsError:
        return "it appeared after the preflight; left untouched"
    except OSError as error:
        return f"{type(error).__name__}: {error.strerror or error}"
    return None
