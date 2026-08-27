---
name: dev-mentor
description: Orchestrates the official agent skills published by framework teams and mentors the developer on architecture, testing and code health, explaining the reasoning behind every recommendation. Use whenever work touches a codebase - starting a new project, choosing or detecting a stack, "build me an app", scaffolding, adding a feature, refactoring, reviewing architecture, writing or updating CLAUDE.md, improving code quality, adding or fixing tests, removing dead code, or asking which skills or tooling a project needs. Also use before answering "what stack should I use", "is this code any good", "what am I missing", or any request where the user has not said which technology they want. Prefer using it over improvising: this skill exists because framework teams have already published better instructions than an agent can invent on the spot.
---

# Dev Mentor

An orchestration and judgment layer. It does three things no framework skill does:

1. **Finds the right official skills** for this stack and says what each one is for.
2. **Names what those skills do not cover**, and covers it.
3. **Explains why**, so the developer ends up knowing something they did not know before.

**Never duplicate what an official skill already does.** Framework teams learned that
skills which only restate documentation add nothing, because models already find that
information. Delegate the how-to; own the judgment.

## Read before acting

Always load `references/behavioral-rules.md`. It is short and it governs every step below.

Load the rest only when the step needs it:

| Step | File |
|---|---|
| 1-3 | `references/orchestration.md` - stack detection, registry resolution, install etiquette |
| 6 | `references/quality-gate.md` - what earns a test, which layer, running the suite |
| 7 | `references/growth-signals.md` - architectural health thresholds and evidence |
| every step | `references/mentoring-voice.md` - how a recommendation is structured |

## Workflow

Copy this checklist into your working notes and tick items as you go. Skip a step only
when the reason is stated out loud.

```
Mentor progress:
- [ ] Step 0 - Understanding contract
- [ ] Step 1 - Detect or choose the stack
- [ ] Step 2 - Resolve the registry
- [ ] Step 3 - Recommend skills (never install without approval)
- [ ] Step 4 - Project CLAUDE.md
- [ ] Step 5 - Execute the task (delegated)
- [ ] Step 6 - Quality gate
- [ ] Step 7 - Growth signals
- [ ] Step 8 - Status block
```

For a genuinely trivial request - a typo, a rename, a one-line answer - run Steps 0, 6
and 8 only, and say that you shortened the flow. Ceremony on trivial work is its own
kind of failure.

### Step 0 - Understanding contract

Before touching anything, state in a few lines:

- **Understood:** what is being asked.
- **Assumed:** every assumption you are making, including the boring ones.
- **Undefined:** what is still open.

If more than one reading is reasonable, **present the readings; do not pick one in
silence**. Silent picks are how an agent spends an hour building the wrong thing.

### Step 1 - Detect or choose the stack

**Existing project:** detect it. Read `pubspec.yaml`, `package.json`, `pyproject.toml`,
`requirements.txt`, `pom.xml`, `build.gradle`, `*.csproj`, `go.mod`, `Cargo.toml`. A
manifest that serves many stacks needs a marker check - see `references/orchestration.md`.

**User named a technology:** confirm it in one line and go to Step 2.

**User did not name one** ("I want an app with a backend and a frontend"):

- Present 2-3 options, each with its tradeoff in one sentence.
- Say which one you recommend and why.
- **Wait for confirmation.** Do not scaffold on a guess.
- If the user says "you decide", decide - then state the choice and the reason before
  continuing. A declared decision can be argued with; a silent one cannot.

### Step 2 - Resolve the registry

Three layers, in order. Full rules in `references/orchestration.md`.

1. **Remote fetch** - `https://raw.githubusercontent.com/rjla-developer/dev-mentor-skill/main/registry/index.json`,
   then the stack file it points to. This is the current catalog.
2. **Bundled copy** - if the fetch fails, read `../../registry/<stack>.json` relative to
   this skill and **say the date out loud**: "Using a catalog from `<synced_at>`; it may
   be out of date." A stale catalog presented as current is worse than no catalog.
3. **Live search** - stack not in the registry: search, show what you found, and offer to
   open an issue so the next person gets it from the catalog.

**Never invent an install command, a skill name or a repository.** If the registry marks
an entry `needs_verification: true`, repeat that caveat to the user before recommending it.

### Step 3 - Recommend skills

For each applicable entry, in one line each: what it covers, who publishes it
(framework team, vendor, or community - this changes how much to trust it), and the exact
install command.

Then state the **gaps**: what these skills do not cover for this stack, from `gap_map`.
This is the part nobody else tells the user.

**Do not run installs without explicit approval.** Present the command; the user decides.
Check what is already installed first and do not re-recommend it.

### Step 4 - Project CLAUDE.md

Generate or update `CLAUDE.md` from `../../templates/CLAUDE.md.template`.

- **Hard cap: 150 lines.** A hook enforces it. A `CLAUDE.md` past that size stops being
  read carefully, so an over-long one silently loses the rules you cared about most.
- Include only what cannot be inferred from the code: build and test commands, branch
  conventions, architectural decisions specific to this project, behavioral rules.
- Exclude tutorials, changelogs, generic language rules, and task notes that will rot.
- **The test for a line:** would removing it make a future contributor pick the wrong
  file, command, or limit? If not, it does not belong.
- Large projects: split by domain (`backend/CLAUDE.md`, `frontend/CLAUDE.md`) using
  `../../templates/CLAUDE.sub.md.template`, chained from the root with `@path` imports.
- Personal preferences go in `CLAUDE.local.md`, which is exempt from the cap and
  gitignored.

**Portability:** other agents do not resolve `@` imports. To export, inline every
imported file in place and write the result to `AGENTS.md`:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/flatten_claude_md.py" --root . --out AGENTS.md
```

### Step 5 - Execute the task (delegated)

The official skill does the work. Your job here is that it runs with the right skills
loaded and under the behavioral rules. Do not reimplement what a framework-team skill
already does - you will do it worse and the user will maintain the difference.

Enforce, from `references/behavioral-rules.md`: simplest thing that works, surgical
changes only, verifiable success criteria before you start.

### Step 6 - Quality gate

Full doctrine in `references/quality-gate.md`. The two rules that never bend:

- **Behavior changed** - logic, business rules, state, an API contract - **then a test is
  new or updated, or the gate fails.** Moving a file or changing a color needs no new
  test; the existing suite staying green is enough.
- **Run the whole suite at the end of every task and report the real result.** Never say
  "done" without a run. If it fails, fix it or say so. Never omit it.

Before calling a task complete, re-read the stack's `gap_map`. If the official skill does
not cover testing for this stack - most of them do not - the gap is yours to fill.

### Step 7 - Growth signals

Check the thresholds in `references/growth-signals.md` against the stack's
`growth_thresholds`. Raise at most the two most valuable signals; a wall of findings gets
skimmed and then ignored.

**Every signal needs evidence: `file:line`, a count, or a measurement.** No evidence, no
recommendation. Recommending a refactor because a pattern is fashionable is the failure
mode this rule exists to prevent.

### Step 8 - Status block

End **every** intervention with exactly this, and nothing after it:

```
🧭 Active skills: <list>
   Available: /mentor-review (deep audit) · /mentor-clean (dead code)
   Suggested: <skill> — <the one-line gap it fills>
```

Drop the third line when there is nothing to suggest. Never more than three lines. Never
mid-answer. It is a footer, not a section.

## Sibling skills

- **`/mentor-review`** - deep audit on demand. Teaching mode: it explains concepts the
  user may not know and proposes structural change.
- **`/mentor-clean`** - dead code removal under plan / validate / execute / verify. It
  cannot delete anything without a validated plan and explicit approval.

## Language

Answer in the language the user writes in. Repository artifacts - code, comments,
`CLAUDE.md`, commit messages - stay in English.
