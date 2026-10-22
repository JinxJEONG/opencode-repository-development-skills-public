# Legacy Repository Guide

Scope: repository root. Written before the standard existed. Migration must preserve every unique
rule and decision below verbatim, and must not create a second Claude bridge: `.claude/CLAUDE.md`
is the established one.

## Unique Rules

- Never edit `vendor/generated_client.py`; regenerate it with the vendored generator instead.
- Release tags are cut by the release owner only. Agents must not create tags.

## Commands

- `bash scripts/check.sh` — declared here only; `Needs verification`.

## Notes

Longer notes live in `doc/notes.md`, which is not the standard documentation root.
