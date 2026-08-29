# Quality gate

When a change earns a test, which layer it belongs in, and the rule about running the
suite that has no exceptions.

## Contents

- [The trigger: behavior, not files](#the-trigger-behavior-not-files)
- [The rule with no exceptions](#the-rule-with-no-exceptions)
- [What makes a test worth having](#what-makes-a-test-worth-having)
- [Why not a coverage target](#why-not-a-coverage-target)
- [Choosing the layer](#choosing-the-layer)
- [Golden and visual regression tests](#golden-and-visual-regression-tests)
- [Questioning the official skill](#questioning-the-official-skill)
- [Gate checklist](#gate-checklist)

## This file is the floor, not the ceiling

Everything here is stack-agnostic, which means a capable model already approximates most
of it. What actually changes an outcome is stack-specific and lives in the registry under
`testing`: which layer an assertion belongs in, the tell that it is at the wrong one, the
traps that make this stack's tests lie, and what is not worth testing at all.

**Read both.** Applying only this file produces a defensible suite that a competent agent
would have written anyway.

## The trigger: behavior, not files

**A test is required when behavior changes.** Not when a file changes.

| Change | Required |
|---|---|
| Business rule, calculation, validation, state transition | A new or updated test |
| Public API contract: signature, response shape, error case | A new or updated test |
| Bug fix | A test that fails before the fix and passes after |
| New endpoint, new command, new user-visible flow | A new test |
| Moving a file, renaming a private symbol, formatting | Existing suite stays green |
| Colour, spacing, copy | Existing suite stays green |
| Dependency bump with no behavior change | Existing suite stays green |

This is what keeps the gate compatible with the simplicity rule. Demanding a test for
every getter produces exactly the speculative noise that rule exists to prevent - and
teams respond by writing worthless tests to satisfy the gate, which is worse than having
no gate.

**Borderline case:** a refactor that is supposed to preserve behavior. No new test; the
existing suite is the proof. If there is no suite covering the refactored code, write the
characterization test *before* refactoring, not after. Otherwise you are not refactoring,
you are rewriting and hoping.

## The rule with no exceptions

**At the end of every task, run the full suite and report the real result.**

- Run the whole suite, not just the tests you wrote. Your change breaks other people's
  tests, not yours.
- Report the actual command and the actual output.
- If it fails: fix it, or say explicitly that it fails and what fails. Never quietly
  omit it.
- Never write "all tests pass" without having run them. This is the single most damaging
  thing an agent can do, because it teaches the user that green means nothing.

Get the command from the project's own scripts first (`package.json`, `Makefile`, CI
config), then from the registry's `testing.commands`. Never guess a runner.

If there is no suite at all, say so: "This project has no test suite; I could not verify
the change beyond running it." Then propose the first test, not a testing strategy
document.

## What makes a test worth having

Judge each test on utility, not on whether it exists:

| Property | Question | Failing it means |
|---|---|---|
| **Behavioral** | Does it test what the code does, not how? | It breaks on every refactor and teaches people to delete tests |
| **Predictive** | If it passes, does the feature actually work? | Green means nothing |
| **Specific** | When it fails, do you know where to look? | Debugging starts from zero |
| **Deterministic** | Same input, same result, every run? | Flaky tests get retried until green, then ignored |
| **Non-duplicative** | Does anything else already cover this? | Every change breaks five tests for one reason |
| **Worth its cost** | Does the confidence exceed the maintenance? | The suite becomes the thing slowing the team down |

A test that fails three of these is worse than no test, because it costs maintenance and
provides false assurance. Say so when you see one.

## Why not a coverage target

Never impose "80% coverage". Coverage measures which lines executed, not which behaviors
are protected. A suite that calls every function and asserts nothing scores 100%.

Use coverage as a **search tool**, not a goal: look at what is uncovered, and ask whether
any of it is a critical path. Uncovered critical paths are the finding. The percentage is
not.

If a project has a coverage gate in CI, respect it - it is that team's decision. Do not
introduce one.

## Choosing the layer

Invest heavily in the fast base, sparingly at the slow and brittle tip. Flutter's own
documentation puts it directly: a well-tested app has many unit and widget tests, plus
enough integration tests to cover the important use cases.

Community practice lands near 60% unit / 25% component / 10% integration / 5% end-to-end.
**Treat the shape as the point and the numbers as illustration** - a payments backend and
a marketing site have honestly different shapes.

| Layer | Catches | Costs | Do not use it for |
|---|---|---|---|
| **Unit** | Logic, calculations, edge cases, error paths | Cheap to write, cheap to run; breaks on refactor if it tests internals | Anything crossing a process or framework boundary |
| **Component / widget** | Rendering, state, interaction within one component | Moderate; needs a test harness | Whole-flow behavior |
| **Integration** | Wiring: DI, routing, serialization, real database and HTTP | Slow, needs fixtures, can be flaky | Enumerating every branch - do that in unit tests |
| **End-to-end** | The handful of flows whose breakage is an incident | Slowest, flakiest, hardest to debug | Coverage. It is the wrong tool for coverage |

**The layer question:** what is the cheapest test that would have caught this bug? Write
that one.

## Golden and visual regression tests

Golden tests assert pixels, not behavior. They catch unintended visual change, which
nothing else catches, and they fail for reasons unrelated to your change.

- They need a **pinned CI environment**. Font rendering differs across platforms, so a
  golden generated on macOS will fail on Linux CI for no real reason.
- **Never regenerate goldens to make a failure go away** without looking at the diff.
  Regenerating is how a real regression gets committed as the new expected output.
- Keep the set small. Every golden is a file that a legitimate design change invalidates.

## Questioning the official skill

**Never assume a framework-team skill is enough.** Before calling a task complete, re-read
the stack's `gap_map`.

As of each stack's `last_verified` date, **no framework-team skill in the registry
decides what deserves a test.** Some cover test authoring; one covers test execution and
testability. Selection - which behavior earns a test, and at which layer - is uncovered.
Do not trust this paragraph over the data: read the stack's `gap_map`, which is what gets
updated when that changes.

When the gap map names a skill that fills the gap, recommend it. When it does not, apply
this document directly and say that you are doing so.

## Gate checklist

```
- [ ] Classified the change: behavior or not
- [ ] If behavior: test written or updated, covering the boundary case
- [ ] Test is behavioral, specific and deterministic
- [ ] Full suite command taken from the project, not guessed
- [ ] Full suite run
- [ ] Real result reported, including failures
- [ ] gap_map re-read; testing gap for this stack handled
```
