---
name: feedback_phase_progression
description: How a phase closes (per algorithm on recognition + execution, not per problem), that phase dates are checkpoints not deadlines, and that a 🔴 on an un-taught technique is phase-gated not churned
metadata:
  type: feedback
reconciled: 2026-09-11
---

**Operational surfaces** — `references/technique-coverage.md` (phase-exit `no-green` blocker list) and
`references/weekly-build.md` (queue-trigger audit each build). This file is the *why*. Merges the former
`phase_exit_per_algorithm` (anchor), `phase_dates_are_advisory`, `phase_gated_blanks`.

## Phase exit is judged per ALGORITHM, on two axes (Jul 26, 2026)

At phase close every **algorithm** in the phase clears **both**: **recognition** (shape → algorithm +
picking feature, cold, label-stripped — a clean cold cue, no unresolved trigger in
`recognition_gotchas.md`) and **execution** (**≥1 problem for that algorithm at 🟢**, coded). Recognition
without execution is knowing a name; execution without recognition is a solution waiting to be told its
problem — the interview grades the first in two minutes and the second for thirty.

*Why this replaces "every problem 🎓 Graduated":* 🎓 needs `graduate_at_streak` coded 🟢s + the long
interval → 90+ days/problem, against a ~3–5 week phase — unmeetable by construction, so it was ignored, and
an ignored gate is worse than a loose one. **Tolerance:** a lingering 🟡 on the 2nd/3rd problem of an
algorithm that already has a 🟢 is fine; **an algorithm with zero 🟢s, or an unresolved recognition trigger,
is not** — that's unlearned, not a rough edge. Report **per algorithm** at close (eleven healthy-looking
problems can hide one entirely-unlearned algorithm), and **schedule anything carried out in the same
breath** (a carried gap that isn't slotted is a forgotten one). Pairs with [[feedback_consolidation_reps]]
(one problem can't establish recognition).

## Phase dates are checkpoints, not deadlines (Aug 5, 2026)

An unfinished phase **carries forward** — a normal outcome, not a failure state (*"if we are not finished,
it is what it is, we keep trucking along"* — set when 0 of 5 Advanced Graphs algorithms had a 🟢 eleven
days out). The exit criteria above still hold; the *date* is not the thing they must be met by. *Why:* the
comfort→interval engine already decides when something is learned; a calendar can't know whether
Bellman-Ford stuck, the tracker can. **Never frame a date as a countdown or "closes on an unproven phase"**
— report *which algorithms have no 🟢* and let the state drive. A slipped phase **does not** raise the
effort ceiling, license intake against negative surplus ([[feedback_intake_and_surplus]]), or make a
protected rep movable — running long is a reason to keep intake *low*, never to cram. Keep reporting the
blunt honest state; just drop the deadline framing. Applies to every phase, both tracks (DSA and SD).
Related: [[feedback_gate_on_internal_state]] (triggers read from the repo, never a calendar/job event),
[[feedback_let_learner_pace]].

## A 🔴 on an un-taught technique is phase-gated, not churned

Before treating an overdue 🔴 as urgent, check whether its **technique has been taught** (its
`study_guide.md` phase has happened). A Blank with no foundation is a **premature attempt**, not a
forgetting — the Blank-interval loop assumes forgetting, so retrying just re-blanks it and churns forever
while inflating the backlog signal (Jul 12 audit: "5 urgent 🔴s" was really 3; two were premature
Backtracking/DP attempts). **Phase-gate it:** move the row into the Knowledge Expansion Queue with an
explicit trigger; do NOT just set a far-future `Next Review Date` (the script recomputes it to
`latest_attempt + interval` and it snaps back). Check for orphans (a technique in no phase — e.g. 912 Merge
Sort — either park or close as a one-off). Same trigger mechanism as [[feedback_method_variant_promotion]].

⚠️ **Audit the queue's triggers at every weekly build, and prefer CONDITIONS to dates.** A date-based
trigger can fire and be missed **silently** — a parked item and a missed item look identical (Jul 26: 53
D&C carried "active block week of Jul 6" and sat three weeks past, unfired, with an abandoned stub). Prefer
*"when 42 graduates"*, *"when Backtracking opens"*, *"once surplus ≥ 1"* — a condition can't silently
expire; **when re-triggering a missed item, replace the date with a condition**, or the same failure
recurs. (This is exactly the trap `project_familiarity_engine_revisit`'s expired Sep-7 date fell into.)
