---
name: jinx-verify-change
description: Verify an implementation, fix, or refactor against acceptance criteria and existing checks, including affected agent context; not repository context setup or broad maintenance.
---

# Verify Change

Use this after a change is complete enough to check. It verifies the affected behavior with the smallest sufficient set of *existing* project checks and reports evidence, not confidence.

## Inputs And Output

Treat the current change as the task-owned file boundary, not every unrelated working-tree edit. Accept a Git comparison, supplied diff, explicit file list, or reproducible non-Git inventory as evidence of that boundary.

Produce an evidence-based report with a per-check result: `PASS`, `FAIL`, `BLOCKED`, or `NOT_APPLICABLE`. A required check whose result is unknown or blocked cannot yield an overall pass. Use the template in the reference without omitting unknowns.

## Three Layers Of Evidence

Every verification covers the layers the change actually touches, and never substitutes one for another:

1. **Structure and static checks**: `standard/tools/jinx_context_check.py --root <repo>` for the context surface, plus the project's own lint and type checks. Read-only, deterministic, and static only: it never establishes semantic coverage or runtime loading, and every report states that scope itself.
2. **Spec-to-code consistency**: for each affected `docs/specs/<feature>.md` criterion, does the code satisfy it, and are implementation and verification states separate? An unmet criterion is a gap, not a document to rewrite. Read exact clauses from retained authoritative sources, not a paraphrase under `docs/`.
3. **Real behavior**: the project's existing tests and, for a user-facing surface, actual use through the real path.

Documentation checks passing on a plan-only feature means the *docs* are consistent. It never means the feature is verified; record that explicitly. A clean structural run is the same kind of result: it establishes the shapes it measured, and nothing about whether a document's content is right.

## Workflow

1. Discover the change. In Git, inspect the working tree, staged changes, and the established comparison base. Outside Git, use the task's change list, a reproducible inventory, or a supplied diff. Mark an unknown boundary as unknown instead of guessing.
2. Load instructions before planning checks: root and local `AGENTS.md`, Codex overrides, Claude instructions and rules, Kiro steering, configured OpenCode sources. Follow the active agent's actual loading and each rule's scope; report unresolved conflicts. Read the applicable specs as intended behavior even when code differs.
3. Build the affected scope. Trace callers, consumers, shared types, contracts, generated outputs, configuration, and tests. Classify the impact tier with [the verification strategy](references/verification-strategy.md).
4. Choose canonical commands: named by applicable instructions and `docs/project.md`, then package scripts, task runners, build configuration, existing CI definitions, and nearby focused tests. Never invent a command or substitute an assumed equivalent. When none is established, record `Not established` / `BLOCKED` rather than a plausible substitute.
5. Run the minimum sufficient verification across the three layers the change touches, including [structure rule verification](references/verification-strategy.md#structure-rule-verification) for affected file placement, inputs, experiments, outputs, or copies. Record each command, working directory, result, and the behavior it covered. For a user-facing surface, record the real path used, the steps, and the observed result.
6. Attribute every failure from evidence: `caused by current change`, `pre-existing failure`, `environment problem`, or `unknown`. A failure is not pre-existing without a clean comparison, prior evidence, or a reproducible unchanged baseline. Never claim a cause the evidence does not support.
7. When the change touches a source `docs/README.md` names as authoritative outside `docs/`, confirm the record still holds: the source exists at that path, its named consumer still binds it, the document carrying its coverage still links the exact sections, and that coverage still matches the clauses that changed. A changed retained source needs a fresh read, not an updated pointer.
8. When remediation is authorized, fix only failures caused by the current change and update affected task-owned docs or agent references. Never weaken requirements/checks to pass a gate, break a retained-source binding, copy mutable requirements into `docs/`, or remove persisted records. Re-run affected checks and reassess impact when scope changes. A read-only request makes no edits.
9. Report using the reference's template, with each check's result and every unknown, blocked, and unverified item stated.

## Selective Reference Loading

Read `references/verification-strategy.md` when selecting an impact tier, resolving command precedence, mapping behavior to checks, handling a non-Git workspace, attributing a failure, escalating scope, or composing the report. A routine narrow change may use it only for the template.

When instructions, commands, paths, specifications, or architecture change, use [agent context verification](references/verification-strategy.md#agent-context-verification). Default targets are Codex, Claude Code, Kiro, and OpenCode unless narrowed; none is assumed installed, and a leaf change does not require four runtime sessions.

Read `surface-size` as guidance, not a gate: it always passes, and an over-goal surface is trimmed by moving detail into `docs/`, never by deleting a rule to satisfy it.

Read [mandatory project layout](standard/contract.md#mandatory-project-layout), [central configuration](standard/contract.md#central-configuration), and [structure refactoring](standard/contract.md#structure-refactoring), then the project's architecture rules and map. Check affected paths against `src/<package>/<feature>/`, `tests/<feature>/`, `experiments/<experiment>/`, `outputs/`, `docs/{architecture,specs,plans}`, root `AGENTS.md`, and language-native root central configuration. Required basic directories may be empty but not omitted. Python uses root `config.py`; an unknown language's configuration choice is `Not established`.

Existing paths aren't exceptions; only proven framework or external bindings justify a narrow recorded exception. Internal imports must be repaired. Check real config propagation, invalid-value rejection, and supported package/runtime launch when configuration or migration is affected; no hidden defaults/environment reads below the root config and no brittle cwd/`sys.path` tricks. Keep algorithmic constants local. Don't turn verification into broad initialization or migration: authorized remediation stays change-scoped, audit/read-only makes no edits, and broader adoption gaps go to bootstrap or maintenance.

Naming alone can't distinguish a supported version or distribution copy from an unmanaged history snapshot. Include semantic compliance separately from static integrity and feature behavior in the existing report. PLAN_ONLY scaffolding and a structural pass never establish feature completion.

## Completion Criteria

Complete only when the change boundary is evidenced, applicable instructions and acceptance criteria were consulted, checks match the affected scope, every required check has a recorded result, failures are attributed from evidence, and remediation was reverified. For affected agent context, keep static structure, coverage judgement, and observed loading separate per target. State every unverified item and risk explicitly. Do not report an overall pass while a required check is `FAIL`, `BLOCKED`, or unknown.

## Safety Boundaries

- Do not perform unrelated refactors, dependency upgrades, full-repository formatting, or any unrelated change while verifying.
- Do not hide, delete, or disable tests; weaken lint, type checks, or acceptance criteria; silently change CI; invent commands; or automate Git, CI, commits, pushes, pull requests, or releases.
- Do not redesign the context standard or perform long-term context maintenance here.
- Do not install scripts, hooks, CI, or runtime dependencies into the target project. This package's checker runs from the installed skill; the repository that develops these packages owns its own test assets.
- Do not generate project-specific skills or auxiliary deploy, debug, database, frontend, backend, code-review, test, or release skills; no self-improvement loops or background agents.

## Non-responsibilities And Handoffs

This skill doesn't initialize a standard or repair broad drift. Hand first-use setup to `jinx-bootstrap`, including `BLOCKED context-present`, and established-standard drift/upgrades to `jinx-context-maintenance`. If a required command, environment, credential, or cause can't be established within scope, include the boundary, attempted command, failure, attribution, and needed follow-up in the handoff.
