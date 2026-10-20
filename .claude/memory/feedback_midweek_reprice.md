---
name: feedback_midweek_reprice
description: The weekly build's "what does not fit" verdict has a shelf life of about one session — re-run effort_budget.py after logging results and re-seat from the slip list when headroom opens
metadata:
  type: feedback
reconciled: 2026-09-11
---

**Operational rule lives in the skill** — `references/effort-budget.md` (Re-price mid-week). This file is
the *why* + the evidence.

**Set by the learner Aug 17, 2026**, on seeing demand fall by a quarter in one morning: *"that is a
good signal to let us know that we can and should modify the current week's schedule as we progress
throughout the week."*

**The schedule is built once and then read as fixed. Demand is not fixed** — every rated rep changes
it, and a single conversion can move more than a whole day's slack.

## The evidence

| | demand | advisory floor | headroom |
|---|---|---|---|
| Aug 17, before the session | 7.16 u/day (50.1/wk) | **8** = the ceiling | **0** |
| Aug 17, after three reps | 5.58 u/day (39.0/wk) | 6 | **~2 u/day · 17/wk** |

One row did most of it: **853 converting 🔴 → 🟢 took it from 3.5 units/week to 0.7.** The build had
written *"the week is nearly full before anything is added"* and *"there is no slack anywhere"* — both
true when written, both wrong by lunchtime.

## The rule

1. **After logging the day's results, re-run `python scripts/effort_budget.py`.** It is one call.
2. **If headroom opened, re-seat from the slip list — oldest first — in the same edit.** Same
   schedule-integrity discipline as a deferral: the board changes, or the finding did not happen.
3. **Say what changed and why**, so a re-seat is not mistaken for scope creep.

## ⚠️ Two things that do NOT follow

**1. Weekly headroom does not seat an indivisible item.** The daily ceiling is a separate constraint.
On Aug 17 the week gained 17 units of weekly headroom and **84 Largest Rectangle still did not fit**:
it is a single 4.5-unit Hard, every remaining day sat at 7.5–8.0, and the largest spare on any one day
was 0.5. Seating it needs **one day cut to 3.5**, which weekly slack cannot do. *Check the day, not
just the week.*

**2. Headroom resting on a PROVISIONAL 🟢 is contingent, not banked.** `effort_budget.py` prices a
Streak-0 Clean at its short lock-down interval, so the number is honest — but the row has not proved
anything yet. 853 at its lock-down check:

| Outcome | cost |
|---|---|
| holds → 🟢 s1 | 0.23 u/wk |
| stays 🟢 s0 | 0.70 |
| slips 🟡 | 1.40 |
| **slips 🔴** | **10.50** |

So a conversion that has not survived its lock-down can still swing ~10 units/week back. **Spend that
headroom on deferrable work (🟢 backlog, an unseen problem) — never on permanent new demand.**

Pairs with [[feedback_intake_and_surplus]] (surplus is a rate, measured at the build) and
[[feedback_schedule_integrity]]. Related: [[feedback_phase_progression]].

2026-10-06: a mid-week reseat also needs a spare row under `effort_budget.max_rows_per_day`; the `scheduling` skill's Mid-week section is the procedure.
