"""Core docs, docs/ structure, archive filenames, plan-state uniqueness, and legacy ledger scope."""

from __future__ import annotations

from pathlib import Path

from .result import FAIL, NOT_APPLICABLE, PASS, CheckResult
from .spec import (
    CATEGORIES,
    CORE_DOCS,
    DISCOVERY_FILENAMES,
    DOCS_ROOT,
    LEGACY_LEDGER_PATH,
    META_DIR,
    PLAN_STATES,
    read_text,
)


def docs_checks(root: Path) -> list[CheckResult]:
    return [_core(root), _structure(root), _archive(root), _plans_unique(root), _legacy_ledger(root)]


def _core(root: Path) -> CheckResult:
    missing = sorted(name for name in CORE_DOCS if not _non_empty(root / name))
    if missing:
        return CheckResult("docs-core", FAIL, f"missing or empty core docs: {', '.join(missing)}")
    return CheckResult("docs-core", PASS, f"{len(CORE_DOCS)} core docs present")


def _structure(root: Path) -> CheckResult:
    """Core directories must exist. An extra directory is reported, never failed.

    A project can have a good reason for a directory outside the recommended names, and that reason
    lives in prose no check can read. Failing on the name alone would either force a rename or
    invite a policy-exception file, so the unrecognized names are named in the report instead.
    """
    docs = root / DOCS_ROOT
    if not docs.is_dir():
        return CheckResult("docs-structure", FAIL, f"missing documentation root: {DOCS_ROOT}/")
    recognized = set(CATEGORIES) | {META_DIR}
    extra = sorted(
        entry.name for entry in docs.iterdir() if entry.is_dir() and entry.name not in recognized
    )
    if extra:
        return CheckResult(
            "docs-structure",
            PASS,
            f"{DOCS_ROOT}/ present; directories outside the recommended names, "
            f"left to the project to justify in {DOCS_ROOT}/README.md: {', '.join(extra)}",
        )
    return CheckResult("docs-structure", PASS, f"{DOCS_ROOT}/ uses recommended category names only")


def _archive(root: Path) -> CheckResult:
    docs = root / DOCS_ROOT
    if not docs.is_dir():
        return CheckResult("archive-no-discovery", NOT_APPLICABLE, f"no {DOCS_ROOT}/ directory")
    offenders = sorted(
        str(path.relative_to(root))
        for path in docs.rglob("*.md")
        if path.is_file() and path.name in DISCOVERY_FILENAMES
    )
    if offenders:
        return CheckResult(
            "archive-no-discovery",
            FAIL,
            f"auto-discovered agent filenames under {DOCS_ROOT}/ keep loading: {', '.join(offenders)}",
        )
    return CheckResult("archive-no-discovery", PASS, f"no auto-loading agent filenames under {DOCS_ROOT}/")


def _plans_unique(root: Path) -> CheckResult:
    seen: dict[str, list[str]] = {}
    for state in PLAN_STATES:
        directory = root / state
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*.md")):
            seen.setdefault(path.name, []).append(str(path.relative_to(root)))
    duplicates = sorted(f"{name} -> {', '.join(paths)}" for name, paths in seen.items() if len(paths) > 1)
    if duplicates:
        return CheckResult("plans-unique", FAIL, f"plan in multiple states: {'; '.join(duplicates)}")
    return CheckResult("plans-unique", PASS, f"{len(seen)} plan files each in one state")


def _legacy_ledger(root: Path) -> CheckResult:
    """A coverage ledger persisted under an earlier standard version is optional history.

    It is no longer required, no longer validated, and never rewritten or removed by this tooling.
    Reporting that it exists tells an agent there is prior audit work worth reading.
    """
    if not (root / LEGACY_LEDGER_PATH).exists():
        return CheckResult(
            "legacy-ledger", NOT_APPLICABLE, f"no {LEGACY_LEDGER_PATH}; none is required"
        )
    return CheckResult(
        "legacy-ledger",
        PASS,
        f"{LEGACY_LEDGER_PATH} exists as optional historical input: read it for prior audit "
        "findings; this tooling neither validates nor modifies it",
    )


def _non_empty(path: Path) -> bool:
    text = read_text(path) if path.is_file() else None
    return bool(text and text.strip())
