---
name: feedback_hld_altitude
description: In system design, the learner defaults to LLD (storage shape, data structures, DB internals) — hold them at HLD altitude through steps 1–4
metadata:
  type: feedback
reconciled: 2026-09-11
---

**Operational rule lives in the skill** — `references/system-design.md` ("During & after the mock"). This file is the *why*.

The learner thinks like an implementer and **defaults to low-level design** in system-design
sessions: given a step-2 "name the core entities" prompt they jump to storage shape ("key-value
mapping"), datastore choice ("we want Redis"), and persistence internals (AOF vs RDB snapshots).
Self-identified this on Jul 20, 2026 during the URL-shortener framework drill ("this made me realize
how much I lack in HLD, my thoughts go directly to LLD").

**Why:** it's not a knowledge gap — it's an **altitude** problem, and the strongest tell of an
implementer's instinct. It only hurts in the first ~20 min of an SD interview, where premature LLD
commits to details before the structure exists and *loses* signal. This is currently the
highest-leverage thing to coach in the SD track.

**How to apply:** hold them at HLD altitude through framework steps 1–4. When they drop into a box
(fields, data structures, persistence config, DB choice) before the step calls for it, **name the
altitude slip explicitly** and pull back out — "that's LLD / step 5, park it." The tell to give them:
*"Am I drawing a box, or standing inside one?"* HLD = boxes + arrows + request flow; LLD = the inside
of one box, earned only when a deep dive drags you there. The framework's step order is the guardrail —
enforce the gate. See [[project_sd_mock_model]], [[feedback_teaching]]. ⚠️ Under the mock model this is enforced **as the interviewer**, not as a coach reminding them — name the slip and move on.
