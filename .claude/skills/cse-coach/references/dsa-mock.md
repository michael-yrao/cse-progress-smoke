<!-- reconciled: 2026-10-19 -->
# DSA mock interview — you interview, the learner codes

**Open this** before seating or running the recurring DSA mock (the 🎤 row), and before writing its
debrief. **Not for** a normal DSA rep (`review-workflow.md`). **Not for** a System Design mock
(`system-design.md`). **Not for** naming the base problem in the schedule file — that lets it be read
up in advance, which destroys the only thing the mock measures. Name it at the session only.

## The slot

Every `dsa_mock.every_days` (anchor `dsa_mock.first_due` in `cse.config.yml`; afterwards the clock is the last row of
[`docs/foundations/dsa/mocks/README.md`](docs/foundations/dsa/mocks/README.md)'s log). Seated on
Sunday as the first row of the day: `🎤 Mock interview (<Diff>) | 🎤 | | | Mock`. No problem number, no
technique. It is priced as a 🔴 blank at the named difficulty, via `--schedule-day`. It is that week's
unseen problem, so that week carries no 🎯 probe. The SessionStart banner says when one is due.

## Before

- **Pick.** `company_demand.md` → `### bigtech — top-100 problems`, Status `—`, at least three
  companies in *Asked by* (fallback: the "Asked by ≥3 target companies and untracked" list). The
  technique must be 🟢 or 🎓 in `technique_coverage.md` — never a zero-green technique, same guard as
  a probe. Pick the family first (rotate; highest demand not yet mocked), then the problem. A
  LeetCode-premium problem only with a NeetCode mirror.
- **Difficulty ratchet.** First mock Medium. Medium 🟢 → next is Hard. Hard 🟢 → Hard. Any 🟡 or 🔴
  → Medium next. The level-raiser verdict never moves it. State = the log's last row.
- **Cold rule.** Unseen = no tracker row, not in the probe log, not in `dashboard/pattern_sense.yml`, no file under
  `dsa/probes/` or `dsa/leetcode/`. An editorial read of the exact problem caps the base at 🟡 — **say it before, not
  after**.
- **Scaffold at the start of the mock session**, never at kickoff: `python scripts/new_problem.py
  --mock --number <n> --title "<Title>" --signature "<sig>"`. It writes to `dsa/probes/`. Present the **local file link only** — the LC page spoils
  the technique call.
- **Say the timebox out loud:** ~5 clarify · ~25-30 base · ~15-20 level raiser · ~5 complexity ·
  ~15 debrief after.

## During — interviewer, not coach

- No hints, no teaching, no leading questions. On a stall: silence, then "what are you weighing?".
- **The level raiser is thrown once** — when the base is coded, or at ~minute 35, whichever is first.
  Pick the move at the session, cold, from the family's row in the README Move bank.
- **The closing complexity question is gate 1** — time and space, each with a why-clause, before any
  rating is proposed.

## The move taxonomy

| # | Move | The interviewer's sentence | Leans toward |
|---|---|---|---|
| 1 | **Stream / online** | "Now the input arrives one element at a time; answer after each." | Google, Amazon |
| 2 | **Scale out** | "Now it doesn't fit in memory." / "Now it's across 100 machines." | Amazon (SDE-III bar), Google |
| 3 | **Repeated queries** | "Now I'll ask this 10⁶ times on the same data — what do you precompute?" | Google |
| 4 | **Generalize** | "Now k instead of 2." / "Now 2-D." / "Now weighted." / "Now with deletions." | Google, Meta |
| 5 | **Tighten the bound** | "Can you do it in O(1) extra space?" / "Without recursion?" / "Better than O(n log n)?" | Meta, Google |
| 6 | **Relax an assumption** | "Now there are duplicates / negatives / it's unsorted / the graph has cycles." | Meta (Move Zeros → negatives), Amazon |
| 7 | **Productionize** | "Make it an API: what's the signature, what if two callers race, what if a call fails midway?" | Amazon (LRU → API), Apple, Netflix |

## Scoring

- **Base problem:** the normal comfort rating. The closing complexity question is the complexity
  gate; the rating itself ignores Big-O, as everywhere.
- **Level raiser:** **pass / partial / fail** on an adaptability checklist — restated the delta ·
  named what survives · trade-off before code · correct approach · coded if time. Pass = correct
  approach plus at least three others. Partial = correct approach, or at least three others. Fail =
  neither. **Never a comfort glyph for the level raiser.**

## After — the debrief

Immediately, same session, in this order:

1. **Propose the base comfort rating and confirm it** (one rating proposal per turn).
2. **Score the checklist out loud**, with the evidence for each item.
3. **Write** `docs/foundations/dsa/mocks/<YYYYMMDD>_<slug>.md` from
   [`mock_debrief_template.md`](docs/foundations/dsa/templates/mock_debrief_template.md).
4. **Log the row** in the README's Log table.
5. **Tracker row** for the base problem, always (a Medium/Hard coded cold is an asset). The level
   raiser earns no row; its code is a second method in the same file.
6. **`git mv`** the file from `dsa/probes/` to `dsa/leetcode/<category>/` in the same edit as the
   tracker row (`check_phantom_scaffolds.py` catches one without the other).
7. **Ledgers:** `recognition_gotchas.md` always · `complexity_gotchas.md` on a miss · `stuck_log.md`
   on a non-🟢.
8. **Rewrite the schedule row**, struck and named: `🎤 ~~[N Title](file) · [LC](url)~~ | 🎤 | 🟡 | <date> | Mock`.

Open questions go in the debrief as bare questions, never as summaries of the answer.

## Ratchet · Trigger

Ratchet: see Before. Trigger: `dsa_mock.every_days` since the last log row; the SessionStart banner
fires when due is within a week and no live schedule carries a 🎤 row; `weekly-build.md` carries the
same check as a step.

full rule: `decisions.yml` `dsa-mock-interview-sep30`.
