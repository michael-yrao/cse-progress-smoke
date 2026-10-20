---
name: feedback_end_of_week_schedule
description: Why the last session of the week archives + generates next week's schedule before the commit — a week with no schedule file is not a neutral state
metadata:
  type: feedback
reconciled: 2026-09-11
---

**Operational rule lives in the skill** — the full close-out checklist (archive + generate next week,
complexity cleanup, comfort audit, concept primers, unseen-on-non-SD-days, fill order) is in
`.claude/skills/cse-coach/references/weekly-build.md`, and the trigger is CLAUDE.md gate 7. This file is
just the *why*.

**A week with no schedule file is not neutral.** The learner noticed the Jun 29 week began with no
schedule at all — and the weekly build is where surplus is recomputed, the per-day load row is drawn (an
aggregate is not a schedule), and `technique_coverage.md` is read to pick conversion reps. Skip it and the
next week silently runs off the previous week's assumptions. So archive-current **and** generate-next
happen **together**, before the commit — never one without the other.

Related: [[feedback_intake_and_surplus]], [[feedback_schedule_integrity]], [[project_sd_mock_model]]
(the Sunday slot is a mock, placed not priced).
