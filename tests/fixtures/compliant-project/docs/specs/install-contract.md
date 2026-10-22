# Install And Usage Coverage

Status: `approved` — provenance: [`../../README.md`](../../README.md) is the published distribution
surface, so its install and usage clauses are the approved authority. No criterion below is derived
from what `src/widget.py` currently does.

## Authoritative Source

| Clause | Authoritative source | Consumer that binds it | Disposition |
| --- | --- | --- | --- |
| Install command | [`README.md#install`](../../README.md#install) | `external:` published package readme | reference-integrated |
| Usage entry point | [`README.md#usage`](../../README.md#usage) | `external:` published package readme | reference-integrated |

`README.md` is the published package readme and stays authoritative for the install and usage contract.
This document links those sections and adds project acceptance coverage without copying their commands.

## Requirement

An operator can install the service and reach the widget list using the published readme alone.

## Acceptance Criteria

Each criterion maps to one clause of the retained source, not to a section name or a summary of it.

| Criterion | Clause it covers | Provenance |
| --- | --- | --- |
| 1 | [`README.md#install`](../../README.md#install) install command | published distribution surface |
| 2 | [`README.md#usage`](../../README.md#usage) usage entry point | published distribution surface |

1. Given the install step in [`README.md#install`](../../README.md#install), when an operator follows
   it, then the service package is available.
2. Given the usage step in [`README.md#usage`](../../README.md#usage), when the operator requests
   `/widgets`, then a JSON array is returned.

## Implementation State

| Criterion | Implementation | Verification | Evidence |
| --- | --- | --- | --- |
| 1 | implemented | unverified | `README.md#install` declares the command; no recorded run |
| 2 | implemented | unverified | `src/widget.py` defines the handler; no recorded request |

## Open Gaps

- Neither criterion has a recorded check result. The suite exercises no install and issues no request,
  so both stay `unverified` rather than borrowing a passing unrelated test.

## Verification

| Criterion | Check | Result |
| --- | --- | --- |
| 1 | `python3 -m unittest discover tests` | `NOT_APPLICABLE` |
| 2 | `python3 -m unittest discover tests` | `NOT_APPLICABLE` |
