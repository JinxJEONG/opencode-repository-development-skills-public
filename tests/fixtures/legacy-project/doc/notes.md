# Legacy Project Notes

Scope: repository root. This predates the standard: there is no `docs/` tree, no manifest, and no
Kiro steering. It carries unique rules that migration must preserve verbatim.

## Unique Rules

- Never edit `vendor/generated_client.py`; regenerate it with the vendored generator instead.
- Release tags are cut by the release owner only. Agents must not create tags.

## Decision History

- 2026-02: chose the vendored generator over a hand-written client. Still in force.
