---
name: feedback_lineup_links_only
description: Why a presented lineup is problem-name + links and NOTHING else, and why every on-board problem mention carries the [file]·[LC/NC] pair — the occurrence log behind both
metadata:
  type: feedback
reconciled: 2026-09-18
---

**Operational rule lives in the skill** — `.claude/skills/cse-coach/references/scaffolding.md`
("Presenting the kickoff / lineup board") and CLAUDE.md gate 4. This file is the *why* + the occurrence
log. Merges the former `feedback_kickoff_table_format` and `feedback_kickoff_table_links` (whose line-62
"put anything long in the Note cell" was a stale pre-Sep-4 remnant, now removed — it contradicted the
name+links-only rule).

## Two rules, one subject

1. **A presented lineup is problem name + links, NOTHING else.** No technique, note, difficulty, comfort,
   or units column; no technique parenthetical in the title. Anything beyond the name **spoils the
   recognition front-gate** — the thing the gate exists to measure. Comfort/units are for the schedule
   file (planning), never the lineup shown to the learner. **Build it from `scripts/links.py <n> ...`
   verbatim** — hand-copying schedule rows is what leaks the spoiler (the row carries `(Floyd-Warshall)`
   in its title and rep directives in its Note cell). Tightened Sep 4, 2026 (learner, twice: *"The tables
   should just be the name of the problems and links, nothing else."*).
2. **Every on-board actionable problem mention carries the `[file] · [LC/NC]` pair**, inside the problem
   cell (`NC` = the free NeetCode mirror when the problem is LC-premium). The file link opens the scaffold
   in one click; the problem link is the canonical reference. Off-board mentions (coverage lists,
   regression comparisons, roll-ups) stay **bare** — a link is an invitation, reserve it for what's due.

## Why both are correctness rules, not formatting

- **A column beyond the name pre-localizes the technique or the exact miss to watch** — the same class as
  the retry-handover spoiler (number + links only, no prior failure category). Leaked as a "Focus" column
  on 124 (Sep 3), a Note column + technique-in-title on 84/1462 (Sep 4), and a "What it is" column on the
  Sep 11 Friday board (239 → "monotonic-deque", 134 → "running-tank reset"). The Sep 11 recurrence — the
  3rd after the prose was tightened — escalated this root off the prose rung to a **blocking hook** (below).
- **A link to an off-board problem advertises a rep that isn't due** — on the night this was set, that is
  how 503 (🟢, due Sep 9) got pulled 26 days early while a 🟡 and a 🔴 sat undone. For an unscaffolded
  retry the file link is also the spoiler the caveat below forbids.

## The occurrence log (why the source fixes exist)

The links rule lapsed **12+ times** (Jul 20/21/23/30/31, Aug 3/5/6/12/14/21/23/27) — every time the output
stopped being the kickoff table (a rule anchored to an *artifact* decays when the artifact changes). The
fixes climbed the ladder:

- **Scaffold case → source-fixed** (`new_problem.py` prints a `LINKS:` line, Aug 3) — has not lapsed since.
- **Restate / "what's next" case → Stop hook** `problem_link_reminder.py` (Aug 12; re-enabled Aug 14 after
  shipping DISABLED; taught the day's board Aug 30 so it flags only on-board numbers). Also blocks a
  **broken** `.py` link (Aug 27 — a present-but-dead `../../../` path copied from a schedule row).
- **Note (learner's call):** the bare-number check in `problem_link_reminder.py` was removed
  (it read moved-out schedule rows as today's board and matched non-problem numbers), so the
  "Restate / what's next" bullet above and the `todays_board()` idea below no longer apply. The rule is now
  prose-only; boards come from `remaining.py` / `links.py`. `broken_file_links` and `spoiler_lineup` stay.
- **Lineup format → source-fixed** (`scripts/links.py`, the name+links-only builder, Sep 4).
- **"What's left" restate → source-fixed** (`scripts/remaining.py`, Sep 17). `links.py` still takes
  numbers the coach hand-supplies, so a restate built by *recalling* what's open can drop an item — done
  **twice in one session Sep 17** (said "one left" omitting 560; then dropped 721 from an earlier restate).
  `remaining.py` removes the recall: it reads the current week's schedule, finds the session-date
  day-block, and prints the **un-struck** rows as the same `[file]·[LC]` pairs (via `link_line`), so it is
  spoiler-free and this rule + the Stop hook are unaffected. New coach rule: answer any "what's left / what
  else / what's next / remaining" by **running `remaining.py`**, never from memory. Skill-only rung by the
  learner's call (no hook); the candidate next rung — an "incomplete-board" detector in
  `problem_link_reminder.py` reusing `todays_board()` — stays noted for if it slips again. See
  `references/scaffolding.md` ("Presenting the kickoff / lineup board"), `decisions.yml`
  `remaining-board-source-fix`.
- **Spoiler-column case → Stop hook** `problem_link_reminder.py::spoiler_lineup` (Sep 11). Blocks a
  presented lineup **table** whose scaffold-`.py`-link row carries a *semantic* extra column, a comfort/tag
  emoji, or a technique parenthetical in the title, and routes the re-emit through `scripts/links.py`. Prose
  (SKILL.md §4 + `references/scaffolding.md`, both naming the exact forbidden columns) had failed this root
  3× — Sep 3/4/11 — so it earned the rung above. Board-independent: the scaffold-`.py`-link signature already
  scopes it to a lineup, so rating/coverage/schedule tables never trip it.
  - **A bare numeric index column is EXEMPT (learner's call, Sep 12).** `| 138 | [138 Copy…] |` or a running
    `1, 2, 3` only echoes the number already in the link text — it localizes nothing the lineup doesn't
    already show, so it is not a spoiler. The detector over-flagged one (`_is_index_cell` now exempts it);
    the spoiler is a *semantic* cell (Note/Focus/technique/comfort/units/difficulty), not an index. A
    technique parenthetical or a comfort emoji in the same table still blocks.
- ⚠️ **Never write a bare problem number** in narration — the Stop hook gathers all assistant text, so a
  loose number trips it even when linked elsewhere. Refer to a problem by name/role; a number appears only
  inside its pair (Aug 23).

## Scope + the one caveat

- **Scope (Aug 14/15):** the pair is for **on-board actionable** items (kickoff, hand-over, restate,
  "what's next"). Not for context mentions. Enforced: the hook resolves the day's board from tracker due
  dates + today's schedule row.
- ⚠️ **A retry's file link is a spoiler until scaffolded.** Kickoff-table files are safe (scaffolded
  first, prior attempts stashed). In a **selection/candidate menu** the retry isn't scaffolded yet →
  **LC/NC only**; surface the file link only after the pick is scaffolded. (Learned Jul 20.)
- ⚠️ **A recognition probe is the INVERSE pair: local file link YES, LC/NC link NO** (Sep 14, 2026; the DSA-mock base problem too).
  It is the one on-board item where the *problem-page* link is the spoiler — LC's topic tags / editorial
  name the technique, which is the whole thing the probe measures. The `dsa/probes/<n>_<snake>.py` path
  names the *problem*, not the technique, and the learner must open the file to do the rep — so present it
  as `[<n> <title>](dsa/probes/…py)` with **no** `· [LC]`. Prior wording said a probe "stays UNLINKED,"
  which over-corrected and left the learner asking for the file link **3× on Sep 14**. Enforcement: created
  via `new_problem.py --probe` (prints the local link only); `scaffold_links_reminder.py` and the Stop
  hook's message both carry the probe branch. Dated: `decisions.yml` `probe-local-file-link`.

Related: [[feedback_no_spoilers]], [[feedback_recommend_by_number_steer_by_description]],
[[feedback_schedule_integrity]].
