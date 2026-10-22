"""Scaffold planning and content generation from the shipped templates."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Literal, TypeAlias

from .spec import (
    AGENTS_ROOT,
    CLAUDE_NESTED,
    CLAUDE_ROOT,
    DOCS_ROOT,
    KIRO_STEERING,
    MANIFEST_PATH,
    read_text,
)

GENERATED_PATHS = (MANIFEST_PATH,)
REQUIRED_DIRECTORIES: Final = (
    "src",
    "tests",
    "experiments",
    "outputs",
    "docs/architecture",
    "docs/specs",
    "docs/plans/active",
    "docs/plans/completed",
)
ScaffoldAction: TypeAlias = Literal["keep", "create", "mkdir"]

# target path -> template filename
FILE_TEMPLATES = {
    "AGENTS.md": "agents-root.template.md",
    "docs/README.md": "docs-readme.template.md",
    "docs/project.md": "project.template.md",
    "docs/architecture/overview.md": "architecture-overview.template.md",
    "docs/plans/README.md": "plans-readme.template.md",
}
PUBLISHED_MARKERS = (
    "docs/_config.yml",
    "docs/mkdocs.yml",
    "docs/.nojekyll",
    "docs/index.html",
    "docs/_build",
    "mkdocs.yml",
    "docusaurus.config.js",
    "docusaurus.config.ts",
)


@dataclass(frozen=True)
class ScaffoldRequest:
    """One scaffold run: where to write, what to write from, and for whom."""

    root: Path
    templates: Path
    targets: tuple[str, ...]
    version: str

    @property
    def has_nested_bridge(self) -> bool:
        return (self.root / CLAUDE_NESTED).is_file()


def blockers(request: ScaffoldRequest) -> list[str]:
    """Every condition that forbids writing, collected before a single file is created."""
    published = sorted(marker for marker in PUBLISHED_MARKERS if (request.root / marker).exists())
    if published:
        return [
            f"this looks like a published or generated documentation site ({', '.join(published)}); "
            f"scaffolding {DOCS_ROOT}/ could overwrite published source or output"
        ]
    actions = plan(request)
    found: list[str] = []
    for _, path in actions:
        found.extend(_destination_blockers(request.root, path))
    found.extend(_template_blockers(request, actions))
    return sorted(set(found))


def _destination_blockers(root: Path, path: str) -> list[str]:
    """Reject symlinked paths and collisions with the required destination type."""
    found = _ancestor_blockers(root, path)
    target = root / path
    if target.is_symlink():
        found.append(f"{path} is a symlink to {_link_target(target)}; refusing to write through it")
    elif path in REQUIRED_DIRECTORIES:
        if target.exists() and not target.is_dir():
            found.append(f"{path} exists but is not a directory; the scaffold will not remove it")
    elif target.is_dir():
        found.append(
            f"{path} exists as a directory where the standard requires a file; "
            "the scaffold will not remove it"
        )
    return found


def _ancestor_blockers(root: Path, path: str) -> list[str]:
    relative = Path(path)
    for index in range(1, len(relative.parts)):
        ancestor = root.joinpath(*relative.parts[:index])
        shown = "/".join(relative.parts[:index])
        if ancestor.is_symlink():
            return [
                f"{shown} is a symlink; writing through it would place files at "
                f"{_link_target(ancestor)} instead of inside the repository"
            ]
        if ancestor.exists() and not ancestor.is_dir():
            return [f"{shown} exists but is not a directory, so {path} cannot be created"]
    return []


def _link_target(path: Path) -> str:
    try:
        return str(path.readlink())
    except OSError:
        return "an unreadable target"


def _template_blockers(request: ScaffoldRequest, actions: list[tuple[ScaffoldAction, str]]) -> list[str]:
    """A template that cannot be read would otherwise be written out as an empty file."""
    found = []
    for action, path in actions:
        if action != "create" or path in GENERATED_PATHS:
            continue
        name = _template_name(path)
        source = request.templates / name
        if not source.is_file():
            found.append(f"missing template {name} needed for {path}")
        elif read_text(source) is None:
            found.append(f"unreadable template {name} needed for {path}")
    return found


def plan(request: ScaffoldRequest) -> list[tuple[ScaffoldAction, str]]:
    """`(keep|create|mkdir, path)` for each required file or directory, sorted by path."""
    paths = list(FILE_TEMPLATES)
    if "claude" in request.targets and not request.has_nested_bridge:
        paths.append(CLAUDE_ROOT)
    if "kiro" in request.targets:
        paths.append(KIRO_STEERING)
    paths.extend(GENERATED_PATHS)
    paths.extend(REQUIRED_DIRECTORIES)
    actions: list[tuple[ScaffoldAction, str]] = []
    for path in sorted(paths):
        action: ScaffoldAction = "mkdir" if path in REQUIRED_DIRECTORIES else "create"
        if (request.root / path).exists():
            action = "keep"
        actions.append((action, path))
    return actions


def content(request: ScaffoldRequest, path: str) -> str | None:
    """Template text for `path`, or None when its template cannot be read."""
    if path == MANIFEST_PATH:
        return _manifest(request)
    return read_text(request.templates / _template_name(path))


def _template_name(path: str) -> str:
    template = FILE_TEMPLATES.get(path)
    if template is not None:
        return template
    return "claude-bridge.template.md" if path == CLAUDE_ROOT else "kiro-steering.template.md"


def _manifest(request: ScaffoldRequest) -> str:
    """The minimal manifest: the standard version, plus the surfaces this run established.

    Nothing derived from the filesystem is recorded. A per-category state duplicated what a
    directory listing already answers, and went stale on the first document anyone added.
    """
    payload = {
        "standardVersion": request.version,
        "managedPaths": _managed_paths(request),
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _managed_paths(request: ScaffoldRequest) -> dict[str, str]:
    """Only declare a path this run establishes: a declared path must exist."""
    managed = {"sharedInstructions": AGENTS_ROOT}
    if "claude" in request.targets:
        managed["claudeBridge"] = CLAUDE_NESTED if request.has_nested_bridge else CLAUDE_ROOT
    if "kiro" in request.targets:
        managed["kiroSteering"] = KIRO_STEERING
    return managed
