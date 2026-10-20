# Self-Evaluation Log

**Append-only record of every correction the coach receives** — whether the learner catches
it or the coach catches itself. This is the raw data; the weekly meta-review clusters it and
**promotes repeats into rule files** in this folder (cse-coach skill §8).

> **A one-off correction is noise. A *repeated* one is a missing rule.** This log exists to
> tell those apart — which it can only do if entries actually get written. Append **in the
> same flow as the fix**, never "later."

## Format

```
- YYYY-MM-DD — <what went wrong> → <the fix>. Root: <why it happened>. [P1|P2] (status: open | consolidated→[[rule-name]])
```

- **`[P1]`** — broke *"close the loop completely and proactively"* (§0.1)
- **`[P2]`** — broke *"the learner owns the thinking and the code"* (§0.2)
- **status** — starts `open`; becomes `consolidated→[[rule]]` once promoted.

## Weekly meta-review (first session of the week, or when `open` entries reach ~8)

1. **Cluster** the `open` entries by **root cause**, not by symptom. Two entries with
   different surfaces and the same root are one cluster.
2. **Any root cause appearing 2+ times gets promoted** — write or tighten a rule file in
   this folder so the mistake is prevented *structurally*, not merely remembered.
3. Mark those entries `consolidated→[[rule]]`. Leave genuine one-offs `open` — they may
   cluster later.
4. **Never delete an entry.** Append-only; only the status changes.

An entry is warranted for: a wrong value logged, an artifact mislabeled, a missed
propagation (an unstaged file, a due problem left unscheduled), a spoiler slip, a bad
assumption, a rating rationalised upward, or an explanation that left the learner *more*
confused than before.

---

<!-- Entries below, oldest first. -->

- 2026-07-25 — (synced from cse-progress) Coach kept appending "ready for the next problem?" to answers while the learner was still working through a complexity follow-up. **2nd occurrence** (1st: Jul 19 Redis card review, "ready for N?" every turn). Root: driving *progression* instead of letting the learner drive — twin of front-loading *depth*. Promoted → [[feedback_let_learner_pace]] and skill §1b. [P2] (status: consolidated→[[feedback_let_learner_pace]])
- 2026-07-25 — (synced from cse-progress) On a design problem with two complexity misses in one first-time rep, the coach proposed 🟡 (treating the 2nd miss as a cap-triggering "repeat"). Learner corrected: the freebie is **per-problem-per-rep, not per-method** — both misses spend the one freebie; the cap fires only on a problem already carded from a **prior** rep. Root: misread freebie granularity → would drop clean 🟢 to 🟡 (+10 vs +30, interval corruption). Fix: clarified [[feedback_ask_complexity]] + skill §3 step 4. [P1] (status: consolidated→[[feedback_ask_complexity]])
- 2026-07-25 — (synced from cse-progress) New mechanism added, not a correction: **recognition front-gate** — learner states shape→technique+why before coding, mirroring the complexity back-gate; addresses that solving-in-isolation never trains cold problem→technique recognition (what the interview grades first). Promoted → [[feedback_recognition_gate]] + skill §3 step 3. (status: consolidated→[[feedback_recognition_gate]])
