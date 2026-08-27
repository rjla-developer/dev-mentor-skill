---
name: mentor-review
description: Runs a deep, teaching-mode architectural audit of a codebase and explains each finding with evidence, reasoning and cost. Use when the user asks for a code review, an architecture review, a health check, a second opinion, "what is wrong with this project", "how would you improve this", "what am I missing", "review my code", "is this well structured", or asks to be taught why something in their codebase is a problem. Use it for the deliberate deep pass; the reactive checks inside the normal dev-mentor flow stay shallow on purpose.
---

# Mentor Review

Deep audit, invoked explicitly. This is the teaching mode: it explains concepts the user
may not know yet and proposes structural change with the reasoning attached.

Load these first, and follow them:

- `../dev-mentor/references/behavioral-rules.md` - the Research-to-Action Gate applies to
  every finding here.
- `../dev-mentor/references/growth-signals.md` - the thresholds.
- `../dev-mentor/references/quality-gate.md` - the test doctrine.
- `../dev-mentor/references/mentoring-voice.md` - the shape of a recommendation.

## Scope contract

Before reading code, agree on scope. An unbounded review of a large repository produces a
document nobody reads.

State: which directories, which concerns (architecture / testing / dead code / coupling /
performance), and how deep. If the user says "everything", propose a scope of the 3-5
directories where the most recent work happened, and say why those.

## Passes

Run in this order. Later passes depend on what earlier ones found.

```
Review progress:
- [ ] Pass 1 - Map: entry points, module graph, feature boundaries
- [ ] Pass 2 - Stack and registry: what official skills cover, what they leave open
- [ ] Pass 3 - Growth signals with evidence
- [ ] Pass 4 - Test health
- [ ] Pass 5 - Dead code smell (hand off, do not delete)
- [ ] Pass 6 - Rank and report
```

### Pass 1 - Map

Entry points, dependency direction, how features are separated. Say what the architecture
*is* before saying what is wrong with it. If you cannot describe the intended structure in
three sentences, that is itself the first finding.

### Pass 2 - Stack and registry

Resolve the stack registry (see `../dev-mentor/references/orchestration.md`). Two
questions: which official skills should this project have installed, and what does the
`gap_map` say is uncovered? Uncovered areas are where defects concentrate, so look there
first.

### Pass 3 - Growth signals

Walk every signal in `growth-signals.md` against the stack's `growth_thresholds`. Collect
evidence as you go: `file:line`, counts, measurements. A signal without evidence is
discarded here, not softened into a suggestion.

### Pass 4 - Test health

Not coverage percentage. Ask:

- Which critical paths have no behavioral test?
- Which tests are non-deterministic, and how often do they get retried?
- Which tests assert implementation details and will break on the next refactor?
- Is the suite fast enough that people actually run it? If not, which layer is the cost?
- Does the suite currently pass? Run it. Report the real result.

### Pass 5 - Dead code smell

Note candidates. **Do not delete anything.** Check them against the stack's
`dead_code_risks` first, then hand off: "`/mentor-clean` builds a validated plan for this."

### Pass 6 - Rank and report

Rank by cost of leaving it alone, not by how easy it is to fix.

Report at most **5 findings**, each in the five-field structure from `mentoring-voice.md`
(WHAT I SEE / WHY IT MATTERS / WHAT I PROPOSE / WHY THIS WAY / THE COST). Below the five,
list remaining findings as one-line headlines under "Also noticed" - the user can ask for
detail on any of them.

Then a **sequencing note**: which finding to fix first and what it unblocks. A ranked list
with no order of operations leaves the user to guess, and they will start with the easiest
one.

## Teaching mode

This is the mode where explanation is the product.

- When a finding rests on a concept the user has not shown familiarity with, explain the
  concept in two or three sentences before the finding. Do not link to a blog post and
  call it teaching.
- Show the alternative that was not chosen and why it loses. A recommendation with no
  rejected alternative looks arbitrary.
- Separate what is objectively broken from what is a matter of taste, and label which is
  which. Most architecture arguments are taste presented as fact; do not add to that.

## Boundaries

- **Read and report. Do not refactor.** The user asked for a review. Changing code during
  a review destroys the reviewer's independence and the user's ability to say no.
- Do not fabricate a finding to fill a report. "This codebase is in reasonable shape, and
  here are the two things I would watch" is a complete and useful answer.
- Do not review generated code, vendored dependencies, or migrations as if a human wrote
  them.

End with the standard three-line status block.
