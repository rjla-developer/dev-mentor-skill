# Philosophy

Why this project exists, what it refuses to do, and where the ideas came from.

## Contents

- [The problem](#the-problem)
- [What this is not](#what-this-is-not)
- [Principles](#principles)
- [Tradeoffs we accept](#tradeoffs-we-accept)
- [Sources](#sources)

## The problem

Framework teams have published hundreds of excellent agent skills. Four things are still
missing.

**Nobody knows they exist.** The average user asks an agent to build an app and the agent
improvises, installing nothing, when a skill written by the people who maintain the
framework was one command away.

**Nobody orchestrates them.** There is no layer that says: for your stack, install these
three, in this order, and here is what they still leave uncovered.

**None of them teach.** They are capabilities - how to build a responsive layout - not
judgment: you have forty widgets duplicating one button, extract a component library.

**They have gaps.** Flutter's framework-team skills cover layouts, routing and JSON
serialization. They do not cover testing strategy. Someone has to notice that and fill it.

## What this is not

**Not a documentation collection.** The Flutter team published that skills which only
provide documentation add no value, because modern models already find that information -
so they pivoted to task-oriented skills. This project applies the same lesson: zero
duplicated documentation, anywhere.

**Not a reimplementation.** Whatever a framework-team skill does, it does better than we
would. Delegate, and say so.

**Not a code generator.** It is a layer of judgment, orchestration and quality.

## Principles

**Brutal concision.** The context window is a shared resource. Every paragraph must
justify its tokens. If the model already knows it, do not write it down.

**Progressive disclosure.** `SKILL.md` under 500 lines. References one level deep - never
`SKILL.md -> a.md -> b.md`, because partially-read nested files hand the model a fragment
it cannot tell is a fragment. Files over 100 lines carry a table of contents.

**Calibrated degrees of freedom.** Prose where judgment is needed; scripts with no
parameters where consistency is critical and a mistake is expensive.

**Evidence before recommendation** (the Research-to-Action Gate). Every refactor proposal
cites a concrete defect in *this* codebase, with `file:line`. No evidence, no
recommendation. This is what separates a mentor from a fashion feed.

**Test desiderata over coverage numbers.** A test earns its place by being behavioral,
predictive, specific, deterministic, non-duplicative and worth its maintenance - not by
moving a percentage. A suite that calls everything and asserts nothing scores 100%.

**Plan, validate, execute, verify** for anything destructive. Never direct execution.

**No time-sensitive content.** No "as of August 2026, use X". Superseded material moves to
a collapsed *Older patterns* section rather than aging in place at the top of a file.

## Tradeoffs we accept

**Caution costs speed.** The understanding contract, the approval gates and the plan
artifacts all add turns. On trivial work that overhead is real and unjustified, which is
why the skills shorten the flow for trivial work and say that they did.

**Explanation costs tokens.** The five-field recommendation format is longer than a
one-line lint message. That cost is the product: a linter tells you what; a mentor tells
you why, and the user carries the why to the next project.

**Honesty costs completeness.** Several registry entries ship flagged
`needs_verification` rather than filled with plausible values. A catalog with honest gaps
is more useful than one that looks complete and 404s.

**The registry ages.** It is the weakest part of the design and always will be. The
mitigations are structural: fetch remotely so a merged PR reaches everyone, state the
sync date whenever the bundled copy is used, probe every URL weekly, and make
contribution the path of least resistance.

## Sources

The design borrows deliberately, and says from whom:

- **Anthropic's skill-authoring guidance** - progressive disclosure, concision, degrees of
  freedom, evaluations written before documentation.
- **The Flutter team** - the finding that documentation-only skills add no value, which is
  the constraint this project is built around.
- **Vercel** - fetching a canonical source at run time instead of freezing a copy inside
  the skill.
- **Andrej Karpathy's four principles** for agent behavior - think before coding,
  simplicity first, surgical changes, goal-directed execution.
- **Kent Beck's test desiderata** - judging tests by their properties rather than by a
  coverage number.
- **Trail of Bits, Microsoft, the .NET team, the Angular team, Expo, Callstack, Cloudflare
  and TestMu AI** - the skills the registry points at, which are the reason an
  orchestration layer is worth having at all.
