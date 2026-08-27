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

## How to run one

There is no automated harness yet — this is deliberate. Run the scenario by hand in a
throwaway directory with the plugin installed, then check each `expected_behavior` item.
Record the result in the issue for that scenario.

Contributions that add a harness are welcome; see [CONTRIBUTING.md](../CONTRIBUTING.md).
