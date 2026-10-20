---
name: feedback-consolidation-reps
description: A technique needs MULTIPLE problems, not one — near-identical siblings are the training signal (their minor differences are what recognition grades), and they don't count against the new-algorithm intake cap
metadata:
  type: feedback
reconciled: 2026-09-06
---

**Set by the learner Jul 26, 2026:** *"we need multiple problems of the same flavor for users to
actually knock down the technique, even if they look similar enough — users need the repetition and
be able to recognize the minor differences."*

**The rule:** intake has **two classes**, and the difficulty-tiered cap governs only the first.

| Class | Definition | Expected | Cascade | Against the cap? |
|---|---|---|---|---|
| **New-technique** | first problem of an algorithm | 🔴 | ~2–3 warmup slots over a fortnight | **yes** (3/4/5 by tier) |
| **Consolidation rep** | another problem in a technique already at 🟡+ | 🟡/🟢 | none | **no** — separate ≤2/week budget |

**Why:** one problem per technique trains **recall of that problem's solution**, not the technique —
there's no variation to generalize across, so what's learned is "743 is the Dijkstra one," a lookup
rather than a skill. Transfer requires multiple surface forms of one underlying idea, and the **minor
differences between near-identical problems are the training signal, not redundancy**: cost-as-max vs
cost-as-sum, multiplicative vs additive relaxation, hop-capped vs unbounded. That discrimination is
exactly what the [[feedback_recognition_gate]] front-gate grades, and it is untrainable from a single
instance.

**The cap never applied to these anyway** — its own stated rationale is the *blank tax*: "a 🔴 costs 1
active slot plus ~2–3 follow-up warmup slots as its Blank-interval retries settle." That is the cost of learning an
algorithm. A sibling in a known technique produces no 🔴 and no cascade, so charging it against a
new-algorithm budget was a category error ([[feedback_intake_and_surplus]] still holds, unchanged,
for its actual class).

**How to apply:**

1. **"Similar to one already done" is an argument FOR scheduling it, not against.** This reverses the
   usual redundancy instinct — check that instinct whenever declining a problem.
2. **Gate: base technique must be 🟡 or better.** Siblings consolidate a half-formed technique (that's
   the point — interleaving while it settles is what makes it stick), but against a 🔴 they just
   double-blank. Teach first, then consolidate.
3. **Slot them lighter than new-technique problems** — closer to a review of a technique than an intake
   of one. Active block if the problem is Hard, generous warmup otherwise.
4. **Aim for ~3–4 problems per technique** before treating it as covered, spanning the meaningful
   variations rather than repeating the same shape.
   - ⚠️ **"~3–4" is the DEFAULT, not a cap — the operative clause is *spanning the meaningful
     variations*.** Where a technique genuinely has more distinct flavours than that, the honest bar is
     the flavour count, set per-technique via `min_problems` in `techniques.yml` (the same mechanism that
     drops Dutch National Flag to 1). **Intervals was raised to 5 on Aug 28, 2026** for exactly this
     reason: merge-by-start, insert-into-sorted, schedule-by-end, max-concurrent sweep-line, and
     two-list intersection are five different procedures, not five phrasings of one. A technique sitting
     at "3/3, bar met" while three of its flavours have never been written is the failure this bullet
     exists to prevent — see `decisions.yml` `interval-flavours-declared`.
5. Distinct from [[feedback_method_variant_promotion]]: that is *many techniques on one problem* and is
   gated on the base retiring. This is *one technique across many problems*, gated only at 🟡. Different
   axis, different gate — don't apply one rule's gate to the other.

## ⚠️ Sibling gate is 🟡+, NOT `green:base` (added Aug 23, 2026)

**A thin-technique coverage sibling gates on the standard `🟡+` consolidation gate — never on the base
problem going 🟢 first.** The `green:base` hold (224 waited on `green:150`; the Floyd Fast/Slow variant
on `green:202`) was stricter than this rule and **counterproductive for a thin technique**: a second
problem is another path to the technique's *first* 🟢 and trains the transfer that re-repping one problem
cannot — so gating coverage behind the base going green can **deadlock** a technique stuck at 🟡.

**Why:** the goal for a thin technique is *coverage* (3–4 surface forms). Requiring the single existing
problem to reach 🟢 before a second may enter means a technique that keeps hovering at 🟡 never gets the
second surface form that would actually teach it. The learner's framing (Aug 23): *"for the techniques
without proper coverage, we can drop the gate on another problem being green."*

**How to apply:** a sibling is schedulable once the base is **🟡 or better** (the standard gate). **One
guard retained** — the thing `green:base` was a blunt proxy for:

> A 🟡 that was **heavily coach-guided** (near-🔴 — multiple coach-supplied fixes, per the stuck_log) is
> treated as 🔴 for sibling purposes → convert/teach first, no sibling yet. Against a genuinely-unlearned
> base a sibling just double-blanks (§2a).

**The distinction is 🟡 *quality*, and it is a judgement:** 150 (clean-🟡, recognition hit / execution
slip) → sibling OK; 239 (🟡 after *three* coach fixes Aug 22) → convert first. See
`decisions.yml` `sibling-gate-yellow-not-green`. Related: [[feedback_intake_and_surplus]] (when to
spend capacity on this coverage), [[feedback_coverage_gap_ledger]].

## ⚠️ WHERE a sibling comes from: PULL first, author last (added Aug 29, 2026)

**The candidate population for a coverage sibling is a company frequency pull — `python
scripts/pull_interview.py --company <C> --technique <t>` — and only if that does not yield enough
coverage do you reach for anything else.** Learner, Aug 29: *"let's make sure the population comes
from company pulls first and then we can reach for others if there is not enough coverage"*, clarified
as the pool that provides a **technique's coverage**, not intake generally.

**Why this had to be written down:** everything above specifies *when* a technique needs another
problem and says **nothing about where the problem comes from**. That silence is not neutral — the
source defaults to coach invention, which is how **227 Basic Calculator II** reached a board. It was
never in NC150 and never in a pull. It entered on Aug 11, 2026 as a *justification*: the learner had
rejected 150 Evaluate RPN (*"I don't see anything of value here"*), the defence offered was *"it's the
base rung under 224/227/772"*, and the build then recorded that one of 224/227 must be scheduled **or
the prerequisite leads nowhere**. A thin problem generated its own sequel. Two weeks later the learner
reached the same verdict unprompted — *"digit and calculator problems with stack sucks … it feels like
a brain teaser than an actual technique check or teach"* — and 227 was parked.

⭐ **THE COROLLARY IS THE SHARPER HALF: if a rung exists only to justify the problem below it,
re-examine the RUNG — do not schedule the sequel.** The Aug 11 note already recorded that *the
learner's reaction is the data, not my rebuttal*, and then scheduled the rebuttal anyway.

⚠️ **Applied to the rungs ALREADY IN THE PLAN, Aug 31, 2026 — not only to future ones.** Parking 227
on Aug 29 left **224 Basic Calculator** sitting in the Waiting Room under `🟡:150`, flagged but not
re-examined. It fails the same test for the same reason: it is the parens rung of a ladder authored to
defend its own base, never frequency-pulled, and the learner has now rejected the family twice. **224
is parked beside 227**; Stack-expression's 2nd problem is **394 Decode String** (`pull_interview.py
--company Google --technique stack`, freq 58.3, and not in the phase plan), and both parked rungs
re-gate on `rated:394`.

**The general form:** adopting a sourcing rule does not retroactively clean the board. At the first
weekly build after one lands, **walk the Waiting Room and re-price every entry against it** — an
authored rung is invisible once it is already listed, because a Waiting Room row looks identical
whether it came from a pull or from a rebuttal. `decisions.yml` `stack-expression-ladder-parked`.

**This is EXEMPT from the post-NC150 pull gate.** [[feedback_expansion_pull_scheduling]] says *"during
NC150 there are no interview pulls yet — the roadmap is the work"*, and that stands: it governs
**filling application slots**. It was never about **sourcing a coverage sibling**, and the tool has
supported `--technique` all along.

**How to apply, at the weekly build:**

1. A technique needs coverage → run the pull, technique-filtered, and read it by frequency.
2. Prefer a candidate already in the phase plan — but **verify it**. The `⚠ already in the phase plan`
   flag is a **fuzzy substring match on the title and is only a FLAG, by design** (the script says so).
   It false-positived on Aug 29: *Decode String* was flagged as planned because *Encode and Decode
   Strings* (271) contains it. **Grep the study guide before calling a swap free.**
3. Only if the pull yields too little coverage do you hand-pick — and say in the build that you did,
   and why.
4. A high-frequency pull that proves genuinely interview-worthy goes **into the phase plan**, per
   [[feedback_roi_promotes_to_curriculum]] — not parked in the Expansion Queue.

Recorded in `decisions.yml` `coverage-sibling-pulled-not-authored`; occurrence log in
`self_eval_log.md` 2026-08-29.
