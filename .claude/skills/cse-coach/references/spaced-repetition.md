<!-- reconciled: 2026-09-25 -->
# Comfort-based spaced repetition — the ladder

**Open this** before proposing a comfort rating or reasoning about a next-review interval.
**Not for** the day's total load (that's `effort-budget.md`). **Not for** hand-computing dates
— run `python scripts/update_review_dates.py`, which computes every date from the config.

**All interval values live** in [`cse.config.yml`](cse.config.yml) under `intervals:`. Read
them there or run the script; never restate a number here (single-source rule).

## The ladder (the part that does not change)

| Comfort | Next review |
|---------|-------------|
| 🟢 Clean — **provisional** (Streak 0: first Clean directly after a 🔴 Blank) | shortest Clean interval — a lock-down check |
| 🟢 Clean — Streak 1 | longer |
| 🟢 Clean — Streak 2 | longer still |
| 🎓 Graduated (`graduate_at_streak`+) | longest — a recurring spot check |
| 🟡 Shaky | short |
| 🔴 Blank | shortest of all |

## Rating each rep

- **🟢 Clean** — coded from a blank page, no hints. Second-guessing the data structure or
  peeking → Shaky. A no-code blueprint caps at Shaky (coding required); the sole exception is
  a flawless spot check confirming an already-🎓 problem. **The rating ignores Big-O**
  — a complexity miss never lowers or caps it (`review-workflow.md` §1).
- **🟡 Shaky** — got there but needed a nudge, peeked, or wasn't fully confident mid-approach.
- **🔴 Blank** — couldn't recall the approach; had to look it up.

Infer the rating from the session and **propose it for confirmation** (review-workflow.md step
4); the learner's call is final, but flag a dishonest 🟢.

## Provisional Clean (added Jul 18, 2026)

A 🟢 that *directly follows a 🔴* is logged with **Streak 0** (not 1). It earns only a
lock-down interval to verify the Blank→Clean stuck, before the normal Streak-1 one. Survives
(Clean again) → log Streak 1; slips → resets as usual. **Only Blank→Clean is provisional** — a
🟢 after a 🟡 is a normal Streak-1 Clean. Rationale: one Clean right after a Blank may be recall
of fresh teaching, not durable retention (same logic as the teach/measure split).

⚠️ **Headroom resting on a provisional 🟢 is contingent, not banked** — a slip at the lock-down
swings demand back. Spend it only on deferrable work, never permanent new demand (see
`effort-budget.md`).

full rule: `cse.config.yml` `intervals:`; `decisions.yml` `graduate-then-retire`,
`rating-ignores-complexity`;
[`feedback_provisional_clean.md`](.claude/memory/feedback_provisional_clean.md),
[`feedback_infer_comfort.md`](.claude/memory/feedback_infer_comfort.md).
