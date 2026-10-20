"""Tests for check_timeline_gaps.py — the timeline-gap reconstruction report.

Stdlib unittest, no filesystem access (see test_gamify.py's docstring for why that
matters in this repo). classify_gaps() is pure: it takes the same rows/sched shapes as
gamify.build_problems() and never reads a file itself.

    python scripts/test_check_timeline_gaps.py
"""
from __future__ import annotations

import unittest

import check_timeline_gaps as ctg


def _row(num, comfort, streak, diff="Medium", due="2026-12-01", reps=""):
    return {"num": str(num), "title": f"P{num}", "diff": diff, "comfort": comfort,
            "streak": streak, "due": due, "reps": reps}


class ClassifyGapsTests(unittest.TestCase):
    def test_rep_with_schedule_end_glyph_is_not_a_gap(self):
        rows = [_row(763, "🟡", 0, reps="2026-09-09, 2026-09-19")]
        sched = {"2026-09-09": {763: "🔴"}, "2026-09-19": {763: "🟡"}}
        gaps, counts = ctg.classify_gaps(rows, sched)
        self.assertEqual(gaps, [])
        self.assertEqual(counts["reconstructed"], 2)
        self.assertEqual(counts["gaps"], 0)

    def test_single_variant_rep_with_no_schedule_entry_is_a_gap(self):
        # Two reps; the FIRST (pre-archive, 2026-04-23) has no matching schedule entry
        # anywhere — a real, fixable gap. The last point always anchors to the tracker's
        # current comfort (build_problems' own fallback), so it's deliberately given a
        # date that DOES have a schedule entry — the gap must show up on the first rep,
        # never masked by the anchor.
        rows = [_row(206, "🎓", 3, reps="2026-04-23, 2026-09-19")]
        sched = {"2026-09-19": {206: "🎓"}}   # 2026-04-23 has no entry
        gaps, counts = ctg.classify_gaps(rows, sched)
        self.assertEqual(len(gaps), 1)
        self.assertEqual(gaps[0]["lcNumber"], 206)
        self.assertEqual(gaps[0]["dates"], ["2026-04-23"])
        self.assertEqual(counts["gaps"], 1)
        self.assertEqual(counts["expectedNull"], 0)

    def test_multi_variant_null_is_expected_not_a_gap(self):
        # Two rows share number 21 (method variants — Recursion vs Iterative). Every
        # non-final point degrades to null regardless of whether a schedule entry
        # exists (gamify.build_problems' own guard against fabricating which variant a
        # rep belonged to) — that is EXPECTED, not a fixable gap.
        rows = [_row(21, "🎓", 3, reps="2026-08-01, 2026-09-19"),
                _row(21, "🟢", 1, reps="2026-08-01, 2026-09-19")]
        sched = {"2026-08-01": {21: "🟡"}, "2026-09-19": {21: "🎓"}}
        gaps, counts = ctg.classify_gaps(rows, sched)
        self.assertEqual(gaps, [])
        self.assertEqual(counts["expectedNull"], 2)   # the two rows' first points
        self.assertEqual(counts["gaps"], 0)


if __name__ == "__main__":
    unittest.main()
