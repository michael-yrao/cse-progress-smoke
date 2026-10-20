---
name: feedback_concept_primer
description: Before the FIRST exposure to a named algorithm, run a short unrated session on the OBJECT it finds and the name of that object — the procedure comes later, on a different day
metadata:
  type: feedback
reconciled: 2026-09-06
---

**Set by the learner Aug 16, 2026**, off the back of Hierholzer: *"I did not remember concepts of
Eulerian Paths, Circuits or Graphs before doing Hierholzer so it is making it very difficult to stick.
So I think what we can do better is do a conceptual learning session before we do the algorithm for the
first time and explain what problem the algorithm solves."*

## The gap this closes

Two artifacts already pointed at this and **both are passive**:

- [[feedback_teaching]] (Jul 26) says lead with the problem and the broken assumption,
  never the mechanism. But it fires **while you are already explaining** — i.e. *after* a rep went wrong.
- `patterns/README.md` → *Graph algorithms — the name index* (Aug 5) is a **lookup you must know to go
  read**. `stuck_log.md` records that it was prompted by this very failure: *"same failure kind as 332's
  Eulerian and 143's tortoise-and-hare."*

Neither puts anything in front of the **first attempt**. That is the repo's own thesis about itself: a
rule that must fire unprompted cannot live as a paragraph, it has to be **a step in an executable list**.

## The evidence

**332 Reconstruct Itinerary is the worked example, and it is expensive.** Attempted **Jul 22 🔴 · Jul 28
🔴** (converted to a teach) **· Aug 4 🟡 · Aug 14** could not be written at all (second teach) **· Aug 18**
rated rep still pending. Five sessions and three `stuck_log` entries on one algorithm. The Jul 28 entry
names the cause exactly: *"could not name Eulerian path — and had never encoded the
Eulerian-vs-Hamiltonian split."*

**The first attempt WAS the introduction to the concept.** That is the defect.

⭐ **The converse is also on record.** The Aug 14 recognition ledger holds the learner's **strongest
picking-feature call in the repo** — *"visited holds edges not nodes"* — on this same problem, once the
concept had finally landed. The call was always available; the vocabulary was missing for three weeks.

## The primer

Scheduled **at the weekly build**, whenever the week contains a first exposure to a named algorithm.
**~15 minutes · unrated · no tracker row · ~1.0 unit.**

| Covers | Deliberately excludes |
|---|---|
| **The object** — what thing is being found, and **its name**. *"A walk that uses every edge exactly once. It is called an Eulerian path."* | **The procedure.** That is the first rep, or the teach if the rep stalls |
| **The discriminator** — the nearest neighbouring object and the one feature that separates them. *Eulerian = edges, Hamiltonian = nodes — and one is linear while the other is NP-hard* | **The proof.** Only on request, and later. See [[feedback_teaching]] |
| **Why it needs an algorithm at all** — what the obvious approach does, and what it costs | |

⚠️ **The first attempt lands at least a day later.** Same reason a teach is gap-protected: a primer
measured in the same sitting measures nothing. What it is measured BY is whether the recognition call
fires on the first rep — you cannot make a call about a class of object you cannot name.

## Consequence for the pattern notes

This splits a rule set Aug 15 (procedure notes are written **after** the rep, because a written
procedure is a spoiler):

- **Concept note → BEFORE.** The object and why it exists is not a spoiler; it is the retrieval cue.
- **Procedure note → AFTER.** Unchanged.

Which also means the `⚠️ not written` entries in `patterns/README.md` get filled as a **byproduct of the
primer**, rather than as a chore nobody schedules.

## Where it starts — Intervals + Greedy, NOT Backtracking

**Trial on the Intervals + Greedy phase (Aug 24 – Sep 13)**, moved earlier at the learner's request
Aug 16. The coach had proposed Backtracking (Sep 14) for the extra runway; earlier is the better call —
the format gets a real test three weeks sooner, and Backtracking then inherits a proven one instead of
being the experiment.

⚠️ **This makes it immediate: the phase opens Aug 24, so the primer must be SCHEDULED IN THE AUG 17
WEEK.** It is an item for that build, not a later one.

**The two primers this phase actually needs** — note that neither object is exotic, which is the point:
the failure mode is not "unfamiliar word", it is "memorised trick with no anchor".

| Primer | The object | The discriminator |
|---|---|---|
| **Intervals** | a pair `[start, end]`, and the fact that **sorting makes overlap a LOCAL check** — an O(n²) all-pairs comparison becomes one pass | **which key you sort by, and why**: by *start* to merge, by *end* to schedule the most non-overlapping. Picking the wrong key is the whole difficulty, and it is invisible if the rule was memorised |
| **Greedy** | what makes a greedy choice **provably correct** — the exchange argument | **greedy vs DP.** Greedy commits and never revisits; DP must weigh every option. The learner already has this instinct from Dijkstra and Hierholzer, where "commit and never revisit" was the load-bearing idea both times — name it once and it transfers |

⭐ **The greedy-vs-DP discriminator is worth the primer on its own.** 1D DP opens weeks
later, and the two phases are told apart by exactly this question. Teaching it as an object now, rather
than as a per-problem trick, is what makes the DP phase land.

**1D/2D DP (Oct–Nov) remains the case this really has to work for.**
