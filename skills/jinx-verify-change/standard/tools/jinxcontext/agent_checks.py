"""Agent surface checks: root router, Claude bridge, Kiro steering route, advisory size."""

from __future__ import annotations

from pathlib import Path

from .result import FAIL, NOT_APPLICABLE, PASS, CheckResult
from .spec import (
    AGENTS_LINE_GOAL,
    AGENTS_ROOT,
    CLAUDE_NESTED,
    CLAUDE_ROOT,
    KIRO_STEERING,
    MANAGED_SURFACE_EXCLUSIONS,
    MANAGED_SURFACE_GOAL_LINES,
    MANAGED_SURFACES,
    kiro_embeds,
    parse_frontmatter,
    pure_line_count,
    read_text,
)

DOCS_INDEX = "docs/README.md"


def agents_checks(root: Path) -> list[CheckResult]:
    path = root / AGENTS_ROOT
    text = read_text(path) if path.is_file() else None
    if not text or not text.strip():
        return [
            CheckResult("agents-root", FAIL, f"missing or empty: {AGENTS_ROOT}"),
            CheckResult("agents-routing", FAIL, f"cannot check routing without {AGENTS_ROOT}"),
            CheckResult("bridge-no-cycle", FAIL, f"cannot check imports without {AGENTS_ROOT}"),
        ]
    return [
        CheckResult("agents-root", PASS, f"{AGENTS_ROOT} present"),
        _routing(text),
        _no_cycle(text),
    ]


def _routing(text: str) -> CheckResult:
    if DOCS_INDEX in text:
        return CheckResult("agents-routing", PASS, f"{AGENTS_ROOT} routes to {DOCS_INDEX}")
    return CheckResult("agents-routing", FAIL, f"{AGENTS_ROOT} does not route to {DOCS_INDEX}")


def _no_cycle(text: str) -> CheckResult:
    cycles = sorted(
        line.strip() for line in text.splitlines() if line.strip().startswith("@") and "CLAUDE.md" in line
    )
    if cycles:
        return CheckResult(
            "bridge-no-cycle", FAIL, f"{AGENTS_ROOT} imports a Claude file: {'; '.join(cycles)}"
        )
    return CheckResult("bridge-no-cycle", PASS, f"{AGENTS_ROOT} imports no Claude file")


def surface_size_check(root: Path) -> CheckResult:
    """Advisory line count for the managed surfaces, always PASS.

    It reports each surface, the total, and what the total deliberately excludes. Size is a
    judgement: a long router may be carrying rules that must not be deleted to hit a number, so
    this reports the measurement and leaves the decision to the agent and the user.
    """
    measured = {
        name: pure_line_count(text)
        for name in MANAGED_SURFACES
        if (text := read_text(root / name)) is not None
    }
    total = sum(measured.values())
    counted = ", ".join(f"{name}={measured[name]}" for name in sorted(measured))
    scope = f"counted {counted}" if measured else "no managed surface file exists"
    absent = sorted(set(MANAGED_SURFACES) - set(measured))
    if absent:
        scope += f"; absent {', '.join(absent)}"
    scope += f"; not counted: {', '.join(MANAGED_SURFACE_EXCLUSIONS)}"

    notes = []
    router = measured.get(AGENTS_ROOT)
    if router is not None and router > AGENTS_LINE_GOAL:
        notes.append(f"{AGENTS_ROOT} is above its ~{AGENTS_LINE_GOAL}-line goal")
    if total > MANAGED_SURFACE_GOAL_LINES:
        notes.append(f"the total is above the ~{MANAGED_SURFACE_GOAL_LINES}-line goal")
    advice = (
        f"; {' and '.join(notes)} — consider moving detail into docs/, never dropping a rule"
        if notes
        else ""
    )
    return CheckResult(
        "surface-size",
        PASS,
        f"managed surfaces hold {total} non-blank lines ({scope}){advice}",
    )


def claude_checks(root: Path, targets: tuple[str, ...]) -> list[CheckResult]:
    if "claude" not in targets:
        return [CheckResult("claude-bridge", NOT_APPLICABLE, "claude not in --targets")]
    root_bridge = _has_import(read_text(root / CLAUDE_ROOT) or "", AGENTS_ROOT)
    nested_bridge = _has_import(read_text(root / CLAUDE_NESTED) or "", f"../{AGENTS_ROOT}")
    if root_bridge and nested_bridge:
        return [
            CheckResult(
                "claude-bridge",
                FAIL,
                f"two bridges define the shared import: {CLAUDE_ROOT} and {CLAUDE_NESTED}; "
                "keep the established one",
            )
        ]
    if root_bridge:
        return [CheckResult("claude-bridge", PASS, f"{CLAUDE_ROOT} imports @{AGENTS_ROOT}")]
    if nested_bridge:
        return [CheckResult("claude-bridge", PASS, f"{CLAUDE_NESTED} imports @../{AGENTS_ROOT}")]
    return [
        CheckResult(
            "claude-bridge",
            FAIL,
            f"no effective bridge: add @{AGENTS_ROOT} to {CLAUDE_ROOT} "
            f"or @../{AGENTS_ROOT} to {CLAUDE_NESTED}",
        )
    ]


def _has_import(text: str, target: str) -> bool:
    return any(line.strip() == f"@{target}" for line in text.splitlines())


def kiro_checks(root: Path, targets: tuple[str, ...]) -> list[CheckResult]:
    if "kiro" not in targets:
        return [
            CheckResult("kiro-steering", NOT_APPLICABLE, "kiro not in --targets"),
            CheckResult("kiro-steering-no-embed", NOT_APPLICABLE, "kiro not in --targets"),
        ]
    path = root / KIRO_STEERING
    text = read_text(path) if path.is_file() else None
    if not text:
        return [
            CheckResult("kiro-steering", FAIL, f"missing mandatory steering file: {KIRO_STEERING}"),
            CheckResult("kiro-steering-no-embed", FAIL, f"cannot inspect {KIRO_STEERING}"),
        ]
    return [_steering_route(text), _steering_no_embed(text)]


def _steering_route(text: str) -> CheckResult:
    problems = []
    frontmatter = parse_frontmatter(text)
    if frontmatter is None or frontmatter.get("inclusion") != "always":
        problems.append("frontmatter must set inclusion: always")
    if AGENTS_ROOT not in text:
        problems.append(f"must route to root {AGENTS_ROOT}")
    if DOCS_INDEX not in text:
        problems.append(f"must name {DOCS_INDEX} as the fallback")
    if problems:
        return CheckResult("kiro-steering", FAIL, f"{KIRO_STEERING}: " + "; ".join(problems))
    return CheckResult("kiro-steering", PASS, f"{KIRO_STEERING} routes with inclusion: always")


def _steering_no_embed(text: str) -> CheckResult:
    embeds = kiro_embeds(text)
    if embeds:
        return CheckResult(
            "kiro-steering-no-embed",
            FAIL,
            f"{KIRO_STEERING} embeds or imports whole documents: {'; '.join(embeds)}",
        )
    return CheckResult("kiro-steering-no-embed", PASS, f"{KIRO_STEERING} routes without embedding")
