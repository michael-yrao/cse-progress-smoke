---
name: cse-init
description: >-
  First-run setup / scaffolding for cse-coach. Use when a learner is setting up
  the repo for the first time ("set me up", "/cse-init", no cse.config.yml yet),
  or wants to scaffold cse-coach into an existing practice repo. Runs the
  conversational intake, writes cse.config.yml, generates the roadmap and week-1
  schedule, and installs the git hook.
---

# cse-init — first-run setup & scaffolding

> STUB — full logic lands in build step 6 (bootstrap). The behavior below is the
> contract; `scripts/bootstrap.py` implements the mechanical parts.

When there is no `cse.config.yml`, run setup:

1. **Present all questions at once** (single warm block, coach voice — see the
   cse-coach skill's voice guideline): name, start date, target (default
   `competitive`), solution language (default Python), which pillar leads. Do **not**
   ask for a daily load: the effort budget prices days in *units* (see
   `references/effort-budget.md`), and the legacy `daily_cap` is read by nothing. Do **not** ask for a
   `reach_beyond` number — tell them they'll always
   train at least one tier past their target because that's what makes it stick.
2. After they answer, if they chose to lead with System Design before the
   readiness gate, push back kindly (SD study is theirs to start any time, but the
   coach's scored mocks recommend a DSA foundation first); proceed only on explicit
   override (record it).
3. Write `cse.config.yml` (from `cse.config.example.yml`).
4. Generate the personalized `study_guide.md` roadmap from the chosen curriculum tiers
   projected onto `start_date`. Week 1 comes from `scripts/build_week.py` (bootstrap runs
   it), not a hand-built file.
5. Reset the trackers to header + seed row; empty the logs.
5a. **Scaffold `.claude/memory/`** — `MEMORY.md` (the index the coach reads at every session
   start) and an empty `self_eval_log.md`. This is the **destination** for the
   self-evaluation loop (CLAUDE.md always-on gate 5 + `docs/ARCHITECTURE.md`): corrections land in the log, recurring ones get
   promoted into rule files here, and the folder is **committed** so behavior learned on one
   machine follows the learner to every other. Without it, "promote into standing behavior"
   has nowhere to write and every lesson is re-learned from scratch.
6. **Do the git setup for them** — the learner runs no git commands. If the repo
   isn't initialized yet, run `git init`, then `git config core.hooksPath .githooks`
   to activate the tracker hook. (`bootstrap.py` does both.) The only thing the
   learner ever invokes is setup itself.
7. **No editor setup — the retry blank page is built in.** On a retry, `new_problem.py`
   physically moves prior attempts out of the file into a `<root>/.history/` stash, so the
   file opens blank in *any* editor, on GitHub, and in a plain `git diff` — no VSCode
   config, no extension, nothing to reproduce per machine. `restore_history.py` pastes the
   history back at session end (`references/retry-and-restore.md`). There is nothing to install here.
7a. **Set up the progress dashboard.** Create the `dashboard/` directory, then run
   `python scripts/gamify.py` once to write the first `progress.json` +
   `progress-summary.json` (the pre-commit hook keeps them current after every rep, so this
   is a one-time seed, not something the learner repeats). Also run
   `python scripts/build_cheatsheets.py` once so `dashboard/cheat-sheets.json` exists.
   Tell them their dashboard URL is
   `https://progressiveoverflow.com/progress?repo=<owner>/<name>` — it only works once the
   repo is **public**; while it stays private, mention that quietly and move on (see
   `references/motivation.md`).
8. Sign off in the same voice: name tomorrow's first problem and remind them the
   only report you ever ask for is "Clean, Shaky, or Blank?"

**Drop-in mode:** to scaffold cse-coach into an existing repo, copy `.claude/`,
`scripts/`, `.githooks/`, `cse.config.example.yml`, and the `docs/foundations/`
scaffold (which carries the editor templates), then run the same setup.
