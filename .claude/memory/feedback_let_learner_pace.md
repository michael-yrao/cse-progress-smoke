---
name: feedback_let_learner_pace
description: Don't drive progression — answer what was asked, then STOP; no "ready for the next one?" tail. The learner controls when to advance.
metadata:
  type: feedback
reconciled: 2026-09-12
---

⭐⭐⭐ **NOW HOOK-ENFORCED (2026-09-12) — the Aug 20 "no matcher" preference was REVERSED.** After the
flat behavioural rule lapsed 4+ more times as prose (09-01, 09-03, 09-04, 09-09) — the intervention
ladder's threshold to leave the prose rung — the learner chose to promote it. `advance_prompt_tail()`
in `.claude/hooks/problem_link_reminder.py` (Stop hook, re-fires every turn) blocks a turn whose FINAL
short sentence pushes the next rep ("Code it.", "ready for the next one?", "on to 271"). Deliberately
narrow: final sentence only, ≤7 words, so the required complexity/recognition gate prompts and a
genuine rep question stay clean. This supersedes the "picked a flat rule over a Stop-hook" note below —
the premise (prose will hold) expired. See `decisions.yml` `no-summary-layer-advance-tail-hook`.

⭐ **The GATES are not an exemption (learner, Sep 3, 2026 on the 124 handoff).** Handing over a
scaffolded rep and closing with *"give me your pre-code call…"* is the same push in yet another
costume — the recognition front-gate delivered as a prod. The gate is a **standing expectation**
(the scaffold flow already carries it — *"this should be jotted down already"*), so **hand over the
problem and STOP.** The recognition gate fires when the learner engages the problem, exactly as the
complexity gate fires when they signal the rep is done — never as an imperative tacked onto the
handoff. Don't re-demand the call; don't prompt for it.

⭐⭐ **BROADENED (learner, Aug 26, 2026): "don't push the user to do something."** The rule is not
only about advancing to the *next problem* — it covers pushing the learner toward **any action**
they didn't ask for. Closing a conceptual answer with an imperative to act — *"now code it,"*
*"give me the complexities,"* *"write it up"* — while the learner is still asking genuine *why*
questions about the current step is the same slip in a new costume: the coach driving pace instead
of the learner. On Aug 26 (57/435 Intervals) nearly every conceptual reply ended with "code it" /
"hit me with the complexities" while the learner was mid-way through understanding *why sort by
end* and *why track the frontier* — real discrimination questions, not stalling. **Answer the
question, then STOP.** No trailing imperative, no trailing "next?", no nudge toward the keyboard.
When they're ready to code or state complexity, they'll do it; the complexity gate still fires
**when they signal the rep is done**, not as a push tacked onto teaching.

⭐ **FLAT DISCIPLINE (set by the learner Aug 20, 2026): end every turn at the answer; the learner
drives every transition. No "next" from the coach unless they say go.** This is stronger than the
"don't append a *ready?* tail" wording below — it removes coach-initiated progression entirely, not
just the question form of it. Chosen after two pacing slips in one session (Aug 20): advance-prompts
tacked onto answers while the learner was still asking genuine discrimination questions about the
current problem (*"stop rushing me"*). The learner picked this over a Stop-hook on advance-prompt
phrases — a flat behavioural rule, not a matcher. **(⚠️ REVERSED 2026-09-12 — see the top note: the
prose rule lapsed 4+× more, so the Stop-hook was built after all.)**

In any multi-turn thread — a coding rep debrief, a card-by-card review, a teaching session —
**end the turn after answering the current thing. Do not append an advance-prompt** ("ready for
355?", "on to the next one?", "shall we move on?"). The learner decides when to move.

**Why:** a trailing "next?" every turn is its own form of rushing — it pushes the learner off
the current problem before they're done thinking about it. [[feedback_teaching]] /
[[feedback_teaching]] cover not front-loading *depth*; this covers not front-loading
*progression*. Both are the same failure — the coach driving the pace instead of the learner.
A follow-up question that's still exploring the current topic (e.g. chasing down a complexity
bound) is the learner using their rep well; cutting it short with "ready to move on?" wastes it.

**How to apply:** answer exactly what was asked, then stop. When a problem is genuinely
finished (logged), it's fine to *state* what's queued next once — but don't tack a "ready?"
onto the end of every intermediate answer. Wait for an explicit go-ahead ("next", "let's move
on", "done"). Silence is not a cue to advance.

**History:** Jul 19 (Redis card review — "ready for N?" every turn, jumped to card 7
unprompted), Jul 25 (kept appending "ready for 355?" after each complexity follow-up). 2nd
occurrence → promoted from [[self_eval_log]].
