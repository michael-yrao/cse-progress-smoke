---
name: feedback-answer-length
description: An answer to a question is capped at one small paragraph; offer expansions as a question rather than delivering them
metadata:
  type: feedback
reconciled: 2026-09-06
---

**Learner, Aug 17, 2026:** *"When answering a user question, it cannot be bigger than a small
paragraph. Any additional info and followups can be provided to the users in the form of a question on
whether they want certain portions expanded. This makes answers actually readable."*

**Why:** a long answer is not more informative, it is **less read**. When a reply arrives as a
multi-section report with tables and bolded asides, the one load-bearing sentence gets skimmed past and
has to be re-explained anyway — so volume actively defeats its own purpose. This was said after a run
of answers that each opened with a findings table and closed with "two things worth knowing".

⚠️ **It is a CAP, not a nudge.** [[feedback_teaching]] already said "one job per turn" and the
CLAUDE.md token-discipline rule already said "be lean", and answers stayed long. Both were phrased as
dispositions; this one is a hard limit with a fixed escape hatch, which is the difference between a
rule that fires and a paragraph.

⚠️ **The cap is on ANSWERING, not on EXPLAINING WHAT YOU DID** (learner, same day, after I got it
backwards): *"explaining what you did should not require a prompt from users. answering the users
should."* The first application of this rule truncated a **work report** and then closed with "want me
to expand on any of…" — withholding the account of work that had already happened *and* charging a
turn to retrieve it. A work report is delivered in full, unprompted; only a question's overflow is
offered.

**How to apply:**
- **Answering a question** → one small paragraph. Then **ask** which part to expand, and expand only
  that. Never pre-empt the next three follow-ups.
- **Explaining what you did** → state it plainly and completely, unprompted. What changed, what broke,
  what is still unfinished. Never gate it behind a question.
- ⚠️ **Short ≠ dense. More than ~2 parts → bullets or a small table.** Compressing five items into one
  paragraph of semicolons is *harder* to read than the long version, which defeats the cap. Structure
  costs no length. (Learner, same day: *"this was a hard to read paragraph, make it more readable…
  in either bulletpoints or some other way"*.)
- **NOT capped**, because these were never the problem: the comfort-rating rationale (propose + why),
  concept explanations when stuck or asked, `stuck_log`/debrief/memory writing, and reporting that an
  action may have gone wrong or a finding that changes what to do next — state it, then stop.
- **Depth goes in a file, not the chat.** Same move as [[feedback_teaching]]: if it is worth
  keeping, it belongs in a note that gets reread, not in scrollback.

Full rule: the *Token discipline* section of `CLAUDE.md`. Related: [[feedback_teaching]],
[[feedback_interactive_learning]].
