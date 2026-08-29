# Orchestration

How to detect a stack, resolve the registry, and recommend skills without inventing
anything.

## Contents

- [Why the catalog lives outside the skill](#why-the-catalog-lives-outside-the-skill)
- [Stack detection](#stack-detection)
- [Registry resolution: three layers](#registry-resolution-three-layers)
- [Reading a stack entry](#reading-a-stack-entry)
- [Recommending and installing](#recommending-and-installing)
- [Stack not in the registry](#stack-not-in-the-registry)
- [Failure messages](#failure-messages)

## Why the catalog lives outside the skill

A skill is static markdown. It learns nothing after it ships. If a framework team
publishes two new skills tomorrow, a hardcoded list starts lying immediately and keeps
lying until someone edits it.

So the catalog lives in `registry/` in the repository and is fetched at run time. A merged
pull request reaches every user without anyone reinstalling anything.

## Stack detection

Read manifests, not file extensions. Extensions tell you a language; manifests tell you a
stack.

| Manifest | Suggests | Confirm with marker |
|---|---|---|
| `pubspec.yaml` | Flutter or Dart | `sdk: flutter` |
| `package.json` | many | `"next":`, `"@angular/core":`, `"expo":`, `"@nestjs/core":` |
| `pyproject.toml`, `requirements.txt` | Python | `fastapi`, `django`, `flask` |
| `pom.xml`, `build.gradle` | JVM | `spring-boot-starter` |
| `*.csproj`, `*.sln` | .NET | `Microsoft.NET.Sdk.Web` |
| `go.mod` | Go | `gin-gonic`, `labstack/echo` |
| `Cargo.toml` | Rust | `axum`, `actix-web` |

`package.json` and `pyproject.toml` each serve half a dozen stacks. **Always check the
marker.** Never conclude "Next.js" from the presence of `package.json` alone.

Multiple stacks in one repository is normal, not an error. A monorepo with an Expo app and
a NestJS API resolves to two entries; recommend for both and say which directory each
applies to.

Detection finding nothing is a legitimate result. Say so and go to the Step 1 choice flow;
do not guess from a filename.

## Registry resolution: three layers

### 1. Remote fetch (preferred)

```
https://raw.githubusercontent.com/rjla-developer/dev-mentor-skill/main/registry/index.json
https://raw.githubusercontent.com/rjla-developer/dev-mentor-skill/main/registry/<stack>.json
```

Read `index.json` first: it lists which stacks exist, their files, and `synced_at`.

### 2. Bundled copy (offline fallback)

The registry travels with the skill at `../../registry/` relative to `SKILL.md`. Use it
when the fetch fails, and **always state the date**:

> Using a bundled catalog from 2026-08-27. It may be out of date - I could not reach the
> remote registry.

This matters because environments differ: Claude Code and claude.ai can reach the network
at run time; the API cannot. An agent that silently serves a stale catalog as current is
doing something worse than being offline.

### 3. Live search (last resort)

Stack absent from the registry: search for it, show what you found with its source URL,
and offer to open an issue so the catalog covers it next time.

**Never state an install command you have not seen in a primary source.** Not from memory,
not by analogy with another stack's command. Different publishers use different CLIs -
some use `npx skills add`, some use a plugin marketplace, some use a different tool
entirely. A wrong install command sends the user to a 404 and costs you their trust.

## Reading a stack entry

| Field | How to use it |
|---|---|
| `official_skills[].owner_kind` | `framework-team` beats `vendor` beats `community`. Say which one you are recommending. |
| `official_skills[].install` | Verbatim. `null` means unknown; then `needs_verification` is true and you must say so. |
| `official_skills[].covers` | What you must NOT reimplement. |
| `official_skills[].does_not_cover` | What you must handle yourself. |
| `gap_map` | The part nobody else tells the user. Read it out loud at Step 3 and again at Step 6. |
| `testing.commands` | The real commands for the quality gate. Verify against the project's own scripts before running. |
| `testing.layers[]` | Which layer an assertion belongs in, plus `signal_you_picked_wrong` - the tell that it sits at the wrong one. |
| `testing.rules` / `traps` / `what_not_to_test` | Stack-specific test judgment. The traps are what a model is least likely to volunteer unprompted. |
| `key_decisions` | The choices this stack forces with no framework default. Surface them at Step 1; each carries the cost of getting it wrong, which is what justifies interrupting the user. |
| `architecture` | The structural doctrine: pattern, `folder_strategy`, the `variants` a senior chooses between, and `rules` - checkable invariants that go verbatim into the project's `CLAUDE.md`. Check `recommended_by`: `framework-team` is doctrine, anything else is an opinion and must be presented as one. A layer marked `optional` stays absent until an observed reason appears. |
| `growth_thresholds` | Overrides the generic thresholds in `growth-signals.md`. |
| `operability` | What a boundary, an authorization decision and a shippable build look like in this stack. Feeds `delivery-gates.md`. |
| `dead_code_risks` | Feeds `/mentor-clean`'s `requires_human_review` classification. |
| `last_verified` | If it is old, say so when the recommendation matters. |

`needs_verification: true` anywhere in an entry is not a reason to hide the entry. It is a
reason to present it with the caveat attached: "the registry lists this but the install
route was not confirmed - check it before running."

## Recommending and installing

Format, one line per skill:

```
<id> (<owner_kind>, <owner>) - covers <covers>. Install: <install>
```

Then the gaps, then the command list. Then stop.

**Rules:**

- Never run an install command without explicit approval. Show it; let the user decide.
- Check what is already installed and do not re-recommend it.
- Recommend the framework-team skill before the vendor one before the community one.
- Do not recommend every skill in a large collection. `microsoft/skills` has 175 skills;
  name the two that apply.
- When `index.json` reports `has_framework_team_skill: false` for the stack, say so
  plainly. It is useful information, not an embarrassment.

## Stack not in the registry

**This is the common case, not the exception.** There will always be more stacks outside
the catalog than inside it, so the quality of this path matters more than the number of
entries. Saying "not in the catalog, I will use my own doctrine" and then falling back to
stack-agnostic advice adds nothing - it is honest and useless at the same time.

Do all five, in order:

1. **Apply the category defaults.** `index.json` carries `category_defaults` keyed by
   backend / frontend / fullstack / mobile / infra: the decisions any stack in that
   category forces, and the operability rules that hold regardless of framework. These are
   weaker than a real entry but far stronger than nothing.
2. **Research the framework's own guidance, live.** Look for the maintainers' architecture
   guide, testing guide and project-structure page. Ten minutes of reading turns "I have no
   entry" into "the maintainers recommend this, and here is the part they leave to you".
   Cite what you find; label anything you could not confirm.
3. **Say which is which.** Be explicit about what came from the maintainers, what came from
   the category defaults, and what is your own judgment. The user is entitled to know how
   much weight each carries.
4. **Search for official skills** and report them with source URLs, labelled framework-team,
   vendor or community.
5. **Offer to contribute the entry.** You have just done the research a registry entry
   needs - offer to draft it. Point at `.github/ISSUE_TEMPLATE/new-stack.yml`. This is how
   the catalog grows: from the gaps its own users hit.

**Never state an install command or an architecture recommendation you have not seen in a
primary source.** Not from memory, not by analogy with another stack. A wrong install
command sends the user to a 404; a wrong architecture claim sends them to a rewrite.

## Failure messages

Be specific about which layer failed, because the user's next action differs:

| Situation | Say |
|---|---|
| Fetch failed | "Could not reach the remote registry; using the bundled copy from `<synced_at>`." |
| Stack missing | "`<stack>` is not in the catalog. Here is what I found by searching, and here is how to add it." |
| Entry unverified | "The catalog lists `<id>` but flags the install command as unverified. Check it before running." |
| No skills at all | "No official skills found for `<stack>`. I will work from the codebase and its documentation, applying the mentor's own doctrine." |
