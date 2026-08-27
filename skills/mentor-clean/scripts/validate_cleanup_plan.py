#!/usr/bin/env python3
"""Validate a cleanup plan immediately before execution. Deletes nothing.

    python3 validate_cleanup_plan.py --root . --plan cleanup-plan.json

Run this again right before executing, even if the plan was built a minute ago. Between
building and executing, the tree can move: a file gets edited, a branch gets switched, a
symbol acquires a new caller. This script is what catches that.

Exit codes:
    0  plan is safe to execute
    1  plan is not safe; every reason is printed with what to do about it
    2  the script could not run
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys

PLAN_VERSION = 1

# Files the cleanup workflow writes itself; their presence does not make a tree dirty.
TOOL_ARTIFACTS = {"candidates.json", "cleanup-plan.json"}

REQUIRED_TOP_LEVEL = [
    "plan_version", "repo_root", "git_head", "git_branch",
    "tests_passed_before", "test_command", "approved",
    "candidates", "requires_human_review",
]
REQUIRED_ENTRY = [
    "path", "symbol", "action", "sha256", "risk", "risk_reasons",
    "requires_human_review", "evidence",
]

problems: list = []


def fail(message: str, fix: str) -> None:
    problems.append((message, fix))


def die(message: str) -> None:
    print("ERROR: {}".format(message), file=sys.stderr)
    sys.exit(2)


def run_git(root: str, args: list):
    try:
        return subprocess.run(["git"] + args, cwd=root, capture_output=True,
                              text=True, check=False)
    except FileNotFoundError:
        die("git is not installed or not on PATH.")
    except OSError as exc:
        die("could not run git: {}".format(exc))


def sha256_of(path: str):
    digest = hashlib.sha256()
    try:
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
    except OSError:
        return None
    return digest.hexdigest()


def load_plan(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            plan = json.load(handle)
    except FileNotFoundError:
        die("plan not found: {}. Build one with build_cleanup_plan.py.".format(path))
    except json.JSONDecodeError as exc:
        die("plan is not valid JSON: {}".format(exc))
    except OSError as exc:
        die("cannot read plan: {}".format(exc))
    if not isinstance(plan, dict):
        die("plan must be a JSON object.")
    return plan


def check_structure(plan: dict) -> None:
    if plan.get("plan_version") != PLAN_VERSION:
        fail("plan_version is {}, this validator expects {}"
             .format(plan.get("plan_version"), PLAN_VERSION),
             "Rebuild the plan with the current build_cleanup_plan.py.")
    for field in REQUIRED_TOP_LEVEL:
        if field not in plan:
            fail('plan is missing "{}"'.format(field),
                 "Rebuild the plan; do not hand-edit it.")


def check_preconditions(plan: dict, root: str) -> None:
    if plan.get("tests_passed_before") is not True:
        fail("the plan does not record a green suite before planning",
             "Rebuild the plan. build_cleanup_plan.py runs the suite itself and refuses "
             "to write a plan when it fails.")

    if plan.get("approved") is not True:
        fail("the plan is not approved",
             'Show the plan to the user, then set "approved": true only after they say '
             "yes. The user approves the plan, not the deletion.")

    status = run_git(root, ["status", "--porcelain"])
    if status.returncode != 0:
        fail("git status failed: {}".format(status.stderr.strip()),
             "Check that --root points at a git working tree.")
    else:
        # The plan files this workflow writes are not project changes; everything else -
        # modified or untracked - is, and untracked files are invisible to git grep.
        dirty = [line[3:].strip().strip('"') for line in status.stdout.splitlines()
                 if len(line) >= 4
                 and os.path.basename(line[3:].strip().strip('"')) not in TOOL_ARTIFACTS]
        if dirty:
            fail("the working tree is dirty: {}".format(", ".join(dirty[:10])),
                 "Commit or stash first. Execution must produce a diff containing nothing "
                 "but the cleanup.")

    head = run_git(root, ["rev-parse", "HEAD"])
    if head.returncode == 0:
        current = head.stdout.strip()
        if current != plan.get("git_head"):
            fail("HEAD is {} but the plan was built against {}"
                 .format(current[:12], str(plan.get("git_head"))[:12]),
                 "The tree moved after the plan was built. Rebuild the plan; its "
                 "evidence is about a different commit.")

    if os.path.abspath(root) != os.path.abspath(str(plan.get("repo_root", ""))):
        fail("plan was built for {} but --root is {}"
             .format(plan.get("repo_root"), os.path.abspath(root)),
             "Run the validator against the repository the plan was built for.")


def check_entries(plan: dict, root: str) -> None:
    candidates = plan.get("candidates")
    if not isinstance(candidates, list):
        fail('"candidates" is not an array', "Rebuild the plan.")
        return
    if not candidates:
        fail("the plan has no executable candidates",
             "Nothing to do. Stop here rather than executing an empty plan.")

    seen_paths = {}
    for index, entry in enumerate(candidates):
        where = "candidates[{}]".format(index)
        if not isinstance(entry, dict):
            fail("{} is not an object".format(where), "Rebuild the plan.")
            continue
        for field in REQUIRED_ENTRY:
            if field not in entry:
                fail("{} is missing {}".format(where, field), "Rebuild the plan.")

        path = entry.get("path", "")
        symbol = entry.get("symbol", "?")

        # The core safety rule: nothing needing human review is ever executable.
        if entry.get("requires_human_review"):
            fail("{} ({}) is marked requires_human_review but sits in the executable "
                 "list".format(where, path),
                 "Move it to requires_human_review, or have a human clear it and rebuild "
                 "the plan. Never promote it by editing this file.")

        if entry.get("risk") != "low":
            fail("{} ({}) has risk={} in the executable list"
                 .format(where, path, entry.get("risk")),
                 "Only low-risk candidates execute automatically. Everything else is a "
                 "human decision.")

        evidence = entry.get("evidence") or {}
        if not isinstance(evidence, dict) or "inbound_references_source" not in evidence:
            fail("{} ({}) has no reference evidence".format(where, path),
                 "Rebuild the plan. A candidate with no evidence is a guess.")
        elif evidence.get("inbound_references_source", 0) > 0:
            fail("{} ({}) has {} inbound source reference(s)"
                 .format(where, path, evidence["inbound_references_source"]),
                 "It is not dead. Remove it from the plan.")

        full = os.path.join(root, path)
        if not os.path.isfile(full):
            fail("{} ({}) no longer exists".format(where, path),
                 "Rebuild the plan; the candidate list is stale.")
        else:
            actual = sha256_of(full)
            if actual is None:
                fail("{} ({}) cannot be read".format(where, path),
                     "Check file permissions, then rebuild the plan.")
            elif actual != entry.get("sha256"):
                fail("{} ({}) changed since the plan was built".format(where, path),
                     "Someone edited it. Rebuild the plan so the evidence matches the "
                     "file you are about to delete.")

        if path in seen_paths and seen_paths[path] != symbol:
            fail("{} deletes from {} which another entry also touches".format(where, path),
                 "Merge the entries. Two edits to one file in one plan can conflict.")
        seen_paths[path] = symbol

        if "\\" in path:
            fail("{} path uses backslashes".format(where), "Use forward slashes.")

    review = plan.get("requires_human_review")
    if isinstance(review, list):
        for index, entry in enumerate(review):
            if isinstance(entry, dict) and not entry.get("risk_reasons"):
                fail("requires_human_review[{}] has no stated reason".format(index),
                     "A human cannot review a flag with no reason attached. Rebuild.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a cleanup plan.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--plan", default="cleanup-plan.json")
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        die("--root {} is not a directory".format(root))

    plan = load_plan(args.plan)
    check_structure(plan)
    check_preconditions(plan, root)
    check_entries(plan, root)

    executable = len(plan.get("candidates") or [])
    review = len(plan.get("requires_human_review") or [])

    if problems:
        print("Plan REJECTED - {} problem(s):\n".format(len(problems)), file=sys.stderr)
        for message, fix in problems:
            print("  * {}\n    -> {}\n".format(message, fix), file=sys.stderr)
        print("Nothing was deleted.", file=sys.stderr)
        return 1

    print("Plan accepted.")
    print("  {} file(s) will be touched".format(executable))
    print("  {} candidate(s) held back for human review".format(review))
    print("  baseline commit: {}".format(str(plan.get("git_head"))[:12]))
    print("\nExecute on a dedicated branch, then run: {}"
          .format(plan.get("test_command")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
