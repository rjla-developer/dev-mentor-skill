#!/usr/bin/env python3
"""Build a dead-code cleanup plan. Deletes nothing.

    python3 build_cleanup_plan.py \
        --root . \
        --candidates candidates.json \
        --test-command "flutter test" \
        --out cleanup-plan.json

candidates.json is produced by the agent's analysis:

    {"candidates": [{"path": "lib/legacy/old_parser.dart",
                     "symbol": "OldParser",
                     "kind": "class",
                     "action": "delete-file"}]}

The script enforces the two preconditions that a model cannot be trusted to check by
eye - a clean working tree and a green suite - then classifies every candidate by risk
and splits the safe ones from the ones a human has to look at.

Exit codes:
    0  plan written
    1  a precondition failed, or no candidate survived (message says which)
    2  the script could not run (bad arguments, missing files, git unavailable)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

# --- Risk model -------------------------------------------------------------------
#
# Every pattern below marks code that looks unreferenced to a text search but is reached
# by a mechanism the search cannot see. Deleting one of these is the failure mode this
# whole script exists to prevent, so they are never "safe" - they go to human review.

# Generated files. Regenerating them is the only correct edit; a hand deletion comes back
# on the next build, or worse, does not.
GENERATED_PATTERNS = [
    (r"\.g\.dart$", "Dart build_runner output"),
    (r"\.freezed\.dart$", "Dart freezed output"),
    (r"\.mocks\.dart$", "Dart mockito output"),
    (r"\.pb\.(go|py|dart|ts|cc|java)$", "protobuf output"),
    (r"_pb2\.py$", "protobuf output"),
    (r"\.generated\.(ts|cs|java)$", "code generator output"),
    (r"\.designer\.cs$", ".NET designer output"),
    (r"migrations?/", "database migration - discovered by directory scan, not by import"),
    (r"/generated/", "generator output directory"),
]

# Files whose contents are reached by convention or configuration rather than by import.
CONVENTION_PATTERNS = [
    (r"(^|/)app/.*/(page|layout|loading|error|route|template)\.(t|j)sx?$",
     "Next.js App Router file - reachable by filesystem convention, never imported"),
    (r"(^|/)pages/.*\.(t|j)sx?$",
     "Next.js Pages Router file - reachable by filesystem convention"),
    (r"(^|/)app/.*\.(t|j)sx?$",
     "expo-router file - reachable by filesystem convention"),
    (r"(^|/)__init__\.py$", "Python package marker - deleting it breaks imports"),
    (r"conftest\.py$", "pytest fixture discovery file"),
    (r"Program\.(cs|fs)$", ".NET entry point"),
    (r"(^|/)main\.(dart|py|go|ts)$", "entry point"),
]

# Reference sites that do NOT prove the symbol is alive in production code.
TEST_PATH_RE = re.compile(
    r"(^|/)(tests?|__tests__|spec|integration_test)/|"
    r"(_test|_spec|\.test|\.spec|Test|Tests)\.[a-z]+$"
)
CONFIG_PATH_RE = re.compile(
    r"(^|/)(\.github|\.circleci|\.gitlab-ci\.yml|ci|deploy)/|"
    r"(^|/)[^/]*\.(ya?ml|toml|ini|cfg|json|props|targets)$"
)
DOC_PATH_RE = re.compile(r"\.(md|mdx|rst|txt)$")

# A symbol reachable by reflection, DI-by-name or a string key looks dead to every static
# tool. These markers near a reference site mean "a human decides".
DYNAMIC_ACCESS_MARKERS = [
    "getIt", "GetIt", "registerSingleton", "registerFactory",  # Dart service locators
    "@Injectable", "@Inject", "useClass", "useFactory", "provide:",  # Angular / Nest DI
    "AddScoped", "AddSingleton", "AddTransient", "GetService",  # .NET DI
    "@Bean", "@Component", "@Service", "@Autowired", "Class.forName",  # Spring
    "getattr", "importlib", "__import__", "globals()[",  # Python dynamic access
    "reflect", "Reflection", "Activator.CreateInstance",  # reflection
    "dynamic(", "React.lazy", "require(",  # dynamic import
]

RISK_LOW = "low"
RISK_MEDIUM = "medium"
RISK_HIGH = "high"

PLAN_VERSION = 1
DEFAULT_TEST_TIMEOUT_SECONDS = 1800  # 30 min: long enough for a mobile or JVM suite.

# Files this workflow writes itself. They never reference project symbols, so their
# presence in an otherwise clean tree is not a reason to refuse.
TOOL_ARTIFACTS = {"candidates.json", "cleanup-plan.json"}


def die(message: str, code: int = 2) -> None:
    print("ERROR: {}".format(message), file=sys.stderr)
    sys.exit(code)


def run_git(root: str, args: list) -> str:
    """Run a git command, converting every failure into an explicit message."""
    try:
        result = subprocess.run(
            ["git"] + args, cwd=root, capture_output=True, text=True, check=False
        )
    except FileNotFoundError:
        die("git is not installed or not on PATH. mentor-clean requires git, because "
            "the only safe way to run this operation is on a branch you can throw away.")
    except OSError as exc:
        die("could not run git: {}".format(exc))
    if result.returncode != 0:
        die("git {} failed: {}".format(" ".join(args), result.stderr.strip()))
    return result.stdout


def dirty_paths(root: str) -> list:
    """Paths that make the tree unclean, excluding this tool's own artifacts.

    Untracked files matter here as much as modified ones: git grep only searches tracked
    files, so an untracked source file referencing a candidate is invisible to the
    evidence gathering. The only exceptions are the plan files this workflow itself
    creates, which contain no references to anything.
    """
    status = run_git(root, ["status", "--porcelain"])
    paths = []
    for line in status.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].strip().strip('"')
        if os.path.basename(path) in TOOL_ARTIFACTS:
            continue
        paths.append(path)
    return paths


def check_preconditions(root: str, test_command: str, test_timeout: int) -> dict:
    """Clean tree, then a green suite. Both are hard requirements, with no override."""
    inside = run_git(root, ["rev-parse", "--is-inside-work-tree"]).strip()
    if inside != "true":
        die("{} is not inside a git working tree.".format(root), 1)

    dirty = dirty_paths(root)
    if dirty:
        changed = "\n  ".join(dirty[:20])
        die("the working tree is not clean. Commit or stash these first, so the cleanup "
            "is a diff you can revert in one command, and so that git grep can see every "
            "file that might reference a candidate:\n  {}".format(changed), 1)

    head = run_git(root, ["rev-parse", "HEAD"]).strip()
    branch = run_git(root, ["rev-parse", "--abbrev-ref", "HEAD"]).strip()

    print("Running the suite before planning: {}".format(test_command))
    try:
        proc = subprocess.run(
            test_command, cwd=root, shell=True, capture_output=True, text=True,
            timeout=test_timeout, check=False,
        )
    except subprocess.TimeoutExpired:
        die("the test command exceeded {}s. Raise --test-timeout, or narrow the suite. "
            "A cleanup planned against an unverified baseline is worthless."
            .format(test_timeout), 1)
    except OSError as exc:
        die("could not run the test command: {}".format(exc), 1)

    if proc.returncode != 0:
        tail = (proc.stdout or "")[-2000:] + (proc.stderr or "")[-2000:]
        die("the suite fails before any cleanup (exit {}). Fix it first - otherwise a "
            "failure after the cleanup proves nothing.\n--- last output ---\n{}"
            .format(proc.returncode, tail.strip()), 1)

    print("  suite green at {}".format(head[:12]))
    return {"git_head": head, "git_branch": branch,
            "tests_passed_before": True, "test_command": test_command}


def sha256_of(path: str) -> str:
    digest = hashlib.sha256()
    try:
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
    except OSError as exc:
        die("cannot hash {}: {}".format(path, exc))
    return digest.hexdigest()


def match_patterns(rel_path: str, patterns: list) -> list:
    return [reason for pattern, reason in patterns if re.search(pattern, rel_path)]


def find_references(root: str, symbol: str, own_path: str) -> list:
    """Every tracked line mentioning the symbol, excluding its own file.

    git grep is used deliberately: it searches tracked files only, so build output and
    vendored dependencies do not create phantom references.
    """
    try:
        result = subprocess.run(
            ["git", "grep", "-n", "-F", "-e", symbol],
            cwd=root, capture_output=True, text=True, check=False,
        )
    except OSError as exc:
        die("could not run git grep: {}".format(exc))

    # git grep exits 1 when there are no matches. That is a result, not an error.
    if result.returncode not in (0, 1):
        die("git grep failed for {}: {}".format(symbol, result.stderr.strip()))

    sites = []
    for line in result.stdout.splitlines():
        parts = line.split(":", 2)
        if len(parts) != 3:
            continue
        file_path, line_no, text = parts
        if file_path == own_path:
            continue
        if TEST_PATH_RE.search(file_path):
            context = "test"
        elif CONFIG_PATH_RE.search(file_path):
            context = "config"
        elif DOC_PATH_RE.search(file_path):
            context = "docs"
        else:
            context = "source"
        sites.append({
            "file": file_path,
            "line": int(line_no) if line_no.isdigit() else 0,
            "context": context,
            "text": text.strip()[:160],
        })
    return sites


def scan_dynamic_markers(root: str, own_path: str) -> list:
    """Markers inside the candidate's own file that suggest it is reached dynamically."""
    full = os.path.join(root, own_path)
    try:
        with open(full, "r", encoding="utf-8", errors="replace") as handle:
            content = handle.read()
    except OSError:
        return []
    return [marker for marker in DYNAMIC_ACCESS_MARKERS if marker in content]


def classify(root: str, candidate: dict) -> dict:
    rel_path = candidate["path"]
    symbol = candidate["symbol"]
    full_path = os.path.join(root, rel_path)

    if not os.path.isfile(full_path):
        return {"path": rel_path, "symbol": symbol, "error":
                "file does not exist; the candidate list is stale"}

    sites = find_references(root, symbol, rel_path)
    source_sites = [s for s in sites if s["context"] == "source"]
    test_sites = [s for s in sites if s["context"] == "test"]
    config_sites = [s for s in sites if s["context"] == "config"]

    reasons = []
    reasons += match_patterns(rel_path, GENERATED_PATTERNS)
    reasons += match_patterns(rel_path, CONVENTION_PATTERNS)
    markers = scan_dynamic_markers(root, rel_path)
    if markers:
        reasons.append("file contains dynamic-access markers ({}); a static search "
                       "cannot prove it is unreachable".format(", ".join(markers[:4])))
    if config_sites:
        reasons.append("referenced from configuration or CI ({})"
                       .format(config_sites[0]["file"]))
    if test_sites and not source_sites:
        reasons.append("referenced only from tests - either the code is dead and the "
                       "test with it, or the test is the last real consumer")
    if source_sites:
        reasons.append("{} reference(s) in source: {}".format(
            len(source_sites),
            ", ".join("{}:{}".format(s["file"], s["line"]) for s in source_sites[:5])))

    if source_sites:
        risk = RISK_HIGH
    elif reasons:
        risk = RISK_MEDIUM
    else:
        risk = RISK_LOW

    requires_human_review = risk != RISK_LOW

    return {
        "path": rel_path,
        "symbol": symbol,
        "kind": candidate.get("kind", "unknown"),
        "action": candidate.get("action", "delete-symbol"),
        "sha256": sha256_of(full_path),
        "risk": risk,
        "risk_reasons": reasons,
        "requires_human_review": requires_human_review,
        "evidence": {
            "inbound_references_total": len(sites),
            "inbound_references_source": len(source_sites),
            "inbound_references_test": len(test_sites),
            "inbound_references_config": len(config_sites),
            "reference_sites": sites[:25],
            "searched_with": "git grep -n -F -e {}".format(symbol),
        },
    }


def load_candidates(path: str) -> list:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        die("candidates file not found: {}".format(path))
    except json.JSONDecodeError as exc:
        die("candidates file is not valid JSON: {}".format(exc))
    except OSError as exc:
        die("cannot read candidates file: {}".format(exc))

    candidates = data.get("candidates") if isinstance(data, dict) else data
    if not isinstance(candidates, list) or not candidates:
        die('candidates file must contain a non-empty "candidates" array.')
    for index, item in enumerate(candidates):
        if not isinstance(item, dict):
            die("candidates[{}] is not an object.".format(index))
        for field in ("path", "symbol"):
            if not item.get(field):
                die('candidates[{}] is missing "{}".'.format(index, field))
        if "\\" in item["path"]:
            die('candidates[{}].path uses backslashes; use forward slashes.'.format(index))
    return candidates


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a dead-code cleanup plan.")
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--candidates", required=True, help="candidates JSON file")
    parser.add_argument("--test-command", required=True,
                        help="full-suite command; it must pass before a plan is built")
    parser.add_argument("--test-timeout", type=int, default=DEFAULT_TEST_TIMEOUT_SECONDS)
    parser.add_argument("--out", default="cleanup-plan.json")
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        die("--root {} is not a directory".format(root))

    baseline = check_preconditions(root, args.test_command, args.test_timeout)
    candidates = load_candidates(args.candidates)

    safe, review, broken = [], [], []
    for candidate in candidates:
        entry = classify(root, candidate)
        if "error" in entry:
            broken.append(entry)
        elif entry["requires_human_review"]:
            review.append(entry)
        else:
            safe.append(entry)

    plan = {
        "plan_version": PLAN_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "repo_root": root,
        "approved": False,
        "candidates": safe,
        "requires_human_review": review,
        "unresolved": broken,
    }
    plan.update(baseline)

    try:
        with open(args.out, "w", encoding="utf-8") as handle:
            json.dump(plan, handle, indent=2)
            handle.write("\n")
    except OSError as exc:
        die("cannot write {}: {}".format(args.out, exc))

    print("\nPlan written to {}".format(args.out))
    print("  {} safe candidate(s)".format(len(safe)))
    print("  {} need human review".format(len(review)))
    print("  {} unresolved (stale candidate list)".format(len(broken)))
    print("\nNothing has been deleted. Next: show the plan to the user, get approval, "
          "then run validate_cleanup_plan.py.")

    if not safe and not review:
        print("\nNo candidate survived classification. Nothing to clean.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
