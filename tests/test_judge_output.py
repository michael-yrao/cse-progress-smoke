"""Tests for scripts/judge_output.py — the LLM output-quality judge.

Stdlib unittest on purpose (this engine has no pytest dependency of its own). Runnable
two ways:

    python tests/test_judge_output.py
    python -m pytest tests/test_judge_output.py -q

Covers: transcript turn-splitting at real user-message boundaries (with a sidechain
entry that must be skipped), rubric loading + placeholder substitution, the
DEFAULT_CONFIG fallback announcing itself, a mocked Messages-API round trip, an
unparseable reply, and the `--check` exit-code contract. No test makes a real network
call.
"""
from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import judge_output as jo  # noqa: E402

REPO = Path(__file__).resolve().parents[1]


def _entry(**kwargs) -> str:
    return json.dumps(kwargs)


def _write_transcript(lines: list[dict]) -> Path:
    fh = tempfile.NamedTemporaryFile(
        mode="w", suffix=".jsonl", delete=False, encoding="utf-8"
    )
    for line in lines:
        fh.write(json.dumps(line) + "\n")
    fh.close()
    return Path(fh.name)


class TurnSplittingTests(unittest.TestCase):
    def test_boundary_evidence_and_sidechain_skip(self):
        long_result = "x" * 250  # longer than TOOL_RESULT_EXCERPT_CHARS
        lines = [
            {"type": "user", "message": {"role": "user", "content": "Start today"}},
            {
                "type": "assistant",
                "message": {"role": "assistant", "content": [{"type": "text", "text": "Here is your board:"}]},
            },
            {
                "type": "assistant",
                "message": {"role": "assistant", "content": [{"type": "tool_use", "name": "Read", "id": "t1"}]},
            },
            {
                "type": "user",
                "message": {
                    "role": "user",
                    "content": [{"type": "tool_result", "tool_use_id": "t1", "content": long_result}],
                },
            },
            {
                "type": "assistant",
                "message": {"role": "assistant", "content": [{"type": "text", "text": "Final answer."}]},
            },
            {
                "type": "assistant",
                "isSidechain": True,
                "message": {"role": "assistant", "content": [{"type": "text", "text": "SUBAGENT NOISE"}]},
            },
            {"type": "user", "message": {"role": "user", "content": "thanks, next"}},
            {
                "type": "assistant",
                "message": {"role": "assistant", "content": [{"type": "text", "text": "Second turn text."}]},
            },
        ]
        path = _write_transcript(lines)
        try:
            turns = jo.load_transcript_turns(path)
        finally:
            path.unlink()

        self.assertEqual(len(turns), 2)
        self.assertEqual(turns[0]["text"], "Here is your board:\nFinal answer.")
        self.assertNotIn("SUBAGENT NOISE", turns[0]["text"])
        self.assertEqual(turns[0]["tool_uses"], ["Read"])
        self.assertEqual(turns[0]["tool_results"], [long_result[: jo.TOOL_RESULT_EXCERPT_CHARS]])
        self.assertEqual(turns[1]["text"], "Second turn text.")
        self.assertEqual(turns[1]["tool_uses"], [])

    def test_turns_flag_keeps_only_the_last_n(self):
        lines = [{"type": "user", "message": {"role": "user", "content": "go"}}]
        for i in range(3):
            lines.append(
                {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": f"t{i}"}]}}
            )
            lines.append({"type": "user", "message": {"role": "user", "content": "next"}})
        path = _write_transcript(lines)
        try:
            turns = jo.load_transcript_turns(path)
        finally:
            path.unlink()
        self.assertEqual([t["text"] for t in turns[-2:]], ["t1", "t2"])

    def test_missing_transcript_returns_no_turns(self):
        self.assertEqual(jo.load_transcript_turns(Path("does/not/exist.jsonl")), [])


class RubricLoadingTests(unittest.TestCase):
    def test_rubric_file_loads_and_substitutes_placeholder(self):
        text = jo.load_rubric()
        self.assertIn("{max_sentence_words}", text)
        substituted = text.replace("{max_sentence_words}", "20")
        self.assertNotIn("{max_sentence_words}", substituted)
        self.assertIn("20 words", substituted)

    def test_rubric_carries_no_config_values(self):
        text = jo.load_rubric()
        # The pass_threshold and judge_model must never be copied into the rubric —
        # only the readability placeholder is a config value.
        self.assertNotIn("0.75", text)
        self.assertNotIn("claude-sonnet-5", text)


class ConfigFallbackTests(unittest.TestCase):
    def _run_with_config(self, yaml_text: str | None) -> tuple[dict, str]:
        fh = tempfile.NamedTemporaryFile(
            mode="w", suffix=".yml", delete=False, encoding="utf-8"
        )
        if yaml_text is not None:
            fh.write(yaml_text)
        fh.close()
        buf = io.StringIO()
        with mock.patch.object(jo, "CONFIG", Path(fh.name)):
            with redirect_stdout(buf):
                cfg = jo.load_config()
        Path(fh.name).unlink()
        return cfg, buf.getvalue()

    def test_missing_block_announces_every_key(self):
        cfg, out = self._run_with_config("gamification:\n  on_schedule_target: 0.9\n")
        self.assertEqual(cfg, jo.DEFAULT_CONFIG)
        for key in jo.DEFAULT_CONFIG:
            self.assertIn(key, out, f"expected a fallback announcement naming {key!r}")

    def test_partial_block_only_announces_missing_keys(self):
        cfg, out = self._run_with_config(
            "output_quality:\n  judge_model: claude-custom-9\n"
        )
        self.assertEqual(cfg["judge_model"], "claude-custom-9")
        self.assertNotIn("output_quality.judge_model", out)
        self.assertIn("pass_threshold", out)
        self.assertIn("max_sentence_words", out)

    def test_full_block_announces_nothing(self):
        cfg, out = self._run_with_config(
            "output_quality:\n"
            "  judge_model: claude-sonnet-5\n"
            "  pass_threshold: 0.8\n"
            "  readability:\n"
            "    max_sentence_words: 18\n"
        )
        self.assertEqual(cfg["pass_threshold"], 0.8)
        self.assertEqual(cfg["max_sentence_words"], 18)
        self.assertEqual(out, "")


class _FakeResponse:
    def __init__(self, body: bytes) -> None:
        self._body = body

    def read(self) -> bytes:
        return self._body

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, *exc) -> None:
        return None


def _messages_payload(reply_text: str) -> bytes:
    return json.dumps({"content": [{"type": "text", "text": reply_text}]}).encode("utf-8")


class JudgeRoundTripTests(unittest.TestCase):
    def test_call_judge_parses_a_clean_verdict(self):
        verdict = {
            "moment": "answer to a question",
            "f1": {"precision": 1.0, "recall": 0.5, "f1": 0.67},
            "groundedness": 2,
            "narrative": 2,
            "readability": 1,
            "notes": ["one long sentence"],
        }
        reply = "Here is my grading.\n" + json.dumps(verdict) + "\nDone."
        with mock.patch.object(jo.urllib.request, "urlopen", return_value=_FakeResponse(_messages_payload(reply))):
            score = jo.call_judge("prompt", "claude-sonnet-5", "sk-test", 0)
        self.assertEqual(score["moment"], "answer to a question")
        self.assertAlmostEqual(score["f1"]["f1"], 0.67)
        self.assertEqual(score["groundedness"], 2.0)
        self.assertEqual(score["notes"], ["one long sentence"])

    def test_unparseable_reply_scores_zero_with_a_note(self):
        with mock.patch.object(
            jo.urllib.request, "urlopen", return_value=_FakeResponse(_messages_payload("not json at all"))
        ):
            score = jo.call_judge("prompt", "claude-sonnet-5", "sk-test", 0)
        self.assertEqual(score["notes"], ["unparseable"])
        self.assertEqual(score["f1"], {"precision": 0.0, "recall": 0.0, "f1": 0.0})
        self.assertEqual(score["groundedness"], 0.0)

    def test_dry_run_never_calls_urlopen(self):
        lines = [
            {"type": "user", "message": {"role": "user", "content": "go"}},
            {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": "hi"}]}},
        ]
        path = _write_transcript(lines)
        argv = ["judge_output.py", str(path), "--dry-run"]
        try:
            with mock.patch.object(jo.urllib.request, "urlopen") as urlopen_mock:
                with mock.patch.object(sys, "argv", argv):
                    buf = io.StringIO()
                    with redirect_stdout(buf):
                        jo.main()
                urlopen_mock.assert_not_called()
        finally:
            path.unlink()
        self.assertIn("Return JSON only", buf.getvalue())


class CheckExitCodeTests(unittest.TestCase):
    def _run_main(self, argv: list[str], score: dict) -> int:
        with mock.patch.object(jo, "call_judge", side_effect=lambda *a, **k: score):
            with mock.patch.dict("os.environ", {"ANTHROPIC_API_KEY": "sk-test"}):
                with redirect_stdout(io.StringIO()):
                    with self.assertRaises(SystemExit) as ctx:
                        with mock.patch.object(sys, "argv", argv):
                            jo.main()
        return ctx.exception.code

    def test_check_exits_1_below_threshold(self):
        lines = [
            {"type": "user", "message": {"role": "user", "content": "go"}},
            {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": "hi"}]}},
        ]
        path = _write_transcript(lines)
        low_score = jo._zero_score("answer to a question", [])
        argv = ["judge_output.py", str(path), "--check"]
        try:
            code = self._run_main(argv, low_score)
        finally:
            path.unlink()
        self.assertEqual(code, 1)

    def test_check_exits_0_at_or_above_threshold(self):
        lines = [
            {"type": "user", "message": {"role": "user", "content": "go"}},
            {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": "hi"}]}},
        ]
        path = _write_transcript(lines)
        perfect_score = {
            "moment": "answer to a question",
            "f1": {"precision": 1.0, "recall": 1.0, "f1": 1.0},
            "groundedness": 2.0,
            "narrative": 2.0,
            "readability": 2.0,
            "notes": [],
        }
        argv = ["judge_output.py", str(path), "--check"]
        try:
            code = self._run_main(argv, perfect_score)
        finally:
            path.unlink()
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
