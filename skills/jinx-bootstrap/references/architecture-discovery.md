# Architecture Discovery

Use this reference to establish current and required structure, trace consumers, and plan safe mandatory migration. Preserve business behavior; don't add tooling, upgrade dependencies, or automate CI or Git.

## Trace Structure From Evidence

1. Start with workspace and build manifests, entry points, module exports, configuration, tests, and existing architecture or decision records. Use SPEC and PLAN documents to identify intended behavior and open work, not to prove implementation.
2. Identify runtime or delivery units and their responsibilities. Follow representative entry points through calls, imports, API contracts, events, jobs, storage, or output generation as applicable. For a library or documentation repository, trace its public interface or authoring-to-consumer path instead of inventing a service topology.
3. Establish dependency direction and shared contracts from both producers and consumers. A directory name, dependency declaration, or diagram alone does not prove a live relationship. Distinguish a statically traced path from observed runtime behavior.
4. Record existing enforcement for important boundaries, such as an import rule, schema, test, or CI invocation. Distinguish declared, observed passing, and unverified checks; name missing enforcement without installing it.
5. Compare intended, actual, and mandatory structure. Label aligned, planned but absent, conflicting, or unknown relationships with evidence. Preserve business requirements and decisions; repair structural gaps in setup, while unrelated business gaps remain separate work.

Use a compact map in the audit report, or reuse an existing architecture document when a durable update is warranted:

| Unit or flow | Responsibility and entry point | Dependency or contract | Evidence and verification state | Intended/actual gap |
| --- | --- | --- | --- | --- |

Record ownership only from an established ownership source. Note inaccessible areas and untraced relationships. Sample enough real paths to explain the main units and cross-boundary interactions; expand only where a contradiction or missing relationship changes the context decision. Do not dump a full directory listing or treat a partial trace as complete coverage.

## Structure Rule Adoption

Read [mandatory project layout](../standard/contract.md#mandatory-project-layout), [central configuration](../standard/contract.md#central-configuration), and [structure refactoring](../standard/contract.md#structure-refactoring). Integrate their working rules and actual/required map into `docs/architecture/overview.md`, preserving units, contracts, dependencies, and flows. Link retained authority by exact section and record it in `docs/README.md`; don't create a competing rule.

1. Map authored modules to `src/<package>/<feature>/`, tests to `tests/<feature>/`, experiments to `experiments/<experiment>/`, generated output to `outputs/`, documentation to `docs/{architecture,specs,plans}`, and shared instructions to root `AGENTS.md`. Always create basic `src/`, `tests/`, `experiments/`, `outputs/`, and `docs/{architecture,specs,plans}` directories, even when unused. PLAN_ONLY adds evidence-backed package/module shells and minimal import/config wiring, not application business behavior.
2. Trace root scripts, package entry points, imports, test discovery, build/package/deploy paths, ignore rules, and public consumers. Plan moves and responsibility-based splits with their connection repairs. Existing layout and internal imports aren't exceptions; retain only proven framework or external bindings, with their narrow constraint and evidence recorded.
3. Identify provided/collected originals, versions, transformation destinations, output policies, and retention/tracking exceptions. Preserve originals and dirty data; external identifiers need no local replica or secrets. Migration changes destinations and consumers, not the content of original inputs.
4. Establish experiment purpose, active/adopted/closed state, adoption destination, and production consumers. Move maintained production responsibilities into source and repair consumers so delivery doesn't depend on experiments. Don't promote unapproved business behavior or destroy experiment evidence.
5. Inventory editable values, defaults, environment/secret reads, and validation. Python uses root `config.py`; choose other root settings files from actual language/runtime evidence. If the language is unknown, record the choice `Not established`. Centralize those values and loading/validation, then wire lower modules through supported imports or injection; remove hidden defaults/environment reads, not algorithmic constants. No brittle cwd or `sys.path` loading tricks.
6. Trace revision history and copies by source, purpose, consumer, selection point, and synchronization, not names. Preserve supported versions, managed workspaces, distribution copies, and historical records; disposition of old history copies needs its own authorization.
7. Fill the compact map with actual and required paths, migrations, exceptions, and open facts. Unused content may be `Not applicable`, but its basic directory still exists. Unknown policies stay `Not established`; unimplemented business behavior stays planned. Add no history tooling, per-file registry, or mandatory report.
8. Connect the index and effective agent routes to the same project rule section. After a route change, use an available authorized fresh session to check discovery and editing-location choice. A link isn't runtime loading evidence.
9. Verify migrations through affected tests/build gates, real configuration propagation to consumers, invalid-value rejection, and supported package/runtime launch. Record unavailable checks as blocked and distinguish adoption from feature verification.

Keep genuine conflicts and unresolved facts in the existing Unresolved table in `docs/README.md`. Setup authorizes necessary structural code/config, path, and ignore repairs, including path/command references in existing CI under the contract's narrow allowance. Inspect these before moving targets; block connected moves if repair would require forbidden policy changes. No unrelated features, dependency upgrades, unsafe overwrites or record deletion. A template scaffold creates only missing structure; the agent owns semantic migration.

## Pertinent Boundary Candidates

Survey these as candidates, not automatic `AGENTS.md` destinations:

| Signal | What to inspect |
| --- | --- |
| Repository root | Shared execution rules and links needed across tasks |
| Workspace packages, apps, services, or independent manifests | Separate command cwd, toolchain, public contract, or validation scope |
| Source, API, library, or domain subtrees | Local constraints that differ from shared conventions |
| Tests and fixtures | Distinct setup, isolation, data handling, or test commands |
| Workflow or infrastructure directories | Existing operational constraints; read-only discovery does not authorize CI edits |
| Maintained docs or wiki tooling | Separate authoring rules or validation commands, if established |
| Generated, vendored, dependency, cache, or build output | Identify the generator or maintained source; keep instructions outside generated or third-party output |

For each relevant candidate, record `path -> evidence -> material difference from parent -> decision`. Decide among:

- **Parent coverage**: no distinct execution rule; do not create a nested file.
- **Linked documentation**: the distinction explains architecture or rationale, but does not change how an agent works in the subtree.
- **Nested instruction**: a concrete local rule or validation need would otherwise be missed. Preserve existing valid instructions and include only the local difference.
- **Unresolved**: evidence is insufficient; mark `Needs verification` and leave existing guidance intact.

For example, two packages using the same root commands need no nested instructions merely because both have manifests. A generated-client subtree may need a warning at the nearest maintained boundary pointing to its generator; it does not justify editing generated files. An existing nested file deserves review even when no new file is needed.

## Keep Rules And Explanations Separate

`AGENTS.md` holds actionable constraints and pointers needed during execution. `docs/architecture/overview.md` explains responsibilities, dependency direction, contracts, flows, and rationale. Keep safety-critical rules in their applicable scope; meet size guidance by moving explanation, not dropping rules. Follow [documentation taxonomy](documentation-taxonomy.md) for document homes and [the migration map](migration.md) for moves and consumer repairs.

Discovery identifies the checks required to prove migration safety. Use existing project gates and focused propagation/invalid-value/launch checks; don't install a new enforcement system in the target.

## Design Sources

- [Deep Wiki pertinent folder detection](https://github.com/microsoft/skills/blob/23d0dac5f83f268166a17f0bc7dc6c73dc348a33/.github/plugins/deep-wiki/skills/wiki-agents-md/SKILL.md#pertinent-folder-detection) informs the candidate scan. Here, candidates require a material local-rule difference; folder existence does not mandate generation, and existing instructions remain auditable.
- [mblode architecture scope separation](https://github.com/mblode/agent-skills/blob/ec7f60811b30aa5eb0be58772cedbfc86454186f/skills/codebase-architecture/SKILL.md#related-skills) informs the distinction between instructions and architecture explanation. This workflow performs mandatory structural migration, not general architecture redesign or new enforcement tooling.
