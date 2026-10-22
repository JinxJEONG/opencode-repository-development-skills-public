# Verification Strategy

Fixed paths, check ids, and exit codes are defined in [`../standard/contract.md`](../standard/contract.md).

## Result Vocabulary

| Result | Use when |
| --- | --- |
| `PASS` | The check ran and the behavior it covers held |
| `FAIL` | The check ran and the behavior it covers did not hold |
| `BLOCKED` | The check could not run: no canonical command, missing environment, unavailable credential, unresolved authority |
| `NOT_APPLICABLE` | The change does not touch what the check covers, with a stated rationale |

A required check that is `BLOCKED` or unknown cannot produce an overall pass. `NOT_APPLICABLE` requires a rationale; it is not a way to retire an inconvenient check. Never relabel a `FAIL` to clear a gate.

## Determine Impact

| Tier | Typical change | Minimum evidence |
| --- | --- | --- |
| Narrow | Isolated leaf logic, copy, or a focused test | Focused test or direct user surface check, plus required local quality checks |
| Connected | Module behavior, public function, route, schema, or configuration | Focused tests and dependent consumer checks, plus applicable type, lint, or build checks |
| Shared or core | Shared type, library, authentication, data contract, build tooling, or widely used configuration | Targeted consumer checks, required project gates, integration or manual surface evidence, and a documented scope review |

Treat an unknown dependency boundary as connected until evidence narrows it. Increase the tier when a changed contract, generated artifact, migration, user-visible behavior, or shared configuration can affect consumers outside the edited files.

## Choose Commands

Use the first applicable source in this order:

1. Applicable shared and native agent instructions, respecting the active tool's loading and explicit rule scope.
2. Project documentation that names verification commands or required gates.
3. Package scripts, task-runner definitions, or tool configuration owned by the project.
4. Existing CI definitions as a source for commands and requirements. Authorized change-scoped remediation may repair migration-required path/command references under the contract, never silently alter triggers, permissions, deployment policy or unrelated gates.
5. Nearby focused tests or established local developer commands.

If sources conflict, apply established instruction authority and scope; report unresolved conflicts rather than selecting by filename alone. If no canonical command exists, report `Not established`, run only checks whose purpose is clear from the repository, and do not invent a replacement command. Existing code establishes observed behavior, not the acceptance criteria it must satisfy.

## Map Scope To Verification

| Changed surface | Verification evidence |
| --- | --- |
| Pure implementation logic | Focused unit or module test, then required local type or lint check |
| Public API or shared type | Focused producer and consumer tests, type check, and contract or integration evidence when available |
| User-facing UI or CLI | Focused automated check plus direct manual use through the real surface |
| Configuration, build, or tooling | Canonical validation/build, real root-config propagation to affected consumers, invalid-value rejection, and supported package/runtime launch |
| Agent instructions or context structure | `../standard/tools/jinx_context_check.py --root <repo>`, plus the behavior check the instruction directs when practical |
| Specification or acceptance criteria | Per-criterion spec-to-code comparison, and the existing test or real-surface step that criterion names |
| A source `docs/README.md` names as authoritative outside `docs/` | That source's clauses and the document carrying its coverage, re-read against the change |

Run the smallest set that covers the actual risk. A shared or core tier must not be treated as narrow merely because the diff is small.

## Structure Rule Verification

Use [mandatory project layout](../standard/contract.md#mandatory-project-layout), [central configuration](../standard/contract.md#central-configuration), [structure refactoring](../standard/contract.md#structure-refactoring), and the project's architecture rules/map against the affected change. Don't turn a leaf change into broad initialization or migration. Established-standard drift goes to maintenance; first setup goes to bootstrap. An unresolved rule needed by this change is `BLOCKED`, not permission to guess.

| Affected role | Evidence to inspect |
| --- | --- |
| Authored files and tests | Required `src/<package>/<feature>/` and `tests/<feature>/` homes, root `AGENTS.md`, and `docs/{architecture,specs,plans}`; basic directories must exist even if empty. Existing layout and repairable internal imports aren't exceptions. |
| Original inputs and transformations | Input/output arguments and write paths, revision identifiers, and a safe existing test or disposable-data run when needed. Never test preservation by risking the real original. |
| Experiments or adopted work | `experiments/<experiment>/`, recorded purpose/state/destination and production imports/build/delivery consumers; production must not depend on experiment execution. |
| Generated output | `outputs/`, generation destinations, and narrow proven framework/external path or retention/tracking exceptions. A tracked baseline or distribution copy isn't automatically a violation. |
| Central configuration | Python root `config.py`, otherwise an evidence-backed native root settings file; unknown language choice is `Not established`. Root owns editable non-secret values/defaults and environment/secret loading/validation. Lower modules consume supported imports/injection, not hidden defaults or environment reads. Keep algorithmic constants local. |
| Apparent duplicates or versions | Purpose, current editing source, selection/connection point, history mechanism and synchronization. Folder names alone are insufficient. |
| Changed locations or policies | Updated map and inbound links, imports, build configuration and real execution paths affected by the move. |

Record result, evidence, and gaps in the existing report. Unaffected roles are `NOT_APPLICABLE` with a reason; a proven violation is `FAIL`. Only a proven framework or external binding permits a narrow recorded path exception. Unknown or blocked required claims prevent an overall pass. Byte comparisons or safe disposable-data execution can establish input protection; declarations alone can't.

For configuration or migration changes, prove a real value change propagates through affected consumer paths, invalid values are rejected, and supported package/runtime launch works. Don't count a config-file assertion or consumer-bypassing mock as propagation, and don't use brittle cwd assumptions or `sys.path` tricks. Keep affected feature/test/type/build gates; structural adoption doesn't replace business verification.

Authorized remediation may repair task-owned moves/splits, imports, config consumers, and necessary build/package/deploy paths or ignore rules caused by the change. Read-only/audit makes no edits. Don't initialize the whole layout, repair unrelated drift, delete records/copies without approval, change business contracts, upgrade dependencies, or automate Git/CI to clear a gate. Broader adoption goes to bootstrap/maintenance. After an agent route change, use an available authorized fresh-session discovery/location-choice check and report its limits. Ordinary leaf edits don't require four runtime sessions.

## Spec-To-Code Consistency

For each affected criterion in `docs/specs/<feature>.md`, record `criterion | required behavior | authoritative source | observed code | implementation state | verification state`. Implementation and verification are independent: an implemented criterion with no recorded check result is `unverified`, never verified. Three outcomes are legitimate for the criterion itself: met with evidence; an implementation gap recorded honestly; or a state that cannot be established, recorded `BLOCKED`. Rewriting the criterion to match current behavior is not one of them.

When a requirement lives in a retained source listed under Authoritative Sources in `docs/README.md`, read its exact clauses. A paraphrase under `docs/` isn't the requirement; a mismatch is a duplicate-authority defect, not a licence to pick whichever reads better.

Check each criterion's provenance before treating it as binding. A criterion traceable to an authoritative clause or an accepted decision is approved; one derived from what the code does is `observed`; one written during this pass is `proposed`. Code establishes observed behavior, never the requirement it must satisfy, so a criterion with no authority behind it is an open decision, not a satisfied requirement. A criterion must also map to the individual clause it covers: a table naming a section and summarizing it hides which clauses have coverage.

Record what a check actually exercised. A test asserting that a document still declares a value proves the document's content and location; it proves nothing about the application behavior that value governs. That criterion's verification covers the document fact only, and the behavioral criterion stays `unverified`.

A plan-only feature can have consistent documentation and zero verified behavior. Report `docs consistent: PASS`, scaffold/configuration check results where applicable, and `feature behavior: NOT_APPLICABLE (not implemented)` separately. Never combine them into a pass implying the feature works.

## Retained Source Verification

When a change touches a retained source listed in `docs/README.md` or its `docs/specs/` coverage:

| Condition | Required result |
| --- | --- |
| The retained source changed | Re-read its clauses against the document that carries its coverage, and correct that document. A passing structural run is not a re-read. |
| The document no longer links its source | `FAIL`: repair the Markdown link to the exact `path#section`. `anchors-resolve` catches a broken fragment; a path named in prose satisfies nothing. |
| A cited section no longer exists in the source | `FAIL`: re-map the citation to the clause's current heading and re-read it. |
| A named consumer no longer exists | `FAIL`: restore the consumer, or correct the row in `docs/README.md` to what actually binds the source now. |
| A moved or deleted consumer-bound source | `FAIL`: restore it. Moving such a source to satisfy the taxonomy breaks the consumer that binds it. |
| The requirement was copied into `docs/` | `FAIL`: two editable homes for one requirement. Replace the copy with a section link. |
| The coverage cannot be established within this change's scope | No overall pass. Report the outstanding work and hand it to `jinx-context-maintenance`. |

## Agent Context Verification

For changes to instructions, commands, paths, specifications, or architecture, check affected canonical docs and their consumers for all requested agents, defaulting to Codex, Claude Code, Kiro, and OpenCode. If context is unaffected, record that assessment and skip unrelated loader tests.

Start with `../standard/tools/jinx_context_check.py --root <repo>` for read-only static integrity. It reports its scope and managed-surface size guidance; it doesn't establish semantic coverage, migration correctness, or runtime loading.

| Consumer | Evidence to inspect |
| --- | --- |
| Codex | Applicable AGENTS chain and existing overrides from root to launch directory; an override may hide the changed ordinary guide. |
| Claude Code | The one effective bridge on its established branch, or native AGENTS loading, including local `.claude/rules/` conditions. Verify imported paths, cycles, and nested scope independently of the root bridge. |
| Kiro IDE / Kiro CLI | Shared AGENTS and `.kiro/steering/project-context.md` with `inclusion: always` and [execution checkpoints](../standard/contract.md#kiro-execution-checkpoints), plus preserved scoped steering. Inspect effective custom-agent resources and application/version/CLI engine separately. One surface's successful loading is not proof for the other. |
| OpenCode | AGENTS and configured instruction sources; a plain link or `@path` is not proof of automatic import. |

Check exact filename casing, links, imports, commands, preservation of tool-specific rules, and intended versus implemented status. Check that a second context refresh would not duplicate bridges or rewrite unchanged facts. Do not equate static integrity with actual loading. Use loader diagnostics in a fresh session when available and authorized; record unavailable versions, tools, credentials, or blocked settings as `BLOCKED` / `Needs verification`. Do not assume Codex, Claude Code, Kiro, or OpenCode is installed, do not install or authenticate a tool merely to clear this report, and do not rewrite runtime settings or personal instructions.

Official references, checked 2026-09-25: [Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Claude Code](https://code.claude.com/docs/en/memory), [Kiro steering](https://kiro.dev/docs/steering/), [Kiro resources](https://kiro.dev/docs/custom-agents/configuration-reference/), [OpenCode](https://opencode.ai/docs/rules/). Recheck version-dependent behavior when needed; Kiro's steering and custom-agent pages differ on default inheritance, so inspect effective configuration.

Keep corrections within the current change boundary and authorization. Report existing missing bridges or broad drift for `jinx-context-maintenance`, and `BLOCKED context-present` for `jinx-bootstrap`. Do not label a feature verified merely because all instruction files exist or all documentation checks pass.

For Kiro behavioral evidence, compare actual source and commands against the project's rules before trusting the agent's report or tests. Specifically inspect trial defaults outside the root settings surface, unresolved/invalid values converted to defaults, configuration errors caught to continue, path mutation in demos/tests, and missing canonical documentation updates. A test that expects the prohibited fallback demonstrates the mismatch, not compliance. When authorized to run a scenario, derive expected behavior from the existing contract and exercise the real root loader and consumer; do not supply the desired implementation paths as the scenario's answer. If testing is deferred, do not run this scenario, static checks or fresh-session probes; record `Needs verification` with the user's reason.

## Discover Changes

For Git, inspect unstaged and staged diffs, status, and the agreed comparison base. Include untracked files when relevant. Do not assume every working-tree change belongs to the current task.

For non-Git workspaces, use the supplied change list, a reproducible file inventory, timestamps only as supporting evidence, and task context. State the method and its limits. If no boundary can be established, stop short of a complete verification claim.

## Attribute Failures

| Attribution | Required evidence |
| --- | --- |
| `caused by current change` | Failure follows the changed path and disappears when the current change is corrected, or a direct causal link is reproduced |
| `pre-existing failure` | The same failure occurs on an unchanged comparison or is supported by trustworthy prior evidence |
| `environment problem` | A missing dependency, unavailable service, credential, platform condition, or tool failure is reproduced independently of the changed behavior |
| `unknown` | Evidence does not meet another category |

Never relabel a failure to pass a gate. Preserve its output, record the command and environment facts that matter, and re-run affected checks after each correction. Escalate when a required command is missing, the scope crosses a shared boundary without a viable check, a failure remains unknown, a necessary environment dependency is unavailable, or verification would require forbidden changes.

## Final Report Template

```text
Change boundary: <Git comparison or non-Git discovery method and limits>
Affected scope and tier: <files, consumers, tier, rationale>
Instructions and docs consulted: <paths and purpose>
Structure and static checks: <check id -> PASS|FAIL|BLOCKED|NOT_APPLICABLE, with cause; static structure only>
Structure adoption: <affected roles -> result, actual/required paths, binding exceptions, migrations, unresolved gaps; NOT_APPLICABLE with reason for unaffected roles>
Configuration migration: <real propagation, invalid-value rejection, supported package/runtime launch -> results/evidence; or NOT_APPLICABLE with rationale>
Spec-to-code consistency: <criterion -> required behavior, authoritative source, observed code, implementation state, verification state; or NOT_APPLICABLE with rationale>
Retained sources: <affected source -> clauses read, document carrying its coverage, result; or NOT_APPLICABLE with rationale>
Agent context: <unaffected with rationale, or per-agent entry points, static checks, runtime evidence, gaps, and handoff>
Behavior verification: <command, working directory, result, behavior covered>
Manual checks: <real surface, steps, observed result, or NOT_APPLICABLE with rationale>
Failures: <attribution, evidence, remediation, reverification>
Unverified items: <none, or each item with why it is BLOCKED or unknown>
Risks: <none or residual risk>
Cleanup: <files or artifacts removed, or none>
DoneClaim: <what the evidence establishes and what it explicitly does not establish>
```

Every required row carries a result. An overall pass is only legitimate when no required row is `FAIL`, `BLOCKED`, or unknown.
