# Project

Source of truth: this file for scope, status, and canonical commands. Fill each field from evidence;
use `Unknown`, `Not established`, or `Needs verification` when evidence is missing.

## Purpose And Scope

- Purpose: <one or two lines>
- In scope: <observable areas this repository owns>
- Out of scope: <explicitly excluded areas>

## Implementation Status

| Area | Implementation | Verification | Evidence |
| --- | --- | --- | --- |
| <area or project> | `EMPTY` \| `PLAN_ONLY` \| `PARTIAL` \| `IMPLEMENTED` | verified \| unverified \| `Needs verification` | `<path or observed command result>` |

A planned path or command stays labelled as planned until it is observed to exist and run. An
implemented area with no recorded check result is `unverified`; do not promote it without evidence.
The mandatory skeleton may exist while feature behavior remains EMPTY or PLAN_ONLY.

## Canonical Commands

| Purpose | Command | Defined in | State |
| --- | --- | --- | --- |
| <purpose> | `<exact command>` | `<declaring path>` | verified \| declared \| `Needs verification` |

## Requirements And Gaps

| Requirement | Spec | Authoritative source | Implementation state |
| --- | --- | --- | --- |
| <requirement> | `docs/specs/<feature>.md` | `this documentation` or `<retained path#section>` | met \| gap \| `Needs verification` |

A source that stays authoritative outside `docs/` is listed in
[the documentation index](README.md#authoritative-sources) with the consumer that binds it in place.
Cite it; do not duplicate its mutable requirements here.
