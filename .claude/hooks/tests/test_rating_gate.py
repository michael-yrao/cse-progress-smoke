"""Tests for .claude/hooks/rating_gate.py (the Stop hook's trigger and block message).

Run with: python .claude/hooks/tests/test_rating_gate.py
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "rating_gate.py"
LEARNER_MESSAGE = "yeah I think that solution is done and correct"  # no time/space words


def run_hook(assistant_text: str) -> str:
    entries = [
        {"type": "user", "message": {"content": LEARNER_MESSAGE}},
        {
            "type": "assistant",
            "message": {"content": [{"type": "text", "text": assistant_text}]},
        },
    ]
    with tempfile.TemporaryDirectory() as tmp:
        transcript = Path(tmp) / "transcript.jsonl"
        transcript.write_text("\n".join(json.dumps(e) for e in entries), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps({"transcript_path": str(transcript)}),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
    return result.stdout


class RatingGateTests(unittest.TestCase):
    def test_block_only_on_a_glyph_or_rating_word_proposal(self):
        cases = [
            # (turn, expected matched tokens in the block reason; None = no block)
            ("Build clean, confirm the s1 fallback before the push.", None),
            ("Coded from a blank page — reads 🟢 s2. Rate it?", ("🟢", "Rate it")),
        ]
        for turn, tokens in cases:
            with self.subTest(turn):
                out = run_hook(turn)
                if tokens is None:
                    self.assertEqual(out, "")
                    continue
                payload = json.loads(out)
                self.assertEqual(payload["decision"], "block")
                for token in tokens:
                    self.assertIn(token, payload["reason"])


if __name__ == "__main__":
    unittest.main()
