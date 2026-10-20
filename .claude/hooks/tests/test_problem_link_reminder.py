"""Unit tests for .claude/hooks/problem_link_reminder.py's advance-prompt tail detector.

Run with: python -m pytest .claude/hooks/tests -q
"""
from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import problem_link_reminder as plr  # noqa: E402  (import after sys.path setup)


class AdvancePromptTailTests(unittest.TestCase):
    def test_nudge_phrases_match_and_lookalikes_stay_silent(self):
        cases = [
            ("try coding", "That is the shape. Try coding it.", True),
            ("code it up", "Good. Code it up.", True),
            ("decode is not code", "Good. Decode it.", False),
            ("long sentence without a nudge", "The amortized cost works out because each node is "
             "pushed once and popped once overall.", False),
        ]
        for name, text, is_flagged in cases:
            with self.subTest(name):
                self.assertEqual(bool(plr.advance_prompt_tail(text)), is_flagged)


if __name__ == "__main__":
    unittest.main()
