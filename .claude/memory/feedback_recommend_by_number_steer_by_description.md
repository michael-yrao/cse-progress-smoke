---
name: feedback_recommend_by_number_steer_by_description
description: When recommending a problem, name only the pick by number+link; refer to problems you're steering away from by description, not number
metadata:
  type: feedback
reconciled: 2026-09-11
---

**Operational rule lives in the skill** — `references/scaffolding.md` ("Presenting the lineup"). This file is the *why*.

When answering "what's a quick one / what should I do", **name only the problem you are
recommending, with its link. Refer to every problem you are steering AWAY from by description
— "the Hard on the board", "the two 🟡s" — never by its number.**

**Why:** The link-reminder Stop hook ([[feedback_lineup_links_only]]) fires on *any* on-board
number mentioned without a link, and cannot tell a recommendation from a dismissal. On Aug 22,
2026 the coach recommended 3 but named 239 as a contrast ("239 is a Hard, not quick"); the hook
then forced 239's link to the top of the reply — **advertising the exact rep the coach was waving
the learner off.** The learner caught it: *"the hook is working against my question... you
responded with the problem I should do and the hook popped up the other problem."*

**How to apply:** A link is an invitation. Only the recommended problem should carry one. Describe
the alternatives so no stray number trips the hook and no unwanted rep gets advertised. This is
coach-side; the hook's inability to distinguish intent is noted as an upstream limitation in
[[project_upstream_candidates]].
