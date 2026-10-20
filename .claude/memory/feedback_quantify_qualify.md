---
name: feedback_quantify_qualify
description: In system design, drill quantify (a number on every claim) + qualify (condition + boundary on every choice) at every framework step
metadata:
  type: feedback
reconciled: 2026-09-11
---

**Operational rule lives in the skill** — `references/system-design.md` ("During & after the mock"). This file is the *why*.

Standing SD coaching discipline (learner requested Jul 20, 2026): push the learner to **quantify and
qualify** every statement so they build the habit of high-quality, senior-level answers.

- **Quantify** = a number on every claim. "Read-heavy" → "100:1, ~100k read QPS vs ~1k write." Turns an
  assertion into checkable reasoning.
- **Qualify** = a condition + boundary on every choice. Name the assumption (what must be true), the
  tradeoff (what was given up), and where it breaks + the alternative. "Eventual consistency" →
  "eventual because a 2s-stale redirect is harmless; payments would force strong."

**Why:** it's the single highest-leverage *speaking* habit in the interview — the difference between
"correct" and "senior." Volunteering the number/condition before being asked is the signal interviewers
grade.

**How to apply:** at every framework step, when the learner states a bare adjective (fast, big,
scalable, heavy, read-heavy) or a bare choice, **push for the number and the condition** before moving
on. Coach them toward the fusion template: *"I'll use [choice] because [quantified pressure]; it trades
[X for Y] and holds while [condition] — it breaks at [scale], where I'd move to [alternative]."* Full
per-step targets + examples live in `<your-sd-study-repo>/framework.md`
("Quantify & Qualify" section). Pairs with [[feedback_hld_altitude]] — altitude keeps them in the right
step, quantify/qualify makes each step's answer defensible.
