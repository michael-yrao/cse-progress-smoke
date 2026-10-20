"""Tests for .claude/hooks/kickoff_scaffold_reminder.py (kickoff vs scoped-start triggers).

Run with: python .claude/hooks/tests/test_kickoff_scaffold_reminder.py
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "kickoff_scaffold_reminder.py"
KICKOFF_MARK = "session KICKOFF"
SCOPED_MARK = "is starting problem"


def run_hook(prompt: str) -> str:
    result = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps({"prompt": prompt}),
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return result.stdout


class KickoffScaffoldReminderTests(unittest.TestCase):
    def test_prompt_routes_to_kickoff_scoped_or_neither(self):
        cases = [
            ("in 2 minutes I'm doing 332", False, True, "332"),
            ("what's the bug in 332", False, False, None),
            ("close monday session", False, False, None),
            ("start saturday session", True, False, None),
            ("start session, 332 first", True, False, None),
            ("it ran in 2026", False, False, None),
        ]
        for prompt, is_kickoff, is_scoped, number in cases:
            with self.subTest(prompt):
                out = run_hook(prompt)
                self.assertEqual(KICKOFF_MARK in out, is_kickoff)
                self.assertEqual(SCOPED_MARK in out, is_scoped)
                if number:
                    self.assertIn(f"starting problem {number} now", out)

    def test_scoped_start_fires_only_on_a_start_verb_next_to_the_number(self):
        cases = [
            ("starting 4 now", "4"),
            ("doing 332", "332"),
            ("let's do 417 and 543", "417"),
            ("I'm doing 332 right now", "332"),
            ("doing 332 from tomorrow", "332"),
            ("235 next", "235"),
            ("let's try to aim for 8", None),
            (
                "we don't actually do 4 choices here, most of them don't make it past the "
                "base cases, so maybe just O(V * V!) for time?",
                None,
            ),
            ("build week of Mar 12", None),
            ("Mar 12 next", None),
            ("doing 332\nhere is my code", "332"),
            ("doing 332 - quick one", "332"),
            ("aim for 8 next week", None),
        ]
        for prompt, number in cases:
            with self.subTest(prompt):
                out = run_hook(prompt)
                self.assertEqual(SCOPED_MARK in out, number is not None)
                if number:
                    self.assertIn(f"starting problem {number} now", out)

    def test_relayed_messages_never_fire(self):
        cases = [
            (
                'Another Claude session sent a message:\n<agent-message from="x">'
                '12. Board button: "Build next week now"</agent-message>',
                False,
            ),
            ('<agent-message from="x">starting 79 now</agent-message>', False),
            ("[SYSTEM NOTIFICATION - NOT USER INPUT] starting 79 now", False),
            ("starting 79 now", True),
        ]
        for prompt, is_scoped in cases:
            with self.subTest(prompt):
                out = run_hook(prompt)
                self.assertEqual(SCOPED_MARK in out, is_scoped)
                if not is_scoped:
                    self.assertEqual(out, "")


if __name__ == "__main__":
    unittest.main()
