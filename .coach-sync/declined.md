# Promotion declines

Paths that `promote_report.py` will keep reporting, and that we have **decided not to
promote**. The point of recording them is the one in that script's own docstring: without
this file, a deliberate decline and a thing nobody noticed look identical on every run,
and a report where most rows are already-answered questions stops being read.

Format: one `path — reason` line under a heading. Re-open any of these freely — a decline
is a judgement at a point in time, not a lock.

## Coaching rules already encoded in `.claude/skills/cse-coach/SKILL.md`

The practice repo keeps these as memory files because that is where they were *discovered*.
Canonical absorbed each one into the skill instead, which is the **stronger rung** — the
skill/CLAUDE.md pair is always injected, memory files are opt-in reads (CLAUDE.md gate 5,
the intervention ladder).
Shipping both would fork one rule across two files that then drift apart.

**Before declining a new one on this basis, actually grep the skill for it.** The reason
these are listed individually rather than as a blanket rule is that the check was done per
file, and the next person deserves the same standard.

- `.claude/memory/feedback_algorithm_purpose_first.md` — skill §7a (purpose before mechanism)
- `.claude/memory/feedback_check_schedule_before_docs.md` — skill §4
- `.claude/memory/feedback_code_by_default.md` — skill §2a scaffold table
- `.claude/memory/feedback_coding_for_clean.md` — skill §2 (Comfort scale)
- `.claude/memory/feedback_consolidation_reps.md` — skill §5 (intake classes)
- `.claude/memory/feedback_daily_cap.md` — skill §4 (`daily_cap`)
- `.claude/memory/feedback_expansion_pull_scheduling.md` — `references/weekly-build.md` (the
  "Needs work" callout is the pull-order source) + `references/technique-coverage.md`
  (`pull_interview.py` mechanics, the post-NC150 pull gate)
- `.claude/memory/feedback_gate_on_internal_state.md` — skill §4
- `.claude/memory/feedback_infer_comfort.md` — skill §3 step 4
- `.claude/memory/feedback_interactive_learning.md` — skill §7a (teaching formats)
- `.claude/memory/feedback_method_variant_promotion.md` — skill §5
- `.claude/memory/feedback_new_vs_retry.md` — **no current home.** Its rule (a schedule's separate
  "New Problems This Week" table vs. a `study_guide.md` roadmap-phase source) describes a schedule
  format the engine has since moved past — the current board tags a new row with 🆕 directly in the
  one Daily Schedule table (see `scripts/gamify.py`'s `kind: 'new'`), so there is no separate table
  left to misfile a retry into. Left declined rather than repointed to something that doesn't cover it.
- `.claude/memory/feedback_no_code_edits.md` — skill §0.2
- `.claude/memory/feedback_no_prior_attempt_comparison.md` — skill §2a / §3.2
- `.claude/memory/feedback_no_spoilers.md` — skill §3 step 3
- `.claude/memory/feedback_operating_principles.md` — skill §0 (the two principles)
- `.claude/memory/feedback_phase_exit_per_algorithm.md` — skill §5 phase-exit bullet
- `.claude/memory/feedback_phase_gated_blanks.md` — skill §2 / §5 Waiting Room
- `.claude/memory/feedback_read_before_asserting.md` — skill §3 (read before asserting *and* hinting)
- `.claude/memory/feedback_roi_promotes_to_curriculum.md` — skill §5 (ROI line)
- `.claude/memory/feedback_schedule_markdown.md` — **no current home**, same reason as
  `feedback_new_vs_retry.md` above: the bare-number-bullet escape guarded a "Carryover from this
  week" preview section that the current single-table schedule format no longer has.
- `.claude/memory/feedback_self_evaluation.md` — CLAUDE.md gate 5, **including the intervention ladder**
- `.claude/memory/feedback_spine_first.md` — skill §1a
- `.claude/memory/feedback_whiteboard_fidelity.md` — skill §3 step 2

## Superseded by a renamed/merged practice-repo file (retired here)

These package-only files were dropped when the practice repo renamed or merged the rule into a
file canonical now ships. Keeping them would fork one rule across a dead name and a live one.
The surviving file (named) carries the same content.

- `.claude/memory/feedback_turn_economy.md` — renamed → `feedback_answer_length.md`
- `.claude/memory/feedback_kickoff_table_links.md` — merged → `feedback_lineup_links_only.md`
- `.claude/memory/feedback_procedure_first.md` — folded into `feedback_teaching.md` (and skill §1)
- `.claude/memory/feedback_difficulty_tiered_intake.md` — merged → `feedback_intake_and_surplus.md`
- `.claude/memory/feedback_early_completion_backfill.md` — merged → `feedback_intake_and_surplus.md`
- `.claude/memory/feedback_surplus_triggered_intake.md` — merged → `feedback_intake_and_surplus.md`
  (`references/effort-budget.md` the unit model, `references/weekly-build.md` surplus at the build,
  `references/technique-coverage.md` weak-technique fill)
- `.claude/memory/feedback_batch_commits.md`, `feedback_git_commit.md`,
  `feedback_end_of_session_push.md` — all three merged → `feedback_commit_discipline.md`
  (CLAUDE.md gate 8 + SKILL.md §3 step 8 / `references/review-workflow.md` Step 8)
- `.claude/memory/feedback_proactive_scheduling.md` — merged → `feedback_schedule_integrity.md`
  (`references/review-workflow.md` Schedule integrity + `references/weekly-build.md` the tracker
  sweep). `feedback_schedule_mistakes.md` above (skill §4, out-of-order detection) merged into the
  same file — flagging as a related correction found while verifying this one, not separately
  requested this round.

## No longer declined — ships as its own file, not absorbed into the skill

- `.claude/memory/feedback_end_of_week_schedule.md` had a stale entry here claiming "skill §9 / §9a
  absorbed it." False: this file ships in canonical, byte-identical to the practice repo's copy
  (confirmed via `diff`). It was never a decline candidate; the line was simply wrong and is removed.

## Learner-state / agent-workflow — not coaching content

- `.claude/memory/feedback_execution_workflow.md` — global agent-workflow evidence, not coaching;
  it lives in `~/.claude/rules`.

## Local customizations that should stay local

- `AGENTS.md` — canonical's version is the general one (it points at the skill and covers
  both pillars). The practice repo's is a personal cut-down pointing at its own
  CLAUDE.md. **Sync direction is inverted for this file** — canonical is ahead.
- `scripts/pull_interview.py` — the only delta is comments renaming the example repo.
- `.githooks/pre-commit` — canonical's SSOT trigger also matches `cse.config.example.yml` (an
  adopter/template checkout has the example, not a live `cse.config.yml`); otherwise identical.
- `scripts/update_review_dates.py` — canonical keeps a `sys.path` guard so `import session_date`
  resolves when the module is imported (the shipped test harness), which the practice repo dropped.
- `scripts/check_single_source.py` — canonical falls back to `cse.config.example.yml` when the live
  `cse.config.yml` is absent (a template/adopter checkout before setup); the practice repo always has
  the live file.
- `.claude/memory/project_ai_pillar.md` — canonical ships a **genericized template**; the practice-repo
  version is personal state (dated roadmap). **Never sync down** — re-syncing re-introduces personal data.
- `.claude/memory/project_recognition_probes.md` — genericized template; practice version carries live
  unit figures and dated probe history. Never sync down.
- `.claude/memory/project_sd_mock_model.md` — genericized template; practice version names a private
  study repo and dated study state. Never sync down.
- `.claude/skills/cse-coach/references/motivation.md` — canonical drops a dangling
  `[[project_gamification]]` link; that memory file is learner state and does not ship.
- `docs/ARCHITECTURE.md` — canonical-only prose ("A fifth artifact: the generated data contract")
  describing `dashboard/progress.schema.json` as a source-tier artifact; the practice repo has no
  counterpart section to diff against.
- `docs/foundations/dsa/mastery/techniques.yml` — learner-owned: its `problems:` lists are the
  learner's own solved-problem history, deliberately outside `ENGINE_PATHS`. Its SCHEMA (the
  `doc:` join key, the `tier:` vocabulary, the zero-problem tier blocks) is hand-synced on every
  promotion instead — and it drifted silently from Sep 21 to Sep 23 because nothing reported it;
  see the promotion notes for this round.

These three are the only `project_*` files that ship at all (by explicit name in `ENGINE_PATHS`);
every other `project_*` file is learner data and stays out entirely.

## Genericized this round — permanently DIFFERENT by design (Sep 21/22/23 port)

These files were ported but with dated incidents / real problem numbers / private-repo names
softened for a template audience (CLAUDE.md's genericization rule). `promote_report` will keep
flagging them DIFFERENT forever, because it hashes content — that is expected, not an oversight.

- `.claude/hooks/problem_link_reminder.py` — one word-choice difference in a comment (quote-mark
  placement); no substantive drift.
- `.claude/hooks/rating_gate.py` — dropped a couple of "On 2026-09-19 …" / "Added 2026-09-20 …"
  dated-incident lead-ins in comments and one test-fixture date ("the Sep 21 call" → generic);
  the SUMMARY_CONTEXT/REPORT_CONTEXT fix itself is byte-for-byte the same logic.
- `.claude/hooks/session_start_memory.py` — the global-layer canary try/except and the `{canary}`
  field in `emit` are removed (the canary hook does not ship, see `global_layer_canary.py` below),
  along with the `sys.path.insert` that only served the canary import. The practice repo's
  `progress_banner` docstring adds a dated "Path note" and drops the "including a fresh template
  checkout, which has no dashboard/ yet" clause; canonical keeps the template-relevant clause and
  adds no dated note. The streak-liveness fix itself (`_STREAK_LIVE_GRACE_DAYS`,
  `_streak_is_live`, the liveness branch in `progress_banner`) is byte-for-byte the same logic.
- `scripts/check_schedule_integrity.py` — the module docstring's checks-3/4 table and the check-4
  header comment drop the specific incident citations ("the 2026-09-14 leak (84, 547)", "78
  Subsets", "1102/1631 Dijkstra") in favor of a generic description; the check logic itself is
  unchanged.
- `scripts/new_problem.py` — dropped one `(self_eval 2026-09-15)` citation to a private log entry
  that does not ship; the regex/logic fix is unchanged.
- `scripts/test_check_schedule_integrity.py` — every fixture (dates, LC numbers, titles) is
  invented; the practice repo's version is tuned against its own real current week (Sep 14/21,
  2026; problems 22/78/1552/55/332/34/39/46). Every adversarial trap shape (date, decimal unit
  count, approximate rep count, bare intake count, `+N` interval suffix, bare-numbered 🆕 row,
  pre-Daily-Schedule masking table) is preserved with neutral stand-ins.
- `.claude/skills/cse-coach/SKILL.md` — one line in §7 renamed a reference to the learner's private
  SD study repo to a generic description.
- `.claude/skills/cse-coach/references/scaffolding.md` — dropped a real incident date/numbers
  ("Sep 17, 2026 (dropped 560, then 721)" → generic) and a real CLI example date (`--date
  2026-09-14` → `--date <YYYY-MM-DD>`) in a pre-existing section this round also touched.
- `.claude/skills/cse-coach/references/weekly-build.md` — genericized several incident citations
  (a real multi-variant mixup's problem numbers, `self_eval` dated citations, "the 2026-09-14
  leak") and — the substantive change — **dropped the whole "How the Sunday close-out is RUN"
  subagent-orchestration section** (tech-lead/engineer split, `~/.claude/rules/execution-
  workflow.md`): that is the learner's personal multi-agent Claude Code workflow, not a coaching-
  engine concept. The two genuinely coaching-relevant passes it described (the standing self-eval
  meta-review pass, and the lean-daily-table format guardrail) are kept as plain checklist bullets.
- `.claude/memory/feedback_explanation_register.md` — genericized "mid-22 backtracking" (a real
  problem reference) to "mid-session", and dropped a `self_eval_log 2026-09-19` citation to a
  private log entry that does not ship.
- `decisions.yml` — ported the engine-concept entries (`banned-openers-to-hook`,
  `gamification-progress-platform`, `typo-self-fix-not-a-real-fix`, `eow-close-out-process-sep20`
  [genericized: dropped the execution-workflow-subagent clause and its `affects:` tag, kept
  weekly_build/complexity_gate/self_evaluation], `schedule-item-kind-tags-sep21`,
  `coach-gamification-promoted-sep21` [dropped citations to unshipped memory files]); **skipped**
  `hard-multiplier-1p3` (learner tempo calibration, see the effort_budget.py entry in the Oct 6 section below),
  `execution-workflow-global-sep21`, `execution-workflow-pyramid-sep21`,
  `enforcement-layer-versioned-sep21`, `role-gate-deny-hooks-sep21` (all learner-state /
  agent-workflow, not coaching — same reasoning as `feedback_execution_workflow.md` above).
- `scripts/build_cheatsheets.py` — the practice repo's `DOC_URL_TMPL` hardcodes
  `github.com/michael-yrao/cse-progress`; canonical derives the docUrl base from
  `git remote get-url origin` instead, since the package doesn't know an adopter's own
  GitHub owner/repo at authoring time. Citations of `docs/cse-coach/learn_cheatsheet_plan.md`
  ("the plan") are reworded to point at this module's own docstring / the patterns README.
- `scripts/check_cheatsheets.py` — same plan-doc citation rewording as above; logic unchanged.
- `scripts/test_build_cheatsheets.py` — same plan-doc citation rewording; test assertions
  unchanged (the golden test still reproduces `scripts/fixtures/cheat-sheets.seed.json`).
- `scripts/fixtures/cheat-sheets.schema.json` — same citation rewording in its `description`
  field.
- `scripts/fixtures/cheat-sheets.seed.json` — the 18 `docUrl` values point at
  `michael-yrao/cse-coach` instead of `michael-yrao/cse-progress`; everything else byte-equal.
- `docs/foundations/dsa/patterns/README.md` — "The machine-readable contract" section's plan
  link is reworded to point at `scripts/build_cheatsheets.py`'s module docstring instead.
- `.claude/skills/cse-coach/references/system-design.md` — the learner's private SD-study-repo
  name/URL is replaced with the `<your-sd-study-repo>` placeholder canonical already carries.
- `.claude/memory/feedback_coverage_gap_ledger.md` — same private SD-study-repo name/URL
  replaced with `<your-sd-study-repo>`.
- `.claude/memory/feedback_quantify_qualify.md` — same private SD-study-repo name/URL
  replaced with `<your-sd-study-repo>`.

## Genericized this round — permanently DIFFERENT by design (Oct 6 port, v0.8.0)

Same standing as the Sep 21/22/23 list above: ported with dated incidents, decision ids, real problem
numbers and author-data fixtures softened for a template audience; `promote_report` hashes content and
will keep flagging each of these DIFFERENT. The logic is the practice repo's, line for line.
Compared against `cse-progress` at HEAD `c4fb59e` (its working tree was being edited).

- `scripts/gamify.py` — dated-incident lead-ins ("Sep 21/26, 2026"), decision-id and unshipped
  memory-file citations (`schedule-history`, `feedback_session_dating`) and real problem-number
  examples (1216, 743, 39) in comments and docstrings replaced with generic wording; the dashboard
  payload logic is unchanged.
- `scripts/test_gamify.py` — dated-incident and decision-id citations (`*-sep26`, `*-sep27`) in
  docstrings and comments, the "no pytest/CI" remark, and author-data test rows rewritten as
  inline fixtures; every asserted branch is preserved.
- `dashboard/progress.schema.json` — `description` strings only: dated incidents ("Sep 21, 2026"),
  decision ids and the "~56 rows" author figure dropped; types, enums and `required` are byte-equal.
- `scripts/effort_budget.py` — real problem numbers (79, 452, 496), dated incident citations and the
  `schedule_priority.py` / decision-id references in comments genericized; **and** canonical keeps
  Hard 1.5 where the practice repo's default is Hard 1.3 (decisions.yml `hard-multiplier-1p3`), a
  learner tempo calibration with countervailing evidence unresolved, so it matches
  `cse.config.example.yml`. Permanently different on both counts.
- `scripts/links.py` — at full parity with the practice repo since v0.9.0 (`JUDGE_LABELS`,
  `judge_label`, the `SITE_*` constants); only comments and docstrings are genericized (decision ids
  and dated incidents dropped).
- `scripts/export_showcase.py` — decision ids folded to
  `dashboard-contract-exporters-oct6`, `project_gamification.md` citations dropped, and an empty
  `showcase.yml` / `bigo.yml` is a clean no-op (exit 0, nothing written, so the site keeps its
  fallback).
- `scripts/export_bigo.py` — decision ids folded to
  `dashboard-contract-exporters-oct6`, `project_gamification.md` citations dropped, and an empty
  `showcase.yml` / `bigo.yml` is a clean no-op (exit 0, nothing written, so the site keeps its
  fallback); it also tolerates an absent complexity-miss ledger.
- `scripts/export_practice.py` — decision ids folded to one canonical id; zero specs in `dsa/tests`
  writes nothing and exits 0.
- `scripts/export_manifest.py` — absent generated JSON is simply not listed; no manifest is written
  when there is no dashboard JSON to cover.
- `scripts/dashboard_indexes.py` — an absent `practice.json` / `showcase.json` is skipped rather
  than an error.
- `scripts/test_contract_schema.py` — author-data rows (`showcase/733.json`, the committed
  `practice.json`) replaced with inline fixtures, plus one empty-input case for the no-op
  behaviour above.
- `scripts/test_export_practice.py` — author-data rows (`showcase/733.json`, the committed
  `practice.json`) replaced with inline fixtures, plus one empty-input case for the no-op
  behaviour above.
- `scripts/test_export_manifest.py` — author-data rows (`showcase/733.json`, the committed
  `practice.json`) replaced with inline fixtures, plus one empty-input case for the no-op
  behaviour above.
- `scripts/test_showcase.py` — the verbatim check against the author's real `showcase.json` and
  the one test pinned to the author's 733 solution are dropped or made skip-until-generated.
- `scripts/test_bigo.py` — the verbatim check against the author's real data and the one test
  pinned to the author's 733 solution are dropped or made skip-until-generated; the
  absent-ledger case is added.
- `dashboard/showcase.schema.json` — title reads "cse-coach" not "cse-progress"; contract unchanged.

## Site half: contract exporters promoted (Oct 6, 2026), curation tools stay local

On Sep 23, 2026 the whole grounded-solutions showcase tooling was declined as "a display concern
of the site, not the engine". **Reversed Oct 6, 2026** (`decisions.yml`
`dashboard-contract-exporters-oct6`): the exporters, their schemas and their pre-commit gate now
ship, because an adopter's own dashboard is rendered by the same site. What was promoted:
`export_showcase.py`, `export_bigo.py`, `export_practice.py`, `dashboard_indexes.py`,
`export_manifest.py`, `contract_schema.py`, their `test_*.py`, the seven
`dashboard/*.schema.json` contracts, `requirements.txt`, and the `run_py` helper plus the
showcase / Big-O / practice / manifest blocks of `.githooks/pre-commit`. The decisions
`showcase-contract`, `bigo-contract`, `practice-contract`, `practice-contract-shapes`,
`dashboard-manifest-and-indexes-oct6` and `contract-schema-validation-oct6` are folded into the
one canonical entry rather than copied.

Still local, same reason as before (they curate the author's own picks or seed from the author's
site):

- `scripts/showcase_candidates.py` — the read-only tool that surfaces showcase candidates from
  the learner's own solution files.
- `scripts/seed_bigo.py` — seeds `dashboard/bigo.yml` once from the author's site metadata; an
  adopter's manifest starts empty.
- `scripts/test_seed_bigo.py` — tests the seeding script above, which does not ship; an adopter's
  manifest starts empty.
- `dashboard/showcase.yml` and `dashboard/bigo.yml` content — the author's picks. Canonical ships
  both empty (see their header comments); they are learner-owned and deliberately outside
  `ENGINE_PATHS`.

Shipped as-is, not declined: `.github/workflows/notify-site.yml` ships unchanged because
`fold-attempts.yml` and `weekly-build.yml` call it with `uses:`. It names the author's site repo, and
it is a no-op unless the learner sets the `SITE_DISPATCH_TOKEN` secret.

## Personal scheduling decisions (v0.9.0 port)

`decisions.yml` entries added to the practice repo between `c4fb59e` and `6d7b318` that record the
author's own calendar, tempo or agent workflow rather than an engine rule. They do not ship; the
engine-concept entries from the same range were promoted with dated incidents, real problem numbers
and learner quotes dropped. Ids are listed without a path, so none of these hides a file.

- `wedding-lite-oct18`, `wedding-lite-problem-count-oct18` — a temporary reduced-load window around
  one learner's life event, and the `wedding_lite` config block that drives it (declined below).
- `ceiling-from-below-wedding-oct10` — the same window's build-to-the-ceiling tempo.
- `dsa-mock-first-due-dec6-oct10` — moves one learner's first mock to a personal date.
- `sun-oct18-over-ceiling-for-3620`, `sun-oct18-wedding-lite-reseat`, `reseat-648-124-oct16`,
  `oct19-build-46-hold` — one-off reseats and holds of the author's own rows on named days.
- `retire-53-prefix-sum-oct12` — retires one variant of one problem in the author's tracker.
- `build-at-last-week-done-oct11` — sizes one build to the author's completed units that week.
- `coverage-recalibration-oct10` — the author's NC150 audit, learning-rate evidence and a list of
  problems the author declined to demote; its engine content (the coverage formula) already ships as
  `coverage-threshold-formula-sep27`.
- `backlog-forecast-rerun-oct7` — a history note of the author's own forecast run.
- `self-eval-meta-review-oct7` — the author's meta-review outcome, centred on a hook in the author's
  global `~/.claude`; agent workflow, not coaching (same reasoning as `feedback_execution_workflow.md`).

`intervals-split-four-ways-oct6`, `greedy-family-oct18`, `problem-link-order-oct09` and
`practice-link-label-po-oct10` were skipped in the first pass of this port and **promoted afterwards**
(genericized): `scripts/links.py` and `scripts/company_demand.py` now ship, and the starter
`techniques.yml` carries the split Intervals entries and the `greedy` family.

## Declined at the v0.9.0 port

- `.claude/hooks/global_layer_canary.py` — checks the author's own global `~/.claude` layer
  (rules, hooks, settings) is wired; it names files an adopter does not have.
- `.claude/hooks/tests/test_global_layer_canary.py` — tests the canary above, which does not ship.
- `docs/SETUP.md` — per-machine setup notes for the author's machines; the shipped `docs/HOOKS.md` covers
  adopter setup.
- `dashboard/cheat-sheets.schema.json` — outside `ENGINE_PATHS` by design: the cheat-sheets contract
  is checked by `scripts/check_cheatsheets.py` and the fixture schema under `scripts/fixtures/`.
- `cse.config.yml` `wedding_lite:` block — one learner's temporary reduced-load window (lines 176-188
  of the practice repo's config at `6d7b318`). Not ported, and no generic "lite period" is invented
  in its place; the other new config keys ship in `cse.config.example.yml` with neutral defaults.
  The practice repo's `intake_per_week: 0` and `carry_forward_min_streak: 1` are that window's
  overrides, so the example ships the engine defaults (2 and 2).
- `docs/foundations/dsa/mastery/techniques.yml` — still learner-owned and hand-synced. At v0.9.0
  the schema vocabulary was synced: the renamed `doc: dynamic_programming` join key (now on
  `1D Dynamic Programming`), the `greedy` family, the four-way Intervals split, and the `strings`,
  `math_sim`, `design` and `bit_manipulation` core families (names, `tier:` and `doc:` keys, empty
  `problems:` lists) that `company_demand.py` maps tags onto. The practice repo's `builds_on:` graph,
  the binary-search axis entries, the declared roadmap problems and the `queued` / `planned` header
  notes are the author's vocabulary and are not copied into the starter file.

## Genericized this round — permanently DIFFERENT by design (Oct 19 port, v0.9.0)

Same standing as the Oct 6 list above: ported with dated incidents, decision ids, real problem
numbers, private-repo names and author-data fixtures softened for a template audience;
`promote_report` hashes content and will keep flagging each of these DIFFERENT. The logic is the
practice repo's, line for line, unless a bullet says otherwise. Paths already listed in an earlier
section (`effort_budget.py`, `gamify.py`, `export_*.py`, `new_problem.py` and the like) keep that
bullet; the Oct 19 changes to them are comment-level in the same way.

Scripts and their tests

- `scripts/test_session_date.py` — ported as `scripts/test_session_date_override.py`, because
  `tests/test_session_date.py` has the same basename and pytest aborts collection on duplicate
  basenames.
- `scripts/build_week.py` — the module docstring's "dropped in headless mode" list ends at the SD
  slot; the practice repo's list also names the author's personal lite-period setting, which does not ship.
- `scripts/company_demand.py` — the default company roster is generic (edit it to your own target
  companies); the dated vocabulary-dump comments and the pointer to the author's private career
  strategy file are dropped.
- `scripts/test_company_demand.py` — builds its tracker, `techniques.yml` and study guide inline
  (`setUpModule`) instead of reading the checkout; `LiveVocabularyTests` still checks the shipped
  `techniques.yml`.
- `scripts/backlog_forecast.py` — `TALLY_FROM_STAMP` is `"00000000"` (every archive counts); the
  practice repo's value is the author's own start stamp. Comments reworded to match.
- `scripts/pattern_sense.py` — an empty deck file exits 0 and writes nothing (the site keeps its
  fallback), and the optional input files may be absent; the decision-id citation is dropped.
- `scripts/test_pattern_sense.py` — adds the empty-decks and missing-file cases for the behaviour
  above.
- `scripts/test_check_practice_spec.py` — `Real9001SpecTests` is dropped; it reads the author's
  `dsa/tests/9001_*.yml`.
- `scripts/contract_schema.py` — the missing-jsonschema hint says `py -m pip install -r
  requirements.txt` and exits through `SystemExit` with it.
- `scripts/meta_review_digest.py` — dated review citations and the author's log size dropped from
  docstrings and output text; the digest logic is unchanged.
- `scripts/remaining.py` — a dated self-eval citation and a real date example in comments dropped;
  logic unchanged.
- `scripts/test_remaining.py` — fixture dates are neutral stand-ins.
- `scripts/test_effort_budget.py` — fixture dates are neutral stand-ins.
- `scripts/restore_history.py` — a dated incident (a real problem number and dates) in a docstring
  is described generically; logic unchanged.
- `scripts/session_date.py` — one comment cites no private log entry; logic unchanged.
- `scripts/technique_coverage.py` — one docstring drops a dated learner quote; logic unchanged.
- `scripts/test_technique_coverage.py` — dated references and the "no pytest" remark dropped from
  the docstrings; assertions unchanged.
- `scripts/test_update_review_dates.py` — comment wording only (the practice repo's copy has a
  formatting typo, `rows =uprd...`, fixed here).
- `scripts/test_links.py` — a source-encoding difference only (a literal `·` instead of its
  `·` escape); the same assertions.

Dashboard schemas

- `dashboard/big-o.schema.json` — `title` reads "cse-coach" not "cse-progress"; the contract is byte-equal.
- `dashboard/manifest.schema.json` — `title` reads "cse-coach" not "cse-progress"; the contract is byte-equal.
- `dashboard/pattern-sense.schema.json` — `title` reads "cse-coach" not "cse-progress"; the contract is byte-equal.
- `dashboard/practice-index.schema.json` — `title` reads "cse-coach" not "cse-progress"; the contract is byte-equal.
- `dashboard/practice.schema.json` — `title` reads "cse-coach" not "cse-progress"; the contract is byte-equal.
- `dashboard/showcase-index.schema.json` — `title` reads "cse-coach" not "cse-progress"; the contract is byte-equal.
- `dashboard/showcase-problem.schema.json` — `title` reads "cse-coach" not "cse-progress"; the contract is byte-equal.

Hooks and the pre-commit script

- `.claude/hooks/commit_push_gate.py` — the dated list of incidents that motivated the gate is
  described generically, the reference to the author's global `role_gate.py` is dropped, and
  `DENY_REASON` names the commit-and-push gate instead of a CLAUDE.md gate number; the deny logic
  is the same.
- `.claude/hooks/kickoff_scaffold_reminder.py` — dated incident lead-ins in the docstring and
  comments (a real date and problem number) reworded generically; the trigger regexes are the same.
- `.claude/hooks/tests/test_kickoff_scaffold_reminder.py` — fixture dates ("Mar 12" and the like)
  are neutral stand-ins; every asserted branch is preserved.
- `.claude/hooks/tests/test_session_start_memory.py` — fixture dates are 2027 stand-ins; every
  asserted branch is preserved.
- `.githooks/pre-commit` — comments only, apart from the SSOT trigger that also matches
  `cse.config.example.yml` (recorded under "Local customizations" above): dated incidents and the
  wording that names the author's private study material are reworded. That earlier bullet's path
  has no extension, which `promote_report`'s declined-path parser cannot read, so this file stays
  in the report.

Pattern docs

- `docs/foundations/dsa/patterns/data-structures/graph.md` — a dated correction note and a problem
  number dropped from one table row; a blank line differs.
- `docs/foundations/dsa/patterns/techniques/backtracking.md` — the dated "added ... via <problem>"
  heading note and the dated miss history in the complexity trap are reworded generically.
- `docs/foundations/dsa/patterns/techniques/dynamic_programming.md` — dated, problem-numbered trap
  and example citations reworded ("a 1D DP primer", no problem numbers); content otherwise equal.

Skills and references

- `.claude/skills/cse-coach/references/dsa-mock.md` — the link to the unshipped
  `project_dsa_mock.md` is dropped and the `first_due` anchor names `cse.config.yml`.
- `.claude/skills/cse-coach/references/effort-budget.md` — the dated "complexity re-asks" heading
  date and the `wedding_lite` section (one learner's reduced-load window, declined above) are dropped.
- `.claude/skills/cse-coach/references/output-quality.md` — the private SD study repo is named
  generically.
- `.claude/skills/cse-coach/references/retry-and-restore.md` — dated incident citations and real
  problem numbers dropped.
- `.claude/skills/cse-coach/references/review-workflow.md` — dated incident citations and the
  learner's quote dropped.
- `.claude/skills/cse-coach/references/spaced-repetition.md` — a dated annotation on the
  rating-ignores-Big-O rule dropped.
- `.claude/skills/cse-coach/references/technique-coverage.md` — the site is named generically and
  a real external-judge example title is replaced with a placeholder.
- `.claude/skills/effort-units/SKILL.md` — "cse-progress" reads "this repo"; dated incident
  citations dropped.
- `.claude/skills/scheduling/SKILL.md` — "cse-progress" reads "this repo"; the `wedding_lite`
  steps (one learner's reduced-load window, declined above) and dated citations dropped.
- `.claude/skills/practice-problem/SKILL.md` — "cse-progress" reads "this repo"; personal problem
  numbers dropped.
- `.claude/skills/practice-problem/references/solution.md` — "cse-progress" reads "this repo";
  personal problem numbers dropped.
- `.claude/skills/practice-problem/references/spec.md` — "cse-progress" reads "this repo"; personal
  problem numbers dropped.

Memory

- `.claude/memory/feedback_ask_complexity.md` — dated annotation on the rating-ignores-Big-O rule dropped.
- `.claude/memory/feedback_concept_primer.md` — a dated note about the author's own roadmap dropped.
- `.claude/memory/feedback_lineup_links_only.md` — dated notes and self-eval log citations dropped.
- `.claude/memory/feedback_positive_phrasing.md` — dated learner quote and incident dropped.
- `.claude/memory/feedback_reps_over_drills.md` — the dated incident with real problem numbers and
  the learner's quote dropped.
- `.claude/memory/feedback_site_plain_language.md` — dated learner quote and the real study-guide
  figures dropped.

