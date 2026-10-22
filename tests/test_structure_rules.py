"""Tooling creates the skeleton; agents own semantic migration and certification.

Prose is reviewed through scenarios, not pinned strings. These tests cover observable CLI effects.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from support import (  # noqa: E402
    CHECKER,
    MANIFEST,
    PACKAGES,
    REPO_ROOT,
    REQUIRED_DIRECTORIES,
    SCAFFOLD,
    compliant_fixture,
    run,
    statuses,
    tree_snapshot,
)


class StructureAdoptionBoundaries(unittest.TestCase):
    def test_new_manifest_declares_141_when_scaffolded(self) -> None:
        # Given a new project, with no version declaration
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            # When the public scaffold creates its context
            result = run(SCAFFOLD, "--root", temporary)
            # Then it declares the release being introduced, not the preceding version
            self.assertEqual(result.returncode, 0, result.stdout)
            manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
            self.assertEqual(manifest["standardVersion"], "1.4.1")

    def test_12_manifest_fails_version_check_without_mutation(self) -> None:
        # Given an otherwise valid context still declaring the preceding standard
        with compliant_fixture() as root:
            (root / MANIFEST).write_text('{"standardVersion": "1.2.0"}\n', encoding="utf-8")
            before = tree_snapshot(root)
            # When the current checker inspects it
            result = run(CHECKER, "--root", str(root))
            # Then it requests an explicit upgrade without rewriting the project
            failures = {key for key, value in statuses(result.stdout).items() if value == "FAIL"}
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertEqual(failures, {"manifest-version"})
            self.assertEqual(tree_snapshot(root), before)

    def test_existing_architecture_and_version_survive_scaffold(self) -> None:
        # Given a previous-version project with custom architecture and input placement
        with compliant_fixture() as root:
            (root / MANIFEST).write_text('{"standardVersion": "1.2.0"}\n', encoding="utf-8")
            (root / "docs/architecture/overview.md").write_text(
                "# Local layout\n\nKeep inputs in vendor-assets; implementation is pending.\n",
                encoding="utf-8",
            )
            before = tree_snapshot(root)
            # When scaffold runs again
            result = run(SCAFFOLD, "--root", str(root))
            # Then adoption has not silently overwritten existing policy or version
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(tree_snapshot(root), before)

    def test_standalone_packages_preserve_flat_source_inputs_and_parallel_versions(self) -> None:
        for package in PACKAGES:
            with self.subTest(package=package), tempfile.TemporaryDirectory() as temporary:
                # Given an isolated installed package and established non-prescribed locations
                base = Path(temporary)
                installed = base / "installed" / package
                shutil.copytree(REPO_ROOT / "skills" / package, installed)
                root = base / "project"
                root.mkdir()
                originals = {
                    "main.py": b"print('flat entry')\n",
                    "vendor-assets/input.bin": b"\x00\xfforiginal\x80",
                    "api/v1/schema.json": b'{"version": 1}\n',
                    "api/v2/schema.json": b'{"version": 2}\n',
                    ".gitignore": b"local-output/\n",
                }
                for name, content in originals.items():
                    path = root / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(content)
                scaffold = installed / "standard/tools/jinx_context_scaffold.py"
                # When each standalone package's scaffold is used outside the repository
                result = subprocess.run(
                    [sys.executable, str(scaffold), "--root", str(root)],
                    cwd=temporary, capture_output=True, text=True, check=False,
                )
                # Then only context files and the required skeleton are added, with no input edits
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                for name, content in originals.items():
                    self.assertEqual((root / name).read_bytes(), content, name)
                created = {str(path.relative_to(root)) for path in root.rglob("*") if path.is_file()}
                self.assertEqual(created - originals.keys(), {
                    "AGENTS.md", "CLAUDE.md", ".kiro/steering/project-context.md",
                    "docs/README.md", "docs/project.md", "docs/architecture/overview.md",
                    "docs/plans/README.md", MANIFEST,
                })
                self.assertEqual(
                    {path.name for path in root.iterdir() if path.is_dir()},
                    {"api", "vendor-assets", "docs", ".kiro", "src", "tests", "experiments", "outputs"},
                )
                for directory in REQUIRED_DIRECTORIES:
                    self.assertTrue((root / directory).is_dir(), directory)


if __name__ == "__main__":
    unittest.main()
