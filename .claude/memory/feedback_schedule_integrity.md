---
name: feedback_schedule_integrity
description: Why every logged result is proactively re-slotted (due-within-7d sweep) and every out-of-order attempt fixes both sides of the swap — the close-the-loop scheduling why
metadata:
  type: feedback
reconciled: 2026-09-11
---

**Operational rule lives in the skill** — `references/review-workflow.md` (Schedule integrity) +
`references/weekly-build.md` (the tracker sweep), and it is partly hook-enforced
(`scripts/check_schedule_integrity.py`, pre-commit). This file is the *why*. Merges the former
`proactive_scheduling` and `schedule_mistakes`. (`schedule_markdown` stays separate — a rendering gotcha,
different concern.)

## Proactively slot what's coming due

After logging any result, scan `dsa_progress.md` for problems whose next-review date falls within 7 days
and slot them into the schedule **in the same edit** — don't wait for the learner to notice. At close-out,
present a brief due-date summary (everything due within 7 days, grouped by day). *Why:* the learner had to
point out that 33 and 994 were due Thu/Fri but weren't scheduled — the loop should close itself.

## Fix both sides of an out-of-order swap

When logging, cross-check the problem against today's schedule. If it was done early or from the wrong day,
**detect the displaced problem and re-slot it in the same edit** — mark the right day done, give the
displaced rep a new slot. *Why:* the learner did 355 (Thu's block) on Wednesday instead of 621 (Wed's
block) and had to flag it after the fact. Cases: did tomorrow's block today → move today's to tomorrow;
did a future problem early → move its schedule entry to today (the tracker attempt date is source of truth,
but the schedule should reflect the day it was actually done).

**The governing invariant** (normative in review-workflow.md): a problem dropped or deferred gets a new
specific slot in the **same edit** — a deferred problem with no new date is a missed problem. Related:
[[feedback_lineup_links_only]] (a re-slotted board is still name+links-only), [[feedback_operating_principles]] P1.

2026-10-06: a due row may now also be seated by the schedule's carried section (proven rows only); the `scheduling` skill holds the carry rule.
