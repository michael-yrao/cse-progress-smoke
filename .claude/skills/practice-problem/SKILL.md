---
name: practice-problem
description: >-
  How a LeetCode problem gets its practice spec (dsa/tests/<n>_<snake>.yml, run in the
  browser on the site's practice page) and its site solution (a .steps.ts walkthrough with
  grounded code, a showcase.yml pick, a bigo.yml pick). Use when a problem is seated on a
  week with no spec; for "write a practice spec", "make N runnable", "add a solution /
  visualizer / walkthrough for N"; when adding a .steps.ts; or when picking a showcase or
  Big-O entry. This is the procedure behind the weekly build's spec step.
---
<!-- reconciled: 2026-10-19 -->
# practice-problem — a problem number to a verified spec and a site solution

Two halves, each a reference. Open only the half the task needs.

| Half | Produces | Lives in | The site shows it as | Reference |
|---|---|---|---|---|
| **Spec** | `dsa/tests/<n>_<snake>.yml`, exported to `dashboard/practice.json` | this repo | the editor and Run on `/practice/<n>` | [`references/spec.md`](references/spec.md) |
| **Solution** | `<category>/<id>.steps.ts`, a `dashboard/showcase.yml` pick, a `dashboard/bigo.yml` pick | the site repo and this repo | the Solution tab on `/practice/<n>/solution` | [`references/solution.md`](references/solution.md) |

A problem may have either half or both. The site's catalogue reads them separately:
`isRunnable` is "the contract has this number", `hasSolution` is "the number is in
`ALL_ALGORITHMS`" (`src/app/features/practice/practice-catalogue.ts` in the site repo).

## Invariants for both halves

1. **LeetCode's number is the join key** everywhere: the spec's filename and `number`, the
   steps file's `lcNumber`, `lc:` in `showcase.yml` and `bigo.yml`. Never match by title or slug.
2. **A wrong value is a hard error, never fail-soft.** `export_practice.py`, `export_showcase.py`
   and `export_bigo.py` all exit 1 on a spec or pick they cannot resolve (decisions
   `practice-contract`, `showcase-contract`, `bigo-contract`). Do not loosen a check to make it pass.
3. **Nothing is hand-copied that a script derives.** The site stores no solution code and no
   expected value of its own; it fetches `showcase.json` and `practice.json`.
4. **Every number you state comes from a command run in this turn.** Counts of specs, problems
   or picks go stale; run the script and quote it.

## Where each rule is stated (read these; do not restate them)

| Subject | Source |
|---|---|
| The spec contract, its shapes, its figure | `decisions.yml` `practice-contract`, `practice-contract-shapes`, `practice-figure`, `practice-figure-shapes-oct4`; `scripts/export_practice.py` docstring and `validate_spec` |
| Running a solution file against a spec | `scripts/check_practice_spec.py` docstring |
| Spec at seating | `cse-coach/references/weekly-build.md` ("Write a practice spec for every seated problem that has none") and `scaffolding.md` ("When a spec exists, the scaffold reads it") |
| Grounded code | `decisions.yml` `showcase-contract`; `dashboard/showcase.yml` header; `scripts/showcase_candidates.py` |
| Big-O picks | `decisions.yml` `bigo-contract`; `dashboard/bigo.yml` header |
| The site's solution rules | the site `CLAUDE.md`: "Source of truth", "Visualizer quality bar", "Wiring a new visualizer" |

## Commands (each exists; `--help` shown by every script)

| Question | Command |
|---|---|
| Do all specs validate, and is `practice.json` current? | `python scripts/export_practice.py --check` |
| Does a solution file pass a spec? | `python scripts/check_practice_spec.py <spec> <solution> [--method NAME]` |
| Which attempts can a showcase entry pick? | `python scripts/showcase_candidates.py <numbers>` |
| Does every showcase pick resolve? | `python scripts/export_showcase.py --check` |
| Does every Big-O pick resolve? | `python scripts/export_bigo.py --check` |
| Is this skill read against every decision? | `python scripts/reconcile.py` |

`--check` and `--stdout` write nothing. `export_practice.py` with no flag writes
`dashboard/practice.json`; the pre-commit hook also regenerates it when a spec is staged.
