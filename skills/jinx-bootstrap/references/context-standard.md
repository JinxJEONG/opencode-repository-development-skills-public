# Repository Context Standard

Use this reference for detailed bootstrap criteria. Read [mandatory project layout](../standard/contract.md#mandatory-project-layout), [central configuration](../standard/contract.md#central-configuration), and [structure refactoring](../standard/contract.md#structure-refactoring) in the contract. Gather evidence for safe structural code/config migration and context adoption, not unrelated business changes, new skills, or automation.

## Audit Surfaces

Inspect only relevant files and directories, beginning at the repository root:

- Shared and native agent instructions from [agent file setup](agent-files.md), `README*`, `CONTRIBUTING*`, architecture docs, runbooks, changelogs, and ownership files.
- Git metadata and worktree status when available. A dirty tree is evidence of current state, not permission to alter or discard others' work.
- Package, workspace, build, formatter, linter, type-checker, test, task-runner, container, deployment, and CI configuration.
- Dependency manifests and lockfiles, source entry points, public API or application boundaries, tests, generated-code declarations, and database or infrastructure definitions when present.
- Existing issue, release, handoff, or lessons records only when they are maintained repository artifacts.

For each inspected fact, record the defining path and the observed evidence. If a file is absent or conflicting, use `Unknown`, `Not established`, or `Needs verification` rather than filling the gap from convention.

Classify **GREENFIELD** only when no applicable root or nested instruction, maintained context document, or established context structure is found. Otherwise classify **EXISTING**. For an incomplete prior audit, use EXISTING and label its gaps rather than restarting or replacing it.

Separately classify implementation as EMPTY, PLAN_ONLY, PARTIAL, or IMPLEMENTED. EMPTY still gets the skeleton and rules with unknown language/settings marked `Not established`. Planning documents may make context EXISTING while implementation remains PLAN_ONLY. Create basic directories even when empty: `src/`, `tests/`, `experiments/`, `outputs/`, and `docs/{architecture,specs,plans}`, plus root `AGENTS.md`. Scaffold evidence-backed package/feature directories at `src/<package>/<feature>/`, tests at `tests/<feature>/`, and experiments at `experiments/<experiment>/`. Establish root `config.py` for known Python or a native root settings file for another evidenced language. Capture goals, criteria, and task order from plans without implementing business behavior or claiming planned commands ran.

## Stack, Commands, and Sources of Truth

Derive the stack from executable and declarative artifacts, not folder names or README claims. For claims about current implementation, prefer this order when sources conflict:

1. Observed executable configuration and successful current command output.
2. Versioned manifests, lockfiles, schemas, and checked-in automation definitions.
3. Source code, tests, and generated-file declarations.
4. Maintained repository instructions and documentation.
5. Historical notes and informal descriptions.

Map each command to its declaration and its purpose. Record a command only after locating its script, task definition, workflow, or other authoritative source. If a command looks plausible but cannot be established, mark it `Needs verification`; never present a guessed command as canonical. A passing message is not proof if it targets a different directory, skips work, uses stale output, or masks failures.

For instructions, inspect shared and native surfaces, preserving their scope and the target agent's loading rules. Executable evidence establishes actual behavior; it does not override instructions or authorize actions. For intended design, requirements, and unresolved conflicts, use [canonical-source classification](documentation-taxonomy.md#canonical-source-classification). Generated or vendored directories are boundaries, not permission to edit generated output. Record inaccessible paths, unavailable tools, command failures, and skipped checks as `Needs verification`; do not substitute a guessed result. Execute only non-destructive commands whose purpose and authorization are established by the audit.

## Complexity Tiers

Mandatory layout is the same at every tier. The tier decides only how many additional context documents and nested instructions evidence justifies, not whether basic directories or central configuration are adopted.

| Tier | Evidence pattern | Beyond the core |
| --- | --- | --- |
| 1 | Small, single-language repository with one entry point and few commands | Core docs only |
| 2 | Multiple packages, meaningful tooling, or separate test and application areas | Core docs plus the specs and guides the audit shows are needed |
| 3 | Monorepo, multiple deployable units, generated code, or distinct local rules | Adds nested instructions at real boundaries |
| 4 | Large or regulated system with several ownership, runtime, or infrastructure domains | Adds layered nested context, each scoped to a concrete boundary |

Choose the lowest tier supported by evidence. Use [architecture discovery](architecture-discovery.md#pertinent-boundary-candidates) for local instruction boundaries. Create required directories, but don't add optional documents or nested guides merely because a directory exists.

## Templates

The contract defines templates shipped under `../standard/templates/`. Run `../standard/tools/jinx_context_scaffold.py --root <repo>` for create-only structure, inspect blocked/partial results, then replace placeholders with target evidence. It never merges or migrates existing code/configuration; the agent performs semantic migration and missing known-module scaffolding.

| Surface | Template |
| --- | --- |
| Root task router | `agents-root.template.md` |
| Claude bridge | `claude-bridge.template.md` |
| Kiro steering | `kiro-steering.template.md` |
| `docs/README.md` | `docs-readme.template.md` |
| `docs/project.md` | `project.template.md` |
| `docs/architecture/overview.md` | `architecture-overview.template.md` |
| `docs/plans/README.md` | `plans-readme.template.md` |
| `docs/specs/<feature>.md` | `spec.template.md` |
| `docs/plans/active/<task>.md` | `plan.template.md` |
| `docs/_meta/manifest.json` | `manifest.template.json` |

A placeholder file isn't a deliverable. Purpose, commands, boundaries, and requirements come from evidence. Create non-core documents only for a durable need; a retained consumer-bound source always needs its `docs/specs/<feature>.md` acceptance coverage. Basic directories remain required whether or not they contain documents.

Migrate actual code by responsibility while preserving functionality, business contracts, dirty work, and data. Repair internal imports, configuration consumers, and required build/package/deploy paths and ignore rules. Existing layout isn't an exception; only proven framework or external bindings permit narrow recorded exceptions. Preserve retained technical authorities and records without copying their mutable requirements.

Root configuration owns editable non-secret values/defaults and central environment/secret loading/validation; consumers use supported imports or injection. Remove hidden defaults and lower-module environment reads, not algorithmic constants. Require real consumer propagation, invalid-value rejection, and supported package/runtime launch without brittle cwd or `sys.path` tricks, alongside affected project gates. PLAN_ONLY checks the structure/configuration that exists without claiming business implementation or feature completion.

### Nested `AGENTS.md`

Add one only when a subtree has rules that differ materially from its parent, such as generated-code boundaries, a separate toolchain, domain-specific validation, or a distinct ownership contract. The nested file must state its scope, what it overrides or supplements, and the path to the parent context. Never restate the root file in full.

```markdown
# [Subtree] Guide

Scope: [directory]
Parent context: [relative path]
Local rules: [only material differences]
Validation: [authoritative command or `Needs verification`]
```

## Optional Records

A decision, guide, or verification record needs a durable purpose and its fixed category. Identify its source or state `Not established`. Empty directories need no placeholder documents; mandatory basic directories are still created.

## Validation Checklist

- `../standard/tools/jinx_context_check.py --root <repo>` passes, or every remaining item is reported as blocked with a named cause. Its scope is static structure, never semantic coverage.
- `docs/README.md` names each retained authority, its coverage and binding consumer, plus unresolved items; the architecture map records actual/required paths and narrow proven exceptions.
- Each retained source is reached by a real Markdown link to its exact `path#section` from the document that defers to it, is reported as an exception, and carries no duplicate editable copy under `docs/`.
- Every acceptance criterion records the clause it covers and where that requirement came from. A criterion derived from existing behavior is `observed`, one the agent wrote this pass is `proposed`, and neither is reported as approved.
- The mode is explicitly GREENFIELD or EXISTING and supported by inspected context.
- Implementation maturity is recorded separately; planned requirements and paths are not described as implemented, and verification state is a separate field from implementation state.
- The `surface-size` report was read as guidance: a surface above its goal is trimmed by moving detail into `docs/`, never by deleting a rule.
- Each stack claim and command points to an authoritative file or observed execution.
- Every source of truth has a clear precedence decision.
- Architecture relationships have source evidence, and planned behavior is not reported as implemented.
- Documentation roles, canonical sources, and migration decisions are explicit; unresolved authority is labelled.
- No scaffolded placeholder remains unfilled, and trimming the root router never removed a safety rule.
- Nested instructions exist only at material rule boundaries and do not duplicate parent context.
- Each target agent has an explicit coverage result, with imports/conditional rules preserved and static checks distinguished from observed loading.
- Claims without evidence are marked `Unknown`, `Not established`, or `Needs verification`.
- Dirty-worktree state is reported accurately and no unrelated change is reverted, staged, committed, pushed, or hidden.
- Stale files, cached results, skipped tasks, and misleading success output are not treated as validation.
- Code/config and build/package/deploy path or ignore changes are necessary to mandatory migration, with functionality, contracts, dirty work, originals, and records preserved.
- Basic directories exist even when empty; actual moves/splits and internal import/config-consumer repairs are complete or explicitly blocked, not replaced by documentation.
- Real root-config propagation, invalid-value rejection, and supported package/runtime launch have recorded results; static shape isn't semantic migration evidence.
- No new skill, watcher, background agent, self-improvement flow, installed package tooling, dependency upgrade, agent runtime/global edit, Git hook, CI automation, commit, push, or pull request was created. Existing CI edits only repair migration-required paths/command references under the contract; triggers, permissions, secrets, deployment policy and unrelated gates remain unchanged.
- The final report names established facts, unresolved facts, changed context, preserved material, risks, and the correct next handoff.

## Final Report Contract

Report context mode, implementation maturity, repository boundary, actual/required architecture and command maps, canonical-source decisions, complexity tier, [migration](migration.md) decisions, consumer repairs, and narrow binding exceptions. Separate structure adoption, config propagation/invalid-value/launch results, static checks, semantic coverage, per-agent loading, and feature verification. Include blocked items, preservation evidence, risks, and the next handoff. If a handoff skill is unavailable, describe the remaining work directly rather than implying completion.

Never report the relocation as complete while a source is retained outside `docs/`, and never present a passing static run as evidence that the documentation covers its sources.
