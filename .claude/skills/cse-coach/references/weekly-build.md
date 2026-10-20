<!-- reconciled: 2026-10-19 -->
# End-of-week close-out & schedule build

**The ordered procedure is the [`scheduling`](../../scheduling/SKILL.md) skill; this file is the
trigger and the why.** **Open this** when today is the last session of the week. **Not for** a mid-week rep (that's
`review-workflow.md`). **Not for** pricing a single day in progress (that's `effort-budget.md`
`--schedule-day`). The check is *"is today the last session of the week"* — **not** "does it feel
like a milestone". This was missed Aug 2, 2026, when a long session closed out on everything
*except* this.

**Archive + generate next week — both, in the same close-out, before the commit:**

```sh
git mv docs/foundations/schedules/<this-Mon>_schedule.md docs/foundations/schedules/archive/
# then write docs/foundations/schedules/<next-Mon>_schedule.md
```

Never one without the other. A week with no schedule file is not neutral. The weekly build is
where surplus is recomputed, the per-day load row is drawn (an aggregate is not a schedule). It
also reads `technique_coverage.md` to pick conversion reps. Skip it and next week runs off last
week's assumptions.

## The close-out checklist

- ⭐ **End-of-week complexity cleanup.** The queue covers
  every rep's misses. Read the cleanup-queue table in
  [`complexity_gotchas.md`](docs/foundations/dsa/mastery/complexity_gotchas.md). This covers any
  missed Big-O, since the rating no longer considers complexity. For each queued problem, have the
  learner **re-open that code and re-state time + space cold, with the why**. No re-solving; only the
  bound. Clean → clear the row; missed again → keep it queued and escalate to a proper complexity
  teach on that category. An empty queue is a clean pass, not a skip.
- ⭐ **Cold complexity probes fire at the Sunday close-out**, NOT scattered across weekday warmups.
  This was consolidated Sep 20, 2026 — STANDING, learner's call. ~2 probes fire **cold on any mature 🟢/🎓
  solved problem** to keep the miss-cluster categories fresh. The learner states time + space cold on
  the existing code. **Disposable — only a MISS is carded** (probe ledger in `complexity_gotchas.md`); a
  repeated same-category miss escalates to a teach. **ALL complexity checks** now live in one
  focused block on Sunday. That block covers both these probes AND the cleanup queue above. The weekday
  boards carry none, so the daily tables stay lean and the learner meets complexity work in a single sitting.
- **Why the pull order is the technique comfort audit's** (`scripts/technique_comfort_audit.py`;
  the why-lines and the FUTURE block are hand-authored, the script names any gap).
  - **The "⚠️ Needs work" callout** at the top is the pull-order source. Priority:
    **🔴/🟡 conversions (zero-green list, weakest first) > overdue 🟢 cleans > thin-green fills +
    probes.** A zero-green technique outranks *discretionary* work and *fresh* cleans — but **not** a
    clean aged far past its interval (a retention risk that manufactures new demand). A 🔴 bills ~12×
    a 🟢 forever, so converting one removes the most demand.
- **Regenerate the company-demand report — `python scripts/company_demand.py --tier all`** (network;
  not a hook). Read its per-tier "demand vs supply" tables beside `technique_coverage.md`: a
  `NO FAMILY` verdict is a vocabulary gap (add the family to `techniques.yml`), a `not started`/`thin`
  family with high demand is a pull-order input, and the "asked by ≥3 targets and untracked" list is
  the pull population.
- **⚠️ Does the week contain a FIRST exposure to a named algorithm?** Then it carries a CONCEPT
  PRIMER, scheduled before that problem. ~15 min, unrated, no tracker row, ~1.0 unit. It covers
  the object being found and its name, and the nearest neighbouring object and the one feature
  that separates them. It also covers why the obvious approach is not enough, and stops there.
  **The first attempt lands at least a day later.** A primer measured in the same sitting
  measures nothing. What measures it is whether the recognition call fires. A problem whose
  first attempt WAS the introduction to its algorithm once cost five sessions.
- **Unseen problems.** A problem seen 3+ times measures retention of that problem's solution, not
  the technique; unseen problems are the only test of recognition and transfer. New intake is
  `effort_budget.intake_per_week` problems, seated on the earliest days with room; a recognition
  probe and the mock are the week's other unseen rows; a day with no unseen row is fine
  (`scheduling`).
- **⚠️ Recompute any NUMERIC reason before renewing a deferral.** An item held because "surplus is
  −9.6" or "the board is full" expires silently the moment the number moves. Re-derive it, or
  restate the hold as a **state** condition (`green:Dijkstra`, `graduates:210`).
- **⚠️ Check every active phase has reps on the board.** (Found Aug 9, 2026: `Sliding Window +
  Stack` opened Aug 3 and sat a week with zero of its 8 problems in the tracker. It was invisible
  because the board was full of legitimate review work.)
- **Why a variant label is read from the tracker row.** One build once tagged several rows with
  the *other* variant in each case, which would have re-repped a graduated or not-yet-due variant.
  The board label is hand-authored, so verify it against the row (`scheduling`).
- **Why the integrity and phantom checks run on every build.** Two overdue 🔴s once crossed a
  week boundary and slipped consecutive builds, so a due row on no board is the "nothing dropped without
  a date" violation. A phantom row is one that discovery minted for a scaffolded, never-attempted
  file; a stranded probe sits outside `solutions.roots`. Steps: `scheduling`.
- **⚠️ Self-eval meta-review + skill-update evaluation (Sunday, STANDING).** Run
  `python scripts/meta_review_digest.py` (one line per OPEN entry). For each open entry: resolved →
  consolidate it into `self_eval_archive.md`. Still live → decide whether it names a recurring miss
  that warrants a **skill / CLAUDE.md change** per the intervention ladder, and make that change
  **in this pass**. A self-eval that sits open for weeks is exactly the failure this pass exists to
  stop. Sunday is where the log gets drained and the skills get updated *because* of it, not just
  where entries pile up.
- **⚠️ Lean daily table — THE FORMAT.** The board must read **at a glance.** Columns are
  **`| Problem | S | E | Next | Technique |`**:
  - **Problem** — glyph prefix(es) + `[name](file) · [LC](url) · [PO](site url)` (a variant parenthetical
    stays, read from the tracker row per the variant rule above). The `[PO]` link is
    `https://progressiveoverflow.com/practice/<n>`, present only when a spec `dsa/tests/<n>_*.yml` exists
    AND the row's own judge link is not already the site (an external-judge row keeps its single
    `[PO]` link). Compose the cell with `python scripts/links.py --schedule N …`;
    `check_schedule_integrity.py` flags a row that lacks it;
  - **S / E** — start / end comfort glyph; a 🟢 in **S** carries its streak going in (`🟢 s1`), which `effort_budget.py` prices from; **Next** — next-review glyph;
  - **Technique** — exactly **ONE word** (Backtracking · Dijkstra · Kruskal · Prefix-sum · …), nothing else.
  - **Row order** — within each day, problems run from highest priority to lowest: 🔴/🟡 conversions first, then new problems, then 🟢 reviews, with easy reviews last. A board shown to the learner keeps that order. `scripts/schedule_priority.py` applies this order, and the pre-commit hook runs it on a staged schedule.

  Three homes, so nothing is lost by leaving the table. *Rep rationale* ("was 🔴 last cycle",
  "template writable cold?") goes to the mastery ledgers (`stuck_log.md` · `complexity_gotchas.md` ·
  `recognition_gotchas.md`). *Status* (protected / backfill / new / moved / variant / probe / primer)
  goes to the **glyph** per the Tags legend, never prose. *A build caveat that truly needs a
  sentence* goes to a compact **⚙️ Build notes** list below the table, keyed by problem #. Examples:
  a move + new date, an LC-premium mirror, a scaffold note. A Note column carrying prose is a
  **build defect** — trim it. ⚠️ A cold complexity/recognition re-ask that prints its own answer in
  the board is a **spoiler bug**. The answer stays in the ledger; only the problem and which bound
  go on the board. full rule: `decisions.yml` `eow-close-out-process-sep20`.
- **If the AI pillar is still PARKED, test its activation trigger** (see
  [`project_ai_pillar`](.claude/memory/project_ai_pillar.md)): DP/Backtracking phases closed AND
  `effort_budget.py` shows ≥2 days/week well under the ceiling for 2 weeks. Met → raise starting it
  with the learner; not met → say nothing. This is the firing mechanism that keeps "deferred" from
  becoming "forgotten" — don't skip it just because AI isn't on the board.

**Day order:** within each day, place **all DSA first, SD last**. The SD slot gets the open-ended
tail, so SD also absorbs any overrun. Spine-then-pull has no natural stopping point; bounded DSA
reps do. Never push SD to the next day unless the learner asks (a started design that moves
becomes unratable). full rule:
[`feedback_dsa_before_sd`](.claude/memory/feedback_dsa_before_sd.md).

**Minimum contents of the built week:** capacity/surplus arithmetic · per-day load row · daily
table · protected reps · backlog/slip list (nothing dropped without a date or an explicit "no date
exists") · SD slots (placed, never priced — see `effort-budget.md`) · end-of-week targets ·
next-week preview · concept primers.

## The build procedure

The ordered steps (sweep, demand, forecast, pull order, content rules, pricing each day with its row
line, headers, the checkers, practice specs, the preview and the carried section), the row cap, the
carry rule and the intake backstop are the [`scheduling`](../../scheduling/SKILL.md) skill. Pricing
is the `effort-units` skill; budget policy is `effort-budget.md`. Coverage / which technique to pull:
`technique-coverage.md`.

## Headless build

`scripts/build_week.py` (run by `weekly-build.yml` when `automation.weekly_build` is true) builds the week
mechanically, with no coach in the loop. It drops forecast talk, the complexity block, the Pattern Sense
deck, the `technique_comfort_audit` pull order, primers, probes and mocks, spec authoring (replaced by
preferring site-runnable problems, `automation.prefer_practice_spec`), the next-week preview, prose goals
and day labels, and the SD slot. A coached build, above, adds all of these back.

## Pattern Sense results

From `pattern_sense.starts`, each week's build writes a Pattern Sense deck (the `scheduling` skill's
Pattern Sense step; `decisions.yml` `pattern-sense-weekly-oct18`). When the learner pastes a `PS1`
code at any session, run `python scripts/pattern_sense.py ingest "<code>"`. Results now arrive as
`dashboard/pattern_sense_results/<YYYYMMDD>.json`, saved by the site (owner only;
`decisions.yml` `pattern-sense-github-save-oct18`): run `python scripts/pattern_sense.py ingest
--pending`; a pasted `PS1` code still works through `ingest "<code>"`. Either way it writes nothing: paste
its `results:` block under that deck in `dashboard/pattern_sense.yml`, and log each draft line it
prints for a miss to `recognition_gotchas.md`. A miss changes no comfort rating. A problem that has
been in a deck is never used as a probe or a mock.

full rule: [`complexity_gotchas.md`](docs/foundations/dsa/mastery/complexity_gotchas.md);
`decisions.yml` `complexity-cleanup-formalized`, `rating-ignores-complexity`,
`complexity-probe-drill`, `technique-comfort-audit`;
[`feedback_end_of_week_schedule.md`](.claude/memory/feedback_end_of_week_schedule.md),
[`feedback_concept_primer.md`](.claude/memory/feedback_concept_primer.md),
[`feedback_unseen_on_non_sd_days.md`](.claude/memory/feedback_unseen_on_non_sd_days.md).
