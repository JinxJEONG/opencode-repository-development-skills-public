"""Fixed standard facts plus small file and steering helpers shared by the checks."""

from __future__ import annotations

from pathlib import Path

DOCS_ROOT = "docs"
CORE_DOCS = (
    "docs/README.md",
    "docs/project.md",
    "docs/architecture/overview.md",
    "docs/plans/README.md",
)
# Recommended category names. A directory outside this set is reported as scope, not failed: a
# project may have a documented reason for one, and no check here can read that reason.
CATEGORIES = (
    "architecture",
    "specs",
    "plans",
    "decisions",
    "guides",
    "verification",
    "archive",
)
META_DIR = "_meta"
MANIFEST_PATH = "docs/_meta/manifest.json"
LEGACY_LEDGER_PATH = "docs/_meta/coverage-ledger.json"

AGENTS_ROOT = "AGENTS.md"
CLAUDE_ROOT = "CLAUDE.md"
CLAUDE_NESTED = ".claude/CLAUDE.md"
KIRO_STEERING = ".kiro/steering/project-context.md"
DISCOVERY_FILENAMES = ("AGENTS.md", "AGENTS.override.md", "CLAUDE.md")
CHURN_KEYS = ("generatedAt", "updatedAt", "timestamp", "lastRun")
PLAN_STATES = ("docs/plans/active", "docs/plans/completed")

# Advisory line guidance. Over one of these the check still reports PASS with a warning: size is a
# judgement call, and failing a run for it invites deleting a safety rule to fit the number.
AGENTS_LINE_GOAL = 100
SKILL_LINE_GOAL = 120
MANAGED_SURFACES = (AGENTS_ROOT, CLAUDE_ROOT, CLAUDE_NESTED, KIRO_STEERING)
MANAGED_SURFACE_GOAL_LINES = 320
MANAGED_SURFACE_EXCLUSIONS = (
    "nested AGENTS.md files below the root",
    "skill bodies loaded on invocation",
    "runtime-configured or personal instruction sources",
)

KIRO_EMBED_MARKERS = ("#[[file:", "#[[File:")
MANAGED_REQUIRED = "sharedInstructions"
MANAGED_KEYS = {
    MANAGED_REQUIRED: (AGENTS_ROOT,),
    "claudeBridge": (CLAUDE_ROOT, CLAUDE_NESTED),
    "kiroSteering": (KIRO_STEERING,),
}


def read_text(path: Path) -> str | None:
    """Return file text, or None when it is absent or undecodable."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def pure_line_count(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip())


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Parse a flat `key: value` YAML frontmatter block. None when absent."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, separator, value = line.partition(":")
        if not separator:
            return None
        fields[key.strip()] = value.strip().strip("'\"")
    return None


def kiro_embeds(text: str) -> list[str]:
    """Active Kiro file embeds or whole-document imports, wherever they appear on a line.

    An embed inside a sentence still loads the document, so the marker is matched anywhere, not
    only at the start of a line. A fenced code block is documentation, not an active embed.
    """
    found: list[str] = []
    fenced = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if any(marker in line for marker in KIRO_EMBED_MARKERS):
            found.append(stripped)
        elif stripped.startswith("@") and stripped.endswith(".md"):
            found.append(stripped)
    return sorted(set(found))
