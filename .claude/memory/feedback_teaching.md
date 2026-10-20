---
name: feedback_teaching
description: Why coaching explanations lead with the spine (and, for an algorithm, its purpose then its procedure), one job per turn — the worked examples behind the rule
metadata:
  type: feedback
reconciled: 2026-09-11
---

**Operational rule lives in the skill** — `.claude/skills/cse-coach/SKILL.md` §1 (Lead with the spine ·
One job per turn · Teach an algorithm procedure-first). This file is the *why* + the worked examples.
Merges the former `spine_first`, `procedure_first`, `algorithm_purpose_first`, `turn_economy`.

## 1. Lead with the spine — then stop

Open every conceptual explanation with the **2–3 load-bearing facts everything else derives from**, stated
plainly, then check in. Detail is a *second* message, on request.

> **Redis is a dictionary that lives on another computer** (Jul 14 2026): a **dictionary** → key lookup,
> no queries; on **another computer** → every server shares it (the point), every read is a network trip
> (the price); **one thing at a time** → commands can't race, one slow command stalls everyone. Pipelining,
> `MGET`, sharding are all *tactics for living with those three facts*.

**Why:** the failure mode is front-loading tactics before the spine exists to hang them on. That Redis
thread answered a one-line question with four escalating essays and left the learner *more* confused —
**volume of correct detail destroys comprehension when the skeleton isn't there yet.** Detail is not free;
each paragraph raises the chance the spine gets buried. On "I'm lost," strip *down* to the spine.

## 2. For an algorithm: purpose first, then procedure — proof last

**(a) Purpose before mechanism** (set by the learner Jul 26, on 787/Bellman-Ford): state the problem it
solves and **the broken assumption it repairs** in a simpler algorithm, then its cost, *then* the loop.
*"Dijkstra settles the cheapest node and never revisits; a negative edge can lower an already-settled
distance, so that step is invalid → Bellman-Ford, O(V·E)."* Mechanism tells you *how to run it*; purpose
tells you *when to reach for it* — which is what recognition (and the interview's first two minutes) grades.
Without purpose an algorithm is a memorized procedure with no retrieval cue, and comes back 🔴. (The front
half of this — object + name + discriminator — is promoted to a scheduled **primer** before the first
attempt: [[feedback_concept_primer]]; 332 cost five sessions because its first attempt WAS the intro to
Eulerian paths.)

**(b) When they're CODING an unknown algorithm, procedure leads** (Prim's/1584, Jul 18): give the literal
imperative loop in plain language — *"each round: pick the unvisited node with the smallest number, mark it
done, update its neighbors"* — and **hand-trace a tiny 3–4 element example**. Proof/complexity/jargon only
later, only if they ask "why does this work?". The failed order opened with the cut-property proof,
"settled" nodes, and O(V² log V) before they could run a step — their own code comments (*"get the closest
node we haven't visited"*) were clearer than the prose. **Answer a mechanics question with mechanics; strip
jargon; on "this makes no sense" strip DOWN, never add another layer of why.** Purpose is one sentence
*before* the procedure, not an epilogue.

## 3. One job per turn (interactive sessions)

In a derive-the-design / Socratic / failure-mode drill, keep each turn to **one job**: a one-line
affirmation + at most one correction + one question, then stop. Push depth (tables, mnemonics, full
derivations) into the **written note** ("added to your note"), not the chat — the chat is the dialogue, the
note is the reference. Progressive disclosure: short answer, then *offer* the deeper why. When they nail it,
acknowledge in one line and move on — never re-explain what they just demonstrated.

**Why:** the Jul 15 Redis derive session was pedagogically excellent but each turn stacked
affirm+correct+sharpen+ask+tables into walls of text (*"it helped a lot, the issue is it was a lot of walls
of text"*). The depth helped; the packaging buried it — and those are separable.

Related: [[feedback_interactive_learning]] (how this feels across a whole session; and its true-zero floor),
[[feedback_explanation_register]] (show values before naming; the no-nonsense register), the answer-length
cap in CLAUDE.md, [[feedback_operating_principles]].
