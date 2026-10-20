---
name: project_recognition_probes
description: Weekly cold recognition probe — one unseen problem/week from an already-🟢 technique, label stripped, disposable (no tracker row on 🟢).
metadata:
  type: project
reconciled: 2026-09-06
---

<!-- TEMPLATE. The reusable design for a weekly recognition probe. Personal state (which techniques
     are banked, the live surplus/deficit numbers, per-probe history) belongs in the learner's own
     trackers/logs, NOT in this shipped file. -->

**The hole it fills.** Phase exit grades two axes, recognition and execution. The tracker measures
execution well and recognition **barely at all**, because *a retry names its own technique* — the row
says the method and the folder names the pattern, so the learner is told the answer before opening the
file. Recognition evidence must come from **new problems and cold cues**. A weekly probe supplies the
cold-cue reps the board otherwise lacks. See [[feedback_recognition_gate]].

## The design

| | |
|---|---|
| **Cadence** | ~1/week (a **consolidation rep** — a separate small budget; does **not** count against new-algorithm intake, [[feedback_consolidation_reps]]) |
| **Source pool** | techniques already at **🟢 or 🎓** in `technique_coverage.md`, **Medium or below** |
| **Which problem** | **pick the TECHNIQUE first**, then the easiest *unseen* problem that genuinely forces it. Difficulty is a consequence of the technique, never set in advance |
| **Tracker row** | **none if 🟢** — a disposable rep. Only 🟡/🔴 earns a row, because only a gap needs repetition |
| **Always logged** | the *recognition* outcome → `recognition_gotchas.md`, regardless of rating |

⚠️ **Never probe a technique that is 🟡 or has no 🟢.** Those need **conversion reps**, not probes — a
probe there just manufactures a 🟡 row. Probe only techniques whose execution is already banked, so the
measurement isolates recognition.

## Difficulty follows the technique

The rule is **"Medium or below," not Easy-only.** An Easy-only pool structurally cannot probe most
banked techniques — many exist only at Medium+ (Topological Sort, Union-Find, Monotonic Stack, Binary
Search on Answer, …), and those are disproportionately the ones where *recognition* is the hard part.
Easy-only therefore measures the easy half of the very axis the probe exists to measure.

1. **Pick the technique, then the problem** — the easiest unseen problem that genuinely forces it.
2. **Per-technique ratchet** — a technique probed at Easy that came back 🟢 gets its next probe at Medium.
3. **Cap at Medium; no Hard probes** — a Hard is the most expensive object in the system and typically
   fails on *execution*, contaminating a measurement whose subject is the pre-code call.

**Budget:** price the probe at the weekly build (a Medium probe is 🟡-equivalent × Medium, a real slot at
the ceiling, not a free extra).

## ⚠️ The scaffold path is a spoiler — this rep needs its own root

`new_problem.py` writes to `dsa/leetcode/<pattern>/<number>_<name>.py`, and **the path names the
technique**, handing over the answer before the statement is read. Use a **neutral root outside
`solutions.roots`** (e.g. `dsa/probes/`), which does double duty: a root outside `solutions.roots` also
stops `update_review_dates.py` from auto-resurrecting a tracker row for a deliberately untracked problem.

⭐ **Converse rule: when a probe comes back 🟡/🔴 and earns a row, MOVE the file into
`dsa/leetcode/<pattern>/` in the same edit.** Left in the probe root it becomes a tracked problem the
retry scripts cannot reach (`new_problem.py` and `restore_history.py` resolve under `solutions.roots`).
The probe root protects an *untracked* rep; once a row exists the protection is over.

**Strip the label everywhere:** don't name the pattern, topic tag, or neighbouring problems when
presenting it. The learner states **shape → technique → the one feature that picks it** cold, and *that
statement is the thing being measured* — the code is secondary.

## The free diagnostic

Because a 🟢 creates no row and a 🟡/🔴 does, **the row-creation rate over a rolling window of probes IS
the measurement of whether the pool still teaches**: mostly-🟢 → the pool has stopped teaching; a steady
stream of 🟡/🔴 → real gaps remain, keep consolidating.

⚠️ **Two ORDERED levers answer "the pool is mostly 🟢," cheapest first:** (1) raise difficulty inside the
pool you already own (Easy → Medium) — zero permanent demand; (2) **only when Medium is also mostly 🟢**,
open the next expansion tier — every new technique is maintenance demand forever. Exhaust the free lever
first.
