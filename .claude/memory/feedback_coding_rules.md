---
name: feedback_coding_rules
description: Why the learner codes every line from a blank page (coding is the only path to 🟢), writes data-structure defs inline, and the coach never edits their .py — plus the explicit-over-terse boundary
metadata:
  type: feedback
reconciled: 2026-09-11
---

**Operational rules live in the skill** — `SKILL.md` §2 (Comfort scale: coding required for 🟢) + the
invariant (learner writes every line), `references/scaffolding.md` (whiteboard fidelity, no shared imports),
`references/spaced-repetition.md` (the 🟢 rubric). This file is the *why*. Merges the former
`coding_for_clean`, `code_by_default`, `whiteboard_fidelity`, `no_code_edits`, `explicit_over_terse`.

## Coding is the only path to 🟢

A no-code blueprint (the 15-min warmup format) **cannot** log Clean — best it earns is 🟡, no matter how
flawless. The one carve-out: a flawless no-code spot check on an already-**🎓 Graduated** problem *confirms*
it (stays 🎓). *Why:* "mostly remembered it out loud" is not mastery; coding your way to Graduated is what
buys cheap no-code maintenance later.

## Code every rep by default — but scaffold only what was asked

Every rep is a **coded** rep by default, warmups included; a no-code blueprint is an explicit opt-in, not
the house default. *Why (Jul 14):* the approach was recalled fine but the **pointer/boundary arithmetic
collapsed at the keyboard** (206, 424, 75, 567, 901 all failed there, never on the approach) — a blueprint
can't catch what only breaks when you type it.

⚠️ **Reconciled contradiction (with `scaffolding.md`):** the old wording said *"scaffold a file for every
scheduled problem."* That is only true **on an explicit kickoff** — a *named* problem is a request that
scaffolds exactly what was named, and batch-scaffolding otherwise plants phantom tracker rows (see
`scaffolding.md` "Scaffold scope"). So: **code-by-default governs the REP FORMAT (coded, not blueprinted);
scaffolding scope governs WHICH files get made (only what the kickoff/request names).** They are different
axes. Warmups stay 15 min; if the day would blow the ceiling, trim warmup *count*, don't downgrade a rep to
no-code.

## Whiteboard fidelity — write the whole thing, including the node classes

Every solution is written in full from a blank page, including any `ListNode`/`TreeNode`/`TrieNode`/`Node`
definitions it needs. **No shared `datamodel` module to import** — re-deriving the scaffolding is part of
the rep, exactly as on an interview whiteboard. Importing boilerplate skips reps you should reproduce cold.

## The coach never edits the learner's code

Never edit `.py` files under `dsa/` — the learner writes and maintains every line; the coach reads,
explains, finds bugs, and offers fixes **as text they type themselves**. (Editing docs, schedules, and the
tracker is fine.) The coach *may* touch a tooling artifact — dating a helper class at rating time — but
never the learner's own logic or comments ([[feedback_learner_code_boundary]]).

## Explicit over terse — don't propose "more Pythonic" rewrites

The learner writes conditions longhand on purpose (`nr >= 0 and nr < rows` over `0 <= nr < rows`) — *"i
like being explicit with my code for easier readability"* (Aug 3, on 994). These are interview-rep
artifacts read cold weeks later under time pressure; an explicit conjunction has no idiom to misremember at
a whiteboard. **In a code review flag correctness, complexity, and misleading names** (e.g. `minSize` for a
threshold) — **never** chained comparisons, comprehension-vs-loop, `enumerate`/`zip`, walrus, or ternaries
whose only argument is brevity. Style was never a 🟢 criterion ([[feedback_infer_comfort]]). Repo tooling
under `scripts/` is ordinary code and follows normal style. (`no_code_edits` and `explicit_over_terse` are
distinct edges kept here together — the first is a hard invariant, the second a review-scope rule.)
