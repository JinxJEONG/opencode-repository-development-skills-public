"""Package-mode checks: skill frontmatter, size, references, embedded standard copy."""

from __future__ import annotations

from pathlib import Path

from .inventory import missing_assets, required_assets
from .links import link_checks
from .result import FAIL, PASS, CheckResult
from .spec import SKILL_LINE_GOAL, parse_frontmatter, pure_line_count, read_text


def check_package(package: Path, standard_version: str) -> list[CheckResult]:
    """Checks for one distributable package. Ids are qualified with the package name."""
    results = _skill_checks(package)
    results.extend(link_checks(package, _package_docs(package), prefix="package-references-"))
    results.extend(_standard_copy_checks(package, standard_version))
    return [CheckResult(f"{package.name}:{item.check}", item.status, item.message) for item in results]


def _package_docs(package: Path) -> list[Path]:
    """Package-owned Markdown. Templates are excluded: their links resolve in a target project."""
    templates = package / "standard" / "templates"
    return sorted(
        path
        for path in package.rglob("*.md")
        if path.is_file() and templates not in path.parents
    )


def _skill_checks(package: Path) -> list[CheckResult]:
    path = package / "SKILL.md"
    text = read_text(path) if path.is_file() else None
    if text is None:
        return [
            CheckResult("package-skill-frontmatter", FAIL, f"missing or unreadable: {package.name}/SKILL.md"),
            CheckResult("package-skill-size", FAIL, f"cannot measure {package.name}/SKILL.md"),
        ]
    frontmatter = parse_frontmatter(text)
    if frontmatter is None:
        frontmatter_result = CheckResult(
            "package-skill-frontmatter",
            FAIL,
            f"{package.name}/SKILL.md has no parseable `---` frontmatter block",
        )
    elif frontmatter.get("name") != package.name:
        frontmatter_result = CheckResult(
            "package-skill-frontmatter",
            FAIL,
            f"{package.name}/SKILL.md declares name {frontmatter.get('name')!r}, expected {package.name!r}",
        )
    elif not frontmatter.get("description"):
        frontmatter_result = CheckResult(
            "package-skill-frontmatter", FAIL, f"{package.name}/SKILL.md has no description"
        )
    else:
        frontmatter_result = CheckResult(
            "package-skill-frontmatter", PASS, f"{package.name}/SKILL.md name and description valid"
        )

    lines = pure_line_count(text)
    note = (
        f", above the ~{SKILL_LINE_GOAL}-line goal; consider moving detail into references/"
        if lines > SKILL_LINE_GOAL
        else ""
    )
    # Advisory: an over-goal entry point is a size judgement, not a broken package.
    size_result = CheckResult(
        "package-skill-size", PASS, f"{package.name}/SKILL.md has {lines} non-blank lines{note}"
    )
    return [frontmatter_result, size_result]


def _standard_copy_checks(package: Path, standard_version: str) -> list[CheckResult]:
    embedded = package / "standard"
    missing = missing_assets(embedded)
    if missing:
        shown = ", ".join(missing[:8]) + (f", and {len(missing) - 8} more" if len(missing) > 8 else "")
        return [
            CheckResult(
                "package-standard-present",
                FAIL,
                f"{package.name}/standard/ is incomplete, missing {len(missing)} of "
                f"{len(required_assets())} required assets: {shown}",
            ),
            CheckResult(
                "package-standard-version",
                FAIL,
                f"cannot trust {package.name}/standard/VERSION from an incomplete copy",
            ),
        ]
    declared = (read_text(embedded / "VERSION") or "").strip()
    version_result = (
        CheckResult("package-standard-version", PASS, f"{package.name}/standard/VERSION is {declared}")
        if declared == standard_version
        else CheckResult(
            "package-standard-version",
            FAIL,
            f"{package.name}/standard/VERSION is {declared!r}, acting standard is {standard_version!r}",
        )
    )
    return [
        CheckResult(
            "package-standard-present",
            PASS,
            f"{package.name}/standard/ carries all {len(required_assets())} required assets",
        ),
        version_result,
    ]
