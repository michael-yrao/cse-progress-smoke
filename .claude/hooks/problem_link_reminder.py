"""Stop hook: block a turn that breaks one of four lineup/prose rules.

At Stop, read the last assistant turn from the transcript and run, in order:
  1. `broken_file_links`   - a `.py` link whose path does not resolve from the repo root;
  2. `spoiler_lineup`      - a lineup TABLE carrying more than problem name + links;
  3. `advance_prompt_tail` - a short trailing nudge to the next rep;
  4. `banned_opener`       - a throat-clearing interjection opening a paragraph.
The first match blocks once with its message so the agent re-emits the turn.

Deliberately conservative - a hook that cries wolf trains the agent to skim past it.
`stop_hook_active` short-circuits, so it can never loop.

The bare-number link check (a problem number with no markdown link) was removed
2026-10-18 at the learner's request: it read moved-out schedule rows as today's board
and matched non-problem numbers.
"""
import json
import re
import sys
from pathlib import Path

# The TARGET of a markdown link (the part in parens), captured. Used to check that a
# solution-file link actually RESOLVES — a present-but-dead link passes the "is it
# linked" test above while clicking does nothing. This is the Aug 27, 2026 lapse: paths
# copied from a schedule row (`../../../dsa/...`, correct relative to that file, dead
# relative to the repo root the chat renderer uses).
MD_LINK_TARGET = re.compile(r"\[[^\]]*\]\(([^)]*)\)")

REPO_ROOT = Path(__file__).resolve().parents[2]


def _is_real_user_message(entry: dict) -> bool:
    """True for a human turn, False for a `tool_result` carrier.

    Tool results are recorded as `type: "user"` entries *inside* an assistant turn, so
    they are NOT turn boundaries. Only an entry whose content holds no `tool_result`
    block ends the turn.
    """
    if entry.get("type") != "user":
        return False
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, str):
        return True
    if not isinstance(content, list):
        return False
    return not any(
        isinstance(block, dict) and block.get("type") == "tool_result"
        for block in content
    )


def last_turn_text(transcript_path: str) -> str:
    """All assistant `text` emitted since the last real user message.

    One turn spans MANY assistant entries — `thinking`, `text` and `tool_use` are each
    their own record — so reading only the final assistant entry sees a tool call and
    nothing else. Walk back to the last human message instead, skipping the interleaved
    `tool_result` carriers and any sidechain (subagent) output.
    """
    try:
        with open(transcript_path, encoding="utf-8") as fh:
            entries = [json.loads(ln) for ln in fh if ln.strip()]
    except (OSError, json.JSONDecodeError, ValueError):
        return ""

    chunks: list[str] = []
    for entry in reversed(entries):
        if _is_real_user_message(entry):
            break
        if entry.get("type") != "assistant" or entry.get("isSidechain"):
            continue
        content = (entry.get("message") or {}).get("content") or []
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                chunks.append(block.get("text", ""))

    return chr(10).join(reversed(chunks))


def broken_file_links(text: str) -> list[str]:
    """Solution-file (`.py`) link targets in `text` that do NOT resolve from the repo root.

    The chat renderer resolves a relative link against the WORKSPACE ROOT, which is
    REPO_ROOT here. A `.py` target that does not exist when joined to REPO_ROOT is a dead
    link — the Aug 27, 2026 failure, where `../../../dsa/...` (correct inside a schedule
    file) climbed out of the repo and clicked nowhere.

    Deliberately scoped to `.py` targets — the problem-link rule's own domain — so ordinary
    doc/URL links are never second-guessed. URLs and absolute paths are skipped; a `#Lnn`
    line anchor is stripped before the check. Returns the offending targets, in order.
    """
    broken: list[str] = []
    for target in MD_LINK_TARGET.findall(text):
        target = target.strip()
        if "://" in target or target.startswith(("#", "mailto:")):
            continue  # a URL or an in-page anchor, not a repo file
        path = target.split("#", 1)[0].strip()  # drop a #Lnn line anchor
        if not path.endswith(".py"):
            continue
        if Path(path).is_absolute():
            continue  # an absolute path is the author's call, not a chat-relative link
        if not (REPO_ROOT / path).resolve().exists():
            broken.append(target)
    return broken


BROKEN_MESSAGE = (
    "DEAD LINK — this turn links solution file(s) whose path does NOT resolve from the "
    "repo root: {paths}\n"
    "The chat renderer resolves a relative link against the WORKSPACE ROOT (the repo "
    "root), so a `../../../dsa/...` path copied from a schedule row (correct THERE, three "
    "folders deep) clicks nowhere here. Re-emit ONLY the fixed link line(s), one each, with "
    "a REPO-ROOT-RELATIVE path (e.g. `dsa/leetcode/stack/853_car_fleet.py`). The cleanest "
    "way to get it right: run `python scripts/links.py <number> ...` and paste its output — "
    "it reads the path from disk so it cannot be wrong.\n"
    "Rule: .claude/memory/feedback_lineup_links_only.md"
)


# ── Spoiler-column detector ─────────────────────────────────────────────────────
# A presented lineup is problem NAME + LINKS and nothing else — build it from
# `scripts/links.py`, which emits PLAIN LINES, not a table. So a markdown TABLE that
# wraps a scaffold `.py` link and adds a SEMANTIC column (a Note/Focus/technique/comfort/
# units column, a comfort emoji, a technique parenthetical in the title) is a spoiler: it
# pre-localizes the technique or the exact miss to watch and defeats the recognition
# front-gate. This lapsed as prose 3+ times — Sep 3 (a "Focus" column), Sep 4 (a Note
# column + technique-in-title), Sep 11 (a "What it is" column) — so it is a hook, per the
# intervention ladder. See feedback_lineup_links_only.md.
#
# EXEMPT: a bare numeric index column (`| 138 | [138 Copy…](…) |` or a running `1, 2, 3`).
# It merely echoes the problem number already visible in the link text — it localizes
# nothing the lineup doesn't already show, so it is NOT a spoiler. (Learner, Sep 12, 2026:
# "the index column is fine.")

# A markdown link, capturing (visible text, target).
MD_LINK_FULL = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")

# Comfort ratings and schedule tags — a comfort/tag column has no place in a lineup.
LINEUP_EMOJI = re.compile(r"🟢|🟡|🔴|🎓|🆕|🎯|🎤|🔥|⚙️|🔤")

# A technique parenthetical inside a link title, e.g. `(Monotonic Deque)`,
# `(Floyd-Warshall)`. `links.py` output never carries one.
TITLE_PARENTHETICAL = re.compile(r"\([A-Z][^)]*\)")


def _is_index_cell(cell: str) -> bool:
    """True for a bare numeric index column — `138`, `1`, `1.` — which only echoes the
    problem number already shown in the link text. Not a spoiler, so it is exempt from the
    extra-column signal below. (Learner's call, Sep 12, 2026.)"""
    return cell.rstrip(".").strip().isdigit()


def _is_scaffold_py_link(target: str) -> bool:
    """True for a solution-file link like `dsa/leetcode/stack/239_...py` — the signature
    of an ACTIONABLE lineup. Rating, coverage and schedule-explanation tables carry LC
    URLs or bare numbers, never a scaffold `.py`, so keying on this keeps the detector
    from crying wolf on tables that are legitimately allowed to have columns."""
    t = target.split("#", 1)[0].strip()
    return t.endswith(".py") and "dsa/" in t and "://" not in t


def spoiler_lineup(text: str) -> "list[str]":
    """Signals that a presented lineup/board TABLE carries more than name + links.

    Fires only on a table ROW that itself holds a `dsa/….py` scaffold link, so a
    rating-rationale / coverage / schedule table (no scaffold links) never trips it.
    Returns the human-readable signals found (empty = clean).
    """
    signals: "list[str]" = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        links = MD_LINK_FULL.findall(line)
        py_links = [(vis, tgt) for vis, tgt in links if _is_scaffold_py_link(tgt)]
        if not py_links:
            continue  # not a lineup row — a table may legitimately have columns here

        cells = [c.strip() for c in line.strip("|").split("|")]
        pair_cells = [
            c for c in cells
            if any(_is_scaffold_py_link(t) for _, t in MD_LINK_FULL.findall(c))
        ]
        # A cell that is neither the problem pair, a pure `---`/`:` separator, nor a bare
        # numeric index is an extra column — the primary signal, since the correct lineup
        # is not a table. A numeric index echoes the link's own number and is exempt.
        others = [
            c for c in cells
            if c and c not in pair_cells and (set(c) - set("-:")) and not _is_index_cell(c)
        ]
        if len(cells) > 1 and others:
            preview = ", ".join(repr(c[:24]) for c in others[:3])
            signals.append(f"an extra column beside the problem ({preview})")
        if LINEUP_EMOJI.search(line):
            signals.append("a comfort/tag emoji column")
        for vis, _ in py_links:
            if TITLE_PARENTHETICAL.search(vis):
                signals.append(f"a technique parenthetical in the title ({vis.strip()})")
        if signals:
            break  # one offending row is enough

    seen: "set[str]" = set()
    out: "list[str]" = []
    for s in signals:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


SPOILER_MESSAGE = (
    "SPOILER COLUMN — this turn presents a lineup/board as a TABLE carrying more than the "
    "problem name + links: {signals}.\n"
    "A presented lineup is name + links ONLY. Any SEMANTIC column — Note/Focus/"
    "technique/comfort/units/difficulty, a comfort emoji, or a technique parenthetical in "
    "the title — hands the learner the recognition call before they make it, which is the "
    "one thing the recognition front-gate exists to measure. (A bare numeric index column "
    "is fine — it only echoes the number already in the link.)\n"
    "Re-emit the lineup as name + links ONLY, one problem per line, built from "
    "`python scripts/links.py <n> ...` VERBATIM — no table, no extra cells. Comfort and "
    "units belong in the schedule file, never the lineup shown to the learner. A "
    "recognition probe OR the DSA-mock base problem carries its LOCAL FILE LINK ONLY — [<n> <title>](dsa/probes/<file>.py) "
    "— and NEVER an LC/NC link (the problem page's tags/editorial spoil the technique call).\n"
    "Rule: .claude/memory/feedback_lineup_links_only.md"
)


# ── Advance-prompt-tail detector ─────────────────────────────────────────────────
# When a point resolves, the turn ENDS at the answer — the learner sets the tempo
# (SKILL.md principle 3; decisions.yml `pace-flat-discipline`; feedback_let_learner_pace).
# A trailing imperative or nudge toward the NEXT rep — "Code it.", "ready for the next
# one?", "on to 271", "shall we move on?" — drives a progression the learner already
# owns. This lapsed as PROSE 4+ times (2026-08-20 ×2, 09-01, 09-03, 09-04, 09-09), which
# is the intervention ladder's threshold to leave the prose rung, so it becomes a hook.
#
# Deliberately narrow, like every detector here: it inspects only the turn's FINAL
# sentence and only when that sentence is SHORT (a tacked-on tail, not a substantive
# close). So "once you code it up, the amortized O(1) shows" — a long final sentence
# mid-teach — and a genuine question the rep itself raised are untouched, and the
# REQUIRED gate prompts (complexity / recognition) never match the advance vocabulary.
# A false positive trains the agent to skim past the hook, the one cost a hook can't pay.

# Short advance nudges that ARE the whole tail (matched against the cleaned final
# sentence exactly). Bare "next"/"ready" are deliberately EXCLUDED — too ambiguous, and
# "whenever you're ready" is the blessed learner-paced close, which must stay silent.
ADVANCE_EXACT = {
    "go", "go ahead", "go for it", "let's go", "lets go", "onward",
    "next one", "next up",
}

# Nudges recognizable wherever they sit inside a short final sentence.
ADVANCE_PHRASE = re.compile(
    r"(?:"
    r"\bcod(?:e|ing)\s+(?:it|this|that)(?:\s+up)?"   # "code it up", "try coding it"; \b keeps "decode it" out
    r"|ready\s+for\s+(?:the\s+|another\b|a\s+)?(?:next|one)"
    r"|ready\s+to\s+move\s+on"
    r"|(?:shall|should)\s+we\s+move\s+on"
    r"|let'?s\s+move\s+on"
    r"|let'?s\s+(?:do|tackle|start|try)\s+(?:the\s+)?next"
    r"|move\s+on\s+to\s+(?:the\s+)?next"
    r"|on\s+to\s+(?:the\s+)?(?:next|\d{1,4})"
    r"|go\s+ahead\s+and\s+\w+"                                  # "go ahead and write the code"
    r"|(?:now\s+)?write\s+(?:the\s+|your\s+)?(?:code|solution)"   # "write the code", "now write your solution"
    r")",
    re.IGNORECASE,
)

# A tail is a SHORT final sentence. Longer than this is a substantive close, not a nudge.
ADVANCE_TAIL_MAX_WORDS = 7


def _final_sentence(text: str) -> str:
    """The turn's last sentence, cleaned of markdown, for tail inspection.

    Takes the last non-empty line, strips a leading list/quote/heading marker and
    surrounding emphasis, then returns the final sentence within it.
    """
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    if not lines:
        return ""
    last = lines[-1]
    last = re.sub(r"^[>\-*\d.)#\s]+", "", last)          # leading list/quote/heading markers
    last = last.replace("*", "").replace("`", "").strip()  # emphasis / code ticks
    parts = [p.strip() for p in re.split(r"[.!?]+", last) if p.strip()]
    return parts[-1] if parts else ""


def advance_prompt_tail(text: str) -> str:
    """The advance-prompt tail ending this turn, or "" when it ends cleanly.

    Returns the offending fragment so the block message can quote it back.
    """
    tail = _final_sentence(text)
    norm = tail.lower().rstrip("?!.").strip()
    if not norm or len(norm.split()) > ADVANCE_TAIL_MAX_WORDS:
        return ""                                   # a substantive close, not a nudge
    if norm in ADVANCE_EXACT or ADVANCE_PHRASE.search(norm):
        return tail
    return ""


ADVANCE_MESSAGE = (
    "ADVANCE-PROMPT TAIL — this turn ends by pushing the learner to the next rep: "
    "\"{tail}\".\n"
    "The learner sets the tempo (SKILL.md principle 3). When a point resolves, END THE "
    "TURN at the answer — no \"code it\", no \"go\", no \"on to X\", no \"ready for the "
    "next one?\". Silence is the correct close; the learner drives every transition.\n"
    "Re-emit the turn WITHOUT the trailing nudge — keep the substance, drop the last "
    "sentence that pushes pace. (A genuine question the rep itself raised is fine; this "
    "fires only on a short tail that advances the learner.)\n"
    "Rule: .claude/memory/feedback_let_learner_pace.md"
)


# ── Banned-opener detector ───────────────────────────────────────────────────────
# The mirror of advance_prompt_tail at the OTHER end of the turn: a turn that corrects
# something starts with the correction, not with a throat-clearing interjection. The
# learner banned these Aug 15, 2026 (*"starting a sentence with careful really doesn't
# add any value ... just get to the meat"*) and again Sep 19, 2026, explicitly pairing
# it with the advance-tail hook (*"remove the prefixing statements that don't add value
# like how we removed the ending statements"*). Prose has now lapsed >=2x, which is the
# intervention ladder's threshold to leave the prose rung, so it becomes a hook.
#
# Deliberately narrow, like every detector here (a false positive trains the agent to
# skim past the hook). The TELL is the em-dash dangle: a banned interjection immediately
# followed by an em-dash / en-dash / "--" (`Careful -`, `Fair -`, `Right -`), plus the
# "Right, so" comma continuation and a few fixed throat-clears that cannot be a real
# sentence start (`So:`, `Worth noting`, `Here's the thing`, `Good question, but`). A
# bare `So the invariant holds ...` or `Good catch on the boundary.` has no dangle and
# stays clean. Checked at the start of the message AND of every paragraph (the learner's
# chosen scope Sep 19), because an opener buried mid-turn is the same throat-clear.
OPENER_RE = re.compile(
    r"^(?:"
    r"(?:careful|no|fair|right|good|ah|well|so|two\s+things|one\s+thing)\s*(?:[—–]|--)"
    r"|(?:right|good|well|ah|no)\s*,\s*so\b"
    r"|so\s*:"
    r"|worth\s+noting\b"
    r"|here'?s\s+the\s+thing\b"
    r"|good\s+question,?\s+but\b"
    r")",
    re.IGNORECASE,
)


def banned_opener(text: str) -> "list[str]":
    """Throat-clearing interjections opening the message or any paragraph, or [].

    Returns the offending fragments so the block message can quote them back. Skips
    fenced code, blockquotes (may quote the learner) and table rows.
    """
    found: "list[str]" = []
    in_fence = False
    prev_blank = True  # start of text is a paragraph boundary
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            prev_blank = False
            continue
        if in_fence:
            prev_blank = False
            continue
        if not stripped:
            prev_blank = True
            continue
        if prev_blank and not (stripped.startswith(">") or stripped.startswith("|")):
            cleaned = re.sub(r"^[>\-*\d.)#\s]+", "", stripped)         # list/quote/heading markers
            cleaned = cleaned.replace("*", "").replace("`", "").lstrip()  # emphasis / code ticks
            m = OPENER_RE.match(cleaned)
            if m:
                found.append(m.group(0).strip())
        prev_blank = False
    return found


OPENER_MESSAGE = (
    "BANNED OPENER -- this turn opens a paragraph with a throat-clearing interjection: "
    "{openers}.\n"
    "Start with the fact. These lead-ins delete with zero information loss and read as a "
    "teacher clearing their throat (feedback_explanation_register.md -> BANNED OPENERS). "
    "The test: delete the opening clause; if the sentence still stands, it should never "
    "have carried one -- \"Careful - every car has the same end position\" -> \"Every car "
    "has the same end position.\"\n"
    "Re-emit the turn with each flagged paragraph starting at the fact -- drop the "
    "interjection and the dangling dash. (A bare \"So the invariant holds ...\" with no "
    "dangle, or \"Good catch\" with no dash, is fine and never fires.)\n"
    "Rule: .claude/memory/feedback_explanation_register.md"
)


# Re-enabled 2026-08-14 after the 10th lapse got past it. It was disabled on the day it
# was written because `last_assistant_text()` read only the FINAL assistant entry, which
# is almost always a `tool_use` record with no text. The replacement above gathers the
# whole turn. Note the disable-note's own proposed fix ("back to the last `user` entry")
# would still have been wrong: `tool_result` records are typed `user` and sit INSIDE a
# turn, so that boundary truncates mid-turn. The boundary is the last *human* message.
#
# The original unit tests passed on a hand-built transcript with one text entry per
# message — they exercised the regex, never the transcript SHAPE. Tests now run against
# a real `.jsonl` from this project (see `_selftest` below).


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return  # Malformed input is not this hook's problem — stay silent.

    # Never block twice on one turn: the second pass is the corrected reply.
    if payload.get("stop_hook_active"):
        return

    text = last_turn_text(payload.get("transcript_path", ""))
    if not text:
        return

    # A present-but-dead file link passes the "is it linked" test but clicks nowhere.
    # Checked first: it needs no cue word — a broken path is broken whatever the turn is
    # about.
    broken = broken_file_links(text)
    if broken:
        json.dump(
            {"decision": "block", "reason": BROKEN_MESSAGE.format(paths=", ".join(broken))},
            sys.stdout,
        )
        return

    # A presented lineup carrying more than name + links spoils the recognition gate.
    # Board-independent: the scaffold-`.py`-link signature already scopes it to a lineup.
    spoiler = spoiler_lineup(text)
    if spoiler:
        json.dump(
            {"decision": "block", "reason": SPOILER_MESSAGE.format(signals="; ".join(spoiler))},
            sys.stdout,
        )
        return

    # A turn that resolves and then pushes to the next rep drives pace the learner owns.
    # Board-independent: it reads only the turn's own final sentence.
    tail = advance_prompt_tail(text)
    if tail:
        json.dump(
            {"decision": "block", "reason": ADVANCE_MESSAGE.format(tail=tail)},
            sys.stdout,
        )
        return

    # A turn that opens with a throat-clearing interjection buries the fact behind a
    # deletable lead-in. It reads only the turn's own paragraph starts.
    openers = banned_opener(text)
    if openers:
        json.dump(
            {"decision": "block", "reason": OPENER_MESSAGE.format(openers=", ".join(f'"{o}"' for o in openers))},
            sys.stdout,
        )


# ── Self-test ─────────────────────────────────────────────────────────────────
# `python .claude/hooks/problem_link_reminder.py --selftest`
#
# Two halves, and the SECOND is the one that matters. The Aug 12 version of this hook
# passed its tests and was still broken, because those tests fed a hand-built transcript
# with one text entry per message. Real transcripts split a turn across many assistant
# entries and interleave `tool_result` records typed `user`. So: point `--selftest` at a
# real `.jsonl` to exercise `last_turn_text` against the true shape.
# Path-resolution cases for broken_file_links. The passing paths must be REAL files in
# this repo so the check exercises the true filesystem, not a mock.
BROKEN_CASES = [
    # (name, text, should_flag)
    ("repo-root-relative -> ok",
     "[853 Car Fleet](dsa/leetcode/stack/853_car_fleet.py)", False),
    ("schedule-relative -> dead",
     "[853 Car Fleet](../../../dsa/leetcode/stack/853_car_fleet.py)", True),
    ("line anchor kept, path ok",
     "[853](dsa/leetcode/stack/853_car_fleet.py#L12)", False),
    ("nonexistent file -> dead",
     "[999 Nope](dsa/leetcode/stack/999_does_not_exist.py)", True),
    ("URL is not a file link",
     "[LC](https://leetcode.com/problems/car-fleet/)", False),
    ("non-.py relative link ignored",
     "[setup](docs/SETUP.md)", False),
]


# Spoiler-column cases for spoiler_lineup. A lineup is name + links ONLY; a table
# wrapping a scaffold `.py` link with anything else is the failure.
SPOILER_CASES = [
    # (name, text, should_flag)
    ("4-column lineup table -> block",
     "| # | Problem | Mode | What it is |\n|---|---|---|---|\n"
     "| 1 | [239 Sliding Window Maximum](dsa/leetcode/stack/239_sliding_window_maximum.py) · "
     "[LC](https://leetcode.com/problems/sliding-window-maximum/) | retry | monotonic-deque blocker |",
     True),
    ("comfort-emoji column -> block",
     "| [846 Hand of Straights](dsa/leetcode/greedy/846_hand_of_straights.py) · "
     "[LC](https://leetcode.com/problems/hand-of-straights/) | 🆕 |",
     True),
    ("technique parenthetical in title -> block",
     "| [239 Sliding Window Maximum (Monotonic Deque)](dsa/leetcode/stack/239_sliding_window_maximum.py) · "
     "[LC](https://leetcode.com/problems/sliding-window-maximum/) |",
     True),
    ("mock-tag emoji beside a scaffold link -> block",
     "| 🎤 [131 Palindrome Partitioning](dsa/probes/131_palindrome_partitioning.py) |",
     True),
    ("plain mock line, no scaffold link -> ok",
     "| 🎤 Mock interview (Medium) | 🎤 |  |  | Mock |",
     False),
    ("clean plain lines -> ok",
     "[239 Sliding Window Maximum](dsa/leetcode/stack/239_sliding_window_maximum.py) · "
     "[LC](https://leetcode.com/problems/sliding-window-maximum/)\n"
     "[846 Hand of Straights](dsa/leetcode/greedy/846_hand_of_straights.py) · "
     "[LC](https://leetcode.com/problems/hand-of-straights/)",
     False),
    ("single-column pair table -> ok",
     "| Today |\n|---|\n| [846 Hand of Straights](dsa/leetcode/greedy/846_hand_of_straights.py) · "
     "[LC](https://leetcode.com/problems/hand-of-straights/) |",
     False),
    ("bare numeric index column -> ok (learner's call Sep 12)",
     "| # | Problem |\n|---|---|\n"
     "| 138 | [138 Copy List with Random Pointer](dsa/leetcode/linked_list/138_copy_list_with_random_pointer.py) · "
     "[LC](https://leetcode.com/problems/copy-list-with-random-pointer/) |\n"
     "| 167 | [167 Two Sum II](dsa/leetcode/two_pointers/167_two_sum_2.py) · "
     "[LC](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) |",
     False),
    ("rating table, no scaffold link -> ok",
     "| Axis | Verdict |\n|---|---|\n| recognition | clean |\n| complexity | O(n)/O(1) |",
     False),
    ("coverage table, LC links only -> ok",
     "| Technique | Problems |\n|---|---|\n| Monotonic Stack | "
     "[496](https://leetcode.com/problems/next-greater-element-i/), "
     "[901](https://leetcode.com/problems/online-stock-span/) |",
     False),
]


# Advance-prompt-tail cases for advance_prompt_tail. The turn ENDS at the answer; a
# short trailing nudge to the next rep is the failure. The required gate prompts and a
# genuine rep question must stay clean.
ADVANCE_CASES = [
    # (name, text, should_flag)
    ("bare 'Code it.'", "The invariant holds at each pop. Code it.", True),
    ("'code it up' tail", "That's the monotonic-deque direction settled.\nNow code it up.", True),
    ("ready for the next one", "Deque direction is settled. Ready for the next one?", True),
    ("on to a number", "Nice — that closes 239. On to 271.", True),
    ("shall we move on", "The recognition call is right. Shall we move on?", True),
    ("bare go", "Looks right.\nGo.", True),
    ("let's do the next", "Complexity checks out. Let's do the next problem.", True),
    ("go ahead and write the code", "That settles the pruning bound. Go ahead and write the code.", True),
    ("bare write the code", "The call is right.\nWrite the code.", True),
    # Negatives — must stay silent.
    ("ends on the answer", "The amortized cost is O(n) because each index is pushed and popped once.", False),
    ("complexity gate prompt", "What's the time and space complexity — each with a why?", False),
    ("recognition gate prompt", "What shape do you see, and what technique does it pick?", False),
    ("code-it inside a long close",
     "Once you code it up the two-pointer walk makes the O(n) bound obvious.", False),
    ("write-the-code inside a long close",
     "When you write the code, the base case is the empty remainder, not the full string.", False),
    ("whenever you're ready (blessed close)", "That settles the invariant. Whenever you're ready.", False),
    ("genuine rep question", "Does the deque hold indices or values in your version?", False),
    ("make sense check", "So the window never shrinks past the max. Make sense?", False),
]


# Banned-opener cases for banned_opener. A turn STARTS at the fact; a throat-clearing
# interjection with an em-dash dangle (or a fixed throat-clear) is the failure. Bare
# sentence-initial "So"/"Good" with no dangle, and legitimate em-dashes mid-sentence,
# must stay silent.
OPENER_CASES = [
    # (name, text, should_flag)
    ("Careful - dangle", "Careful — every car has the same end position.", True),
    ("Fair - dangle", "Fair — the O(n) version drops the rescan.", True),
    ("Right, so", "Right, so the deque holds indices, not values.", True),
    ("mid-turn paragraph opener",
     "The invariant holds at each pop.\n\nRight — that also settles the boundary case.", True),
    ("So: throat-clear", "So: the amortized cost is O(n).", True),
    ("Worth noting", "Worth noting the empty-array case returns 0.", True),
    ("double-hyphen dangle", "No -- the heap holds at most k entries.", True),
    ("bold-wrapped opener", "**Careful** — the base case is off by one.", True),
    # Negatives -- must stay silent.
    ("bare So, no dangle", "So the invariant holds because each index is pushed once.", False),
    ("Good catch, no dash", "Good catch on the boundary condition.", False),
    ("em-dash mid-sentence", "The deque is monotonic — that is what makes it O(n).", False),
    ("no leading interjection", "Every car has the same end position, so they merge.", False),
    ("code fence with # So", "```python\n# So this is fine inside code\nx = 1\n```", False),
    ("blockquote learner text", "> Careful — I think the deque is wrong here.", False),
    ("number-so is not comma-so", "Right now the deque is empty, so we push.", False),
]


def _selftest(transcript: str | None = None) -> int:
    failures = 0
    broken_failures = 0
    for name, text, expected in BROKEN_CASES:
        got = bool(broken_file_links(text))
        if got != expected:
            broken_failures += 1
            print(f"FAIL  {name}: flag={got}, expected {expected} -> "
                  f"{broken_file_links(text)}")
    failures += broken_failures
    print(f"broken:   {len(BROKEN_CASES) - broken_failures}/{len(BROKEN_CASES)} passed")

    spoiler_failures = 0
    for name, text, expected in SPOILER_CASES:
        got = bool(spoiler_lineup(text))
        if got != expected:
            spoiler_failures += 1
            print(f"FAIL  {name}: flag={got}, expected {expected} -> {spoiler_lineup(text)}")
    failures += spoiler_failures
    print(f"spoiler:  {len(SPOILER_CASES) - spoiler_failures}/{len(SPOILER_CASES)} passed")

    advance_failures = 0
    for name, text, expected in ADVANCE_CASES:
        got = bool(advance_prompt_tail(text))
        if got != expected:
            advance_failures += 1
            print(f"FAIL  {name}: flag={got}, expected {expected} -> "
                  f"{advance_prompt_tail(text)!r}")
    failures += advance_failures
    print(f"advance:  {len(ADVANCE_CASES) - advance_failures}/{len(ADVANCE_CASES)} passed")

    opener_failures = 0
    for name, text, expected in OPENER_CASES:
        got = bool(banned_opener(text))
        if got != expected:
            opener_failures += 1
            print(f"FAIL  {name}: flag={got}, expected {expected} -> "
                  f"{banned_opener(text)!r}")
    failures += opener_failures
    print(f"opener:   {len(OPENER_CASES) - opener_failures}/{len(OPENER_CASES)} passed")

    if transcript:
        text = last_turn_text(transcript)
        if not text.strip():
            failures += 1
            print("FAIL  last_turn_text returned nothing from a real transcript "
                  "-- this is the Aug 12 defect, do NOT ship")
        else:
            print(f"transcript: recovered {len(text)} chars of assistant text")
    else:
        print("transcript: SKIPPED -- pass a real .jsonl path to exercise the shape")
    return 1 if failures else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        args = [a for a in sys.argv[1:] if a != "--selftest"]
        sys.exit(_selftest(args[0] if args else None))
    main()
