# Migration Map

Use this for safe adoption of [mandatory project layout](../standard/contract.md#mandatory-project-layout), [central configuration](../standard/contract.md#central-configuration), and [structure refactoring](../standard/contract.md#structure-refactoring). Migration covers application structure/configuration and agent-facing context while preserving functionality, business contracts, dirty work, original data, and records. Audit-only makes no edits.

## Inventory Every Source First

Inventory every affected source, test, experiment, output, config consumer, build/package/deploy path, ignore rule, and context file before changing it:

| Old path | Role | Unique content it carries | Decision | Destination | Binding consumer | Evidence |
| --- | --- | --- | --- | --- | --- | --- |

`Unique content` includes functionality, public/business contracts, local rules, decision rationale, unmet requirements, scope, commands and their declarations, or preserved data. Carry it across before retiring a path. An unmet requirement moves to `docs/specs/<feature>.md` as a gap, never as a removed line.

`Binding consumer` names what reads or publishes a source at its path. Establish the binding from evidence, not a filename. Distinguish proven framework/external requirements from internal imports, test paths, and build declarations that must be repaired as part of migration.

The inventory is working material. Keep the durable layout/config map in `docs/architecture/overview.md`, retained authorities and open gaps in `docs/README.md`, and results in the existing report. Add no machine ledger or per-file registry.

## Decisions

| Decision | Use when | Required action |
| --- | --- | --- |
| Keep | The file is already at its standard path with valid content | Leave wording and location intact |
| Move or split | Code, tests, experiments, outputs, or context don't occupy their required home | Migrate by responsibility; preserve contracts and repair imports, consumers, links, and necessary build/package/deploy paths and ignore rules |
| Merge | Several sources cover one claim | Carry every unique constraint into the single canonical home before removing copies |
| Retain | A proven framework or external binding requires a narrow non-standard location, or an established retained-source contract binds authority there | Record constraint, consumer evidence, and affected scope; link exact authority sections and report the exception, not completed relocation |
| Out of scope | Unrelated business behavior, external/private material, or public/generated content not requiring path repair | Record the boundary; don't rewrite it as a side effect of migration |
| Retire | Superseded or removed | Archive as `docs/archive/<name>-superseded.md`, keep the decision history, repair references |
| Blocked | Two live authorities genuinely conflict | Leave both untouched and report the exact conflict and the decision needed |

Existing layout isn't an exception. Create basic `src/`, `tests/`, `experiments/`, `outputs/`, and `docs/{architecture,specs,plans}` directories even when empty. Move authored application modules to `src/<package>/<feature>/`, tests to `tests/<feature>/`, and experiments to `experiments/<experiment>/`. Repair internal imports instead of retaining old paths for convenience. Keep externally bound public docs and generated content under their evidenced consumers; don't hand-edit generated output or absorb a published docs site.

## Semantic Code And Configuration Migration

1. Record pre-migration commands/results where runnable, public/business contracts, dirty edits, data destinations, and recoverability. Pause only an affected move that can't preserve those safely.
2. Move/split modules by actual responsibilities, including maintained code currently in experiments. Repair callers, imports, test discovery, entry points, package/build/deploy paths, and ignore rules necessary for the migration. Keep production independent of experiment execution. Don't implement unrelated business changes or delete history copies to clear a gate.
3. Use root `config.py` for Python and an evidence-backed language-native root settings file otherwise. Unknown language means `Not established`, not a guessed Python file. Root configuration owns editable non-secret values/defaults and environment/secret loading and validation; keep secret values out of committed files.
4. Replace lower-module defaults/environment reads with supported imports or injection from that authority. Keep algorithmic constants local. Preserve intended behavior while removing duplicate configuration authorities; don't use cwd-dependent imports or `sys.path` patches to make root configuration reachable.
5. Prove a real configuration change reaches representative consumers, invalid values are rejected, and the supported package/runtime launch succeeds. Run affected tests/type/build gates and check original data preservation. A declaration-only assertion or mock bypassing the consumer doesn't establish propagation.
6. For PLAN_ONLY, create basic structure and evidence-backed known modules/configuration, not business implementation. Check the scaffold/config path that exists and label future feature behavior unimplemented. The create-only template tool never performs semantic migration; the agent does.

## A Source A Consumer Binds In Place

Some authoritative material has an established retained-source contract or a proven external binding. Two patterns recur:

```text
README.md      package readme a distribution surface publishes
DESIGN.md      contract a test reads by path
```

Preserve the binding and its authority. Don't treat a repairable internal code import as equivalent to a retained technical contract. Claiming everything lives under `docs/` while a source is retained is false. For each retained source:

1. Link its exact sections from `docs/` with real Markdown links to `path#section`, and name which
   clauses it owns. A path written in prose is a description, not a reference an agent can follow.
2. Add a row to **Authoritative Sources** in `docs/README.md`: the source, where its coverage lives, and
   the consumer that binds it with the evidence that the consumer reads it.
3. Write the project's own `docs/specs/<feature>.md` acceptance coverage mapping each criterion to the
   individual clause it covers, with that clause's provenance. Additive project criteria, never a
   wholesale mirror, and never a section name standing in for the clauses inside it.
4. Never copy its mutable requirements into `docs/`. Two editable homes for one requirement is a
   duplicate-authority defect.
5. Report the retention as an exception, not as a completed relocation.

A safe reference integration is not blocked. Reserve `blocked` for a real conflict between two live
authorities that evidence cannot resolve.

A mixed-role file, such as a published readme with agent-facing rules, keeps its published content and moves only the agent-facing rules into the taxonomy. Record the role split and binding evidence.

## Archived Agent Docs Must Stop Loading

`AGENTS.md`, `AGENTS.override.md`, and `CLAUDE.md` are auto-discovered filenames. A historical copy
under any of those names keeps being loaded as live instruction, which is why the checker fails
`archive-no-discovery`. Archive as a non-discovery filename instead:

```text
AGENTS.md              -> docs/archive/agents-root-superseded.md
packages/api/AGENTS.md -> docs/archive/agents-packages-api-superseded.md
CLAUDE.md              -> docs/archive/claude-root-superseded.md
```

Add a one-line status header naming what superseded it. Never leave two live authorities for one claim.

## A Persisted Coverage Ledger

A project established under standard `1.1.0` may hold `docs/_meta/coverage-ledger.json`. Treat it as
prior audit work worth reading, never as a file to clean up:

- Read it first. Its rows name sources someone already examined, and its unresolved rows are findings.
- Carry what still holds into `docs/README.md` under **Authoritative Sources** and **Unresolved**.
- Leave the file in place. Removing or migrating it needs the user's explicit approval, and a migration
  keeps the original copy until they confirm. Deleting a user's audit record on your own initiative is
  destroying evidence, not tidying.

## Blocking Conditions

Stop the scoped mutation and report, rather than writing somewhere else:

| Condition | Evidence to name |
| --- | --- |
| Unsafe collision | The existing path, its unique content, and why it cannot be safely merged |
| Published or generated docs root | The build config, publishing workflow, or generator that owns it |
| Unreadable source | The path and the read failure |
| Unresolved authority | The two conflicting sources and the decision needed |
| Dirty overlapping work | The uncommitted file and the edit that would overwrite it |

A blocked item isn't a pass and never justifies a parallel root. Internal imports and configurable paths are migration tasks, not blocking external bindings. A narrow proven binding permits an explicit exception only for the bound area, not exemption from the whole standard.

## After Migration

Re-run `../standard/tools/jinx_context_check.py --root <repo>` for static paths, links, anchors, and archive safety, then record semantic migration checks separately. Report moves/splits, consumer repairs, configuration propagation/invalid-value/launch results, preserved functionality/data/work, narrow exceptions, and blocked items. Structure adoption, source coverage, agent loading, and feature verification remain separate outcomes; a static pass proves none of the latter three.
