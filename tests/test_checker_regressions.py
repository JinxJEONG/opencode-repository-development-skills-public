"""Checker read-path regressions: a malformed input must be reported, never skipped.

Each class pins one reproduced defect where the checker read a document, failed to understand part of
it, and reported a pass anyway. Scaffold write-path regressions live in `test_scaffold_regressions.py`.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from support import (  # noqa: E402
    CHECKER,
    REPO_ROOT,
    STANDARD_DIR,
    append,
    run,
    scaffolded_project,
    statuses,
)


@contextmanager
def installed_package() -> Iterator[tuple[Path, Path]]:
    with tempfile.TemporaryDirectory() as temporary:
        parent = Path(temporary)
        package = parent / "jinx-bootstrap"
        shutil.copytree(REPO_ROOT / "skills/jinx-bootstrap", package)
        yield parent, package


def rewrite_managed(root: Path, managed: dict[str, object]) -> None:
    path = root / "docs/_meta/manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["managedPaths"] = managed
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class PackageInventory(unittest.TestCase):
    """Defect 2: a four-asset spot check passed a package whose templates had been deleted."""

    def test_deleted_templates_directory_fails(self) -> None:
        with installed_package() as (parent, package):
            shutil.rmtree(package / "standard/templates")

            result = run(CHECKER, "--mode", "package", "--root", str(parent), "--package", package.name)

            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertEqual(statuses(result.stdout)["jinx-bootstrap:package-standard-present"], "FAIL")
            self.assertIn("templates/agents-root.template.md", result.stdout)

    def test_missing_support_module_fails(self) -> None:
        with installed_package() as (parent, package):
            (package / "standard/tools/jinxcontext/markdown.py").unlink()

            result = run(CHECKER, "--mode", "package", "--root", str(parent), "--package", package.name)

            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("tools/jinxcontext/markdown.py", result.stdout)

    def test_incomplete_copy_does_not_claim_a_trusted_version(self) -> None:
        with installed_package() as (parent, package):
            (package / "standard/templates/spec.template.md").unlink()

            result = run(CHECKER, "--mode", "package", "--root", str(parent), "--package", package.name)

            self.assertEqual(statuses(result.stdout)["jinx-bootstrap:package-standard-version"], "FAIL")

    def test_shipped_packages_carry_every_required_asset(self) -> None:
        sys.path.insert(0, str(STANDARD_DIR / "tools"))
        from jinxcontext.inventory import missing_assets  # noqa: PLC0415

        for package in ("jinx-bootstrap", "jinx-context-maintenance", "jinx-verify-change"):
            with self.subTest(package=package):
                self.assertEqual(missing_assets(REPO_ROOT / "skills" / package / "standard"), [])


class ManifestNonObject(unittest.TestCase):
    """Defect 3: a null, array, or scalar manifest crashed the version check."""

    def test_each_non_object_manifest_reports_structurally(self) -> None:
        for body, kind in (("null", "NoneType"), ("[]", "list"), ("42", "int"), ('"text"', "str")):
            with self.subTest(body=body), scaffolded_project() as root:
                (root / "docs/_meta/manifest.json").write_text(f"{body}\n", encoding="utf-8")

                result = run(CHECKER, "--root", str(root))

                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertNotIn("Traceback", result.stdout + result.stderr)
                parsed = statuses(result.stdout)
                for check in ("manifest-schema", "manifest-version", "manifest-managed-paths"):
                    self.assertEqual(parsed[check], "FAIL")
                self.assertIn(kind, result.stdout)

    def test_report_is_deterministic(self) -> None:
        with scaffolded_project() as root:
            (root / "docs/_meta/manifest.json").write_text("null\n", encoding="utf-8")
            first = run(CHECKER, "--root", str(root))
            second = run(CHECKER, "--root", str(root))
            self.assertEqual(first.stdout, second.stdout)


class ReferenceStyleLinks(unittest.TestCase):
    """Defect 4: `[text][label]` with `[label]: missing.md` was ignored and reported as complete."""

    def test_reference_definition_target_must_resolve(self) -> None:
        with scaffolded_project() as root:
            append(root / "docs/README.md", "\nSee [Broken][lost].\n\n[lost]: missing.md\n")

            result = run(CHECKER, "--root", str(root))

            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertEqual(statuses(result.stdout)["links-resolve"], "FAIL")
            self.assertIn("missing.md", result.stdout)

    def test_undefined_reference_label_is_reported_not_ignored(self) -> None:
        with scaffolded_project() as root:
            append(root / "docs/README.md", "\nSee [Broken][nowhere].\n")

            result = run(CHECKER, "--root", str(root))

            self.assertEqual(statuses(result.stdout)["links-resolve"], "FAIL")
            self.assertIn("no matching link definition", result.stdout)

    def test_resolvable_reference_definition_passes(self) -> None:
        with scaffolded_project() as root:
            append(root / "docs/README.md", "\nSee [Project][project].\n\n[project]: project.md\n")

            result = run(CHECKER, "--root", str(root))

            self.assertEqual(result.returncode, 0, result.stdout)


class KiroInlineEmbed(unittest.TestCase):
    """Defect 5: an embed inside a sentence bypassed the line-prefix no-embed check."""

    STEERING = ".kiro/steering/project-context.md"

    def test_inline_embed_is_detected(self) -> None:
        with scaffolded_project() as root:
            append(root / self.STEERING, "\nLoad #[[file:../../AGENTS.md]] before work.\n")

            result = run(CHECKER, "--root", str(root))

            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertEqual(statuses(result.stdout)["kiro-steering-no-embed"], "FAIL")
            self.assertIn("#[[file:../../AGENTS.md]]", result.stdout)

    def test_inline_capitalized_embed_is_detected(self) -> None:
        with scaffolded_project() as root:
            append(root / self.STEERING, "\nAlso pull in #[[File:../../docs/project.md]] here.\n")

            result = run(CHECKER, "--root", str(root))

            self.assertEqual(statuses(result.stdout)["kiro-steering-no-embed"], "FAIL")

    def test_embed_shown_inside_a_fenced_block_is_documentation(self) -> None:
        with scaffolded_project() as root:
            append(root / self.STEERING, "\nNever write this:\n\n```text\n#[[file:../../AGENTS.md]]\n```\n")

            result = run(CHECKER, "--root", str(root))

            self.assertEqual(statuses(result.stdout)["kiro-steering-no-embed"], "PASS", result.stdout)


class ManagedPathSemantics(unittest.TestCase):
    """Defect 6: a non-string managedPaths value was skipped and still counted as a pass."""

    def test_non_string_value_fails(self) -> None:
        result = self._with_managed({"sharedInstructions": 42})
        self.assertEqual(statuses(result.stdout)["manifest-managed-paths"], "FAIL")
        self.assertIn("non-empty string path", result.stdout)

    def test_blank_value_fails(self) -> None:
        result = self._with_managed({"sharedInstructions": "AGENTS.md", "claudeBridge": "  "})
        self.assertEqual(statuses(result.stdout)["manifest-managed-paths"], "FAIL")

    def test_non_canonical_path_for_a_managed_key_fails(self) -> None:
        result = self._with_managed({"sharedInstructions": "AGENTS.md", "kiroSteering": "docs/README.md"})
        self.assertEqual(statuses(result.stdout)["manifest-managed-paths"], "FAIL")
        self.assertIn("must be one of", result.stdout)

    def test_unknown_key_fails(self) -> None:
        result = self._with_managed({"sharedInstructions": "AGENTS.md", "extra": "AGENTS.md"})
        self.assertEqual(statuses(result.stdout)["manifest-managed-paths"], "FAIL")
        self.assertIn("unknown managedPaths keys: extra", result.stdout)

    def test_missing_required_key_fails(self) -> None:
        result = self._with_managed({"claudeBridge": "CLAUDE.md"})
        self.assertEqual(statuses(result.stdout)["manifest-managed-paths"], "FAIL")
        self.assertIn("sharedInstructions is required", result.stdout)

    def test_nested_bridge_path_is_accepted_for_the_bridge_key(self) -> None:
        with scaffolded_project() as root:
            nested = root / ".claude/CLAUDE.md"
            nested.parent.mkdir(parents=True, exist_ok=True)
            nested.write_text("@../AGENTS.md\n", encoding="utf-8")
            (root / "CLAUDE.md").unlink()
            rewrite_managed(root, {"sharedInstructions": "AGENTS.md", "claudeBridge": ".claude/CLAUDE.md"})

            result = run(CHECKER, "--root", str(root))

            self.assertEqual(statuses(result.stdout)["manifest-managed-paths"], "PASS", result.stdout)

    def _with_managed(self, managed: dict[str, object]):
        with scaffolded_project() as root:
            rewrite_managed(root, managed)
            return run(CHECKER, "--root", str(root))


if __name__ == "__main__":
    unittest.main()
