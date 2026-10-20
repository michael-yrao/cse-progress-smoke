---
name: feedback-dsa-before-sd
description: Standing session order — clear all DSA first, then run SD last, so the SD slot has an open-ended tail for the learner's questions
metadata:
  type: feedback
reconciled: 2026-09-11
---

**Operational rule lives in the skill** — `references/weekly-build.md` ("Day order"). This file is the *why*.

**Set by the learner Aug 9, 2026:** *"let's finish all DSA and then SD as the standard so we can spend
more time on SD at the end for me to ask a lot of questions."*

**The rule:** on any day carrying both, **DSA runs first and SD runs last** — every day, not just when
the board is light. Schedule files should place the SD slot at the end of the day, and a kickoff lineup
should present it that way.

**Why it's the right order for this learner specifically.** SD here is taught **spine-then-pull**
([[feedback_interactive_learning]]) — the session ends when their questions run out, not when a
checklist does. That makes SD the one item on the board with **no natural stopping point**, and an
item with no stopping point must go last or it gets truncated by whatever follows it. DSA reps are the
opposite: each one is bounded, and a bounded thing scheduled last just gets done.

**⚠️ The cost, which must be said out loud when the day is tight.** The weekly build's overrun valve is
*"the cheap 🟢 sweeps yield if SD runs long."* **Running DSA first inverts that valve** — the sweeps are
already spent by the time SD starts, so SD becomes the thing that absorbs an overrun, which is the exact
outcome this rule exists to prevent.

**So on a full day, decide the yield BEFORE starting, not after.** If the board is near the ceiling and
the learner wants a long SD tail, the cheapest 🟢 sweeps come off the board **at kickoff** — a deliberate
pre-commitment, re-slotted in the same edit per the schedule-integrity rule. Never discover at 4pm that
the only thing left to cut is the SD tail.

**How to apply:** at kickoff, present DSA first and SD last; if the day is at or near the effort ceiling,
name the sweeps that would yield and ask whether to drop them now. See [[feedback_let_learner_pace]] —
this is their pacing decision, offered early rather than forced late.

⚠️ **But do not read "under the ceiling" as room to trim.** Offered the cut on Aug 9 (the day priced
just under the then-ceiling), the learner declined it: *"no we do them all. I have to keep myself to a
high standard, not stay below the … pointer per day."* **The ceiling is a ceiling, not a target to
undershoot.** A board that prices under it is a board that gets done — offer the yield decision
**once**, at kickoff, and then drop it. Do not re-raise it mid-day, and never pre-emptively shrink a
legal board to buy comfort margin.

⚠️⚠️ **Restated harder Aug 13, 2026 as a standing build instruction — then partly superseded Aug 16.**
The Aug 13 form was *"i want to go as close to 9 if possible, go over if needed"*, i.e. build every day
at the ceiling and backfill freed units rather than banking them (that was the day the three SD lanes
went away). **On Aug 16 the learner lowered the ceiling themselves** — *"it is getting harder to fit in
SD filling DSA with 9 points each day, so I might want to lax back to 8"* — which retires the literal
number and the "go over if needed" clause with it.

**What survives is the disposition, not the figure: build to the ceiling, don't undershoot it, and
never go over it.** The ceiling lives in `cse.config.yml`; read it there. Spend freed units on the
**🟢 backlog and due reviews, never on extra new intake** — that distinction is what keeps this from
colliding with
"headroom is not a mandate to fill": a rushed *new* problem lands 🟡 and bills ~12× forever, while an
overdue 🟢 is demand already on the board at 0.5–1.0 units, the cheapest and safest thing to add.
Intake stays at the difficulty-tier caps regardless of how much room exists.

## 🚫 SD does not get pushed to the next day (same conversation, Aug 9, 2026)

> *"let's try not to push SD to the next day unless the user asks especially if it's already started."*

**SD finishes on the day it is scheduled.** Deferring it is the learner's call to make, never a
suggestion to offer — and an SD item that is **already in progress** is effectively unmovable, because
moving it is what makes it unratable.

**Why the "already started" clause is the load-bearing half.** A design is *one row, one session, rated
cold*. The second sitting is no longer cold, so a design spread across days cannot be rated at all — it
silently leaves the SD tracker while still looking like progress on the schedule. Every push compounds
that. (Live example: the URL shortener banked steps 1–3 on Aug 2 and resumed Aug 9; a further push would
make it a third sitting.) **The correct move when a design overruns is to finish it at HLD depth and rate
what happened**, pushing any untouched deep dives to a *separate* row — not to continue the same rep next
week.

**How to apply:** never propose "we can pick SD up tomorrow" as the overrun release valve. If the day is
tight, the release valve is a 🟢 DSA sweep (offered at kickoff, per above), never the SD slot. If the
learner themselves chooses to defer, that's their call — re-slot it to a specific day in the same edit
and note whether the design was already started, since that decides whether it can still be rated.
