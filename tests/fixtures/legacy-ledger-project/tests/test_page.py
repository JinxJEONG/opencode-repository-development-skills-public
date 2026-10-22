"""Fixture consumer that binds DESIGN.md in place by reading it by path."""

from pathlib import Path


def test_design_tokens_are_declared() -> None:
    design = (Path(__file__).parents[1] / "DESIGN.md").read_text(encoding="utf-8")
    assert "--widget-gutter" in design
