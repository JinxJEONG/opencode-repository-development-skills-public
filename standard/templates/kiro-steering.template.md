---
inclusion: always
---

# Kiro IDE And CLI Project Execution

Before editing, read root `AGENTS.md` for shared execution rules, commands, and boundaries.
If its content is not available in this session, open it now; a link or file listing is not a read.

Read only the document your task needs:

| Task | Document |
| --- | --- |
| Any change | `docs/project.md` |
| File placement or settings | `docs/architecture/overview.md` (structure rules, map and central configuration) |
| Behavior or contract change | `docs/specs/<feature>.md` |
| Structure or boundaries | `docs/architecture/overview.md` |
| Multi-step or in-flight work | `docs/plans/README.md` |

If the task does not match a row above, start from `docs/README.md`.

## Before Editing And Before Completion

- Use the architecture map to identify actual source, test and output paths; identify the root
  settings file, validation/consumer route and supported launch command before changing them.
  Record unresolved decisions in the task response or existing plan, not invented defaults.
- Demos, experiments and temporary trials obey the same rules. Put authorized temporary defaults
  at the root settings boundary. Never turn an unresolved/invalid value into a lower-level fallback,
  bypass the root validator, or catch configuration loading errors to continue with a default.
- Do not insert paths into `sys.path` or add path-search workarounds for tests/demos. Use the
  supported module/package command; report an unestablished launch or missing dependency instead.
- Compare your actual changes against those decisions. Update affected commands in `docs/project.md`,
  structure/settings routes in `docs/architecture/overview.md`, and affected specifications/references.
  Passing your own tests does not prove these rules were followed.
- Separate IDE/CLI loading evidence, explicit file reads, behavior checks and unverified claims.
  If testing is deferred by the user, do not run it or launch verification sessions; report the gap.

`docs/` remains the canonical home for specifications and plans. These checkpoints summarize the
shared rules; do not copy whole documents or create a second requirements authority here.
