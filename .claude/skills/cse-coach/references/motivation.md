<!-- reconciled: 2026-10-19 -->
# Motivation & progress — surfacing the journey honestly

**Open this** at a *celebration moment*: session start, when a real milestone lands (a graduation,
a retirement, a streak threshold), and at the weekly close-out. **Not for** manufacturing hype
mid-rep — progress is surfaced *around* the work, never during the rating.

## The one rule: celebrate what was **earned**, never nudge for a badge

Every progress signal here is computed from records that already exist and keys off a
**genuine, unfakeable event**. A graduation is three cold cleans across spaced intervals; a
retirement is a graduated problem clearing its spot checks; a streak is showing up. **Never** let
a badge or streak leak into a rating. You still infer comfort from the session and flag a dishonest
🟢 exactly as before (`review-workflow.md`, [[feedback_infer_comfort]]). The gamification exists to
make honest progress *visible*, not to buy a rep. If celebrating a milestone would tempt the
learner toward a soft 🟢 to keep a streak alive, say the honest thing. The streak survives a 🟡, a
rep happened.

## What is real progress here (and what is not)

The dashboard reads `progress.json` (emitted by `scripts/gamify.py`); the site renders it. The
signals, in order of what "on track" means for spaced repetition:

- **Study-day streak** — consistency, the precondition for SR working. **SR-honest**: it rewards
  practicing *when due*, with a bank of streak freezes (`gamification.streak_freeze_max` and
  `gamification.streak_freeze_earn_every` in `cse.config.yml`): a missed day spends a freeze, study
  days earn them back, a gap longer than the bank breaks the run. It never pushes daily grinding
  against the effort budget.
- **The maturation pipeline** 🔴→🟡→🟢→🎓→🏆 and the **trophy case** (🎓 + 🏆) — the system's whole
  purpose is problems maturing up this ladder. This, not row count, is the accomplishment record.
- **Technique coverage** — breadth toward interview-technique mastery.
- **On-schedule health** — are due reviews being cleared; the SR-specific "keeping up" gauge.

⚠️ **Row count is still not progress** (`project_library_carrying_capacity`) — a *shrinking* tracker
is healthy. Report the pipeline and the trophy case, never "N problems in the tracker."

## When to surface it

| Moment | Do |
|---|---|
| **Session start** | the SessionStart hook already injects a one-line PROGRESS banner (streak + trophies + dashboard link). Acknowledge it warmly in a sentence if it is notable; don't recompute or expand it. |
| **A milestone lands this rep** (a graduation, a retirement, a streak threshold crossed, a comeback) | one genuine, specific line: *what* was earned and *why it counts*. Deliver it in the coach's warm voice, not gushing, not a checklist. |
| **Weekly close-out** (`weekly-build.md`) | note the week's pipeline movement (what converted, what graduated) as part of the close-out. |

## Mechanics

- The numbers are computed, never hand-tallied: `python scripts/gamify.py` writes `progress.json`.
  The pre-commit hook does this automatically when a rep lands. `--banner` prints the one-line
  summary; `--validate` checks it without writing.
- Tuned thresholds (the streak-freeze bank size and earn rate, milestone lengths) live **only** in
  `cse.config.yml` `gamification:` — name the key, never restate the number here.
- The dashboard lives at `progressiveoverflow.com/progress`. By default it uses its own repo; pass
  `?repo=owner/name` for any public cse-coach repo. Decision:
  `gamification-progress-platform` (`decisions.yml`).
