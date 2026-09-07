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

## 0.1.0

Initial release: dev-mentor orchestrator, mentor-review, mentor-clean, an eight-stack
registry, the 150-line `CLAUDE.md` hook, and four eval scenarios.
