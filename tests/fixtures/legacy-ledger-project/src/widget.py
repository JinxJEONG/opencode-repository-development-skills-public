"""Fixture application code. Migration must not absorb it into docs/."""


def list_widgets() -> list[dict[str, str]]:
    return [{"id": "w-1", "name": "first"}]
