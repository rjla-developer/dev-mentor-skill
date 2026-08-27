#!/usr/bin/env python3
"""Validate every SKILL.md against the authoring rules this repository commits to.

    python3 scripts/validate_skills.py

Checks:
  * SKILL.md under 500 lines
  * frontmatter present, with name and description
  * name: lowercase, digits and hyphens, <=64 chars, no reserved words
  * description: <=1024 chars, third person (not starting with an imperative "Use"/"I")
  * every referenced local file exists
  * references are one level deep: a file under references/ must not point at another
  * reference files over 100 lines carry a table of contents
  * no backslash paths anywhere

Exit codes:
    0  all good
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

MAX_SKILL_LINES = 500          # progressive disclosure: SKILL.md is the entry point only
TOC_REQUIRED_ABOVE = 100       # a longer reference gets read partially without a map
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
RESERVED_WORDS = ("anthropic", "claude")

NAME_RE = re.compile(r"^[a-z0-9-]+$")
LOCAL_LINK_RE = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|py|json|template))`")

# Top-level directories this repository owns. A relative path starting with one of them
# is a link into the repo; anything else is an example of someone else's project layout.
OWNED_DIRS = {"skills", "references", "registry", "templates", "scripts", "hooks",
              "docs", "evals", ".github", ".claude-plugin"}

errors: list = []


def error(where: str, message: str) -> None:
    errors.append("{}: {}".format(where, message))


def parse_frontmatter(text: str, where: str):
    if not text.startswith("---\n"):
        error(where, "no YAML frontmatter. A skill without frontmatter never loads.")
        return None
    end = text.find("\n---", 4)
    if end == -1:
        error(where, "frontmatter is not closed with ---.")
        return None
    block = text[4:end]
    fields = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def check_skill(skill_dir: str) -> None:
    rel_dir = os.path.relpath(skill_dir, REPO_ROOT)
    skill_path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_path):
        error(rel_dir, "has no SKILL.md.")
        return

    try:
        with open(skill_path, "r", encoding="utf-8") as handle:
            text = handle.read()
    except OSError as exc:
        error(rel_dir, "cannot read SKILL.md: {}".format(exc))
        return

    where = os.path.join(rel_dir, "SKILL.md").replace(os.sep, "/")
    lines = text.splitlines()
    if len(lines) > MAX_SKILL_LINES:
        error(where, "{} lines; the cap is {}. Move detail into references/."
              .format(len(lines), MAX_SKILL_LINES))

    fields = parse_frontmatter(text, where)
    if fields is None:
        return

    name = fields.get("name", "")
    if not name:
        error(where, "frontmatter has no name.")
    else:
        if not NAME_RE.match(name):
            error(where, 'name "{}" must be lowercase letters, digits and hyphens only.'
                  .format(name))
        if len(name) > MAX_NAME_LENGTH:
            error(where, "name is {} chars; the cap is {}."
                  .format(len(name), MAX_NAME_LENGTH))
        for word in RESERVED_WORDS:
            if word in name.lower():
                error(where, 'name contains the reserved word "{}".'.format(word))
        expected = os.path.basename(skill_dir)
        if name != expected:
            error(where, 'name "{}" does not match the directory "{}".'
                  .format(name, expected))

    description = fields.get("description", "")
    if not description:
        error(where, "frontmatter has no description. Without one the skill never "
                     "triggers.")
    else:
        if len(description) > MAX_DESCRIPTION_LENGTH:
            error(where, "description is {} chars; the cap is {}."
                  .format(len(description), MAX_DESCRIPTION_LENGTH))
        first = description.split()[0].lower().rstrip(".,")
        if first in ("use", "you", "i", "this"):
            error(where, 'description starts with "{}"; it must be third person and '
                         "describe what the skill does before saying when to use it."
                  .format(first))
        if " use " not in description.lower() and "use when" not in description.lower():
            error(where, "description never says when to use the skill. Both halves - "
                         "what it does AND when to use it - are required.")

    check_links(skill_path, where, allow_references=True)

    ref_dir = os.path.join(skill_dir, "references")
    if os.path.isdir(ref_dir):
        for name in sorted(os.listdir(ref_dir)):
            if name.endswith(".md"):
                check_reference(os.path.join(ref_dir, name))


def check_reference(path: str) -> None:
    where = os.path.relpath(path, REPO_ROOT).replace(os.sep, "/")
    try:
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()
    except OSError as exc:
        error(where, "cannot read: {}".format(exc))
        return

    lines = text.splitlines()
    if len(lines) > TOC_REQUIRED_ABOVE and "## Contents" not in text:
        error(where, "{} lines with no '## Contents' table of contents. Files this long "
                     "get read partially; the map is what keeps that from losing "
                     "information.".format(len(lines)))

    # One level of depth: a reference must not send the reader to another reference.
    for match in LOCAL_LINK_RE.finditer(text):
        target = match.group(1)
        if target.endswith(".md") and "references/" in target:
            error(where, 'points at "{}". References are one level deep from SKILL.md; '
                         "chained references get read with head -n and lose content."
                  .format(target))
    check_links(path, where, allow_references=False)


def check_links(path: str, where: str, allow_references: bool) -> None:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()
    except OSError:
        return
    if "\\" in text.replace("\\n", "").replace('\\"', ""):
        # Only flag backslashes that look like path separators.
        for line in text.splitlines():
            if re.search(r"[A-Za-z0-9_]\\[A-Za-z0-9_]", line):
                error(where, "path uses a backslash: {}".format(line.strip()[:80]))
                break

    base = os.path.dirname(path)
    for match in LOCAL_LINK_RE.finditer(text):
        target = match.group(1)
        # Only path-like tokens are links. A bare filename in prose - package.json,
        # CLAUDE.md, conftest.py - names a concept, not a file in this repository, and
        # a first segment we do not own - backend/CLAUDE.md - describes a user's project.
        if "/" not in target or target.startswith("http") or "{{" in target or "$" in target:
            continue
        first_segment = target.split("/", 1)[0]
        if not (target.startswith(("./", "../")) or first_segment in OWNED_DIRS):
            continue
        resolved = os.path.normpath(os.path.join(base, target))
        if not os.path.exists(resolved):
            # Reference paths in prose may be repo-relative instead of file-relative.
            alt = os.path.normpath(os.path.join(REPO_ROOT, target))
            if not os.path.exists(alt):
                error(where, 'references "{}" which does not exist at {} or {}.'
                      .format(target, os.path.relpath(resolved, REPO_ROOT),
                              os.path.relpath(alt, REPO_ROOT)))


def main() -> int:
    if not os.path.isdir(SKILLS_DIR):
        print("FATAL: {} not found.".format(SKILLS_DIR), file=sys.stderr)
        return 2

    skill_dirs = [os.path.join(SKILLS_DIR, name) for name in sorted(os.listdir(SKILLS_DIR))
                  if os.path.isdir(os.path.join(SKILLS_DIR, name))]
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
    print("  all skills valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
