# <Feature>

Status: `proposed` | `approved` | `implemented` | `superseded by <path>` (evidence: `<path>`)

## Requirement

<What must be true. Intended behavior, independent of current code.>

## Authoritative Source

| Clause | Authoritative source | Consumer that binds it | Disposition |
| --- | --- | --- | --- |
| <clause> | `<path#section>` or `this document` | `<path that reads the source>` or `None` | stays at its source \| moved here |

A row naming a source other than this document means that source stays authoritative for the clause:
link it, do not restate its mutable requirements here. The same source appears in
[the documentation index](../README.md#authoritative-sources).

## Acceptance Criteria

1. Given <precondition>, when <action>, then <observable outcome>.
2. ...

Each criterion must be observable through a real surface. Do not write a criterion that can only be
confirmed by reading the implementation. A criterion whose requirement lives in a retained source
cites that source's exact section instead of paraphrasing its values.

## Implementation State

| Criterion | Implementation | Verification | Evidence |
| --- | --- | --- | --- |
| 1 | implemented \| gap \| `Needs verification` | verified \| unverified \| `BLOCKED` | `<path, command, or observed result>` |

Implementation and verification are separate states: an implemented criterion with no recorded check
result is `unverified`, never verified. An unmet criterion is an implementation gap. Do not rewrite it
to match current behavior.

## Verification

| Criterion | Check | Result |
| --- | --- | --- |
| 1 | `<existing project command or manual surface step>` | `PASS` \| `FAIL` \| `BLOCKED` \| `NOT_APPLICABLE` |
