# DSA Progress

<!--
Notes for the coach / future agents:
- Columns: Difficulty, Problem, Comfort, Streak, Next Review Date, Latest Rep Date, Rep Dates.
- ⚠️ Renamed "Attempt" -> "Rep" (header stat + both date columns). update_review_dates.py still
  RECOGNIZES the older spellings and upgrades whichever it finds, so an un-migrated tracker parses
  fine. The in-file `# ── Attempt · <date> ──` banners in solution files were deliberately NOT renamed.
- `Streak` = consecutive Clean results. Increments on Clean; resets to 0 on Shaky or Blank.
- `Next Review Date` is COMPUTED from Comfort + Streak by scripts/update_review_dates.py
  (intervals come from cse.config.yml; defaults: Clean s1 +30, s2 +60, Retired +180,
  Shaky +10, Blank +2). Do not hand-edit it — edit Comfort/Streak and re-run the script.
- At Streak == graduate_at_streak (default 3), change Comfort to 🎓 to graduate the problem.
  Retired problems return for a spot check every 180 days.
- 🏆 GRADUATION — the tier above 🎓. A 🎓 problem passing TWO consecutive 180-day spot checks
  leaves this table for a plain-list `## 🏆 Retired` section: no interval, no ongoing cost.
  Why: even at +180 a row bills ~0.039 slots/week FOREVER, so without a release valve the
  library caps out around 500–600 problems. Re-enters at 🟡 if it resurfaces and fails.
- DISPOSABLE REPS — not every solved problem earns a row. A consolidation rep or an
  application pull is a probe testing whether a TECHNIQUE transfers, not an asset to maintain:
  log the outcome to the technique's ledger (mastery/recognition_gotchas.md,
  mastery/complexity_gotchas.md) and create NO row if it came back 🟢. Only 🟡/🔴 earns a row.
- ⚠️ BOTH of the above need a `discovery_skip` entry (or, for probes, a root outside
  solutions.roots). Discovery re-adds any problem it finds without a row, so deleting a row
  alone silently resurrects it on the next commit. Keep the Graduated list a PLAIN BULLET
  LIST — never this 7-column table — or the parser picks it back up.
- WHAT THIS FILE MEANS: "everything still unproven" — a work queue, not a trophy case. A
  shrinking row count is the healthy direction; don't report row count as progress. The
  accomplishment record is the 🏆 list plus the technique ledgers.
- The script also auto-discovers solution files under the configured roots
  (cse.config.yml → solutions.roots/globs) and adds missing rows.
- Titles should include the method when relevant, e.g. `(BFS)` / `(DFS)`; a same-number
  problem solved by a different method gets a NEW row, not an overwrite.
- The pre-commit hook runs the script when this file or a solution file is staged.
  Manual run: `python scripts/update_review_dates.py`.
- Replace the example row below with your own once you log your first problem.
-->

> **0** problems &nbsp;·&nbsp; **0** solutions &nbsp;·&nbsp; **0** reps

| | 🏆 Retired | 🎓 Graduated | 🟢 Clean | 🟡 Shaky | 🔴 Blank |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Solutions** | 0 | 0 | 0 | 0 | 0 |

| Difficulty | Problem | Comfort | Streak | Next Review Date | Latest Rep Date | Rep Dates |
|---|---|---|---|---|---|---|
| Easy | [1. Two Sum](https://leetcode.com/problems/two-sum/) | 🔴 | 0 |  |  |  |

## Knowledge Expansion Queue

Problems for algorithmic depth — not part of the spaced-repetition stats. These enter the schedule when the relevant topic arrives. (Populated as you cross into the expansion tiers; see `../study_guide.md` and `../../../curriculum/`.)
