"""Project-mode orchestration: context gate, then manifest, docs, agent, and link checks."""

from __future__ import annotations

from pathlib import Path

from .agent_checks import agents_checks, claude_checks, kiro_checks, surface_size_check
from .docs_checks import docs_checks
from .links import link_checks
from .manifest_checks import manifest_checks
from .result import BLOCKED, PASS, CheckResult
from .spec import AGENTS_ROOT, CLAUDE_NESTED, CLAUDE_ROOT, DOCS_ROOT, KIRO_STEERING, MANIFEST_PATH

ALL_TARGETS = ("codex", "claude", "kiro", "opencode")


def check_project(root: Path, targets: tuple[str, ...], standard_version: str) -> list[CheckResult]:
    if not (root / AGENTS_ROOT).exists() and not (root / MANIFEST_PATH).exists():
        return [
            CheckResult(
                "context-present",
                BLOCKED,
                f"no context standard found at {root}: neither {AGENTS_ROOT} nor "
                f"{MANIFEST_PATH} exists; run jinx-bootstrap before claiming verification",
            )
        ]

    results = [CheckResult("context-present", PASS, "shared instructions or manifest present")]
    results.extend(manifest_checks(root, standard_version))
    results.extend(docs_checks(root))
    results.extend(agents_checks(root))
    results.append(surface_size_check(root))
    results.extend(claude_checks(root, targets))
    results.extend(kiro_checks(root, targets))
    results.extend(link_checks(root, _managed_files(root)))
    return results


def _managed_files(root: Path) -> list[Path]:
    candidates = [root / AGENTS_ROOT, root / CLAUDE_ROOT, root / CLAUDE_NESTED, root / KIRO_STEERING]
    docs = root / DOCS_ROOT
    if docs.is_dir():
        candidates.extend(sorted(path for path in docs.rglob("*.md") if path.is_file()))
    return [path for path in candidates if path.is_file()]
