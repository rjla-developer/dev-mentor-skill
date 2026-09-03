# Optional CLAUDE.md sections

Blocks to add to a project's `CLAUDE.md` **only when the condition is met**. Do not paste
one in as scaffolding to be filled later — an unfilled section costs lines against the
150-line cap and teaches a reader nothing.

Adding a section is a decision. If you cannot say which condition triggered it, it does
not go in.

---

## Known landmines

**Add when:** a platform or library trap has actually been hit in this project.

The highest-value section in any `CLAUDE.md` — the only part that cannot be re-derived by
reading the code, because the code looks correct right up until the trap fires. Append the
moment one is found, during the task, not afterwards.

```markdown
## Known landmines

- {{LANDMINE}} — {{WHAT_IT_BREAKS}} — {{WHAT_TO_DO_INSTEAD}}
```

---

## Domain rules

**Add when:** the project has business rules with exact thresholds a reader could not
infer from the code.

```markdown
## Domain rules

These are the product rules. Change them only on request, and update {{TEST_FILE}} in the
same change.

- {{RULE_WITH_ITS_EXACT_BOUND}}
```

---

## Testing rules

**Add when:** the stack has `testing.rules` or `what_not_to_test` entries that changed how
this project is tested. One line in the quality gate is enough otherwise.

```markdown
## Testing rules

- {{TEST_RULE}}
- Not worth testing here: {{WHAT_NOT_TO_TEST}}
```

---

## Failure policy

**Add when:** the project calls anything it does not control — a network, a queue, a
model, a database.

```markdown
## Failure policy

- {{BOUNDARY}}: {{RETRY_DEGRADE_OR_FAIL_LOUDLY}} — because {{REASON}}
```

---

## Conventions

**Add when:** a convention here differs from what a contributor would assume.

```markdown
## Conventions

- Branches: {{BRANCH_CONVENTION}}
- Commits: {{COMMIT_CONVENTION}}
```

---

## Sub-projects

**Add when:** the repository is split by domain and the root file would otherwise exceed
the cap.

```markdown
@{{PATH_TO_SUB_CLAUDE_MD}}
```
