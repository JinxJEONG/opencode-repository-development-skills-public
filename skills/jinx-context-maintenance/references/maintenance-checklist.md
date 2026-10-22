# Context Maintenance Checklist

Read this reference only when the main workflow needs a detailed comparison, a classification decision, a lesson lifecycle decision, nested instruction review, or final cross-file consistency checking. The fixed paths, manifest fields, and check ids live in [`../standard/contract.md`](../standard/contract.md).

## Comparison Surfaces

Compare existing context against the smallest relevant set of current surfaces:

- Executable source, generated command definitions, and runtime entry points.
- Active configuration, manifests, tool settings, and declared scripts.
- Repository layout, package boundaries, ownership files, and current paths.
- Canonical developer commands and their documented prerequisites.
- Root and nested `AGENTS.md`, Codex overrides, Claude instructions/imports/rules, `.kiro/steering/`, and configured OpenCode instruction sources.
- `docs/specs/`, `docs/plans/`, and `docs/decisions/`, including approval state, implementation state, and verification state as separate fields.
- `docs/README.md`, `docs/project.md`, `docs/architecture/overview.md`, `docs/guides/`, `docs/verification/`, and `docs/_meta/manifest.json`.
- Every source `docs/README.md` names as authoritative outside `docs/`, read again at its current path.
- Agent-facing documents that appeared outside the standard since the last pass, and public or generated documentation as a boundary that migration must not absorb.

Code and active configuration establish current behavior; approved requirements establish intended behavior; instructions establish permitted actions. Recorded checks establish verified behavior. Keep unmet business requirements as gaps and preserve decision history. Repair mandatory layout/configuration drift within an authorized refresh, but hand unrelated business defects to separate work rather than changing requirements.

## Classification Criteria

| Class | Apply when | Required action |
| --- | --- | --- |
| `VALID` | The claim matches current authoritative state and is useful. | Keep it unchanged. |
| `STALE` | A current-state claim is outdated, or a requirement/decision was explicitly superseded. | Correct the current-state claim or record supersession; do not discard unmet requirements. |
| `MISSING` | A durable, necessary fact has no suitable context entry. | Add the smallest accurate statement. |
| `DUPLICATED` | Equivalent guidance appears in more than one place without a scope reason. | Keep one canonical statement and replace copies with a local pointer only when needed. |
| `CONFLICTING` | Applicable instructions or docs prescribe incompatible actions. | Use claim type, scope, and decision evidence; retain unresolved conflicts for the necessary decision. |
| `OBSOLETE` | The material describes a removed, superseded, or no-longer-useful concern. | Retire live guidance and repair references; retain useful decision history with its status. |

Use `Unknown`, `Not established`, or `Needs verification` when evidence cannot establish the classification. Don't turn uncertainty into a fact.

## Update Matrix

| Finding | Minimal update | Do not do |
| --- | --- | --- |
| Wrong command or path | Update the single canonical instruction and affected references. | Change code to fit the document. |
| Missing durable rule | Add it at the narrowest scope that serves all affected readers. | Create a project-specific skill or broad policy. |
| Duplicate guidance | Preserve the canonical source and remove redundant copies. | Scatter near-identical rules across files. |
| Conflicting guidance | Resolve by the authority for that claim and its scope; report unresolved decisions. | Treat code as permission to remove a requirement or instruction. |
| Removed component | Delete stale guidance and dangling links. | Preserve historical instructions as live requirements. |
| Mandatory layout or central-config drift | Perform necessary moves/splits, import/config-consumer repairs, and build/package/deploy path and ignore updates; prove behavior is preserved. | Replace migration with a map update or invent an existing-layout exception. |
| Unrelated business defect | Record evidence and hand off corrective work. | Change business contracts or implement unrelated features during maintenance. |
| New or changed feature | Update its `docs/specs/<feature>.md`, implementation status, architecture, and affected agent pointers. | Infer approval or mark completion without evidence. |
| Missing agent entry point | Add the bridge or steering route the contract requires, in the established branch. | Replace valid user instructions, add a second bridge, or recreate the documentation tree. |
| New agent doc outside the standard | Route its content to the fixed home, repair inbound links, archive the source under a non-discovery filename. | Leave two live authorities for one claim. |
| Structural check failing | Fix the named cause: manifest version, managed path, link, anchor, core doc, or archived filename. | Edit the manifest to describe a structure that does not exist. |
| Retained source changed since it was last read | Re-read it against the document that defers to it, and correct that document's coverage. | Assume the coverage still holds because the structure still passes. |
| Retained source no longer linked by its target | Restore the Markdown link to its exact `path#section` from the document that defers to it. | Name the path in prose and call it a reference, or copy the source's requirements into `docs/`. |
| Retained source missing from `docs/README.md` | Add its row: the source, where its coverage lives, and the consumer that binds it with evidence. | Leave the retention undocumented and report the relocation as complete. |
| Criterion whose authority is the current code | Record it `observed` and raise the missing approval as an open decision. | Label it `approved` because the behavior already exists. |
| Consumer-bound source someone moved into `docs/` | Restore it to the path its consumer reads and record why it stays. | Leave the move in place because the taxonomy looks tidier. |
| Persisted `docs/_meta/coverage-ledger.json` | Read it as prior audit findings and carry what still holds into `docs/README.md`. | Delete or rewrite it; that needs the user's explicit approval and a preserved copy. |
| Unresolved item with no record | Add it to the Unresolved table in `docs/README.md` with its evidence and who decides. | Omit it so the pass reads clean. |
| Plan state incoherent | Keep one canonical authority per plan, label supersession, and match the plan index to the files. | Keep the same plan filename in two states. |
| Surface above its size goal | Move explanation into `docs/`. | Drop a safety rule to hit the number. |

## Structure Rule Maintenance

Read [mandatory project layout](../standard/contract.md#mandatory-project-layout), [central configuration](../standard/contract.md#central-configuration), [structure refactoring](../standard/contract.md#structure-refactoring), and the project's architecture rules/map. Reuse existing classifications and Unresolved records; add no ledger or mandatory report. A missing map and layout/configuration drift in an established standard belong to maintenance. Audit-only reports without mutation; a requested refresh/upgrade performs the necessary migration within scope.

| Compare with live evidence | Disposition |
| --- | --- |
| Editing homes, tests, app/package boundaries, agent routes | Enforce `src/<package>/<feature>/`, `tests/<feature>/`, root `AGENTS.md`, and `docs/{architecture,specs,plans}`; migrate source/tests and repair imports, consumers, maps, and links. |
| Original inputs, transformations, output destinations | Preserve originals, revisions, dirty data, and external identifiers. Repair transformation destinations/consumers safely, never overwrite originals. |
| Experiments and production consumers | Enforce `experiments/<experiment>/` and purpose/state/adoption destination. Move maintained production responsibilities to source and repair dependencies without implementing unapproved behavior. |
| Generated outputs and retention/tracking contracts | Enforce `outputs/`; preserve narrow evidenced tool-required locations, baselines, generated code, distribution, or releases. Repair necessary ignore/build/package/deploy paths, not CI automation. |
| Root central configuration and consumers | Python uses `config.py`; other languages use an evidenced native root settings file. Centralize editable non-secret values/defaults and environment/secret loading/validation; lower modules consume through supported imports/injection, with no hidden defaults/environment reads. Keep algorithmic constants local. |
| Revision mechanism and apparent copies | Trace source, purpose, consumer, selection point and synchronization before classifying. Supported versions and managed workspaces/copies may be `VALID`; unmanaged history copies remain findings, not deletion targets. |
| Newly needed, unused, or planned roles | Always create basic `src/`, `tests/`, `experiments/`, `outputs/`, and required docs directories even when empty. PLAN_ONLY scaffolds evidence-backed known modules/configuration, not business implementation. Unknown language/config choice stays `Not established`. |

Update the map for area/path/policy changes, not every new file. Existing layout doesn't excuse noncompliance; only proven framework/external bindings justify narrow recorded exceptions. Internal imports and adjustable build paths must be repaired. Preserve retained-source authority by exact section link and unresolved genuine business-contract conflicts by record, not silent replacement.

The scaffold is create-only; the agent performs semantic migration. Before declaring adoption, prove real root-config propagation to consumers, invalid-value rejection, supported package/runtime launch without brittle cwd or `sys.path` tricks, affected tests/build gates, and preservation of functionality, contracts, dirty work, and data. An unknown or blocked required check isn't a pass. For PLAN_ONLY, report checks on existing scaffold/config separately from unimplemented business behavior.

Restore the index and effective agent routes to the project authority. After a route change, check discovery and editing-location choice in an available authorized fresh session; a link isn't loading evidence. Report structure adoption, semantic source coverage, agent loading, and feature verification separately. Neither a current manifest nor a static pass proves migration correctness.

## Lessons Lifecycle

| Decision | Use when | Result |
| --- | --- | --- |
| Keep | The lesson is accurate, durable, specific, and still prevents a recurring mistake. | Retain it where it is. |
| Remove | The lesson is disproven, expired, vague, or redundant. | Delete it and repair references. |
| Promote | The same lesson applies across several scopes and has repeated evidence. | Move it to the narrowest shared context that covers those scopes. |
| Replace | An older lesson is superseded by a clearer current rule. | Substitute the old entry, rather than appending another exception. |

Lessons are context, not a changelog. Keep only guidance that helps a future contributor make a correct decision.

## Agent Surface Checks

Apply to all requested targets, defaulting to all four below. Missing local executables leave runtime checks `Needs verification`; they do not justify silently omitting an agent's files. Official behavior was checked on 2026-09-25; recheck documentation when the installed version or loader behavior differs.

| Agent | Inspect and maintain |
| --- | --- |
| Codex | Root/local `AGENTS.md`, existing `AGENTS.override.md`, and instruction discovery settings. Overrides can hide same-directory AGENTS; preserve their exceptions and inspect the effective chain from repository root to launch directory. |
| Claude Code | Root/local `CLAUDE.md`, `.claude/CLAUDE.md`, imports, and `.claude/rules/` conditions. Keep exactly one effective bridge on the established branch: root `CLAUDE.md` with `@AGENTS.md`, or `@../AGENTS.md` in an established `.claude/CLAUDE.md`. Never add a second. Inspect nested coverage separately. |
| Kiro IDE / Kiro CLI | Root/local `AGENTS.md` and `.kiro/steering/`. Restore the mandatory `inclusion: always` route and integrate [execution checkpoints](../standard/contract.md#kiro-execution-checkpoints) into an existing route without embedding documents or discarding native rules. The scaffold does not update an existing file. Preserve other inclusion modes; migrate a `.kiro/specs/` entry into `docs/specs/` or report it blocked, never mirror it. |
| OpenCode | Shared `AGENTS.md` and existing `opencode.json`/`opencode.jsonc` instruction sources. Preserve explicit document-read routing: ordinary links and `@path` text are not automatically imported. Report stale configuration references without editing runtime settings unless authorized. |

Keep exact casing, inspect case variants before creating files, and resolve imports relative to their containing file. Imports must not form cycles; do not import CLAUDE back into AGENTS. Preserve unique native rules and dirty content. Don't turn a scoped or manually included rule into an always-loaded instruction. Personal, local-private, and managed instructions are inspection-only constraints unless the user explicitly includes them in the edit scope.

Claude's default connection is an actual import, even if native AGENTS loading works on this machine; skip it only for a user-selected native-only setup and report its version/settings requirements. Do not remove working imports just because a newer version exists. For an editable repository Codex override hiding shared AGENTS, preserve exceptions and add an explicit read directive to the shared file; do not invent an `@path` import. Report blocked coverage when privacy, scope, conflict, or dirty edits prevent a safe connection. A directive is not runtime proof.

Kiro custom-agent resource inheritance varies with configuration, and its official pages differ on the default: inspect actual resources and loading rather than assuming. Existing settings that block loading must be reported with a concrete follow-up, not silently changed.

Separate IDE and CLI evidence, including installed version and CLI engine/profile when known. Inspect implementations as well as routing: a lower-level temporary default, unresolved-value coercion, caught configuration failure, `sys.path` workaround or missing command/docs update remains a finding even if the agent read the guide and its tests passed. Strengthen the existing project-local execution reminders, not global profiles. When the user defers testing, leave behavior/loading `Needs verification` and do not start validation sessions.

For each agent report `entry points | local/conditional rules | changed/preserved/native-covered/blocked | static checks | runtime evidence`. When available, inspect fresh-session loader diagnostics and a representative nested scope. Do not install or authenticate another agent solely for verification. Keep static validity, observed loading, and behavioral compliance distinct.

Official sources: [Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Claude Code](https://code.claude.com/docs/en/memory), [Kiro steering](https://kiro.dev/docs/steering/), [Kiro resources](https://kiro.dev/docs/custom-agents/configuration-reference/), [OpenCode](https://opencode.ai/docs/rules/).

## Local Instruction Review

For each nested instruction file, verify that it:

- Applies to a real subtree with a distinct local need.
- Adds or overrides only rules relevant to that subtree.
- Doesn't contradict applicable parent instructions without an explicit, evidence-based local reason.
- Doesn't duplicate parent guidance merely for convenience.
- Refers to current paths, commands, configuration, and ownership boundaries.
- Has no stale references to removed files, tooling, or components.

Preserve each guide's explicit subtree scope and parent constraints. Verify each target agent's actual loading; do not assume that every tool discovers or combines nested guides identically. A root Claude import does not automatically import every nested AGENTS file; add scoped bridges when needed. Kiro may load AGENTS files across the workspace, so local instructions must state where they apply.

## A Second Pass Is A Real Re-Read

A repeat pass re-reads live sources. Re-running a create-only scaffold isn't a semantic check: existing files remain untouched.

1. Re-read every authoritative source in `docs/README.md` at its current path. A static pass says nothing about content accuracy.
2. Confirm `requirement -> exact authoritative clause -> coverage document -> implementation state -> verification state`. Implementation and verification are independent; implemented without a recorded check is `unverified`.
3. Confirm each retained source has an exact-section Markdown link, `docs/specs/<feature>.md` acceptance coverage, an existing binding consumer, and no duplicate editable requirements under `docs/`.
4. Close resolved items in Unresolved, add new findings, and retain genuine conflicts with both sources and the needed decision. Safe reference integration isn't a conflict.
5. Account for every normative clause, including uncovered ones, as met, an open gap, or a conflict. Don't drop inconvenient clauses to make the pass look clean.

Report this judgement separately from the static checker. Neither replaces the other; a clean run over unread sources isn't an audit.

## Final Consistency Checks

1. Re-run `../standard/tools/jinx_context_check.py --root <repo>`; it passes or each remaining item is reported blocked with a named cause. Its scope is static structure, not coverage.
2. Re-read changed context with applicable shared instructions and native agent surfaces.
3. Resolve changed paths, commands, document links, imports, and references; check inbound references to moved material.
4. Confirm required behavior, observed code, and verified behavior stay distinct, that implementation and verification are separate recorded states, and that intended requirements and decisions remain intact.
5. Confirm plan state is coherent: one canonical authority per plan, disjoint states, supersession labelled, index matching the files.
6. Confirm each classification has evidence and each `Unknown` item is labelled rather than guessed.
7. Confirm code/config and build/package/deploy path or ignore edits are necessary to authorized migration, preserve business behavior, and have consumer checks. No new skills, dependency upgrades, agent runtime/global edits, installed package tools, hooks, watchers, background/self-improvement flows, or Git/CI automation.
8. Confirm this maintenance pass didn't claim to verify an individual feature or replace `jinx-verify-change`, and didn't report a bootstrap handoff as completed maintenance.
9. Confirm unchanged inputs would not add duplicate imports, copies, or timestamps, and unrelated worktree changes remain preserved.
