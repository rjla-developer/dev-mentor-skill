# Contributing

You do not need permission to propose a change. Fork, edit, open the pull request.

## Contents

- [The one rule](#the-one-rule)
- [Adding a stack](#adding-a-stack)
- [Verifying that a skill exists](#verifying-that-a-skill-exists)
- [Fixing a stale entry](#fixing-a-stale-entry)
- [Changing a threshold](#changing-a-threshold)
- [Editing the skills themselves](#editing-the-skills-themselves)
- [Running the checks](#running-the-checks)
- [Pull request expectations](#pull-request-expectations)

## The one rule

**A field you cannot verify against a primary source is marked, never guessed.**

```jsonc
{
  "id": "someorg/skills",
  "install": null,
  "needs_verification": true,
  "notes": "Repository confirmed 2026-08-27; install route not confirmed."
}
```

CI fails when `install` is `null` without `needs_verification: true`, so the honest path is
also the only path that merges. A plausible-looking wrong command sends someone to a 404,
and after that nobody trusts the rest of the catalog either.

**Partial entries are welcome.** Three verified skills and four flagged fields is a real
contribution. The next person starts from research instead of from nothing.

## Adding a stack

1. Pick one from [docs/ROADMAP.md](docs/ROADMAP.md), or propose your own with
   [the new-stack template](.github/ISSUE_TEMPLATE/new-stack.yml).
2. Say in the issue that you are working on it.
3. Copy the closest existing `registry/<stack>.json` and fill every field below.
4. Add the stack to `registry/index.json`, including `has_framework_team_skill`.
5. Run the checks.
6. Open the pull request.

### Required fields

| Field | Requirement |
|---|---|
| `stack` | Lowercase, digits, hyphens. Must equal the filename. |
| `display_name` | What a human calls it. |
| `category` | `frontend` / `backend` / `fullstack` / `mobile` / `infra`. |
| `detection.files` | Manifests that suggest the stack. Forward slashes only. |
| `detection.markers` | Required whenever the manifest serves several stacks - `package.json` and `pyproject.toml` always need one. |
| `last_verified` | The date **you** did the research. Not a copy from another file. |
| `official_skills[]` | `id`, `owner`, `owner_kind`, `install`, `covers`, `does_not_cover`, `source_url`. |
| `gap_map[]` | At least one entry. `gap`, `why_it_matters`, `fallback` are required; `filled_by` may be `null`. |
| `testing.layers` | The layers that make sense for this stack. |
| `testing.commands.full_suite` | Required. The quality gate runs it before reporting any task complete. |
| `growth_thresholds` | Every value states the number **and** the unit. No bare numbers. |
| `dead_code_risks` | The convention-based and dynamic-access patterns of this stack. |

### `gap_map` is the most valuable field

Anyone can list what a skill covers - the README says so. The gap map says what it leaves
open, which is what the mentor then has to handle itself. An entry with an empty `gap_map`
is claiming a stack is fully covered; if you believe that, say why in `notes`.

## Verifying that a skill exists

Before writing an `official_skills` entry:

1. **Open the repository.** Not a blog post, not an aggregator, not a search summary - the
   repository or the framework's own documentation.
2. **Read the install command from the README** and copy it verbatim. Publishers use
   different tooling: some use `npx skills add`, some ship a plugin marketplace, some use a
   different CLI entirely. Never transfer a command from one publisher to another.
3. **Confirm the individual skill names** by listing the repository, not by inferring them
   from the project name.
4. **Set `owner_kind` honestly.** `framework-team` means the people who maintain the
   framework. A well-known consultancy is `community`. A platform vendor is `vendor`. The
   mentor tells users which one it is, so a wrong label misinforms them directly.
5. **Anything you could not do above** → `needs_verification: true` and a note saying what
   is unconfirmed.

## Fixing a stale entry

Use [the stale-skill template](.github/ISSUE_TEMPLATE/stale-skill.yml), or go straight to a
pull request. Include what you ran or opened and what happened - a URL and an error message
beat a description.

When a skill has been withdrawn, do not just delete the entry: move what it covered into
`gap_map`, so the mentor keeps covering that ground itself.

## Changing a threshold

Thresholds in `skills/dev-mentor/references/growth-signals.md` and in each stack's
`growth_thresholds` are calibration, not law. To change one, include:

- the current value and the proposed one,
- what goes wrong at the current value - noisy on real code, or silent on a real problem,
- an example from a real codebase.

A miscalibrated threshold makes the mentor noisy, and a noisy mentor gets muted. This is a
welcome kind of pull request.

## Editing the skills themselves

Rules that CI enforces:

- `SKILL.md` under 500 lines.
- Frontmatter `name`: lowercase, digits and hyphens, at most 64 characters, matching the
  directory, and containing neither reserved word.
- Frontmatter `description`: at most 1024 characters, third person, stating **what it does
  and when to use it**. Models under-trigger skills, so be deliberately insistent about the
  triggers.
- References are **one level deep** from `SKILL.md`. A reference file must not point at
  another reference file.
- Reference files over 100 lines carry a `## Contents` table of contents.
- Forward slashes in every path.
- No time-sensitive statements. Superseded material goes in a collapsed *Older patterns*
  section at the end of the file, never inline.

Adding content is not free: every line competes for the same context window. If you add a
paragraph, say in the pull request what it buys.

## Running the checks

```bash
pip install jsonschema
python3 scripts/validate_registry.py
python3 scripts/validate_skills.py
```

Both run in CI on every pull request, along with the hook test and an eval-scenario check.

## Pull request expectations

- Conventional commit messages: `feat(registry): add sveltekit`, `fix(hooks): ...`.
- One concern per pull request. A stack addition and a threshold change are two.
- Say what you verified and how. "Opened the repo, copied the install command from the
  README" is exactly the right level of detail.
- Say what you could not verify. That is not a weakness in the contribution; it is the
  contribution being trustworthy.
