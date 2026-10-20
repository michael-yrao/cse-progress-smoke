---
name: feedback_output_quality
description: One message per turn, sent after the last tool call; every repo-state claim names its tool result; four standards (F1, groundedness, narrative quality, readability) score a coaching turn
metadata:
  type: feedback
reconciled: 2026-09-25
---

Operational rule lives in the skill — [`references/output-quality.md`](.claude/skills/cse-coach/references/output-quality.md); this file is the why + evidence.

**Why:** the learner asked (2026-09-25) for this skill to stop overloading its output. This
is a client-facing skill, and other adopters read it too, so the packaging matters as much as
the content. The standard is built around four dimensions:

| Standard | Meaning |
|---|---|
| **F1** | Say only what's needed, and everything that's needed. |
| **Groundedness** | Every repo-state claim points at a tool result. |
| **Narrative quality** | One thread per turn, finalized before speaking. |
| **Readability** | Short sentences, tables for parallels. |

Nothing overloads the learner unless the answer is already final.

Evidence that these were live failure classes before this rule:
- 2026-08-03 (`self_eval_log.md`) — claimed a note was updated ("added to your note") before the
  write happened; the edit landed a turn later.
- 2026-08-21 [P1] (`self_eval_log.md`) — reported an edit that was never made, a grep mistaken
  for a write.
- 2026-08-21 [P1] (`self_eval_log.md`) — reported a schedule-integrity failure that had not
  happened, from a partial read.
- 2026-07-15 (`feedback_teaching.md`) — a pedagogically strong session buried in "walls of text".
- 2026-08-17 (`self_eval_log.md`) — a work report truncated by misapplying the answer-length cap.

**How to apply** — mirrors the pre-send check in `references/output-quality.md`:
- Send one message per turn, after the last tool call, never between them.
- Point every repo-state claim at a tool result from this turn, or phrase it as a plan.
- Check this moment's content-contract items are all present before sending.
- Cut anything the learner doesn't need for their next action.
- Keep one thread per turn: answer first, then why, then next only if asked.

Related: [[feedback_answer_length]], [[feedback_explanation_register]],
[[feedback_read_before_asserting]], [[feedback_verify_terminal_actions]].
