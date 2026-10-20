---
name: feedback-greedy-conveyor
description: Greedy is a family, not a procedure — lock it down with breadth. Standing conveyor: each time a greedy problem goes 🟢 Clean, pull in ONE new greedy sibling, capped at ~2–3 extra beyond the current sub-track. Source from a company frequency pull, pick for DISTINCT safety-argument flavors
metadata:
  type: feedback
reconciled: 2026-09-09
---

**Set by the learner Sep 9, 2026:** *"greedy is very hard to lock down, each is unique in its own way
but has similar recognition. Can we have higher [more] problems for greedy to make sure i lock it
down"* — and, on timing: *"bring one in each time a greedy problem goes clean."*

**The rule (a conversion-gated conveyor):**
- Each time a greedy problem converts to **🟢 Clean**, pull **one** new greedy sibling into the
  schedule at the next build.
- **Cap at ~2–3 extra** beyond whatever the greedy sub-track already holds — this is breadth to lock
  the technique, not an open-ended stream. When the cap is hit, stop the conveyor.
- **Source from a company frequency pull** (`pull_interview.py --technique Greedy`), not hand-picked
  — [[feedback_consolidation_reps]] / the coverage-sibling-pulled-not-authored rule.

**Why greedy specifically earns a conveyor when one problem is usually enough for recognition:**
Greedy has **no reusable procedure**. What transfers between greedy problems is (1) recognizing a
*local* choice is safe to commit without backtracking, and (2) the **safety/exchange argument** for
*why* — and (2) is bespoke per problem (last-index reach in 763, running-tank-can't-recover in 134,
sort-by-end in 435). "Each is unique but recognition is similar" is the exact signature of a technique
that needs **breadth, not depth on one problem**. So pick siblings for *distinct argument flavors*
(heap-greedy, custom-comparator-greedy, two-pointer-pairing-greedy), not near-duplicates.

**Why the gate is self-regulating on capacity:** a 🟢 conversion *removes* demand (matures a row off
the short interval) before the new row lands, and it's evidence the technique is sticking — so intake
grows only when both room and readiness are demonstrated. Ties directly to [[feedback_midweek_reprice]]
(re-price after a conversion) and the surplus-triggered-intake gate.

**How to apply:** at each weekly build, check whether any greedy problem went 🟢 since the last build;
if so and the cap isn't hit, seat one queued greedy sibling. Staged queue (Sep 9, 2026): **Reorganize
String** (heap), **Largest Number** (custom comparator), **Boats to Save People** (two-pointer pairing).
Trigger `green:<any greedy>` in the Waiting Room.
