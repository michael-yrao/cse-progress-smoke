<!-- reconciled: 2026-10-19 -->
# Retries: hide prior attempts, restore at session end

**Open this** when scaffolding a retry (a problem whose file already exists) or when
closing out a session before the commit. **Not for** new problems — that's
`scaffolding.md`. **Not for** reading or parsing a learner's prior solution to decide
anything: the slice is opaque by design (see the invariant below).

## Retries must not show prior attempts

**On a retry the new stub goes at the TOP** of the `Solution` class. Everything below it
(the prior attempts) is MOVED OUT of the file into a per-problem stash at
`<root>/.history/<number>_<snake>.txt`. Reading your own previous solution before a retry
destroys the rep — the point is recall from a blank page. So the spoiler isn't hidden, it's
*physically absent* while you work. The file holds only the statement, today's blank stub,
and a one-line pointer to the stash.

This needs **no editor and no extension** — it reads as a blank page in any editor, on
GitHub, in a plain `git diff`. That portability is the whole reason for the stash. The old
approach folded attempts with the `zokugun.explicit-folding` extension, whose config had to
be reproduced by hand on every machine — all gone. It's a speed bump, not a lock: the stash
is one click away, and that's accepted. What it buys is that seeing your old solution becomes
a deliberate act, not an accident.

**Module-level helpers move too (source fix).** A helper the learner wrote above
`class Solution` (`class UF`, `class TrieNode`) goes to the stash with the prior attempts, below a
marker line, and restore puts it back directly above `class Solution`. A class the stub's own
signature names (`TreeNode`, `ListNode`, `Node`) is the problem's interface and stays in the file.
A stash with no marker line is the older format and restores as before. One case still stays in
view, so name it in the hand-over when you see it: a module-level helper that is not a `def` or
`class` (an assignment, a lambda).

## Restore the stash once the day's reps are done

The stash protects *before* the attempt. Once the rep is written, the prior attempts belong
back as dated history — **restore at end of session, before the commit:**

```sh
python scripts/restore_history.py            # today's completed attempts
python scripts/restore_history.py --dry-run  # report only
```

Restore pastes the stash back *after* today's completed attempt (recent on top), deletes the
stash file, and strips the pointer. This reconstructs the single file with full dated history,
exactly as before the extract. It also migrates **legacy folded files**: a solution still
carrying an old `# region ⚠ PRIOR ATTEMPTS` fold has the markers stripped here.

- **It only restores** a problem whose dated attempt has a real body. A retry scaffolded but
  never attempted still has `pass` under today's stub. Pasting the prior attempts back would
  expose the old solution before the rep happened, the exact failure the extract prevents.
  Those keep their stash *out* of the file and are reported as kept. `--all` overrides the
  guard (for reconciling old files, never at session end).
- **Committed, but self-clearing.** `.history/` is tracked, not ignored. On a normal day
  restore empties it before the session-end commit, so nothing extra is committed. If a
  session is **cut short**, the stash files are still committed — the extracted state travels
  to the next machine (where restore finishes the job). A cut-short-then-resumed retry
  re-extracts safely: an un-attempted stub is dropped and the existing stash is left untouched
  (never clobbered with an empty stub).
- **Restore dates today's colliding helper itself.** An undated
  helper in today's code that a restored attempt also defines (`UF`) becomes `UF_<stamp>`:
  definition and uses, today's code only, never the stash. It also strips the old
  `# NOTE: suffix any helper class` banner. The learner writes or pastes helpers with plain
  names; the oldest stays the undated canonical one. Without this, Python binds the *last*
  definition and today's code runs the older class (found on 211, two identical `TrieNode`s —
  nothing crashed). The duplicate-name warning remains as the net when restore can't rename
  (no stamp, unparseable body).

### Worked example — a retry, start to finish

```sh
# 1. Scaffold the retry (file already exists) — prior attempts move to the stash
$ python scripts/new_problem.py --number 211 --title "Design Add and Search Words" \
    --pattern trees --method addWord
Retry: inserted addWord_20260910 at top of class Solution
Stashed prior attempts → .history/211_design_add_and_search_words.txt
```

The file now reads as a blank page:

```python
class Solution:
    def addWord_20260910(self, word: str) -> None:
        pass
    # prior attempts stashed → .history/211_design_add_and_search_words.txt
```

```sh
# 2. …learner writes the attempt, coach rates it…
# 3. End of session, before the commit — restore
$ python scripts/restore_history.py
Restored 211 (addWord_20260910 has a body); stash removed.
```

## The load-bearing invariant (unchanged from the fold era)

Today's stub goes at the **top**, and *everything below it* is the prior-attempts slice. It is a
**verbatim line slice**, moved to the stash and later pasted back **without the script ever
parsing its shape**. Dated methods, dated sibling classes, and trailing unittest blocks all vary
and are not ours to interpret. Extract cuts at EOF; restore appends at EOF; today's attempt
sits above. **Keep it that way** — anything that reaches *into* a prior solution to decide the
cut is how this breaks.

## Notes for whoever maintains this

- **The un-attempted guard ignores scaffold method signatures** inside a dated *class* attempt
  (fixed Aug 10, 2026). `attempt_has_body` counted any non-`pass` line as work, so a design
  problem's own `def __init__(...)`/`def add(...)` made every multi-method scaffold look
  attempted. Restore would paste the prior solution back before the rep ran. Found on 703
  (`class KthLargest_20260810`). Single-method (`def <name>_<stamp>`) scaffolds were never
  affected — their body really is just `pass`.
- The stash is a **`.txt`**, deliberately: it never matches the `*.py` source glob, so
  discovery (`update_review_dates.py`) ignores it and no phantom row appears. If you ever add
  `.txt` to `source_globs`, exclude `.history/` there.
- **Two scaffold layouts, one slice.** Single method → a dated `def <method>_<stamp>` at the
  top of `class Solution`; the slice is the remaining indented methods. **Multi-method**
  (`--method encode,decode`) or a legacy file with no `class Solution` → a dated
  `class Solution_<stamp>` at module level (matching
  [271](dsa/leetcode/arrays_and_hash/271_encode_and_decode_string.py)). The slice is the prior
  module-level classes. Either way the slice pastes straight back.
- The stub carries the problem's **real signature**, pulled from the existing method. A *new*
  problem has no prior method to read — that's what `--signature` is for.
- `new_problem.py` strips any leftover pointer and legacy `# region` markers before
  re-extracting, so it's idempotent and migrates old folded files on their next retry.
- `restore_history.py` keys the stash back by **problem number** (globs `<root>/*/<number>_*.py`)
  because the stash filename drops the pattern folder. The number is the identity. That's the same
  reason `new_problem.py` matches on it, and **refuses** a write whose `--title`/`--pattern` would fork
  history into a second file (naming the file it found; `--force-new` overrides).
