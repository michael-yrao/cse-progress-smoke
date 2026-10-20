<!-- reconciled: 2026-09-25 -->
# LeetCode review workflow — gate detail

**Open this** for any problem discussion. That means solving, reviewing, or the learner mentioning a
problem by number or name. **Not for** setting the file up (`scaffolding.md`) or the weekly
close-out (`weekly-build.md`). **Not a tempo to impose** — it's the checklist for closing a
rep correctly; the learner sets when to move on (SKILL.md principle 3).

The step spine is in SKILL.md §3. This file carries the gate detail and the "why".

## Step 0 — Recognition gate (before any solution code)

Have them state **shape → technique → the one feature that picks it** over the nearest
neighbour. For example: *weighted* edges → Dijkstra not BFS; marking *edges* visited not nodes → Eulerian
not Hamiltonian. If they already wrote a pre-code comment, **that comment IS the call** —
confirm or correct it before they code.

- ⚠️ **The learner writes the call.** The coach must not lead. When you prompt verbally, name
  only the **shape cues** and ask for the technique — **never list candidate techniques.** A
  leading multiple-choice (*"monotonic deque or a heap?"*) hands over the answer (the spoiler
  that leaked on 239, Aug 20). The scaffold no longer prints a RECOGNITION block (removed
  Aug 22, 2026) — the anti-spoiler purpose rests on the top-comment habit plus this rule.
- ⚠️ **The top-of-method comment IS the call.** The block is optional (Aug 21, 2026). Read
  the top comment as the call; never re-demand a scaffold block, never read a blank block as a
  missing gate. Being asked to use a form is what makes them route around it. Don't build a
  mechanism to police comment order. Enforcement is trust-based; the ungameable measure is the
  **cold hit rate over ~15 label-stripped probes**, not per-rep policing.
- **Log the call either way.** Hit AND miss each get one dated line in the miss ledger. A miss-only
  ledger has no denominator: "no entries" and "never asked" look identical. Found Aug 9, 2026:
  two entries in six weeks, no way to tell a clean streak from an unfired gate.
- **Front-gate vs back-gate:** this is the front-gate, the complexity gate is the back-gate.
  Recognition is what the interview grades in its first two minutes; solving a problem you were
  *told the name of* never trains it.
- ⚠️ **A retry half-spoils this.** The tracker row names the method and the folder names the
  pattern. The *measured* recognition reps are **new problems**, **weekly probes**, and **cold cues**
  (a statement fired with its label stripped). Fire the gate on retries anyway, for the habit.
  Do not read a retry hit as evidence for phase exit.

full rule: [`recognition_gotchas.md`](docs/foundations/dsa/mastery/recognition_gotchas.md),
[`feedback_recognition_gate.md`](.claude/memory/feedback_recognition_gate.md),
[`project_recognition_probes.md`](.claude/memory/project_recognition_probes.md); `decisions.yml`
`recognition-block-removed-from-scaffold`, `recognition-call-is-the-top-comment`.

## Step 1 — Complexity gate (before any rating is proposed)

Ask for **time AND space, each with an itemized why-clause** ("O(1), one fixed 26-array" — not
a bare "O(1)"). Don't move on until they answer or explicitly pass.

- **It exists to surface the miss**, not to gate the rating. The rating no longer considers
  complexity at all. Asking is still mandatory because it's the only way a miss
  gets caught, carded, and queued for the end-of-week cleanup. It's also mandatory because
  volunteering it unprompted is the interview habit being trained. Skipping the ask still leaves the learner
  confirming on incomplete information — the miss just goes uncaught, not uncapped.
- **It fires on the rep, not the ritual.** A session arriving as "what's wrong with my code"
  with no scaffold or kickoff is still a rep. If you're about to propose a rating, it's overdue.
- ⭐ **A Big-O miss never caps the rating.** This supersedes the earlier
  clean-code-only waiver. Rate on recognition + code only. A wrong, prompted, or
  taught complexity bound never lowers or caps the rating. This holds on any rep, not just a
  clean one. Always still correct the miss and ledger it, then **queue the missed bound in the
  end-of-week complexity cleanup**, re-asked cold at the close-out (`weekly-build.md`). A real
  fix to the *code* can still affect the rating through the code criterion. That's the code
  being shaky, not the complexity miss capping it.
- **Before correcting the learner's bound, prove yours.** Apply the problem's constraints to both
  bounds first. Then name a worst-case input that forces the bound you are about to claim, or count
  the operations by running the code. For space, price what each stack frame holds, not only how
  many frames there are. When a complexity rule is taught for the first time, search `stuck_log.md`
  for earlier entries on the same technique and correct any that contradict it.

full rule: [`complexity_gotchas.md`](docs/foundations/dsa/mastery/complexity_gotchas.md),
[`feedback_ask_complexity.md`](.claude/memory/feedback_ask_complexity.md); `decisions.yml`
`complexity-cleanup-formalized`, `rating-ignores-complexity`.

## Step 2 — Stuck? Read their solution file before hinting

Not before *asserting* — before **hinting**. It is one tool call and it is free. On 540
(Jul 27) coaching started immediately: worked array, indices, the pair-start parity rule. The
learner already had `m % 2 == 0` in the file. Handing over something they'd derived wastes
the rep and is a spoiler. It then contaminated the *rating*: 🔴 was proposed on a false premise
and the learner had to correct the person rating them. Ratings set intervals, so an unverified
premise here outlives the session. 3+ occurrences (Jul 25/27/29).

**A claim about what the learner's code does, lacks, or costs is read from that code, not from a
proxy.** Read the whole file before saying something is absent from it, and the dated attempt under
discussion before naming which implementation it uses. Check a local statement's edge case against
LeetCode's current constraints before calling it a failure, and count a structure's size under the
code as written before correcting a bound.

**Struggling with a technique? The remedy is the next real rep.** Do not offer a no-code drill or a
detached exercise in its place. The learner learns by doing the problem again and asking questions
as they come up. Answer those questions in full, then let the schedule bring the problem back.

full rule: [`feedback_read_before_asserting.md`](.claude/memory/feedback_read_before_asserting.md),
[`feedback_reps_over_drills.md`](.claude/memory/feedback_reps_over_drills.md).

## Steps 3–5 — Mark, rate, log

3. Mark the problem completed in the current week's schedule table.
4. **Infer the comfort rating, propose it plainly for confirmation** — don't ask an open "how
   did that feel?" when the transcript answers it. Judge from what you watched: how many hints,
   whether they self-caught bugs, whether they derived the approach. Propose + log on their
   yes/override — never silently. Comfort is self-reported, so their call is final; honesty over
   agreeableness. If they claim 🟢 but you supplied a real fix they missed (or it was a no-code
   rep), say so, then defer. The **rating rationale is not length-capped**: propose + why, in
   full. Scale + ladder: `spaced-repetition.md`. full rule:
   [`feedback_infer_comfort.md`](.claude/memory/feedback_infer_comfort.md).
5. Update `docs/foundations/dsa/mastery/dsa_progress.md`; the pre-commit hook recomputes dates.
   Log non-Clean in `stuck_log.md`. A 🔴 entry is full: where stuck, core realization, snippet.
   A 🟡 entry is a one-liner: sticking point only. Add the problem to `techniques.yml` in the
   same edit (see `technique-coverage.md`).

## Site-completed reps

A rep marked complete on the site's practice page arrives in `dsa/attempts/<YYYYMMDD>/`. The `fold-attempts`
GitHub Action runs `python scripts/fold_attempt.py --apply --all` on every push to `dsa/attempts/**`. It
does the fold, the tracker row (the rating ladder from `spaced-repetition.md`), the schedule strike,
pull-in or late-completion placement, the next review when it falls in the same week, the complexity
queue row and the recognition-miss entry, then commits through the pre-commit hook and pushes.
The workflow is `.github/workflows/fold-attempts.yml`. Each attempt folds as one transaction: a refused
attempt is restored, logged as `refused:`, and stays in the inbox; later attempts still fold.

- **The rating is the learner's own**, picked on the site. It is logged as given; never propose or adjust it.
- **The complexity question is asked on the site**, before the rating: time and space, each with a why. The
  fold judges the labels against `bigo.yml`. On a match nothing is queued. A mismatch or a no-reference
  row goes to the cleanup queue in `complexity_gotchas.md`, and the first Sunday complexity block takes
  those only.
- **A missing top-of-method call** (`recognition: missing`) is logged as a recognition miss in
  `recognition_gotchas.md`.
- **Unfinished saves stay in the inbox.** The script refuses them.

**Stays manual:**

- Retirement 🎓 to 🏆: the Action names a candidate in its job summary; the coach decides.
- A failed job: a blocking check (exit 2) pushes nothing. Fix the cause, then fold by hand with
  `python scripts/fold_attempt.py --apply <inbox path>`.
- An attempt the fold refuses: it stays in the inbox; the coach folds it by hand.

List the inbox with `python scripts/fold_attempt.py --pending`.

`decisions.yml` `practice-site-reps-oct18`, `practice-site-complexity-oct19`, `practice-site-fold-action-oct19`.

## Schedule integrity

**Any lineup or restate table you present** (mark-completed step, "what's next", hand-over) is **problem
name + links only**. Build from `python scripts/remaining.py` (a day's board) or `python scripts/links.py <n> ...` (a named hand-over), no Note/Focus/technique/comfort column
(it spoils the recognition gate). See `scaffolding.md` → "Presenting the kickoff / lineup board".

When a problem is dropped or deferred, **a new specific slot is assigned in the same edit**.
Never remove a problem without immediately adding it to another day. A deferred problem with no
new date is a missed problem. Every row that moves off a day, started or not, stays on
that day, unstruck, with its new date in Next, prefixed `←` when it moved to an earlier day and
`→` when it moved to a later one (the copy on the destination day carries the same arrow). The day's plan is a record of what was
planned, never rewritten after the fact. The moved row is not billed on that day (effort-units skill). Its header pins the plan once (` · planned X units`). `check_schedule_integrity.py` reports a row that vanished from a started day since HEAD, and a started day whose header dropped with no planned figure. After logging any result, add its computed next-review date to the
appropriate week's schedule (this week or further out). Don't leave it only in the tracker. The
spaced-repetition dates are the source of truth; the schedules must reflect them. When the
target week's file doesn't exist yet, note the problem in the nearest schedule's preview section.
Spread across available slots rather than stacking on already-heavy days.

⭐ **The near half is checked, not remembered (Aug 21, 2026):**

```sh
python scripts/check_schedule_integrity.py          # current week: done rows vs the tracker
python scripts/check_schedule_integrity.py --check  # exit 1 on a finding
```

Runs from the pre-commit hook when a tracker or schedule file is staged. Reports two things: a
**struck row missing its `End`/`Next`**, and a **rep the tracker dates inside this week whose
row is not struck**. ⚠️ It does **not** verify every future date is pre-placed. Distant dates
are *pulled* by the weekly build's tracker sweep, so that reading would report ~73 of 115 healthy
rows. The paragraph above is still yours to run.

## Step 8 — Ask before every commit and every push

Make the edits, say what is staged, and **stop**. Accumulate edits across the session; they land
in one commit when the learner says so. Commit early only if the learner is about to switch
machines or the session ends unexpectedly — and then *say so and ask*, never decide unilaterally.
The normative rule lives in the always-injected CLAUDE.md (that copy wins); this is the workflow
step. full rule: [`feedback_commit_discipline.md`](.claude/memory/feedback_commit_discipline.md).
