"""What version 1.2.0 deliberately stopped requiring, and what replaced it.

Each case here replaces a removed coverage-ledger assertion. The old suite proved that an
unaudited-but-structurally-clean project was blocked by a per-row ledger; these prove the same
honesty property without that machinery — the report never claims more than file shapes, a
persisted ledger is read as history instead of validated, and a judgement call is reported rather
than failed.
"""

from __future__ import annotations

import json
import shutil
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from support import (  # noqa: E402
    CHECKER,
    LEGACY_LEDGER,
    MANIFEST,
    SCAFFOLD,
    STANDARD_DIR,
    append,
    compliant_fixture,
    legacy_fixture,
    run,
    scaffolded_project,
    statuses,
    tree_snapshot,
)


class LedgerIsOptionalHistoryNotARequirement(unittest.TestCase):
    """Replaces every `ledger-present` / `ledger-schema` / `ledger-coverage-audit` assertion.

    Those checks failed or blocked a project over a ledger file. A ledger is now input an agent may
    read, so the checks that consumed it are gone and the file is only reported.
    """

    def test_a_project_without_a_ledger_needs_nothing_more(self) -> None:
        with compliant_fixture() as root:
            result = run(CHECKER, "--root", str(root))

            parsed = statuses(result.stdout)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(parsed["legacy-ledger"], "NOT_APPLICABLE")
            self.assertIn("none is required", result.stdout)

    def test_no_ledger_check_id_is_reported_any_more(self) -> None:
        with legacy_fixture() as root:
            result = run(CHECKER, "--root", str(root))

            removed = sorted(
                check
                for check in statuses(result.stdout)
                if check.startswith("ledger-") or check == "manifest-category-state"
            )
            self.assertEqual(removed, [], result.stdout)

    def test_a_persisted_ledger_is_reported_as_readable_history(self) -> None:
        with legacy_fixture() as root:
            result = run(CHECKER, "--root", str(root))

            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(statuses(result.stdout)["legacy-ledger"], "PASS")
            self.assertIn("optional historical input", result.stdout)
            self.assertIn("neither validates nor modifies it", result.stdout)

    def test_a_malformed_persisted_ledger_does_not_fail_the_run(self) -> None:
        # Given a ledger no schema check reads any more
        with legacy_fixture() as root:
            (root / LEGACY_LEDGER).write_text("{ not json at all\n", encoding="utf-8")

            result = run(CHECKER, "--root", str(root))

            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_neither_tool_writes_or_removes_a_persisted_ledger(self) -> None:
        # A user's audit record is never rewritten by tooling on their behalf.
        with legacy_fixture() as root:
            before = tree_snapshot(root)

            checked = run(CHECKER, "--root", str(root))
            scaffolded = run(SCAFFOLD, "--root", str(root))

            self.assertEqual(checked.returncode, 0, checked.stdout)
            self.assertEqual(scaffolded.returncode, 0, scaffolded.stdout)
            self.assertEqual(tree_snapshot(root), before)

    def test_the_scaffold_creates_no_ledger(self) -> None:
        with scaffolded_project() as root:
            self.assertFalse((root / LEGACY_LEDGER).exists())
            self.assertEqual(run(CHECKER, "--root", str(root)).returncode, 0)


class ManifestNeedsOnlyItsVersion(unittest.TestCase):
    """Replaces the `manifest-category-state` and full-schema assertions."""

    def test_the_scaffolded_manifest_carries_the_version_and_managed_paths_only(self) -> None:
        with scaffolded_project() as root:
            manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))

            self.assertEqual(sorted(manifest), ["managedPaths", "standardVersion"])

    def test_a_manifest_with_only_the_version_passes(self) -> None:
        with compliant_fixture() as root:
            version = (STANDARD_DIR / "VERSION").read_text(encoding="utf-8").strip()
            (root / MANIFEST).write_text(
                json.dumps({"standardVersion": version}) + "\n", encoding="utf-8"
            )

            result = run(CHECKER, "--root", str(root))

            parsed = statuses(result.stdout)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(parsed["manifest-schema"], "PASS")
            self.assertEqual(parsed["manifest-managed-paths"], "NOT_APPLICABLE")

    def test_the_persisted_rich_shape_passes_and_its_extra_keys_are_named(self) -> None:
        # Given a manifest still carrying the 1.1 `categories` map
        with legacy_fixture() as root:
            self.assertIn("categories", json.loads((root / MANIFEST).read_text(encoding="utf-8")))

            result = run(CHECKER, "--root", str(root))

            self.assertEqual(statuses(result.stdout)["manifest-schema"], "PASS", result.stdout)
            self.assertIn("keys carried but not required: categories", result.stdout)

    def test_a_stale_category_state_no_longer_contradicts_anything(self) -> None:
        # The 1.1 checker failed when `specs: declared` held documents. Nothing reads it now.
        with legacy_fixture() as root:
            manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
            self.assertEqual(manifest["categories"]["specs"], "declared")
            specs = root / "docs/specs"
            specs.mkdir(parents=True, exist_ok=True)
            (specs / "widget.md").write_text("# Widget\n\nA real document.\n", encoding="utf-8")

            result = run(CHECKER, "--root", str(root))

            self.assertEqual(result.returncode, 0, result.stdout)

    def test_a_missing_version_still_fails(self) -> None:
        with compliant_fixture() as root:
            (root / MANIFEST).write_text(json.dumps({"managedPaths": {}}) + "\n", encoding="utf-8")

            result = run(CHECKER, "--root", str(root))

            parsed = statuses(result.stdout)
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertEqual(parsed["manifest-schema"], "FAIL")
            self.assertEqual(parsed["manifest-version"], "FAIL")


class SizeAndStructureAreReportedNotFailed(unittest.TestCase):
    """Replaces `agents-size`, `managed-surface-budget`, and the `docs-taxonomy` failure.

    Each used to fail a run over a judgement call, which pressured an agent into deleting a rule or
    renaming a directory to clear a gate. They now report the measurement.
    """

    def test_an_oversized_router_reports_the_goal_without_failing(self) -> None:
        with compliant_fixture() as root:
            append(root / "AGENTS.md", "\n" + "\n".join(f"- rule {n}" for n in range(400)) + "\n")

            result = run(CHECKER, "--root", str(root))

            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(statuses(result.stdout)["surface-size"], "PASS")
            self.assertIn("above its ~100-line goal", result.stdout)
            self.assertIn("never dropping a rule", result.stdout)

    def test_the_surface_report_names_what_it_counted_and_excluded(self) -> None:
        with compliant_fixture() as root:
            line = next(
                line
                for line in run(CHECKER, "--root", str(root)).stdout.splitlines()
                if "surface-size" in line
            )

            self.assertIn("AGENTS.md=", line)
            self.assertIn("absent .claude/CLAUDE.md", line)
            self.assertIn("not counted: nested AGENTS.md files below the root", line)

    def test_a_nested_agents_file_does_not_change_the_count(self) -> None:
        with compliant_fixture() as root:
            before = run(CHECKER, "--root", str(root)).stdout
            nested = root / "src/AGENTS.md"
            nested.write_text("# Local rules\n\n" + "\n".join(["- x"] * 200) + "\n", encoding="utf-8")

            self.assertEqual(run(CHECKER, "--root", str(root)).stdout, before)

    def test_an_unrecognized_docs_directory_is_reported_as_scope(self) -> None:
        with compliant_fixture() as root:
            notes = root / "docs/adr"
            notes.mkdir()
            (notes / "0001.md").write_text("# ADR 1\n\nA record.\n", encoding="utf-8")

            result = run(CHECKER, "--root", str(root))

            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(statuses(result.stdout)["docs-structure"], "PASS")
            self.assertIn("directories outside the recommended names", result.stdout)
            self.assertIn("adr", result.stdout)

    def test_a_missing_docs_root_still_fails(self) -> None:
        with compliant_fixture() as root:
            shutil.rmtree(root / "docs")

            result = run(CHECKER, "--root", str(root))

            self.assertEqual(statuses(result.stdout)["docs-structure"], "FAIL", result.stdout)
            self.assertEqual(result.returncode, 1, result.stdout)


if __name__ == "__main__":
    unittest.main()
