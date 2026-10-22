"""Markdown link, reference-definition, and heading-anchor extraction."""

from __future__ import annotations

import re
from dataclasses import dataclass

_INLINE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
_DEFINITION = re.compile(r"^ {0,3}\[([^\]]+)\]:[ \t]*<?([^>\s]+)>?", re.MULTILINE)
_REFERENCE = re.compile(r"(?<!!)\[([^\]]*)\]\[([^\]]*)\]")
_HEADING = re.compile(r"^ {0,3}#{1,6}\s+(.*?)\s*$", re.MULTILINE)
# Anything that is not a word character, whitespace, or hyphen is dropped. `\w` is Unicode-aware,
# so Korean, Japanese, Cyrillic, and accented headings keep their letters instead of slugging to "".
_ANCHOR_STRIP = re.compile(r"[^\w\s-]", re.UNICODE)
_EXPLICIT_ATTRIBUTE = re.compile(r"<[^>]*\b(?:id|name)\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)
_EXPLICIT_BRACE = re.compile(r"\{#([^}\s]+)\}")
_FENCE = re.compile(r"^(?: {0,3})(?:```|~~~).*?^(?: {0,3})(?:```|~~~)[ \t]*$", re.MULTILINE | re.DOTALL)
_CODE_SPAN = re.compile(r"(`+)(?:(?!\1).)*?\1", re.DOTALL)
_EXTERNAL = ("http://", "https://", "mailto:", "//")


@dataclass(frozen=True)
class MarkdownLinks:
    """Link targets that must resolve, plus reference usages that cannot be resolved at all."""

    targets: tuple[str, ...]
    undefined_labels: tuple[str, ...]


def markdown_links(source: str) -> MarkdownLinks:
    """Inline links, reference-definition targets, and undefined reference labels.

    A reference definition (`[label]: path`) is a link the document makes, so its target is
    validated even when only shortcut syntax uses it. A `[text][label]` usage whose label has no
    definition cannot be resolved, and is reported rather than silently ignored. Fenced blocks and
    code spans are illustrations, not links the document makes, so they are stripped first.
    """
    text = strip_code(source)
    definitions = {label.strip().lower(): target for label, target in _DEFINITION.findall(text)}
    targets = [target for target in _INLINE.findall(text) if _is_relative(target)]
    targets += [target for target in definitions.values() if _is_relative(target)]
    undefined = sorted(
        {
            f"[{text_part}][{label}]"
            for text_part, label in _REFERENCE.findall(text)
            if (label.strip() or text_part.strip()).lower() not in definitions
        }
    )
    return MarkdownLinks(targets=tuple(targets), undefined_labels=tuple(undefined))


def strip_code(text: str) -> str:
    """Blank out fenced blocks and inline code spans, preserving line count for messages."""
    return _CODE_SPAN.sub(lambda match: "\n" * match.group(0).count("\n"), strip_fences(text))


def strip_fences(text: str) -> str:
    """Blank out fenced blocks only, preserving line count.

    Headings use this rather than `strip_code`: a code span inside a heading is part of the text the
    slug is generated from, so blanking it would lose the words it holds.
    """
    return _FENCE.sub(lambda match: "\n" * match.group(0).count("\n"), text)


def _is_relative(target: str) -> bool:
    return bool(target) and not target.lower().startswith(_EXTERNAL)


def heading_anchors(text: str) -> set[str]:
    """Every fragment a link in this document can reach.

    Three sources, because all three are how a real document is linked: generated heading slugs,
    the `-1`/`-2` suffixes a repeated heading gets, and anchors the author declared explicitly with
    an HTML `id`/`name` attribute or a `{#custom}` suffix.

    The two reads strip different amounts of code, because code means different things to each. An
    explicit anchor is markup the document emits, so a fenced block *or* an inline code span holding
    one is showing it, not declaring it. A heading's inline code is part of its visible text, so only
    fences are stripped there — blanking the span would drop the words its slug is built from.
    """
    declarations = strip_code(text)
    anchors: set[str] = set(_EXPLICIT_ATTRIBUTE.findall(declarations))
    anchors.update(_EXPLICIT_BRACE.findall(declarations))
    seen: dict[str, int] = {}
    for match in _HEADING.finditer(strip_fences(text)):
        slug = slugify(match.group(1))
        if not slug:
            continue
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        anchors.add(slug if count == 0 else f"{slug}-{count}")
    return anchors


def slugify(heading: str) -> str:
    """The fragment a heading generates: lowercased, punctuation dropped, spaces hyphenated.

    Unicode letters survive, so a Korean heading resolves instead of collapsing to an empty slug.
    An explicit `{#custom}` suffix is not part of the generated text and is removed first.
    """
    text = _EXPLICIT_BRACE.sub("", heading).strip().lower()
    text = re.sub(r"`|\*|_", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = _ANCHOR_STRIP.sub("", text)
    return re.sub(r"\s+", "-", text).strip("-")
