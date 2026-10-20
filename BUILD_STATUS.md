# cse-coach — build status

Staging build of the `cse-coach` repo (design: `../../docs/planning/cse-coach-extraction-design.md`).
Lives under `build/cse-coach/` on the `cse-review` design branch until it's solid,
then gets pushed to its own private GitHub repo (Q4: private first).

Tracking the §7 phased build plan:

| # | Step | Status |
|---|------|--------|
| 1 | Scaffold repo — skeleton (2 pillars: DSA + System Design), license, README, CLAUDE.md, config example, hook, skill in place | ✅ done |
| 2 | Port engine — config-driven `update_review_dates.py` (intervals/root/globs from `cse.config.yml`, stdlib-only) + tests | ✅ done |
| 3 | Port DSA scaffold — patterns/fundamentals (copied clean), blank tracker/logs, `solution_template.py` + `new_problem.py` scaffolder (tested: create/retry/discovery) | ✅ done |
| 4 | Port System Design pillar — study guide, templates, blank `design_progress.md`; engine now multi-tracker (`--tracker`, no discovery) + hook wired; tests pass | ✅ done |
| 5 | System Design = mock-interview model — the learner studies SD externally; the coach runs cold mocks scored on a 7-point rubric; debriefs to `mocks/`; both trackers idempotent | ✅ done |
| 6 | Author curriculum + backlog pools — DSA milestone (18 phases / 150 problems), Tier 1/2 expansion, interview + competitive backlog; SD tiers (mock board). All YAML valid | ✅ done |
| 7 | Write bootstrap — args/interactive intake, `reach_beyond ≥ 1` floor, projects NC150 → dated roadmap + week-1 schedule, installs hook. Tested end-to-end | ✅ done |
| 8 | Extract coaching skill — SKILL.md in place + CLAUDE.md wired | ✅ done |
| 9 | README (coach voice, interaction model) + `docs/PHILOSOPHY.md` | ✅ done |
| 10 | Dogfood — full adopter flow verified (bootstrap → scaffold → log DSA Clean +30 → log SD mock Shaky +10, all via the git hook) | ✅ done |
| 11 | Publish — create private GitHub repo, push | ⏸ awaiting go-ahead (outward-facing; staged & testable from build/cse-coach on the branch) |

## How to test the staged build

Copy it out of the design branch and drive it (don't run bootstrap in-place — it
writes personal files):

```sh
cp -r build/cse-coach /tmp/cse-coach && cd /tmp/cse-coach && git init -q
python scripts/bootstrap.py --name You --start 2026-07-13 --non-interactive
python scripts/new_problem.py --number 1 --title "Two Sum" --pattern arrays_and_hash
python tests/test_engine.py            # 5 engine tests
git add -A && git commit -m wip        # pre-commit hook recomputes trackers
```

Then open it in Claude Code and just talk to the coach ("start today", solve,
report Clean/Shaky/Blank). Bootstrap prompts interactively if you omit the flags.

## Notes
- Much study content can be **ported from `cse-review`** (patterns, fundamentals,
  SD study guide/templates, competitive backlog) with personal data stripped.
- The skill (`.claude/skills/cse-coach/SKILL.md`) and README are already the real
  drafted versions, moved in during step 1.
- **Engine (step 2):** zero external deps (stdlib only; no PyYAML). Config parsed
  with targeted regex over the documented `cse.config.yml` subset. Defaults exactly
  reproduce cse-review behavior. `DISCOVERY_SKIP_NUMBERS` emptied (the `{76}` was
  cse-review-personal). Run tests: `python tests/test_engine.py`.
- **Multi-pillar tracker iteration** (step 4): added `recompute_simple()` +
  `--tracker` — recompute/re-sort a same-format tracker with NO source discovery;
  the DSA `main()` is untouched (its tests still pass). Hook passes `--tracker` for
  the SD tracker. Verified idempotent (2nd run = no-op) on real trackers.
- **Seed rows must use the engine's canonical format** — empty fields are TWO
  spaces (`|  |`), not one. Hand-written single-space empties mis-parse. Both seed
  rows normalized; the DSA tracker carries its auto-summary block.

## Architecture sync (post-0.2.0)

Promoted the practice repo's architectural evolution up to canonical (via `promote_report.py`,
curated by hand). Personal data stripped; redistribution invariants preserved. Bump VERSION and
run the release steps (`update_coach.py --emit-manifest` + tag) when ready.

- **Skill restructured** — the monolithic `SKILL.md` became a lean **spine + 8 `references/`**
  (loaded per coaching moment).
- **Reconciliation system added** — `decisions.yml`, `reconciled:` frontmatter, `scripts/reconcile.py`,
  and the 4-tier model in `docs/ARCHITECTURE.md`. `CLAUDE.md` now carries the always-on gate layer (L1).
- **New hooks/scripts** — `rating_gate.py`, `problem_link_reminder.py`, `kickoff_scaffold_reminder.py`;
  `reconcile.py`, `check_schedule_integrity.py`, `technique_comfort_audit.py`, `links.py`. The
  pre-commit hook wires the schedule-integrity + reconcile + single-source checkers (report-only).
- **Recognition-probe feature** — `new_problem.py --probe` writes to `dsa/probes/` (neutral path,
  "you name it" header, local-link-only); `update_review_dates.py` folds rowless probes into the
  summary counts (`+N`). Blank `dsa/probes/README.md` template ships.
- **Current model** — SD is off-board and **unpriced** (retired `sd_*_units`); effort `ceiling` 8.0;
  `graduate_at_streak` vocabulary. `cse.config.example.yml` reconciled to match.
- **Schedules** moved to the shared `docs/foundations/schedules/` (both pillars), out of `dsa/`.
- **AI pillar** returns as an OPTIONAL, parked third pillar (`project_ai_pillar.md`, off by default).
- **Memory** matched to the practice repo's non-declined set (superseded dupes retired to
  `.coach-sync/declined.md`; the 3 genericized `project_*` templates ship by explicit `ENGINE_PATHS` name).
- **Two engine adaptations kept** (recorded in `declined.md`): `update_review_dates.py`'s `sys.path`
  guard (the shipped test harness imports it) and `check_single_source.py`'s fallback to
  `cse.config.example.yml` when no live config exists yet.

Verified: all four test suites pass, `check_single_source`/`reconcile` run, and the adopter flow
(bootstrap → scaffold normal + probe → engine) works end-to-end. Every engine `import yaml` is lazy
with a regex-scrape fallback (`except ImportError`), so PyYAML stays optional — the stdlib guarantee
holds by construction, not by luck.

## v0.9.0 sync

Promoted the practice repo's changes since v0.8.0 (via `promote_report.py`, curated by hand;
personal data stripped, redistribution invariants preserved). Release steps: `update_coach.py
--emit-manifest`, then the `v0.9.0` tag.

- **Three new skills** — `effort-units` (every effort-unit number comes from `effort_budget.py` in one
  named mode), `scheduling` (the ordered weekly-build, reseat, deferral and intake procedure) and
  `practice-problem` (a problem's practice spec and site solution).
- **The scheduling scripts** — `schedule_priority.py`, `backlog_forecast.py`, `company_demand.py`,
  `fold_attempt.py`, `check_line_endings.py`, with the row cap, intake-rate and unproven-overdue
  backstop rules in `cse.config.example.yml`.
- **Pattern Sense** — `pattern_sense.py`, its schema and an empty `dashboard/pattern_sense.yml`; an
  empty deck file writes nothing, so the site keeps its fallback.
- **Practice contract extensions** — `check_practice_spec.py` and the extended spec codecs, `judge`
  bindings, `anyOf` expected values and `unordered-inner` compare mode.
- **Decision-tree cheat sheets** — the `dynamic_programming.md` technique doc (memoization folded in)
  and the family vocabulary in `techniques.yml` (`greedy`, `strings`, `math_sim`, `design`,
  `bit_manipulation`, the four-way Intervals split).
- **Commit-push gate** — `commit_push_gate.py` denies a chained commit-and-push, so the pre-commit
  hook's output is read between the two commands.
- **Onboarding** — sign in at progressiveoverflow.com/start and choose DSA: the site creates
  `<you>/cse-progress` from this template (collaborators only while this repo is private). The
  starter `dashboard/` ships the generated progress, cheat-sheet and manifest JSON; the exporters
  that need your own data (practice, Big-O, showcase, Pattern Sense) write nothing until you add it.

Verified: the full suite passes, `check_single_source` / `reconcile` run, and every shipped
`dashboard/*.json` that has a schema validates against it (`tests/test_dashboard_contract.py`).

## v0.10.0 sync

The headless study track (`decisions.yml` `headless-study-track-oct19`): a learner with no clone works on
the site, and the engine runs as three Actions in their own repo. `onboard.yml` runs
`scripts/bootstrap.py --intake` on the `intake.yml` the site writes; `fold-attempts.yml` folds site reps,
one transaction per attempt; `weekly-build.yml` runs `scripts/build_week.py`. Bootstrap gained `--intake`
(validated name, target, timezone, start date), the `timezone` and `automation:` config keys, filled
placeholder dates, an undated-row strip for the tracker, and a `build_week.py` call in place of
`write_week1`. Release steps: `update_coach.py --emit-manifest`, then the `v0.10.0` tag.
