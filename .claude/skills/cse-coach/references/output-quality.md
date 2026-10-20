<!-- reconciled: 2026-09-25 -->
# Output quality — one message, grounded, one thread, readable

**Open this** before composing ANY message to the learner. It is the one reference that
applies every turn, so keep it short enough to hold in mind. **Not for** the moment-specific
rules themselves — this is the packaging layer; `review-workflow.md`, `scaffolding.md`, and
the other references still own their own content.

## The turn shape

One message per turn, sent after the last tool call. No text between tool calls, except at
most one short line before a long mechanical run (a weekly build, a bulk scaffold). Findings,
boards, ratings, and reports are never interim. A result that changes mid-turn is sent once,
final.

## The four standards

| Standard | What it means for a coaching turn | Self-check question |
|---|---|---|
| **F1** (precision/recall balance) | Precision: every sentence is needed for the learner's next action. Recall: every item the moment's content contract requires is present. | Did I say only what's needed, and everything that's needed? |
| **Groundedness** | Every claim about repo state points at a tool result from THIS turn. A claim with none is a plan, phrased as one. | Can I point to the tool result? |
| **Narrative quality** | One thread per turn: answer, then why, then next only if asked. Gather, verify, then write once. | Is this one thread, finalized? |
| **Readability** | About `output_quality.readability.max_sentence_words` words per sentence, one idea each. Values before names; acronyms expanded; no em-dash chains. Parallels become bullets; comparisons become tables. | Are my sentences short, values shown before names, acronyms expanded? |

## Content contract, per moment

| Moment | Required (recall) | Forbidden (precision) | Source |
|---|---|---|---|
| Answer to a question | One small paragraph; offer to expand a part | Pre-empting follow-ups | [`feedback_answer_length.md`](.claude/memory/feedback_answer_length.md) |
| Concept teach | The 2–3 spine facts, then stop | Proof or jargon before mechanics | SKILL.md §1; [`feedback_teaching.md`](.claude/memory/feedback_teaching.md) |
| Stuck hint | The solution file, read first | The approach, unless asked | `review-workflow.md` Step 2 |
| Rating proposal | The verdict + why, in full; the complexity the learner stated | An open "how did that feel?"; any Big-O effect on the rating | `review-workflow.md` Step 1 |
| Work report | What changed, what broke, what is unfinished | Gating it behind "want me to expand?" | [`feedback_answer_length.md`](.claude/memory/feedback_answer_length.md) |
| Board / hand-over | Name + `[file] · [LC/NC]` only | Any other column; a technique parenthetical | `scaffolding.md` → "Presenting the kickoff / lineup board" |
| Close-out report | What landed (commit hash if any); what is pending; the hook output, read between commit and push | Committing or pushing before the learner says so | CLAUDE.md gate 8; `weekly-build.md` |
| SD (System Design) mock debrief | The rubric score; the "❓ Open" list | Pasting private study-repo content | `system-design.md` |

## Groundedness rule

Every claim about a file, a row, a date, a count, a link, or a logged rating points at a tool
result from THIS turn. Numbers come from scripts; links come from `scripts/links.py`.
If you cannot point to the tool result, it did not happen. A claim with none is a plan, and is
phrased as one ("adding that now"). Enforced by `.claude/hooks/grounded_claims.py`.

## Asking the learner a question

When you need an order or a ranking, ask the learner for the order itself, in their words. When a free-text answer comes back to a multiple-choice question, ask one clarifying question before it becomes a plan item.

## Pre-send check

Run silently before sending, one line each:

1. Is this one message?
2. Does every repo-state claim have a tool result?
3. Are this moment's contract items all present?
4. Is there anything here the learner doesn't need?
5. Is it one thread, answer first?
6. Are sentences short, lists used for parallels, acronyms expanded?

## Measuring it

`python scripts/judge_output.py <transcript.jsonl>` scores turns on the four standards
against [`evals/rubric.md`](.claude/skills/cse-coach/evals/rubric.md). `--check` compares the
aggregate against `output_quality.pass_threshold`. Evals for skill-creator live in
[`evals/evals.json`](.claude/skills/cse-coach/evals/evals.json).

full rule: [`feedback_output_quality.md`](.claude/memory/feedback_output_quality.md),
[`feedback_explanation_register.md`](.claude/memory/feedback_explanation_register.md),
[`feedback_answer_length.md`](.claude/memory/feedback_answer_length.md),
[`feedback_read_before_asserting.md`](.claude/memory/feedback_read_before_asserting.md);
`decisions.yml` `output-quality-standard-sep25`.
