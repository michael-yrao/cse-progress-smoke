---
name: feedback_site_plain_language
description: every label, chip and number shown on the site must be understandable on its own — no coach-internal vocabulary ("variant gap", "thin", a bare "0/2") without plain wording or an explanation on the page
metadata:
  type: feedback
reconciled: 2026-10-19
---

**Anything the site says must be easily understandable by someone who has not read the repo.** Set by the
learner after asking what "variant gap" meant on a technique's Mastery row: *"if it says something
on the site, it should be easily understandable."*

**Why:** the Mastery tab was rendering the coach's internal vocabulary straight from the coverage report —
`thin`, `variant gap`, `no 🟢` — and an unexplained ratio. The learner read a `0/2` as "the study guide has
only 2 problems for this technique". It had seven; the 2 is `min_problems`, the coverage bar. A label that
needs the repo to decode is wrong on a public page, and a number with no unit gets read as the nearest
plausible thing.

**How to apply:**
- A chip or label is a plain phrase, not a term of art: say what the learner would do about it ("needs 2 more
  problems", "one variation not tried yet"), not what the report calls it.
- A number carries its unit and its meaning on the page: "1 of 3 needed", never a bare "1/3".
- If a term must stay, the page explains it where it appears (a hover title AND visible legend text — a hover
  alone is invisible on a phone).
- This governs the SITE. The coach's own files (`technique_coverage.md`, `techniques.yml`, the tracker) keep
  their vocabulary; the translation happens at the render, not in the data.
- Before shipping a site change that adds a label, read it as a stranger would. Same test as
  [[feedback_expand_acronyms]]: an unexplained term halts the reader rather than degrading gracefully.

Related: [[feedback_expand_acronyms]], [[feedback_explanation_register]].
