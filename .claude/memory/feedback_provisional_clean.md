---
name: feedback_provisional_clean
description: A 🟢 Clean that directly follows a 🔴 Blank is logged with Streak 0 (provisional) → a short lock-down interval, not the normal Streak-1 one; only Blank→Clean is provisional
metadata:
  type: feedback
reconciled: 2026-09-11
---

**Operational rule + values live elsewhere** — the ladder is in `references/spaced-repetition.md`, and
**every interval value is in `cse.config.yml` under `intervals:`** (never restate a number here — the
single-source rule). This file is the *why*.

**When logging a 🟢 Clean that directly follows a 🔴 Blank, set Streak 0, not 1.** `update_review_dates.py`
treats a 🟢 with Streak 0 as a **provisional Clean** and computes the **`intervals.clean.provisional`**
value (a lock-down check), not the normal Streak-1 interval. Rationale: one Clean right after a Blank may be
recall of fresh teaching, not durable retention (same logic as the teach/measure split). It has to survive
the lock-down check before earning the real ladder.

**How it flows:**
- 🔴 → 🟢 : log the 🟢 with **Streak 0** → the provisional (lock-down) interval.
- Survives (🟢 again at the lock-down check): log **Streak 1**, rejoining the normal ladder.
- Slips (🟡/🔴): resets as usual.
- **🟡 → 🟢 is NOT provisional** — log Streak 1 as normal. Only **Blank→Clean** gets the lock-down (a 🟡 got
  there with a nudge; a 🔴 blanked — less trustworthy).

**Do not "fix" a 🟢 / Streak-0 row to Streak 1** — that silently deletes the lock-down and the row jumps to
the full Streak-1 interval.

**Why (added Jul 18, 2026):** the learner wanted 787 Bellman-Ford (🔴 Jul 14 → 🟢 Jul 16) reviewed at the
short lock-down interval to confirm it stuck, not the full Streak-1 one. Generalized into this policy
instead of a one-off manual date (the pre-commit hook recomputes and reverts manual date edits — the Redis
date incident). Documented in the `dsa_progress.md` header and the ladder in `references/spaced-repetition.md`.
Related: [[feedback_infer_comfort]] (this fires at log time, keyed to the *prior* attempt's comfort).
