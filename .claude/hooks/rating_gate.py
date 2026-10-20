"""Stop hook: block a turn that PROPOSES a comfort rating before the learner has
stated BOTH time and space complexity themselves.

The complexity gate (CLAUDE.md LeetCode Review Workflow step 1; `feedback_ask_complexity`)
requires the learner to volunteer **time AND space, each with a why-clause, BEFORE any
rating is proposed**. It kept being run backwards — the rating proposed first, the gate
treated as a formality:
  - 2026-08-22 (15): rating proposed, then the freebie ledger checked.
  - 2026-08-23 (127): 🟡 proposed with SPACE given but TIME never stated — and the coach
    then recited the time bound itself. Learner: *"i didn't do the time yet, we shouldn't
    be rushing towards the rating."*

Both are the same defect: the rating is the destination and the gate a box to tick on the
way. A memory-file note is the weakest fix (prose the agent must remember to obey). This
hook binds the check to the exact moment it fails — the rating proposal — so it cannot be
skipped. Learner's call, 2026-08-23: *"put a clear gate at the rating where it requires
code completion + time and space complexities given."*

Mechanism (mirror of `problem_link_reminder.py`): at Stop, read the assistant's last turn;
if it PROPOSES a rating, scan the learner's recent messages for a time signal AND a space
signal. Missing either → block once (`stop_hook_active` guards against a loop), naming what
is missing, so the gate is completed before the rating stands.

Deliberately conservative, for the same reason the link hook is — a hook that cries wolf
gets skimmed past:
  - it fires only when BOTH a comfort marker AND a proposal cue are present, so ordinary
    talk *about* ratings (explaining the scale, citing a past rating) does not trip it;
  - it checks the LEARNER's transcript, not a self-asserted checklist the agent could write
    falsely — the ungameable form;
  - code-completion is implicit: a rating on a `pass` stub can't arise, there's nothing to
    read, so the gate that matters is the complexity one;
  - a single block only. If both axes really were given without the literal words (rare —
    "O(n) then O(1)"), the re-send passes. One nudge, never a wall.

NOT in scope: whether the stated complexity is CORRECT. That's judgement (the coach's job).
The rating itself ignores complexity entirely — a miss is corrected, carded in
complexity_gotchas.md, and queued for the end-of-week cleanup, never a rating input; that
scoring rule lives in `feedback_ask_complexity`. This hook enforces only that both axes were
ASKED FOR and given before the rating — the mechanizable half.
"""
import json
import re
import sys

# ── Rating-proposal detection ───────────────────────────────────────────────────
# A comfort verdict: a comfort glyph, or the word rating / comfort.
# The bare words clean/shaky/blank and s0-s2 do not count: a non-coaching turn (an engineer
# spawn report: "build clean", "the s1 fallback") once blocked as a rating proposal, with no
# rating and no problem under review. Those words appear in ordinary prose; a real proposal
# always carries a glyph or says rating/comfort.
COMFORT = re.compile(r"🟢|🟡|🔴|🎓|\b(?:rating|comfort)\b", re.IGNORECASE)
# A cue that the turn is PROPOSING a rating — i.e. asking the learner to DECIDE, which is the
# defining feature of a proposal (workflow step 4: "propose it for confirmation"). A recap only
# REPORTS already-logged ratings and asks for nothing.
#
# ⚠️ Do NOT match a bare next-review date ("→ Sep 2", "Oct 22"): a session recap lists exactly
# those alongside the comfort emoji ("567 🟢 s2 · Oct 22"), so date-matching false-fired on the
# Aug 23 close-out recap. The decision-request cue is the clean discriminator — a recap has none.
#
# Do NOT match a bare "rate": it is also the ordinary noun for a frequency ("row-creation
# rate", "hit rate", "pass rate"), and on Aug 28, 2026 that blocked a turn that proposed
# NOTHING -- a factual answer about the probe tally, rendering six past results as a table of
# comfort glyphs. A RECORD of past results and a PROPOSAL about a current one are lexically
# identical except for the decision request, so only decision-request forms of the verb count.
PROPOSE_CUE = re.compile(
    r"\bconfirm\b|\bproposed?\b|\boverride\b|\baccept\b|\brating[:?]"
    r"|\brate\s+(?:it|this|that|the\s+rep)\b|\brate\?",
    re.IGNORECASE,
)

# A meta / self-eval / log summary QUOTES comfort glyphs as records, not as a live verdict.
# A meta-review + completion summary once tripped this hook: it quoted self_eval_log
# lines full of 🟢/🟡/🔴 next to words like "override"/"proposed" that describe PAST logged
# ratings, not a rating being proposed now. Same class as the recap and 'rate'-as-frequency
# exemptions above — a RECORD is not a PROPOSAL. These markers do not occur in an ordinary
# rep turn, so exempting them opens only a narrow, documented hole (a real rating buried in
# a meta turn blocks-once at worst if this ever fires).
SUMMARY_CONTEXT = re.compile(
    r"meta[-_ ]review|self[-_ ]eval|self_eval_log|self_eval_archive"
    r"|intervention ladder|consolidated\s*(?:→|->)|decisions\.yml",
    re.IGNORECASE,
)

# A DASHBOARD / DEPLOY report renders comfort glyphs and words like "clean" as DATA, not as a
# verdict on a rep. The gamification feature (scripts/gamify.py -> progress.json, the
# progressiveoverflow.com dashboard) means routine status/deploy reports carry 🟢/🎓 and
# "streak" (the dashboard's own vocabulary) alongside incidental cue words ("build clean",
# "accept the fallback"), which once tripped this gate on a pure software-deploy turn — no
# rep in sight.
#
# The discriminators here are terms that CANNOT occur in a real rep-rating proposal: a comfort
# verdict for a LeetCode rep never mentions progress.json, the dashboard, a deploy, or the site.
# ⚠️ Deliberately NOT keyed on streak / pipeline / badge / trophy alone — those DO appear in a
# genuine rating turn ("🟢 s2 → streak 3 → graduates"), so exempting them would open a real hole.
#
# Scoped to the PARAGRAPH, not the whole turn: `proposes_rating` splits the turn on blank
# lines and tests only the paragraphs that do NOT match REPORT_CONTEXT. Matching the whole
# turn was itself a defect — a turn that mentions a deploy AND, in a separate paragraph,
# genuinely proposes a rating ("Shipped the dashboard... \n\n Time O(n)... space O(1) — 🟢
# proposed. Confirm?") let the real proposal slip past ungated. SUMMARY_CONTEXT stays
# turn-wide below: a meta/self-eval summary quotes glyphs as records throughout, so no
# paragraph of it is a live proposal either.
REPORT_CONTEXT = re.compile(
    r"progress\.json|progress\.schema|progressiveoverflow|\bdashboard\b|\bgamif\w*"
    r"|raw\.githubusercontent|contents/progress|refresh button|github pages"
    r"|\bdeploy(?:ed|ment|s)?\b|pages? deploy",
    re.IGNORECASE,
)

# ── Complexity signals in the LEARNER's messages ────────────────────────────────
BIG_O = re.compile(r"O\s*\(", re.IGNORECASE)
TIME_SIGNAL = re.compile(
    r"\btime\b|\bamortiz\w*|\bruntime\b|\bper[- ]call\b|\bO\([^)]*\)\s*(?:time|per)",
    re.IGNORECASE,
)
SPACE_SIGNAL = re.compile(
    r"\bspace\b|\bmemory\b|\bin[- ]?place\b|\bauxiliary\b|\bfootprint\b|\bextra\s+(?:space|storage)\b",
    re.IGNORECASE,
)

LOOKBACK_TURNS = 8  # a rep's discussion spans several turns; scan the learner's recent ones.


def _is_real_user_message(entry: dict) -> bool:
    """True for a human turn, False for a tool_result carrier (typed 'user', mid-turn)."""
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


def _entries(transcript_path: str) -> "list[dict]":
    try:
        with open(transcript_path, encoding="utf-8") as fh:
            return [json.loads(ln) for ln in fh if ln.strip()]
    except (OSError, json.JSONDecodeError, ValueError):
        return []


def last_turn_text(entries: "list[dict]") -> str:
    """All assistant `text` since the last real user message (one turn, many entries)."""
    chunks: list[str] = []
    for entry in reversed(entries):
        if _is_real_user_message(entry):
            break
        if entry.get("type") != "assistant" or entry.get("isSidechain"):
            continue
        content = (entry.get("message") or {}).get("content") or []
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    chunks.append(block.get("text", ""))
    return "\n".join(reversed(chunks))


def learner_text(entries: "list[dict]", turns: int = LOOKBACK_TURNS) -> str:
    """Concatenated text of the last `turns` real user messages."""
    chunks: list[str] = []
    seen = 0
    for entry in reversed(entries):
        if not _is_real_user_message(entry):
            continue
        seen += 1
        if seen > turns:
            break
        content = (entry.get("message") or {}).get("content")
        if isinstance(content, str):
            chunks.append(content)
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    chunks.append(block.get("text", ""))
    return "\n".join(reversed(chunks))


def rating_signals(turn: str) -> "tuple[str, str] | None":
    """(comfort token, proposal cue) that make `turn` a rating proposal, or None."""
    if SUMMARY_CONTEXT.search(turn):
        return None  # a log / meta-review summary records ratings, it does not propose one
    paragraphs = re.split(r"\n\s*\n", turn)
    non_report = [p for p in paragraphs if not REPORT_CONTEXT.search(p)]
    remainder = "\n\n".join(non_report)  # dashboard/deploy paragraphs dropped, rest kept
    comfort = COMFORT.search(remainder)
    cue = PROPOSE_CUE.search(remainder)
    if comfort and cue:
        return comfort.group(0), cue.group(0)
    return None


def proposes_rating(turn: str) -> bool:
    return rating_signals(turn) is not None


def missing_axes(learner: str) -> "list[str]":
    """Which complexity axes the learner has NOT evidenced. Empty = gate satisfied.

    An axis counts as given only if its keyword/proxy appears. NO Big-O-count credit:
    the tempting "two O() expressions => both axes given" heuristic misfires on exactly
    the case this hook exists for -- the 127 rep gave `O(V)` and `O(V+E)`, *both space*,
    with time never stated; a count rule reads two O()s and wrongly credits time.

    There is no textual way to tell which axis a bare `O(...)` names, so the only robust
    rule is the axis word. The gate already requires a why-clause per axis, and a real
    why-clause names the axis ("O(1) space, one fixed array") -- so in practice both words
    appear. The accepted cost is the rare abbreviated answer ("O(n) time, then O(1)") where
    space is unworded: it blocks ONCE, and the re-send passes (stop_hook_active).
    """
    missing = []
    if not TIME_SIGNAL.search(learner):
        missing.append("TIME")
    if not SPACE_SIGNAL.search(learner):
        missing.append("SPACE")
    return missing


MESSAGE = (
    "RATING GATE — this turn proposes a comfort rating, but the learner has not stated "
    "{missing} complexity in their recent messages.\n"
    "The complexity gate is BOTH axes, each with a why-clause, stated by the LEARNER, "
    "BEFORE any rating (CLAUDE.md LeetCode Review Workflow step 1; feedback_ask_complexity). "
    "It was run backwards on 15 (Aug 22) and 127 (Aug 23) — rating first, gate as a "
    "formality.\n"
    "DO NOT rate yet. Ask the learner for {missing} (each itemized), wait for their answer, "
    "and — if a bound is a miss — correct it and card it in complexity_gotchas.md. The miss "
    "never changes the rating; only then propose it, on recognition + code.\n"
    "If the learner genuinely already stated both axes above (just without the words "
    '"time"/"space"), re-send — this blocks once.\n'
    "Matched: comfort token {comfort!r}, proposal cue {cue!r}.\n"
    "Rule: .claude/memory/feedback_ask_complexity.md"
)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return
    if payload.get("stop_hook_active"):
        return  # never block twice — the re-send passes.

    entries = _entries(payload.get("transcript_path", ""))
    if not entries:
        return
    turn = last_turn_text(entries)
    signals = rating_signals(turn) if turn else None
    if not signals:
        return

    missing = missing_axes(learner_text(entries))
    if not missing:
        return

    comfort, cue = signals
    json.dump(
        {
            "decision": "block",
            "reason": MESSAGE.format(missing=" and ".join(missing), comfort=comfort, cue=cue),
        },
        sys.stdout,
    )


# ── Self-test ─────────────────────────────────────────────────────────────────
# python .claude/hooks/rating_gate.py --selftest
PROPOSE_CASES = [
    # (name, turn_text, should_be_detected_as_proposal)
    ("emoji + confirm", "That reads as 🟡 Shaky — confirm?", True),
    ("word + arrow date", "Rating: 🟢 s2 → Oct 22. Confirm?", True),
    ("blank + proposed", "Proposed: 🔴 Blank, streak resets.", True),
    ("scale explanation, no propose cue", "The scale is 🟢 clean, 🟡 shaky, 🔴 blank.", False),
    ("past rating cite, no cue", "Your last rep on this was 🟡.", False),
    ("plain prose", "Nice, the BFS looks correct and clean.", False),
    # The Aug 23 close-out recap false positive: comfort markers + next-review dates, but it
    # REPORTS logged ratings and asks for no decision. Must NOT trip.
    ("session recap, no decision request",
     "Recap: 567 🟢 s2 (Oct 22) · 901 🟢 s1 (Sep 22) · 127 🟡 (Sep 2). Pushed.", False),
    ("override-style proposal", "Proposed: 🟡 Shaky → Sep 2. Accept or override?", True),
    # The Aug 28, 2026 results-table false positive: comfort glyphs plus the word "rate" used
    # as a FREQUENCY, proposing nothing. Must NOT trip.
    ("probe tally, 'rate' as a frequency",
     "Probes: 🟢 🟢 🟡 🟢 🟢 🟢 — row-creation rate 17%, the pool still teaches.", False),
    ("rate as a decision request", "Coded from a blank page, no hints — reads 🟡. Rate it?", True),
    # A spawn-report false positive: no glyph and no rating/comfort word.
    ("non-coaching report, bare clean/s1 words",
     "Build clean, confirm the s1 fallback before the push.", False),
    # A meta-review / completion summary false positive: comfort glyphs quoted from
    # self_eval_log next to record-words ("override"/"proposed"), proposing nothing live.
    ("meta-review summary, quoted glyphs",
     "Meta-review: consolidated→ 912 recorded 🟡→🟢 override pending the next build. Confirm the commit?", False),
    ("self-eval log summary",
     "Logged to self_eval_log.md: 540 🟡 stuck_log fix, proposed as a review-workflow step.", False),
    ("decisions.yml summary with glyphs",
     "decisions.yml: 283/206 🟢→🎓 graduate override recorded; nothing to accept here.", False),
    # Gamification-deploy false positives: status/deploy reports carry the dashboard's
    # glyphs + "clean"/"accept" but propose no rating. Must NOT trip.
    ("deploy report with glyphs + cue",
     "Shipped the dashboard: 🔥 115-day streak, 19 🎓, 97 🟢. Build clean; progress.json live. Accept the fallback design?", False),
    ("dashboard fetch report",
     "The progressiveoverflow.com dashboard now fetches progress.json; 🟢/🎓 render. Confirm the push?", False),
    ("pages deploy summary",
     "Pages deploy: success. Build clean, 17 tests pass, streak 🔥 shows 🟢/🟡. Rate it?", False),
    # Control: the same glyphs + cue WITHOUT dashboard/deploy context is still a real proposal.
    ("real proposal survives the new exemption",
     "Coded from a blank page, no hints — reads 🟢 s2. Rate it?", True),
    # Paragraph scoping: a deploy-report paragraph PLUS a separate paragraph that genuinely
    # proposes a rating — the whole-turn exemption used to swallow the real proposal too.
    ("deploy paragraph + separate real proposal, paragraph-scoped",
     "Shipped the dashboard: 🔥 115-day streak, 19 🎓, 97 🟢. Build clean; progress.json live."
     "\n\n"
     "Time O(n) because one pass; space O(1) — 🟢 proposed. Confirm?", True),
]

AXES_CASES = [
    # (name, learner_text, expected_missing)
    ("both worded", "time is O(n) for the pass, space is O(1) fixed array", []),
    ("space only (the 127 case)", "visited holds O(V), adjMap is O(V+E) for space", ["TIME"]),
    ("time only", "time is O(n log n) because we sort", ["SPACE"]),
    # Accepted conservative misses: an axis stated only as a bare O() (no word) blocks
    # once, then the re-send passes. Documented, not a bug.
    ("time worded, space bare (blocks once)", "O(n) time, then O(1)", ["SPACE"]),
    ("space worded, time bare (blocks once)", "space O(n), and O(n log n)", ["TIME"]),
    ("neither — no complexity", "yeah I think that solution is done and correct", ["TIME", "SPACE"]),
    ("amortized counts as time", "amortized O(1) per call, O(n) space overall", []),
    ("memory counts as space", "runtime is O(n), memory is O(1)", []),
]


def _selftest() -> int:
    fails = 0
    for name, text, expected in PROPOSE_CASES:
        got = proposes_rating(text)
        if got != expected:
            fails += 1
            print(f"FAIL propose  {name}: got {got}, expected {expected}")
    for name, text, expected in AXES_CASES:
        got = missing_axes(text)
        if got != expected:
            fails += 1
            print(f"FAIL axes  {name}: got {got}, expected {expected}")
    total = len(PROPOSE_CASES) + len(AXES_CASES)
    print(f"rating_gate: {total - fails}/{total} passed")
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    main()
