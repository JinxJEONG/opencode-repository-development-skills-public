# Design Contract Coverage

Status: `approved` — provenance: [../decisions](../README.md) holds no decision record, so approval
rests on the retained authority itself: [`../../DESIGN.md`](../../DESIGN.md) declares the token
contract as binding. No criterion below is derived from what `src/widget.py` currently does.

## Authoritative Source

| Clause | Authoritative source | Consumer that binds it | Disposition |
| --- | --- | --- | --- |
| Color token names and values | [`DESIGN.md#color-tokens`](../../DESIGN.md#color-tokens) | `tests/test_page.py` | protected-source |
| Layout token names and values | [`DESIGN.md#layout-tokens`](../../DESIGN.md#layout-tokens) | `tests/test_page.py` | protected-source |

`DESIGN.md` stays authoritative for every token value. This document adds the project's acceptance
coverage for it and never restates a token value, so there is one editable authority per requirement.

## Requirement

The widget page renders using only the tokens declared in `DESIGN.md`, and the token contract stays
readable at its current path for the consumer that asserts it.

## Acceptance Criteria

Each criterion maps to one clause of the retained source, not to a section name or a summary of it.

| Criterion | Clause it covers | Provenance |
| --- | --- | --- |
| 1 | [`DESIGN.md#color-tokens`](../../DESIGN.md#color-tokens) token list | retained authority |
| 2 | [`DESIGN.md#layout-tokens`](../../DESIGN.md#layout-tokens) gutter value | retained authority |
| 3 | retention of the source path | `tests/test_page.py` binding, recorded in the ledger |

1. Given the token set in [`DESIGN.md#color-tokens`](../../DESIGN.md#color-tokens), when the page
   renders, then every color comes from a token named in that section.
2. Given the gutter value in [`DESIGN.md#layout-tokens`](../../DESIGN.md#layout-tokens), when the page
   renders, then its gutter equals that value.
3. Given `tests/test_page.py` reads `DESIGN.md` by path, when the contract moves, then that test fails,
   so the source stays in place.

## Implementation State

| Criterion | Implementation | Verification | Evidence |
| --- | --- | --- | --- |
| 1 | gap | unverified | no token usage audit exists in `src/widget.py` |
| 2 | gap | unverified | no rendering path reads the gutter token |
| 3 | implemented | verified | `tests/test_page.py` fails if `DESIGN.md` moves |

Criterion 3 is verified only as a document-retention fact. `tests/test_page.py` asserts that
`DESIGN.md` still declares `--widget-gutter`; it never renders the page, so it establishes nothing
about criteria 1 and 2.

## Open Gaps

- Criteria 1 and 2 are unmet implementation gaps. The audit accounts for them; it does not close them.
- No approval authority exists for this project beyond the retained source. Recorded here rather than
  inferred from the readme.

## Verification

| Criterion | Check | Result |
| --- | --- | --- |
| 1 | `python3 -m unittest discover tests` | `NOT_APPLICABLE` |
| 2 | `python3 -m unittest discover tests` | `NOT_APPLICABLE` |
| 3 | `python3 -m unittest discover tests` | `PASS` |
