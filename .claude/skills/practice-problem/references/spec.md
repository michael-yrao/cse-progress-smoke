<!-- reconciled: 2026-10-19 -->
# Spec half — a problem number to a verified `dsa/tests/<n>_<snake>.yml`

A spec is one YAML file. `scripts/export_practice.py` turns every spec into
`dashboard/practice.json`; the site's practice page runs the learner's Python in the browser
against its cases. No reference solution is published, only inputs and expected values.
The weekly build requires one per seated problem (`cse-coach/references/weekly-build.md`).

## Read first, in this order

1. `decisions.yml` `practice-contract`, `practice-figure`, `practice-figure-shapes-oct4`, `practice-contract-shapes`, `practice-contract-ext-oct19`.
2. `scripts/export_practice.py`: the docstring, then `validate_spec` (every rule a spec must meet).
3. One existing spec in `dsa/tests/` for the shape you need (table below).
4. `scripts/check_practice_spec.py`: the docstring.

## Fields

| Key | Rule |
|---|---|
| `number`, `title` | LeetCode's number and title. `number` must equal the filename's leading number (the validator checks). |
| `url` | `https://leetcode.com/problems/<slug>/`. The slug is LeetCode's own (the tracker `docs/foundations/dsa/mastery/dsa_progress.md` links it); the site steps file's `id` is not always the same slug. A premium problem keeps its LeetCode URL. |
| `statement` | Omit it when the site has a steps file for the number: the Description tab then shows that file's `description`, `examples` and `constraints`. Write one when the site has no steps file. An existing statement stays. An indented statement line has a length cap that `validate_spec` names. `new_problem.py` scaffolds from the spec's statement when there is one, else from its own stub. |
| `entry` | `{class: Solution, method: <LeetCode's method name>}`: LeetCode's name, not the learner's (`search` for 704 even if the file says `loopSearch`). Design classes and round-trip: see Shapes. |
| `signature` | LeetCode's Python signature without `self`, e.g. `"n: int -> bool"`. Parsed by `new_problem.parse_signature`, so a scaffold and the site's blank editor agree. |
| `compare` | `exact`, `unordered`, `unordered-nested` or `unordered-inner`. Read the statement: if any order is accepted, say so here. `unordered` is any order at the top level; `unordered-nested` is also any order inside each inner list; `unordered-inner` is any order inside each inner list with the outer order fixed (a problem returning a pair of lists, such as critical and pseudo-critical edges). When the problem accepts any one of several whole answers, a case's `expected` is `{anyOf: [...]}` (below). |
| `cases` | The statement's examples first, each `example: true`, with `args` parsed from the site's `examples[].input` strings exactly. Then the stored random cases, sized per `scaffolding.md` ("When a spec exists…"). At least one case has `example: true`. One case per line, in flow style, as the existing specs do. |
| `figure` | Add one when an example input is a drawable graph or a grid (`practice-figure`, `practice-figure-shapes-oct4`). A grid: `kind: grid`, `gridArg`. A graph: `kind: graph` and exactly one edge source: `edgesArg` (an edge list whose endpoints are ints or names; an int node count via `nodeCountArg`, or named nodes via `nodesArg`, an argument listing the node names, never both), `matrixArg` (a square matrix; undirected only) or `adjArg` (a neighbour list; `oneBased: true` when its entries count from 1). `directed: true` for a directed graph. `highlight: expected` when the problem's expected value is a list of the drawn graph's edges. The site draws each `example: true` input from it. |
| `result`, `types`, `entry.kind`, `methods` | Only for the shapes below. |

**External-judge problems (9001–9999)** (decision `external-judge-plain-values-oct4`). `url` is the judge's
page (the practice page links its title to it) and `statement` is always written. The method name is the
title in camelCase. The problem is rebuilt as our own variant: a method call, 0-indexed, plain Python values,
never the judge's output strings or its stdin layout. A result that can be
infinite uses `number-inf` (Shapes).

A spec is data: no prose beyond a `#` comment where a rule below asks for one.

## Shapes

| Problem shape | Spec | Exemplar |
|---|---|---|
| Plain: returns its answer | no `result`, no `types` | `202_happy_number.yml` |
| Mutates an argument, returns None | `result: {arg: i}` compares argument `i` after the call | `75_sort_colors.yml` |
| Returns k, the first k items judged | `result: {argPrefix: i}`; any order allowed means `compare: unordered` | `27_remove_element.yml` |
| Linked list in or out | `types: {args: [list-node, …], result: list-node}`; a mutate-in-place list problem uses `result: {arg: 0}` with `types.args` only | `206_reverse_linked_list.yml` |
| Linked list with a cycle | `types: {args: [list-node-cycle]}`; each arg is `[[values], pos]` | `141_linked_list_cycle.yml` |
| Several linked lists in | `types: {args: [list-node-list, …], result: list-node}` (arg only); the arg is an array of arrays, each built as `list-node` builds it | none yet (23) |
| Returns a node of the input list | `types: {args: [list-node-cycle, …], result: list-node-ref}` (result only; needs a `list-node` or `list-node-cycle` arg); `expected` is the node's 0-based index, `null` for none | none yet (142) |
| Judge API the solution calls | a case's `judge: {isBadVersion: <int>}` binds that global for the case; the name must be one the exporter knows; `judge` is not an argument | none yet (278) |
| Any one of several answers | a case's `expected: {anyOf: [a, b, …]}`: `anyOf` is the mapping's only key and its list is non-empty; matches when one entry matches under `compare` | none yet (753) |
| Design class built from a node | an ops spec with `types: {args: […]}` encodes the constructor's args only; the list's length is the `__init__` parameter count; an `expected` element may be an `anyOf` mapping | none yet (382) |
| Linked list with random pointers | `types: {args: [random-list], result: random-list}`; each node `[val, randomIndex or null]` | `138_copy_list_with_random_pointer.yml` |
| Binary tree | `types: {args: [tree-node, …]}`; add `result: tree-node` when a tree comes back | `104_maximum_depth_of_binary_tree.yml`; `226_invert_binary_tree.yml` returns a tree |
| Tree plus node arguments | `tree-value` args and result address a node by its value; a `tree-value` arg needs a `tree-node` arg | `235_lowest_common_ancestor_of_a_binary_search_tree.yml` |
| Graph node | `types: {args: [graph-node], result: graph-node}`, a 1-indexed adjacency list | `133_clone_graph.yml` |
| Number result that can be ±infinity | `types: {args: [null, …], result: number-inf}` (result only); `expected` writes `math.inf` / `-math.inf` as `"Infinity"` / `"-Infinity"`, other numbers bare | `9001_single_source_shortest_path_negative_weights.yml` |
| Design class | `entry: {class: <Class>, kind: ops}`, a `methods:` list of `name(params) -> ret` lines, cases `{ops: [Class, put, get, …], args: [[…], …], expected: [null, …]}`. `ops[0]` is the class; `ops`, `args` and `expected` have equal length. | `146_lru_cache.yml` |
| Encode / decode | `entry: {class: Codec, kind: round-trip, encode: encode, decode: decode}`, `signature`, `decodeSignature`; `expected` is the input. `types` applies to the encode args and the decoded result, as for a single method | `271_encode_and_decode_strings.yml` |

`types.args` must have one codec per parameter in `signature` (the validator counts); for an ops spec, one per `__init__` parameter.
Arg-only codecs: `list-node-cycle`, `list-node-list`. Result-only codecs: `number-inf`, `list-node-ref`.

**`judge`.** A case may carry `judge: {isBadVersion: <int>}`. Before the call the runner binds a global of
that name for the solution, from a fixed registry (`JUDGE_APIS` in `check_practice_spec.py` and the site's
driver; `JUDGE_NAMES` in the exporter): `isBadVersion(v)` is true when `v >= <int>`. A case without `judge`
sees no binding. The statement names the API, as LeetCode's stub does.

**`anyOf`.** `expected: {anyOf: [a, b, …]}` passes when the result matches any one entry under `compare`.
The mapping has no other key and the list is not empty, else the validator rejects it. In an ops case an
element of `expected` may be an `anyOf` mapping; the outputs then compare element by element.

## A case must have ONE right answer under its compare mode

The site compares values. When the problem accepts several answers, build only cases that
admit one, or use an unordered mode.

| Situation | Rule | Say it in the spec |
|---|---|---|
| Any valid order or arrangement (course order 210, alien alphabet 269, itinerary 2097) | Only inputs whose answer is unique: a chain forces 210, a total order forces 269, a single Eulerian path forces 2097. The reference asserts uniqueness by enumeration or by construction. | A `#` comment at the top, as `210_course_schedule_ii.yml` does |
| Any one of several (peak 162) | Only inputs with a single answer (one peak), or `expected: {anyOf: [...]}` listing every valid answer when the list is small enough to enumerate | A `#` comment |
| Ties or several accepted lists (973, 347, 684, 1, 229, 417) | Avoid ties, else `compare: unordered` | `compare` |

## How an expected value is produced (the part that must not be wrong)

1. Write an independent reference solution in a session scratchpad, outside the repo, with the
   class and method named as the spec's `entry`. Never commit it.
2. Generate the extra cases with a small script in the scratchpad: the edge cases the
   constraints imply (empty where allowed, size 1, all equal, sorted, reversed, the maximum
   value, k at both ends) and random ones small enough to read by eye. Use a large size only
   where the constraint's upper bound matters, and sparingly. A matrix or grid input grows
   with n squared and `practice.json` is downloaded whole: keep every case line under about
   1,500 characters.
3. Check the reference against the spec:
   `python scripts/check_practice_spec.py dsa/tests/<spec>.yml <scratchpad>/<n>.py` must print PASS.
4. Check the learner's file against the same spec. Find it with
   `Get-ChildItem dsa/leetcode -Recurse -Filter '<n>_*.py'` (the category folder is not always
   the topic). Without `--method`, every method whose name starts with
   the entry's method name runs, so dated attempts (`isHappy_<date>`) each get a line.
   Use `--method` when the learner's name differs from LeetCode's.
5. Read the result:
   - A learner method that fails is reported by name. It may be a known-wrong attempt. It is
     never a reason to change an expected value.
   - No learner method passes, or the reference and the learner disagree on a case: stop on
     that problem and report it. Do not resolve the disagreement yourself.
6. `python scripts/export_practice.py --check` must exit 0. It validates every spec and
   fails if `dashboard/practice.json` differs from what the specs would produce, so it
   reports `practice.json` stale after you add a spec until the file is regenerated.

## Limits

- `check_practice_spec.py` has no timeout. A looping attempt hangs it; pass `--method` to
  skip that attempt.
- `random-list` cannot tell a returned original list from a copy.
- The site's in-browser Python (Pyodide) is verified only by running a problem in the browser.
  The checker uses the site's semantics but does not execute that path.

## When a commit is asked for

Stage the spec file(s) by name. The pre-commit hook regenerates and stages
`dashboard/practice.json` when a `dsa/tests/*.yml` is staged, and runs `--check` report-only:
read its output before the commit counts as clean. A spec creates no solution file and
plants no tracker row (`weekly-build.md`).
