---
name: scheduling
description: >-
  The ordered procedure for building and editing the study schedule: the weekly
  build, mid-week reseats, deferral, carry-forward past the row cap, the weekly intake rate and
  the unproven-overdue backstop. Use when building, repricing or editing a schedule: the last
  session of the week, seating or moving a row, deciding what to carry to next week, or
  deciding how many new problems the build seats. Unit numbers still come from the
  effort-units skill.
reconciled: 2026-10-19
---
# scheduling — one ordered procedure for the weekly build

The policy lives elsewhere: the unit model and the ceiling in the cse-coach reference
[`effort-budget.md`](../cse-coach/references/effort-budget.md), the why of the close-out in
[`weekly-build.md`](../cse-coach/references/weekly-build.md), the numbers in `cse.config.yml`
`effort_budget:` and `intervals:`. This skill is the order of the steps. It never restates a
number: it names the key.

## Three rules

1. **Every unit number goes through [`effort-units`](../effort-units/SKILL.md).** A day header's first figure equals the script's `built`; a started day may also carry a pinned planned figure (effort-units). No estimates.
2. **A day has two caps.** Units (`effort_budget.ceiling`) and rows
   (`effort_budget.max_rows_per_day`). Check both, with the script, on every touched day.
3. **A tracker date is never edited to make a day fit.** A row that does not fit is carried in
   the schedule file; its due date stays where the ladder put it. A learner-requested deferral past
   the ladder date goes in `docs/foundations/dsa/mastery/holds.yml` with a date and a decision id,
   never a typed tracker date.

## Which command answers which question

| Question | Command | Quote |
|---|---|---|
| What is due by the end of the week, priced? | `effort_budget.py --due <Sunday>` | the total |
| Weekly demand, overdue cost, unproven-overdue count, the intake line | `effort_budget.py` (no flag) | demand · overdue · unproven · intake |
| Does the configured intake rate pile up a backlog? | `backlog_forecast.py --check` | the last line |
| What would these problems cost on a day not yet started? | `effort_budget.py --day N N …` | `TOTAL` and the row line |
| What does a built day cost, and how many rows? | `effort_budget.py --schedule-day YYYY-MM-DD` | `built` and the row line |
| Is the order right? | `schedule_priority.py` | exit code |
| Is every due row seated or validly carried? | `check_schedule_integrity.py` | exit code |

## The weekly build, in order

1. **Trigger.** Last session of the week (`weekly-build.md`). Both the archive and next week's
   file land before the commit.
2. **Sweep.** `effort_budget.py --due <Sunday>` lists every row due in the week, priced.
3. **Demand.** `effort_budget.py` with no flag: read demand, overdue, the unproven-overdue line
   and the intake line.
4. **Forecast.** `backlog_forecast.py --check`. The configured `intake_per_week` must not read
   piling. If it does, say so to the learner: the key is theirs to change, not the build's.
5. **Archive** this week's file.
6. **Complexity block.** The cleanup queue and the cold probes sit in one Sunday block (why:
   `weekly-build.md`). Complexity rows are unpriced and not counted toward the row cap.
7. **Pattern Sense.** From `pattern_sense.starts` on, once per week (the deck is unpriced and
   seats no row):
   - Run `pattern_sense.py ingest --pending` and log any pending week (paste its `results:` block,
     log its miss lines) before `propose`.
   - Run `pattern_sense.py propose --week <Monday>`. It lists `pattern_sense.per_week` picks and
     one spare round, and prints each pick's statement to the terminal only.
   - Per pick: label the family, the technique (a `techniques.yml` name in that family) and the
     cue, and paraphrase the statement (shape, ask, constraints, one example; no title).
   - A pick you cannot label goes under `skipped:` in the deck and the next spare takes its place.
   - Write the deck into `dashboard/pattern_sense.yml`, run `pattern_sense.py export --check`,
     then `export`.
   - Write one line, `## Pattern Sense`, after the Daily Schedule: the deck's week, no problem
     number or title. It is prose, never a table row.
8. **Pull order.** `technique_comfort_audit.py`; read the "Needs work" callout first.
9. **Content rules.**
   - A first exposure to a named algorithm carries a concept primer, a day before the first
     attempt.
   - New intake is `effort_budget.intake_per_week` problems, seated on the earliest days with
     room; a recognition probe and the mock are the week's other unseen rows; a day with no
     unseen row is fine.
   - Mock due: seat the 🎤 row on Sunday per [`dsa-mock.md`](../cse-coach/references/dsa-mock.md).
   - A variant label is read from the due tracker row, never typed.
10. **Price each hypothetical day** with `--day N N …` and read the row line beside `TOTAL`.
11. **Write the file.** Lean table, rows ordered highest priority first, DSA before SD. Each row's
    link cell is pasted from `links.py --schedule N …`, never typed (it adds `· [PO](site url)`).
12. **Headers.** `--schedule-day` per day; set each header's first figure to `built`. A build writes no planned figure.
13. **Order.** `schedule_priority.py`.
14. **Integrity.** `check_schedule_integrity.py`. Every due row is seated, validly carried, or
    given a new tracker date (a deferral gets a date in the same edit).
15. **Phantoms.** `check_phantom_scaffolds.py`.
16. **Practice specs** for every seated problem with none, then `export_practice.py`
    (procedure: `practice-problem`).
17. **Preview and carried section.** Write the next-week preview and the
    `## ⏭️ Carried to next week (row cap)` section.

## Row cap

A day holds at most `effort_budget.max_rows_per_day` rows. Every row in the day block counts,
struck rows included; Complexity-technique rows do not. The cap fixes a day's shape; units
still bind the week. A day over the cap is fixed by carrying, not by editing a tracker date.

## Carry rule

- A row carried past its week goes in the `## ⏭️ Carried to next week (row cap)` section, one
  bullet per row: `- [N Title](path) · 🟢 s2 · due YYYY-MM-DD · carried from <Day>`.
- Only **proven** rows are carried: 🎓, or 🟢 at a streak of `carry_forward_min_streak` or
  above. Easy 🟢 rows go first, from the bottom of the priority order.
- **Unproven rows are never carried:** 🔴, 🟡, and 🟢 below `carry_forward_min_streak`. They
  displace a proven row from a full day instead.
- The tracker's due date is untouched; the integrity check accepts a carried row only when
  the tracker row meets the rule above.

## Intake and the backstop

- The weekly build seats `effort_budget.intake_per_week` new problems. The 🎤 mock and a 🎯
  recognition probe are not intake.
- **Backstop:** when the count of overdue unproven tracker rows reaches
  `effort_budget.intake_pause_overdue_unproven`, the next build seats no new problem. The count
  is the unproven line of the no-flag output.
- Why the rate and the backstop have these values: the forecast's simulation table in
  `decisions.yml` `intake-rate-and-backstop-oct6`. Re-run `backlog_forecast.py` to re-check; do
  not copy its numbers here.

## Reading the output

| Line | Meaning | Do |
|---|---|---|
| `rows N / cap` | the day's row count against the cap | nothing |
| `!! N ROWS, cap is …` | the day is over the row cap | carry the lowest-priority proven rows |
| `overdue unproven: N … not triggered` | below the backstop | build as usual |
| `overdue unproven: N … TRIGGERED` | at or above the backstop | seat no new problem |
| forecast last line reads `piling` | the configured rate outruns the reps | tell the learner |

## Mid-week

After logging a day's results, run `--schedule-day` and the no-flag run. Reseat a row from the
carried list only when the day shows spare rows AND spare units (policy: `effort-budget.md`
"Re-price mid-week"). Moving a row between days, started or not, follows `effort-units`. A pull into the live session (the learner starts a later day's row now) leaves the row on its origin day as a `←` row per effort-units, adds its copy to the session date, and scaffolds it in the same turn.
