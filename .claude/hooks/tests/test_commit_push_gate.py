"""Unit tests for .claude/hooks/commit_push_gate.py.

Run with: python -m pytest .claude/hooks/tests -q
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import commit_push_gate as gate  # noqa: E402  (import after sys.path setup)


def _run_main(stdin_text: str) -> tuple[str, int]:
    """Drive `main()` the way the harness does; return (stdout, exit code)."""
    captured = io.StringIO()
    exit_code = 0
    with contextlib.redirect_stdout(captured), \
            mock.patch.object(sys, "stdin", io.StringIO(stdin_text)):
        try:
            gate.main()
        except SystemExit as exit_signal:
            exit_code = exit_signal.code
    return captured.getvalue(), exit_code


def _payload(tool_name: str, command: str) -> str:
    return json.dumps({"tool_name": tool_name, "tool_input": {"command": command}})


class CommitPushGateTests(unittest.TestCase):
    def test_denies_only_a_chained_commit_and_push(self):
        cases = [
            (_payload("Bash", "git commit -m x; git push origin main"), True),
            (_payload("Bash", "git commit -m x && git push"), True),
            (_payload("PowerShell", "git commit -m x; if ($?) { git push origin main }"), True),
            (_payload("Bash", "git -C ../site commit -m x; git -C ../site push"), True),
            (_payload("Bash", 'git commit -m "fix: push handler"'), False),
            (_payload("Bash", "git push origin main"), False),
            (_payload("Bash", "git status; git log --oneline"), False),
            (_payload("Bash", "echo '{\"c\": \"git commit -m x; git push origin main\"}'"
                              " | python hook.py"), False),
            (_payload("Bash", "cat >> notes.yml <<'EOF'\n"
                              "denies one command that chains `git commit` and `git push`.\n"
                              "EOF"), False),
            ("not json", False),
        ]
        for stdin_text, should_deny in cases:
            with self.subTest(stdin=stdin_text):
                out, code = _run_main(stdin_text)
                if should_deny:
                    decision = json.loads(out)["hookSpecificOutput"]
                    self.assertEqual(decision["permissionDecision"], "deny")
                    self.assertEqual(decision["permissionDecisionReason"], gate.DENY_REASON)
                    self.assertEqual(code, gate.DENY_EXIT_CODE)
                else:
                    self.assertEqual((out, code), ("", 0))


if __name__ == "__main__":
    unittest.main()
