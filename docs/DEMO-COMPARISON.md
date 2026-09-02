# Demo comparison log

A controlled A/B of the same build task, run twice: once with the developer's normal
setup, once with that setup plus `dev-mentor`. This file is the running record - what was
held constant, what was observed, and which claims the evidence actually supports.

It is written to be falsifiable. Anything that turned out differently from what we
expected is recorded as such, including our own wrong predictions.

## Contents

- [Environment](#environment)
- [The task](#the-task)
- [Run A - baseline](#run-a---baseline)
- [Run B - with dev-mentor](#run-b---with-dev-mentor)
- [Observed differences](#observed-differences)
- [Predictions that failed](#predictions-that-failed)
- [Claims we can and cannot make](#claims-we-can-and-cannot-make)
- [Control caveats](#control-caveats)

## Environment

Held identical across both runs unless noted.

| | Value |
|---|---|
| Machine | MacBook Air, macOS |
| Model | Opus 5 (1M context), Claude Max |
| Permission mode | auto mode on |
| User skills active | **57** in `~/.claude/skills` (the gstack suite) |
| Plugins | `swift-lsp@claude-plugins-official` |
| Network | Available |
| API keys | None provided - tests had to run without network or credentials |

**The only intended difference:** run B additionally has `dev-mentor` installed from
`rjla-developer/dev-mentor-skill` via the plugin marketplace.

This is deliberately **not** a clean-room comparison against a bare Claude. It answers the
question a reader actually has: *"I already have my skills - does this add anything?"* A
comparison against zero skills would answer a question nobody is asking.

## The task

Identical prompt, pasted verbatim into both runs: build the full turn of an Alexa English
tutor skill - transcript in, model correction, spoken reply out, progress record updated -
with four progress rules carrying exact thresholds (30%, 3 clean dialogues, 3
misunderstandings), and a latency constraint. No deploy, no Amazon console.

The prompt deliberately says **nothing** about stack, tests, `CLAUDE.md`, or which skills
to use. Those absences are what the comparison measures.

**Known defect in the prompt:** one rule arrived truncated - *"El alumno sube de nivel en
un escenario cuando compluidos sin ningún error"*, missing the number and the noun. It was
truncated identically in both runs, so it does not break the comparison. It turned into a
useful probe: both runs had the chance to guess or to ask.

## Run A - baseline

Directory: `english-mentor`. Duration: **13m 26s**.

What it did:

1. Checked the directory was empty.
2. **Stopped and asked two questions before writing any file:**
   - the truncated level-up rule -> answered "3 dialogues in a row without errors"
   - **"¿Sobre qué stack construyo el turno?"** -> answered "Node.js + ASK SDK v2"
3. Loaded the bundled `claude-api` skill and read its TypeScript reference.
4. Built `src/domain`, `src/tutor`, `src/handlers`, `src/persistence`, `models`, `test`.
5. Hit a real dependency problem: `@anthropic-ai/sdk` 0.70.1 lacked the API it needed.
   Diagnosed it, upgraded to 0.122.0, upgraded `zod` to v4, got a clean typecheck.
6. Ran the suite: **33 tests, 33 passing**, no network, no keys.
7. Wrote a 144-line `README.md`.
8. Reported three judgment calls it had made, plus a locale problem it could not solve in
   code (invocation in Spanish, learner answers in English, one recognizer for both).

Artifacts: `src/`, `test/`, `models/en-US.json`, `models/es-ES.json`, `README.md`,
`.env.example`, `tsconfig.json`, `tsconfig.test.json`, `package.json`.
**No `CLAUDE.md`.**

**This is a strong baseline.** Any claim that dev-mentor "produces better code" is not
supported by this run and should not be made.

## Run B - with dev-mentor

Directory: `english-mentor-with-skill`. Claude Code 2.1.251. Completed.

1. Read its own plugin files - `behavioral-rules.md`, `orchestration.md`,
   `mentoring-voice.md`, `quality-gate.md`, `growth-signals.md`, `CLAUDE.md.template`.
2. **Fetched the live remote registry.** `curl` to
   `raw.githubusercontent.com/rjla-developer/dev-mentor-skill/main/registry/index.json`,
   returning `synced_at: 2026-08-28`. First production exercise of the three-layer
   resolution described in `docs/REGISTRY.md`.
3. Opened with the understanding contract before writing anything: **Entendido**;
   **Asumido** - four contestable assumptions (Claude via API, ~8s Alexa cutoff giving a
   3-4s model budget, the definition of "Alexa did not understand", where scenario state
   lives); **Indefinido** - refused to guess the truncated rule and said why, *"cambia el
   modelo de datos"*.
4. **Reported the gap in its own catalog, unprompted:** Alexa absent, nearest entries
   `nestjs` and `fastapi`, neither covers ASK SDK; would work from its own doctrine and
   offered to open an issue.
5. Asked **three** decisions - level-up rule, stack, persistence - each with enumerated
   readings and the cost of each. Run A asked two and decided persistence alone.
6. Built with vitest. **19 tests passing.** Typecheck clean.
7. **Wrote `CLAUDE.md` (110 lines)** from the plugin template: stack, exact commands,
   layer boundaries, and architectural decisions each with its reason.
8. Reported an explicit **quality gate**: both commands, both results.
9. Reported one architectural finding in the five-field structure, with evidence -
   `models/en-US.json:18-21`, `AMAZON.SearchQuery` needs a carrier phrase, so the learner
   must say *"I say, a table for two"*; proposal, reasoning, and cost all stated.
10. **Reported growth signals as a negative result:** *"ninguna cruza umbral en 13
    ficheros"*, explicitly declining to count the single-implementation `ProgressStore`
    port as a finding because it was the developer's decision, not an observed defect.
11. Declared what it had not measured: *"No he medido la latencia real (no hay clave en
    este entorno)"*.
12. Ended with the three-line status block, including a concrete suggestion.

## Test suites compared

Both suites were read, not counted. "19 vs 33" is not a finding on its own.

| | Run A | Run B |
|---|---|---|
| Tests | **33** | 19 |
| Test code | **689 lines** | 299 lines |
| Runner | `node:test` | vitest |
| Rule boundaries covered | Yes | Yes |
| SSML escaping of learner and model text | **Yes** | No |
| Persistent attributes not clobbered on save | **Yes** | No |
| Backward-compatible record migration | **Yes** | No |
| Level cap, cross-session level retention | **Yes** | No |
| CommonJS/ESM entrypoint interop | No | **Yes** |
| Selection justified in the report | No - a count | **Yes - boundaries named** |

**Run A's suite is broader, and the extra tests are not padding.** It covers SSML escaping
of untrusted learner and model text, not clobbering unrelated persistent attributes, and
filling missing fields when reading an older record. Real failure modes that run B never
touches.

Run B's suite is tighter, and every test is justified in the final report - including why
the interop test exists (`ask-sdk-core` is CommonJS, the project is ESM, and that only
breaks when the entrypoint loads).

**Run A wins on test coverage. Do not claim otherwise.**

## Observed differences

Only differences with direct evidence in a transcript.

| Dimension | Run A | Run B |
|---|---|---|
| Asked before writing code | **Yes** - 2 questions | **Yes** - 3 questions |
| Stack chosen by | The developer | The developer |
| Shape of the ambiguous question | Open-ended | **4 enumerated readings, each with its cost** |
| Assumptions stated | At the end, as 3 post-hoc decisions | **Up front**, as 4 contestable assumptions |
| Decisions surfaced | 2 | 3 - also **persistence** |
| Consulted a skill catalog | No | **Yes - live remote fetch, date reported** |
| Declared what it does not know | No | **Yes - stack absent, offered an issue** |
| `CLAUDE.md` | **None** | **110 lines** |
| `README.md` | **144 lines** | None |
| Tests | **33, broader** | 19, tighter and justified |
| Quality gate reported | Implicit in prose | **Explicit: commands + results** |
| Architectural finding | Locale conflict, in prose | Carrier phrase, **`file:line` + cost** |
| Growth signals | Not assessed | **Assessed, reported as none crossed** |
| Declared what it had not measured | No | **Yes - latency, no key available** |
| Status block | No | **Yes, with a next suggestion** |
| Found the `maxRetries: 0` timeout trap | **Yes** | **Yes** |
| Handled a degraded turn correctly | **Yes** | **Yes** |
| Found a real platform-level problem | **Yes** - locale | **Yes** - carrier phrase |

The honest summary: **not "it produces better code" - run A's code is at least as good and
its test suite is broader. The difference is that more of the decision surface is visible
before it is baked in, the tool states the boundary of its own knowledge, and the project
keeps a memory of what was decided.**

The single most concrete artifact difference is `CLAUDE.md`. Run A's next session starts
cold - it will re-derive the build commands, the layer boundaries, and the three judgment
calls it already made. Run B's next session reads them.

## Run C - dev-mentor after the operability work

Same prompt, same directory pattern, Claude Code 2.1.251, stage answered `prototype`.
29 tests in 4 files, 498 lines. Typecheck and build clean.

**Two category rules fired visibly, and both were written from run A's wins.**

`"Untrusted text reaching an output format is escaped, and the escaping has its own test"`
produced a dedicated `test/ssml.test.ts` with six tests, including double-escaping of
ampersands and neutralising SSML the model itself put in its reply. Run A had one such
test; run B had none.

`"Every stated failure policy has a test: the timeout path, the retry exhaustion path, the
degraded path"` produced eight tests on the correction client alone - clamping the attempt
timeout to the remaining budget, refusing to retry when the budget cannot pay for another
attempt, and giving up without calling the API when the deadline has already passed.

The stage answer also did its job: observability, durable persistence, authorization and
cross-session history were all deferred with the stage that makes them due, rather than
demanded at a prototype.

### What run A still covers that run C does not

| Area | A | C |
|---|---|---|
| Persistent store not clobbering neighbours | tested | store deferred |
| Reading a record written by an earlier version | tested | store deferred |
| Speech content variety (correction cap, session close summary) | 7 speech tests | 6, all on escaping |

The first two are not misses. Run C deferred durable persistence and wrote the deferral
down; run A built it and tested it. **Which is better depends on the stage, and run C was
told prototype.** The comparison to draw is not "C tested less" but "C took on less scope
and said so".

### Where run C is still behind run A: product surface

The test comparison above looks only at test coverage. Comparing what the two programs
actually *do* tells a different story, and it is less flattering.

| | A | C |
|---|---|---|
| Alexa cards (visual companion) | 3 files use them | **none** |
| Spoken corrections capped per turn | `errors.slice(0, 2)`, rest to the card | **no cap** |
| `AMAZON.HelpIntent` | implemented | **absent** |
| A "how am I doing" intent | `MyProgressIntent` | absent |
| Durable persistence | built and tested | deferred, recorded |

Two of these are defects, not restraint:

**No correction cap.** A learner who made five mistakes in one turn gets all five read
aloud before the conversation continues. For a language tutor that is not a rough edge -
it is the product failing at its job. Run A capped spoken corrections at two and pushed
the rest to the Alexa card. Run C has no cap and no card, so it has nowhere to push them.

**No Help intent.** Help, Cancel and Stop are the standard built-in intents an Alexa skill
is expected to handle. Run C has Cancel and Stop and no Help.

The rest is arguably scope run A added beyond the prompt, and run C's own doctrine -
surgical changes, no speculative generality - would defend leaving it out.

### The meta-finding: the tool optimises for what it can check

Run C spent its budget on eight failure-policy tests, six escaping tests, a 127-line
`CLAUDE.md`, gates, deferrals and landmines. Run A spent its budget on cards, a correction
cap, a progress intent and a session summary.

**Every gate, rule and threshold in this project is checkable. Nothing in it asks whether
the thing is any good to use.** Gate 5 covers whether the project runs from a clean clone;
nothing covers whether the feature is usable by the person it was built for.

That is a structural bias, not a bug in one run: a tool made of checkable rules will pull
effort toward the checkable. Recorded here rather than fixed reflexively - adding a tenth
gate for "is it good" would be a checklist item standing in for judgment, which is the
failure this project keeps warning about.

### A finding against dev-mentor itself

`src/domain/progress.ts` in run C carries this comment:

> *"Integer comparison on purpose: `count / total >= 0.30` is a float compare, and the
> boundary case (3 of 10) is exactly where this rule is supposed to be exact."*

Run A used `REINFORCE_THRESHOLD = 0.3` and a float compare. Testing both forms over every
`count/total` pair up to total 2000 - roughly two million comparisons - produced **zero
discrepancies**. Integer arithmetic is better practice and self-documenting, but the
justification as written claims a defect that does not exist at any realistic input.

This is the failure mode the Research-to-Action Gate exists to prevent, appearing in the
output of the tool that enforces it. Plausible reasoning stated with more confidence than
the evidence supports. Recorded here rather than quietly dropped.

## Predictions that failed

Recorded because a project whose premise is evidence over opinion has to publish the
misses.

**"Without the skill it picks the stack silently."** False. Run A asked
*"¿Sobre qué stack construyo el turno?"* before writing a single file. The prediction was
made from a final screenshot, before the full transcript was available. The strongest
expected differentiator does not exist against a 57-skill baseline.

**"The baseline will not run its tests."** False. Run A ran the suite and reported 33
passing, unprompted.

**"The baseline will not surface architectural findings."** False. Run A found the locale
problem on its own. Run B found a different one, the `AMAZON.SearchQuery` carrier phrase.
Both real, both platform-level.

**"The skill will write better tests."** False. Run A's suite is broader on real failure
modes - SSML escaping, persistent-attribute isolation, record migration. Run B tests none
of those.

## Claims we can and cannot make

**Supported by the evidence:**

- dev-mentor states its assumptions before the work rather than after.
- dev-mentor consults a live external catalog, and says so, with a date.
- dev-mentor reports when a stack is absent from that catalog instead of staying quiet.
- dev-mentor surfaced one decision (persistence) that the baseline made alone.
- dev-mentor produced a `CLAUDE.md`; the baseline produced none. Run B's next session
  starts warm; run A's starts cold.
- dev-mentor reported its quality gate explicitly, as commands and results.
- dev-mentor structured its finding with `file:line` evidence and a stated cost, and
  reported growth signals as a negative result rather than inventing one.
- dev-mentor declared what it had not measured.

**Not supported - do not claim:**

- "Produces better code." The baseline's output is strong.
- "Without it, the agent decides for you." The baseline asked.
- "Without it, tests do not get run." The baseline ran them.
- "It writes better tests." True of run C only in the two areas that were written down as
  rules, and only against run B. Run A remains broader where it took on more scope.
- "Its reasoning is always evidence-backed." Run C produced a confident justification for
  integer arithmetic that two million test comparisons do not support.
- "It produces a more complete product." Run C shipped no Alexa card, no cap on spoken
  corrections and no Help intent. Run A had all three.

## Control caveats

Publish these alongside any result.

- **57 personal skills were active in both runs.** This is a marginal-value comparison, not
  a comparison against a bare Claude. A reader without those skills may see different
  behavior on both sides.
- **Claude Code version.** Run A ran on 2.1.243. Confirm run B's version; a mismatch is a
  minor uncontrolled variable worth naming.
- **The answers were matched by hand across runs.** Run B was answered to mirror run A:
  3 dialogues, TypeScript + ask-sdk-core, and a `ProgressStore` interface with an
  in-memory implementation for tests plus the Alexa persistent-attributes adapter
  (DynamoDB) for Lambda - which is what run A built. Without matching them, the two runs
  would diverge for reasons unrelated to the skill.
- **The agreed rule diverged from the prompt's original intent.** The prompt said "3
  turnos"; truncation removed it, and run A was answered "3 diálogos". Run B was answered
  the same way for comparability. Consistent across both runs, so the comparison holds.
- **The prompt carried a truncated rule** in both runs. Identical on both sides, so the
  comparison holds - but it means both runs were also being tested on how they handle a
  malformed requirement, which was not the original intent.
- **The plugin reported a partial load failure.** `/plugin install` printed
  *"Installed dev-mentor. The plugin couldn't be loaded - see /plugin for details."* The
  skill itself loaded and ran, but the `PostToolUse` hook did not fire automatically - the
  transcript shows `validate_claude_md.py` being invoked by hand instead. The 150-line cap
  was therefore **not** enforced by the hook during this run. Cause not yet diagnosed.
- **Neither product was evaluated.** This compares how the work was done and what it left
  behind - questions asked, assumptions declared, artifacts produced, tests written. It
  does **not** compare the delivered product: neither skill was ever run, no human read
  both codebases side by side for naming, cohesion or readability, and nobody asked which
  one they would rather maintain in six months. Every claim here is about process and
  artifacts. A claim about product quality would need a different experiment.
- **One run per side.** Model output varies between runs. A single pair is an anecdote,
  not a measurement. Three runs per side would be needed before publishing a rate.
