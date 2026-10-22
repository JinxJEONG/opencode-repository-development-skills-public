# Architecture Overview

Separate required structure, actual migrated paths, and planned but unimplemented units. Mark an
untraced relationship `Needs verification`; do not invent project-specific features or commands.

## Structure Operating Rules

Use these rules with the [Structure Map](#structure-map) before choosing file locations or processing
data. This section is the project's working authority, not a link to a user's installed skill.
Where a source is bound in place by a consumer (such as a test or distribution process), replace its clause's restatement here with an exact
section link and record it in [Authoritative Sources](../README.md#authoritative-sources).
Do not silently override an approved project contract; record an unresolved conflict first.

1. Use `src/<package>/<feature>/` for maintained functionality, `tests/<feature>/` for tests,
   `experiments/<experiment>/` for experiments and `outputs/` for generated results. Create these base
   directories plus `docs/architecture/`, `docs/specs/` and `docs/plans/{active,completed}/` even when
   empty. Actual subdirectory names require evidence. Shared code needs real shared responsibility.
   Root configuration and required build/launch declarations stay at root; move functional code.
2. Never copy the whole project into `v1/`, `v2/`, or `final/` to manage development history.
   Use the established revision mechanism. If none is known, preserve the work and record the
   decision needed; do not create copy trees or initialize, commit, or tag a repository unasked.
3. Allow purposeful compatibility versions, comparison implementations, and managed workspaces.
   Identify their selection/connection point and editing home. Distribution copies need an authored
   source, consumer, and synchronization method; release outputs are not development homes.
4. Keep supplied/collected development inputs in `data/raw/`, `tests/fixtures/` or external storage, separate
   from source, processed data, and output. Do not overwrite originals with transformations;
   revisions leave earlier inputs identifiable and recoverable. Shared inputs have one canonical
   location. Put transformations in `data/processed/`. Record external
   versions/identifiers without secrets, mandatory replicas, or forced large-file commits.
   This rule does not change normal production database updates.
5. When experiments exist, record their area, purpose, active/adopted/closed state, and adoption
   destination. Production execution and delivery must not depend on the experiment area.
6. Put project-controlled results/logs/caches in `outputs/`; record tool-mandated path exceptions. Never
   overwrite originals or human-maintained source. Normally keep reproducible output out of source
   history; record contract-required generated code, baselines, distribution, and release exceptions
   with their approved policy or binding tool/consumer contract. Recording a proposal is not approval.
7. Name files by role and established conventions, not `new`, `final`, `backup`, or `copy` variants
   that multiply editing homes. Compatibility, dataset, and experiment identifiers are legitimate;
   a filename alone proves no violation.
8. Migrate nonstandard paths and update imports, execution/data paths, tests, build/package/deploy
   references, documents and instructions together. Update this map when areas, paths, or policies
   change, not for every file addition. Preserve others' unfinished work, originals, and records.
   Check recoverability before an authorized deletion/replacement; it does not grant permission.

Bootstrap/maintenance includes necessary code restructuring, central settings integration and
related path/ignore repairs, not unrelated feature work. Move already-adopted experiment functionality
into maintained source without adopting unapproved experimental behavior. Preserve business contracts,
original bytes and other workers' edits. Ask before destructive deletion or conflicting overwrites.
Audit/read-only work never mutates. No history-tool setup or Git/CI automation. At completion, report
actual placement, config propagation, input preservation, reference repairs and normal behavior checks;
documentation or a filled map alone is not success. No new per-task report file is required.
Existing CI may receive only migration-required path/command-reference repairs. Preserve triggers,
permissions, secrets, deployment policy and unrelated gates; block connected moves before breaking
consumers when a safe repair needs broader authorization. Local checks do not certify hosted CI.
Static structure checks do not prove compliance. When an agent tool or instruction route changes,
use an available authorized fresh session to identify the rule section read and choose a location for
one representative file with its rationale, without creating it solely for the check. Record that
observation and its limits; unavailable runtime evidence is `Needs verification`, never a pass.

### Central Configuration

- Root editing surface: <exact language-native file, or `Not established` until language chosen>.
- Add/edit settings: <actual keys/groups and workflow>; keep tunable values and non-secret defaults
  here, not hidden in lower modules. Do not force `config.py` on non-Python projects.
- Consumption: <supported import/typed loader/injection route and consumer locations>.
- Overrides and validation: <precedence, environment/secret resolution and invalid-value behavior>.
- Packaging/launch: <how supported runtime and installed distribution receive the root settings>.
- Verification: <root value change -> observed feature result; invalid value -> observed rejection>.

No consumer-local fallback values, duplicate tunables, or independent environment reads. Keep genuine
algorithm constants and per-request arguments local. A source loader may be required by packaging,
but editable values remain at root. Avoid cwd assumptions and import-path hacks. Resolve secrets
centrally without committing values or exposing private settings to clients. Restore QA-only values.

### Structure Map

Fill from evidence; split rows by app/package when needed. Record standard destinations and actual
migration state, not arbitrary existing locations. Required base directories are always created;
use `Not applicable` only for optional roles, `Not established` for undecided language/names, and
`planned; unimplemented` for future behavior. Record exact constraint/consumer and evidence for a
narrow framework or external contract exception. Existing habits or internal imports are not exceptions.
Preserve consumer-bound authoritative documents by section link. Add no per-file registry.

If a missing or conflicting entry prevents a safe location or preservation decision, pause that
affected action and record the evidence and decision owner (or `Not established`) in
[Unresolved](../README.md#unresolved). Independent authorized work may continue.

| Role | Actual path or external identifier | Management rule, exception, and evidence |
| --- | --- | --- |
| Rules and entry points | <this section or retained authority; human index; effective agent routes> | <one authority; loading evidence or `Needs verification`> |
| Source and authored work | <src/package/feature and genuine shared areas> | <migration state and exceptions> |
| Central settings | <root settings file and lower consumption route> | <propagation, validation and launch evidence> |
| Tests | <tests/feature and tests/fixtures> | <behavioral coverage and exceptions> |
| Original inputs | <dedicated local/external location and version/identifier> | <preservation and revision policy> |
| Processed data and generated output | <data/processed when needed; outputs> | <regeneration, retention, tracking exceptions> |
| Experiments | <experiments base; named experiments when present> | <purpose, state, adoption destination or empty> |
| History and managed copies | <revision mechanism and copy locations> | <version identification, authored source, consumer, synchronization> |

## Units

| Unit | Responsibility | Entry point | Evidence |
| --- | --- | --- | --- |
| <unit> | <one line> | `<path>` | `<path or observed result>` |

## Dependencies And Contracts

| From | To | Contract | Evidence | Verification state |
| --- | --- | --- | --- | --- |
| <unit> | <unit> | <API, schema, event, file> | `<path>` | statically traced \| observed \| `Needs verification` |

## Representative Flows

1. <entry point> -> <step> -> <observable outcome> (evidence: `<path>`)

## Intended Versus Actual

| Relationship | Intended (spec/plan) | Actual (code) | Disposition |
| --- | --- | --- | --- |
| <relationship> | `docs/specs/<feature>.md` | `<path>` or absent | aligned \| planned-absent \| conflicting \| `Unknown` |

## Boundary Enforcement

| Boundary | Enforcement | State |
| --- | --- | --- |
| <boundary> | <test, lint rule, schema, or `None`> | declared \| observed passing \| unverified \| missing |
