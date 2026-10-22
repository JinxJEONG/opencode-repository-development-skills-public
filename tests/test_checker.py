"""Checker behavior against the fixture repositories."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from support import CHECKER, FIXTURES, STANDARD_DIR, run, statuses  # noqa: E402


class CompliantProject(unittest.TestCase):
    def test_no_check_fails_and_the_process_reports_success(self) -> None:
        # Given a repository that satisfies the standard
        # When the checker runs in project mode
        result = run(CHECKER, "--root", str(FIXTURES / "compliant-project"))
        # Then nothing fails and no check reports a status it cannot establish
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        parsed = statuses(result.stdout)
        self.assertEqual(sorted(set(parsed.values())), ["NOT_APPLICABLE", "PASS"], result.stdout)
        self.assertGreaterEqual(len(parsed), 15)

    def test_every_report_states_its_own_scope(self) -> None:
        # Given any run, the output must not read as a readiness claim
        result = run(CHECKER, "--root", str(FIXTURES / "compliant-project"))

        self.assertIn("scope: static structure only", result.stdout)
        self.assertIn("does not establish", result.stdout)

    def test_repeated_runs_are_byte_identical(self) -> None:
        first = run(CHECKER, "--root", str(FIXTURES / "compliant-project"))
        second = run(CHECKER, "--root", str(FIXTURES / "compliant-project"))
        self.assertEqual(first.stdout, second.stdout)

    def test_json_output_carries_sorted_results_and_the_scope(self) -> None:
        result = run(CHECKER, "--root", str(FIXTURES / "compliant-project"), "--format", "json")
        payload = json.loads(result.stdout)
        ids = [item["check"] for item in payload["results"]]
        self.assertEqual(ids, sorted(ids))
        self.assertNotIn("FAIL", {item["status"] for item in payload["results"]})
        self.assertIn("static structure only", payload["scope"])

    def test_checker_writes_nothing(self) -> None:
        project = FIXTURES / "compliant-project"
        before = {
            str(path.relative_to(project)): path.read_text(encoding="utf-8")
            for path in sorted(project.rglob("*"))
            if path.is_file()
        }
        run(CHECKER, "--root", str(project))
        after = {
            str(path.relative_to(project)): path.read_text(encoding="utf-8")
            for path in sorted(project.rglob("*"))
            if path.is_file()
        }
        self.assertEqual(before, after)


class BrokenProject(unittest.TestCase):
    def setUp(self) -> None:
        self.result = run(CHECKER, "--root", str(FIXTURES / "broken-project"))
        self.statuses = statuses(self.result.stdout)

    def test_exit_code_reports_failure(self) -> None:
        self.assertEqual(self.result.returncode, 1, self.result.stdout)

    def test_named_defects_each_fail(self) -> None:
        for check in (
            "agents-routing",
            "anchors-resolve",
            "archive-no-discovery",
            "bridge-no-cycle",
            "claude-bridge",
            "docs-core",
            "kiro-steering",
            "links-resolve",
            "manifest-managed-paths",
            "manifest-schema",
            "manifest-version",
            "plans-unique",
        ):
            with self.subTest(check=check):
                self.assertEqual(self.statuses.get(check), "FAIL")

    def test_failures_name_the_offending_path(self) -> None:
        self.assertIn("docs/archive/AGENTS.md", self.result.stdout)
        self.assertIn("docs/guides/missing.md", self.result.stdout)
        self.assertIn("dupe.md", self.result.stdout)
        self.assertIn("generatedAt", self.result.stdout)

    def test_version_mismatch_names_both_versions(self) -> None:
        acting = (STANDARD_DIR / "VERSION").read_text(encoding="utf-8").strip()
        self.assertNotEqual(acting, "0.9.0", "the fixture must declare a stale version")
        line = next(line for line in self.result.stdout.splitlines() if "manifest-version" in line)
        self.assertIn("0.9.0", line)
        self.assertIn(acting, line)


class MissingContext(unittest.TestCase):
    def test_no_context_blocks_instead_of_failing(self) -> None:
        # Given a plan-only repository with no context standard
        result = run(CHECKER, "--root", str(FIXTURES / "plan-only-project"))
        # Then the checker blocks, names the handoff, and never claims a pass
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("BLOCKED", result.stdout)
        self.assertIn("jinx-bootstrap", result.stdout)
        self.assertNotIn("PASS ", result.stdout)


class LegacyProject(unittest.TestCase):
    def test_established_nested_bridge_is_accepted(self) -> None:
        result = run(CHECKER, "--root", str(FIXTURES / "legacy-project"))
        parsed = statuses(result.stdout)
        self.assertEqual(parsed["claude-bridge"], "PASS")
        self.assertIn(".claude/CLAUDE.md", result.stdout)

    def test_missing_standard_structure_still_fails(self) -> None:
        result = run(CHECKER, "--root", str(FIXTURES / "legacy-project"))
        parsed = statuses(result.stdout)
        self.assertEqual(parsed["docs-core"], "FAIL")
        self.assertEqual(parsed["manifest-present"], "FAIL")
        self.assertEqual(result.returncode, 1)


class TargetNarrowing(unittest.TestCase):
    def test_narrowing_marks_not_applicable_without_hiding_failures(self) -> None:
        result = run(
            CHECKER, "--root", str(FIXTURES / "legacy-project"), "--targets", "codex,opencode"
        )
        parsed = statuses(result.stdout)
        self.assertEqual(parsed["claude-bridge"], "NOT_APPLICABLE")
        self.assertEqual(parsed["kiro-steering"], "NOT_APPLICABLE")
        self.assertEqual(parsed["docs-core"], "FAIL")
        self.assertEqual(result.returncode, 1)


class CliContract(unittest.TestCase):
    def test_help_describes_modes_and_exit_codes(self) -> None:
        result = run(CHECKER, "--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("--mode", result.stdout)
        self.assertIn("exit codes", result.stdout)

    def test_unknown_target_is_a_usage_error(self) -> None:
        result = run(CHECKER, "--root", str(FIXTURES / "compliant-project"), "--targets", "cursor")
        self.assertEqual(result.returncode, 64)
        self.assertIn("unknown --targets", result.stdout + result.stderr)

    def test_missing_root_is_a_usage_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            absent = Path(temporary) / "absent"
            result = run(CHECKER, "--root", str(absent))
        self.assertEqual(result.returncode, 64)

    def test_package_flag_rejected_in_project_mode(self) -> None:
        result = run(CHECKER, "--root", ".", "--package", "skills/jinx-bootstrap")
        self.assertEqual(result.returncode, 64)

    def test_package_mode_requires_a_package(self) -> None:
        result = run(CHECKER, "--mode", "package", "--root", ".")
        self.assertEqual(result.returncode, 64)

    def test_invalid_mode_is_a_usage_error(self) -> None:
        result = run(CHECKER, "--mode", "galaxy")
        self.assertEqual(result.returncode, 64)


if __name__ == "__main__":
    unittest.main()
