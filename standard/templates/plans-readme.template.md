# Plans

One plan file per task, under exactly one state at a time. A filename must not exist in two states.

| State | Path | Meaning |
| --- | --- | --- |
| Active | `active/<task>.md` | in flight |
| Completed | `completed/<task>.md` | landed; keep the outcome, not the play-by-play |
| Superseded | `completed/<task>.md` with a `Status: superseded by <path>` line | replaced by another plan |

## Active

| Task | Plan | Spec | Status |
| --- | --- | --- | --- |
| <task> | `active/<task>.md` | `docs/specs/<feature>.md` | <state> |

## Completed

| Task | Plan | Outcome |
| --- | --- | --- |
| <task> | `completed/<task>.md` | <what became true> |

Move a plan by moving the file and updating this index in the same change. Unmet requirements stay in
`docs/specs/`; completing a plan does not close a requirement without evidence.
