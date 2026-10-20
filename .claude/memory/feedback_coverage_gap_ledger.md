---
name: feedback_coverage_gap_ledger
description: Log what a session did NOT reach as bare open questions — since Aug 13, 2026 this lives in the mock debrief's "Open probes" section, and it is what the midweek deep-dive round runs on
metadata:
  type: feedback
reconciled: 2026-09-11
---

**Operational rule lives in the skill** — `references/system-design.md` ("During & after the mock"). This file is the *why*.

**Set by the learner Aug 9, 2026:**

> *"the questions I ask might not cover everything that we want to learn about a technology or concept so
> I want you to flag what are the facts and details that are still missing or not addressed after each
> teaching and learning session and then after the appropriate learning sessions are done, we do mock
> interviews that test based on the questions we accumulated."*

⚠️ **Where this lives changed Aug 13, 2026** ([[project_sd_mock_model]]). It was a
`## ❓ Open — not yet asked` section at the bottom of a technology/concept card, written at the end of a
teaching session. **Teaching sessions are no longer scheduled**, so the ledger moved to the place that
now generates the same thing: the **`❓ Open probes`** section of each mock debrief in
`<your-sd-study-repo>` `mocks/` (the SD track left this repo Aug 15, 2026).

**The move is an upgrade, not a relocation.** The card version recorded *what a conversation happened not
to reach* — bounded by what the learner could already see was missing, which is the hole it was patching
in the first place. The debrief version records **what they could not answer under time pressure when an
interviewer pushed.** That is the same coverage report with a harder instrument behind it.

**The procedure (a numbered step in CLAUDE.md's SD section — not left as a paragraph here, per the
[[feedback_self_evaluation]] intervention ladder):**

1. At the **end of the mock**, in the debrief, list everything interview-relevant the mock exposed and
   did not resolve.
2. Bound it by the **L6 ROI line** ([[project_sd_roi_line]]). An unbounded list becomes noise and stops
   being read.
3. Each is a **bare open question, never a summary of the answer.** "We never covered how the queue
   handles poison messages — it works by…" spoils the item and kills the probe. Written as a question,
   one artifact is both the coverage report and the next deep-dive round's material.
4. **Ask whether to answer any of them now or hold them for the deep-dive round — every time, both
   directions genuinely open.** The learner's reason: *"depends on the availability of the user and how
   much more learning the user can still take honestly."* Only they can answer that. Do not default
   either way.
5. **A design with an empty probe bank has nothing left to push on** — that is the repo-evaluable trigger
   for the midweek slot going to the next question instead ([[feedback_gate_on_internal_state]]).

⚠️ **End of session only.** Surfacing a gap mid-mock is a hint, which is the one thing the interviewer
role forbids.

**Still applies verbatim to requested teaching.** When the learner asks to be taught something
off-schedule, spine-then-pull still governs the format ([[feedback_interactive_learning]]) and closing
with the unreached questions still applies — write them into the relevant reference card.
