---
name: feedback_learner_code_boundary
description: What the coach may and may not touch in the learner's solution — a pure tooling artifact (dating a helper for the stash) yes; their reasoning or comments never
metadata:
  type: feedback
reconciled: 2026-09-11
---

**Operational rule lives in the skill** — `SKILL.md` invariant + `references/retry-and-restore.md`
(dated-helper / duplicate-name warning). This file is the *why* and the boundary. Merges the former
`coach_dates_helper_classes` and `dont_rewrite_learner_comments`. See also
[[feedback_coding_rules]] (never edit `.py` logic) and [[feedback_no_spoilers]].

**The line:** the coach may edit a **pure tooling artifact** the learner delegated; the coach may **never**
touch the learner's reasoning — their code logic or their comments.

## Coach dates helper classes (tooling artifact → coach touches it)

The learner writes helpers (`TrieNode`, `Node`, `ListNode`) with their **natural** names — what they'd
write on LeetCode or in an interview. The **coach** renames an undated top-level helper to
`<Name>_<YYYYMMDD>` at rating/close-out time (one `replace_all` on the name + references; check it didn't
also hit illustrative text in the scaffold banner and revert that), **before `restore_history.py`** runs.
Never ask the learner to date a helper. *Why:* the dated name exists only to stop today's helper colliding
with a same-named one from a prior attempt when restore merges the stash (Python keeps the *last*
definition — the 208/211 `TrieNode` incident). That's a repo-tooling artifact, not real practice; forcing
it on the learner trains an unnatural habit (*"I wouldn't name it like that … in an interview"*, Aug 22).
(Upstream: the real fix would be restore auto-namespacing, but its invariant is never to parse the
prior-attempt slice — see [[project_upstream_candidates]].)

## Never rewrite the learner's comments (reasoning → hands off)

A comment the learner wrote is **their verbal-communication rep** — the skill an interview grades in its
first minutes. When one is drifted/inaccurate, **name what's wrong and let them reword it** ("line 35 still
describes the old size-based rule"), then stop — even when they ask "how do I fix this comment?", answer
with *what it should convey*, not the sentence to paste. *Why:* rewriting it hands over the articulation,
which is the thing being trained (learner, Aug 22, after the coach rewrote a drifted comment on 239).

**The contrast is the whole rule:** tooling scaffolding (helper dating) = coach may touch; the learner's
own reasoning (code logic, comments) = never.
