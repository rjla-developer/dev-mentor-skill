# Project stage

What a project owes depends on who is depending on it. A mentor that applies production
standards to a two-day spike is not rigorous, it is useless - and it gets muted.

## Contents

- [Why this exists](#why-this-exists)
- [The five stages](#the-five-stages)
- [How to detect the stage](#how-to-detect-the-stage)
- [What each stage owes](#what-each-stage-owes)
- [Deferral is a decision, not an omission](#deferral-is-a-decision-not-an-omission)
- [Stage transitions](#stage-transitions)

## Why this exists

"You have no observability" is noise on a prototype and a release blocker in production.
The same sentence. The difference is the stage, and nothing in a codebase states it.

So ask, once, and write it into `CLAUDE.md`. Every later recommendation is filtered
through it. This is the difference between a mentor and a linter with opinions: a linter
does not know what the project is for.

## The five stages

| Stage | Who depends on it | The question that defines it |
|---|---|---|
| `spike` | Nobody. It answers a question and dies. | Will this be deleted next week? |
| `prototype` | People who will see it, not rely on it. | Would a failure embarrass you, or cost someone? |
| `pre-release` | Nobody yet, but soon and for real. | Are you building toward a date with users? |
| `production` | Real users, right now. | Does a bad deploy cost someone something? |
| `maintenance` | Real users; change is rare and risk-managed. | Is the main risk now breaking what works? |

`spike` and `prototype` are not lesser stages. Applying production discipline to a spike
destroys the only thing a spike is for, which is speed of learning.

## How to detect the stage

Ask. It takes one line and the answer cannot be inferred reliably.

Signals worth checking first, so the question is informed rather than blank:

| Signal | Suggests |
|---|---|
| No git history, or a single commit | `spike` or `prototype` |
| No CI, no deploy config | `spike`, `prototype`, early `pre-release` |
| CI, deploy config, error tracking wired | `production` |
| A changelog, release tags, a version | `production` or `maintenance` |
| Open issues about migrations and rollbacks | `production` |
| Commits are mostly dependency bumps | `maintenance` |

State what you inferred and let the user correct it: *"This looks like a prototype - no CI
and no deploy config. Say if it is heading to production sooner than that."*

## What each stage owes

The middle column is the one that keeps this useful. **Waste** means: doing it here costs
more than it returns, and a mentor that demands it is wrong.

### `spike`

- **Required:** nothing but that it runs, and that it is labelled a spike so nobody ships it.
- **Waste:** tests, architecture, error handling, observability, docs.
- **The one rule:** a spike that survives two weeks is no longer a spike. Re-stage it.

### `prototype`

- **Required:** tests on the rules being demonstrated - the demo must not lie. A stated
  failure policy for anything that talks to a network, because a demo that hangs is worse
  than one that says "unavailable".
- **Deferred, and recorded:** observability, migrations, performance budgets, a11y beyond
  keyboard reachability.
- **Waste:** full test coverage, extraction into packages, rollback plans.

### `pre-release`

- **Required:** business rules under test; failure policy at every external boundary;
  authorization decided per endpoint including "public on purpose"; secrets out of the
  repository; a README a new developer can follow.
- **Deferred, and recorded:** performance budgets unless a target is already known.
- **Waste:** optimising anything nobody has measured.

### `production`

- **Required:** everything above, plus - observability that answers "is it broken right
  now"; reversible migrations; a rollback path; a11y for anything user-facing; a stated
  definition of done that includes running clean from a fresh clone.
- **Waste:** nothing on this list. This is the stage where the five gaps are all real.

### `maintenance`

- **Required:** everything from production, plus a bias against change. Every change
  states what it risks and how it is reverted.
- **Waste:** refactors with no observed defect. Here more than anywhere, the
  Research-to-Action Gate is the whole job.

## Deferral is a decision, not an omission

At every stage below `production`, things are deliberately not done. The difference
between a fast team and a reckless one is that the fast team **wrote down what it skipped**.

Record deferrals in the project's `CLAUDE.md` under a heading the next person will find,
with the stage that makes them due:

```
## Deferred

- Observability — due at production. Nothing currently reports a failed turn.
- Reversible migrations — due at production. Schema changes are hand-applied.
```

An undocumented deferral is indistinguishable from an oversight, and it will be
rediscovered at the worst possible moment by someone who assumes it was never considered.

## Stage transitions

The transition is the moment to re-audit, and it is the only time a large batch of
findings is appropriate. Moving `pre-release` -> `production` means every deferral in that
list comes due at once.

Say so plainly when the stage changes: *"Moving this to production makes four deferred
items due. Here they are, ranked by what a failure costs."*
