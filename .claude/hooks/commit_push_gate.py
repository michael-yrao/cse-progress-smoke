"""PreToolUse hook: deny a single Bash/PowerShell command that chains `git commit` and `git push`.

Commit and push are TWO commands, because the pre-commit hook's output must be read
between them -- an `ERROR:` line from a report-only check holds the push. The rule lapsed
as prose: a chained commit+push shipped a stale generated file, then was chained again in
a PowerShell call.

Mechanism: read the PreToolUse payload (`tool_name` Bash or PowerShell, `tool_input.command`).
Split the command into shell segments on `;`, `&&`, `||`, `|`, `(`, `{` and newline. A segment
counts only when, after leading whitespace, it STARTS with `git`, then optional flags
(`-C <path>`, `--flag`), then the subcommand. Deny, with the reason below, when some segment
is a commit and some segment is a push. So prose that merely names the subcommands (a commit
message containing "push", an echoed JSON payload, a heredoc sentence) does not match.
Knowingly not caught: an env-prefixed `FOO=1 git commit`, and a heredoc body line that itself
starts with `git commit`.

Leaves alone: a lone commit, a lone push, any other command, any other tool, and malformed or
non-JSON stdin (silence, exit 0). The deny shape is `permissionDecision: "deny"` JSON on
stdout with exit code 2.

Session-scoped on purpose: it also blocks a chained commit+push aimed at another repo from a
session opened here. No working-directory or repo detection. Stdlib only.

Wiring: see docs/HOOKS.md (PreToolUse, matcher `Bash|PowerShell`).
"""
import json
import re
import sys

WATCHED_TOOLS = ("Bash", "PowerShell")
DENY_EXIT_CODE = 2
DENY_REASON = (
    "commit and push are two commands in this repo — run the commit alone, read the "
    "pre-commit hook's output for any ERROR: line, then push in a separate call "
    "(CLAUDE.md commit and push gate)"
)


SEGMENT_SPLIT_PATTERN = re.compile(r";|&&|\|\||\||\(|\{|\n")


def _git_subcommand_pattern(subcommand: str) -> "re.Pattern[str]":
    """A segment that STARTS with `git`, optional flags (e.g. `-C <path>`), then `subcommand`."""
    return re.compile(
        r"^\s*git\b(?:\s+-[A-Za-z]\s+\S+|\s+--\S+)*\s+" + subcommand + r"\b", re.IGNORECASE
    )


COMMIT_PATTERN = _git_subcommand_pattern("commit")
PUSH_PATTERN = _git_subcommand_pattern("push")


def _segments(command: str) -> list[str]:
    return SEGMENT_SPLIT_PATTERN.split(command)


def chains_commit_and_push(command: str) -> bool:
    segments = _segments(command)
    return (any(COMMIT_PATTERN.match(s) for s in segments)
            and any(PUSH_PATTERN.match(s) for s in segments))


def _command_of(payload: object) -> str:
    """The watched tool's command text, or "" for anything else (never raises)."""
    if not isinstance(payload, dict) or payload.get("tool_name") not in WATCHED_TOOLS:
        return ""
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return ""
    return str(tool_input.get("command", "") or "")


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return  # malformed input is not this hook's problem -- stay silent, exit 0

    if not chains_commit_and_push(_command_of(payload)):
        return

    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": DENY_REASON,
            }
        },
        sys.stdout,
    )
    sys.exit(DENY_EXIT_CODE)


if __name__ == "__main__":
    main()
