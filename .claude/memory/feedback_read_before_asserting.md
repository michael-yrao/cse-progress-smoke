---
name: feedback_read_before_asserting
description: Never assert what a file/tracker/log contains from memory, impression, or a partial read — Read it first; grep/tail answer "does X exist", never "what is the state of this"
metadata:
  type: feedback
reconciled: 2026-09-06
---

**Before asserting what a file contains, READ it.** Never state a count, a date, a comfort
rating, a prior attempt, or a file's state from **memory, impression, or a partial read**.

`grep`, `tail`, `head`, and `wc` answer *"does this substring exist"* or *"how big is this"* —
they **never** answer *"what is the state of this file."* Treating a partial read as a whole
read is the failure; the tool is fine, the inference is not.

**Why:** two occurrences, same root, different surfaces — which is what promoted this:

- **2026-07-07** — told the learner "146's last two attempts were 🔴" when the tracker showed
  **one**. Conflated *"appeared on two schedule boards"* with *"attempted twice."* Recited
  from impression instead of reading the row.
- **2026-07-14** — ran `tail -14` on `self_eval_log.md`, hit the trailing comment and blank
  lines, and declared **"the log is empty, the loop isn't running."** It had **15 entries**.
  Asserted a file's state from a partial read.

The second one was merely embarrassing. The same reflex aimed at a tracker row produces a
**wrong comfort rating → wrong interval**, and aimed at a schedule produces a **dropped
problem**. The engine is only as honest as the reads underneath it.

**How to apply:**
- Citing history (attempt counts, dates, prior comfort, streaks) → **Read the tracker row
  first.** Every time. No exceptions for "I just looked at it."
- Claiming a file is empty / unchanged / missing a thing → **Read the file**, don't infer it
  from a `tail` or a zero-match `grep`. A zero-match grep means *your pattern* didn't match.
- Reporting on the *state* of something (is this loop running? is this rule present?) →
  that's a **read**, not a search.
- When you catch yourself about to say "it looks like X is empty/missing/wrong," that phrasing
  **is the tell**. Go read it.
