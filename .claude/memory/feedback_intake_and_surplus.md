---
name: feedback_intake_and_surplus
description: Why review demand is a rate priced in units (not a headcount), how surplus gates pulls/intake, why new intake is difficulty-tiered (the blank tax), and why an early completion asks before backfilling
metadata:
  type: feedback
reconciled: 2026-09-11
---

**Operational surfaces** — `references/effort-budget.md` (the unit model, the script),
`references/weekly-build.md` (surplus at the build, fill order), `references/technique-coverage.md`
(weak-technique fill). This file is the *why* + the derivation. Merges the former
`surplus_triggered_intake` (anchor), `difficulty_tiered_intake`, `early_completion_backfill`.

## Review demand is a RATE, priced in units — gate on it, never on a date

<!-- single-source-ok: DERIVATION — the intervals are inputs to `1 / interval`, not restated config values. -->
Each tracked row generates `1 / interval` reps/day: 🔴 +2 → 0.50/day · 🟡 +10 → 0.10 · 🟢 s1 → 0.033 ·
🟢 s2 → 0.017 · 🎓 → 0.006. **A graduated problem generates ~1/83rd the load of a Blank** — retirement
removes a problem from the schedule, it doesn't just relabel it. **Capacity is UNITS, not problem-slots
(Aug 7).** Don't hand-compute — `scripts/effort_budget.py` sums this demand and prices it against the
config ceiling.

**The finding:** the hole opens **after** NC150. During the roadmap, new intake feeds streak-1 rows at a
heavy rate and demand tracks capacity; when intake stops and the population matures, demand falls to ~75%
idle by late 2027. So a shrinking review list is **the intervals doing their job**, not being ahead — it
means capacity needs redirecting. The stale-🟢 backlog is **arithmetic, not neglect**: diligence can't
drain it while demand exceeds capacity.

**How to apply:** at every build run the script *before* slotting; **gate pulls and extra intake on the
surplus number, never on a date** (supersedes "no pulls until NC150 done" — correct only while
over-subscribed). Fill order: ≤0 → reviews only · 1–5 → consolidation reps · 6–12 → + application pulls ·
13+ → + open Tier 1 early. ⚠️ **The surplus measures the WEEK, not the DAY — an aggregate is not a
schedule.** A negative-surplus week still holds under-ceiling days (SD slot + doubled warmups land
unevenly); slipping reviews off a week with slack days is a false shortage that costs real reps (Jul 27: a
−7.3 build slipped 12 🟢 while Wed held 1 and Sun held 2; four came straight back). Under-ceiling days
absorb items back, preferring ones already due that day.

⚠️ **Fill under-ceiling days with weak-technique coverage before deferring it (Aug 23).** Priority:
**zero-green conversions & their siblings > thin-green fills > backlog** (the `technique_comfort_audit`
"Needs work" order, applied to filling capacity). Prefer a **new sibling** over pulling an existing review
forward (trains transfer, adds a 🟢 path, no interval shortening); pull a review forward only when the
sibling is a variant on that same problem. The ≤2/wk consolidation cap may flex up **when the tracker is
under-subscribed** and the intake targets zero-green/thin techniques — still respect the per-day ceiling and
the blank tax. See `decisions.yml` `fill-capacity-with-weak-coverage`.

## New intake is difficulty-tiered — the blank tax

Intake is tiered, not a flat 5/week: moderate categories 4–5, hard/algorithm-dense (Advanced Graphs,
Backtracking) **4**, DP **3**. *Why:* a hard-category new problem introduces a new algorithm, so the first
attempt almost always logs 🔴, and each 🔴 spawns a +2 retry eating a warmup slot — empirically ~3 slots
over the first fortnight, not 1. At 5/week that cascade starves the backlog (Jul 14, after Advanced Graphs,
mis-bucketed as moderate, produced back-to-back 🔴 on 743 + 787 in one week). **SSOT = the "🎚️ Category
Difficulty Tiers" table in `study_guide.md`** — read it at each build, cap that phase's intake at its row,
route freed active-block slots to coded backlog. A category earns a harder tier when its new problems
consistently log 🔴 on first exposure.

## An early completion asks before backfilling

When a scheduled problem is finished **early**, mark it done on the actual day and strike its future slot
([[feedback_schedule_integrity]]). If striking it drops that future day **below its effort floor** (read
from `cse.config.yml effort_budget:` / the script — this step named a bare "5" until Aug 30, the exact
restated-value drift `check_single_source.py` catches), **ask** whether to backfill — don't silently leave
the day short or silently fill it. On yes, pull the highest-priority due item (🔴 > 🟡 > 🟢 > 🎓, favoring
the overdue-🟢 burn-down) and re-slot in the same edit. *Why:* the day's budget has a floor as well as a
ceiling, but what to backfill (or whether to bank the lighter day) is the learner's call.

Related: [[feedback_consolidation_reps]], [[feedback_phase_progression]], [[feedback_recognition_probes]]
(the probe is the release valve when intake caps bind — it costs no permanent demand).

2026-10-06: intake is now `effort_budget.intake_per_week` with an unproven-overdue backstop; the `scheduling` skill and `decisions.yml` `intake-rate-and-backstop-oct6` supersede the per-tier counts.
