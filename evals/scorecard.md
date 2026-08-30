# Run scorecard

A fixed checklist for judging one run, in about five minutes, without needing anyone's
opinion. Fill it in from the transcript and the resulting repository.

## What it measures, and what it does not

It measures **whether the skill's rules fired**. That is compliance, not quality.

A run can score 14/14 and still produce mediocre software, and a strong baseline can score
4/14 and produce good software - that happened, and it is recorded in
[`../docs/DEMO-COMPARISON.md`](../docs/DEMO-COMPARISON.md). Judging the software still
takes judgment.

What this replaces is worse than judgment: **one person reading a transcript and forming an
impression that is not comparable to the last one.** A fixed list is comparable across runs
and across people, and it moves when you change the skill.

## The discriminating rows

These are the checks that came out **differently** across recorded runs. A check that every
run passes measures nothing about the tool - those are listed further down as controls.

| # | Check | How to verify |
|---|---|---|
| 1 | Assumptions stated **before** any file was written | Scroll to the first response. Post-hoc "three things I decided" does not count |
| 2 | A skills catalog was consulted, and its sync date stated | Look for the fetch and a date in the text |
| 3 | It declared what it does **not** know | An explicit "not in the catalog" or "I have not measured this" |
| 4 | An ambiguous requirement was decomposed into enumerated readings | Options with costs, not an open "what did you mean?" |
| 5 | The project stage was established before the work | `spike` / `prototype` / `pre-release` / `production` / `maintenance` |
| 6 | A `CLAUDE.md` was written | The file exists |
| 7 | Deferrals recorded **with the stage that makes them due** | A `## Deferred` section, each item naming a stage |
| 8 | Landmines discovered during the work were written down | A `## Known landmines` section, non-empty |
| 9 | The quality gate reported real commands and real results | The command appears, and so does its output |
| 10 | Findings carry `file:line` evidence | At least one finding with a concrete location |
| 11 | Growth signals assessed, including a negative result | "Nothing crosses a threshold" counts as a pass; silence does not |
| 12 | Untrusted input reaching an output format is escaped, **with its own test** | A test file or test case for the escaping |
| 13 | Every stated failure policy has a test | Timeout path, retry exhaustion, degraded path |
| 14 | It stated what it had **not** verified or measured | An explicit limitation, not an omission |

**Score:** count of passes out of 14.

## Controls: checks that did not discriminate

Every recorded run passed these, with and without the plugin. **They are not evidence for
the tool.** They are here so nobody claims them as such.

| Check | Why it is a control |
|---|---|
| Asked something before writing code | A capable agent often asks anyway |
| Ran the full suite and reported real numbers | The baseline did this unprompted |
| Found a genuine platform-level problem | Both baselines found one, unaided |
| Found the retry-multiplies-your-timeout trap | Found by every run |

If a change to the skill turns one of these into a differentiator, move it up. If a
discriminating row starts passing on every baseline, move it down here. **The controls
list is what keeps the scorecard honest.**

## Recorded results

Filled from the transcripts in [`../docs/DEMO-COMPARISON.md`](../docs/DEMO-COMPARISON.md).
Baseline for all three: Claude Code with 57 personal skills already installed.

| # | Check | A (no plugin) | B (early plugin) | C (after operability work) |
|---|---|---|---|---|
| 1 | Assumptions before the work | no - post-hoc | yes | yes |
| 2 | Catalog consulted, date stated | no | yes | yes |
| 3 | Declared what it does not know | no | yes | yes |
| 4 | Ambiguity decomposed | no - open question | yes | yes |
| 5 | Project stage established | no | no | **yes** |
| 6 | `CLAUDE.md` written | no | yes | yes |
| 7 | Deferrals with due stage | no | no | **yes** |
| 8 | Landmines written down | no - found, not recorded | no | **yes** |
| 9 | Quality gate with real results | prose only | yes | yes |
| 10 | Findings carry `file:line` | no | yes | yes |
| 11 | Growth signals assessed | no | yes | yes |
| 12 | Untrusted input escaped, with test | partial - 1 test | **no** | **yes - 6 tests** |
| 13 | Failure policy fully tested | partial | partial | **yes - 8 tests** |
| 14 | Stated what it had not measured | no | yes | yes |
| | **Score** | **1.5 / 14** | **10 / 14** | **14 / 14** |

Row 12 is the one worth staring at. The baseline scored **higher than the early plugin**
there - that gap is what produced the category testing rules, and row 12 and 13 are where
run C's improvement came from. **The scorecard found the gap before the rules existed.**

## How to run it

1. Do the task with the plugin disabled. Save the transcript.
2. Do the same task, same prompt, with it enabled. Save that transcript.
3. Fill both columns.
4. Record the score and the environment in `DEMO-COMPARISON.md`.

**Report the controls alongside the score**, and say how many personal skills were active.
A score against a bare Claude means something different from a score against a 57-skill
setup, and quoting one as the other is the easiest way to lose the reader's trust.

One run per side is an anecdote. Three per side before quoting a rate.
