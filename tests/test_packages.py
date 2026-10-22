"""Package synchronization and standalone operation of each distributable skill."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from support import (  # noqa: E402
    CHECKER,
    FIXTURES,
    PACKAGES,
    REPO_ROOT,
    STANDARD_DIR,
    SYNC,
    run,
    statuses,
)


class PackageChecks(unittest.TestCase):
    def test_every_shipped_package_passes_package_mode(self) -> None:
        arguments = ["--mode", "package", "--root", str(REPO_ROOT)]
        for package in PACKAGES:
            arguments.extend(["--package", f"skills/{package}"])
        result = run(CHECKER, *arguments)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(sorted(set(statuses(result.stdout).values())), ["PASS"], result.stdout)

    def test_mismatched_package_name_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "jinx-renamed"
            shutil.copytree(REPO_ROOT / "skills/jinx-bootstrap", package)
            result = run(CHECKER, "--mode", "package", "--root", temporary, "--package", "jinx-renamed")
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertEqual(statuses(result.stdout)["jinx-renamed:package-skill-frontmatter"], "FAIL")

    def test_package_without_standard_copy_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "jinx-bootstrap"
            shutil.copytree(REPO_ROOT / "skills/jinx-bootstrap", package)
            shutil.rmtree(package / "standard")
            result = run(CHECKER, "--mode", "package", "--root", temporary, "--package", "jinx-bootstrap")
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertEqual(statuses(result.stdout)["jinx-bootstrap:package-standard-present"], "FAIL")

    def test_stale_package_standard_version_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "jinx-bootstrap"
            shutil.copytree(REPO_ROOT / "skills/jinx-bootstrap", package)
            (package / "standard/VERSION").write_text("0.0.1\n", encoding="utf-8")
            result = run(CHECKER, "--mode", "package", "--root", temporary, "--package", "jinx-bootstrap")
            self.assertEqual(statuses(result.stdout)["jinx-bootstrap:package-standard-version"], "FAIL")

    def test_broken_package_reference_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "jinx-bootstrap"
            shutil.copytree(REPO_ROOT / "skills/jinx-bootstrap", package)
            skill = package / "SKILL.md"
            skill.write_text(
                skill.read_text(encoding="utf-8") + "\nSee [gone](references/not-here.md).\n",
                encoding="utf-8",
            )
            result = run(CHECKER, "--mode", "package", "--root", temporary, "--package", "jinx-bootstrap")
            self.assertEqual(
                statuses(result.stdout)["jinx-bootstrap:package-references-links-resolve"], "FAIL"
            )


class Synchronization(unittest.TestCase):
    def test_repository_is_in_sync(self) -> None:
        result = run(SYNC, "--check")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("all packages in sync", result.stdout)

    def test_check_detects_drift_and_sync_repairs_it(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            clone = Path(temporary) / "repo"
            shutil.copytree(
                REPO_ROOT,
                clone,
                ignore=shutil.ignore_patterns(".git", ".omo", ".memsearch", ".codegraph", "__pycache__"),
            )
            (clone / "skills/jinx-verify-change/standard/VERSION").write_text("9.9.9\n", encoding="utf-8")
            drifted = run(SYNC, "--check", "--repo", str(clone))
            self.assertEqual(drifted.returncode, 1, drifted.stdout)
            self.assertIn("differs: VERSION", drifted.stdout)

            repaired = run(SYNC, "--repo", str(clone))
            self.assertEqual(repaired.returncode, 0, repaired.stdout)
            verified = run(SYNC, "--check", "--repo", str(clone))
            self.assertEqual(verified.returncode, 0, verified.stdout)

    def test_sync_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            clone = Path(temporary) / "repo"
            shutil.copytree(
                REPO_ROOT,
                clone,
                ignore=shutil.ignore_patterns(".git", ".omo", ".memsearch", ".codegraph", "__pycache__"),
            )
            run(SYNC, "--repo", str(clone))
            first = _digest(clone / "skills")
            run(SYNC, "--repo", str(clone))
            self.assertEqual(_digest(clone / "skills"), first)

    def test_every_package_copy_matches_the_maintained_source(self) -> None:
        expected = _digest(STANDARD_DIR)
        for package in PACKAGES:
            with self.subTest(package=package):
                self.assertEqual(_digest(REPO_ROOT / "skills" / package / "standard"), expected)

    def test_missing_source_is_a_usage_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = run(SYNC, "--repo", temporary)
            self.assertEqual(result.returncode, 64)


class StandaloneInstallation(unittest.TestCase):
    """An installed package must work without the repository or a sibling package."""

    def test_each_installed_package_runs_its_own_tooling(self) -> None:
        for package in PACKAGES:
            with self.subTest(package=package), tempfile.TemporaryDirectory() as temporary:
                installed = Path(temporary) / "skills" / package
                shutil.copytree(REPO_ROOT / "skills" / package, installed)
                checker = installed / "standard/tools/jinx_context_check.py"
                result = subprocess.run(
                    [sys.executable, str(checker), "--root", str(FIXTURES / "compliant-project")],
                    capture_output=True,
                    text=True,
                    check=False,
                    cwd=temporary,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertNotIn("FAIL", set(statuses(result.stdout).values()), result.stdout)

    def test_installed_scaffold_runs_without_the_repository(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            installed = Path(temporary) / "skills/jinx-bootstrap"
            shutil.copytree(REPO_ROOT / "skills/jinx-bootstrap", installed)
            project = Path(temporary) / "project"
            project.mkdir()
            scaffold = installed / "standard/tools/jinx_context_scaffold.py"
            created = subprocess.run(
                [sys.executable, str(scaffold), "--root", str(project)],
                capture_output=True,
                text=True,
                check=False,
                cwd=temporary,
            )
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            self.assertTrue((project / "docs/_meta/manifest.json").is_file())


def _digest(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): path.read_text(encoding="utf-8", errors="replace")
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


if __name__ == "__main__":
    unittest.main()
