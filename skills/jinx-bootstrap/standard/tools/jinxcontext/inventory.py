"""Required inventory of a distributable package's embedded standard copy."""

from __future__ import annotations

from pathlib import Path

TEMPLATE_FILES = (
    "agents-root.template.md",
    "architecture-overview.template.md",
    "claude-bridge.template.md",
    "docs-readme.template.md",
    "kiro-steering.template.md",
    "manifest.template.json",
    "plan.template.md",
    "plans-readme.template.md",
    "project.template.md",
    "spec.template.md",
)
SUPPORT_MODULES = (
    "__init__.py",
    "agent_checks.py",
    "cli.py",
    "docs_checks.py",
    "links.py",
    "manifest_checks.py",
    "markdown.py",
    "package_checks.py",
    "project_checks.py",
    "result.py",
    "scaffold.py",
    "scaffold_plan.py",
    "spec.py",
)
ENTRY_POINTS = ("tools/jinx_context_check.py", "tools/jinx_context_scaffold.py")
ROOT_ASSETS = ("contract.md", "VERSION")


def required_assets() -> tuple[str, ...]:
    """Every file a standard copy must carry for both tools to run standalone."""
    return (
        *ROOT_ASSETS,
        *ENTRY_POINTS,
        *(f"templates/{name}" for name in TEMPLATE_FILES),
        *(f"tools/jinxcontext/{name}" for name in SUPPORT_MODULES),
    )


def missing_assets(standard_dir: Path) -> list[str]:
    return sorted(name for name in required_assets() if not (standard_dir / name).is_file())
