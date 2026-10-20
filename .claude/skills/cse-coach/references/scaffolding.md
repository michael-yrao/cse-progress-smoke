<!-- reconciled: 2026-10-19 -->
# Scaffolding a problem

**Open this** before you create or set up any problem file for the learner.
**Not for** retries' prior-attempt handling — that's `retry-and-restore.md`. **Not for**
writing any solution logic. The script writes the scaffold only; the learner writes
everything, including any `ListNode`/`TreeNode` defs (whiteboard fidelity — no shared
data-model imports).

Set the file up **before** they start — never make them create it or paste the statement.

## Scaffold scope follows what the learner named — batch only on a kickoff

- **A message naming specific problems scaffolds exactly those.** "I'll do 235", "let's
  do 417 and 543", "235 next", "doing 332", "I'm doing 332 right now", "doing 332 from
  tomorrow" → scaffold those, and nothing else. A day named with "from" is the source of a
  pull; the rep is in the live session, so reseat (effort-units) and scaffold in the same turn.
  - ⚠️ **A problem name narrows scope** ONLY when NO session-start phrase shares the message.
    "let's start our friday session, graduate merge sorted list" is a **kickoff**. The
    session-start phrase governs, and the named problem is a *priority* (which rep to lead
    with), not a scope-limiter. Scaffold the WHOLE board. Do not let a named problem downgrade
    an explicit kickoff to a single-problem request. Do not override the
    `kickoff_scaffold_reminder.py` flag with your own read. This was caught Sep 18, 2026: the hook
    fired, the read overrode it, and only 21 got scaffolded.
- **Batch the whole day only on a real kickoff.** That means an explicit "start today" / "start
  (this/the) session" / "start `<day>` session" / "what's up today" / `/start-day`. It also covers
  a first message that asks for *the day* rather than for a problem. **"Start session" is a
  kickoff**, not a bare session-start greeting. Scaffold the day's whole board. This was caught
  Sep 12, 2026 on "start saturday session": the board was presented, but scaffolding didn't
  happen. On a kickoff, scaffold **every** problem on the day's schedule. That means the active
  block *and* both warmup slots, 🔴/🟡/🟢 alike. All of it happens in one batch. (This repo
  overrides the cse-coach default of files-only-for-coding-reps.)
- **A named problem is a request, not a kickoff.** Do not infer a kickoff from "first
  message I've seen today," and don't batch because it's cheap. If genuinely ambiguous,
  scaffold what they named and *ask* before batching the rest.
- **A pull the learner recalls** but the record does not show is a NEW pull. It is not a
  restore. Before scaffolding it, check the technique's phase in `study_guide.md`. Out of phase → decline by description
  and offer the in-phase seat; do not endorse it on the learner's stated motive.

### Why scope is a correctness rule, not a preference

A scaffolded-but-unattempted file is not inert — its blast radius is the tracker:

- **Discovery plants phantom rows.** `update_review_dates.py` auto-adds any problem file
  with no tracker row as **🔴 Blank / streak 0 / attempt date = today / next review = the
  Blank interval** (`discover_source_problems`). It skips a file whose
  every stub body is still `pass`, so a scaffold never attempted no longer gains a row. A
  file with one line of real code in it is still discovered: an abandoned half-attempt
  committed by the end-of-session `git status` sweep gains a Blank that never happened,
  plus a near-term rep to service it (the Blank interval is the shortest).
  - ⚠️ **DELETING THE SCAFFOLD DOES NOT DELETE THE ROW.** Undo BOTH, in the same edit.
    Once discovery has run, the row is independent of the file; removing the `.py` leaves
    the row and the script has nothing to reconcile it against. Delete the file AND the
    tracker row, then re-run the script to confirm the row does not return. (Found Aug 31,
    2026 on 84 — file deleted, row survived uncommitted for a rep that never happened.)
  - **Grep for a phantom:** `| Unknown | [<n>. …] | 🔴 | 0 | | | |` — **`Unknown`
    difficulty and blank dates**. Blank dates are why it hides (no scheduled demand, never
    in a due list); only reading the tracker's tail surfaces it. Or run
    **`python scripts/check_phantom_scaffolds.py`**. It flags phantom rows (empty Rep Dates /
    `Unknown`) AND stranded probes (an earned probe still under `dsa/probes/`), and runs
    report-only from pre-commit.
- **Retry scaffolds move history out of the file.** Scaffolding a retry they didn't ask for
  stashes prior attempts to `.history/`. Restore correctly declines an unattempted stub, so
  the file stays blank and the stash ships. That is a solution file emptied for a rep that never ran.
- **Dates are session-dated, not wall-clock** (fixed at source Aug 2, 2026).
  `new_problem.py`, `restore_history.py`, `update_review_dates.py` resolve the session date
  via [`scripts/session_date.py`](scripts/session_date.py). A dirty tree past midnight means the
  session started yesterday. Each takes `--date` to override, and announces it.

So: scaffold what was asked for.

**Consequence, stated plainly:** coding is the only path to 🟢, so scaffolding a 🟡/🟢 warmup
**raises** its ceiling from the no-code cap (🟡) to a real 🟢. Warmups are still 15-min slots
— if they'd rather blueprint one verbally, the file just goes unused; nothing is lost.

## The call

```sh
python scripts/new_problem.py --number 743 --title "Network Delay Time" --pattern graphs \
    --signature "times: List[List[int]], n: int, k: int -> int" \
    [--method networkDelayTime] [--url ...] [--premium]
```

- **New problem** → creates `dsa/leetcode/<pattern>/<number>_<snake>.py` from
  [`docs/foundations/dsa/templates/solution_template.py`](docs/foundations/dsa/templates/solution_template.py).
- **Retry** (file exists) → inserts a dated stub `def <method>_<YYYYMMDD>(self)`; never a
  second file. (Full retry handling: `retry-and-restore.md`.)
- **Always pass `--signature` on a new problem.** `self` is implied, return annotation
  optional. Without it the stub is a bare `(self)` and the learner retypes the signature
  every attempt — transcription, not recall. Repeat once per `--method`, in order, for a
  multi-method problem. On a retry it's only a fallback — the signature already in the file
  wins (it can't drift from disk).
- **Attempts are keyed by date, not a counter** (`checkInclusion_20260712`) — matches the
  file convention and keys straight to the tracker's attempt dates.
- `--premium` links the free NeetCode mirror instead of the paywalled LC page. **Usually
  unnecessary since Aug 7, 2026** — the script asks LeetCode's GraphQL API whether the
  problem is paid-only and switches hosts on its own.
- **When a spec exists, the scaffold reads it.** If `dsa/tests/<number>_<snake>.yml` exists,
  `new_problem.py` takes the statement and the signature from it, so pass neither. If the
  problem will be run on the site and has no spec, write the spec first: the statement, the
  entry point, the signature, the comparison mode, the statement's examples, and about 30
  stored random cases. Compute their expected values with a reference kept out of the repo.
  Then run `python scripts/export_practice.py --check`. Add a `figure` when the input is a
  graph or a grid, so the site draws each example.

**Fill the problem statement for them** — the learner never pastes it. Fetch it from the
source and write it into the `{statement}` slot. In low-token / caveman mode, write a
compressed *caveman version* instead of the full text.

### Worked example — scaffolding a new problem

```sh
$ python scripts/new_problem.py --number 743 --title "Network Delay Time" \
    --pattern graphs --signature "times: List[List[int]], n: int, k: int -> int"
Created dsa/leetcode/graphs/743_network_delay_time.py
LINKS: https://leetcode.com/problems/network-delay-time/
```

The created file holds the statement + a bare stub — no logic:

```python
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        pass
```

## Link verification (added Aug 7, 2026)

Before printing `LINKS:` the script checks the slug against `leetcode.com/graphql`: does it
exist, does `questionFrontendId` match `--number`, is it premium. **Warn-only.** It never
blocks a scaffold and is silent when offline.

- **A status-code check does not work on either host** (tried first): LeetCode returns `403`
  to a HEAD for real and fake slugs alike (bot protection); NeetCode returns `200` for both
  (SPA). A 404 check would pass every broken link. Hence GraphQL.
- **NeetCode cannot be verified at all** — no API, SPA answers 200 for anything. Renamed
  problems live in the hand-curated `NEETCODE_RENAMES` map (`alien-dictionary` →
  `foreign-dictionary`). **Add an entry** the moment a premium link is found broken. That's
  the only way it grows; an unlisted premium slug says so rather than implying it was checked.
- ⚠️ A TLS-trust failure is **not** "offline." A Python with no root certificates fails every
  call forever, so silence would leave the check looking installed while never running. It
  prints one line naming the fix (`Install Certificates.command` / `pip install certifi`).

## Where a problem links

LeetCode if it is free there → NeetCode if its own list has it → HelloInterview if its catalog has it → progressiveoverflow (`https://progressiveoverflow.com/practice/<n>`, label `PO`). A problem none of the first three carries is never skipped: write its practice spec (the `practice-problem` skill) so the practice page exists, then link it. The spec's own `url:` keeps the problem's source page, which the practice page's title links to. Confirm each of the first three against that site's own list before linking it. `decisions.yml` `problem-link-order-oct04`.

## Presenting the kickoff / lineup board — name + links, NOTHING else

A presented lineup carries **only the problem, as its links**: `[<n> <title>](repo-relative .py path) · [LC]`
(or `[NC]` if premium), the pair inside the problem cell. This applies to the kickoff board, a
mid-session restate, and a "what's next" hand-over alike. **No Note/Focus/technique/comfort/
units/difficulty column,** and no technique parenthetical in the title.

⚠️ **Any column beyond the name spoils the recognition front-gate** — the one thing the gate
exists to measure. `Course Schedule IV (Floyd-Warshall)`, a "Focus" cell reading "post-order
hinge", and a Note cell with the exact miss to watch are all examples. Each one hands the
learner the call before they recall it. Comfort/units belong in the *schedule file* for planning; they never ride the lineup
shown to the learner. (Learner, twice: *"The tables should just be the name of the problems and
links, nothing else."*)

The one exception to name + links only: a problem with 2+ tracker rows shows ` · method: <due method>` after its links (decision `variant-label-on-board-oct11`); `remaining.py` prints it from the day's schedule row.

List the day's problems from highest priority to lowest: 🔴/🟡 conversions first, then new problems, then 🟢 reviews, with easy reviews last. `scripts/schedule_priority.py` sorts each day's rows into this order when a schedule is committed, and `remaining.py` prints them in this order.

⚠️ **Any table whose rows are linked problems is a lineup**, whatever the turn is about: a work report and a plan count as much as a board. List the problems as name + links only, and key any detail by something other than the problem. A size constraint is a spoiler too, because density is a recognition cue.

⭐ **Build every lineup from a script, VERBATIM: `remaining.py` for a day's board, `links.py <n> ...` for a named hand-over.** Never hand-copy schedule rows.
The script reads the title from each file's header, so it emits a clean pair with no technique
parenthetical and no Note column. Hand-copying a row drags along its `(technique)` title and its
rep-directive Note cell, which is exactly how the spoiler leaks. Run it, paste the lines, add
nothing:

```sh
$ python scripts/links.py 743 332
[743 Network Delay Time](dsa/leetcode/graphs/743_network_delay_time.py) · [LC](https://leetcode.com/problems/network-delay-time/)
[332 Reconstruct Itinerary](dsa/leetcode/graphs/332_reconstruct_itinerary.py) · [LC](https://leetcode.com/problems/reconstruct-itinerary/)
```

⭐ **"What's left / what else / what's next / remaining / still open?"** → run `scripts/remaining.py`,
NEVER hand-assemble the number list. `links.py` takes numbers *you* supply, and the moment you pick
that set from memory of what's been done you can drop an open item. This happened twice in one
session, once each direction. `remaining.py` removes the recall step. It reads the current week's
schedule, finds the session-date day-block, and prints the **un-struck** rows (the open board) as
the same clean `[file]·[LC]` pairs. It calls `links.py`'s `link_line`, so it is spoiler-free. The
name+links-only rule still holds. Run it, paste the
lines, add nothing:

```sh
$ python scripts/remaining.py           # today's open board (session date)
$ python scripts/remaining.py --date <YYYY-MM-DD>   # → "Nothing left … ✅" when all struck
```

**Division of labor:** `remaining.py` for any board of the day. That covers the kickoff board right after
scaffolding (nothing is struck yet, so it prints the whole day) and *"what is open right now"* alike, both
in priority order. `links.py <n> …` only for a single named hand-over ("let's do 102"). It prints coding rows under `Code · N` and the day's `Complexity`-technique rows under `Complexity re-asks · N`; paste both groups with their labels. full rule: [`feedback_lineup_links_only.md`](.claude/memory/feedback_lineup_links_only.md).

⭐ **Recommend by number, steer by description.** When you suggest what to do next, link **only the pick**
(name + `[file]·[LC]`). Refer to problems you're steering *away from* by **description, not number**. A
link is an invitation, so linking a steer-away advertises the rep you're declining. full rule:
[`feedback_recommend_by_number_steer_by_description`](.claude/memory/feedback_recommend_by_number_steer_by_description.md).

⭐ **Before calling a rep optional or ranking it last, read its technique's row in `technique_coverage.md`.** A rep that closes a listed variant gap, or belongs to a technique with no 🟢 yet, stays a priority.

full rule: [`feedback_lineup_links_only.md`](.claude/memory/feedback_lineup_links_only.md); the links
pair itself is the links rule (both links, inside the problem cell, `NC` when premium).

## The recognition probe variant

A **recognition probe** gets a file — but at a neutral path that does **not** name the
technique (so the page can't leak the call). See `dsa/probes/README.md`. (The old "blind
sprint" exception is gone. A page left blank *was* the rep. SD blind sprints
and the AI track were both retired Aug 13, 2026.)

- **Create it with `new_problem.py --probe`** (added Sep 14, 2026), not a hand-written file:
  ```sh
  python scripts/new_problem.py --probe --number 648 --title "Replace Words" \
      --signature "dictionary: List[str], sentence: str -> str"
  ```
  It writes the blind file to `dsa/probes/<n>_<snake>.py` (the "🎯 RECOGNITION PROBE — you
  name it" header + the shape→technique→picking-feature prompt). It skips the tracker entirely
  (outside `solutions.roots`), and prints the **local file link ONLY**. Fill the statement.
- **Present a probe (or the DSA-mock base problem)** with its LOCAL file link only — never LC/NC. `[<n> <title>](dsa/probes/…py)`
  and nothing else. The problem/number/title do not spoil; only the technique-bearing LC page
  (its tags/editorial) does. This is the inverse of the normal `[file] · [LC]` pair — see
  [[feedback_lineup_links_only]] ("a recognition probe is the INVERSE pair"). Don't leave it
  unlinked: the learner needs to open the file to do the rep.
