"""Check results, deterministic rendering, and exit codes."""

from __future__ import annotations

import json
from dataclasses import dataclass

PASS = "PASS"
FAIL = "FAIL"
BLOCKED = "BLOCKED"
NOT_APPLICABLE = "NOT_APPLICABLE"

EXIT_OK = 0
EXIT_FAIL = 1
EXIT_BLOCKED = 2
EXIT_USAGE = 64

# Printed with every report. Without it a clean run reads as "this repository is ready", which is a
# claim no file-shape check can make.
SCOPE = (
    "scope: static structure only — file presence, shapes, declared paths, links, and anchors. "
    "It does not establish that a document is accurate, that its content covers a requirement, or "
    "that an agent loaded it at runtime. Those are the agent's recorded judgement, reported separately."
)


@dataclass(frozen=True)
class CheckResult:
    """One check outcome. `message` must name the offending path when not PASS."""

    check: str
    status: str
    message: str

    def __post_init__(self) -> None:
        if self.status not in (PASS, FAIL, BLOCKED, NOT_APPLICABLE):
            raise ValueError(f"unknown status: {self.status}")


def sort_results(results: list[CheckResult]) -> list[CheckResult]:
    return sorted(results, key=lambda item: item.check)


def render_text(results: list[CheckResult]) -> str:
    ordered = sort_results(results)
    width = max((len(item.status) for item in ordered), default=0)
    lines = [f"{item.status.ljust(width)}  {item.check}  {item.message}" for item in ordered]
    counts = {status: 0 for status in (PASS, FAIL, BLOCKED, NOT_APPLICABLE)}
    for item in ordered:
        counts[item.status] += 1
    summary = " ".join(f"{status}={counts[status]}" for status in (PASS, FAIL, BLOCKED, NOT_APPLICABLE))
    lines.append(f"summary: {summary}")
    lines.append(SCOPE)
    return "\n".join(lines)


def render_json(results: list[CheckResult]) -> str:
    payload = {
        "scope": SCOPE.removeprefix("scope: "),
        "results": [
            {"check": item.check, "status": item.status, "message": item.message}
            for item in sort_results(results)
        ],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def exit_code(results: list[CheckResult]) -> int:
    if any(item.status == FAIL for item in results):
        return EXIT_FAIL
    if any(item.status == BLOCKED for item in results):
        return EXIT_BLOCKED
    return EXIT_OK
