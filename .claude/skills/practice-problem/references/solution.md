<!-- reconciled: 2026-10-19 -->
# Solution half — a problem number to a site walkthrough, a showcase pick and a Big-O pick

The site stores no solution code. Its walkthrough traces the learner's real lines by anchor,
and the code is fetched from this repo's `dashboard/showcase.json`. The site repo is a
sibling checkout of this repo; locate it on the current machine (the site's `CLAUDE.md`,
"Source of truth"). If the learner's solution is missing from this repo,
ask before writing one (same file).

## The three artifacts

| Artifact | Where | Join key | Checked by |
|---|---|---|---|
| Walkthrough | site `src/app/algorithms/<category>/<id>.steps.ts`, exporting an `AlgorithmMeta` | `lcNumber`; `${lcNumber}:${variant}` for the code | `npm run check:groundedness` |
| Showcase pick | this repo's `dashboard/showcase.yml` | `lc` + `variant` | `python scripts/export_showcase.py --check` |
| Big-O pick | this repo's `dashboard/bigo.yml` | `lc` (or `lc:variant` for a twin file) | `python scripts/export_bigo.py --check` |

## 1. The showcase pick (this repo)

- One entry per (`lc`, `variant`): `symbol`, and when needed `container`, `file`, `helpers`.
  The `dashboard/showcase.yml` header defines each key; read it, do not guess a default.
- `variant` is the site's kebab-case approach id, never a date.
- List candidates with `python scripts/showcase_candidates.py <number>`. It never writes the
  manifest. A person reads the source and picks; add a `# why:` comment under the entry.
- Renaming or deleting a picked symbol is a breaking change that `--check` surfaces
  (`showcase-contract`).

## 2. The walkthrough (site)

1. **File and registration.** Create `src/app/algorithms/<category>/<id>.steps.ts`. It is not
   picked up automatically: in `src/app/core/data/algorithms.data.ts` add the `import` and add
   `<name>Meta` to `ALL_ALGORITHMS`. The site `CLAUDE.md` ("Wiring a new visualizer") says "the
   matching category's array"; in the file, `ALGORITHMS_BY_CATEGORY` is derived from
   `ALL_ALGORITHMS` by `category`, so `ALL_ALGORITHMS` is the one place to add it.
2. **Meta.** `AlgorithmMeta` in `src/app/core/models/algorithm.model.ts`: `id`, `lcNumber`,
   `title`, `difficulty`, `category`, `tags`, `description`, `examples`, `constraints`,
   `hint`, `solutions`. When the spec has no `statement`, the Description tab shows
   `description`, `examples` and `constraints`, so write them for a reader who has not seen
   the problem.
3. **One `SolutionVariant` per distinct approach.** Dated re-practices of one approach collapse
   to one variant, using the cleanest, most commented instance (site `CLAUDE.md`). Each
   variant has `label`, `variant`, `generateSteps`, `timeComplexity`, `spaceComplexity`; the
   model requires all five.
4. **Anchors, not pasted code.** Each step's `anchor: { match, nth?, to? }` resolves against
   the fetched `showcase.json`. Do not invent, paraphrase or hand-copy source, and keep the
   `explanation` faithful to the comments in the learner's lines (site `CLAUDE.md`).
   `two-sum.steps.ts` is a full example: `anchor: { match: 'if diff in map:' }`.
5. **The step trace.** The site's rule, quoted: "push a step for **every loop iteration and
   every recursion call** (including inner/nested loops, base cases, and returns) — never
   collapse a loop into a single summary step. Log every relevant variable in each step's
   `variables` / `state.counters`. No `generateSteps` may return `[]`." (site `CLAUDE.md`,
   "Visualizer quality bar".)
   - The only empty case the repo allows is the pending header on the file's first lines:
     `// Walkthrough pending — grounded code only. Variant '<id>' joins <n>:<id> (symbol <name>); …`
     with `generateSteps: () => []` (`happy-number.steps.ts`). The meta, the complexities and
     the showcase pick are all still required. The catalogue then shows `hasSolution` true and
     `isVisualized` false (`hasVisualization` needs a non-empty trace).
   - ⚠️ The quality bar says never `[]` and the pending form is `[]`. Both stand today.

## 3. The Big-O pick (this repo)

- An entry per problem in `dashboard/bigo.yml` with `time` and `space`, each a label from
  `export_bigo.COMPLEXITY_POOL`. The site checks answers by exact string equality against that
  pool, so a spelling outside it is a hard error.
- The pick is the latest dated attempt in the file; a file with no dated attempt needs an
  explicit `symbol:` (`bigo-contract`).
- Bounds are the learner's own rep. Write `TODO` for a bound not yet filled in; it is skipped
  with a warning, never emitted. Do not fill or verify a bound for the learner
  (`bigo-contract`).

## 4. Verify (site repo, then this repo)

| Check | Command |
|---|---|
| Anchors resolve | `$env:SHOWCASE_JSON = '<path to a fetched dashboard/showcase.json>'; npm run check:groundedness` |
| Lint, unit tests, build | the site `CLAUDE.md`, "Lint & test" |
| Showcase and Big-O picks | `python scripts/export_showcase.py --check`, `python scripts/export_bigo.py --check` |
| In the browser | `/practice/<n>` and `/practice/<n>/solution` (routes in `src/app/app.routes.ts`) |

`dashboard/showcase.json` is written by `export_showcase.py`; the pre-commit hook regenerates it
when a solution file or the manifest is staged. Point `SHOWCASE_JSON` at a copy that includes
your new pick.

## Limits

- `check:groundedness` (`ci/groundedness.check.ts`) checks the contract and that anchors
  resolve. A step's `explanation` and `state` are checked by reading them, not by a script.
- The two `--check` commands read the live solution files. An uncommitted edit that renames a
  symbol or empties a scaffold fails them even when the manifest is correct.
