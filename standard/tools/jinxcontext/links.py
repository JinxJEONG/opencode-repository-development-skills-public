"""Relative link and anchor resolution for managed Markdown files."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

from .markdown import heading_anchors, markdown_links
from .result import FAIL, NOT_APPLICABLE, PASS, CheckResult
from .spec import read_text


@dataclass
class _Tally:
    broken_links: list[str] = field(default_factory=list)
    broken_anchors: list[str] = field(default_factory=list)
    links: int = 0
    anchors: int = 0


def link_checks(root: Path, files: list[Path], prefix: str = "") -> list[CheckResult]:
    """Check that every relative link target and `#anchor` resolves."""
    link_id = f"{prefix}links-resolve" if prefix else "links-resolve"
    anchor_id = f"{prefix}anchors-resolve" if prefix else "anchors-resolve"
    if not files:
        return [
            CheckResult(link_id, NOT_APPLICABLE, "no managed Markdown files"),
            CheckResult(anchor_id, NOT_APPLICABLE, "no managed Markdown files"),
        ]

    tally = _Tally()
    for source in files:
        text = read_text(source)
        if text is None:
            tally.broken_links.append(f"{_rel(root, source)} is unreadable")
            continue
        _inspect(root, source, text, tally)

    return [
        CheckResult(link_id, FAIL, f"unresolved links: {'; '.join(sorted(tally.broken_links))}")
        if tally.broken_links
        else CheckResult(link_id, PASS, f"{tally.links} relative links resolve"),
        CheckResult(anchor_id, FAIL, f"unresolved anchors: {'; '.join(sorted(tally.broken_anchors))}")
        if tally.broken_anchors
        else CheckResult(anchor_id, PASS, f"{tally.anchors} anchors resolve"),
    ]


def _inspect(root: Path, source: Path, text: str, tally: _Tally) -> None:
    links = markdown_links(text)
    for label in links.undefined_labels:
        tally.broken_links.append(f"{_rel(root, source)} -> {label} (no matching link definition)")
    for target in links.targets:
        path_part, _, fragment = target.partition("#")
        anchor_target = source
        if path_part:
            tally.links += 1
            resolved = _resolve(source, path_part)
            if resolved is None or not resolved.exists():
                tally.broken_links.append(f"{_rel(root, source)} -> {target}")
                continue
            anchor_target = resolved
        if not fragment:
            continue
        tally.anchors += 1
        if anchor_target.is_dir() or anchor_target.suffix.lower() != ".md":
            continue
        target_text = read_text(anchor_target)
        if target_text is None:
            tally.broken_anchors.append(f"{_rel(root, source)} -> {target} (unreadable target)")
            continue
        if _normalize(fragment) not in heading_anchors(target_text):
            tally.broken_anchors.append(f"{_rel(root, source)} -> {target}")


def _resolve(source: Path, path_part: str) -> Path | None:
    if path_part.startswith("/"):
        return None
    try:
        return (source.parent / unquote(path_part)).resolve()
    except (OSError, ValueError):
        return None


def _normalize(fragment: str) -> str:
    return unquote(fragment).strip().lower()


def _rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)
