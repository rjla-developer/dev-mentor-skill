# Delivery gates

Tests prove the code does what you meant. These gates ask a different question: **what
happens when it does not.** Structure and verification are covered elsewhere; this file is
about operability - everything that decides whether a project survives contact with real
users.

Every gate below is filtered through `project-stage.md`. A gate demanded at the wrong
stage is noise, and noise gets the whole mentor muted.

## Contents

- [How to use this](#how-to-use-this)
- [Gate 1 - Failure policy per boundary](#gate-1---failure-policy-per-boundary)
- [Gate 2 - Observability](#gate-2---observability)
- [Gate 3 - Authorization and secrets](#gate-3---authorization-and-secrets)
- [Gate 4 - Accessibility](#gate-4---accessibility)
- [Gate 5 - Definition of done](#gate-5---definition-of-done)
- [Gate 6 - Reversible data changes](#gate-6---reversible-data-changes)
- [Gate 7 - Rollback](#gate-7---rollback)
- [Gate 8 - Performance budget](#gate-8---performance-budget)
- [Gate 9 - Dependency hygiene](#gate-9---dependency-hygiene)
- [When each gate is due](#when-each-gate-is-due)
- [How to raise one](#how-to-raise-one)

## How to use this

Do not run all nine on every task. Run the ones the change touches, at the stage the
project is in. A gate is **answered**, not passed: the answer may be "we accept this risk
until production", and that answer gets written into the `## Deferred` section of
`CLAUDE.md`.

The single most valuable habit here is asking Gate 1 on every new external call. Agents
write happy paths by default, and nobody notices until the happy path ends.

## Gate 1 - Failure policy per boundary

**The question:** for each call that leaves this process - HTTP, database, queue,
filesystem, third-party SDK - what happens when it fails, is slow, or returns garbage?

**An answer is one of:** retry with a bound, degrade to something usable, fail loudly, or
queue for later. Silence is not an answer, and neither is a bare try/catch that swallows.

**What to check:** every boundary has a stated timeout, a stated retry count (including
zero), and a stated behaviour on exhaustion. Retries that stack with an SDK's own retries
are the classic invisible bug - the effective ceiling is the product, not the timeout.

**Failure mode if skipped:** the product hangs instead of failing. Users cannot tell a
slow system from a broken one, so they retry, which makes it worse.

**Due from:** `prototype` for anything on a network. A demo that hangs is worse than one
that says "unavailable".

## Gate 2 - Observability

**The question:** when this breaks in production, how do you find out, and how long does
it take to know which part broke?

**An answer includes:** where errors land, whether logs are structured, and whether one
identifier follows a request across components.

**What to check:** an unhandled failure produces a record somewhere a human will see. Logs
carry enough context to identify the user, the request and the operation - without carrying
personal data that should not be in a log.

**Failure mode if skipped:** you learn about outages from users, and debugging starts from
a screenshot. Retrofitting a correlation id after the fact means touching every layer.

**Due from:** `production`. It is a design decision made earlier - deciding at
`pre-release` costs a line; deciding after launch costs a refactor.

## Gate 3 - Authorization and secrets

**The question:** for each new entry point, who is allowed to call it? And is any
credential reachable from code that ships to a client?

**An answer is explicit, including "public on purpose".** An unguarded endpoint is
indistinguishable from a deliberately public one, and the difference only surfaces when it
is exploited.

**What to check:** every route, handler, action and job states its authorization decision.
No credential in the repository, in a client bundle, or in a log line. Authorization is
enforced in one place per entry point, not two.

**Failure mode if skipped:** the most expensive class of defect in the list, and the only
one with legal consequences.

**Due from:** `pre-release`, and immediately at any stage for secrets - a key committed to
a prototype is a leaked key.

## Gate 4 - Accessibility

**The question:** can this be used without a mouse, and by someone using a screen reader?

**An answer covers:** keyboard reachability and focus order, labels on interactive
elements, contrast, and that state changes are announced rather than only shown.

**What to check:** these are presentation rules, which means they are testable exactly like
any other presentation rule. Treat "the error is announced" the same way you treat "the
error is displayed".

**Failure mode if skipped:** the product is unusable for part of its audience, and in
several jurisdictions that is a legal exposure rather than a quality issue.

**Due from:** keyboard reachability at `prototype`; the rest at `production`. Front-end
stacks only.

## Gate 5 - Definition of done

**The question:** would a new developer get this running from a fresh clone in fifteen
minutes, and does "the tests pass" actually mean "this is shippable"?

**An answer is a written checklist** that includes a clean install from scratch, not just
a green suite on a machine that already works.

**What to check:** clone into an empty directory, follow the README, and see whether it
runs. This is the cheapest audit in the whole file and almost nobody does it.

**Failure mode if skipped:** onboarding costs days instead of an hour, and the gap between
"works" and "shippable" fills with undocumented steps living in one person's head.

**Due from:** `pre-release`.

## Gate 6 - Reversible data changes

**The question:** if this schema change is wrong, how do you undo it without losing data?

**An answer names the reverse operation** and whether it is lossy. Some are legitimately
irreversible - dropping a column destroys what was in it - and that must be known before
the deploy, not after.

**What to check:** the migration runs forward and backward. Deploys that need the old and
new code to coexist are split into two releases, not one.

**Failure mode if skipped:** the only failure in this list that can be permanently
unrecoverable.

**Due from:** `production`, or `pre-release` once real data exists.

## Gate 7 - Rollback

**The question:** this deploy is bad. What do you do in the next five minutes?

**An answer is a procedure**, not an intention. "Redeploy the previous version" only counts
if someone has done it.

**What to check:** the previous version is still deployable, and rolling back does not
strand a schema change the new version made.

**Failure mode if skipped:** a bad deploy becomes a debugging session in production while
users wait.

**Due from:** `production`.

## Gate 8 - Performance budget

**The question:** what is the limit, and how would you know you crossed it?

**An answer is a number with a way to measure it** - a request budget, a bundle size, a
response ceiling imposed by a platform. Without a number, "it feels slow" is the only
signal available, and it arrives late.

**What to check:** the budget is written down and something reports the real figure. Do not
optimise anything nobody has measured; that is speculation with extra steps.

**Due from:** `production`, or earlier when a platform imposes a hard ceiling - an
external timeout is a budget whether you wrote it down or not.

## Gate 9 - Dependency hygiene

**The question:** can this be built the same way in six months?

**An answer covers:** a committed lockfile, a policy on major upgrades, and awareness of
which dependencies are load-bearing and unmaintained.

**What to check:** the lockfile is committed. Nothing critical is pinned to a package with
no releases and open security issues. An upgrade that changes behaviour is its own change,
not a line in a feature PR.

**Due from:** `pre-release`.

## When each gate is due

| Gate | spike | prototype | pre-release | production | maintenance |
|---|---|---|---|---|---|
| 1 Failure policy | - | network only | all boundaries | all boundaries | all boundaries |
| 2 Observability | - | - | decide | required | required |
| 3 Authorization | secrets | secrets | required | required | required |
| 4 Accessibility | - | keyboard | keyboard | required | required |
| 5 Definition of done | - | - | required | required | required |
| 6 Reversible data | - | - | if real data | required | required |
| 7 Rollback | - | - | - | required | required |
| 8 Performance budget | - | platform limits | platform limits | required | required |
| 9 Dependencies | - | - | required | required | required |

A dash means **waste**, not "optional". Demanding it there is a mentor being wrong.

## How to raise one

Same five-field structure as any other finding, from `mentoring-voice.md`. Two additions
that matter here:

- **Name the stage that makes it due.** "This is due at production; you are at
  pre-release" is a plan. "You have no rollback plan" is nagging.
- **Offer the deferral.** If the honest answer is "not yet", say so and write it into the
  `## Deferred` section rather than leaving it unresolved. A recorded deferral is a
  decision; an unrecorded one is an oversight waiting to be rediscovered.
