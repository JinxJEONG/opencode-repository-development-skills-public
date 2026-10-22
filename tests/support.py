"""Shared helpers and fixtures for the standard tooling tests."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Final

REPO_ROOT = Path(__file__).resolve().parent.parent
STANDARD_DIR = REPO_ROOT / "standard"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
CHECKER = STANDARD_DIR / "tools" / "jinx_context_check.py"
SCAFFOLD = STANDARD_DIR / "tools" / "jinx_context_scaffold.py"
SYNC = REPO_ROOT / "tools" / "sync_standard.py"
PACKAGES = ("jinx-bootstrap", "jinx-context-maintenance", "jinx-verify-change")
MANIFEST = "docs/_meta/manifest.json"
LEGACY_LEDGER = "docs/_meta/coverage-ledger.json"
COMPLIANT_FIXTURE = "compliant-project"
LEGACY_FIXTURE = "legacy-ledger-project"
REQUIRED_DIRECTORIES: Final = (
    "src", "tests", "experiments", "outputs", "docs/architecture", "docs/specs",
    "docs/plans/active", "docs/plans/completed",
)


def run(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        text=True,
        check=False,
        cwd=REPO_ROOT,
    )


def statuses(output: str) -> dict[str, str]:
    """Map check id -> status from the checker's text output."""
    parsed: dict[str, str] = {}
    for line in output.splitlines():
        if line.startswith(("summary:", "scope:")) or not line.strip():
            continue
        parts = line.split(None, 2)
        if len(parts) >= 2 and parts[0].isupper():
            parsed[parts[1]] = parts[0]
    return parsed


def copy_fixture(name: str, destination: Path) -> Path:
    target = destination / name
    shutil.copytree(FIXTURES / name, target)
    return target


@contextmanager
def compliant_fixture() -> Iterator[Path]:
    """A writable copy of the repository that satisfies the standard."""
    with tempfile.TemporaryDirectory() as temporary:
        yield copy_fixture(COMPLIANT_FIXTURE, Path(temporary))


@contextmanager
def legacy_fixture() -> Iterator[Path]:
    """A writable copy of a project carrying the 1.1 manifest shape and a persisted ledger."""
    with tempfile.TemporaryDirectory() as temporary:
        yield copy_fixture(LEGACY_FIXTURE, Path(temporary))


@contextmanager
def scaffolded_project() -> Iterator[Path]:
    """A freshly scaffolded project. The scaffold's own output is expected to pass every check."""
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary) / "project"
        root.mkdir()
        run(SCAFFOLD, "--root", str(root))
        yield root


def append(path: Path, extra: str) -> None:
    path.write_text(path.read_text(encoding="utf-8") + extra, encoding="utf-8")


def tree_snapshot(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): path.read_text(encoding="utf-8")
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }
