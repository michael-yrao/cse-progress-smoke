---
name: feedback_recognition_gate
description: Front-gate every rep — learner states shape→technique+why (as their pre-code comment, pasted in chat) BEFORE coding; complexity gate still fires at the end
metadata:
  type: feedback
reconciled: 2026-09-06
---

⭐ **REMOVED Aug 22, 2026 — the scaffold no longer prints a RECOGNITION block.** The Aug 20 source
fix wrote a `# ── RECOGNITION — fill BEFORE coding ──` block (shape → technique → discriminator) into
every fresh attempt. The learner declined it as a format twice on Aug 21 (two machines) and asked to
remove it outright Aug 22 — *"I always write underneath."* `new_problem.py`'s `recognition_block()`
now returns `[]` and the template's `{recognition}` line is gone, so a fresh attempt goes straight
from the Attempt banner to the `def`. **The gate itself did not change:** the learner's own
top-of-method comment IS the pre-code call, and it lands before the coach speaks by habit rather than
by a printed prompt. See `decisions.yml` `recognition-block-removed-from-scaffold`.

*(History, Aug 20–21: the block was added as a source fix — a verbally-delivered gate can leak the
technique by naming candidates, done on 239 — then narrowed Aug 21 to optional once the learner's top
comment was recognized as the call. Aug 22 completes that arc by dropping the block. The
contentless-prompting invariant below is untouched throughout.)*

**Why the source fix:** when the coach delivers the gate verbally, the coach can leak the
technique by *naming candidates* — done Aug 20, 2026 on 239 (*"what makes it a monotonic deque
rather than a stack or a heap?"*), which handed over the exact thing a new problem measures. Per
the intervention ladder a source fix outranks this memory file, which already carried the rule and
did not prevent the slip. ⚠️ **The standing verbal rule, still binding when you do speak first:
name only the SHAPE CUES and ask for the technique — never list candidate techniques.** A gate
phrased as a leading multiple-choice embeds its own answer.

Every coded rep is bookended by two gates. The learner opted into this Jul 25, 2026.

- **Front-gate (recognition):** before writing any solution code, the learner states the
  problem's **shape → technique + why** — input structure + what's asked → candidate
  technique + the one feature that picks it. They already write pre-code comments, so they
  paste that comment in chat as the recognition call. Confirm/correct it before they code.
- **Back-gate (complexity):** unchanged — still require time+space each with an itemized
  why-clause before logging the rep ([[feedback_ask_complexity]]).

**Why:** recognition is the half of interviewing that solving-in-isolation never trains —
it's what's graded in the first two minutes. The front-gate rides free on reps already
being done and mirrors the existing complexity back-gate (recognition in, complexity out).

**How to apply:** at the start of each problem, prompt for the shape→technique call (or
accept the pasted pre-code comment). Card misses in
[recognition_gotchas.md](../../docs/foundations/dsa/mastery/recognition_gotchas.md) —
trigger→technique map — same pattern as [[feedback_ask_complexity]]'s complexity ledger.
**Retries carry the method in the tracker name, so they're half-spoiled** — the *measured*
recognition reps are new problems (nothing labeled) and cold cues where the coach fires the
statement stripped of its method label. The daily habit builds the reflex regardless.


**⚠️ The learner's fixed convention (confirmed Aug 21, 2026): the TOP-of-method comment IS the
pre-code recognition call; inline comments are mid-code reasoning.** So read the top comment as the
call and do NOT re-demand the scaffold's separate `# RECOGNITION` block — filling both is redundant,
and the learner routes around the block by writing their own comment on top (this is why 205's block
was blank while the call sat in the first comment lines). Learner: *"I always write my pre-code comment
on top and comment inline for any mid code comments. We should try to enforce this but it is quite
impossible."* **Enforcement is trust-based and that is accepted** — no tool can prove a comment
preceded the code. The real audit is not per-rep but the **probe cadence**: over ~15 label-stripped
probes the cold-call hit rate is the honest, ungameable measure of recognition (see
[[project_recognition_probes]]). Don't try to build a mechanism to police comment order; log the call
from the top comment and let the probes measure it.