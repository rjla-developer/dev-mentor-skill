#!/usr/bin/env python3
"""Validate the skill against the authoring rules this repository commits to.

    python3 scripts/validate_skills.py

This skill is deliberately one file. There are no reference files, no second level, and
no budget to police - the constraint is simply that SKILL.md stays short enough to be
read whole, every run.

Exit codes:
    0  valid
    1  at least one violation (all are printed)
    2  the script could not run
"""

from __future__ import annotations

import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
SKILLS_DIR = os.path.join(REPO_ROOT, "skills")

# One page. The whole point of the 1.0 rewrite was that ten doctrines dilute the one that
# matters; a cap is how that stays true when the temptation to add a rule comes back.
MAX_SKILL_LINES = 150
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
RESERVED_WORDS = ("anthropic", "claude")
NAME_RE = re.compile(r"^[a-z0-9-]+$")

errors: list = []


def error(where: str, message: str) -> None:
    errors.append("{}: {}".format(where, message))


def check_skill(skill_dir: str) -> None:
    rel = os.path.relpath(skill_dir, REPO_ROOT)
    path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(path):
        error(rel, "has no SKILL.md.")
        return
    try:
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()
    except OSError as exc:
        error(rel, "cannot read SKILL.md: {}".format(exc))
        return

    where = "{}/SKILL.md".format(rel).replace(os.sep, "/")

    lines = text.splitlines()
    if len(lines) > MAX_SKILL_LINES:
        error(where, "{} lines, over the {} cap. This skill is one page on purpose: "
                     "every rule added competes for attention with the two that are "
                     "supported by evidence. Cut something, or do not add it."
              .format(len(lines), MAX_SKILL_LINES))

    if os.path.isdir(os.path.join(skill_dir, "references")):
        error(rel, "has a references/ directory. The 1.0 rewrite removed the reference "
                   "layer deliberately - a rule the model has to go and fetch is a rule "
                   "that competes with the ones already in front of it.")

    if not text.startswith("---\n"):
        error(where, "no YAML frontmatter; the skill will never load.")
        return
    end = text.find("\n---", 4)
    if end == -1:
        error(where, "frontmatter is not closed with ---.")
        return
    fields = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()

    name = fields.get("name", "")
    if not name:
        error(where, "frontmatter has no name.")
    else:
        if not NAME_RE.match(name):
            error(where, 'name "{}" must be lowercase letters, digits and hyphens.'
                  .format(name))
        if len(name) > MAX_NAME_LENGTH:
            error(where, "name is {} chars, over {}.".format(len(name), MAX_NAME_LENGTH))
        for word in RESERVED_WORDS:
            if word in name.lower():
                error(where, 'name contains the reserved word "{}".'.format(word))
        if name != os.path.basename(skill_dir):
            error(where, 'name "{}" does not match the directory "{}".'
                  .format(name, os.path.basename(skill_dir)))

    description = fields.get("description", "")
    if not description:
        error(where, "frontmatter has no description; the skill will never trigger.")
    else:
        if len(description) > MAX_DESCRIPTION_LENGTH:
            error(where, "description is {} chars, over {}."
                  .format(len(description), MAX_DESCRIPTION_LENGTH))
        first = description.split()[0].lower().rstrip(".,")
        if first in ("use", "you", "i", "this"):
            error(where, 'description starts with "{}"; it must be third person and say '
                         "what the skill does before when to use it.".format(first))
        if "use" not in description.lower():
            error(where, "description never says when to use the skill.")

    for line in lines:
        if re.search(r"[A-Za-z0-9_]\\[A-Za-z0-9_]", line):
            error(where, "path uses a backslash: {}".format(line.strip()[:70]))
            break


def main() -> int:
    if not os.path.isdir(SKILLS_DIR):
        print("FATAL: {} not found.".format(SKILLS_DIR), file=sys.stderr)
        return 2
    skill_dirs = [os.path.join(SKILLS_DIR, n) for n in sorted(os.listdir(SKILLS_DIR))
                  if os.path.isdir(os.path.join(SKILLS_DIR, n))]
    if not skill_dirs:
        print("FATAL: no skills found.", file=sys.stderr)
        return 2
    for skill_dir in skill_dirs:
        check_skill(skill_dir)

    print("validate_skills: checked {} skill(s)".format(len(skill_dirs)))
    for message in errors:
        print("  ERROR {}".format(message), file=sys.stderr)
    if errors:
        print("\n{} violation(s).".format(len(errors)), file=sys.stderr)
        return 1
    print("  valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
