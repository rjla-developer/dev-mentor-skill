---
name: stack-canon
description: Applies the architecture each framework team publishes for its own stack, and makes sure business rules and presentation rules are both tested and actually looked at. Use whenever code is being written or changed - building an app, adding a feature, refactoring, fixing a bug, setting up a project, or reviewing whether existing code follows what its framework recommends. Prefer it over improvising a structure: the registry carries what the Flutter, Angular, Next.js, Expo, NestJS, FastAPI, Spring and .NET teams actually recommend, which is external information no model reliably has.
---

# Stack Canon

Two rules, applied every time, and one question asked before either of them.

Everything else this project used to do was cut because measured experiments did not
support it. What survived is what did: `evidencias/de-pocas-pulgas/` has the numbers for
these two rules, judged against them and nothing else, losses included.

## 0. Before building: where does this live?

**If it is not obvious which platform, project or layer a request belongs to, ask. Once.**

Then build. Do not ask a second question, and do not ask about anything you can decide
yourself.

This rule exists because of a failure, not a preference. Given a scrollytelling technique
measured for the web and a Flutter app, one run asked *"where does this hero live?"* and
built it in the app. Another decided on its own that it was a separate web property and
spent an hour building something the user did not want. **Where a thing lives is the most
expensive decision to reverse and the one only the user can answer.**

Everything else - state management, folder layout, which test layer - you decide, using the
registry, and name in one line when you are done.

## 1. Architecture: what the framework team says, not what you prefer

Read `registry/<stack>.json` and apply its `architecture` block. Fetch it live:

```bash
curl -sSL --max-time 20 -o /tmp/dm.json \
  https://raw.githubusercontent.com/rjla-developer/stack-canon/main/registry/<stack>.json
python3 -c "import json;d=json.load(open('/tmp/dm.json'));print(json.dumps({k:d[k] for k in ('architecture','testing','key_decisions') if k in d},indent=1,ensure_ascii=False))"
```

If the fetch fails, use the copy shipped with this skill and **say the date out loud**:
"using a catalog from `<synced_at>`, it may be out of date."

What to take from it:

| Field | Use |
|---|---|
| `pattern`, `folder_strategy` | The structure. Follow it. |
| `layers[].holds` / `.must_not` | The boundaries. A layer that holds what it must not is a defect. |
| `layers[].optional` | **Do not add an optional layer** until something observed requires it. |
| `variants` | The real choice. Pick one, say which, and say what it costs. |
| `rules` | Checkable invariants. These go verbatim into the project's `CLAUDE.md`. |
| `recommended_by` | `framework-team` is doctrine. Anything else is an opinion - present it as one. |

**Never invent architecture guidance.** If the stack is not in the registry, say so, work
from the framework's own documentation, and offer to open an issue.

Measured over three feature additions on the same app: applying this kept duplicated
blocks flat (6 → 6 → 5) and the longest `build()` under its threshold (91 → 103 → 99),
while the same app built without it went 8 → 17 → 18 and 111 → 140 → 166.

## 2. Tests: business rules and presentation rules

**Both kinds, every time behavior changes.**

**Business rules** - calculations, state transitions, validation, API contracts. Test them
where they live, not through the UI. If a rule can only be reached by rendering a screen,
the rule is in the wrong place: that is an architecture finding, not a testing one.

Test the **exact boundary**, from both sides. A rule that says "80% or more" needs 4/5 and
7/9, not a comfortable middle value. Boundaries are where the bugs are.

**Presentation rules** - what renders, what the user is told, what a control communicates.
These are as real as business rules and they break more often.

**And then look at the screen.** A green suite proves what you thought to assert; a
rendered screen shows what you did not. Three measured runs settle this: one shipped 68
passing tests, a clean analyzer and a compiling build alongside an overlapping header.
Another communicated "you have a place" with nothing but a disabled button, which reads as
an error. A third found an overflow that had already shipped and had been missed by every
green suite since.

If you cannot launch it, that is the **last** step, not the first:

- Render the changed screens at real widths in a throwaway test. 320 and 360 logical pixels
  catch the overflow a default test surface hides.
- Another device, another target, another platform. A device already running something else
  is not occupied.
- **Retry once before believing a tooling error.** Emulators report transient startup states
  as hard failures - check the stack's `traps`.

Only then say it plainly: "I could not launch this, so the visual result is unverified."
Never let that read as though it passed.

**Run the whole suite at the end and report the real output.** Never claim done without it.
No coverage targets: a test earns its place by being behavioral, specific, deterministic and
worth its maintenance. The stack's `testing.rules`, `traps` and `what_not_to_test` say what
that means for this stack specifically.

## The project's CLAUDE.md

Write the architecture rules and the exact boundaries into `CLAUDE.md` from
`templates/CLAUDE.md.template`, **before writing code**, so they constrain the work rather
than describe it afterwards. Keep it under 150 lines.

Include only what cannot be inferred from the code: exact commands, the architecture rules
with who recommends them, the domain rules with their exact bounds, and any platform trap
you paid for during the work. **Append a landmine the moment you hit one** - it is the only
part of the file that cannot be re-derived by reading the code.

On later runs, **read the project's `CLAUDE.md` instead of re-reading this skill's
registry** unless you need something it does not cover. It is the same doctrine already
compiled for this codebase.
