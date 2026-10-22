# Repository Development Skills

Current standard: **1.4.1**. This patch strengthens Kiro IDE/CLI instruction compliance; it does not change the mandatory layout or checker schema. Post-hardening tests and native-agent trials are deferred at the user's request, so runtime improvement is not yet verified.

Three skills that establish, maintain, and verify a mandatory project layout and root central configuration, with shared instructions for Codex, Claude Code, Kiro, and OpenCode. Each ships a safe create-only scaffold and deterministic read-only context checker. The agent performs semantic refactoring and runtime verification; tooling alone does not certify adoption. The default target set is all four agents unless narrowed. Model choice does not determine which instruction files an agent application loads.

| Skill | Use it for |
| --- | --- |
| `jinx-bootstrap` | Establish the standard from an empty project, plans, or existing code; migrate code, settings and agent docs into it. |
| `jinx-context-maintenance` | Repair drift and upgrade an established standard, including structure/configuration; full audit by default, scoped on request. |
| `jinx-verify-change` | Verify an implementation, fix, or refactor across structure, spec-to-code consistency, and real behavior. |

## Choosing A Skill

Choose by the requested work, not the age of the repository:

- Plans or code exist, but no trusted structure: bootstrap. The checker reports `BLOCKED context-present`, which is the handoff signal.
- The structure exists, but a new feature, stale document, scattered agent doc, or missing bridge needs attention: maintenance.
- A specific implementation needs evidence that it meets its requirements: verify-change. It may fix failures caused by that change when authorized; read-only verification makes no edits.

Bootstrap classifies context presence separately from implementation maturity. Empty and plan-only projects get the mandatory base directories and instructions, plus evidence-backed planned module directories; no invented feature implementation or commands. An unknown language defers the root settings format, not the structure or rules. Documentation checks never certify an unimplemented feature. Structure adoption and feature verification are separate outcomes.

## The Context Standard

All three skills share [`standard/contract.md`](standard/contract.md): mandatory role destinations, root configuration ownership, documentation paths and checker contracts. Feature names, language and business requirements come from target evidence; existing arbitrary placement is not an exception.

| Surface | Path | Rule |
| --- | --- | --- |
| Shared instructions | `AGENTS.md` | Lightweight task router, goal ~100 non-blank lines, reported as guidance. Trim by moving detail into `docs/`, never by dropping a safety rule. |
| Claude bridge | `CLAUDE.md` with `@AGENTS.md`, or an established `.claude/CLAUDE.md` with `@../AGENTS.md` | Exactly one effective bridge, on whichever branch already exists. |
| Kiro IDE / Kiro CLI steering | `.kiro/steering/project-context.md` | Mandatory, `inclusion: always`. Routes to shared/task docs and carries short implementation checkpoints; no whole-document embeds. Inspect IDE and CLI loading separately. |
| OpenCode | `AGENTS.md` plus already-configured instruction sources | `opencode.json`/`opencode.jsonc` stay read-only. |

```text
docs/README.md                  core: navigation, authoritative sources, unresolved items
docs/project.md                 core: purpose, scope, status, canonical commands
docs/architecture/overview.md   core: units, boundaries, flows
docs/plans/README.md            core: plan lifecycle and index
docs/specs/<feature>.md         requirement + acceptance criteria
docs/plans/active/<task>.md     in-flight plan
docs/plans/completed/           landed and superseded plans
docs/decisions/ docs/guides/ docs/verification/ docs/archive/
docs/_meta/manifest.json        tool-consumed manifest: the standard version and managed paths
```

`docs/` is the canonical home for agent-facing specifications and plans. There is no `.kiro/specs/` mirror and no claim about Kiro's native Specs UI. The four core docs are required. The other names are the recommended set: a directory outside them is reported, not failed, because a project may have a good reason for it and no static check can read that reason — explain it with a row in `docs/README.md`. A category with nothing to say holds no placeholder file.

### Authoritative Sources Outside `docs/`

Some authoritative material cannot move into `docs/` without breaking a consumer: a package `README.md` a distribution surface publishes, a `DESIGN.md` a test reads by path. Those stay where they are and stay authoritative. The document that defers to one links its exact sections, `docs/README.md` records it under **Authoritative Sources** with the consumer that binds it, and the retention is reported as an exception. Copying a retained source's mutable requirements into `docs/` is a duplicate-authority defect, and reporting the relocation as complete while such a source is retained is a false completion claim. A safe reference integration is not blocked; only a real conflict between two live authorities is.

That record is a table humans and agents read, not a schema a tool parses. What replaced the machine ledger is the pair of tables in `docs/README.md`: **Authoritative Sources** for where each claim's authority lives, and **Unresolved** for the gaps, conflicts, and unverified claims a pass leaves open. An omitted gap is the failure those tables exist to prevent.

### The Checker's Scope Is Static Structure

Every report says so in its own output. The checker establishes file presence, declared shapes, path safety, links, and anchors. It does not establish that a document is accurate, that its content covers a requirement, or that an agent loaded it at runtime — those are the agent's judgement, reported separately. A repeat maintenance pass re-reads the live sources; re-running the scaffold creates nothing and proves nothing.

Two things are deliberately reported rather than failed, because failing them pressured an agent into deleting a rule or renaming a directory to clear a gate: `surface-size`, which counts `AGENTS.md`, the bridge, and steering against a ~320-line goal and names what it excludes, and `docs-structure`, which names directories outside the recommended set.

Anchors resolve against a heading's generated slug, the `-1`/`-2` suffixes a repeated heading gets, and an anchor declared explicitly through an HTML `id`/`name` or a `{#custom}` suffix. Slugging is Unicode-aware, so `## 9. API 설계 (FastAPI)` resolves as `#9-api-설계-fastapi` in both its literal and percent-encoded forms.

Runtime settings, custom-agent JSON, and global or personal instruction files are inspected, never silently rewritten; blocked loading is reported with the exact missing connection. Archived agent docs use non-discovery filenames (`docs/archive/agents-root-superseded.md`) so nothing keeps auto-loading. Unmet requirements stay implementation gaps. Unchanged inputs produce no substantive diff. There is no background watcher or scheduled updater.

Setup and maintenance report coverage for all requested agents, including unavailable ones — none of the four is assumed installed. Static file checks, coverage judgement, actual runtime loading, and behavioral compliance are four separate results. Verify-change checks the affected context only; a leaf change does not require four agent sessions. See [agent setup](skills/jinx-bootstrap/references/agent-files.md), [migration](skills/jinx-bootstrap/references/migration.md), [the second pass](skills/jinx-context-maintenance/references/maintenance-checklist.md#a-second-pass-is-a-real-re-read), [maintenance checks](skills/jinx-context-maintenance/references/maintenance-checklist.md#agent-surface-checks), and [verification](skills/jinx-verify-change/references/verification-strategy.md#retained-source-verification).

For Kiro IDE and Kiro CLI, [execution checkpoints](standard/contract.md#kiro-execution-checkpoints) require concrete placement/settings decisions before editing and a diff-to-rules comparison before completion. Temporary demos follow the same central validation and supported import rules; passing self-authored tests cannot excuse a lower-level fallback or missing documentation update. These are instruction-level safeguards, not runtime enforcement. Existing projects need an explicit maintenance update because scaffolding never overwrites their steering file. If testing is deferred by the user, report the unverified behavior without running checks or launching validation sessions.

### Mandatory Structure And Central Settings (1.4.0)

The [mandatory layout](standard/contract.md#mandatory-project-layout) is an actual migration target:

```text
AGENTS.md
<language-native root configuration>
src/<package>/<feature>/
tests/<feature>/
experiments/<experiment>/
outputs/
docs/architecture/  docs/specs/  docs/plans/{active,completed}/
```

Create the base directories even when empty; derive package/feature names from evidence. Keep the
core docs and native bridges listed above. Bootstrap and maintenance move/restructure code and repair
imports, tests, commands and necessary build/package/deploy/ignore paths while preserving behavior.
Only evidenced framework or binding external contracts justify narrow location exceptions, not legacy
habits or internal import volume. Originals, unrelated dirty work, historical records and supported
compatibility versions remain protected. This repository's synchronized `skills/*/standard/` copies
are intentional distribution artifacts with root `standard/` as the editing authority.

[Central configuration](standard/contract.md#central-configuration) owns editable tunables/defaults at
the repository root in a language-native form. Lower features import or receive validated settings;
no hidden duplicate defaults, scattered environment reads or facade-only root file. Resolve secrets
centrally from external sources, never commit them. Verify a root value reaching a feature, invalid
input rejection and supported launch/packaging. Root `AGENTS.md` names the actual file, consumption
route, editing procedure and checks, alongside the short mandatory development rules.

The scaffold creates skeletons, not semantic migrations. [Upgrade explicitly](standard/contract.md#version-upgrade)
by performing the refactor, updating rules/routes, checking behavior and then setting `standardVersion`
to the current `1.4.1` standard. Audit/read-only requests make no edits. A version-only change or static PASS is not
adoption; incomplete moves and unavailable runtime evidence remain explicit. No new skill, watcher,
ledger, per-file registry, required per-task report, hooks or CI automation is introduced.

### Historical Version 1.2.0

`1.2.0` removed the mandatory coverage-ledger machinery `1.1.0` introduced: no ledger file, no per-row schema, no source digests, no review rows, no per-category manifest state. The manifest requires one field, `standardVersion`; established optional fields are validated when present, other keys are carried, and churn-prone keys are forbidden. The router and managed-surface caps became advisory reports.

A ledger a `1.1.0` project already persisted is **optional historical input**. `legacy-ledger` reports that it exists so an agent reads the prior findings; nothing validates it, nothing requires it, and no tool here writes, rewrites, or deletes it. Removing or migrating one needs the user's explicit approval and a preserved copy — deleting a user's audit record unprompted destroys evidence.

When upgrading from `1.1.0`, also carry useful ledger findings into `docs/README.md` and leave the ledger in place. Follow the current integration sequence above before updating the version. An otherwise structurally compliant project with an old manifest fails `manifest-version`, which names both versions; passing it is not a semantic adoption audit.

## Tooling

Two standard-library Python tools ship inside every package under `standard/tools/`, so an installed skill needs no repository clone, sibling package, or dependency install.

| Tool | Purpose |
| --- | --- |
| `jinx_context_check.py` | Read-only deterministic checker. `PASS`/`FAIL`/`BLOCKED`/`NOT_APPLICABLE` per check, plus a scope line on every report; exit `0`/`1`/`2`, `64` on usage error. |
| `jinx_context_scaffold.py` | Creates required base directories and missing context templates. Never moves or overwrites existing files, including the manifest. Repetition produces no diff; directory/file collisions block all writes; post-preflight failures report partial work with exit `2`. |

```sh
# structural audit of a target repository
python3 skills/jinx-bootstrap/standard/tools/jinx_context_check.py --root /path/to/project

# create only the missing standard files, then fill the placeholders from evidence
python3 skills/jinx-bootstrap/standard/tools/jinx_context_scaffold.py --root /path/to/project --dry-run
```

Neither tool infers semantic architecture, requirements, commands, ownership, or coverage. The scaffold writes placeholders; a file with placeholders left in it is not a deliverable. Nothing is installed into the target project: no scripts, hooks, CI, or runtime dependencies.

## Layout

```text
standard/                        maintained source of the shared contract
  contract.md  VERSION
  templates/*.template.md|json
  tools/jinx_context_check.py  tools/jinx_context_scaffold.py  tools/jinxcontext/
tools/sync_standard.py           copies standard/ into each package
tests/                           fixtures + unittest suite for the tooling
commands/                        OpenCode slash-command wrappers
  jinx-bootstrap.md  jinx-context-maintenance.md  jinx-verify-change.md
skills/
  jinx-bootstrap/
    SKILL.md
    references/context-standard.md
    references/architecture-discovery.md
    references/documentation-taxonomy.md
    references/agent-files.md
    references/migration.md
    standard/                    synchronized complete copy
  jinx-context-maintenance/
    SKILL.md
    references/maintenance-checklist.md
    standard/
  jinx-verify-change/
    SKILL.md
    references/verification-strategy.md
    standard/
```

`standard/` at the root is the only authored copy. Each package carries a complete synchronized copy so it works standalone. Keep each skill directory intact, including its `standard/`. `SKILL.md` is the entry point; `references/` supplies focused guidance loaded when needed. Files under `commands/` are OpenCode-specific wrappers; do not copy them into other tools' command directories.

Bootstrap separates observed implementation from intent and refactors code/configuration into the standard while migrating agent-facing docs, carrying unique rules, decisions and unmet requirements, repairing references and archiving superseded instructions under non-discovery names. Public/generated documentation and consumer-bound document authorities remain protected. Maintenance owns structural drift and the second re-read; verify-change owns change-scoped evidence.

## Development

Contributors to this repository use its own tooling and tests. These are package assets; they are never installed into a target project.

```sh
python3 -m unittest discover -s tests -t tests     # fixture-driven suite
python3 tools/sync_standard.py --check             # packages match standard/, exit 1 on drift
python3 tools/sync_standard.py                     # re-synchronize after editing standard/
python3 standard/tools/jinx_context_check.py --mode package --root . \
  --package skills/jinx-bootstrap \
  --package skills/jinx-context-maintenance \
  --package skills/jinx-verify-change
```

Edit `standard/` only, then run `sync_standard.py`. The fixtures are a compliant repository that retains a test-bound `DESIGN.md` and a published `README.md` as recorded exceptions and documents itself partly in Korean, a repository with broken paths, links, anchors, manifest, and archived-filename violations, a `legacy-ledger-project` carrying the persisted `1.1.0` manifest shape and coverage ledger, a plan-only repository with no context, and a legacy repository whose unique rules and established nested bridge must survive scaffolding.

The compliant and legacy-ledger fixtures declare the current version to isolate static checks; they
are not examples of completed semantic adoption. The legacy ledger itself retains its historical
version and contents. The 1.2 upgrade cases in `test_structure_rules.py` exercise explicit version
mismatch and preservation, not automatic migration.

| Test file | Pins |
| --- | --- |
| `test_checker.py` | Per-fixture results, determinism across repeats, the scope line, JSON shape, target narrowing, CLI contract |
| `test_simplification.py` | What `1.2.0` stopped requiring: the ledger as optional history no tool touches, the one-field manifest, a stale category state that contradicts nothing, and size and structure reported rather than failed. Each case names the removed assertion it replaces. |
| `test_anchors.py` | Korean heading slugs, repeated-heading suffixes, explicit HTML and `{#id}` anchors, and a missing fragment still failing |
| `test_scaffold.py` | Create-only behavior, idempotence, blocking, and that no placeholder document appears beyond the core docs |
| `test_scaffold_regressions.py` | Write-path collisions leaving zero writes: escaping symlinks, a directory where a file must go, a damaged template, and an honest partial-failure report |
| `test_checker_regressions.py` | Read-path defects: a non-object manifest, reference-style links, inline Kiro embeds, managed-path semantics |
| `test_packages.py` | Package-mode checks, synchronization and drift, and each package running standalone from an isolated install |
| `test_structure_rules.py` | Current version, unchanged older manifests, and standalone scaffolds preserving code/data while creating required role directories; semantic migration remains agent work |
| `test_scaffold_directories.py` | Empty/plan-only skeletons, dry-run and repeat safety, directory collisions before any write, native bridge and input preservation |

Rule comprehension needs scenario review, not tests pinning prompt sentences. Exercise a flat script,
external/protected inputs, intentional compatibility versions and distribution copies, stale maps,
and a change that overwrites an input or introduces an unmanaged history copy. Report the reader's
actual decisions and any unauthorized action separately from CLI results. Native agent loading also
needs its own fresh-session evidence; package tests certify none of the four agent runtimes.

## Prerequisites

- `git`
- At least one supported agent application
- GitHub CLI (`gh`) only when cloning this private GitHub repository with the example below

Clone the repository after authenticating `gh` through its normal flow. Do not put credentials in commands, URLs, or configuration.

```sh
REPO_DIR="$HOME/src/opencode-repository-development-skills"
gh repo clone JinxJEONG/opencode-repository-development-skills-public "$REPO_DIR"
```

If you obtained the repository another way, set `REPO_DIR` to its absolute path.

## Install For Codex, Claude Code, Or Kiro

**Install into your user directory.** These skills are development tooling you carry between repositories, not a dependency of any one project. A user installation keeps them available everywhere and leaves every target repository untouched.

| Agent | User skill directory (default) | Project skill directory (opt-in) | Official discovery reference |
| --- | --- | --- | --- |
| Codex | `~/.agents/skills/` | `.agents/skills/` | [Build skills](https://learn.chatgpt.com/docs/build-skills) |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` | [Skills](https://code.claude.com/docs/en/skills) |
| Kiro | `~/.kiro/skills/` | `.kiro/skills/` | [Agent skills](https://kiro.dev/docs/skills/) |
| OpenCode | `~/.config/opencode/skills/` | `.opencode/skills/` | [Agent skills](https://opencode.ai/docs/skills/) |

A project installation commits three skill packages into the repository you are working on, so every contributor gets them whether they want them or not, and the repository carries tooling that has nothing to do with its own product. Choose it only when you deliberately want the whole team on a pinned copy. These skills never add themselves to a project: they edit no `opencode.json`, no `.gitignore`, no linter or formatter configuration, and they install no dependency — the checker is standard-library Python that runs from wherever the skill lives.

Installing a skill and generating a target project's instructions are separate operations. Do not install duplicate copies into every compatible discovery location of the same agent.

Paths were checked against official documentation on 2026-09-25. For cloud sessions, use the documented project/package distribution route; a local user directory is not automatically available remotely. Kiro custom agents may require explicit skill resources.

Set `JINX_SKILLS_DIR` to the chosen absolute directory, for example `JINX_SKILLS_DIR="$HOME/.agents/skills"` for local Codex, then run:

```sh
set -eu
REPO_DIR=${REPO_DIR:?Set REPO_DIR to this repository}
JINX_SKILLS_DIR=${JINX_SKILLS_DIR:?Choose the destination from the table}
SKILLS='jinx-bootstrap jinx-context-maintenance jinx-verify-change'

for skill in $SKILLS; do
  test -f "$REPO_DIR/skills/$skill/SKILL.md"
  if [ -e "$JINX_SKILLS_DIR/$skill" ] || [ -L "$JINX_SKILLS_DIR/$skill" ]; then
    printf 'Refusing to overwrite existing target: %s\n' "$JINX_SKILLS_DIR/$skill" >&2
    exit 1
  fi
done
mkdir -p "$JINX_SKILLS_DIR"
for skill in $SKILLS; do
  cp -R "$REPO_DIR/skills/$skill" "$JINX_SKILLS_DIR/$skill"
done
```

Use a fresh session to confirm discovery, then request a skill by name. Codex supports `$jinx-bootstrap`; Claude Code supports `/jinx-bootstrap`. In Kiro, ask it to use `jinx-bootstrap` and confirm the skill is available. The same naming pattern applies to maintenance and verification. No OpenCode command wrapper is needed for these agents.

To refresh copied packages, keep `JINX_SKILLS_DIR` set and use [Update A Copy Installation](#update-a-copy-installation). Repeat for each installation you maintain. Updating this clone alone does not update installed copies.

## OpenCode Install By Copy

Copying into the user directory is the default. It makes the installed skills independent of the clone after installation, and keeps them out of every project repository.

This preflight refuses every existing target before copying anything. It never overwrites a skill silently.

```sh
set -eu

REPO_DIR=${REPO_DIR:?Set REPO_DIR to the cloned repository}
SKILLS_DIR="$HOME/.config/opencode/skills"
COMMANDS_DIR="$HOME/.config/opencode/commands"
SKILLS='jinx-bootstrap jinx-context-maintenance jinx-verify-change'
COMMANDS='jinx-bootstrap jinx-context-maintenance jinx-verify-change'

for skill in $SKILLS; do
  if [ -e "$SKILLS_DIR/$skill" ] || [ -L "$SKILLS_DIR/$skill" ]; then
    printf 'Refusing to overwrite existing target: %s\n' "$SKILLS_DIR/$skill" >&2
    exit 1
  fi
done

for command in $COMMANDS; do
  if [ -e "$COMMANDS_DIR/$command.md" ] || [ -L "$COMMANDS_DIR/$command.md" ]; then
    printf 'Refusing to overwrite existing command: %s\n' "$COMMANDS_DIR/$command.md" >&2
    exit 1
  fi
done

mkdir -p "$SKILLS_DIR" "$COMMANDS_DIR"
for skill in $SKILLS; do
  cp -R "$REPO_DIR/skills/$skill" "$SKILLS_DIR/$skill"
done
for command in $COMMANDS; do
  cp "$REPO_DIR/commands/$command.md" "$COMMANDS_DIR/$command.md"
done
```

Quit and restart OpenCode after installation. It discovers skills from the global directory; skill content is loaded when invoked.

## Migrate An OpenCode Installation From The Previous Names

Use this once if the installed skills are still named `repo-bootstrap`, `repo-context-maintenance`, and `verify-change`. Update the clone first, then run the migration. It supports both copied skill directories and symlinked skills, installs the new command wrappers, removes the old skill entry points only after every replacement is ready, and restores the previous installation if a swap fails. Unrelated skills and commands aren't touched.

```sh
git -C "$REPO_DIR" pull --ff-only
```

```sh
set -eu

REPO_DIR=${REPO_DIR:?Set REPO_DIR to the cloned repository}
REPO_DIR=$(CDPATH= cd "$REPO_DIR" && pwd -P)
SKILLS_DIR="$HOME/.config/opencode/skills"
COMMANDS_DIR="$HOME/.config/opencode/commands"
PAIRS='repo-bootstrap:jinx-bootstrap repo-context-maintenance:jinx-context-maintenance verify-change:jinx-verify-change'
COMMANDS='jinx-bootstrap jinx-context-maintenance jinx-verify-change'
migrated=''
installed_commands=''

for pair in $PAIRS; do
  old=${pair%%:*}
  new=${pair#*:}
  if { [ ! -d "$SKILLS_DIR/$old" ] && [ ! -L "$SKILLS_DIR/$old" ]; } || \
     [ -e "$SKILLS_DIR/$new" ] || [ -L "$SKILLS_DIR/$new" ]; then
    printf 'Expected only the previous skill target: %s -> %s\n' \
      "$SKILLS_DIR/$old" "$SKILLS_DIR/$new" >&2
    exit 1
  fi
  if [ -e "$SKILLS_DIR/$new.new" ] || [ -L "$SKILLS_DIR/$new.new" ] || \
     [ -e "$SKILLS_DIR/$old.previous" ] || [ -L "$SKILLS_DIR/$old.previous" ]; then
    printf 'Refusing to reuse migration workspace for %s\n' "$old" >&2
    exit 1
  fi
  test -d "$REPO_DIR/skills/$new"
done

for command in $COMMANDS; do
  target="$COMMANDS_DIR/$command.md"
  if [ -e "$target" ] || [ -L "$target" ] || \
     [ -e "$target.new" ] || [ -L "$target.new" ]; then
    printf 'Refusing to overwrite command migration target: %s\n' "$target" >&2
    exit 1
  fi
  test -f "$REPO_DIR/commands/$command.md"
done

mkdir -p "$SKILLS_DIR" "$COMMANDS_DIR"

rollback_migration() {
  status=$?
  trap - HUP INT TERM EXIT
  for pair in $migrated; do
    old=${pair%%:*}
    new=${pair#*:}
    if [ -e "$SKILLS_DIR/$old.previous" ] || [ -L "$SKILLS_DIR/$old.previous" ]; then
      if [ -e "$SKILLS_DIR/$new" ] || [ -L "$SKILLS_DIR/$new" ]; then
        mv "$SKILLS_DIR/$new" "$SKILLS_DIR/$new.new" || :
      fi
      mv "$SKILLS_DIR/$old.previous" "$SKILLS_DIR/$old" || :
    fi
  done
  for pair in $PAIRS; do
    new=${pair#*:}
    if [ -L "$SKILLS_DIR/$new.new" ]; then
      rm -f "$SKILLS_DIR/$new.new"
    elif [ -d "$SKILLS_DIR/$new.new" ]; then
      rm -rf "$SKILLS_DIR/$new.new"
    fi
  done
  for command in $installed_commands; do
    rm -f "$COMMANDS_DIR/$command.md"
  done
  for command in $COMMANDS; do
    rm -f "$COMMANDS_DIR/$command.md.new"
  done
  exit "$status"
}

trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
trap 'rollback_migration' EXIT
for pair in $PAIRS; do
  old=${pair%%:*}
  new=${pair#*:}
  if [ -L "$SKILLS_DIR/$old" ]; then
    ln -s "$REPO_DIR/skills/$new" "$SKILLS_DIR/$new.new"
  else
    cp -R "$REPO_DIR/skills/$new" "$SKILLS_DIR/$new.new"
  fi
done
for command in $COMMANDS; do
  cp "$REPO_DIR/commands/$command.md" "$COMMANDS_DIR/$command.md.new"
done

for pair in $PAIRS; do
  old=${pair%%:*}
  new=${pair#*:}
  migrated="$migrated $pair"
  mv "$SKILLS_DIR/$old" "$SKILLS_DIR/$old.previous"
  mv "$SKILLS_DIR/$new.new" "$SKILLS_DIR/$new"
done
for command in $COMMANDS; do
  installed_commands="$installed_commands $command"
  mv "$COMMANDS_DIR/$command.md.new" "$COMMANDS_DIR/$command.md"
done
trap - HUP INT TERM EXIT

for pair in $PAIRS; do
  old=${pair%%:*}
  if [ -L "$SKILLS_DIR/$old.previous" ]; then
    rm -f "$SKILLS_DIR/$old.previous"
  else
    rm -rf "$SKILLS_DIR/$old.previous"
  fi
done
```

Quit and restart OpenCode after migration. The old skill IDs are no longer installed; this procedure does not create compatibility aliases.

## Update A Copy Installation

Use this section after installing or migrating to the `jinx-*` names. First update the clone. The command only fast-forwards, so it won't create a merge commit.

```sh
git -C "$REPO_DIR" pull --ff-only
```

Then run the replacement below. For Codex, Claude Code, or Kiro, set `JINX_SKILLS_DIR` to that installation's directory; otherwise it defaults to OpenCode. It stages each new package as `<skill>.new`, replaces only the three named skill directories, and keeps the previous package as `<skill>.previous` until every replacement succeeds. The rollback trap restores any already-replaced target if a replacement fails. Since a complete package directory is swapped in, files removed upstream don't remain as stale installed files. Other skills in the destination aren't touched.

```sh
set -eu

REPO_DIR=${REPO_DIR:?Set REPO_DIR to the cloned repository}
SKILLS_DIR=${JINX_SKILLS_DIR:-"$HOME/.config/opencode/skills"}
SKILLS='jinx-bootstrap jinx-context-maintenance jinx-verify-change'
swapped=''

for skill in $SKILLS; do
  if [ ! -d "$SKILLS_DIR/$skill" ] || [ -L "$SKILLS_DIR/$skill" ]; then
    printf 'Expected a copied skill directory: %s\n' "$SKILLS_DIR/$skill" >&2
    exit 1
  fi
  if [ -e "$SKILLS_DIR/$skill.new" ] || [ -L "$SKILLS_DIR/$skill.new" ] || \
     [ -e "$SKILLS_DIR/$skill.previous" ] || [ -L "$SKILLS_DIR/$skill.previous" ]; then
    printf 'Refusing to reuse update workspace for %s\n' "$skill" >&2
    exit 1
  fi
  cp -R "$REPO_DIR/skills/$skill" "$SKILLS_DIR/$skill.new"
done

rollback() {
  status=$?
  trap - HUP INT TERM EXIT
  for skill in $swapped; do
    if [ -d "$SKILLS_DIR/$skill.previous" ]; then
      if [ -d "$SKILLS_DIR/$skill" ]; then
        mv "$SKILLS_DIR/$skill" "$SKILLS_DIR/$skill.new" || :
      fi
      mv "$SKILLS_DIR/$skill.previous" "$SKILLS_DIR/$skill" || :
    fi
  done
  exit "$status"
}

trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
trap 'rollback' EXIT
for skill in $SKILLS; do
  swapped="$swapped $skill"
  mv "$SKILLS_DIR/$skill" "$SKILLS_DIR/$skill.previous"
  mv "$SKILLS_DIR/$skill.new" "$SKILLS_DIR/$skill"
done
trap - HUP INT TERM EXIT

for skill in $SKILLS; do
  rm -rf "$SKILLS_DIR/$skill.previous"
done
```

The only deletion is each named temporary `.previous` directory after all three replacements succeed. If the update stops early, leave its `.new` and `.previous` directories in place, inspect them, then either complete the swap or restore the previous copy. Start a fresh session in the target agent after a successful update.

For OpenCode only, update the three copied slash-command wrappers separately. All targets are checked and staged before any replacement. Each previous file remains available until every replacement succeeds, and the rollback trap restores the complete prior command set after a failed swap. Unrelated commands are untouched.

```sh
set -eu

REPO_DIR=${REPO_DIR:?Set REPO_DIR to the cloned repository}
COMMANDS_DIR="$HOME/.config/opencode/commands"
COMMANDS='jinx-bootstrap jinx-context-maintenance jinx-verify-change'
swapped=''

for command in $COMMANDS; do
  target="$COMMANDS_DIR/$command.md"
  if [ ! -f "$target" ] || [ -L "$target" ]; then
    printf 'Expected a copied command file: %s\n' "$target" >&2
    exit 1
  fi
  if [ -e "$target.new" ] || [ -L "$target.new" ] || \
     [ -e "$target.previous" ] || [ -L "$target.previous" ]; then
    printf 'Refusing to reuse command update workspace: %s\n' "$target" >&2
    exit 1
  fi
  cp "$REPO_DIR/commands/$command.md" "$target.new"
done

rollback_commands() {
  status=$?
  trap - HUP INT TERM EXIT
  for command in $swapped; do
    target="$COMMANDS_DIR/$command.md"
    if [ -f "$target.previous" ]; then
      if [ -f "$target" ]; then
        mv "$target" "$target.new" || :
      fi
      mv "$target.previous" "$target" || :
    fi
  done
  for command in $COMMANDS; do
    rm -f "$COMMANDS_DIR/$command.md.new"
  done
  exit "$status"
}

trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
trap 'rollback_commands' EXIT
for command in $COMMANDS; do
  target="$COMMANDS_DIR/$command.md"
  swapped="$swapped $command"
  mv "$target" "$target.previous"
  mv "$target.new" "$target"
done
trap - HUP INT TERM EXIT

for command in $COMMANDS; do
  rm "$COMMANDS_DIR/$command.md.previous"
done
```

## Optional OpenCode Symlink Installation

Symlinks let the native skill directory point at the clone. This is optional, and the links are absolute. Moving or deleting the clone breaks them.

```sh
set -eu

REPO_DIR=${REPO_DIR:?Set REPO_DIR to the cloned repository}
REPO_DIR=$(CDPATH= cd "$REPO_DIR" && pwd -P)
SKILLS_DIR="$HOME/.config/opencode/skills"
COMMANDS_DIR="$HOME/.config/opencode/commands"
SKILLS='jinx-bootstrap jinx-context-maintenance jinx-verify-change'
COMMANDS='jinx-bootstrap jinx-context-maintenance jinx-verify-change'

for skill in $SKILLS; do
  if [ -e "$SKILLS_DIR/$skill" ] || [ -L "$SKILLS_DIR/$skill" ]; then
    printf 'Refusing to overwrite existing target: %s\n' "$SKILLS_DIR/$skill" >&2
    exit 1
  fi
done

for command in $COMMANDS; do
  if [ -e "$COMMANDS_DIR/$command.md" ] || [ -L "$COMMANDS_DIR/$command.md" ]; then
    printf 'Refusing to overwrite existing command: %s\n' "$COMMANDS_DIR/$command.md" >&2
    exit 1
  fi
done

mkdir -p "$SKILLS_DIR" "$COMMANDS_DIR"
for skill in $SKILLS; do
  ln -s "$REPO_DIR/skills/$skill" "$SKILLS_DIR/$skill"
done
for command in $COMMANDS; do
  cp "$REPO_DIR/commands/$command.md" "$COMMANDS_DIR/$command.md"
done
```

After installing or migrating to the `jinx-*` names, update a symlink installation by updating the clone and restarting OpenCode. No current `jinx-*` skill link needs replacing.

```sh
git -C "$REPO_DIR" pull --ff-only
```

Slash commands remain ordinary copied files when skills use symlinks. Update them with the command update procedure above.

## Use

Ask your agent for the skill that matches the work:

- Initial repository mapping or first context setup: `jinx-bootstrap`
- Existing instructions or documentation that may have drifted: `jinx-context-maintenance`
- Verification of the change currently being made: `jinx-verify-change`

After installing OpenCode's wrappers, the same workflows are available as global slash commands:

```text
/jinx-bootstrap
/jinx-context-maintenance
/jinx-verify-change
```

The skills don't automatically generate project-specific skills. They also don't add deployment, debugging, database, frontend, backend, release, or other auxiliary skills.

## Validate

Check each installed package with its own checker, then confirm discovery in a fresh session. Skill discovery is separate from generated project-instruction loading; the skills report those independently. No four-agent runtime certification is implied by package validation.

```sh
SKILLS_DIR=${JINX_SKILLS_DIR:-"$HOME/.config/opencode/skills"}
for skill in jinx-bootstrap jinx-context-maintenance jinx-verify-change; do
  python3 "$SKILLS_DIR/$skill/standard/tools/jinx_context_check.py" \
    --mode package --root "$SKILLS_DIR" --package "$skill"
done
```

Every line should read `PASS`, confirming the entry point, its frontmatter, its references, and the complete embedded `standard/` copy. Package mode validates the package; it says nothing about any target project. For an OpenCode installation, also confirm the wrappers and discovery:

```sh
COMMANDS_DIR="$HOME/.config/opencode/commands"
for skill in jinx-bootstrap jinx-context-maintenance jinx-verify-change; do
  test -f "$COMMANDS_DIR/$skill.md"
done
opencode debug skill
```

`opencode debug skill` output should list each of the three skill names from the native global skill directory. If your OpenCode version doesn't provide that diagnostic, restart OpenCode and confirm the three skills appear in its available-skill list.

## Scope And Exclusions

The scope is three skills plus their standard/templates/tooling. Setup and maintenance include necessary application-code and project-configuration refactoring, not unrelated feature development or dependency upgrades. They also update instructions, native Markdown steering and docs. They do not generate project-specific skills, rewrite runtime/global agent settings, add background automation/hooks, or automate Git and CI. Destructive deletion and overwrite of unrelated work require explicit approval.

The package tooling and this repository's test assets are in scope: they are how the standard is checked and how the packages are developed. What stays out of scope is installing anything into a *target* project — no scripts, hooks, CI, runtime dependencies, or scheduled validation. The checker runs from the installed skill and writes nothing.

Verification may remediate failures caused by the current change when authorized; read-only verification does not edit files.

## Limitations

- The checker proves **static** integrity. It cannot prove that an agent application actually loaded a file at runtime. Runtime loading is reported separately, as observed evidence or `Needs verification`; an unavailable agent or unrunnable runtime check is reported `BLOCKED` / `Needs verification`, never as a pass.
- No check establishes that a document covers the source it claims to. That judgement is the agent's, recorded in `docs/README.md` and reported separately, and no tool sets it.
- `surface-size` and `docs-structure` report judgement calls rather than failing them. A repository can pass every check with an oversized router or an unexplained `docs/` directory; what the report gives you is the measurement and the names.
- No four-agent runtime certification is implied by package validation or by the test suite. Codex, Claude Code, Kiro, and OpenCode availability is never assumed, and the skills do not install or authenticate one to clear a check.
- The tools supply structure. They do not infer architecture, requirements, commands, or ownership; the agent must populate those from the target repository, or mark them `Unknown`, `Not established`, or `Needs verification`.
- The scaffold's preflight is a point-in-time check. It does not defend against a path being replaced between the check and the write; exclusive creation plus an honest `BLOCKED` report with the partial list is what covers that window.
- Agent behavioral compliance — whether a session follows the instructions it loaded — is outside what any static check can establish.
