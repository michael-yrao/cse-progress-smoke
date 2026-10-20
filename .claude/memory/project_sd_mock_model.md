---
name: project_sd_mock_model
description: System Design = cold mock interviews on a fixed question board — the learner studies independently, the coach interviews and scores on a 7-point rubric; no "read about X" ever goes on the schedule.
metadata:
  type: project
reconciled: 2026-09-06
---

<!-- TEMPLATE. The reusable SD-as-mock-interview model. Personal state (which chapters the learner has
     read, whether SD is in study-mode this week, the private study repo's URL, cleared reps) lives in
     the learner's own SD tracker/study guide, NOT in this shipped file. -->

**The split:** the learner learns system design on their own (e.g. via a finished external resource such
as HelloInterview). **The coach's entire job is cold mock interviews on that resource's questions, scored
on the 7-point rubric.** Nothing on the schedule is "read about X". Teaching happens on request,
off-schedule, unrated.

| | |
|---|---|
| **Board** | the external resource's question set, at their tiers (one design = one session) |
| **Cadence** | `mock_plus_deep_dive` — a cold mock + one **conditional** midweek deep-dive round that does not exist until a design is banked with open probes |
| **Rating** | 🟢 needs rubric #1–4 **and** #5 forks / #6 failure modes / #7 evolve-operate. **A prepared mock (breakdown already read) caps at 🟡** — ask before, not after |
| **Artifacts** | one debrief per mock; its `❓ Open probes` section is the deep-dive round's material |

## Study mode — no SD slot goes on the board

When the learner is still studying and has not signaled readiness, **build every week with zero SD
slots** — no mock, no deep-dive round, no placeholder.

- ⚠️ **Do not nudge.** Asking "ready for a mock yet?" at each build converts a learner-owned gate into a
  coach-owned one — the same failure as driving progression ([[feedback_let_learner_pace]]).
- **The learner signals readiness and hands over which question to mock.** Do not pre-pick the mock
  question on their behalf while in study mode — the choice is tied to which material they've completed.
- The first SD session on exit from study mode is a **restructure/scoping** session (scope the study to
  interview depth and no deeper, so it has a stopping condition), then mocks.

## Depth: a HIGH ceiling, a SENIOR bar — different things

- **Ceiling = how far a probe may go: high.** Keep pushing until the answer runs out; that is how the
  edge gets found.
- **Bar = the depth a checkpoint must reach to pass: junior/senior.** Exceptional depth does not gate 🟢.
- **A probe that runs past the bar costs nothing on the rating.** Record it under `❓ Open probes`, marked
  *above the current bar* — that distinction later separates "didn't know it" from "wasn't expected to."
- ⚠️ **When the bar moves, ratings stop being comparable across the move.** Date the change in
  `study_guide.md` and read earlier 🟢s as "🟢 at the senior bar."

**Requirements are a FLOOR.** Ruthless simplification kills *unjustified* sophistication (a queue nobody
needed), never the machinery the pinned non-functional requirements demand. As interviewer, **probe both
directions**: against over-design — *"why do you need this, what breaks if you drop it?"*; against
under-design — *"does this meet the number you pinned? Show me at 10×."* Watch the dodge of scoping
requirements down at step 1 to make the design easy — push the numbers back up.

**Why this model, and the part worth keeping.** A design repo that tries to be a textbook *and* a
scoreboard fails on the textbook half — writing a system-design textbook is open-ended work with no exit
condition, competing for the slots that grade the skill. A finished external resource is already the
textbook. The repo keeps the two jobs it does better than a website: **measurement over time, and the
adversarial half you cannot do alone.**

**How to apply.** Keep SD study material in the learner's chosen home (often a separate private repo);
read its mechanics/rubric before running or proposing a mock. **Never write the question into the weekly
schedule file** — that lets its breakdown be read in advance, which caps the mock. Name it at the
session, same discipline as [[project_recognition_probes]]. Reading the worked answer is "prepared";
previously attempting a design is not. Related: [[feedback_coverage_gap_ledger]], [[feedback_dsa_before_sd]].
