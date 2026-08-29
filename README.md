# dev-mentor-skill

An orchestrator and technical mentor for Claude Code. It finds the agent skills that
framework teams have already published for your stack, tells you exactly what those skills
do **not** cover, and stays in the loop as a mentor: watching architectural health,
enforcing that behavior changes ship with tests, and explaining the reasoning behind every
recommendation.

Flutter, Angular, Expo, Vercel, Microsoft, the .NET team, Trail of Bits, Cloudflare and
others have published hundreds of excellent skills. Almost nobody installs them, nothing
orchestrates them, none of them teach judgment, and all of them have gaps - Flutter's
framework-team skills cover layouts, routing and JSON serialization, but not testing
strategy. This project is the layer on top: it routes you to the right official skills,
covers what they leave open, and explains why. **It contains no framework documentation of
its own** - the Flutter team found that documentation-only skills add no value, and that
finding is the constraint this whole project is built around.

## Install

```bash
/plugin marketplace add rjla-developer/dev-mentor-skill
/plugin install dev-mentor@dev-mentor-marketplace
```

## Getting started

After installing, `dev-mentor` activates on its own whenever you ask for something that
touches code. Models tend to under-trigger skills though, so if you want a deterministic
start - or you are not sure it woke up - paste one of these into your project.

### You are starting from zero

> Use dev-mentor. I want to build **&lt;what you want to build&gt;**. Run the full workflow:
> understanding contract, stack options with their tradeoffs, registry resolution, skill
> recommendations, and CLAUDE.md. Do not install anything and do not write code until I
> confirm the stack.

It will state what it understood and assumed, give you 2-3 stacks with a one-line tradeoff
each, say which it recommends and why, and stop. Nothing is scaffolded until you answer.

### You already have a project

> Use dev-mentor on this repository. Detect the stack, resolve the registry, and tell me:
> which official skills I should have installed, what those skills do not cover, and what
> you would fix first with file:line evidence. Then generate or update CLAUDE.md.
> Do not change any code yet.

It reads your manifests to detect the stack - no questions needed - then reports the
skills you are missing, the gaps they leave, and any growth signal it can back with
evidence. Read-only until you say otherwise.

### After that

Just work normally. The mentor stays in the loop: it enforces the quality gate on every
behavior change, watches the growth thresholds, and ends each turn with a three-line
status block telling you which skills are active and what it would suggest next.

Two commands are always available:

| Command | When |
|---|---|
| `/mentor-review` | You want the deep audit: six passes, up to five ranked findings, teaching mode |
| `/mentor-clean` | You want dead code gone - safely, through a plan you approve |

If the skill does not seem to activate, say so explicitly: *"use the dev-mentor skill"*.

## What it looks like

```
You: I want to build an app with a backend and a frontend.

dev-mentor:
  Understood: a full application, front and back. Assumed: web, not mobile - say so if
  that is wrong. Undefined: the stack, and whether you need SSR.

  Three options:
  - Next.js full stack — one language, one deploy, fastest to first screen. Weakest when
    the backend grows real domain logic.
  - Angular + NestJS — same language, strong conventions on both sides, more setup.
  - Next.js + FastAPI — best if the backend will do data or ML work. Two ecosystems.

  I would pick the first unless you already know the backend gets complicated. Which one?

You: the first one.

dev-mentor:
  Stack: Next.js. Catalog resolved (registry synced 2026-08-27).

  Recommended:
  - vercel-labs/agent-skills (vendor, Vercel) — React performance, data fetching, UI
    review.  npx skills add vercel-labs/agent-skills

  What it does not cover, and I will handle myself:
  - Test strategy — nothing in that collection decides what deserves a test.
  - Server boundary discipline — no skill audits 'use client' boundaries or checks that
    server actions authorize.

  Install it? I will not run anything without your go-ahead.

  [...work happens...]

  Quality gate: pricing rule changed → test added at tests/pricing.test.ts:24, including
  the boundary at exactly 100. Ran `npm test`: 48 passed, 0 failed.

🧭 Active skills: dev-mentor
   Available: /mentor-review (deep audit) · /mentor-clean (dead code)
   Suggested: cloudflare/skills#web-perf — nothing currently measures your Core Web Vitals
```

## What it does

| | |
|---|---|
| **Detects your stack** | From manifests, with marker confirmation - never from a file extension |
| **Resolves a live catalog** | Remote fetch, bundled fallback with the date stated, live search as last resort |
| **Recommends, never installs** | You always see the command and decide |
| **Names the gaps** | The part nobody else writes down |
| **Generates CLAUDE.md** | Capped at 150 lines by a hook, not by good intentions |
| **Enforces a quality gate** | Behavior changed → a test exists. Every task ends with a real suite run and a real result |
| **Watches growth signals** | Eight thresholds, each requiring `file:line` evidence before it says anything |
| **Removes dead code safely** | Plan → validate → approve → execute on a branch → verify → auto-revert |

Three skills: `dev-mentor` (always), `/mentor-review` (deep audit on demand),
`/mentor-clean` (dead code).

## Registry status

Verified 2026-08-27. `needs_verification` means the entry exists but one field could not
be confirmed from a primary source - the mentor repeats that caveat to you rather than
guessing.

Every stack also carries four judgment fields - `architecture`, `testing` rules and traps,
the `key_decisions` the stack forces with no default, and `operability`. That is the part a
capable model cannot supply on its own.

| Stack | Framework-team skill | Notes |
|---|---|---|
| Flutter | yes - `flutter/agent-plugins`, `dart-lang/skills` | Testing strategy is the documented gap |
| Angular | yes - `angular/skills` | Broadest framework-team coverage in the registry |
| React Native / Expo | yes - `expo/skills` (22 skills) | Plus Callstack for performance |
| .NET | yes - `dotnet/skills` (16 plugins) | Closest thing to a framework-team testing skill |
| Next.js / React | no - `vercel-labs/agent-skills` (vendor) | No dedicated Next.js caching or upgrade skill exists |
| FastAPI | partial - a skill ships inside `fastapi/fastapi` | Install route flagged `needs_verification` |
| NestJS | **no** | No NestJS-team collection found. Community options exist; none is canonical |
| Spring Boot | **no** | Largest gap in the registry. If you find one, please open an issue |

Not covered yet: 22 stacks in [docs/ROADMAP.md](docs/ROADMAP.md).

## Contribute

**This catalog ages fast.** Official teams publish new skills every week, install commands
change, repositories move.

If you notice that a technology is missing, that a command changed, that an official skill
no longer exists, or that one of our thresholds is miscalibrated: **fork it, change it, and
send the pull request.** We read it, and if it holds up, it goes in. You do not need
permission to propose something.

The one rule: **an unverifiable field is marked `"needs_verification": true`, never
guessed.** A wrong install command sends someone to a 404, and once that happens the whole
catalog stops being trusted.

- Adding a stack → [CONTRIBUTING.md](CONTRIBUTING.md) and
  [.github/ISSUE_TEMPLATE/new-stack.yml](.github/ISSUE_TEMPLATE/new-stack.yml)
- Reporting a stale entry →
  [.github/ISSUE_TEMPLATE/stale-skill.yml](.github/ISSUE_TEMPLATE/stale-skill.yml)
- Good first contributions → [docs/ROADMAP.md](docs/ROADMAP.md)

## Documentation

| | |
|---|---|
| [docs/PHILOSOPHY.md](docs/PHILOSOPHY.md) | Why this exists, what it refuses to do, the tradeoffs |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | How the pieces fit and why |
| [docs/REGISTRY.md](docs/REGISTRY.md) | How the catalog works and stays current |
| [docs/ROADMAP.md](docs/ROADMAP.md) | The 22 stacks still to cover |
| [evals/](evals/) | Scenarios, written before the documentation |

## Credits

This design borrows deliberately:

- **Anthropic** - skill authoring: progressive disclosure, concision, degrees of freedom,
  evaluations before documentation.
- **The Flutter team** - the finding that documentation-only skills add no value. The
  reason this project stores judgment instead of content.
- **Vercel** - fetching a canonical source at run time rather than freezing a copy in the
  skill.
- **Andrej Karpathy** - the four principles of agent behavior.
- **Kent Beck** - test desiderata over coverage percentages.
- **Trail of Bits, Microsoft, the .NET team, the Angular team, Expo, Callstack, Cloudflare
  and TestMu AI** - the skills the registry points at, and the reason an orchestration
  layer is worth building.

## License

MIT. See [LICENSE](LICENSE).
