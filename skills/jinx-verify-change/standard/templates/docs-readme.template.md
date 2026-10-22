# Documentation Index

Canonical home for specifications, plans, architecture, decisions, guides, and verification records.
A category with nothing to say yet gets no placeholder file; create its document on first real use.

| Area | Path | Holds |
| --- | --- | --- |
| Project overview | [project.md](project.md) | purpose, scope, status, canonical commands |
| Architecture | [architecture/overview.md](architecture/overview.md) | units, boundaries, flows, evidence |
| Structure rules and map | [architecture/overview.md#structure-operating-rules](architecture/overview.md#structure-operating-rules) | editing homes, protected inputs, experiments, output, history/copy exceptions |
| Specifications | `specs/<feature>.md` | required behavior and acceptance criteria |
| Plans | [plans/README.md](plans/README.md) | active, completed, superseded plans |
| Decisions | `decisions/` | decision records with status |
| Guides | `guides/` | procedures and runbooks |
| Verification | `verification/` | verification records |
| Archive | `archive/` | historical copies, non-discovery filenames |

Agent entry points: root `AGENTS.md` (shared rules), the Claude bridge, and
`.kiro/steering/project-context.md`. They route here; they do not copy this content.

A directory here outside the names above is allowed when this file says why it exists. Add a row for
it rather than leaving a reader to guess.

## Authoritative Sources

One editable home per claim. When a consumer outside `docs/` binds a source in place — a test that
reads a contract by path, a packaging surface that publishes a readme — that source stays where it is
and stays authoritative. Link its exact sections from the document that defers to it; do not copy its
mutable requirements into `docs/`.

| Source | Canonical home | Why it stays there |
| --- | --- | --- |
| `<path or path#section>` | `specs/<feature>.md`, or `this source` when it stays authoritative | `<consumer that reads it, with evidence>`, or `moved: source removed` |

## Unresolved

What this documentation has not settled. An empty table means nothing is open, not that nothing was
looked at.

| Item | Why it is open | Who decides |
| --- | --- | --- |
| `<gap, conflict, or unverified claim>` | `<evidence>` | `<owner or `Not established`>` |
