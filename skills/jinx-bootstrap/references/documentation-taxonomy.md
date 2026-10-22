# Documentation Taxonomy And Canonical Sources

Use this reference during initial context setup to classify existing material, identify authoritative sources, and decide which documents the fixed taxonomy actually needs. The category names and paths themselves are fixed by [`../standard/contract.md`](../standard/contract.md); this file decides what belongs in each. Routine drift in an established context architecture belongs to `jinx-context-maintenance`.

## Classify By Role, Not Filename

| Role | What it establishes | Standard home |
| --- | --- | --- |
| Execution instructions | Applicable rules, commands, validation expectations, and preservation boundaries | Root `AGENTS.md` task router, the Claude bridge, `.kiro/steering/project-context.md`, and justified nested guides |
| Product or contract specification | Required behavior and acceptance criteria, with approval state if evidenced | `docs/specs/<feature>.md` |
| Plan or current work | Intended sequence, unresolved work, and status at a stated point | `docs/plans/active/<task>.md`, then `docs/plans/completed/` |
| Architecture explanation | Observed units, responsibilities, dependencies, and flows | `docs/architecture/overview.md` |
| Decision record | Decision, rationale, status, and what it supersedes | `docs/decisions/` |
| Procedure or runbook | How to perform a scoped operation and its prerequisites | `docs/guides/` |
| Verification record | What was checked, how, and the result | `docs/verification/` |
| Generated reference | Derived API, schema, or other generated documentation | Its generator and maintained input; do not hand-edit output or move it into `docs/` |
| Historical or superseded material | Earlier state or decisions, not live instructions | `docs/archive/<name>-superseded.md`, never an auto-discovered agent filename |
| Navigation | How to find the above without repeating their content | `docs/README.md` |
| Human or published product documentation | Product-facing material for a non-agent audience | Its evidenced publishing home; preserve content and repair migration-affected consumers without absorbing it into agent docs |
| Consumer-bound technical contract | Required values a named consumer reads or publishes by path | Its existing path, retained as authoritative, with `docs/specs/<feature>.md` acceptance coverage linking its exact sections |

One file may mix roles; classify sections before proposing a split. Filenames such as `SPEC.md`, timestamps, or polished prose do not establish approval or authority.

## Canonical-Source Classification

For material relevant to the setup, record `path/section | role | authority | validity | evidence | action/destination`. Keep this inventory in the audit report unless the repository needs a maintained index; do not create an extra registry by default.

- **Authority**: canonical for a named claim and scope, supporting/derived, historical/superseded, or unresolved. A file is not universally canonical just because one of its sections is authoritative.
- **Validity**: `VALID`, `STALE`, `MISSING`, `DUPLICATED`, `CONFLICTING`, or `OBSOLETE`, where evidenced. Use `Unknown`, `Not established`, or `Needs verification` when evidence does not support a decision. An unmet approved requirement is an implementation gap, not automatically a stale document.
- **Evidence**: defining path and section/symbol, applicable instruction, explicit decision status, or observed command result. Identify the conflicting sources when authority is unresolved.

Choose authority by the question being answered:

1. **What runs now?** Prefer current executable configuration, source, and observed results using [the context standard](context-standard.md#stack-commands-and-sources-of-truth). A passing test only establishes the behavior it actually exercised.
2. **What should be built?** Use the applicable specification or accepted decision for intended behavior. Record its status and implementation gap; do not infer approval or rewrite requirements to match a defect.
3. **What may an agent do?** Follow applicable instructions and the user's authorized scope. Code and command availability cannot override preservation rules or grant execution permission.
4. **Why or when was it decided?** Use the decision or historical record for its stated period. Keep it distinguishable from live operational guidance.

Each claim gets one editable home, normally in the fixed taxonomy. A retained source with an established binding contract remains the home for its clauses; `docs/` links exact sections instead of restating them. Two editable homes are a duplicate-authority defect regardless of which is "canonical". Record it under Authoritative Sources in `docs/README.md` per [the contract](../standard/contract.md#authoritative-sources-outside-docs) and [migration steps](migration.md#a-source-a-consumer-binds-in-place). This protects retained technical authority, not arbitrary source-code paths: repairable internal imports aren't exceptions to mandatory layout.

Where two equally applicable sources disagree and evidence cannot resolve them, preserve both, record the conflict as blocked, and ask only for the decision needed to proceed. A safe reference integration is not a conflict and is not blocked. Do not invent ownership or choose authority by filename or recency alone.

Record where each acceptance criterion came from, separately from what it says. A criterion traceable to an authoritative clause or an accepted decision is approved. A criterion read off current behavior is `observed`, and one you wrote this pass is `proposed`: neither becomes approved because it is written down. Observed behavior is evidence about the system, never the requirement the system must satisfy, so an unapproved criterion is reported as an open decision.

## Minimize And Reorganize Existing Material

For each change, name evidence, preserved content, destination, and affected consumers/links before editing. Setup or refresh authorizes necessary structural code/config and documentation migration under [structure refactoring](../standard/contract.md#structure-refactoring); audit-only makes no edits. Don't move material across visibility or permission boundaries without authorization.

| Decision | Use when | Preservation check |
| --- | --- | --- |
| Keep | Accurate, useful, correctly scoped | Leave valid wording and location intact |
| Correct | A current-state claim or pointer is disproven | Correct the claim from evidence; preserve intended requirements |
| Link | A fact already has an authoritative home | Replace redundant detail with a pointer; retain critical execution rules where they apply |
| Move | Useful content belongs to a different audience or scope | Keep its meaning and scope, repair inbound links/anchors, and leave a pointer when needed |
| Merge | Overlapping material has one evidenced canonical home | Carry over all unique valid constraints before removing copies |
| Retire | Supersession or removal is established | Preserve decision history; prefer a status label or archive for useful history, and repair references |

For each `AGENTS.md` section, ask whether removing it would cause a concrete execution mistake. Keep repository-specific commands and constraints that pass this test. Relocate explanatory architecture detail to its canonical document when useful; remove only evidenced redundancy or obsolete guidance. Do not shorten by deleting safety constraints, unresolved requirements, or local exceptions. Existing dirty content is not disposable; if an edit overlaps work that cannot be safely preserved, defer that edit and report it.

Core docs and basic directories are required under [mandatory layout](../standard/contract.md#mandatory-project-layout); optional documents need a durable purpose. Empty categories need no placeholder files, but required directories are always created. Use [the migration map](migration.md) for moves and consumer repairs, without leaving duplicate editable documents. A retained source is recorded and linked as an exception, not a stray duplicate. [Central configuration](../standard/contract.md#central-configuration) remains a runtime authority whose consumers must be wired and tested, not another prose summary.

## Completion Check

Re-read changed instructions with applicable parents, local guides, and native agent surfaces. Run `../standard/tools/jinx_context_check.py --root <repo>` to resolve links and anchors and to confirm the core structure holds; check inbound references before retiring paths. Use [agent file setup](agent-files.md) for tool-specific loading. Confirm retained rules keep their scope, that implementation and verification state remain distinct fields, and that the final diff preserves unrelated work. Report the checker's static result and your own coverage judgement separately, and report deferred or blocked restructuring separately from actual changes.

## Design Source

[mblode AGENTS.md audit](https://github.com/mblode/agent-skills/blob/ec7f60811b30aa5eb0be58772cedbfc86454186f/skills/agents-md/SKILL.md) informs the execution-contract test. This taxonomy keeps that test within the three-skill lifecycle; native entry-point maintenance uses the agent file reference and does not require external skills or new automation.
