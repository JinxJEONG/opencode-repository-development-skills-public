# Widget Service — Agent Task Router

Scope: repository root. Canonical documentation index: [docs/README.md](docs/README.md).

## Status

- Implementation maturity: `PARTIAL` (`src/widget.py` exists; export path is a gap)
- Purpose: serve widget records over an internal HTTP API.

## Read Before You Act

| Task | Read first |
| --- | --- |
| Any change | [docs/project.md](docs/project.md) |
| Behavior or contract change | `DESIGN.md` and `README.md`; no `docs/specs/` document exists yet |
| Structure or boundaries | [docs/architecture/overview.md](docs/architecture/overview.md) |
| Multi-step work | [docs/plans/README.md](docs/plans/README.md) |

## Commands

| Purpose | Command | Defined in | State |
| --- | --- | --- | --- |
| Test | `python3 -m unittest discover tests` | `tests/` | verified |

## Boundaries

- Code establishes current behavior; `DESIGN.md` establishes the intended token contract.
- Never commit fixture credentials. Preserve uncommitted work.

## Context Updates

When a change affects a command, path, contract, or architecture, update the affected canonical
document in the same work: commands to [docs/project.md](docs/project.md), behavior to its source,
boundaries to [docs/architecture/overview.md](docs/architecture/overview.md), plan state to
[docs/plans/README.md](docs/plans/README.md).
