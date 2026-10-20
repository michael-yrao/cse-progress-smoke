---
name: feedback_commit_discipline
description: Why the coach asks before every commit/push, accumulates edits into one commit, sweeps git status first, and treats a close-out signal as not-yet-permission — the 31-commit failure behind it
metadata:
  type: feedback
reconciled: 2026-09-14
---

**Operational rule lives in the always-injected layer** — CLAUDE.md gate 8 (ask before every commit/push)
and `SKILL.md` §3 / `references/review-workflow.md` §8. This file is the *why* + the failure log. Merges
the former `batch_commits` (anchor), `git_commit`, `end_of_session_push`.

## Ask before every commit and every push — no exceptions

Set by the learner Aug 16, 2026 (*"ask me before you commit and push, always."*). Make the edits, say what
is staged, **stop**; the learner decides when it lands.

**This replaced a weaker rule that failed.** The prior wording — commit once at the end *"or at a natural
breakpoint"* — is a loophole wide enough to drive a session through: *every* finished unit reads as a
natural breakpoint. **31 commits ran in the Aug 15–16 session under it.** Judgement was the failure point,
so the rule no longer asks for judgement.

## Accumulate, don't commit per problem

Make the per-problem edits (solution file, tracker row, `stuck_log`, schedule strike) as normal, but **don't
`git commit`** each time — they land in one commit when the learner says so. *Why:* every commit fires the
pre-commit hook, which rewrites `dsa_progress.md`, which makes the harness re-inject ~70 lines of the
tracker as a "file modified" notice — ~25 tracker dumps in a session, a large avoidable input-token cost
that compounds (every turn re-sends the conversation; the prompt cache expires over study breaks).

## Sweep git status first; most close-out phrases are not yet permission

- Run `git status` before the final commit to catch **unstaged solution files** — docs/schedule were once
  committed while the learner's new `.py` files were missed. Include any dirty `dsa/leetcode/*.py`
  (incl. post-logging refactors); run `restore_history.py` + `update_review_dates.py` before the final commit.
- A **vague** close-out (*"call it a night"*, *"that's enough for today"*) reports that the work is done — it
  is **not** publish authorization. Surface what's unstaged and *ask* ([[feedback_verify_terminal_actions]]).

## The designated authorization phrase — "close out the day" (Sep 14, 2026)

The learner granted a scoped exception: **an explicit close-out-and-publish instruction IS standing
authorization to commit AND push** without per-action confirmation. Phrase family: *"close out the
day/session/week"*, *"wrap up and commit/push"*, *"commit and push and close"*. Do the pre-commit sweep,
then **report what landed** (transparency, not a second ask).

**Why this does NOT reopen the 31-commit hole.** That failure was **agent judgement** — the agent deciding a
"natural breakpoint" had arrived. This trigger is the **learner's explicit phrase**; the agent never infers
it. Same premise-expired reversal as the advance-prompt-tail hook: the absolute "ask every time" was a
guard against agent discretion, and a learner-uttered command is not agent discretion.

**Still hold and ask (pending-confirmation carve-outs):** an unrated or uncertain rep; an unsettled schedule
or structural decision (SD restart, an over-ceiling day not yet accepted, a deferral without agreement); a
**weekly** close-out whose archive + next-week build isn't done (gate 7 runs first); an unexpected git state
(conflict, detached HEAD, diverged remote); and **any irreversible action beyond an ordinary commit + push**
— deletions, `--force` push, history rewrite — which always ask. Normative sentence: CLAUDE.md gate 8;
dated in `decisions.yml` `close-out-commit-authorization`. The kickoff-scaffold hook now also excludes this
phrase family, so *"close monday session"* is never mistaken for a kickoff.

## The one exception, and how to take it

**Commit early anyway if** the learner is about to switch machines (unpushed work strands them across their
two machines) or the session is ending unexpectedly — losing work beats saving tokens. But **say so and
ask**; never decide unilaterally that this instance is the exception (that judgement is exactly what
produced the 31). See the Aug 16 entry in `self_eval_log.md`.

⭐ **Source-fix candidate (raised, not yet built):** a pre-commit warning when the session is not being
closed out would make this self-enforcing — the link rule is obeyed because a hook enforces it; this ran
unchecked all session because it is only prose. **Partly mooted by the Sep 14 authorization:** a commit on
"close out the day" is now *intended*, so the thing to guard is no longer "did the agent commit" but "did it
commit while something was pending" — a judgement a pre-commit hook can't see, so this stays prose for now.
