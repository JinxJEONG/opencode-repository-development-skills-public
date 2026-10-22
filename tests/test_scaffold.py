"""Scaffold behavior: create-only, idempotent, blocking, and semantically empty."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from support import (  # noqa: E402
    CHECKER,
    MANIFEST,
    SCAFFOLD,
    copy_fixture,
    run,
    statuses,
    tree_snapshot,
)


class FreshRepository(unittest.TestCase):
    def test_scaffold_output_passes_every_structural_check(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "fresh"
            root.mkdir()
            created = run(SCAFFOLD, "--root", str(root))
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            checked = run(CHECKER, "--root", str(root))
            self.assertEqual(checked.returncode, 0, checked.stdout)
            parsed = statuses(checked.stdout)
            self.assertNotIn("FAIL", set(parsed.values()), checked.stdout)
            self.assertNotIn("BLOCKED", set(parsed.values()), checked.stdout)

    def test_a_structural_pass_is_not_reported_as_readiness(self) -> None:
        # Replaces the blocked-audit assertion: the scaffold's placeholders are unfilled, so the
        # report must say what a clean structural run does and does not establish.
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "fresh"
            root.mkdir()
            run(SCAFFOLD, "--root", str(root))
            checked = run(CHECKER, "--root", str(root))
            self.assertIn("scope: static structure only", checked.stdout)
            self.assertIn("does not establish", checked.stdout)
            self.assertIn("<exact command>", (root / "docs/project.md").read_text(encoding="utf-8"))

    def test_second_run_changes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "fresh"
            root.mkdir()
            run(SCAFFOLD, "--root", str(root))
            before = tree_snapshot(root)
            second = run(SCAFFOLD, "--root", str(root))
            after = tree_snapshot(root)
            self.assertEqual(before, after)
            self.assertIn("created=0", second.stdout)
            self.assertNotIn("create ", second.stdout)

    def test_dry_run_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "fresh"
            root.mkdir()
            result = run(SCAFFOLD, "--root", str(root), "--dry-run")
            self.assertEqual(result.returncode, 0)
            self.assertIn("dry-run", result.stdout)
            self.assertEqual(tree_snapshot(root), {})
            self.assertEqual(list(root.iterdir()), [])

    def test_manifest_declares_only_paths_that_exist(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "fresh"
            root.mkdir()
            run(SCAFFOLD, "--root", str(root), "--targets", "codex,opencode")
            manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
            for path in manifest["managedPaths"].values():
                with self.subTest(path=path):
                    self.assertTrue((root / path).exists())
            self.assertNotIn("kiroSteering", manifest["managedPaths"])

    def test_no_placeholder_documents_are_created_beyond_the_core_docs(self) -> None:
        # Replaces the declared-category assertion: with no category state to consult, the property
        # is simply that only the core documents exist.
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "fresh"
            root.mkdir()
            run(SCAFFOLD, "--root", str(root))
            created = sorted(
                str(path.relative_to(root)) for path in (root / "docs").rglob("*.md")
            )
            self.assertEqual(
                created,
                [
                    "docs/README.md",
                    "docs/architecture/overview.md",
                    "docs/plans/README.md",
                    "docs/project.md",
                ],
            )

    def test_scaffold_invents_no_commands_or_architecture(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "fresh"
            root.mkdir()
            run(SCAFFOLD, "--root", str(root))
            project = (root / "docs/project.md").read_text(encoding="utf-8")
            # Placeholders stay placeholders: no concrete command is asserted for the target.
            self.assertIn("<exact command>", project)
            self.assertIn("Needs verification", project)


class ExistingContent(unittest.TestCase):
    def test_existing_files_are_kept_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = copy_fixture("legacy-project", Path(temporary))
            before = tree_snapshot(root)
            result = run(SCAFFOLD, "--root", str(root))
            after = tree_snapshot(root)
            self.assertEqual(result.returncode, 0, result.stdout)
            for path, content in before.items():
                with self.subTest(path=path):
                    self.assertEqual(after[path], content)

    def test_established_nested_bridge_is_not_duplicated(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = copy_fixture("legacy-project", Path(temporary))
            run(SCAFFOLD, "--root", str(root))
            self.assertFalse((root / "CLAUDE.md").exists())
            checked = run(CHECKER, "--root", str(root))
            self.assertEqual(statuses(checked.stdout)["claude-bridge"], "PASS")

    def test_dirty_router_content_survives_and_is_reported_kept(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = copy_fixture("legacy-project", Path(temporary))
            result = run(SCAFFOLD, "--root", str(root))
            self.assertIn("keep  AGENTS.md", result.stdout)
            self.assertIn("vendor/generated_client.py", (root / "AGENTS.md").read_text(encoding="utf-8"))


class Blocking(unittest.TestCase):
    def test_published_docs_root_blocks_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "site"
            (root / "docs").mkdir(parents=True)
            (root / "docs/_config.yml").write_text("theme: minima\n", encoding="utf-8")
            before = tree_snapshot(root)
            result = run(SCAFFOLD, "--root", str(root))
            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertIn("BLOCKED", result.stdout)
            self.assertEqual(tree_snapshot(root), before)

    def test_blocked_run_does_not_redirect_to_another_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "site"
            (root / "docs").mkdir(parents=True)
            (root / "docs/.nojekyll").write_text("", encoding="utf-8")
            run(SCAFFOLD, "--root", str(root))
            siblings = [path for path in Path(temporary).iterdir() if path != root]
            self.assertEqual(siblings, [])


class CliContract(unittest.TestCase):
    def test_help_states_create_only_behavior(self) -> None:
        result = run(SCAFFOLD, "--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Existing files are kept untouched", result.stdout)

    def test_unknown_target_is_a_usage_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = run(SCAFFOLD, "--root", temporary, "--targets", "cursor")
        self.assertEqual(result.returncode, 64)

    def test_missing_root_is_a_usage_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = run(SCAFFOLD, "--root", str(Path(temporary) / "absent"))
        self.assertEqual(result.returncode, 64)


if __name__ == "__main__":
    unittest.main()
