# Changelog

## 0.2.0

Everything here came out of two controlled comparisons against a baseline of 57 personal
skills. Where a change was caused by an observed failure, the failure is named.

### Added

- **`architecture`, `testing.rules` and `key_decisions` for all eight stacks**, verified
  against each framework team's own documentation. The registry previously said what
  skills exist; it now says how the code should be structured, which layer a test belongs
  in, and which decisions the stack forces with no default.
- **`guided` mode, now the default.** The standards are applied rather than discussed:
  decisions resolve from the registry, filtered by project stage, and are declared in a
  short footer afterwards. `technical` mode is opt-in and keeps the old behaviour.
- **Project stage** - spike, prototype, pre-release, production, maintenance. The same
  observation is a release blocker in production and noise on a spike.
- **The run-the-app rule.** A green suite is not evidence the screen is right. Anything
  with a UI must be launched and looked at, or the visual result declared unverified.
  Added after a comparison run shipped 68 passing tests, a clean analyzer and a compiling
  build - alongside an overlapping header no test would ever have caught.

### Fixed

- **The plugin failed to load.** `plugin.json` declared `hooks/hooks.json`, which Claude
  Code already loads by convention, producing "Duplicate hooks file detected". The skill
  still loaded, so nothing looked wrong while the `CLAUDE.md` line cap silently went
  unenforced. Found on the first real marketplace install; CI never installs the plugin.
- **Angular's architecture entry was wrong.** It described `core/shared/features`, which
  is community convention. The official style guide groups by feature and advises against
  directories named for types. Corrected, with the community layout kept as a variant.
- **The template had grown to 145 of the 150 lines it enforces.** Split into a 75-line
  core plus optional blocks, each carrying the condition that admits it.
- `sync_registry.py` reformatted the whole of `index.json` on every run, turning a
  one-line change into a 129-line diff. The weekly pull request exists to be read.

## 1.0.0 — the version that only claims what the evidence supports

Cut from nine capabilities to two. Five measured experiments are in
`docs/DEMO-COMPARISON.md`; they supported the architecture pillar and the testing pillar,
and did not support the rest.

### Removed

`mentor-review` and `mentor-clean` — never invoked once in five experiments. The seven
reference files, including growth signals, delivery gates, project stage and the mentoring
voice. The `guided`/`technical` modes. The three-line status block. The `CLAUDE.md` line-cap
hook and the `AGENTS.md` flattener.

**Why, in one sentence: ten doctrines dilute the one that matters.** The rule "ask when a
decision is expensive to reverse and only the user can answer it" was written, correct, and
buried among nine others — and a run walked straight past it, deciding on its own that a
feature belonged on a different platform entirely. The rule is now third from the top of a
112-line file, with nothing competing.

### Kept

The registry, unchanged: eight stacks with architecture verified against each framework
team's own documentation, stack-specific test rules and traps, and the decisions each stack
forces. This is the asset — it cost research, not code.

The `CLAUDE.md` generation, as the mechanism that makes the architecture rules persist in
the project after the skill is gone.

### Added

**One question before building.** If it is not obvious which platform, project or layer a
request belongs to, ask — once. Written from the failure above.

**Presentation rules as a first-class test subject**, alongside business rules, with the
requirement to launch the app and look at the screen, and the fallbacks for when that is
not possible: real device widths in a throwaway test, another target, retry once before
believing a tooling error.

## Unreleased

### Changed

- **The doctrine no longer reloads when the project already carries it.** A generated
  `CLAUDE.md` is the same doctrine compiled for that codebase at an eighth of the size, so
  runs after the first read it instead of the reference set. References also stopped
  pre-loading - each one loads when its step is reached - and the registry is filtered to
  the fields in use rather than printed whole. Measured: ~26k tokens per run down to ~12k
  on a new project and ~7k on one with a `CLAUDE.md`.
- **The doctrine now has a size cap**, enforced in CI. This project capped the user's
  `CLAUDE.md` at 150 lines and exempted its own references from any limit, which is how
  one of them reached 11.9k bytes.

### Fixed

- **A run reported "no growth signal crossed a threshold" without counting.** Its own
  longest `build()` had grown from 91 to 103 lines against a stated threshold of 100. The
  instruction said "every signal requires evidence" and was read as permission to stay
  silent. `growth-signals.md` now requires producing the number - the nearest value against
  its threshold - or saying plainly that nothing was measured.

## 0.1.0

Initial release: stack-canon orchestrator, mentor-review, mentor-clean, an eight-stack
registry, the 150-line `CLAUDE.md` hook, and four eval scenarios.
