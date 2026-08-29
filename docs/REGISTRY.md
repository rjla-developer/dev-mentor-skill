# The registry

What it is, how the mentor reads it, and how it stays current.

## Contents

- [What it is](#what-it-is)
- [Files](#files)
- [Resolution order at run time](#resolution-order-at-run-time)
- [Field reference](#field-reference)
- [The honesty rule](#the-honesty-rule)
- [Keeping it fresh](#keeping-it-fresh)
- [Adding a stack](#adding-a-stack)

## What it is

A catalog of the official agent skills that exist for each stack, what each one covers,
and - the part nobody else writes down - **what they do not cover**.

It is not documentation. It contains no framework tutorials, no API descriptions, no code
samples. Framework teams found that skills which only restate documentation add nothing,
because models already find that information; they pivoted to task-oriented skills. This
project applies the same lesson: the registry stores routing and judgment, never content
that already exists elsewhere.

## Files

| File | Contents |
|---|---|
| `schema.json` | JSON Schema for a stack entry. CI validates against it. |
| `index.json` | Stack list, `synced_at`, `raw_base_url`, and cross-cutting skills that apply to several stacks. |
| `<stack>.json` | One per stack. The filename must equal the `stack` field. |

## Resolution order at run time

1. **Remote fetch** from `raw_base_url` - the current catalog. A merged pull request
   reaches every user with no reinstall.
2. **Bundled copy** shipped with the skill - used when the fetch fails, and always
   presented with its `synced_at` date: *"Using a catalog from 2026-08-27; it may be out
   of date."* Environments differ in whether they can reach the network at run time, so
   this path is normal, not exceptional.
3. **Live search** - for a stack the catalog does not cover. Findings are shown with their
   source URLs, and the user is offered an issue to add the stack.

A stale catalog served as current is worse than no catalog, which is why the date is
mandatory rather than polite.

## Field reference

| Field | Purpose |
|---|---|
| `stack` | Registry key. Must equal the filename. |
| `category` | frontend / backend / fullstack / mobile / infra |
| `detection.files` | Manifests that suggest this stack |
| `detection.markers` | Substrings that confirm it. Required when the manifest serves many stacks. |
| `last_verified` | The date a human last confirmed every id, command and URL here |
| `official_skills[].id` | `owner/repo`, or `owner/repo#skill` for one skill in a collection |
| `official_skills[].owner_kind` | `framework-team` / `vendor` / `community`. The mentor states this when recommending, because it changes how much to trust the skill. |
| `official_skills[].install` | Verbatim command, or `null` when unknown |
| `official_skills[].covers` | What the mentor must NOT reimplement |
| `official_skills[].does_not_cover` | What the mentor must handle itself |
| `gap_map` | The uncovered ground, why it matters, who fills it, and the fallback |
| `testing.commands` | Real commands. `full_suite` is required - the quality gate runs it. |
| `growth_thresholds` | Stack-specific overrides of the generic thresholds |
| `architecture` | Pattern, `folder_strategy`, the layers with what each must not hold, the `variants` a senior chooses between, and `rules` written verbatim into the project's `CLAUDE.md`. `recommended_by` separates framework-team doctrine from opinion. |
| `testing.layers[]` | What belongs in each layer, and `signal_you_picked_wrong` - the tell that an assertion sits at the wrong one. |
| `testing.rules` / `traps` / `what_not_to_test` | Stack-specific test judgment. `traps` records how a suite in this stack passes while the product is broken. |
| `key_decisions` | The choices this stack forces with no framework default, each with the cost of getting it wrong. |
| `operability` | What counts as a failure boundary here, where authorization lives, the observability idiom, and the commands that prove shippable. |
| `dead_code_risks` | Patterns that look unreferenced but are alive. Feeds `/mentor-clean`. |

## The honesty rule

**A field that cannot be verified against a primary source is marked, never invented.**

```jsonc
{
  "id": "someorg/skills",
  "install": null,
  "needs_verification": true,
  "notes": "Repository confirmed; install route not confirmed on <date>."
}
```

`scripts/validate_registry.py` fails the build when `install` is `null` without
`needs_verification: true`, so the honest path is also the only path that passes CI.

When the mentor reads an entry flagged this way, it repeats the caveat to the user rather
than hiding the entry. An honest gap is more useful than a plausible guess, because a
plausible guess is indistinguishable from a fact until it 404s.

Several entries in the first release carry this flag. That is the system working.

## Keeping it fresh

`.github/workflows/sync-registry.yml` runs weekly. It probes every `source_url`, writes
`docs/registry-sync-report.md`, bumps `synced_at` only when everything resolved, and opens
a pull request.

It **never merges**, and it never edits a stack entry. A 404 can mean a repository was
renamed, moved, or made private - three situations with three different correct responses,
none of which a cron job should pick.

## Adding a stack

See `CONTRIBUTING.md` for the full template, and `docs/ROADMAP.md` for the 22 stacks
already queued. Short version:

1. Copy the closest existing stack file.
2. Fill every field. Open every URL yourself.
3. Mark anything unconfirmed `needs_verification: true`.
4. Add the entry to `index.json`, including `has_framework_team_skill`.
5. Run `python3 scripts/validate_registry.py`.
6. Open the pull request. You do not need permission to propose one.
