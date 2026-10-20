---
name: project_ai_pillar
description: AI Engineering as an optional THIRD pillar, PARKED behind a measured trigger (DSA must lighten first); when activated it is active/scored/spaced like SD, off-board and unpriced.
metadata:
  type: project
reconciled: 2026-09-12
---

<!-- TEMPLATE. This is the package's generic parked-AI-pillar model. It ships OFF by default:
     nothing here is wired into cse.config.yml, no tracker exists, no schedule slot is placed.
     A learner personalizes it (activation state, dates, roadmap) only if and when they turn the
     pillar on. Keep personal state OUT of this file — it is a shipped template, not a live log. -->

**Status: PARKED / OPTIONAL.** AI Engineering is available as a planned third pillar but is **not
started by default**. It activates only when DSA capacity frees up. It is active, scored, and spaced
like the System Design pillar — see [[project_sd_mock_model]]. Ties to [[project_interview_goal]].

**Why parked, not running:** during the heaviest DSA phases a third pillar is additive load with
nowhere to go. The failure mode a parked pillar defends against is *"a plan nobody executed"* — so it
does not start until there is real budget room, and when it does start it is active and scored, never
passive reading.

## Activation trigger (measured, not a date)

Activate at a **weekly build** when BOTH hold:
1. the heavy DSA phases (e.g. DP / Backtracking) have **closed** on the roadmap, and
2. `effort_budget.py` shows **real evening headroom** for a sustained stretch (well under the ceiling
   for two consecutive weeks) — re-derived from the live budget, not guessed. Same ethos as
   [[feedback_midweek_reprice]].

The weekly-build checklist carries the firing step ("if AI still parked, test the trigger"). Until
then, **do not nudge AI** — the same discipline as SD study-mode in [[project_sd_mock_model]].

## On activation — the model

Mirrors the SD pillar: **off-board and UNPRICED** (takes the evening, not the DSA ceiling),
cadence-driven, learner-does-the-work / coach-assesses, its own tracker.

- **A "rep" is active, not reading:** do the work, then produce a small **assessed artifact** — a cold
  explanation of the mechanism plus one modification. The coach probes it cold, reusing the SD drills
  ([[feedback_quantify_qualify]], [[feedback_hld_altitude]], [[feedback_expand_acronyms]]). Comfort and
  spaced re-touch reuse the existing engine.
- **Interview-prioritized ordering** when the goal is interview prep: setup → model APIs → evals → RAG
  → agents → ML system design (the bridge to SD) → then depth.

**NOT built until activation** (avoid premature scaffold, honor single-source): the
`references/ai-engineering.md` skill reference, an `ai_progress.md` tracker, and any `cse.config.yml`
cadence key are created **only on activation** — add a config key only when it holds a live value.
