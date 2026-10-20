---
name: feedback_session_dating
description: Date logs by the study SESSION, not the wall clock — a session crossing midnight keeps its start date; verify the date against the schedule day being marked
metadata:
  type: feedback
reconciled: 2026-09-06
---

Attempt dates and comfort logs follow the **study session**, not the wall-clock date.

- A single continuous session that runs **past midnight keeps the date it started on.** Do not roll logged dates to the next day, and do not treat the session as "over," just because the clock passed midnight. All problems done in one sitting share one date.
- Only advance to a new date when the user begins a **genuinely new session** (they signed off and came back, or explicitly say it's a new day).
- If a "current date" signal is ambiguous or changes mid-session, **cross-check against the weekly schedule row you're actively marking** before dating anything — the schedule day is the source of truth for which session this is.

**Why (promoted from the self-eval log — 2 occurrences of date-handling errors):**
1. Logged a day's problems as Jun 16 when it was Jun 29 (trusted a stale date signal; entries sorted wrong, review dates off).
2. A continuous Thu Jul 2 session crossed midnight and 703 got dated Jul 3 while 98/323 from the same session were Jul 2 — inconsistent. Corrected 703 back to Jul 2.

**How to apply:** Determine the session's date once at the start — **confirm it explicitly with the user rather than inferring it from a problem's due date** (inferring caused a whole session to be mis-anchored to the wrong day). Then use that date for logs in the session. **Caveat when correcting a date:** a session can legitimately span two dates (e.g. the user does a few problems after midnight and considers those the next day) — do NOT assume one session maps to a single date. When the user corrects a date, confirm the per-problem split instead of blanket-re-dating everything. This is an instance of [[feedback_operating_principles]] P1 (accurate, consistent propagation). See [[self_eval_log]].

**⚠ Establish the date BEFORE acting, not just before logging (added 2026-07-29).** The rule above reads like a *logging* rule; it isn't. The session date is an **input to what work gets set up**, so getting it wrong corrupts the session before a single log line is written. On 2026-07-29 the learner opened with *"i'll do 235 early"* just past midnight; the system-prompt date said Jul 30, and on that basis a whole Jul 30 lineup was presented and **four Jul 30 problems were scaffolded** — wrong day's board, wrong daily-cap arithmetic (Thu's 4 instead of Wed's 5, hiding that the rep put the night at **6 against a cap of 5**), and a wrong date stamp written into the solution file. Every downstream statement was confidently wrong because the anchor was.

**In the post-midnight window, establish the date from evidence in the repo before doing anything:**

- **`git log -3 --date=iso`** — the cheapest and strongest signal. Commits timestamped minutes ago mean the session is **live**, not that a new day started. (On Jul 29 there were three commits at 00:00–00:07 wall-clock Jul 30, all Jul 29 session work; the learner had committed 30 minutes earlier. One command would have settled it.)
- **The schedule row** — which day's items are already struck through, and which day's are not.
- **Then confirm with the learner** if it's still ambiguous. Never infer a kickoff, a day, or a lineup from the system-prompt date alone.

**⚠ Tooling that defaults to the wall clock (added 2026-07-24; extended 2026-07-29).** The session date isn't just for logs — **scripts default to `now()` and will silently do the wrong thing past midnight.** `restore_history.py`'s default `--date` is `now()`; on a session that started Jul 24 and crossed into Jul 25, it looked for `_20260725` attempt methods (found none — the scaffolds/solutions are `_20260724`), declared every problem "still empty," and kept **all** stashes out. Committing then ships the solved files *without their restored history*. **On any midnight-crossing close-out, pass the session date explicitly: `python scripts/restore_history.py --date <session-YYYYMMDD>`**, and read the output (all-"Kept" is the tell it used the wrong date). Same vigilance for any other now()-defaulting tooling at close-out.

✅ **FIXED AT SOURCE, Aug 2, 2026 — the paragraph above describes a problem that no longer exists.**
All three scripts now resolve the **session** date through [`scripts/session_date.py`](../../scripts/session_date.py)
instead of `datetime.now()`, and **all three take `--date`** as an explicit override — including
`new_problem.py`, which this file said for two weeks *"has no `--date` flag at all"*. The primary signal
is a **dirty working tree**: past midnight, a session in progress means the session started yesterday.
The scripts announce the override when it fires.

⚠️ **This is the case study for the intervention ladder, and it cuts both ways.** The bug recurred
**three times AFTER** being promoted to this memory file, which is why it was fixed in the tool — but
then the memory file itself sat wrong for two weeks after the fix, telling anyone who read it to
hand-correct a stamp the script already gets right. **A source fix does not retire the rule file; it
obliges you to go rewrite it.**

**The pattern across all three:** every script here that touches a date is wrong past midnight unless the session date is supplied, and two of them fail *silently*. Treat "it's after midnight" as a standing instruction to check each date a tool writes.
