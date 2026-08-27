# Growth signals

Thresholds that say when a codebase has outgrown its current shape. Each one has a
detection method, a proposal, and a way to explain it.

## Contents

- [The golden rule](#the-golden-rule)
- [Signal table](#signal-table)
- [1. Component duplication](#1-component-duplication)
- [2. Oversized feature](#2-oversized-feature)
- [3. High coupling](#3-high-coupling)
- [4. Dependency cycles](#4-dependency-cycles)
- [5. Dead code](#5-dead-code)
- [6. Over-abstraction](#6-over-abstraction)
- [7. Effect cascades](#7-effect-cascades)
- [8. Test gap on a critical path](#8-test-gap-on-a-critical-path)
- [Where these numbers come from](#where-these-numbers-come-from)

## The golden rule

**Every signal requires evidence: `file:line`, a count, or a measurement.** Without
evidence the mentor says nothing. A threshold crossed on a hunch is not a finding.

Raise at most two signals per intervention, ranked by cost of leaving them alone. A list
of eight findings gets skimmed once and then ignored forever.

Stack-specific thresholds in `registry/<stack>.json` under `growth_thresholds` **override**
the generic ones here.

## Signal table

| Signal | Threshold | Proposal |
|---|---|---|
| Component duplication | >=3 occurrences across >=2 features | Extract a shared component |
| Oversized feature | >15 files in one feature folder | Split into sub-features or extract a module |
| High coupling | One module imported by >5 unrelated modules | Review the boundary; possibly extract a package |
| Dependency cycle | Any cycle | Break it with dependency inversion |
| Dead code | A symbol with no inbound references | Hand off to `/mentor-clean` |
| Over-abstraction | An abstraction with one implementation and no second planned | Inline it |
| Effect cascade | A side-effect chain more than 2 levels deep | Flatten toward self-contained components |
| Test gap | A critical path with no behavioral coverage | One risk-targeted test |

## 1. Component duplication

**Detect:** search for structurally similar components across feature folders. Compare
shape, not names - the copies usually get renamed.

**Propose:** extract to a shared component library. Under the threshold, extracting is the
speculative abstraction that the simplicity rule forbids: two similar things are a
coincidence, three are a pattern.

**Explain:** point at the maintenance event that already happened - the change that
updated three copies and missed the fourth. If no such event has happened yet, the cost is
hypothetical, and you should say so.

## 2. Oversized feature

**Detect:** count files per feature folder.

**Propose:** split by sub-domain, or extract the shared part into a module. Do not split by
technical layer (`models/`, `services/`, `widgets/`) if the project is organized by
feature - mixing the two is how a codebase ends up with both and a clear rule for neither.

**Explain:** 15 files is roughly where a person stops being able to hold the folder in
their head and starts using search instead. The cost is orientation time on every visit.

## 3. High coupling

**Detect:** count inbound imports per module. Look for modules imported by parts of the
system with no domain relationship to them.

**Propose:** examine the boundary. Often the module is doing two things and only one of
them is widely needed - split it. Extraction to a package is the right move when the
consumers are genuinely unrelated and the module is genuinely stable.

**Explain:** a module with many unrelated consumers cannot change. Its blast radius is the
whole system, so in practice nobody touches it and workarounds accumulate around it.

## 4. Dependency cycles

**Detect:** language tooling where it exists (`dart analyze`, `madge`, `import-linter`,
`NDepend`). Otherwise trace imports by hand from the suspect module.

**Propose:** invert the dependency. The shared type or interface moves to a third module
that both sides depend on.

**Explain:** cycles break incremental builds, defeat tree shaking, and make the initialization
order load-order dependent - which produces bugs that only appear in release builds.

**Threshold: any cycle.** This is the one signal with no tolerance, because cycles do not
get better on their own and each new one is cheaper to add than the last.

## 5. Dead code

**Detect:** symbols with no inbound references. Every stack has patterns that look dead
and are not - see `dead_code_risks` in the stack's registry entry.

**Propose:** hand off to `/mentor-clean`. Do not delete inline, ever, no matter how obvious
it looks.

**Explain:** dead code is read by every person who greps the file, and is maintained by
anyone who refactors around it. It costs attention, which is the scarcest resource on a
team.

## 6. Over-abstraction

**Detect:** interfaces, base classes, factories or strategy objects with exactly one
implementation and no concrete plan for a second. Configuration options nobody sets.

**Propose:** inline it. Add the abstraction back when the second implementation actually
arrives - that is when you will know what shape it should have.

**Explain:** an abstraction designed for one case is a guess about the second one, and
guesses are usually wrong. Removing it later is harder than adding it later, because by
then code depends on the interface rather than on the thing.

## 7. Effect cascades

**Detect:** trace side-effect chains - an effect that sets state that triggers another
effect that sets state. Count the levels.

**Propose:** flatten toward self-contained components. Derive values instead of syncing
them. Make the flow explicit at the call site.

**Explain:** cascades hide causality behind time. A human reads the code and cannot say
what runs next; an AI agent reading the same code does no better, and both make changes
that fire effects nobody predicted. This threshold is deliberately low, at 2 levels,
because the debugging cost grows faster than the nesting.

## 8. Test gap on a critical path

**Detect:** identify paths where a failure means data loss, a security hole, money moving
wrongly, or an unusable product. Check what covers each one.

**Propose:** one targeted test for the specific risk. Not a coverage campaign.

**Explain:** risk-directed, not percentage-directed. See `quality-gate.md`.

## Where these numbers come from

They are calibration, not law. Each one is set where the cost of the problem starts to
exceed the cost of the fix:

- **3 occurrences / 2 features** - the classic rule-of-three, chosen so that two similar
  things stay a coincidence and the extraction is not speculative.
- **15 files** - roughly the limit of what fits on one screen and in one person's head.
- **5 unrelated consumers** - past this, changing the module needs coordination rather
  than a decision.
- **1 cycle** - cycles compound; there is no safe number.
- **2 effect levels** - the point where reasoning about order stops being reliable, for
  humans and agents alike.

**If a threshold is wrong for a stack, override it in that stack's registry entry. If it
is wrong everywhere, open a pull request with the reasoning** - miscalibrated thresholds
make the mentor noisy, and a noisy mentor gets muted.
