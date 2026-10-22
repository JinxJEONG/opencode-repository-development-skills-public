# Widget Export

Status: `approved` (evidence: [../decisions](../README.md))

## Requirement

Operators can export the widget list as CSV.

## Acceptance Criteria

1. Given widgets exist, when the operator requests an export, then a CSV with a header row is returned.

## Implementation State

| Criterion | State | Evidence |
| --- | --- | --- |
| 1 | gap | no export handler in `src/widget.py` |

## Verification

| Criterion | Check | Result |
| --- | --- | --- |
| 1 | `python3 -m unittest discover tests` | `NOT_APPLICABLE` |
