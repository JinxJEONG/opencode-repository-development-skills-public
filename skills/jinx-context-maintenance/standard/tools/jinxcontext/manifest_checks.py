"""Manifest presence, minimal schema, version, and declared managed paths.

The manifest carries one required fact: which standard version the project was established under.
Everything else is optional and only checked when it is there, so a project persisted under the
richer 1.1 shape keeps parsing without being asked to maintain fields nothing reads.
"""

from __future__ import annotations

import json
from pathlib import Path

from .result import FAIL, NOT_APPLICABLE, PASS, CheckResult
from .spec import (
    CHURN_KEYS,
    DOCS_ROOT,
    MANAGED_KEYS,
    MANAGED_REQUIRED,
    MANIFEST_PATH,
    read_text,
)

REQUIRED_KEY = "standardVersion"
SUPPORTED_SCHEMA_VERSIONS = (1,)


def manifest_checks(root: Path, standard_version: str) -> list[CheckResult]:
    path = root / MANIFEST_PATH
    raw = read_text(path)
    if raw is None:
        return _unreadable(f"missing or unreadable: {MANIFEST_PATH}")
    try:
        manifest = json.loads(raw)
    except json.JSONDecodeError as error:
        return _unreadable(f"{MANIFEST_PATH} is not valid JSON: {error.msg} at line {error.lineno}")
    if not isinstance(manifest, dict):
        # Guard before the field checks: a scalar, null, or array parses but has no `.get`.
        return _unreadable(
            f"{MANIFEST_PATH} must contain a JSON object, found {type(manifest).__name__}",
            present=True,
        )
    return [
        CheckResult("manifest-present", PASS, f"{MANIFEST_PATH} parsed"),
        _schema(manifest),
        _version(manifest, standard_version),
        _managed_paths(root, manifest),
    ]


def _unreadable(message: str, present: bool = False) -> list[CheckResult]:
    presence = (
        CheckResult("manifest-present", PASS, f"{MANIFEST_PATH} parsed")
        if present
        else CheckResult("manifest-present", FAIL, message)
    )
    return [
        presence,
        CheckResult("manifest-schema", FAIL, message),
        CheckResult("manifest-version", FAIL, f"cannot read {REQUIRED_KEY}: {message}"),
        CheckResult("manifest-managed-paths", FAIL, f"cannot read managedPaths: {message}"),
    ]


def _schema(manifest: dict) -> CheckResult:
    problems = []
    if not isinstance(manifest.get(REQUIRED_KEY), str):
        problems.append(f"{REQUIRED_KEY} must be a string")
    schema_version = manifest.get("schemaVersion")
    if schema_version is not None and schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        supported = ", ".join(str(value) for value in SUPPORTED_SCHEMA_VERSIONS)
        problems.append(f"schemaVersion must be one of {supported} when present, found {schema_version!r}")
    docs_root = manifest.get("docsRoot")
    if docs_root is not None and docs_root != DOCS_ROOT:
        problems.append(f'docsRoot must be "{DOCS_ROOT}" when present, found {docs_root!r}')
    churn = sorted(key for key in CHURN_KEYS if key in manifest)
    if churn:
        problems.append(f"churn-prone keys are forbidden: {', '.join(churn)}")
    if problems:
        return CheckResult("manifest-schema", FAIL, f"{MANIFEST_PATH}: " + "; ".join(problems))
    extra = sorted(set(manifest) - {REQUIRED_KEY, "schemaVersion", "docsRoot", "managedPaths"})
    note = f"; keys carried but not required: {', '.join(extra)}" if extra else ""
    return CheckResult("manifest-schema", PASS, f"{MANIFEST_PATH} declares {REQUIRED_KEY}{note}")


def _version(manifest: dict, standard_version: str) -> CheckResult:
    declared = manifest.get(REQUIRED_KEY)
    if declared == standard_version:
        return CheckResult("manifest-version", PASS, f"{REQUIRED_KEY} {standard_version}")
    return CheckResult(
        "manifest-version",
        FAIL,
        f"{MANIFEST_PATH} declares {REQUIRED_KEY} {declared!r}; acting standard is {standard_version!r}",
    )


def _managed_paths(root: Path, manifest: dict) -> CheckResult:
    managed = manifest.get("managedPaths")
    if managed is None:
        return CheckResult(
            "manifest-managed-paths", NOT_APPLICABLE, f"{MANIFEST_PATH} declares no managedPaths"
        )
    if not isinstance(managed, dict):
        return CheckResult(
            "manifest-managed-paths",
            FAIL,
            f"{MANIFEST_PATH}: managedPaths must be an object, found {type(managed).__name__}",
        )
    problems = [problem for key in sorted(managed) for problem in _managed_problems(root, key, managed[key])]
    unknown = sorted(set(managed) - set(MANAGED_KEYS))
    if unknown:
        problems.append(f"unknown managedPaths keys: {', '.join(unknown)}")
    if MANAGED_REQUIRED not in managed:
        problems.append(f"{MANAGED_REQUIRED} is required once managedPaths is declared")
    if problems:
        return CheckResult("manifest-managed-paths", FAIL, f"{MANIFEST_PATH}: " + "; ".join(problems))
    return CheckResult("manifest-managed-paths", PASS, f"{len(managed)} declared managed path(s) exist")


def _managed_problems(root: Path, key: str, value: object) -> list[str]:
    if not isinstance(value, str) or not value.strip():
        return [f"{key} must be a non-empty string path, found {value!r}"]
    allowed = MANAGED_KEYS.get(key)
    if allowed is not None and value not in allowed:
        return [f"{key} must be one of {', '.join(allowed)}, found {value!r}"]
    if not (root / value).exists():
        return [f"{key} declares {value} which does not exist"]
    return []
