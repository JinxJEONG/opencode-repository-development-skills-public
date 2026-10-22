"""Required skeleton directories: real CLI effects, safety, and preservation."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Literal, assert_never

sys.path.insert(0, str(Path(__file__).resolve().parent))

from support import (  # noqa: E402
    REQUIRED_DIRECTORIES,
    SCAFFOLD,
    STANDARD_DIR,
    copy_fixture,
    run,
)


def entries(root: Path) -> set[str]:
    """Include empty directories and dangling links in the observed tree."""
    return {str(path.relative_to(root)) for path in root.rglob("*")}


class RequiredSkeleton(unittest.TestCase):
    def test_plan_schedules_only_missing_directories_when_some_exist(self) -> None:
        sys.path.insert(0, str(STANDARD_DIR / "tools"))
        from jinxcontext.scaffold_plan import ScaffoldRequest, plan

        # Given a partial skeleton and a valid request
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "src").mkdir()
            request = ScaffoldRequest(root, STANDARD_DIR / "templates", ("codex",), "1.3.0")
            # When its actions are planned
            actions = plan(request)
            # Then directories are distinguished from files and existing ones are kept
            self.assertIn(("keep", "src"), actions)
            for directory in REQUIRED_DIRECTORIES[1:]:
                self.assertIn(("mkdir", directory), actions)
            self.assertIn(("create", "AGENTS.md"), actions)
            self.assertEqual(actions, sorted(actions, key=lambda item: item[1]))

    def test_required_directories_materialize_when_project_is_empty_or_plan_only(self) -> None:
        for fixture in (None, "plan-only-project"):
            with self.subTest(fixture=fixture), tempfile.TemporaryDirectory() as temporary:
                # Given an empty or plan-only project
                root = Path(temporary)
                if fixture:
                    root = copy_fixture(fixture, root)
                originals = {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}
                # When the public CLI establishes context
                result = run(SCAFFOLD, "--root", str(root))
                # Then all required directories exist without inferred application files
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                for directory in REQUIRED_DIRECTORIES:
                    self.assertTrue((root / directory).is_dir(), directory)
                for directory in ("src", "tests", "experiments", "outputs", "docs/specs",
                                  "docs/plans/active", "docs/plans/completed"):
                    self.assertEqual(list((root / directory).iterdir()), [])
                for path, body in originals.items():
                    self.assertEqual(path.read_bytes(), body)

    def test_dry_run_reports_directories_without_creating_any_entry(self) -> None:
        # Given an empty project
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            # When the CLI previews its plan
            result = run(SCAFFOLD, "--root", temporary, "--dry-run")
            # Then directory actions are visible but the filesystem remains empty
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for directory in REQUIRED_DIRECTORIES:
                self.assertIn(f"mkdir  {directory}\n", result.stdout)
            self.assertEqual(entries(root), set())
            self.assertIn("16 would be created", result.stdout)

    def test_repeat_preserves_directory_contents_native_bridges_and_configuration(self) -> None:
        # Given a populated skeleton with existing native bridges and configuration
        with tempfile.TemporaryDirectory() as temporary:
            root = copy_fixture("legacy-project", Path(temporary))
            for directory in REQUIRED_DIRECTORIES:
                target = root / directory
                target.mkdir(parents=True, exist_ok=True)
                (target / "owned.bin").write_bytes(b"\x00\xffkeep\x80")
            (root / "pyproject.toml").write_bytes(b"[project]\nname = 'existing'\n")
            first = run(SCAFFOLD, "--root", str(root))
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            before = entries(root)
            originals = {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}
            modified = {path: path.stat().st_mtime_ns for path in originals}
            # When the CLI repeats
            result = run(SCAFFOLD, "--root", str(root))
            # Then there are no new entries, overwritten bytes, or duplicated bridges
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("created=0", result.stdout)
            self.assertEqual(entries(root), before)
            for path, body in originals.items():
                self.assertEqual(path.read_bytes(), body)
                self.assertEqual(path.stat().st_mtime_ns, modified[path])
            self.assertFalse((root / "CLAUDE.md").exists())

    def test_directory_collisions_block_all_writes_when_present(self) -> None:
        collisions: tuple[Literal["file", "fifo", "symlink", "dangling-symlink"], ...] = (
            "file", "fifo", "symlink", "dangling-symlink",
        )
        for directory in (*REQUIRED_DIRECTORIES, "docs", "docs/plans"):
            for collision in collisions:
                with self.subTest(directory=directory, collision=collision):
                    with tempfile.TemporaryDirectory() as temporary:
                        # Given a collision at any required directory or its ancestor
                        base = Path(temporary)
                        root = base / "project"
                        root.mkdir()
                        outside = base / "outside"
                        outside.mkdir()
                        target = root / directory
                        target.parent.mkdir(parents=True, exist_ok=True)
                        match collision:
                            case "file":
                                target.write_bytes(b"existing directory collision")
                            case "fifo":
                                os.mkfifo(target)
                            case "symlink":
                                target.symlink_to(outside, target_is_directory=True)
                            case "dangling-symlink":
                                target.symlink_to(base / "absent", target_is_directory=True)
                            case unreachable:
                                assert_never(unreachable)
                        before = entries(root)
                        # When both actual and preview CLI runs encounter the collision
                        for args in ((), ("--dry-run",)):
                            result = run(SCAFFOLD, "--root", str(root), *args)
                            # Then neither project nor external destination receives any writes
                            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                            self.assertIn(directory, result.stdout)
                            self.assertEqual(entries(root), before)
                            self.assertEqual(entries(outside), set())
                            if collision == "file":
                                self.assertEqual(target.read_bytes(), b"existing directory collision")

    def test_current_standard_runs_standalone_when_copied_outside_repository(self) -> None:
        # Given an isolated copy of root tooling and its own templates/version
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            installed = base / "installed/standard"
            shutil.copytree(STANDARD_DIR, installed)
            root = base / "project"
            root.mkdir()
            # When it runs without repository or sibling package imports
            result = subprocess.run(
                [sys.executable, str(installed / "tools/jinx_context_scaffold.py"),
                 "--root", str(root)],
                cwd=temporary, capture_output=True, text=True, check=False,
            )
            # Then its required directories and version are still package-local
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for directory in REQUIRED_DIRECTORIES:
                self.assertTrue((root / directory).is_dir(), directory)

    def test_scaffold_imports_when_typing_has_no_python_311_assert_never(self) -> None:
        # Given the typing API available before Python 3.11
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            program = (
                "import sys, typing; typing.__dict__.pop('assert_never', None); "
                f"sys.path.insert(0, {str(STANDARD_DIR / 'tools')!r}); "
                "from jinxcontext.scaffold import main; from pathlib import Path; "
                f"raise SystemExit(main(['--root', {temporary!r}], "
                f"Path({str(STANDARD_DIR / 'tools')!r})))"
            )
            # When the scaffold loads and runs using only that API
            result = subprocess.run(
                [sys.executable, "-c", program], cwd=temporary,
                capture_output=True, text=True, check=False,
            )
            # Then the typed extension adds no new runtime import dependency
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for directory in REQUIRED_DIRECTORIES:
                self.assertTrue((root / directory).is_dir(), directory)


if __name__ == "__main__":
    unittest.main()
