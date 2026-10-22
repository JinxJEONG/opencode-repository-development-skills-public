# Jinx Context Standard Contract

Single maintained source for the structure all three `jinx-*` skills establish, maintain, and verify. `standard/` in this repository is the only authored copy; each distributable package carries a complete synchronized copy at `skills/<package>/standard/`, so no package depends on a sibling at runtime. Standard version: see `VERSION`.

This contract fixes the project layout, context paths, and central configuration responsibilities. Bootstrap and maintenance actually refactor a target into that structure; documenting its existing layout is not adoption. Project-specific features, language, commands, and business requirements come from evidence, never guesses. Verification remains change-scoped.

## Agent Surfaces

| Surface | Path | Rule |
| --- | --- | --- |
| Shared instructions | `AGENTS.md` (repository root) | Lightweight task router, goal ~100 non-blank lines. Must route to `docs/README.md`. Size is advisory: move detail into `docs/`, never delete a safety rule to fit a number. |
| Claude bridge | `CLAUDE.md` with `@AGENTS.md`, or an established `.claude/CLAUDE.md` with `@../AGENTS.md` | Bridge only. Whichever branch already exists stays the effective one; never create a second bridge. `AGENTS.md` never imports `CLAUDE.md`. |
| Kiro IDE / Kiro CLI steering | `.kiro/steering/project-context.md` | Mandatory, frontmatter `inclusion: always`. Routes to root `AGENTS.md` and task-relevant docs, with short execution checkpoints below and `docs/README.md` fallback. Must not embed or import whole documents (`#[[file:...]]` and `@<path>` import lines are forbidden here). |
| OpenCode | `AGENTS.md` plus already-configured instruction sources | Read-only for `opencode.json`/`opencode.jsonc`. |
| Runtime settings, custom-agent JSON, global/personal config | — | Read-only. Blocked loading is reported with the exact missing connection, never silently rewritten. |

`docs/` is the canonical home for *agent-facing* navigation, specifications, and plans. Do not create `.kiro/specs/`, do not mirror docs into a second tree, and do not promise native Specs UI behavior.

### Kiro Execution Checkpoints

The native steering route must require action, not just acknowledge a link. Keep detailed project rules in `AGENTS.md` and `docs/architecture/overview.md`; the steering file carries a short execution reminder, not a second editable requirements document.

- Before editing, read the applicable shared instructions, project commands and architecture sections. Identify actual source/test/output destinations, the root settings entry point, its validator and consumer route, and the supported launch command. Use the task response or existing plan, not a new mandatory ledger. Missing information blocks only the decision that needs it; a compliant plan-only skeleton remains possible.
- Enforce the same boundaries in demos, experiments and temporary trials. A temporary value needs authorization and still belongs at the root editing surface. Preserve unresolved or invalid setting errors; do not convert them into feature-local defaults or catch loading failures to continue. A read-only root setting is not permission to bypass it downstream.
- Use the supported module/package launch. Do not add `sys.path` mutations or path-search fallbacks to make a demo/test run. If packaging or launch is unestablished, report that gap rather than treating a workaround as compliance.
- Before reporting completion, compare the actual diff with the chosen destinations and settings route. Update affected canonical commands, architecture and specification references in the same change. Green self-authored tests do not excuse a conflicting default, loading bypass or stale documentation.

Record Kiro IDE and Kiro CLI separately when both are targeted: application/version, CLI engine or profile when known, instruction paths, automatic loading versus explicit reads, and behavior evidence. One surface's result does not certify the other. Inspect effective custom-agent resources without changing runtime settings; report the exact missing connection when blocked. If the user defers testing, do not start fresh sessions or run checks to clear a gate: report implementation and `Needs verification` separately.

## Authoritative Sources Outside `docs/`

One editable home per claim. Some authoritative material cannot move into `docs/` without breaking a consumer: a package `README.md` a distribution surface publishes, a `DESIGN.md` a test reads by path. Those stay where they are and stay authoritative. Relocating or deleting one is a defect, and reporting that everything now lives under `docs/` while such a source is retained is a false completion report.

For a retained source:

- The `docs/` document that defers to it links its exact sections and states which clauses it owns. Never copy its mutable requirements into `docs/`: two editable homes for one requirement is a duplicate-authority defect.
- It is listed in `docs/README.md` under **Authoritative Sources**, with the consumer that binds it in place and the evidence that the consumer reads it. That table is read by agents and humans, not parsed by a tool.
- The retention is reported as an exception, not as a completed relocation.

A safe reference integration is not blocked. Only a genuine conflict between two live authorities is.

## Documentation Taxonomy

```text
docs/README.md                  core: navigation, docs index, authoritative sources, unresolved items
docs/project.md                 core: purpose, scope, status, canonical commands
docs/architecture/overview.md   core: units, boundaries, flows, evidence
docs/plans/README.md            core: plan lifecycle and index
docs/specs/<feature>.md         requirement + acceptance criteria per feature
docs/plans/active/<task>.md     in-flight plan
docs/plans/completed/           landed plans (superseded plans keep a status label)
docs/decisions/                 decision records
docs/guides/                    procedures and runbooks
docs/verification/              verification records
docs/archive/                   historical copies, non-discovery filenames only
docs/_meta/manifest.json        tool-consumed manifest
```

The four core docs are required. The category names above are the recommended set; a directory outside them is reported by `docs-structure` and is not a failure, because a project may have a documented reason for it and no static check can read that reason. Explain such a directory with a row in `docs/README.md`. A category with nothing to say gets no placeholder file — create its first document on real use.

Archived agent docs must not keep auto-loading. Store history as `docs/archive/<name>-superseded.md` (for example `agents-root-superseded.md`); `AGENTS.md`, `AGENTS.override.md`, and `CLAUDE.md` filenames are forbidden anywhere under `docs/`.

## Structure Operating Rules

Put the detailed rules and **Structure Map** in `docs/architecture/overview.md`. Root `AGENTS.md` must also state the short mandatory actions, exact root configuration entry point, consumer pattern, and verification commands so later development follows them. Connect all effective agent entry points and `docs/README.md` to the same project-local authority; never depend on an installed skill path. Preserve existing architecture content and consumer-bound document authorities. Do not silently change business requirements to fit a layout.

1. **Use the mandatory layout.** Move authored functionality into `src/<package>/<feature>/`, tests into `tests/<feature>/`, experiments into `experiments/<experiment>/`, and generated results into `outputs/`. Split or combine code where the structure requires it, preserving behavior. Shared code needs an actual shared responsibility. Existing location alone is not an exception.
2. **Do not copy projects to manage development history.** Whole-project `v1/`, `v2/`, or `final/` copies must not replace the project's established revision history. If no history mechanism is established, preserve the work and record the decision needed; do not create a copy tree, initialize a VCS, commit, or tag on the user's behalf.
3. **Distinguish intentional parallel work.** Supported API/schema versions, comparison algorithms, and VCS-managed workspaces are allowed when their purpose, selection/connection point, and current editing home are clear. Release copies are outputs, not development homes. Synchronized distribution copies are allowed when the authored source, consumer, and synchronization method are known. This repository's `standard/` -> `skills/<package>/standard/` copies are such a case, not history snapshots.
4. **Protect supplied and collected development inputs.** Use `data/raw/<dataset>/` when local originals exist, or `tests/fixtures/` for test inputs. Use `data/processed/` for transformations. Never overwrite originals; preserve byte content and recoverable revisions during moves. External storage needs a non-secret location and version/identifier, not a mandatory replica or large-file commit. This does not change normal production database update policies.
5. **Give experiments a location and lifecycle.** Create the base `experiments/` even when empty; create named subdirectories only for real experiments. Record purpose, active/adopted/closed state and adoption destination. Move already-adopted functionality into `src/` and repair consumers so production no longer depends on the experiment area. Do not promote unapproved experimental behavior merely to clear the layout.
6. **Separate generated outputs.** Put project-controlled results, logs, and caches in `outputs/`, processed data in `data/processed/`. Preserve tool-mandated locations as evidenced exceptions. Never overwrite originals or authored source. Reproducible outputs are normally excluded from source history; preserve required generated code, baselines, synchronized distribution copies, and release artifacts with reasons. Repair only ignore/build/package/deploy paths needed for this migration, without changing release or retention policy.
7. **Name by role, not temporary development state.** Do not multiply editing targets with `new`, `final`, `backup`, or `copy` suffixes. Follow established tool/language naming conventions. Compatibility versions, dataset revisions, and experiment identifiers remain valid; a name alone never proves a violation.
8. **Update connections when structure changes.** Repair imports, execution and data paths, tests, build/package/deploy references, documents, and instructions in the same migration. Update the map when an area/path/policy changes, not for every file addition. Preserve others' unfinished work, originals, and records. Recoverability alone is not permission to delete.

### Mandatory Project Layout

```text
AGENTS.md
<root configuration entry point>
src/<package>/<feature>/
src/<package>/<shared responsibility>/
tests/<feature>/
experiments/<experiment>/
outputs/
docs/README.md
docs/project.md
docs/architecture/overview.md
docs/specs/
docs/plans/README.md
docs/plans/active/
docs/plans/completed/
docs/_meta/manifest.json
```

Create `src/`, `tests/`, `experiments/`, `outputs/`, `docs/architecture/`, `docs/specs/`, and both plan state directories even for an empty or plan-only project. Angle-bracket names are evidence-derived names, never literal placeholders or invented features. Create known planned package/feature directories, but do not implement business logic just to fill them. Git does not retain empty directories: when tracked persistence is required, use a minimal placeholder excluded from runtime behavior; otherwise the scaffold recreates them. Optional data areas are created when inputs exist. Keep the existing native agent bridges and documentation taxonomy in addition to this skeleton.

For multiple applications/packages, place project-owned units under `src/<unit>/`, tests under `tests/<unit>/`, and group settings by unit at the repository root; do not merge independent public interfaces. A framework-mandated path or binding external consumer may require a narrow exception. Record exact path, consumer/constraint, evidence, and compliant alternative in the map. Existing habits, many internal imports, or convenience are NOT exceptions: repair those consumers. A retained authoritative document follows the document-specific rules above, not a blanket exemption for application code. If a real contract prevents safe adoption and no valid exception resolves it, report incomplete migration, not success.

### Central Configuration

Use one documented root editing surface for project-controlled runtime settings and non-secret defaults. Python uses root `config.py`; choose other languages' form from actual tooling, such as `config.ts`/`config.js` where directly supported, or root `config.toml`/`config.json` with a typed loader where executable modules cannot live at root. A proven incompatible runtime/consumer contract may justify a documented native-format exception, not merely an existing preference. Never impose Python on another language. Unknown language means `Not established`, with configuration creation explicitly deferred until that decision; the skeleton and development rules are still established now.

The root surface owns editable values, environment variable names and defaults, override precedence, and required-value/type validation. Lower features receive validated settings through supported imports or dependency injection. A loader may live in source when packaging requires it, but it must not become a hidden second editing home for defaults or tunables. Document how the root source is packaged or supplied for every supported launch mode. No cwd-dependent path hacks, ad hoc `sys.path` mutations, or assumed checkout-only imports.

An unresolved value is not an implicit off/zero/default. Preserve the central validator's rejection instead of replacing it in a feature, test or demo. Authorized trial defaults are scoped at the same root editing surface; they do not approve product defaults or weaken the product contract. A configuration import/loading error must remain visible, not become a fallback execution path.

Move existing tunables out of feature code, reconcile conflicting defaults against current behavior/approved requirements, and remove shadow environment reads and fallback values in consumers. Preserve immutable algorithm constants and genuine per-request inputs where they belong; not every literal is a setting. Keep secrets in the environment or secret store, never in committed root settings or reports. Secret resolution and validation belong to the central configuration boundary; do not expose server secrets in client bundles. Multi-runtime consumers use scoped settings from the same root editing surface, not duplicated defaults.

Root `AGENTS.md` must identify the chosen file, how to add/edit settings, the actual import/injection route, prohibited duplicates/hardcoding, secret handling, and commands to check changes. Creating a config file without rewiring and exercising consumers is not completion. Change a non-secret value at the root and observe the affected feature, test invalid input rejection, and run a supported installed/build/runtime entry path so checkout-only success cannot hide a broken distribution. Restore temporary validation values afterward.

### Structure Refactoring

1. Record worktree state and current supported behavior/commands before mutation. Read plans, rules, source and consumers; separate business contracts from obsolete placement conventions. For a single planning Markdown file, preserve every requirement while moving or mapping it into architecture/spec/plan documents.
2. Classify empty, plan-only, partial or implemented maturity independently from context presence. Inventory old -> standard destination, dependencies, central settings, originals, and narrow exceptions. Use an existing plan or task report, not a per-file registry system. Inspect public consumers before moving paths.
3. Run the create-only scaffold for missing base directories and context files. The agent then edits existing documents and performs semantic migration; the scaffold neither moves application code nor guesses its language. Fill placeholders from evidence, with unknowns explicit.
4. Actually move/restructure task-owned code, tests, inputs, experiments and outputs, centralize settings, and repair all affected references and necessary build/package/deploy/ignore paths. Preserve behavior, data bytes, supported compatibility versions, generated-source provenance, and other workers' edits. Do not create backup project trees. Ask before destructive deletion, irreconcilable collisions or overwrite of unrelated work; stop only the affected action and report it incomplete.
5. Verify pre/post behavior through established checks and the supported execution surface, root configuration propagation and invalid input handling, data preservation and reference integrity. If a baseline cannot run, record the limitation and do not claim equivalence. Plan-only/empty projects have no implemented feature to certify.
6. Update effective agent instructions and the structure map to describe the migrated reality, including remaining gaps. Repeat execution should not reshuffle a compliant project or introduce duplicate instructions. Report structure adoption, config integration, static checks, behavioral evidence and runtime loading separately. Documentation plus empty folders alone never completes an existing-code migration.

### Structure Map

Use one short human/agent-readable table, not a new manifest, ledger, or per-file registry:

| Role | Actual path or external identifier | Management rule, exception, and evidence |
| --- | --- | --- |
| Rules and entry points | Project rule source, human index, effective agent routes | One working authority; report actual loading separately |
| Source and authored work | `src/<package>/<feature>/` and shared responsibility areas | Migrated editing home, or evidenced narrow exception |
| Central settings | Exact root file and lower consumer route | Editable defaults, overrides, validation and supported launch evidence |
| Tests | `tests/<feature>/`, `tests/fixtures/` | Preserved behavioral coverage |
| Original inputs | Dedicated local or external location and version/identifier | Preservation and revision policy |
| Processed data and generated output | Existing output locations | Regeneration, retention, tracking exceptions |
| Experiments | Existing area, if used | Purpose, lifecycle state, adoption destination |
| History and managed copies | Established revision mechanism and copy locations | Version identification, source, consumer, synchronization |

The map records compliance with the mandatory paths, not permission to keep arbitrary old layouts. Mark optional unused roles `Not applicable`, undecided names/language `Not established`, and planned implementation explicitly unimplemented even when its directory exists. Required base directories are never optional. Do not create a second document tree or mandatory per-task report.

If a missing or conflicting map entry prevents a safe location or preservation decision, pause that affected action and record the evidence and decision owner (or `Not established`) in `docs/README.md` under **Unresolved**. Independent authorized work may continue. An exception must cite an approved policy or binding tool/consumer contract; recording a proposed exception does not approve it.

### Adoption And Verification Boundaries

Bootstrap establishes and migrates the structure; maintenance repairs drift or upgrades an established standard; verify-change checks only affected roles and remediates only when authorized. Full application of bootstrap/maintenance includes the necessary structure/configuration refactor, not unrelated feature development. Audit-only/read-only requests never mutate and never report adoption complete. Do not initialize history tools, commit, alter global/runtime agent settings, add hooks or automate CI. Necessary project runtime/build path repairs are distinct from protected agent runtime configuration.

Existing CI definitions are internal consumers too: migration-required path/command-reference repairs are in scope and must be reported. Do not add workflows or change triggers, permissions, secrets, deployment policy, or unrelated gates. Inspect these references before moving their targets. If a required repair exceeds that narrow allowance, block the connected move before breaking the consumer and request the exact missing authorization; never claim successful adoption with a broken workflow. Local command execution validates the repaired path, not hosted CI execution.

At task completion, check affected locations and names, original/output separation, unnecessary copies, and changed references. Keep results in the existing report or task response when no report exists; no new report file is required. Static checks do not prove these semantic rules were followed. When a tool or instruction route changes, use an available authorized fresh session to identify the rule section read and choose a location for one representative file with its rationale, without creating it just for the check. Record that observation and its limits; unavailable runtime checks remain `Needs verification`. Ordinary leaf changes need no four-agent session sweep. Existing feature, build, and test gates still apply.

## Manifest

`docs/_meta/manifest.json` is consumed by tooling, not by readers. It carries one required fact and nothing that churns on an unchanged run.

```json
{
  "standardVersion": "1.4.1",
  "managedPaths": {
    "sharedInstructions": "AGENTS.md",
    "claudeBridge": "CLAUDE.md",
    "kiroSteering": ".kiro/steering/project-context.md"
  }
}
```

Rules: the file must contain a JSON **object** — `null`, an array, or a scalar is rejected with a structured report, never a crash. `standardVersion` is required and must match the acting standard's `VERSION`. `managedPaths` is optional; when present its keys are exactly `sharedInstructions` (required within it, `AGENTS.md`), `claudeBridge` (`CLAUDE.md` or `.claude/CLAUDE.md`), and `kiroSteering` (`.kiro/steering/project-context.md`), each a non-empty string equal to one of its key's canonical paths and present on disk. `schemaVersion` and `docsRoot` are accepted when they carry their established values (`1` and `"docs"`). Keys named `generatedAt`, `updatedAt`, `timestamp`, or `lastRun` are rejected. Any other key is carried without complaint and named in the report, so a manifest persisted under an earlier version keeps passing.

## Legacy Coverage Ledger

A project established under standard `1.1.0` may hold `docs/_meta/coverage-ledger.json`. It is now **optional historical input**:

- `legacy-ledger` reports that it exists, so an agent knows prior audit findings are available to read.
- Nothing validates its schema, and nothing requires it. A project without one is complete.
- No tool in this standard writes, rewrites, or deletes it. Removing or migrating it is a deliberate, user-approved step, and a migration keeps the original copy until the user confirms otherwise.

The retained-source facts a ledger used to hold now live in `docs/README.md` under **Authoritative Sources**, where a reader can follow them.

## What The Tooling Establishes

`standard/tools/jinx_context_check.py` is read-only and deterministic (sorted output, no timestamps). Every check reports `PASS`, `FAIL`, `BLOCKED`, or `NOT_APPLICABLE` with a message naming the offending path, and every report states its own scope.

Its scope is **static structure**: file presence, declared shapes, path safety, links, and anchors. It does not establish that a document is accurate, that its content covers a requirement, or that an agent loaded it at runtime. Those are the agent's recorded judgement, reported separately. A check that cannot establish its subject reports `BLOCKED` or `NOT_APPLICABLE` with the cause, never `PASS`.

| Mode | Check id | Result |
| --- | --- | --- |
| project | `context-present` | `BLOCKED` when neither `AGENTS.md` nor the manifest exists: bootstrap first, do not claim a verified project. |
| project | `manifest-present` | `FAIL` when `docs/_meta/manifest.json` is missing or unparseable. |
| project | `manifest-schema` | `FAIL` when `standardVersion` is absent or not a string, an optional key carries an unsupported value, or a churn-prone key is present. |
| project | `manifest-version` | `FAIL` when `standardVersion` differs from the acting standard `VERSION`. |
| project | `manifest-managed-paths` | `NOT_APPLICABLE` when no `managedPaths` is declared; `FAIL` when a declared path is off-canonical, malformed, or absent. |
| project | `docs-core` | `FAIL` when a core doc is missing or empty. |
| project | `docs-structure` | `FAIL` only when `docs/` itself is missing. Directories outside the recommended names are named in a `PASS` message for the project to justify. |
| project | `archive-no-discovery` | `FAIL` when an auto-discovered agent filename exists under `docs/`. |
| project | `plans-unique` | `FAIL` when the same plan filename appears in more than one plan state. |
| project | `legacy-ledger` | `NOT_APPLICABLE` when no legacy ledger exists; `PASS` naming it as optional historical input when one does. |
| project | `agents-root` | `FAIL` when root `AGENTS.md` is missing or empty. |
| project | `agents-routing` | `FAIL` when root `AGENTS.md` does not route to `docs/README.md`. |
| project | `bridge-no-cycle` | `FAIL` when `AGENTS.md` imports a `CLAUDE.md`. |
| project | `surface-size` | Always `PASS`. Reports the non-blank lines of `AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md`, and the Kiro steering file, what was absent, what it excludes, and whether a goal was exceeded. |
| project | `claude-bridge` | `FAIL` when no effective `@AGENTS.md` / `@../AGENTS.md` bridge exists, or both branches define one. |
| project | `kiro-steering` | `FAIL` when the steering file is missing, lacks `inclusion: always`, or lacks an `AGENTS.md` route and `docs/README.md` fallback. |
| project | `kiro-steering-no-embed` | `FAIL` when steering embeds or imports a whole document. An embed anywhere on an active line counts, including mid-sentence; an example inside a fenced code block does not. |
| project | `links-resolve` | `FAIL` when a relative link has no target. Covers inline `[text](path)`, reference definitions `[label]: path`, and a `[text][label]` usage whose label is undefined. |
| project | `anchors-resolve` | `FAIL` when a `#fragment` link matches no anchor in the target — see [Anchors](#anchors). |
| package | `package-skill-frontmatter` | `FAIL` when `SKILL.md` frontmatter is missing or unparseable, `name` differs from the directory, or no description. |
| package | `package-skill-size` | Always `PASS`, with the line count and a note when it is above the ~120-line goal. |
| package | `package-references-links-resolve` | `FAIL` when a relative link in package-owned Markdown does not resolve. |
| package | `package-references-anchors-resolve` | `FAIL` when a `#fragment` in package-owned Markdown matches no anchor. |
| package | `package-standard-present` | `FAIL` when the package `standard/` copy is missing any required asset: `contract.md`, `VERSION`, both tool entry points, every template, or any `jinxcontext` support module. The full inventory is `tools/jinxcontext/inventory.py`. |
| package | `package-standard-version` | `FAIL` when the package `standard/VERSION` differs from this contract's version, or the copy is incomplete so its version cannot be trusted. |

Package check ids are reported qualified as `<package>:<check>` so several packages can be checked in one run. Template files are excluded from package link checking: their links resolve inside a scaffolded project, not inside the package.

Exit codes: `0` all `PASS`/`NOT_APPLICABLE`, `1` any `FAIL`, `2` any `BLOCKED` with no `FAIL`, `64` usage error. Narrowing `--targets` turns that agent's checks into `NOT_APPLICABLE`; it never hides a failure.

### Anchors

A `#fragment` resolves against three anchor sources, because all three are how real documents are linked:

- the slug a heading generates: lowercased, punctuation dropped, spaces hyphenated. Letters are matched Unicode-aware, so `## 9. API 설계 (FastAPI)` resolves as `#9-api-설계-fastapi` instead of collapsing to an empty slug.
- the `-1`, `-2`, … suffixes a repeated heading receives, in document order.
- an anchor the author declared explicitly, through an HTML `id`/`name` attribute or a `{#custom-id}` heading suffix.

A percent-encoded fragment is decoded before matching, so `#9-api-%EC%84%A4%EA%B3%84-fastapi` and the literal form reach the same heading. Code is an illustration, not a declaration: a heading inside a fenced block is not an anchor, and neither is an explicit `id`/`name` attribute or `{#custom}` suffix shown inside a fenced block or an inline code span. A heading's own inline code stays part of the text its slug is built from.

## Tooling Boundaries

`jinx_context_scaffold.py` creates missing required directories and context files and **never** overwrites, merges, moves, or deletes existing content. Existing destinations are reported `kept`; dry-run writes nothing; repetition produces no diff. Files use exclusive creation. Directory collisions are preflighted along with file destinations. The manifest is create-only too. These tool limits do not restrict the agent's required semantic refactor described above.

It preflights every destination and template before writing anything, and a blocking collision produces **zero** writes:

- a published or generated documentation site: `mkdocs.yml`, `docusaurus.config.js`, `docusaurus.config.ts` at the root, or `docs/_config.yml`, `docs/mkdocs.yml`, `docs/.nojekyll`, `docs/index.html`, `docs/_build`
- a symlinked ancestor or destination — writing through it would place files outside the repository
- an ancestor that exists but is not a directory, so the destination cannot be created
- a directory sitting where the standard requires a file; the scaffold never removes it
- a file, special file, or symlink occupying a required directory
- a template that is missing or unreadable, which would otherwise be written out as an empty file

If a write still fails after the preflight — a permission error, or a template that disappears mid-run — the tool reports each failure as `BLOCKED`, lists what it created before stopping, and exits `2`. A partially applied run is never reported as success. The preflight is a point-in-time check: it does not defend against a path being replaced concurrently between the check and the write, so exclusive creation and the honest failure report are what cover that window.

Neither tool infers semantic architecture, requirements, commands, or ownership — the agent populates every placeholder from actual target evidence, or marks it `Unknown` / `Not established` / `Needs verification`.

Package tooling and repository test assets live in this repository. The skills do not install scripts, hooks, CI, or runtime dependencies into a target project.

## Version Upgrade

### To 1.4.1

`1.4.1` strengthens Kiro IDE/CLI execution guidance without changing the layout, manifest schema or checker scope. It makes the existing central-validation, supported-import and documentation-update requirements explicit in native steering, including temporary demos and trials. Instruction changes are not a claim of behavioral enforcement.

For an established project, read its shared instructions and native steering, then integrate the [Kiro execution checkpoints](#kiro-execution-checkpoints) without replacing unique rules or duplicating requirement authorities. Keep actual project paths and configuration decisions in the shared guide and architecture map. The create-only scaffold does not update existing steering or manifests. Perform any outstanding 1.4.0 adoption work before declaring the current standard; only then update `standardVersion` to `1.4.1`. Record IDE and CLI loading and behavior separately. If testing is deferred, preserve `Needs verification` rather than claiming compliance.

### To 1.4.0

`1.4.0` makes the project skeleton and root central configuration mandatory and makes structure migration part of bootstrap/maintenance. It supersedes 1.3.0's advisory location map and documentation-only migration limits. The manifest schema and static checker scope remain unchanged; the scaffold additionally creates required directories safely. The agent must inspect actual placement and config use: a static PASS does not certify them.

Upgrading an existing project is explicit agent work:

1. Read its current structure, instructions, approved policies, and retained sources. Preserve existing files and records.
2. Perform [structure refactoring](#structure-refactoring), including mandatory directories, root configuration and consumer rewiring. Integrate rules and the resulting map into existing documents and preserve consumer-bound authority. Record incomplete migrations and real conflicts in `docs/README.md`.
3. Connect the human index and affected agent entry points to the same rules. Report static connection and actual fresh-session evidence separately.
4. Only after structural and configuration integration and applicable behavior checks, set `standardVersion` to `1.4.0`. Empty/plan-only projects may record language as unestablished and configuration deferred; unavailable runtime loading stays explicit. Never use the version alone as proof of completion or upgrade it to conceal an incomplete implemented-project migration.

The scaffold keeps existing manifests and architecture documents byte-for-byte. Older manifests fail `manifest-version` until the agent deliberately upgrades them after migration; the scaffold does not install updated skill copies.

### Historical 1.1.0 To 1.2.0 Transition

Standard version `1.2.0` removed the mandatory coverage-ledger machinery: no ledger file, no per-row schema, no digests, no review rows, no per-category manifest state. Retained-source facts moved into `docs/README.md`, and the size caps that could fail a run became advisory reports.

Upgrading from `1.1.0` is explicit, agent-performed work, never a silent rewrite:

1. Fields the older manifest shape carried may stay; nothing requires removing them. For a current upgrade, follow the integration steps above before changing the version.
2. Carry the useful content of an existing `docs/_meta/coverage-ledger.json` into `docs/README.md` under **Authoritative Sources** and **Unresolved**.
3. Leave the ledger file in place unless the user asks for its removal. If they do, preserve a copy until they confirm the migration.

An otherwise structurally compliant `1.1.0` project needs no ledger changes to pass the static checks after a deliberate version update. An unchanged `1.1.0` manifest fails `manifest-version`, which names both versions; that is not a semantic adoption audit.

## Blocking Conditions

Stop and report instead of mutating a scoped surface when: an unsafe collision would overwrite user content; the docs root is a published or generated output tree; a required source is unreadable; plan or spec authority is unresolved; a move would break a named consumer that binds a source in place; or a safe edit would need to overwrite dirty user work. Never redirect the write to an alternate root to avoid the block.
