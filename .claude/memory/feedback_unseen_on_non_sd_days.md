---
name: feedback-unseen-on-non-sd-days
description: Standing rule — every day with no SD slot must carry at least one unseen problem (new intake or a recognition probe)
metadata:
  type: feedback
reconciled: 2026-09-11
---

**Operational rule lives in the skill** — `references/weekly-build.md` (every non-SD day carries ≥1 unseen
problem, placed before backlog). This file is the *why* + the build judgement.

**Set by the learner Aug 9, 2026:** *"I want to always have new or probe problems on days that have no
system design. problems that i have seen more than twice will always be a bit more lenient on me."*

## The rule

**Every day without an SD slot carries at least one *unseen* problem** — either **new intake** from
the current study-guide phase, or a **recognition probe** ([[project_recognition_probes]]). Either
satisfies it; they are interchangeable for this purpose.

⚠️ **The exemption's original basis is GONE (Aug 16, 2026) — re-derive the target, don't assume 4.**
This rule was written when an SD day was **priced at 3.0 units against the day**, so an SD day was
mechanically full and carrying no unseen problem followed from arithmetic. SD is now **off-board and
unpriced**: the whole ceiling was lowered instead, which charges the SD evening **once on every day**
rather than only on SD days. On a literal reading **all seven days now qualify**.

That is not a licence to schedule seven — it means the number is **a judgement made at the build from
that week's actual arithmetic, and stated**. The Aug 17 build is the worked example: it found all seven
qualifying, delivered **3**, and wrote down which four days could not take one and why (three were 100%
due reviews at the ceiling; the fourth would have displaced the oldest slip). **Short is fine; silent
is not.** The old `three_weekly` figure of 4/week survives only as a baseline to measure against.

## Why — the learner's reason, which is the right one

**A problem seen three or more times is a lenient test.** By then the rep measures retention of *that
problem's solution*, not the technique — the shape is familiar, the trap is remembered, and the tracker
row even names the method. It still has value as decay insurance, but its **diagnostic** value has
collapsed. An unseen problem is the only thing that tests recognition and transfer, which is exactly what
an interview grades in its first two minutes.

This is the same argument that produced the probe ([[feedback_recognition_gate]]): the board is ~100%
retries, and a retry half-spoils itself. The rule generalises it from *"one probe a week"* to *"no day
of pure review unless SD is doing the hard work instead."*

## How to apply at the weekly build

1. Mark the SD days first — the Sunday **mock** and, when the probe bank is non-empty, the midweek
   **deep-dive round**. (This once read "lanes ①/②/③"; the three-lane model was retired Aug 13, 2026.)
2. **Every remaining day gets an unseen problem before any 🟢 backlog is placed.**
3. Prefer **new intake from the active phase** — it is time-boxed and does not get done later for free.
   Fall back to a **probe** when phase intake is capped or exhausted.
4. Only then fill remaining units with due reviews and the 🟢 backlog.

⚠️ **The intake caps still bind.** Difficulty-tiered intake ([[feedback_intake_and_surplus]]) is
moderate 5 / hard 4 / DP 3 per week. **The probe is the release valve**: in a DP phase capped at 3, the
fourth non-SD day takes a probe, not a fourth new problem. A probe costs no permanent demand (no tracker
row on 🟢), so it never fights the cap.

## ⚠️ What this costs, and why it is still right

**Unseen problems and the 🟢 backlog burn-down compete for the same units.** On the Aug 10 build, buying
6.5 units of intake pushed the slip list from 4 rows to 9.

Take the trade. **A 🟢 untouched for three months came back clean** — all 8 of the Apr–May block, swept
Aug 5–7, none slipped — so the backlog is **not decaying on the timeline the tracker implies**. Phase
progress *is* time-boxed. **The axis is deferrable vs. not-deferrable, not old vs. new.**

## The failure this was catching

The learner asked *"how come we don't have any new problems this week?"* and the answer exposed that the
**`Sliding Window (finish) + Stack` phase had been open since Aug 3 with zero problems in the tracker** —
a week into a three-week phase, invisible because the board looked full of legitimate review work.
**Nothing in the repo flags an active phase with no reps.** This rule is the structural fix: a day that
cannot be filled with an unseen problem forces the question *"why is there nothing new to pull?"* at
build time, instead of a month later.

2026-10-06: superseded by `effort_budget.intake_per_week` (decision `intake-rate-and-backstop-oct6`); the per-day unseen rule no longer binds.
