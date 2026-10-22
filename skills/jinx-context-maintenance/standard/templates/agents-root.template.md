# <Project name> — Agent Task Router

Scope: repository root. Canonical documentation index: [docs/README.md](docs/README.md).
Fill every placeholder from actual repository evidence. Where evidence is absent, write `Unknown`,
`Not established`, or `Needs verification` — never a plausible guess.

## Status

- Implementation maturity: `EMPTY` | `PLAN_ONLY` | `PARTIAL` | `IMPLEMENTED` (<evidence>)
- Purpose: <one line, or `Not established`>

## Read Before You Act

| Task | Read first |
| --- | --- |
| Any change | [docs/project.md](docs/project.md) |
| File creation, placement, data processing, or generated output | [Structure operating rules and map](docs/architecture/overview.md#structure-operating-rules) |
| Add or change a setting | [Central configuration](docs/architecture/overview.md#central-configuration) |
| Behavior or contract change | `docs/specs/<feature>.md` for the feature |
| Structure, boundaries, or new module | [docs/architecture/overview.md](docs/architecture/overview.md) |
| Multi-step or in-flight work | [docs/plans/README.md](docs/plans/README.md) |
| Unsure where a fact lives | [docs/README.md](docs/README.md) |

Read the task-relevant document only. A full documentation read is not required before an edit.

## Commands

| Purpose | Command | Defined in | State |
| --- | --- | --- | --- |
| <build / test / lint> | `<exact command>` | `<path that declares it>` | verified \| declared \| `Needs verification` |

Never invent a command. If none is established, record `Not established` and say so in reports.

## Mandatory Layout And Settings

- Put maintained functionality in `src/<package>/<feature>/`, tests in `tests/<feature>/`, experiments
  in `experiments/<experiment>/`, results in `outputs/`, and specs/plans in `docs/`. Keep base directories
  even when empty. Derive actual package/feature names from evidence; never create literal placeholders.
- Root configuration: <exact language-native root file, or `Not established` if language undecided>.
  This is the editing home for tunables and non-secret defaults, not a facade over scattered values.
- Add/edit settings there; consumers use <actual supported import or injection route>. Keep override
  precedence and validation centralized. No feature-local duplicate defaults, settings hardcoding, or
  independent environment reads. Keep genuine algorithm constants and per-request input local.
- Preserve central rejection of unresolved/invalid settings and loading errors. Temporary trials
  still put authorized defaults at the root; they cannot introduce downstream fallback values.
  Use supported module/package launches, never `sys.path` insertion or path-search workarounds.
- Resolve secrets at the central boundary from environment/secret storage; never commit their values
  or expose private settings to client bundles. Verify <actual propagation/invalid-input/launch checks>.
- Preserve original inputs under `data/raw/` or `tests/fixtures/`; transformations go to `data/processed/`.
  External inputs need identifiers, not forced copies. Never overwrite originals with outputs.
- Never create `new/final/backup/copy` editing variants or whole-project history copies. Production
  must not depend on `experiments/`. Supported compatibility versions are not history clutter.
- Existing layout is not an exception. Only evidenced framework/external contracts justify a narrow
  alternative recorded in the architecture map; ordinary internal imports must be repaired.

## Boundaries

- Source of truth: code and active configuration establish current behavior; `docs/specs/<feature>.md` establishes
  intended behavior; an unmet requirement is an implementation gap, not a stale document.
- Preserve existing and uncommitted work. Do not revert, stage, or hide unrelated changes.
- Structure adoption/maintenance includes necessary code moves/splits, settings integration, and
  import, test, build/package/deploy path and ignore repairs. Preserve behavior and business contracts.
  Ask before destructive deletion or overwriting unrelated work. Audit/read-only work makes no edits.
  Do not initialize history tools, change agent runtime/global settings, or automate Git/CI. Existing CI
  allows migration-required path/command-reference repairs only; preserve triggers, permissions,
  secrets, deployment policy and unrelated gates. Inspect consumers before moving their targets.
- At completion check placement, central settings consumption, input preservation, copies and all
  changed references; exercise the supported runtime and normal tests. A static PASS or a new config
  file alone is not migration success. Report unverified behavior and incomplete moves explicitly.
  If the user defers testing, leave checks unrun and report `Needs verification`, not success.
- <Repository-specific safety rules: protected paths, generated output, credentials. Keep these even
  when trimming this file for size.>
- Local scoped guides: <path -> subtree, or `None`>

## Context Updates

When a change affects a command, path, contract, or architecture, update the affected canonical
document and the agent-facing references that point at it in the same work:

- Commands or prerequisites change -> [docs/project.md](docs/project.md)
- Behavior or acceptance criteria change -> the feature's `docs/specs/<feature>.md`
- Units, boundaries, flows, or role locations/policies change -> [docs/architecture/overview.md](docs/architecture/overview.md)
- Plan state changes -> [docs/plans/README.md](docs/plans/README.md) and the plan file

Keep unmet requirements. Distinguish implemented from validated. Leave unrelated docs untouched.
This is an execution rule invoked on demand, not a watcher, hook, or scheduler.
