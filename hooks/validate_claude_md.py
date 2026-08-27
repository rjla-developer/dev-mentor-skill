#!/usr/bin/env python3
"""PostToolUse hook: enforce the CLAUDE.md line cap.

Wired to Write and Edit. Reads the hook payload on stdin, and when the edited file is a
CLAUDE.md, checks its length.

Why a hook and not an instruction: a model asked to keep a file short will keep it short
most of the time, and "most of the time" is how a 400-line CLAUDE.md appears. Past a
certain size the file stops being read carefully, and the rules the author cared about
most are the ones that get skipped. A deterministic check is the only kind that holds.

Exit codes (Claude Code hook protocol):
    0  fine; stdout is informational
    2  blocked; stderr is fed back to the model as feedback to act on
"""

from __future__ import annotations

import json
import os
import sys

# 150 lines is roughly four screens. It is set at the point where a contributor stops
# reading top to bottom and starts skimming - past that, added rules dilute the rest
# instead of adding to them. Projects that need more content split by domain into
# sub-files chained with @path imports; that is a structure change, not a bigger cap.
MAX_LINES = 150

# Warn before the cap so the author can restructure deliberately rather than being
# blocked mid-edit. 90% of the cap.
WARN_LINES = int(MAX_LINES * 0.9)

# CLAUDE.local.md holds one developer's personal preferences, is gitignored, and is not
# read by collaborators. Capping it would restrict nobody but its owner.
EXEMPT_BASENAMES = {"CLAUDE.local.md"}
WATCHED_BASENAMES = {"CLAUDE.md"}


def read_payload():
    """Return the hook payload, or None when it is unusable.

    A hook that crashes on an unexpected payload blocks unrelated work, so every parse
    failure here degrades to 'not my business'.
    """
    try:
        raw = sys.stdin.read()
    except (OSError, ValueError):
        return None
    if not raw.strip():
        return None
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def extract_path(payload: dict):
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return None
    path = tool_input.get("file_path") or tool_input.get("path")
    return path if isinstance(path, str) and path else None


def count_lines(path: str):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return sum(1 for _ in handle)
    except FileNotFoundError:
        return None          # Deleted or moved between the edit and this check.
    except OSError as exc:
        print("validate_claude_md: cannot read {}: {}".format(path, exc), file=sys.stderr)
        return None


def main() -> int:
    payload = read_payload()
    if payload is None:
        return 0

    path = extract_path(payload)
    if path is None:
        return 0

    basename = os.path.basename(path)
    if basename in EXEMPT_BASENAMES or basename not in WATCHED_BASENAMES:
        return 0

    lines = count_lines(path)
    if lines is None:
        return 0

    if lines > MAX_LINES:
        print(
            "{} is {} lines; the cap is {}.\n"
            "\n"
            "Cut it back before continuing. In order of what usually works:\n"
            "  1. Delete anything inferable from the code itself. The test for a line: "
            "would removing it make a contributor pick the wrong file, command or limit? "
            "If not, it goes.\n"
            "  2. Delete tutorials, changelogs, generic language rules, and task notes "
            "that will be stale next month.\n"
            "  3. If what remains is genuinely all necessary, split by domain into "
            "backend/CLAUDE.md and frontend/CLAUDE.md, and chain them from the root with "
            "@path imports.\n"
            "  4. Personal preferences belong in CLAUDE.local.md, which is exempt from "
            "this cap and gitignored.\n"
            .format(path, lines, MAX_LINES),
            file=sys.stderr,
        )
        return 2

    if lines >= WARN_LINES:
        print("validate_claude_md: {} is {} lines, approaching the {}-line cap."
              .format(path, lines, MAX_LINES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
