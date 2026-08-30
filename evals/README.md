# Evaluations

These scenarios were written **before** the skill documentation, following Anthropic's
guidance to validate that a skill solves real problems rather than imagined ones.

Each scenario is a JSON file with:

| Field | Meaning |
|---|---|
| `id` | Stable identifier, referenced from CI and from issues |
| `title` | One line summary |
| `setup` | The starting state a reviewer must reproduce |
| `user_prompt` | Verbatim text the user types |
| `expected_behavior` | Observable behaviors, each one independently checkable |
| `failure_modes` | Behaviors that mean the skill regressed |
| `scored_by` | `human` (judgment call) or `script` (deterministic) |

## Scoring a run

[`scorecard.md`](scorecard.md) is a fixed 14-row checklist for judging one run in about
five minutes, plus the controls - checks every baseline passes, which are therefore not
evidence for the tool. It carries the recorded scores for the three runs so far.

Use it whenever you change the skill: the number is comparable across runs in a way that
one person's impression of a transcript is not.

## How to run one

There is no automated harness yet — this is deliberate. Run the scenario by hand in a
throwaway directory with the plugin installed, then check each `expected_behavior` item.
Record the result in the issue for that scenario.

Contributions that add a harness are welcome; see [CONTRIBUTING.md](../CONTRIBUTING.md).
