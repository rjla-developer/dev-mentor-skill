# Roadmap

The 22 stacks the registry does not cover yet. Every one is ready to be copied into an
issue and picked up - each is labelled `good first contribution`, because adding a stack
needs research and honesty rather than familiarity with this codebase.

## Contents

- [How to claim one](#how-to-claim-one)
- [Backend](#backend)
- [Frontend and client](#frontend-and-client)
- [Definition of done](#definition-of-done)

## How to claim one

1. Open an issue with `.github/ISSUE_TEMPLATE/new-stack.yml`, titled `registry: add <stack>`.
2. Say in the issue that you are working on it, so two people do not duplicate the work.
3. Follow the template in `CONTRIBUTING.md`.
4. Open the pull request. You do not need permission to propose one.

You do not have to complete a whole entry. A file with three verified skills and four
fields marked `needs_verification: true` is a genuine contribution - the next person
starts from research instead of from nothing.

## Backend

| Stack | Key | Notes for the researcher |
|---|---|---|
| Node / Express | `express` | Check whether a framework-team skill exists at all; the ecosystem is fragmented. |
| Django | `django` | Look for a Django Software Foundation collection; check Python cross-cutting skills too. |
| Laravel | `laravel` | Laravel ships strong first-party tooling; check whether skills accompany it. |
| Go (Gin / Echo) | `go-web` | May need splitting per framework if detection markers diverge. |
| Ruby on Rails | `rails` | Convention-over-configuration means an unusually large `dead_code_risks` list. |
| Rust (Axum / Actix) | `rust-web` | Check for a Tokio or Axum maintainer collection. |
| Phoenix / Elixir | `phoenix` | LiveView changes what "component duplication" means; calibrate the thresholds. |
| Supabase | `supabase` | Vendor skills likely exist; verify what they cover beyond setup. |
| Firebase Functions | `firebase-functions` | Deployment and secrets belong in `gap_map` if uncovered. |
| GraphQL / Apollo | `apollo` | Cross-cutting rather than a stack; may belong in `index.json` instead. Decide and say why. |
| Serverless (Lambda / Workers) | `serverless` | Cloudflare publishes skills; check what covers Workers specifically. |

## Frontend and client

| Stack | Key | Notes for the researcher |
|---|---|---|
| Vue 3 | `vue` | Check for a Vue core-team collection. |
| Nuxt | `nuxt` | Detection must distinguish it from plain Vue. |
| Svelte / SvelteKit | `sveltekit` | Filesystem routing means convention files dominate `dead_code_risks`. |
| SwiftUI | `swiftui` | Community skills exist; verify publishers carefully before labelling one framework-team. |
| Jetpack Compose | `jetpack-compose` | Check for a Google/Android collection. |
| Astro | `astro` | Islands architecture changes the coupling thresholds. |
| Solid.js | `solidjs` | Small ecosystem; an honest empty `official_skills` may be the right answer. |
| Remix / React Router | `remix` | Overlaps `nextjs` on the React cross-cutting skills; do not duplicate them. |
| Qwik | `qwik` | Resumability changes what an "effect cascade" means; calibrate. |
| Ionic | `ionic` | Hybrid - decide `category` deliberately and justify it in `notes`. |
| shadcn/ui | `shadcn-ui` | Component library rather than a stack; probably belongs in `index.json` cross-cutting. Decide and say why. |

## Stack judgment: complete

Every stack in the registry now carries the four judgment fields. This is what separates a
catalog of links from a tool with an opinion.

| Field | What it answers |
|---|---|
| `architecture` | Which structural variant this framework's team recommends, and what breaks if you choose wrong |
| `testing` | Which layer an assertion belongs in, the tell it is at the wrong one, and how tests lie in this stack |
| `key_decisions` | The choices the stack forces with no framework default |
| `operability` | What a boundary, an authorization decision and a shippable build look like here |

| Stack | architecture | testing | key_decisions | operability |
|---|---|---|---|---|
| Flutter | framework-team | framework-team | done | done |
| Next.js / React | framework-team | framework-team | done | done |
| NestJS | framework-team | framework-team | done | done |
| Angular | needs_verification | done | done | done |
| React Native / Expo | needs_verification | done | done | done |
| FastAPI | needs_verification | framework-team | done | done |
| Spring Boot | needs_verification | framework-team | done | done |
| .NET | needs_verification | framework-team | done | done |

`needs_verification` on architecture means the layering is the mentor's judgment built on
documented conventions, not a maintainer mandate. The mentor says so when it recommends.
**Confirming those five against primary sources is the highest-value contribution
available right now** - the research is done, what is missing is a maintainer quote.

## How to fill a field without writing documentation

The line is sharper than it looks:

| Write this | Not this |
|---|---|
| "A test needing `pumpWidget` is testing the View - move it down" | "How to write a widget test" |
| "Goldens are generated in CI only; a local golden gives an indeterminate failure" | "What golden tests are" |
| "State management has no framework default; it reaches every view model" | "Comparison of Riverpod and Bloc" |
| "A fully mocked TestingModule passes while DI is broken" | "How Nest dependency injection works" |

The test: **could the model have written this line itself from general knowledge?** If yes,
it does not belong in the registry.

## Definition of done

A stack entry is complete when:

- [ ] `registry/<key>.json` validates: `python3 scripts/validate_registry.py`
- [ ] Every `source_url` was opened by a human, not inferred
- [ ] Every unconfirmed field carries `needs_verification: true` rather than a guess
- [ ] `gap_map` has at least one honest entry - if a stack truly has no gaps, say so in
      `notes` and explain why
- [ ] `testing.commands.full_suite` is present and correct
- [ ] `dead_code_risks` lists the convention-based and dynamic-access patterns specific to
      this stack
- [ ] `index.json` updated, including `has_framework_team_skill`
- [ ] `last_verified` set to the date you did the research
