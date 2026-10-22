# Agent File Setup

Use this for repository instruction generation. Targets are agent applications, not underlying model families. Defaults cover Codex, Claude Code, Kiro, and OpenCode. The rules below reflect official documentation checked on 2026-09-25; inspect installed versions and settings rather than assuming every environment behaves identically.

## Shared Context And Existing Material

Use exact filename casing: `AGENTS.md`, `CLAUDE.md`, and `AGENTS.override.md`. Discover differently cased existing names before creating files; preserve their unique content and repair references when a rename is warranted. Never silently overwrite a case variant, symlink target, dirty user edit, or an existing tool-specific rule.

The root `AGENTS.md` is a lightweight task router: status, what to read for which task, canonical commands with their declaring paths, boundaries, and the context update contract. Its size goal is ~100 non-blank lines, reported by `surface-size` as guidance rather than enforced ([`../standard/contract.md`](../standard/contract.md)). Trim by moving explanation into `docs/`, never by dropping a safety rule. Requirements, architecture, decisions, and task state live in their fixed `docs/` homes; content at a non-standard path is migrated with [the migration map](migration.md) rather than left in place. Classify conflicts by scope and intent; code proves current behavior, not permission to discard requirements or instructions.

Inspect repository and relevant ancestor instructions, import targets, `.claude/rules/`, `.kiro/steering/`, and instruction-related settings. Personal and managed files are read-only constraints, not generated project output. Do not traverse unrelated home-directory content. Preserve existing native rules and their inclusion conditions; do not consolidate them merely because a shared file is being introduced.

## Entry Points By Agent

| Agent | Setup action | Loading checks |
| --- | --- | --- |
| Codex | Create or maintain root `AGENTS.md`; use nested files only for material local rules. Preserve existing `AGENTS.override.md`. | At startup, discovery follows root to working directory and selects override before ordinary instructions at each level. Check fallback names and the configured size cap when available. An override can hide the ordinary file at that level. |
| Claude Code | Create a root `CLAUDE.md` containing an actual `@AGENTS.md` import when no effective bridge exists. If `.claude/CLAUDE.md` is the established entry point, add `@../AGENTS.md` there instead. Preserve Claude-only content and `.claude/rules/`. | Native AGENTS support starts at v2.1.277 but depends on settings and existing CLAUDE files. Imports support older or CLAUDE-first setups. Inspect nested CLAUDE files and rules; do not assume a root bridge imports nested AGENTS files. |
| Kiro IDE / Kiro CLI | Root `AGENTS.md` provides shared instructions. Create `.kiro/steering/project-context.md` with `inclusion: always`, task-relevant read routes and the [execution checkpoints](../standard/contract.md#kiro-execution-checkpoints). Maintain existing steering alongside it without embedding whole documents. | Inspect IDE and CLI separately, including application version and CLI engine/profile when known. Confirm effective AGENTS/steering resources and distinguish automatic inclusion from explicit reads. A loaded file is not evidence of behavioral compliance. |
| OpenCode | Root `AGENTS.md` provides shared instructions; preserve existing instruction sources configured in `opencode.json` or `opencode.jsonc`. | AGENTS takes precedence over the CLAUDE fallback. A Markdown link or `@path` text is not an automatic import. Inspect configured `instructions` and verify startup and nested behavior for the installed version. |

For every target, record `agent | entry points | local/conditional rules | changed/preserved/native-covered/blocked | static checks | runtime evidence`. Missing CLI access does not remove a target from the setup: generate its supported files and label runtime loading `Needs verification`. Do not assume any of Codex, Claude Code, Kiro, or OpenCode is installed or authenticated in the environment, and never install one to clear a check.

The default Claude bridge is an actual import, including when native AGENTS loading works on the current machine. Native loading alone is not an existing bridge: retain or create the import for other versions and CLAUDE-first sessions. Skip it only when the user chooses a native-only setup; report the required version/settings and their verification state.

When a repository-owned Codex override hides a shared guide, preserve its exceptions and add an explicit instruction to read the shared guide at its actual path before work, applying the override's scoped exceptions. Codex `@path` text is not an import mechanism. If the override is private, outside the editable scope, or conflicts cannot be resolved while preserving user work, leave it unchanged and report blocked coverage with the exact missing connection. A written read directive is statically connected, not proof that the shared guide was read at runtime.

### Scoped Rules And Imports

Put `Scope: <repository-relative subtree>` in each local guide. Root instructions should direct the agent to read applicable local guides before changing that subtree; do not claim identical automatic discovery across tools. Where Claude needs a nested bridge, import that directory's `AGENTS.md` from an appropriate scoped CLAUDE file and preserve local additions. Keep imports one-way: `CLAUDE.md` imports `AGENTS.md`, never the reverse.

For Kiro, preserve existing `inclusion: always`, `fileMatch`, `manual`, or other supported modes. When adding a file-specific rule, use a matching `fileMatchPattern` and the narrowest useful scope. Beyond the mandatory `project-context.md` route, add steering only for a real conditional-rule need; never copy AGENTS content into product/tech/structure files. `docs/` is the sole canonical home for specifications and plans: do not create `.kiro/specs/`, do not mirror docs into a second tree, and do not promise native Specs UI behavior. Migrate an existing `.kiro/specs/` entry into `docs/specs/` with [the migration map](migration.md), or report it blocked with its cause.

Kiro's steering and custom-agent documentation differ on default resource inheritance. Inspect the actual agent profile, settings, and loaded context. Report a missing resource or disabled inheritance with the exact required connection; do not silently rewrite agent JSON or claim coverage based only on file existence.

Kiro guidance rechecked on 2026-10-04: [steering](https://kiro.dev/docs/steering/) distinguishes full CLI V3 inclusion modes from partial V1/V2 support; `always` is the common route. Do not assume an installed CLI uses V3 or apply its resource-reference syntax to an older engine. The custom-agent route must include the applicable shared/steering resources in its effective context. Inspect the profile in its existing format; these skills do not create or rewrite agent profiles to force loading.

Populate the native steering checkpoints with project-local routes, not installed skill paths. Require concrete placement/configuration decisions before editing, preserved central validation errors, supported imports and affected documentation updates. A demo or temporary task is not an exception. On an established project, integrate these reminders deliberately: the create-only scaffold will keep an older steering file unchanged. Preserve native scoped rules and avoid a duplicate steering file.

### Context Update Contract

Add a concise repository-specific rule to the shared guide, following [the root template](../standard/templates/agents-root.template.md#context-updates): when a change affects a command, path, contract, or architecture, update the affected canonical document and agent-facing references in the same work. Route layout/configuration work to the project's architecture rules implementing [mandatory layout](../standard/contract.md#mandatory-project-layout), [central configuration](../standard/contract.md#central-configuration), and [structure refactoring](../standard/contract.md#structure-refactoring). Preserve unmet requirements, distinguish structure adoption from feature verification, and leave unrelated docs unchanged. Name actual project paths and when to read them, not a required full-repository read before every edit.

When the installed maintenance skill is available, route broader context drift to `jinx-context-maintenance`; otherwise describe the update procedure directly without requiring an unavailable skill. This is an execution instruction and a workflow invoked on demand, not a background watcher or a guarantee that every agent obeys it.

## Verification And Completion

- Run `../standard/tools/jinx_context_check.py --root <repo>` for the static surface checks: bridge presence and uniqueness, import cycles, the Kiro route, router routing and size, links, and anchors. It is read-only and deterministic; it proves static integrity only.
- Resolve imports from the containing file, ordinary Markdown links from their document, and tool-specific references using that tool's documented base. Check missing targets, cycles, casing, stale paths, and scope leakage.
- Review common rules and each native surface together. Preserve unique requirements and tool-only instructions. Generated bridges should reference the shared guide rather than copy its body.
- Check actual loaded context in a fresh session when available and authorized, including a representative nested scope. Do not install or authenticate another agent merely to test loading; report unavailable checks. A model restating a rule alone is weaker evidence than a loader diagnostic showing the file path.
- Re-running against unchanged inputs must preserve content and produce no substantive diff. Do not append another bridge, duplicate a rule, or rewrite timestamps on every run.
- Report static file integrity separately from observed runtime loading and behavioral compliance. Do not promise compatibility with every past or future version.

## Official Sources

- [Codex instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Claude Code instructions and imports](https://code.claude.com/docs/en/memory)
- [Kiro steering](https://kiro.dev/docs/steering/) and [custom-agent resources](https://kiro.dev/docs/custom-agents/configuration-reference/)
- [OpenCode rules and instruction sources](https://opencode.ai/docs/rules/)
