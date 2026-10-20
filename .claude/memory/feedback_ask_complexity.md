---
name: feedback_ask_complexity
description: after a problem is coded, ASK the learner for time & space complexity before rating — don't state it for them
metadata:
  type: feedback
reconciled: 2026-10-19
---

After a problem is done, **ask the learner to state the time and space complexity themselves**
before you confirm the rating. Don't announce the complexity for them.

**Why:** stating complexity is part of the thinking the learner owns ([[feedback_operating_principles]],
§0.2) — and in a real interview *they* have to volunteer it, unprompted. Reciting it for them
removes a rep and hides whether they actually know it.

**How to apply:** on any completed problem, before proposing 🟢/🟡/🔴, ask "time and space?" and let
them answer. Then confirm or correct — state the right complexity yourself only after they've
committed (or explicitly pass). Ties into [[feedback_infer_comfort]].

**✅ RESOLVED (2026-07-24) — the Big-O rating question (pinned Jul 22) is now decided.** Complexity is
enforced through the interval engine (the only real lever) via two rules:

1. **The gate (every rep, no skip):** the learner must state **time AND space, each with an itemized
   why-clause** — "O(1), one fixed 26-array" not a bare "O(1)". Naming each contributor is what
   surfaces the miss; a bare symbol hides it. Don't log any rep until they've answered (or explicitly
   passed). This supersedes the softer "ask for complexity" wording above.

2. **Per-problem freebie, then it counts** *(superseded 2026-09-23 — see the dated section at the
   bottom of this file; the freebie/cap mechanism below no longer governs the rating)*: the **first**
   complexity miss on a given problem → correct it + add it to
   [`complexity_gotchas.md`](../../docs/foundations/dsa/mastery/complexity_gotchas.md), **no rating
   hit**. A **repeat** complexity miss on the **same problem** (a later rep) → **caps that rep at 🟡**.
   The gotchas card doubles as the ledger: **if the problem is already on the card, its freebie is
   spent** → the next miss drops it. The gate and the correction+card entry always happen; the freebie
   only governs the *rating consequence*.

⚠️ **READ THE LEDGER BEFORE PROPOSING THE RATING — not after (promoted 2026-08-23, 2 occurrences;
superseded 2026-09-23 — the ledger no longer decides a rating consequence, kept for the history it
documents).**
The freebie rule above only works if its input is read *first*. Twice the rating was proposed and *then*
the ledger checked, once in each direction: **2026-08-22** on 15 — proposed 🟡 (miss caps) when the
freebie was **unspent** → should have been 🟢; **2026-08-23** on 567 — proposed 🟢 s2 when the freebie was
**spent** (a REPEAT) → the rule says 🟡. Same defect, both signs: a rating that hinges on a complexity
miss was announced to the learner before its deciding input existed. **So the sequence is fixed:**
1. learner states time + space with why-clauses (the gate);
2. if any bound is a miss, **open `complexity_gotchas.md` and read that problem's row** — is the freebie
   spent (problem already carded with a dated miss) or not?
3. *only then* propose the rating, and say the freebie state out loud ("first miss on this problem →
   freebie, no hit" / "already spent Jul 24 → repeat, caps at 🟡").
The tell you skipped it: you named a rating consequence of a complexity miss without having cited the
ledger. If you can't point to the ledger row, you haven't earned the rating yet. (Comfort override still
belongs to the learner afterward — 567 was overridden 🟡→🟢 s2 on defensible pre-constraint grounds — but
the *proposal* must be right first.)

**Why per-problem (not per-category):** the problem is already the unit of spaced repetition here, so
this needs no new taxonomy — check "is this problem on the card?" and rate accordingly. It's less strict
(the same category on a different problem gets a fresh freebie), but the card still teaches the transfer
and the simplicity fits the data model. Learner chose this dial Jul 24 over per-category / separate-track.

**Diagnosis that drove it:** the misses are almost all **space**, in a small set of categories —
fixed-alphabet-array = O(1) (242, 567), recursion stack = O(depth) (206), 2D structure = O(n²) (778),
output-counting. Not general Big-O weakness; 4 specific leaks. Time is consistently correct.

**Use the card to GUIDE, not just to catch (added 2026-07-24).** The gotchas card is also a live prompt:
at complexity time, scan the code's *shape* and fire the matching checklist question — the cue, never
the answer. Trigger → cue: **recursion** → "count the stack, how deep?"; **`[0]*k` fixed array** →
"bounded by input or by the alphabet?"; **grid `visited`/heap of cells** → "frontier: a line or an
area?"; **returns a built structure** → "counting the output or extra-only?".

**First run vs review — opposite postures:**
- **New problem (first-ever attempt):** complexity is a **guided teaching moment**. Cue the checklist
  **proactively, before they answer**, name the category, card it. **Double freebie** — *two* free
  misses before repeats cap at 🟡 — because first exposure means learning the algorithm *and* its
  analysis at once. (Reviews get one freebie.)
- **Review:** ask **cold** — they own the analysis. Cue the *why* only if they give a bare symbol or
  miss. One freebie (ledger state in the card).

The card thus **teaches forward on new problems and tests on reviews**; the trigger→cue map lives in
[`complexity_gotchas.md`](../../docs/foundations/dsa/mastery/complexity_gotchas.md).

## ⚠️ WHEN it fires (added 2026-08-02, after the gate was skipped entirely on 211)

The gate is **step 1 of CLAUDE.md's LeetCode Review Workflow** — ahead of the schedule mark and ahead of
the rating. It was moved there because keeping it *only* here, as a precondition to a workflow that didn't
list it, meant the workflow could reach the rating step without it — and did. Step 3's 🟢 definition
requires *"correct complexity"*, so the list was consuming an input it never gathered.

- **It fires on the rep, not on the ritual.** 211 arrived as *"whats the issue with my code here"* — no
  `new_problem.py` call, no kickoff, no front-gate. None of the usual cues fired, and the gate went with
  them. **The trigger is: am I about to propose a comfort rating?** If yes, the gate is already overdue.
- **The failure is silent, which is why it needs to be a step.** A skipped gate leaves every artifact
  looking correct — no wrong date, no unstaged file, nothing that surfaces later. Only the learner can
  catch it, in the moment, and on 211 that is exactly what happened.
- **Late is better than never, but say so.** Running it after the rating means their confirmation was
  given on incomplete information — re-check whether the miss changes the rating and tell them either way.

## ⚠️ Known false positive in `rating_gate.py` — a RESULTS TABLE reads as a proposal (found Aug 28, 2026)

The hook blocked a turn that proposed **no rating at all**: a factual answer about the probe tally,
rendering the six past probe results as a table of 🟢/🟡 glyphs. The hook saw the glyphs, found no
complexity statement in the learner's recent messages, and blocked.

**The failure shape is not "too sensitive" — it is that a RECORD of a past result and a PROPOSAL about a
current one are lexically identical.** Same class as the link hook's orphan-number problem, which was
fixed by letting the turn carry the fixed tag `(links owed, order unchanged)` to mark a debt rather than
a pick. Candidate fixes, cheapest first:

1. **Let a turn declare itself historical** with a fixed tag the hook recognises (mirrors the link fix).
2. **Require a proposal cue**, not a bare glyph — the rating turns all say *"proposed rating"* /
   *"reads as"* / *"confirm?"*. A glyph inside a markdown table row is almost never a proposal.

⚠️ **Do not fix it by weakening the gate itself.** The gate caught two real backwards-run ratings (15 on
Aug 22, 127 on Aug 23) and that is worth occasional noise. The bug is the *trigger*, not the *rule*.

✅ **FIXED at the Aug 30, 2026 reconcile pass — candidate 2, and the diagnosis was one word off.** The
hook already required a proposal cue; the cue list simply contained a bare `rate`, which is also the
ordinary noun for a frequency. The blocked turn said *"row-creation **rate** 17%"* — the probe
diagnostic's own vocabulary — so the tally answer tripped a rule aimed at *"**rate** it?"*. Narrowed to
the decision-request forms only (`rate it/this/that/the rep`, `rate?`); `confirm`, `proposed`,
`override`, `accept` and `rating:`/`rating?` are untouched, so **the gate is not weakened** — the two
backwards-run ratings above would still block. Two regression cases added; selftest **18/18**.
Candidate 1 (a fixed historical tag) was not needed and is not implemented.

---

## ⭐ Clean code + Big-O miss → don't cap; drill it end-of-week (formalized Sep 3, 2026; generalized
to every rep 2026-09-23 — see the dated section at the bottom of this file)

**Normative sentence lives in CLAUDE.md** (LeetCode Review Workflow step 1) and the rule table in
`complexity_gotchas.md` (rule 4 + the cleanup queue). This is the why + the history.

**The rule as it stood Sep 3–22, 2026:** when **recognition AND code were clean off a blank page** and
the *only* miss was a complexity bound, the miss **does not cap** the comfort rating (rate on the code
— a clean rep is 🟢), and the missed bound is **queued for an end-of-week complexity cleanup** where it
is re-asked cold on the *existing* code. Supersedes the freebie→repeat-🟡 cap (rule 2) for this case
only. If the code itself needed a real fix, that fix still affects the rating — but through the code
criterion, never because a complexity miss rode alongside it.
**2026-09-23: the scope condition above is retired** — see the dated section at the bottom of this
file. A real code fix still affects the rating through the code criterion; a complexity miss never
does, on any rep, clean or not.

**Why (learner, Sep 3, 2026):** *"we do an end of week cleanup for clean code and big O misses only …
the agent can ask the user to look at the code and explain the bounds again at end of the week for
everything that was missed."* The insight: **the code rep and the complexity concept are different
units of learning, and re-repping the first to re-test the second is churn.** Re-solving a problem you
can already solve, just to be re-asked its Big-O, spends a whole rep (and a +10 🟡 interval) to test a
one-minute concept. Decouple them: rate the code honestly, and test the *bound* cheaply off-rep at week
close by re-explaining it on the code already written — no re-solve.

**How to apply:**
- In the moment: still fire the gate, still correct the miss, still ledger it. Only the *rating
  consequence* and the *re-test timing* move.
- Record the missed bound in the cleanup-queue table in `complexity_gotchas.md` (problem · missed bound
  · queued date).
- At the weekly close-out (CLAUDE.md step 7): fire each queued problem cold — *"re-open your code for X,
  give me time + space with the why."* Clean → clear. Missed again → a bound that fails a second cold
  re-explain is a real gap, not churn: escalate to a proper complexity teach on that category.

**First application: 743 Network Delay Time, Sep 3.** Clean lazy-Dijkstra + clean recognition; the space
why-clause mis-attributed the O(E) (called the heap "≤ V nodes"), self-corrected on one non-leading
nudge. Under the pre-Sep-3 rule this was a 3rd repeat miss → 🟡 cap; under this policy it logged **🟢
(🟡→🟢)** with the bound queued. This is the exact case the policy is for: the concept, not the code,
was the gap. [[feedback_let_learner_pace]] · see `decisions.yml` `complexity-cleanup-formalized`.

**Clarification (Sep 20, 2026) — a self-caught typo doesn't count as "the code needed a real fix."** Left
open on 912 (a no-op for that rep either way); learner's read, adopted: a typo the learner spots and fixes
themselves, unprompted, on a one-line pointer / index / bound — no logic change, nobody else surfaced it —
is clean authoring, so the clean-code waiver (rule 4) still holds and it does **not** cap. The picking
feature is **who surfaced it + whether logic changed**: self-caught & logic-unchanged → clean; coach-/test-
surfaced or an algorithm-altering fix → a real fix (→ 🟡, waiver broken). Operational home: rule 4 scope in
`complexity_gotchas.md`; `decisions.yml` `typo-self-fix-not-a-real-fix`.

---

## ⭐ 2026-09-23 — the rating ignores Big-O entirely; the clean-code waiver above generalizes to every rep

**Learner's call:** *"Rating should ignore Big-O going forward — we will be doing the complexity gate at
end of the week to clear them up as we go."*

**What changed.** The complexity gate itself is unchanged — the coach still asks for time AND space,
each with an itemized why-clause, before every rating (rule 1 above; `rating_gate.py` unchanged). What
changed is the *consequence*: a wrong, prompted, or taught complexity bound **never** lowers or caps the
comfort rating, on any rep — not just a clean one. This retires rule 2's freebie/repeat-🟡 cap and lifts
the Sep 3, 2026 clean-code scope condition on the waiver above (*"if the code needed a real fix, the
normal cap stands"*) — that clause is now wrong and superseded. A real fix to the **code** still affects
the rating, but through the ordinary code criterion (a rep that needed a real fix isn't clean), never
because a complexity miss happened to ride alongside it.

**What stays.** Every miss — wrong, prompted, or taught — is still corrected in the moment, still added
to [`complexity_gotchas.md`](../../docs/foundations/dsa/mastery/complexity_gotchas.md), and still queued
into the end-of-week complexity cleanup (`weekly-build.md`), which re-asks it cold on the existing code.
The gate, the correction, and the card all still happen every time; only the rating consequence is gone.

**Why:** the Sep 3 policy already established that the code rep and the complexity concept are different
units of learning, and decoupled them for the clean-code case. This removes the remaining special case —
whether the code also needed a fix was never really about whether the *complexity* concept had been
tested, so gating the complexity waiver on the code's cleanliness was mixing two separate judgments.
Testing complexity happens uniformly, off-rep, at the weekly cleanup; testing code happens on the rep, via
the code criterion. See `decisions.yml` `rating-ignores-complexity` (supersedes `complexity-cleanup-formalized`'s clean-code-only scope).
