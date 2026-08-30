# How it works

What this is, what it tries to do, and the mechanism it uses. Written so someone who has
never seen the repository can decide in five minutes whether it is worth installing.

## Contents

- [What it is](#what-it-is)
- [The problem it addresses](#the-problem-it-addresses)
- [What actually happens when you use it](#what-actually-happens-when-you-use-it)
- [The four things it knows that a model does not](#the-four-things-it-knows-that-a-model-does-not)
- [How it calibrates: project stage](#how-it-calibrates-project-stage)
- [What it does not do](#what-it-does-not-do)
- [What it costs](#what-it-costs)
- [The evidence](#the-evidence)

## What it is

A plugin for Claude Code. It sits in front of the work and does three things a coding
agent does not do on its own:

1. **Surfaces the decisions your stack forces on you** - the ones with no framework
   default, that get inherited for the life of a codebase - and refuses to pick them in
   silence.
2. **Applies the structural and testing rules the framework's own maintainers publish**,
   and says plainly when it is working from its own judgment instead.
3. **Asks what happens when the code fails** - not just whether it works - calibrated to
   how far along the project actually is.

It writes what it decided into your project's `CLAUDE.md`, so the next session starts from
what was already settled instead of re-deriving it.

## The problem it addresses

Framework teams have published hundreds of agent skills. Four things are still missing:

- **Nobody knows they exist.** The average user asks for an app and the agent improvises,
  installing nothing, when a skill written by the framework's maintainers was one command
  away.
- **Nobody orchestrates them.** No layer says: for your stack, install these, and here is
  what they still leave uncovered.
- **None of them teach.** They are capabilities, not judgment.
- **They have gaps.** Flutter's own skills cover layouts, routing and serialization. They
  do not cover testing strategy. Someone has to notice and fill that.

This project is that layer. **It contains no framework documentation of its own** - the
Flutter team published that documentation-only skills add no value, because models already
find that information, and that finding is the constraint this whole project is built
around.

## What actually happens when you use it

A real sequence, from a recorded run:

**1. It establishes what it understood, assumed, and cannot know.**

> *Asumido:* the model is Claude via API; Alexa cuts at ~8s so the model budget is 3-4s
> with a deterministic fallback; "Alexa did not understand" means fallback intent, not a
> model error.
>
> *Indefinido:* the level-up rule arrived truncated. I will not guess it, because it
> changes the data model.

Assumptions land **before** the code, where changing one costs a sentence. Not after,
where it costs a refactor.

**2. It resolves a live catalog and tells you what it does not know.**

> Registry consulted remotely (`synced_at: 2026-08-28`). **Alexa Skills Kit is not in the
> catalog** - the nearest entries are `nestjs` and `fastapi`, neither covers ASK SDK. I
> will work from the category defaults and my own doctrine, and tell you which is which.

The catalog lives outside the plugin and is fetched at run time, so a merged pull request
reaches every user without anyone reinstalling anything.

**3. It surfaces the forced decisions as choices, not questions.**

Not *"what do you want?"* but four enumerated readings with the cost of each - including
one the user had not noticed, the difference between counting turns and counting complete
dialogues, and what each implies for the data model.

**4. It builds, using the framework's rules.**

**5. It runs the real suite and reports the real numbers.** Never "done" without a run.

**6. It reports findings with evidence, and reports when there are none.**

Findings carry `file:line`, why it matters, the proposal, the reasoning, and the cost. And
when nothing crosses a threshold it says so - *"no signal crosses a threshold across 11
files"* - rather than inventing something to look thorough.

## The four things it knows that a model does not

Per stack, held in `registry/<stack>.json`:

| Field | The question it answers |
|---|---|
| `architecture` | Which structural variant this framework's team recommends, which layers are optional, and what breaks if you choose wrong |
| `testing` | Which layer an assertion belongs in, the tell that it is at the wrong one, and **how tests lie in this stack** |
| `key_decisions` | The choices the stack forces with no framework default, each with the cost of getting it wrong |
| `operability` | What counts as a failure boundary here, where authorization lives, and which commands prove shippable rather than merely green |

The bar for anything in the registry: **could the model have written this line from general
knowledge?** If yes, it does not belong there. "How to write a widget test" is out.
*"A test that needs `pumpWidget` is testing the View - move it down a layer"* is in.

For a stack with no entry - the common case - `index.json` carries `category_defaults` for
backend, frontend, fullstack, mobile and infra, and the mentor researches the framework's
own guidance live and offers to contribute the entry back.

## How it calibrates: project stage

This is what keeps it from being a checklist that gets muted.

*"You have no observability"* is a release blocker in production and pure noise on a
two-day spike. Same sentence. Nothing in a codebase says which one applies, so it asks
once and writes the answer into `CLAUDE.md`.

Five stages - `spike`, `prototype`, `pre-release`, `production`, `maintenance` - and for
each one the delivery gates carry three verdicts, not two: **required**, **deferred**, and
**waste**. A gate demanded at the wrong stage is the mentor being wrong.

What is deferred gets written down with the stage that makes it due. A recorded deferral
is a decision; an unrecorded one is an oversight waiting to be rediscovered at the worst
moment.

## What it does not do

Stated plainly, because the recorded comparisons do not support the opposite:

- **It does not write better code than a strong baseline.** Measured against Claude Code
  with 57 personal skills installed, the code quality was comparable.
- **It does not stop an agent deciding silently** - a capable agent often asks anyway. What
  it does is make asking a rule instead of a coincidence.
- **It is not a code generator, and not a documentation collection.**
- **It does not replace the official skills.** It routes you to them and covers what they
  leave open.

## What it costs

| | |
|---|---|
| `SKILL.md` plus all seven references | ~57,000 characters |
| Plus the registry and template, worst case | ~91,000 characters, roughly **23,000 tokens** |
| As a share of a 1M context window | **~2.3%** |

The read is not the real cost. The real cost is the work it induces: it asks questions,
researches live, writes a `CLAUDE.md`, and tests things the baseline skipped. That is the
point of it, and it is not free. To see the actual split for a session, run
`/explain-usage` in that session rather than trusting an estimate.

## The evidence

[`DEMO-COMPARISON.md`](DEMO-COMPARISON.md) is the running record of the same build task run
three times: once on a strong baseline, once with an early version of this plugin, once
after the operability work.

It includes a **"Predictions that failed"** section listing what this project expected and
got wrong, and a list of claims the evidence does **not** support. If you are evaluating
whether to use this, read that file before the README.
