"""Scaffold write-path regressions: a blocking collision must leave zero writes behind.

Every scaffold case asserts the resulting tree, not only the exit code. A preflight that reports a
collision and then writes half the structure anyway is the defect these tests pin. Checker read-path
regressions live in `test_checker_regressions.py`.
"""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from support import (  # noqa: E402
    SCAFFOLD,
    STANDARD_DIR,
    run,
    scaffolded_project,
    tree_snapshot,
)


@contextmanager
def damaged_standard(
    remove: str | None = None, unreadable: str | None = None
) -> Iterator[tuple[Path, Path]]:
    with tempfile.TemporaryDirectory() as temporary:
        base = Path(temporary)
        standard = base / "standard"
        shutil.copytree(STANDARD_DIR, standard)
        if remove:
            (standard / "templates" / remove).unlink()
        if unreadable:
            (standard / "templates" / unreadable).chmod(0o000)
        root = base / "project"
        root.mkdir()
        try:
            yield standard / "tools/jinx_context_scaffold.py", root
        finally:
            if unreadable:
                (standard / "templates" / unreadable).chmod(0o644)


class ScaffoldCollisionPreflight(unittest.TestCase):
    """Defect 1: destinations and templates were not preflighted, so writes escaped or half-applied."""

    def test_docs_symlink_to_outside_blocks_with_zero_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            outside = Path(temporary) / "outside"
            outside.mkdir()
            root = Path(temporary) / "project"
            root.mkdir()
            (root / "docs").symlink_to(outside)

            result = run(SCAFFOLD, "--root", str(root))

            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertIn("symlink", result.stdout)
            self.assertEqual(tree_snapshot(outside), {})
            self.assertEqual(tree_snapshot(root), {})

    def test_symlinked_destination_file_blocks_without_overwriting_its_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            elsewhere = Path(temporary) / "elsewhere.md"
            elsewhere.write_text("owned by someone else\n", encoding="utf-8")
            root = Path(temporary) / "project"
            root.mkdir()
            (root / "AGENTS.md").symlink_to(elsewhere)

            result = run(SCAFFOLD, "--root", str(root))

            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertEqual(elsewhere.read_text(encoding="utf-8"), "owned by someone else\n")

    def test_file_where_a_directory_must_go_blocks_before_any_write(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project"
            (root / "docs").mkdir(parents=True)
            (root / "docs/architecture").write_text("a file, not a directory\n", encoding="utf-8")
            before = tree_snapshot(root)

            result = run(SCAFFOLD, "--root", str(root))

            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertIn("docs/architecture", result.stdout)
            self.assertEqual(tree_snapshot(root), before)

    def test_unreadable_template_blocks_instead_of_writing_an_empty_file(self) -> None:
        with damaged_standard(unreadable="project.template.md") as (scaffold, root):
            result = run(scaffold, "--root", str(root))

            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertIn("unreadable template project.template.md", result.stdout)
            self.assertEqual(tree_snapshot(root), {})

    def test_missing_template_blocks_instead_of_writing_an_empty_file(self) -> None:
        with damaged_standard(remove="docs-readme.template.md") as (scaffold, root):
            result = run(scaffold, "--root", str(root))

            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertIn("missing template docs-readme.template.md", result.stdout)
            self.assertEqual(tree_snapshot(root), {})

    def test_healthy_root_still_scaffolds_non_empty_files(self) -> None:
        with scaffolded_project() as root:
            for path in ("AGENTS.md", "docs/README.md", "docs/project.md", "docs/_meta/manifest.json"):
                with self.subTest(path=path):
                    self.assertGreater((root / path).stat().st_size, 0)


class DestinationTypeCollision(unittest.TestCase):
    """A directory sitting where the standard requires a file must block, not be reported `keep`."""

    def test_directory_at_the_root_router_blocks_with_zero_writes(self) -> None:
        self._assert_blocked("AGENTS.md")

    def test_directory_at_a_core_doc_blocks_with_zero_writes(self) -> None:
        self._assert_blocked("docs/project.md")

    def test_directory_at_the_manifest_blocks_with_zero_writes(self) -> None:
        self._assert_blocked("docs/_meta/manifest.json")

    def _assert_blocked(self, path: str) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project"
            (root / path).mkdir(parents=True)
            before = tree_snapshot(root)

            result = run(SCAFFOLD, "--root", str(root))

            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertIn("exists as a directory", result.stdout)
            self.assertIn(path, result.stdout)
            self.assertEqual(tree_snapshot(root), before)


class PublishedSiteRoot(unittest.TestCase):
    """A published documentation site must block before `docs/` is touched."""

    def test_each_root_marker_blocks(self) -> None:
        for marker in ("mkdocs.yml", "docusaurus.config.js", "docusaurus.config.ts"):
            with self.subTest(marker=marker), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary) / "site"
                root.mkdir()
                (root / marker).write_text("", encoding="utf-8")

                result = run(SCAFFOLD, "--root", str(root))

                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertIn(marker, result.stdout)
                self.assertFalse((root / "docs").exists())
                self.assertFalse((root / "AGENTS.md").exists())

    def test_docs_level_marker_still_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "site"
            (root / "docs").mkdir(parents=True)
            (root / "docs/_config.yml").write_text("theme: minima\n", encoding="utf-8")
            before = tree_snapshot(root)

            result = run(SCAFFOLD, "--root", str(root))

            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertEqual(tree_snapshot(root), before)


class ApplicationFailureIsHonest(unittest.TestCase):
    """A write that fails after the preflight must not be reported as success."""

    def test_unwritable_destination_reports_blocked_and_the_partial_list(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project"
            docs = root / "docs"
            docs.mkdir(parents=True)
            docs.chmod(0o500)
            try:
                result = run(SCAFFOLD, "--root", str(root))
            finally:
                docs.chmod(0o755)

            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertIn("BLOCKED  docs/project.md: PermissionError", result.stdout)
            self.assertIn("BLOCKED  docs/_meta/manifest.json: PermissionError", result.stdout)
            self.assertIn("created before blocking:", result.stdout)
            self.assertIn("blocked=9", result.stdout)
            self.assertFalse((root / "docs/project.md").exists())
            self.assertFalse((root / "docs/_meta/manifest.json").exists())

    def test_template_disappearing_after_preflight_is_reported(self) -> None:
        sys.path.insert(0, str(STANDARD_DIR / "tools"))
        from jinxcontext import scaffold  # noqa: PLC0415
        from jinxcontext.scaffold_plan import ScaffoldRequest, plan  # noqa: PLC0415

        with tempfile.TemporaryDirectory() as temporary:
            standard = Path(temporary) / "standard"
            shutil.copytree(STANDARD_DIR, standard)
            root = Path(temporary) / "project"
            root.mkdir()
            request = ScaffoldRequest(
                root=root,
                templates=standard / "templates",
                targets=("codex", "claude", "kiro", "opencode"),
                version=(standard / "VERSION").read_text(encoding="utf-8").strip(),
            )
            actions = plan(request)
            (standard / "templates/project.template.md").unlink()

            created, failures = scaffold._apply(request, actions)

            self.assertEqual([path for path, _ in failures], ["docs/project.md"])
            self.assertNotIn("docs/project.md", created)
            self.assertFalse((root / "docs/project.md").exists())

    def test_successful_run_reports_zero_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project"
            root.mkdir()

            result = run(SCAFFOLD, "--root", str(root))

            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("blocked=0", result.stdout)
            self.assertNotIn("BLOCKED", result.stdout)



if __name__ == "__main__":
    unittest.main()
