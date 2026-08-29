#!/usr/bin/env python3
"""Validate registry/*.json against registry/schema.json and against the invariants
that JSON Schema cannot express.

Run from anywhere:  python3 scripts/validate_registry.py

Exit codes:
    0  everything valid
    1  at least one validation error (all errors are printed, not just the first)
    2  the validator itself could not run (missing files, unreadable JSON)

jsonschema is optional. When it is installed the full schema is enforced; when it is
not, the structural subset below still runs, and the script says which mode it used.
CI installs jsonschema so the full check always runs there.
"""

from __future__ import annotations

import json
import os
import re
import sys

# Repository layout. The script must work from any working directory, so every path
# is derived from this file's own location rather than from os.getcwd().
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
REGISTRY_DIR = os.path.join(REPO_ROOT, "registry")

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
STACK_KEY_RE = re.compile(r"^[a-z0-9-]+$")
VALID_CATEGORIES = {"frontend", "backend", "fullstack", "mobile", "infra"}
VALID_OWNER_KINDS = {"framework-team", "vendor", "community"}

# Files that live in registry/ but are not stack entries.
NON_STACK_FILES = {"schema.json", "index.json"}

errors: list = []
warnings: list = []


def error(where: str, message: str) -> None:
    errors.append("{}: {}".format(where, message))


def warn(where: str, message: str) -> None:
    warnings.append("{}: {}".format(where, message))


def load_json(path: str):
    """Read a JSON file, reporting the failure instead of raising."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        print("FATAL: missing file {}".format(path), file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as exc:
        print("FATAL: {} is not valid JSON: {}".format(path, exc), file=sys.stderr)
        sys.exit(2)
    except OSError as exc:
        print("FATAL: cannot read {}: {}".format(path, exc), file=sys.stderr)
        sys.exit(2)


def check_stack_entry(name: str, data: dict) -> None:
    """Invariants beyond the schema, each with an actionable message."""
    expected_stack = name[: -len(".json")]
    if data.get("stack") != expected_stack:
        error(name, 'field "stack" is "{}" but the filename says "{}". '
                    "They must match so the mentor can resolve a stack to a file."
              .format(data.get("stack"), expected_stack))

    if not STACK_KEY_RE.match(str(data.get("stack", ""))):
        error(name, 'field "stack" must be lowercase letters, digits and hyphens only.')

    if data.get("category") not in VALID_CATEGORIES:
        error(name, 'field "category" is "{}"; allowed values are {}.'
              .format(data.get("category"), sorted(VALID_CATEGORIES)))

    last_verified = str(data.get("last_verified", ""))
    if not DATE_RE.match(last_verified):
        error(name, 'field "last_verified" must be YYYY-MM-DD, got "{}". '
                    "The mentor shows this date to the user, so a wrong format hides staleness."
              .format(last_verified))

    for key in ("detection", "testing", "growth_thresholds"):
        if not isinstance(data.get(key), dict):
            error(name, 'field "{}" is missing or not an object.'.format(key))

    testing = data.get("testing")
    if isinstance(testing, dict):
        commands = testing.get("commands")
        if not isinstance(commands, dict) or not commands:
            error(name, '"testing.commands" must be a non-empty object.')
        elif "full_suite" not in commands and "full_suite_gradle" not in commands:
            error(name, '"testing.commands" has no full_suite entry. The quality gate '
                        "runs the whole suite before reporting a task complete; without "
                        "this key it has nothing to run.")

    for index, skill in enumerate(data.get("official_skills", []) or []):
        where = "{} official_skills[{}]".format(name, index)
        if not isinstance(skill, dict):
            error(where, "entry is not an object.")
            continue
        for field in ("id", "owner", "covers", "does_not_cover", "source_url"):
            if field not in skill:
                error(where, 'missing required field "{}".'.format(field))
        # The core honesty rule: an unverifiable field is marked, never invented.
        if skill.get("install") is None and not skill.get("needs_verification"):
            error(where, 'install is null but needs_verification is not true. '
                         "An unknown install command must be declared unknown so the "
                         "mentor warns the user instead of guessing one.")
        owner_kind = skill.get("owner_kind")
        if owner_kind is not None and owner_kind not in VALID_OWNER_KINDS:
            error(where, 'owner_kind "{}" is not one of {}.'
                  .format(owner_kind, sorted(VALID_OWNER_KINDS)))
        if owner_kind is None:
            warn(where, "no owner_kind. The mentor states who publishes a skill when "
                        "recommending it; without this it cannot.")
        source_url = str(skill.get("source_url", ""))
        if not source_url.startswith("https://"):
            error(where, 'source_url must be an https URL, got "{}".'.format(source_url))

    architecture = data.get("architecture")
    if architecture is None:
        warn(name, "no architecture block. The mentor then has nothing to say about which "
                   "structural variant this stack's team recommends - the judgment a "
                   "senior actually supplies. See docs/ROADMAP.md.")
    elif architecture.get("recommended_by") == "framework-team" \
            and not architecture.get("needs_verification") \
            and not str(architecture.get("source_url", "")).startswith("https://"):
        error(name, "architecture claims framework-team backing with no source_url. "
                    "Attribute it or mark needs_verification.")

    gap_map = data.get("gap_map")
    if not isinstance(gap_map, list):
        error(name, '"gap_map" must be an array.')
    else:
        for index, gap in enumerate(gap_map):
            where = "{} gap_map[{}]".format(name, index)
            if not isinstance(gap, dict):
                error(where, "entry is not an object.")
                continue
            for field in ("gap", "why_it_matters", "fallback"):
                if not gap.get(field):
                    error(where, 'missing or empty required field "{}".'.format(field))

    # Windows-style separators break path handling on every other platform.
    blob = json.dumps(data)
    if "\\\\" in blob:
        error(name, "contains a backslash. Use forward slashes in every path.")


def check_index(index: dict, stack_files: list) -> None:
    declared = {entry.get("stack"): entry for entry in index.get("stacks", [])}
    on_disk = {f[: -len(".json")] for f in stack_files}

    for missing in sorted(on_disk - set(declared)):
        error("index.json", 'registry/{}.json exists but is not listed in "stacks". '
                            "The mentor reads index.json first, so an unlisted stack is invisible."
              .format(missing))
    for phantom in sorted(set(declared) - on_disk):
        error("index.json", 'lists stack "{}" but registry/{}.json does not exist.'
              .format(phantom, phantom))

    for stack, entry in declared.items():
        file_name = entry.get("file")
        if file_name != "{}.json".format(stack):
            error("index.json", 'stack "{}" points at file "{}"; expected "{}.json".'
                  .format(stack, file_name, stack))
        if not DATE_RE.match(str(entry.get("last_verified", ""))):
            error("index.json", 'stack "{}" has a malformed last_verified.'.format(stack))
        if "has_framework_team_skill" not in entry:
            error("index.json", 'stack "{}" is missing has_framework_team_skill. '
                                "The mentor tells the user when a stack has no "
                                "framework-team skill; this field is how it knows."
                  .format(stack))

    if not DATE_RE.match(str(index.get("synced_at", ""))):
        error("index.json", '"synced_at" must be YYYY-MM-DD. It is shown to the user '
                            "verbatim when the mentor falls back to the bundled copy.")

    base = str(index.get("raw_base_url", ""))
    if not base.startswith("https://") or not base.endswith("/"):
        error("index.json", '"raw_base_url" must be an https URL ending in "/", got "{}".'
              .format(base))


def check_index_matches_stack_files(index: dict) -> None:
    """has_framework_team_skill must reflect what the stack file actually says."""
    for entry in index.get("stacks", []):
        stack = entry.get("stack")
        path = os.path.join(REGISTRY_DIR, "{}.json".format(stack))
        if not os.path.exists(path):
            continue  # already reported by check_index
        data = load_json(path)
        actual = any(
            skill.get("owner_kind") == "framework-team"
            for skill in data.get("official_skills", []) or []
        )
        if bool(entry.get("has_framework_team_skill")) != actual:
            error("index.json", 'stack "{}" declares has_framework_team_skill={} but '
                                "{}.json {} a framework-team skill."
                  .format(stack, entry.get("has_framework_team_skill"), stack,
                          "does contain" if actual else "does not contain"))


def main() -> int:
    if not os.path.isdir(REGISTRY_DIR):
        print("FATAL: {} is not a directory.".format(REGISTRY_DIR), file=sys.stderr)
        return 2

    all_files = sorted(f for f in os.listdir(REGISTRY_DIR) if f.endswith(".json"))
    stack_files = [f for f in all_files if f not in NON_STACK_FILES]
    if not stack_files:
        print("FATAL: no stack files found in registry/.", file=sys.stderr)
        return 2

    schema = load_json(os.path.join(REGISTRY_DIR, "schema.json"))

    validator = None
    try:
        import jsonschema  # type: ignore
        validator = jsonschema.Draft202012Validator(schema)
        mode = "full (jsonschema installed)"
    except ImportError:
        mode = "structural only (jsonschema not installed - run: pip install jsonschema)"

    for name in stack_files:
        data = load_json(os.path.join(REGISTRY_DIR, name))
        if not isinstance(data, dict):
            error(name, "top level value must be an object.")
            continue
        if validator is not None:
            for violation in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
                location = "/".join(str(p) for p in violation.path) or "<root>"
                error(name, "schema violation at {}: {}".format(location, violation.message))
        check_stack_entry(name, data)

    index = load_json(os.path.join(REGISTRY_DIR, "index.json"))
    check_index(index, stack_files)
    check_index_matches_stack_files(index)

    print("validate_registry: {} stack files, mode: {}".format(len(stack_files), mode))
    for message in warnings:
        print("  WARN  {}".format(message))
    for message in errors:
        print("  ERROR {}".format(message), file=sys.stderr)

    if errors:
        print("\n{} error(s). Fix them or mark the unverifiable field with "
              '"needs_verification": true.'.format(len(errors)), file=sys.stderr)
        return 1
    print("  all registry files valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
