---
name: jinx-bootstrap
description: Establish mandatory project layout, central configuration, and repository context from plans or existing code when no trusted standard exists, for Codex, Claude Code, Kiro, and OpenCode.
---

# Repository Bootstrap

## Purpose and Triggers

Use this for initial setup or migration into the mandatory standard. Trigger it in an unfamiliar repository, when no trustworthy context exists, or when existing instructions must be classified before a standard structure can be established. Don't use it for routine drift or to verify one change. An audit-only request remains read-only.

An established standard missing one agent's entry point belongs to `jinx-context-maintenance`. A plan-only project belongs here even when planning documents already exist.

## The Standard

[`standard/contract.md`](standard/contract.md) in this package is the authority for every path, filename, manifest field, and check id. Read it before creating or moving a file. Its structure is fixed; what fills it comes from the target repository's evidence.

Read [mandatory project layout](standard/contract.md#mandatory-project-layout), [central configuration](standard/contract.md#central-configuration), and [structure refactoring](standard/contract.md#structure-refactoring). These require adoption, not an advisory map of existing paths:

- Create the basic directories even when empty: `src/`, `tests/`, `experiments/`, `outputs/`, and `docs/{architecture,specs,plans}`. Place application modules in `src/<package>/<feature>/`, tests in `tests/<feature>/`, and experiments in `experiments/<experiment>/`; keep root `AGENTS.md` and a language-native root central configuration.
- Python uses root `config.py`; other languages use an appropriate root settings file chosen from actual stack evidence. An unknown language means the choice is `Not established`, not an arbitrary Python file.
- `docs/` is the canonical home for agent-facing specifications and plans. Never create `.kiro/specs/` or a second docs tree.
- Consumer-bound authoritative documents stay in place under the contract's retained-source rules, linked by section and recorded in `docs/README.md`. Application-code exceptions need a proven framework or external binding; existing layout and repairable internal imports aren't exceptions.
- Agent runtime settings, custom-agent JSON, and global or personal agent config are read-only. Application configuration migration is in scope. Report blocked agent loading with the exact missing connection.

## Core Rules

- For current-implementation claims, executable configuration, source, and observed output outrank prose.
- Never invent commands, architecture, ownership, or facts. Record `Unknown`, `Not established`, or `Needs verification`.
- Separate observed implementation from intended design, and implementation state from verification state. A spec or plan defines a requirement without proving it is implemented; an implemented requirement with no recorded check result is unverified; code does not authorize removing either.
- The checker's scope is static structure. Whether a document actually covers its source is your judgement, reported separately and never inferred from a passing check.
- Preserve functionality, business contracts, public or generated documentation, unique rules, decisions, dirty work, and original data throughout migration.
- Never create project-specific skills. A future automation opportunity may be reported; it creates nothing.

## Mode and Maturity

- **GREENFIELD**: no useful context exists. Establish the standard directly.
- **EXISTING**: instructions or docs exist. Audit and preserve valid material first, then migrate code, configuration, tests, experiments, outputs, and agent-facing context into the mandatory standard. Valid old paths don't exempt a project from adoption.

Record implementation maturity separately as **EMPTY**, **PLAN_ONLY**, **PARTIAL**, or **IMPLEMENTED**. EMPTY still gets the mandatory skeleton and rules; unknown language and settings choice remain `Not established`. For PLAN_ONLY, create the basic structure and evidence-backed package/feature directories, central configuration when the language is known, documentation, and execution guidance. Derive requirements and task order from plans; don't implement application business behavior or invent runnable commands. Scaffolding doesn't make a planned feature implemented.

## Workflow

1. Confirm the repository root and worktree state. Record what is dirty before touching anything.
2. Run `standard/tools/jinx_context_check.py --root <repo>`. `BLOCKED context-present` confirms bootstrap is the right skill; any other output is the starting baseline.
3. Locate root and nested instructions for every target, including overrides, imports, conditional rules, and configured instruction sources. Preserve each effective scope.
4. Classify context mode and implementation maturity independently.
5. Inventory existing context, specs, plans, decisions, docs, configuration, and automation surfaces. Read instructions before judging them. A `docs/_meta/coverage-ledger.json` left by an earlier standard version is prior audit work: read it, carry what still holds forward, and leave the file alone unless the user asks otherwise.
6. Map languages, tooling, entry points, modules, dependencies, configuration consumers, and representative flows from evidence. Use [architecture discovery](references/architecture-discovery.md#structure-rule-adoption) to map actual and required homes, protected inputs, experiments, outputs, history, and managed copies; identify each migration and proven exception.
7. Map each declared command to its defining configuration, working directory, and verification state. A declared command is not a successful run.
8. Build [the migration inventory](references/migration.md): each affected path gets a decision, destination, consumer evidence, and preserved contracts, rules, decisions, or unmet requirements. Include code splits, imports, config consumers, and build/package/deploy paths and ignore rules required by the move. Establish bindings from evidence, never filenames.
9. Check the blocking conditions in the contract. If one fires, stop the scoped mutation and report it; never redirect the write to an alternate root.
10. Scaffold missing structure with `standard/tools/jinx_context_scaffold.py --root <repo>`. It is create-only and keeps existing files; the agent, not the template tool, performs semantic code/config migration. Read any `BLOCKED` output and partial list before continuing. Create missing basic directories even when unused, fill known modules from evidence, and replace every placeholder.
11. Carry migrated content into its standard home, repair inbound links, and archive superseded agent docs under `docs/archive/<name>-superseded.md` so nothing auto-loads. For a retained consumer-bound source, link exact sections and write `docs/specs/<feature>.md` acceptance coverage mapping each criterion to its clause and provenance; never copy mutable requirements. Add nested instructions only for material local rules.
12. Perform the planned structural migration. Move and split code by responsibility without changing business contracts; repair imports and necessary build/package/deploy paths and ignore rules. Root configuration owns editable non-secret values/defaults and central environment/secret loading and validation; lower modules consume through supported imports or injection, with no hidden defaults or environment reads. Keep algorithmic constants local. Use supported package/runtime loading, never brittle cwd assumptions or `sys.path` tricks.
13. Complete `docs/README.md`: index, **Authoritative Sources** with binding consumers and coverage, and **Unresolved** with gaps, conflicts, and unverified claims. Connect it and effective agent routes to the project's architecture rules and map, not an installed skill path. Re-read migrated context against its sources.
14. Run the static checker and migration behavior checks: real configuration propagation to consumers, invalid-value rejection, and the supported package/runtime launch, plus affected tests/build gates. A configuration declaration or mocked-only path isn't propagation evidence. For PLAN_ONLY, test the scaffold/config loading that exists and report business behavior as not implemented. Compare final changes and preserved data with step 1; report blocked checks by cause.
15. Report mode, maturity, actual/required maps, migration and exception decisions, structure adoption and feature verification as separate outcomes, per-agent static/runtime coverage, semantic coverage judgement, preserved material, unknowns, and handoffs.

Read [the context standard](references/context-standard.md) for detailed audit criteria, source precedence, and validation, [documentation taxonomy](references/documentation-taxonomy.md) for authority classification, and [agent file setup](references/agent-files.md) for per-agent loading rules. References guide decisions; never copy them into a target repository.

## Completion Criteria

Finish only when mode, maturity, the evidence-backed architecture and command map, the `docs/README.md` source and unresolved records, and per-agent coverage are explicit; the checker passes or names blocked items; and no placeholder remains unfilled. A structural pass over documentation nobody read against its sources is not completion. Every uncertain claim stays marked `Unknown`, `Not established`, or `Needs verification`. Distinguish proposed structure, written documentation, declared commands, implementation state, and observed verification. Confirm no unrelated material changed.

Finish only when mandatory directories exist, evidenced code/config migrations and consumer repairs are complete or explicitly blocked, exceptions are narrow and proven, and required migration checks have recorded results. Mark unused content `Not applicable` without omitting its basic directory, and undecided facts `Not established`. A documented rule or static structural pass doesn't prove adoption, configuration propagation, or feature completion.

Upgrading follows [Version Upgrade](standard/contract.md#version-upgrade): integrate the rules, map, and routes before setting `standardVersion`; changing only the version is not adoption. Carry useful ledger findings into `docs/README.md` and leave the old ledger in place unless the user approves removal. The scaffold never rewrites an established manifest or architecture document.

## Safety Boundaries and Non-responsibilities

Code moves/splits, imports, central configuration and consumers, and necessary build/package/deploy paths and ignore changes are in scope for mandatory migration. Existing CI permits only migration-required path/command-reference repairs under the contract; inspect them before moving targets. Don't add workflows or change triggers, permissions, secrets, deployment policy or unrelated gates. Don't implement unrelated features, redesign business behavior, upgrade dependencies, edit Git hooks, or alter agent runtime/global/personal/managed settings. Install no package tooling into targets. Create no new skills, watchers, background agents, self-improvement loops, Git/CI automation, commits, pushes, or pull requests. Don't claim success without evidence or delete/rewrite persisted records without explicit approval and a preserved copy.

Hand later drift and upgrades to `jinx-context-maintenance`. Report unrelated business defects for separate authorized work; use `jinx-verify-change` for feature-correctness evidence. Adoption checks don't replace that outcome.
