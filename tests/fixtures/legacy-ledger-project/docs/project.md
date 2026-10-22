# Project

## Purpose And Scope

- Purpose: serve widget records over an internal HTTP API.
- In scope: widget read and export paths.
- Out of scope: billing.

## Implementation Status

| Area | State | Evidence |
| --- | --- | --- |
| Read path | `IMPLEMENTED` | `src/widget.py` |
| Export path | `PLAN_ONLY` | `README.md#usage` |

## Canonical Commands

| Purpose | Command | Defined in | State |
| --- | --- | --- | --- |
| Test | `python3 -m unittest discover tests` | `tests/` | verified |

## Requirements And Gaps

| Requirement | Spec | Implementation state |
| --- | --- | --- |
| Export returns CSV | `Not established` | gap |
