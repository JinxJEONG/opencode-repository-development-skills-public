---
name: jinx-context-maintenance
description: Audit, repair, and upgrade an established mandatory project layout, central configuration, and agent context standard; not initial setup or feature verification.
---

# Repository Context Maintenance

## Purpose

Keep an established standard accurate and adopted as the repository changes. Restore missing structure and context, repair layout/configuration drift, and perform standard upgrades. It doesn't bootstrap one from scratch.

## When To Use

Use when the standard exists and needs an audit or wider agent coverage. Signals include new features, changed contracts, stale commands, renamed paths, a missing bridge or steering route, scattered new agent docs, conflicting instructions, or obsolete lessons. A missing Claude bridge or Kiro route alone does not require repeating bootstrap.

Do not use this for a repository with no context standard: run `standard/tools/jinx_context_check.py --root <repo>` and, on `BLOCKED context-present`, hand the work to `jinx-bootstrap` rather than claiming maintenance is done. Do not use it to prove an implementation works; that is `jinx-verify-change`.

## Scope Default: Full Audit

Default to a **full audit** of live layout, application configuration and consumers, root and nested `AGENTS.md`, the Claude bridge and rules, `.kiro/steering/`, configured OpenCode instruction sources, and `docs/`. A refresh or upgrade includes necessary structural repairs. Narrow to a **change-scoped refresh** only when explicitly requested; still run the static checker repository-wide and report out-of-scope findings without silently fixing them.

An audit-only request produces classifications and recommendations without editing files.

## The Standard

[`standard/contract.md`](standard/contract.md) is the authority. Read [mandatory project layout](standard/contract.md#mandatory-project-layout), [central configuration](standard/contract.md#central-configuration), and [structure refactoring](standard/contract.md#structure-refactoring). Enforce `src/<package>/<feature>/`, `tests/<feature>/`, `experiments/<experiment>/`, `outputs/`, `docs/{architecture,specs,plans}`, root `AGENTS.md`, and language-native root central configuration. Basic directories always exist, even when empty. Python uses root `config.py`; choose other languages' root settings file from stack evidence, or record `Not established` when the language is unknown.

Existing layout isn't an exception. Retain only narrow, proven framework or external-binding exceptions; repair internal imports rather than citing them as a reason not to move. `docs/` remains the canonical home for specifications and plans. Agent runtime settings, custom-agent JSON, and global/personal agent configuration stay read-only; application configuration migration is in scope.

## Source Of Truth

Choose authority by claim type. **Required behavior** follows approved specs and decisions. **Observed code** establishes what exists now. **Verified behavior** requires a recorded check result. Keep those three distinct. Preserve historical decisions and mark supersession explicitly. An absent business requirement is an implementation gap, never a stale document to rewrite. Repair mandatory layout/configuration drift within the authorized refresh; hand unrelated business defects to separate corrective work.

An authoritative document a named consumer binds in place, such as a published package readme or a contract read by a test, stays authoritative there under the contract's retained-source rules, listed in **Authoritative Sources** and linked by section. Never duplicate mutable requirements or claim retained paths were relocated. This protects document authority, not arbitrary application-code locations: repair internal code imports and test paths affected by migration.

## What This Pass Owes The Documentation

Maintenance owns the records in `docs/README.md`. Re-read every source the **Authoritative Sources** table names, at its current path, and correct the document carrying its coverage when the source moved on. Keep **Unresolved** honest: close what was resolved, add what this pass found, and leave a real conflict open with both sources and the decision needed. A clean checker run over documentation nobody re-read is not an audit, and re-running the scaffold creates nothing and proves nothing.

Never invent repository facts. Mark an unverified fact `Unknown`, `Not established`, or `Needs verification`.

A `docs/_meta/coverage-ledger.json` from an earlier version is prior audit work, not clutter. Read it, carry useful findings into `docs/README.md`, and leave it in place unless the user explicitly approves removal with a preserved copy.

## Agent Coverage

Default to Codex, Claude Code, Kiro, and OpenCode even when invoked from one of them, unless the user narrows the targets. Read [the agent surface checks](references/maintenance-checklist.md#agent-surface-checks) when maintaining entry points. Keep shared rules in the root router, preserve the established Claude bridge branch and local rules, and maintain the Kiro steering route and configured OpenCode sources in their existing scope. Do not assume any of the four is installed; unavailable runtime checks stay `Needs verification`.

## Workflow

1. Run `standard/tools/jinx_context_check.py --root <repo>` first. `BLOCKED context-present` means hand off to `jinx-bootstrap`. Otherwise its output is the static structural baseline, never a coverage result. Record worktree state.
2. Establish authority by claim type. Preserve each agent's scope, imports, overrides, and conditional loading; do not assume one universal precedence rule.
3. Inventory layout, configuration/defaults/environment reads, consumers, live agent context, and `docs/`. Compare required and actual homes using [structure rule maintenance](references/maintenance-checklist.md#structure-rule-maintenance). Missing guidance or mandatory layout drift in an established project belongs here, not a new bootstrap.
4. Classify every finding `VALID`, `STALE`, `MISSING`, `DUPLICATED`, `CONFLICTING`, or `OBSOLETE`, each with evidence. A finding may carry one primary and one evidenced secondary class.
5. Read `references/maintenance-checklist.md` when a classification is unclear, changes span several context files, lessons need lifecycle decisions, or nested scope needs review.
6. Apply the smallest complete migration that restores mandatory structure, configuration ownership, and context accuracy. Create missing basic directories; move/split code by responsibility and repair imports, consumers, build/package/deploy paths and ignore rules as needed. Preserve functionality, business contracts, dirty work, originals, records, valid wording, and unmet requirements. An audit-only pass makes no edits. Complete semantic adoption before updating the manifest as [the contract requires](standard/contract.md#version-upgrade); a version-only edit isn't adoption.
7. Keep plan state coherent: exactly one canonical authority per plan, active and completed sets disjoint, superseded plans labelled with what replaced them, and the plan index matching the files.
8. Review lessons. Keep durable, actionable ones; remove disproven or redundant ones; promote recurring cross-cutting ones to the narrowest shared context; replace outdated guidance instead of stacking another exception.
9. Review the root router, nested guides, Claude imports and rules, and Kiro steering for scope, contradictions, and duplication. Update every affected reference to a changed canonical fact; never copy a whole document into each tool. Read `surface-size` as guidance: trim by moving explanation into `docs/`, never by dropping a rule.
10. Perform the real re-read of step [What This Pass Owes The Documentation](#what-this-pass-owes-the-documentation), using [the second-pass steps](references/maintenance-checklist.md#a-second-pass-is-a-real-re-read). Record the requirement-to-source-to-document mapping with implementation and verification as independent states.
11. Run the static checker and affected migration tests/build gates. Prove real root-config propagation to consumers, invalid-value rejection, and supported package/runtime launch without brittle cwd or `sys.path` tricks. For PLAN_ONLY, check created structure and known config/modules without implementing business behavior. Report blocked checks by cause. Compare final changes and data preservation with step 1; unchanged compliant inputs produce no substantive edit, duplicate bridge, or timestamp churn.

## Completion

Include actual migrations, unchanged valid roles, narrow binding exceptions, unknown facts, and unresolved gaps in the existing report. Don't classify supported versions or synchronized distribution copies as unmanaged history by name, delete historical copies without authorization, or invent an exception. Structure adoption, semantic context coverage, agent loading, and feature verification are separate outcomes.

Root application configuration owns editable non-secret values/defaults, central environment/secret loading and validation. Lower modules use supported imports or injection, with no hidden defaults or environment reads; algorithmic constants remain local. Adoption requires those consumer paths and launch behavior to be checked, not merely a settings file and updated map.

Complete only when examined items have evidence-based classifications, updates are minimal, requirements and decisions remain intact, instructions retain their scope, `docs/README.md` reflects a fresh re-read of the live sources and the currently open items, and the checker passes or names blocked items. Report the checker's static result separately from your own coverage judgement. Report unchanged `VALID` material, modified files, implementation gaps, retained sources with their exception, and unresolved items separately. For each target agent report entry points, changed/preserved/native-covered/blocked status, static checks, and runtime evidence or `Needs verification`. File creation is not proof that an agent loaded it, an implemented feature is not a verified one, and a structural pass is not a completed audit.

## Safety And Boundaries

- Don't bootstrap a context standard from scratch; hand that to `jinx-bootstrap` and don't report maintenance as done.
- Don't replace feature, fix, refactor, or release verification. Use `jinx-verify-change`.
- Don't implement unrelated business features, redesign business contracts, repair unrelated defects, or upgrade dependencies. Necessary structural code/config migration is in scope.
- Don't edit agent runtime/global configuration, personal or managed instructions, model/permission settings, or custom-agent JSON; report blocked loading instead.
- Don't delete or rewrite a user's persisted records, including an older coverage ledger, without explicit approval and a preserved copy.
- Don't generate project-specific skills, additional skills, or automation. Don't create deploy, debug, database, frontend, backend, code-review, test, release, or similar skills.
- Don't create background or self-improvement loops, Git hooks, commits, pushes, pull requests or CI automation. Existing CI permits only migration-required path/command-reference repairs under the contract, not changes to triggers, permissions, secrets, deployment policy or unrelated gates; inspect before moving targets and block a move whose consumer cannot be safely repaired.
- Don't install package scripts, hooks, CI, or runtime dependencies into the target. The checker runs from the installed skill; application files and configuration required by migration aren't installed skill tooling.
- Don't state a repository fact without evidence from its current authoritative surface.

## Handoffs

Hand a repository with no context standard to `jinx-bootstrap`. Hand feature-correctness evidence to `jinx-verify-change`, separately from migration checks. Hand unrelated business defects to the responsible implementation workflow with evidence and affected context claims.
