# stack-canon

A Claude Code plugin that does two things and refuses to do more: it applies the
architecture **each framework team publishes for its own stack**, and it makes sure
business rules and presentation rules are both tested *and actually looked at*.

It used to do nine things. Five measured experiments supported two of them, so the rest
was cut. The experiments — including the ones this project lost — are in
[docs/DEMO-COMPARISON.md](docs/DEMO-COMPARISON.md).

## Install

```bash
/plugin marketplace add rjla-developer/stack-canon
/plugin install stack-canon@stack-canon-marketplace
```

Then just work. It triggers on anything that writes or changes code.

## What it actually does

**Before building, if it is not obvious where a request belongs — which platform, which
project, which layer — it asks once.** Then it builds. That single question exists because
one run asked it and built the right thing, while another decided alone and spent an hour
building something the user never wanted.

**Architecture comes from the framework team, not from taste.** For Flutter that is layered
MVVM, feature-first, repositories that never know about each other, and a domain layer that
stays absent until a second view model needs it — verified against
`docs.flutter.dev/app-architecture/guide`, not a blog. Eight stacks carry the same
treatment.

**Tests cover business rules and presentation rules, at the exact boundary.** A rule that
says "80% or more" gets 4/5 and 7/9, not a comfortable middle value. And then the app gets
launched and the screen looked at — because a green suite proves what you thought to
assert, not what you did not.

## Does it work?

Same Flutter app, built twice from the same prompt, then given the same two features.
Measured at three points:

| | Without | With |
|---|---|---|
| Duplicated blocks | 8 → 17 → **18** | 6 → 6 → **5** |
| Longest `build()` | 111 → 140 → **166** | 91 → 103 → **99** |

The registry's threshold for splitting a widget is 100. One codebase crossed it and kept
going; the other crossed once and came back under.

**And where it lost:** the baseline wrote broader tests in one experiment, found visual
defects twice that this skill missed, and asked the decisive question in a third. All
recorded, with the numbers.

## The registry

The catalogue lives outside the skill and is fetched at run time, so a merged pull request
reaches every user without anyone reinstalling anything. Eight stacks: Flutter, Next.js,
Angular, React Native/Expo, NestJS, FastAPI, Spring Boot, .NET.

Each carries the architecture its framework team recommends, the test rules and traps
specific to that stack, and the decisions the stack forces with no default. See
[docs/REGISTRY.md](docs/REGISTRY.md).

## Contribute

This catalogue ages fast — official teams publish every week, commands change, repositories
move. **Fork it, change it, send the pull request.**

- 22 stacks waiting, with a template: [docs/ROADMAP.md](docs/ROADMAP.md)
- A threshold that is wrong for real code: change it, with the evidence
- A command that no longer works: [report it](.github/ISSUE_TEMPLATE/stale-skill.yml)

One rule: **a fact you cannot verify gets marked `needs_verification: true`, never
guessed.** CI rejects the alternative.

## Credits

The architecture doctrine belongs to the Flutter, Angular, Next.js, Expo, NestJS, FastAPI,
Spring and .NET teams — this project only routes to it and says where it stops. The method
owes Andrej Karpathy's principles for agent behavior and Kent Beck's test desiderata over
coverage numbers.

MIT. See [LICENSE](LICENSE).
