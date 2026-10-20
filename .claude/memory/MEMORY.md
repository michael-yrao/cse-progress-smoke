# Memory Index

**This file is the index the coach loads at the start of every session.** One line per
memory, grouped for scanning. Never put memory *content* here — only pointers.

Opt-in reads: load the file relevant to the current task. **Operational coaching rules live in
the skill** (`.claude/skills/cse-coach/`); most `feedback_*` files below are now the
*why/evidence* behind a rule whose operational copy is in a skill reference or `CLAUDE.md` (§8,
the intervention ladder). A rule folded entirely into the skill has **no** memory file — see
`.coach-sync/declined.md` for those, so one rule never forks across two files.

This folder is **committed to git** — behavioral rules learned on one machine follow the learner
to every other one. A rule that lives only in a session's context is a rule you re-learn the hard way.

## Format

```markdown
---
name: <short-kebab-case-slug>
description: <one line — this is what the coach reads to decide relevance>
metadata:
  type: feedback | project | user | reference
reconciled: <YYYY-MM-DD, only after re-reading against decisions.yml>
---

<The rule, stated plainly. For `feedback` and `project`, follow with **Why:** and
**How to apply:**. Link related memories with [[their-name]] — a [[name]] with no file yet is
not an error, it marks a rule worth writing.>
```

- **`feedback`** — how the coach should behave (corrections *and* confirmed approaches).
- **`project`** — ongoing goals/constraints not derivable from the repo. Absolute dates, not relative.
- **`user`** — who the learner is. **`reference`** — pointers to external resources.

**Before writing a new file, check whether an existing one already covers it** — update it
instead of forking a near-duplicate. Delete memories that turn out to be wrong.

## Index

### North-star (read first)
- [Self-eval log](self_eval_log.md) — append-only running log of corrections; the raw data the weekly meta-review clusters.
  (The two operating principles and the self-evaluation loop are always-on — they live in the skill §0/§8, not as memory files.)

### Coaching voice & teaching
- [Teaching](feedback_teaching.md) — spine-first; for an algorithm purpose-then-procedure (proof last); one job per turn.
- [Explanation register](feedback_explanation_register.md) — show values before naming; no-nonsense engineer voice; on "I don't understand" ask which link broke; banned vocab.
- [Answer length](feedback_answer_length.md) — an answer to a question is one small paragraph; offer expansions, don't dump. Rationale/artifacts exempt.
- [Let the learner pace](feedback_let_learner_pace.md) — end the turn after answering; no "next?" tail; the learner drives advancement.
- [Interactive learning](feedback_interactive_learning.md) — derive/Socratic for heavy concepts, but spine-then-pull; at TRUE ZERO it degrades → teach the spine, let them pull.
- [Concept primer](feedback_concept_primer.md) — before the FIRST exposure to a named algorithm, a short UNRATED session on the object it finds + its name; the procedure comes later.
- [Reps over drills](feedback_reps_over_drills.md) — technique not landing → the next real rep, never a no-code drill or detached exercise.
- [Site plain language](feedback_site_plain_language.md) — every label and number on the site is understandable on its own; no coach vocabulary or bare ratios.
- [Positive phrasing + priority order](feedback_positive_phrasing.md) — rules say what to do; a day's problems run highest priority first; build each day toward the ceiling.
- [Expand acronyms](feedback_expand_acronyms.md) — expand every acronym on first use, chat + note.
- [Output quality](feedback_output_quality.md) — one message per turn after the last tool call; F1 · groundedness · narrative · readability; every repo-state claim names its tool result.

### Rating & gates
- [Recognition gate](feedback_recognition_gate.md) — front-gate: shape→technique+why (their pre-code comment); shape cues only, never candidate techniques.
- [Ask for complexity](feedback_ask_complexity.md) — gate: time + space, each with a why-clause, before any rating; clean-code + Big-O-miss → EOW cleanup, not a cap.
- [Infer comfort](feedback_infer_comfort.md) — read Clean/Shaky/Blank from the session, propose for confirmation; rate hint-volume; flag a dishonest 🟢.
- [Provisional Clean](feedback_provisional_clean.md) — a 🟢 straight after a 🔴 logs Streak 0 (lock-down), not Streak 1; only Blank→Clean is provisional.
- [Coding rules](feedback_coding_rules.md) — coding is the only path to 🟢; whiteboard fidelity (inline node defs); coach never edits `.py`; explicit-over-terse.
- [Read before asserting](feedback_read_before_asserting.md) — read a file before asserting its state; grep answers "exists", not "what is the state".

### Scaffolding, lineup & the learner's code
- [Lineup = links only](feedback_lineup_links_only.md) — a presented board is name + links, NOTHING else (spoils recognition); every on-board mention carries the `[file]·[LC/NC]` pair.
- [Learner-code boundary](feedback_learner_code_boundary.md) — coach may date a helper (tooling); never touch the learner's logic or comments (their reps).
- [Recommend by number, steer by description](feedback_recommend_by_number_steer_by_description.md) — link only the pick; name problems you're steering away from by description, not number (a link is an invitation).

### Scheduling, curriculum & effort
- [Schedule integrity](feedback_schedule_integrity.md) — re-slot every logged result (due-within-7d sweep); fix both sides of an out-of-order swap; a deferral gets a new date in the same edit.
- [Intake & surplus](feedback_intake_and_surplus.md) — demand is a rate in units; surplus gates pulls/intake; difficulty-tiered intake (blank tax); early completion asks before backfill.
- [Phase progression](feedback_phase_progression.md) — phase exit per-algorithm (recognition + execution); dates are checkpoints not deadlines; a 🔴 on an un-taught technique is phase-gated, not churned.
- [Midweek reprice](feedback_midweek_reprice.md) — the build verdict expires as reps land; re-run `effort_budget.py`, re-seat oldest-first; provisional-🟢 headroom is contingent.
- [Consolidation reps](feedback_consolidation_reps.md) — a technique needs 3–4 sibling problems; siblings are the recognition signal; ≤2/wk, gated 🟡+, sourced from a company pull.
- [Greedy conveyor](feedback_greedy_conveyor.md) — each greedy 🟢 pulls one new greedy sibling (cap ~2–3); conversion-gated.
- [Unseen on non-SD days](feedback_unseen_on_non_sd_days.md) — every non-SD day carries ≥1 unseen problem before backlog; a problem seen 3+ times tests retention not recognition.
- [End-of-week schedule](feedback_end_of_week_schedule.md) — archive + generate next week before the commit; a week with no schedule is not neutral. (why-only; checklist in the skill)
- [Coverage-gap ledger](feedback_coverage_gap_ledger.md) — end an SD session by logging what wasn't reached as bare open questions (the mock bank).

### System design
- [DSA before SD](feedback_dsa_before_sd.md) — all DSA first, SD last (open-ended tail); SD absorbs overrun; SD never pushed to next day unless asked.
- [HLD altitude](feedback_hld_altitude.md) — hold the learner at HLD through framework steps 1–4; name each LLD slip.
- [Quantify & qualify](feedback_quantify_qualify.md) — a number on every claim + a condition/boundary on every choice, every step.
- [Self-reported zero](feedback_self_reported_zero.md) — "I don't have X down" = assume ZERO retention; re-teach from the top, unrated.

### Session hygiene
- [Commit discipline](feedback_commit_discipline.md) — ask before every commit/push; accumulate into one commit; git-status sweep; close-out ≠ permission.
- [Verify terminal actions](feedback_verify_terminal_actions.md) — never close out/commit/push/archive on an instruction that contradicts the visible work; a turn with fabricated output is evidence for nothing.
- [Session dating](feedback_session_dating.md) — date by study session, not wall clock; a past-midnight session keeps its start date (source-fixed in the scripts).

### Project templates (personalize on adoption)
- [SD = mock interviews](project_sd_mock_model.md) — the learner studies SD on a finished external resource; the coach runs cold mocks + scores on the 7-point rubric; supports a study-mode hold (zero SD slots, don't nudge). The SD-model record.
- [AI pillar (parked)](project_ai_pillar.md) — AI Engineering as an OPTIONAL third pillar, PARKED behind a measured trigger (DSA must lighten); active/scored/spaced like SD when activated. Don't nudge until the trigger fires.
- [Recognition probes](project_recognition_probes.md) — 1 cold label-stripped probe/week from a 🟢 technique; disposable (no row on 🟢); the recognition axis the board can't test.
