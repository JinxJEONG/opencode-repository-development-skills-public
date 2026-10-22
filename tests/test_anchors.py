"""Anchor resolution: a fragment must reach a heading the target document really declares.

The reproduced defect: `anchors-resolve` stripped every non-ASCII character before slugging, so a
Korean heading produced an empty slug and every link to it failed. A repository documented in Korean
could not clear the check without romanizing its headings. These cases pin the three anchor sources
the checker now accepts, and the failure it must still report.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from support import CHECKER, append, compliant_fixture, run, statuses  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "standard" / "tools"))

from jinxcontext.markdown import heading_anchors, slugify  # noqa: E402

# Headings observed in a real Korean-language planning repository.
KOREAN_HEADINGS = {
    "9. API 설계 (FastAPI)": "9-api-설계-fastapi",
    "T-603. 웹 UI": "t-603-웹-ui",
    "9.6 바인딩과 서비스 소유권": "96-바인딩과-서비스-소유권",
}


class UnicodeHeadingsSlugCorrectly(unittest.TestCase):
    def test_each_korean_heading_keeps_its_letters(self) -> None:
        for heading, expected in KOREAN_HEADINGS.items():
            with self.subTest(heading=heading):
                self.assertEqual(slugify(heading), expected)

    def test_a_korean_heading_never_slugs_to_nothing(self) -> None:
        # The pre-fix behavior: every character dropped, so the slug was "" and no link resolved.
        for heading in KOREAN_HEADINGS:
            with self.subTest(heading=heading):
                self.assertTrue(slugify(heading))

    def test_ascii_slugging_is_unchanged(self) -> None:
        self.assertEqual(slugify("Canonical Commands"), "canonical-commands")
        self.assertEqual(slugify("`code` and *emphasis*"), "code-and-emphasis")


class AnchorSources(unittest.TestCase):
    def test_a_repeated_heading_gets_numbered_anchors_in_document_order(self) -> None:
        anchors = heading_anchors("# Same\n\n# Same\n\n# Same\n")

        self.assertEqual(sorted(anchors), ["same", "same-1", "same-2"])

    def test_an_explicit_html_id_or_name_is_an_anchor(self) -> None:
        anchors = heading_anchors('<a id="owner-table"></a>\n\n# Owners\n\n<span name="legacy">\n')

        self.assertIn("owner-table", anchors)
        self.assertIn("legacy", anchors)

    def test_a_brace_suffix_declares_an_anchor_and_leaves_the_slug_clean(self) -> None:
        anchors = heading_anchors("## Deployment {#deploy}\n")

        self.assertIn("deploy", anchors)
        self.assertIn("deployment", anchors)

    def test_a_heading_inside_a_fenced_block_is_not_an_anchor(self) -> None:
        anchors = heading_anchors("# Real\n\n```md\n# Illustration\n```\n")

        self.assertEqual(sorted(anchors), ["real"])


class CodeDoesNotDeclareAnExplicitAnchor(unittest.TestCase):
    """An explicit anchor shown inside code is an illustration, not markup the document emits.

    Documentation about anchors quotes them in prose. Counting a quoted one let a link to a fragment
    that does not exist report PASS, purely because some file explained the syntax.
    """

    def test_an_html_attribute_inside_an_inline_code_span_is_not_an_anchor(self) -> None:
        anchors = heading_anchors('Never write `<span id="not-an-anchor">` in a heading.\n')

        self.assertNotIn("not-an-anchor", anchors)

    def test_a_brace_suffix_inside_an_inline_code_span_is_not_an_anchor(self) -> None:
        anchors = heading_anchors("Declare one with `{#not-an-anchor}` after the heading.\n")

        self.assertNotIn("not-an-anchor", anchors)

    def test_an_attribute_inside_a_fenced_block_is_not_an_anchor(self) -> None:
        anchors = heading_anchors('# Real\n\n```html\n<a id="not-an-anchor"></a>\n```\n')

        self.assertEqual(sorted(anchors), ["real"])

    def test_a_real_attribute_beside_a_quoted_one_still_counts(self) -> None:
        # The stricter read must not cost a genuine declaration on a nearby line.
        anchors = heading_anchors('<a id="real"></a>\n\nShown only as syntax: `<a id="quoted">`.\n')

        self.assertIn("real", anchors)
        self.assertNotIn("quoted", anchors)

    def test_a_headings_inline_code_is_still_part_of_its_slug(self) -> None:
        # Headings strip fences only: blanking the span would drop the words the slug is built from.
        self.assertEqual(sorted(heading_anchors("## The `surface-size` check\n")), ["the-surface-size-check"])
        self.assertEqual(sorted(heading_anchors("## `docs/` layout\n")), ["docs-layout"])


class AnchorsResolveEndToEnd(unittest.TestCase):
    def test_the_fixture_resolves_korean_literal_percent_encoded_and_explicit_anchors(self) -> None:
        # The fixture index links each shape; a regression in any of them fails the whole check.
        with compliant_fixture() as root:
            result = run(CHECKER, "--root", str(root))

            self.assertEqual(statuses(result.stdout)["anchors-resolve"], "PASS", result.stdout)
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_a_korean_fragment_with_no_matching_heading_still_fails(self) -> None:
        with compliant_fixture() as root:
            append(
                root / "docs/README.md",
                "\n- [없는 제목](architecture/overview.md#존재하지-않는-제목)\n",
            )

            result = run(CHECKER, "--root", str(root))

            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertEqual(statuses(result.stdout)["anchors-resolve"], "FAIL")
            self.assertIn("존재하지-않는-제목", result.stdout)


if __name__ == "__main__":
    unittest.main()
