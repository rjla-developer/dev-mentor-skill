# Architecture

How the pieces fit, and why each one is where it is.

## Contents

- [The shape](#the-shape)
- [Three skills, three jobs](#three-skills-three-jobs)
- [Why the registry is not in the skill](#why-the-registry-is-not-in-the-skill)
- [Why a hook enforces the CLAUDE.md cap](#why-a-hook-enforces-the-claudemd-cap)
- [Degrees of freedom](#degrees-of-freedom)
- [Progressive disclosure](#progressive-disclosure)
- [Data flow](#data-flow)
- [What runs in CI](#what-runs-in-ci)

## The shape

```
.claude-plugin/     plugin + marketplace manifests
skills/
  dev-mentor/       orchestrator - the entry point
    references/     five files, one level deep from SKILL.md
  mentor-review/    deep audit, invoked explicitly
  mentor-clean/     dead code removal, plan-gated
    scripts/        deterministic - the model does not improvise here
registry/           the catalog: schema, index, one file per stack
hooks/              the CLAUDE.md line cap
templates/          CLAUDE.md and sub-file templates
scripts/            repository tooling: validators, sync, flatten
evals/              scenarios, written before the documentation
docs/               this directory
```

## Three skills, three jobs

**`dev-mentor`** runs on nearly every task. It detects the stack, resolves the registry,
recommends skills, keeps `CLAUDE.md` honest, enforces the quality gate, and watches the
growth signals. Its reactive mentoring is deliberately shallow: at most two findings, only
with evidence.

**`mentor-review`** is the deep pass, invoked explicitly. Six passes, teaching mode, up to
five ranked findings with full reasoning. It reads and reports; it does not refactor.

**`mentor-clean`** is the dangerous one. Everything about it is built to make an
unreviewed deletion impossible: two script-enforced preconditions, a plan artifact, an
approval step, a re-validation immediately before execution, a dedicated branch, and an
automatic revert.

They are separate skills rather than modes of one skill because they have different
trigger conditions and very different risk profiles. Bundling them would mean the
dangerous one loads on every task.

## Why the registry is not in the skill

A skill is static markdown. It learns nothing after it ships.

Framework teams publish new skills continuously. A catalog hardcoded into `SKILL.md`
starts lying the day after it is written and keeps lying until someone edits and
republishes the skill. So the catalog lives in `registry/`, is fetched over HTTPS at run
time, and falls back to the bundled copy with the sync date stated out loud.

This is the same pattern Vercel's UI quality skill uses: fetch the canonical guidelines
before each run rather than freezing a copy inside the skill.

The consequence that matters: **a merged pull request reaches every user immediately.**
Nobody reinstalls anything.

## Why a hook enforces the CLAUDE.md cap

Asking a model to keep a file under 150 lines works most of the time. "Most of the time"
is exactly how a 400-line `CLAUDE.md` comes to exist, and a `CLAUDE.md` that long stops
being read carefully - the rules its author cared about most are the ones that get
skipped. Shouting in capitals does not fix this; it is a documented community failure.

So the cap is a `PostToolUse` hook on `Write` and `Edit` that exits 2 with an actionable
message. Deterministic, not aspirational.

**Do not add a `hooks` field to `.claude-plugin/plugin.json`.** `hooks/hooks.json` is
loaded automatically by convention; declaring it in the manifest as well makes the plugin
fail to load with *"Duplicate hooks file detected"* - the skill still loads, but the hook
silently never fires, which is the worst possible failure for a guardrail. The manifest
field is only for *additional* hook files. This was shipped broken in 0.1.0 and found the
first time the plugin was installed from the marketplace.

## The doctrine has a token cost

Loading a reference puts it in context, and that bill arrives on every run. Measured
before any of this was addressed: **~26k tokens per run** - 4.4k for `SKILL.md`, 12.9k for
the whole reference set loaded up front, and ~8.2k for printing two registry files whole.

That is 2.6% of a 1M window, so it was never catastrophic. The problem was the trajectory:
`delivery-gates.md` alone reached 11.9k bytes, and this project capped the *user's*
`CLAUDE.md` at 150 lines while exempting its own doctrine from any limit at all.

Three rules and a cap:

1. **A project's `CLAUDE.md` replaces the references.** It is the doctrine already
   distilled for that codebase - architecture rules, test rules, the landmines that
   project actually hit - at ~1.6k tokens against ~12.9k for the reference set. Run two
   onwards reads it instead.
2. **Never pre-load.** A reference loads when its step is reached. A prototype never needs
   `delivery-gates.md`; a typo fix needs almost none of it.
3. **Filter the registry.** Fetch the stack entry to a file and read the fields the step
   needs, rather than printing 300 lines of JSON.
4. **`MAX_REFERENCE_BYTES` and `MAX_REFERENCES_TOTAL`** in `scripts/validate_skills.py`
   freeze the growth. Both sit just above today's values on purpose: adding to the doctrine
   now requires taking something out.

Measured effect: **~26k to ~12k on a new project, and to ~7k on a project that already has
a generated `CLAUDE.md`.** Not the tenth that was estimated before measuring - `SKILL.md`
itself is 4.4k and always loads, which sets the floor.

What is deliberately *not* optimised is the test-iteration loop. Writing a test, running
it, reading the failure and fixing it costs a few thousand tokens per task, and that is the
work. Cutting there means shipping unverified code; cutting the doctrine reload costs
nothing.

## Degrees of freedom

Calibrated per task, following the guidance that judgment work wants prose and
consistency work wants scripts.

| Area | Freedom | Why |
|---|---|---|
| Stack choice, architecture, mentoring | High - prose instructions | Every codebase differs; a script would be wrong more often than right |
| Growth signals | Medium - numeric thresholds, prose interpretation | The number is checkable; whether it matters here is judgment |
| Registry validation | Low - `scripts/validate_registry.py` | Consistency is the whole value |
| CLAUDE.md cap | Low - a hook | Compliance must not depend on attention |
| Dead code cleanup | Lowest - two scripts, no override flags | The cost of one wrong deletion outweighs the convenience of every right one |

## Progressive disclosure

- `SKILL.md` under 500 lines, always.
- References are **one level deep**. `SKILL.md` points at `references/x.md`; `x.md` points
  at nothing else. Nested references get read partially - a `head -n` of a chained file
  hands the model a fragment it cannot tell is a fragment.
- Reference files over 100 lines carry a table of contents, so a partial read still knows
  what it missed.

`scripts/validate_skills.py` enforces all three in CI.

## Data flow

```
user request
   |
   v
dev-mentor SKILL.md ---> references/*.md        (judgment, loaded on demand)
   |
   +--> detect stack from manifests
   |
   +--> registry: remote fetch -> bundled copy -> live search
   |
   +--> recommend skills (never install without approval)
   |
   +--> delegate execution to the official skill
   |
   +--> quality gate: test required? run full suite, report the real result
   |
   +--> growth signals: evidence or silence
   |
   v
three-line status block
```

## What runs in CI

`validate.yml` on every push and pull request:

- registry against `schema.json`, plus invariants the schema cannot express (filename
  matches `stack`, `install: null` implies `needs_verification`, `index.json` agrees with
  the stack files)
- every `SKILL.md` against the authoring rules
- the plan scripts start and print help
- the `CLAUDE.md` hook, tested on both sides of the cap
- every eval scenario parses and declares at least three observable expectations

`sync-registry.yml` weekly: probes every `source_url`, writes a report, opens a pull
request. It never merges.
