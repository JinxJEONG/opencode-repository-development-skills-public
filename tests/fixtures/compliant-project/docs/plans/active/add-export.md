# Add Export

Spec: [../../specs/widget-export.md](../../specs/widget-export.md) | Status: `active`

## Goal

Return a CSV export of the widget list.

## Steps

- [ ] `src/widget.py`: add an export handler that writes a CSV header then rows

## Verification

| Step | Check | Result |
| --- | --- | --- |
| export handler | `python3 -m unittest discover tests` | `NOT_APPLICABLE` |
