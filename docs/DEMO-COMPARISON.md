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

Directory: `english-mentor-with-skill`. Status: **in progress**.

Observed so far:

1. **Fetched the live remote registry.** `curl` to
   `raw.githubusercontent.com/rjla-developer/dev-mentor-skill/main/registry/index.json`,
   returning `synced_at: 2026-08-28`. First production exercise of the three-layer
   resolution described in `docs/REGISTRY.md`.
2. Opened with the understanding contract **before writing anything**, in the documented
   three-part shape:
   - **Entendido** - restated the task.
   - **Asumido** - four assumptions stated up front and marked as contestable: the model
     is Claude via API (Haiku 4.5 for latency); Alexa cuts at ~8s so the model budget is
     3-4s with a deterministic fallback; "Alexa does not understand" means fallback intent
     or empty transcript, not a model error; scenario and level live in the progress
     record while session state consolidates on close.
   - **Indefinido** - refused to guess the truncated rule, and said why: *"cambia el
     modelo de datos (contar diálogos consecutivos exige guardar racha)"*.
3. **Reported the gap in its own catalog, unprompted:** *"Las skills de Alexa no están en
   el catálogo - las entradas más cercanas son `nestjs` (Node) y `fastapi` (Python),
   ninguna cubre ASK SDK. Lo trabajo con doctrina propia y luego te ofrezco abrir un issue
   para que el stack entre al catálogo."*
4. Asked a structured question set covering **three** decisions: level-up rule, stack, and
   **persistence**. Run A decided persistence on its own.
5. **Decomposed the ambiguous requirement instead of asking openly.** Where run A asked
   *"¿Cuál es la condición exacta?"* and left the developer to reconstruct the rule, run B
   offered four concrete readings - 3 dialogues, 2 dialogues, 1 dialogue, **3 turns** -
   surfacing a turn-versus-dialogue distinction the developer had not noticed, and stating
   the data-model cost of each: *"Exige guardar racha en el registro (se rompe al primer
   error)"*. Both runs asked; only one taught why the question mattered.
5. Loaded the bundled `claude-api` skill, same as run A.

To be filled in when the run completes: tests, artifacts, `CLAUDE.md`, status block,
duration.

## Observed differences

Only differences with direct evidence in a transcript. Anything unverified stays out.

| Dimension | Run A | Run B |
|---|---|---|
| Asked before writing code | **Yes** - 2 questions | **Yes** - 3 questions |
| Stack chosen by | The developer | The developer |
| Assumptions stated | At the end, as 3 post-hoc decisions | **Up front**, as 4 contestable assumptions |
| Decisions surfaced | 2 (rule, stack) | 3 (rule, stack, **persistence**) |
| Shape of the ambiguous question | Open-ended | **4 enumerated readings, each with its data-model cost** |
| Consulted a skill catalog | No | **Yes - live remote fetch** |
| Declared what it does not know | No | **Yes - stack absent from catalog, offered an issue** |
| Official skills for this stack | Not mentioned | Named the nearest entries and said neither covers ASK SDK |
| `CLAUDE.md` | No | pending |
| Tests | 33 passing | pending |

The honest summary of the difference so far: **not "it decides better", but "more of the
decision surface is visible before it is baked in, and the tool states the boundary of its
own knowledge."**

## Predictions that failed

Recorded because a project whose premise is evidence over opinion has to publish the
misses.

**"Without the skill it picks the stack silently."** False. Run A asked
*"¿Sobre qué stack construyo el turno?"* before writing a single file. The prediction was
made from a final screenshot, before the full transcript was available. The strongest
expected differentiator does not exist against a 57-skill baseline.

**"The baseline will not run its tests."** False. Run A ran the suite and reported 33
passing, unprompted.

**"The baseline will not surface architectural findings."** False. Run A found the
locale problem - the one genuinely unsolvable-in-code issue in the whole task - on its
own.

## Claims we can and cannot make

**Supported by the evidence:**

- dev-mentor states its assumptions before the work rather than after.
- dev-mentor consults a live external catalog, and says so, with a date.
- dev-mentor reports when a stack is absent from that catalog instead of staying quiet.
- dev-mentor surfaced one decision (persistence) that the baseline made alone.

**Not supported - do not claim:**

- "Produces better code." The baseline's output is strong.
- "Without it, the agent decides for you." The baseline asked.
- "Without it, tests do not get run." The baseline ran them.

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
- **One run per side.** Model output varies between runs. A single pair is an anecdote,
  not a measurement. Three runs per side would be needed before publishing a rate.
