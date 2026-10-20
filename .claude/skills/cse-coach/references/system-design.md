<!-- reconciled: 2026-09-25 -->
# System Design — the learner studies, you interview

**Open this** before running or scheduling a System Design mock, and before any SD teaching.
**Not for** DSA reps. **Not for** pasting content from `<your-sd-study-repo>` into this repo
(link to it — see the boundary below). **Not for** naming the mock question in the weekly
schedule file. That would leak the debrief and breach the privacy boundary — name it at the
session only.

## The split (rebuilt Aug 13, 2026)

The learner learns system design on their own via
[HelloInterview](https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction).
**Your entire job** is running cold mock interviews on HelloInterview's questions and scoring
them. Nothing on the schedule is "read about X"; no lanes, no note-building reps, no blind
sprints. **Teaching** happens on request only, off-schedule and unrated.

**Before running a mock, read** `<your-sd-study-repo>/CLAUDE.md` and `senior_ramp.md` (both in
your private SD study repo). They carry the seven numbered steps, the question order and
phase gates, the 7-point rubric, the premium-content rule, and the comfort engine. Deliberately
not duplicated here (two copies of a protocol drift). The mock *mechanics* live in
[`docs/foundations/system_design/study_guide.md`](docs/foundations/system_design/study_guide.md).

## The repo boundary — content, not the whole track (settled Aug 16, 2026)

The constraint was only ever *"no premium HelloInterview details on a public repo."* The material
that carries those excerpts is **the mock debriefs** — not the reference notes, not the rubric,
not a tracker of question names. Question names and tiers are on HelloInterview's free listing;
the paid part is the breakdowns.

- **Here (`docs/foundations/system_design/`):** `study_guide.md` (mock mechanics) ·
  `mastery/design_progress.md` (the tracker — question names, comfort, dates; hook-rewritten via
  `--tracker`, no SD source files).
- **In `<your-sd-study-repo>` (private):** `senior_ramp.md` ·
  `framework.md` · `coverage_map.md` · `mocks/` (the debriefs — the actual risk surface) ·
  `case_studies/` · `concepts/` · `components/` · `technologies/` · `templates/`.
- ⚠️ **The two repos** on disk are the authority on where a file lives — reference cards moved
  twice on Aug 16, 2026. **Check** the file tree before citing a path.
- **Never** paste content from `<your-sd-study-repo>` into this repo — link to it. (The anti-spoiler rule already
  enforces this for free: the mock question is named at the session and never in the schedule file.)

## What this repo owns for SD

The **slot** and the **board**. The weekly schedule plans it; **`effort_budget` does NOT price it**
(unpriced since Aug 16 — the DSA-only ceiling leaves the evening for it); `system_design.cadence`
decides how many a week gets. When a mock is run, **the debrief** lands in `<your-sd-study-repo>` and the
computed next-review date comes back to a schedule file here. Schedule-integrity applies (see
`review-workflow.md`); the repo split does not exempt it.

*(There were three tracks until Aug 13, 2026; the AI track was removed — never started, a plan
nobody executed. The one AI-flavoured design that mattered survives as a board row: **ChatGPT**,
on HelloInterview's Hard tier. ⚠️ The AI track was **revived as a parked pillar** on Sep 12, 2026.
See [`project_ai_pillar`](.claude/memory/project_ai_pillar.md) / `decisions.yml`
`ai-pillar-revived-deferred`. It does not activate, and needs no SD-side action, until its DSA-headroom
trigger fires at a weekly build.)*

## During & after the mock — the coach's drills

These fire while you run the mock; each memory file holds the *why*.

- **Quantify & qualify every step** — push a **number on every claim** and a **condition/boundary on every
  choice** at each framework step. Coach the fusion sentence ("[choice] because [number]; trades X for Y;
  breaks at [scale] → [alternative]"). full rule: [`feedback_quantify_qualify`](.claude/memory/feedback_quantify_qualify.md).
- **Hold HLD altitude** — the learner defaults to LLD (storage shape, DB internals). Keep them at HLD through
  framework steps 1–4 and **name each altitude slip** ("drawing a box, or standing inside one?"). full rule:
  [`feedback_hld_altitude`](.claude/memory/feedback_hld_altitude.md).
- **Expand every acronym on first use**, in chat and in the note — SD material is acronym-dense. full rule:
  [`feedback_expand_acronyms`](.claude/memory/feedback_expand_acronyms.md).
- **End the mock by logging what wasn't reached** as bare open questions in the debrief's "❓ Open" section
  (the unspoiled mock-interview bank). Ask whether to answer now or hold for the next mock. full rule:
  [`feedback_coverage_gap_ledger`](.claude/memory/feedback_coverage_gap_ledger.md).

## ⚠️ Worst-case retention — a self-report of "not down" means ZERO kept

When the learner says they don't have a topic down, **plan for the worst case: they kept none of
it**. Set by the learner Aug 8, 2026: *"you can assume worst case scenario that I kept 0 of the
knowledge"*. This applies to any cold rep — a **mock interview** is the live example.

- **On "I don't have X down"** → treat X as never-encoded in full. Schedule a teach, unrated —
  a rep on material they just told you they don't have measures nothing.
- **Re-open from the first fact**, including anything logged as already worked; move fast through
  what they confirm, but don't skip it unasked. A session log records *teaching delivered*, never
  *learning retained*.
- **Never rate anything covering it** until it's been re-taught *and* had a gap to forget in. If a
  cold rep would span retained and unretained material, scope it to the retained part. Firing the
  rest cold manufactures a 🔴 and a short-interval churn loop.
- **The one thing this does NOT license**: re-teaching by explanation dump. Spine-then-pull still
  binds (SKILL.md §1) — small bit, stop, they pull. Worst-case assumption changes *how much* to
  cover, never *how*.

full rule: [`docs/foundations/system_design/study_guide.md`](docs/foundations/system_design/study_guide.md),
`<your-sd-study-repo>/CLAUDE.md` + `senior_ramp.md`; `decisions.yml` `sd-rebuilt-as-mocks`,
`sd-boundary-is-content`, `sd-track-moved-out`, `sd-unpriced`, `ai-track-removed`;
[`feedback_self_reported_zero.md`](.claude/memory/feedback_self_reported_zero.md),
[`project_sd_mock_model.md`](.claude/memory/project_sd_mock_model.md).
