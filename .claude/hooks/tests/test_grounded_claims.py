"""Unit tests for .claude/hooks/grounded_claims.py.

Run with: python -m pytest .claude/hooks/tests -q
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import grounded_claims as gc  # noqa: E402  (import after sys.path setup)


def _run_main(payload: dict) -> str:
    """Drive `main()` the way the harness does: JSON on stdin, JSON (or nothing) on stdout."""
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        with mock.patch.object(sys, "stdin", io.StringIO(json.dumps(payload))):
            gc.main()
    return captured.getvalue()


def _write_jsonl(tmp_dir: str, name: str, entries: list[dict]) -> str:
    path = Path(tmp_dir) / name
    path.write_text("\n".join(json.dumps(e) for e in entries), encoding="utf-8")
    return str(path)


def _text_entry(text: str) -> dict:
    return {"type": "assistant", "message": {"role": "assistant", "content": [
        {"type": "text", "text": text},
    ]}}


def _tool_use_entry(name: str, command: "str | None" = None) -> dict:
    tool_input = {"command": command} if command is not None else {"file_path": "x.py"}
    return {"type": "assistant", "message": {"role": "assistant", "content": [
        {"type": "tool_use", "name": name, "input": tool_input},
    ]}}


def _user_entry(text: str = "go") -> dict:
    return {"type": "user", "message": {"role": "user", "content": text}}


def _tool_result_entry() -> dict:
    """A tool_result carrier: typed 'user' but NOT a turn boundary (see gc._is_real_user_message)."""
    return {"type": "user", "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": "abc", "content": "ok"},
    ]}}


GIT_COMMIT_CMD = "git " + "commit" + " -m x"  # built at runtime -- never a literal in source
GIT_PUSH_CMD = "git " + "push"


class RequiredEndToEndCases(unittest.TestCase):
    """The four behaviors the brief names explicitly, driven stdin -> stdout via main()."""

    def test_bare_claim_no_tool_use_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            path = _write_jsonl(td, "t.jsonl", [
                _user_entry(),
                _text_entry("Logged the entry in the tracker."),
            ])
            out = _run_main({"transcript_path": path})
            payload = json.loads(out)
            self.assertEqual(payload["decision"], "block")
            self.assertIn("Logged the entry in the tracker.", payload["reason"])

    def test_same_claim_with_edit_tool_use_is_silent(self):
        with tempfile.TemporaryDirectory() as td:
            path = _write_jsonl(td, "t.jsonl", [
                _user_entry(),
                _tool_use_entry("Edit"),
                _text_entry("Logged the entry in the tracker."),
            ])
            out = _run_main({"transcript_path": path})
            self.assertEqual(out, "")

    def test_committed_claim_with_only_edit_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            path = _write_jsonl(td, "t.jsonl", [
                _user_entry(),
                _tool_use_entry("Edit"),
                _text_entry("Committed the schedule changes."),
            ])
            out = _run_main({"transcript_path": path})
            payload = json.loads(out)
            self.assertEqual(payload["decision"], "block")

    def test_committed_claim_with_git_commit_bash_is_silent(self):
        with tempfile.TemporaryDirectory() as td:
            path = _write_jsonl(td, "t.jsonl", [
                _user_entry(),
                _tool_use_entry("Bash", command=GIT_COMMIT_CMD),
                _text_entry("Committed the schedule changes."),
            ])
            out = _run_main({"transcript_path": path})
            self.assertEqual(out, "")


class ReadOnlyEvidenceCases(unittest.TestCase):
    """End-to-end (via `main()`, real transcript shape) for the read-only-Bash and
    Agent-delegation evidence rules -- `EVIDENCE_CASES` in the hook itself exercises the
    logic against synthetic `Turn`s directly; these two go through `last_turn` too, so the
    turn-boundary parsing that captures `input.command` and an `Agent` tool_use name is
    also exercised, not just the evidence function in isolation."""

    def test_aug21_case_grep_only_bash_still_blocks(self):
        """The Aug 21, 2026 lapse, in its real shape: a Bash `tool_use` entry (a `grep`
        read), a `tool_result` carrier, then the claim text -- a read-only Bash call
        contributes nothing, so this must still block."""
        with tempfile.TemporaryDirectory() as td:
            path = _write_jsonl(td, "t.jsonl", [
                _user_entry(),
                _tool_use_entry("Bash", command="grep -rn TODO tracker.md"),
                _tool_result_entry(),
                _text_entry("Updated the tracker row."),
            ])
            out = _run_main({"transcript_path": path})
            payload = json.loads(out)
            self.assertEqual(payload["decision"], "block")

    def test_agent_delegation_evidences_a_file_claim(self):
        """An `Agent`/`Task` tool_use is the tool result a delegated claim rests on."""
        with tempfile.TemporaryDirectory() as td:
            path = _write_jsonl(td, "t.jsonl", [
                _user_entry(),
                _tool_use_entry("Agent"),
                _tool_result_entry(),
                _text_entry("Updated the schedule file."),
            ])
            out = _run_main({"transcript_path": path})
            self.assertEqual(out, "")


class RobustnessCases(unittest.TestCase):
    def test_missing_transcript_is_silent(self):
        out = _run_main({"transcript_path": r"C:\does\not\exist.jsonl"})
        self.assertEqual(out, "")

    def test_malformed_stdin_is_silent(self):
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            with mock.patch.object(sys, "stdin", io.StringIO("not json")):
                gc.main()
        self.assertEqual(captured.getvalue(), "")

    def test_null_transcript_path_is_silent(self):
        """`transcript_path: null` must not reach `open(None)` (TypeError)."""
        out = _run_main({"transcript_path": None})
        self.assertEqual(out, "")

    def test_int_transcript_path_is_silent(self):
        """A non-string `transcript_path` (e.g. a bare int) must never reach `open()` at
        all -- `open(5)` opens file descriptor 5, which is not this hook's business."""
        out = _run_main({"transcript_path": 5})
        self.assertEqual(out, "")

    def test_non_utf8_transcript_is_silent(self):
        """A path that exists but isn't valid UTF-8 text must not raise UnicodeDecodeError
        (a ValueError) out of `_entries`."""
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "binary.jsonl"
            path.write_bytes(bytes([0x90, 0x00, 0xFF, 0xFE, 0x80]))
            out = _run_main({"transcript_path": str(path)})
            self.assertEqual(out, "")

    def test_non_dict_message_is_silent(self):
        """A transcript line whose `message` is a truthy non-dict (e.g. a bare string)
        must not raise AttributeError out of `_is_real_user_message`/`last_turn`. The
        malformed entry is the turn's only content, so nothing is recovered from it and
        the turn is silent -- not a crash, and not a false block on unreadable input."""
        with tempfile.TemporaryDirectory() as td:
            path = _write_jsonl(td, "t.jsonl", [
                _user_entry(),
                {"type": "assistant", "message": "not a dict"},
            ])
            out = _run_main({"transcript_path": path})
            self.assertEqual(out, "")

    def test_null_text_block_is_silent(self):
        """A `text` block whose `"text"` key is present but `null` must not raise
        TypeError out of `"\\n".join(...)` in `last_turn` -- `.get("text", "")`'s default
        never fires when the key IS present, just with a null value."""
        with tempfile.TemporaryDirectory() as td:
            path = _write_jsonl(td, "t.jsonl", [
                _user_entry(),
                {"type": "assistant", "message": {"role": "assistant", "content": [
                    {"type": "text", "text": None},
                ]}},
            ])
            out = _run_main({"transcript_path": path})
            self.assertEqual(out, "")

    def test_stop_hook_active_short_circuits(self):
        with tempfile.TemporaryDirectory() as td:
            path = _write_jsonl(td, "t.jsonl", [
                _user_entry(),
                _text_entry("Logged the entry in the tracker."),
            ])
            out = _run_main({"transcript_path": path, "stop_hook_active": True})
            self.assertEqual(out, "")


class TranscriptShapeCases(unittest.TestCase):
    """TRANSCRIPT_CASES: a hand-written transcript with the REAL shape -- text and tool_use as
    separate assistant entries, a tool_result carrier (typed 'user', not a turn boundary)
    interleaved between them, and a genuine user entry that DOES end the turn.

    This is the shape a real Claude Code session actually writes (one JSONL line per content
    block, not one line per turn) -- see the `_entries`/`last_turn` docstrings for why a naive
    "read the last line" approach missed this before (problem_link_reminder.py's own history).
    """

    def _fixture(self, tmp_dir: str) -> "tuple[str, str]":
        """Returns (path_up_to_turn_A, path_up_to_turn_B) -- two prefixes of one session log."""
        entries = [
            _user_entry("kickoff"),
            _tool_use_entry("Edit"),           # turn A's evidence, its own entry
            _tool_result_entry(),              # NOT a turn boundary (typed 'user')
            # a malformed line a real session should never write, but a parser must
            # survive anyway -- `message` here is a truthy non-dict, not skipped by `or {}`
            {"type": "assistant", "message": "not a dict"},
            _text_entry("Logged the entry in the tracker."),  # turn A's claim, its own entry
        ]
        turn_a_path = _write_jsonl(tmp_dir, "turn_a.jsonl", entries)

        entries_b = entries + [
            _user_entry("next"),               # a REAL user message -- ends turn A, starts B
            _text_entry("Logged the entry in the tracker."),  # turn B's claim, no tool_use here
        ]
        turn_b_path = _write_jsonl(tmp_dir, "turn_b.jsonl", entries_b)
        return turn_a_path, turn_b_path

    def test_evidence_found_across_a_tool_result_carrier(self):
        """The Edit tool_use sits in an earlier assistant entry than the claim text, with a
        tool_result carrier in between -- evidence must still be found for THIS turn."""
        with tempfile.TemporaryDirectory() as td:
            turn_a_path, _ = self._fixture(td)
            out = _run_main({"transcript_path": turn_a_path})
            self.assertEqual(out, "")

    def test_previous_turn_tool_use_is_not_evidence(self):
        """The same Edit now sits in the PREVIOUS turn (a real user message intervenes) -- it
        must NOT count as evidence for the new turn's claim."""
        with tempfile.TemporaryDirectory() as td:
            _, turn_b_path = self._fixture(td)
            out = _run_main({"transcript_path": turn_b_path})
            payload = json.loads(out)
            self.assertEqual(payload["decision"], "block")


class DetectorCasesStillPass(unittest.TestCase):
    """Smoke test: the hook's own CASES table (>=12 cases, both block and every exclusion)
    still passes end to end, so a change to one path can't silently break the other."""

    def test_selftest_returns_zero(self):
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            code = gc._selftest()
        self.assertEqual(code, 0, captured.getvalue())


if __name__ == "__main__":
    unittest.main()
