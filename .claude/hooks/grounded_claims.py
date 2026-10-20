"""Stop hook: block a turn that STATES a repo-artifact edit as done with no tool call behind it.

The output-quality standard's groundedness rule ("If you cannot point to the tool result, it
did not happen" -- feedback_output_quality.md) has lapsed as prose:
  - Aug 3, 2026: "Added to your note" -- said before the write actually happened.
  - Aug 21, 2026 x2 [P1]: an edit reported that was never made; a schedule failure reported
    from a partial read.

Mechanism (mirror of `rating_gate.py` / `problem_link_reminder.py`): at Stop, read the
assistant's last turn -- its text AND the tool_use blocks (name + `input.command`) issued
during that same turn. A CLAIM is a sentence whose shape says "I did X" (first-person or
sentence-initial past-tense verb) about a repo artifact (file/tracker/schedule/... cue). A
claim needs EVIDENCE: `committed` needs a Bash/PowerShell command containing `git commit`;
`pushed` needs `git push`; every other verb needs a Write/Edit/MultiEdit/NotebookEdit,
an Agent/Task delegation, or a Bash/PowerShell command in the same turn -- but a
Bash/PowerShell command counts only when it is NOT read-only (a `grep`/`cat`/`git status`
read contributes nothing; a write, a script that mutates state, or an unrecognized shape
does). A claim with no matching evidence blocks once (`stop_hook_active` guards the loop),
naming the offending sentence(s).

Deliberately conservative -- this is a DSA (data structures & algorithms) coaching repo, and
the artifact-claim vocabulary collides with teaching vocabulary: `log` as in O(log n), `row`/
`table` for a DP (dynamic programming) table, `branch` in backtracking. A hook that cries wolf
on a complexity explanation trains the agent to skim past it, which costs exactly the
reliability that makes a hook stronger than prose. So:
  - a claim requires a first-person or sentence-initial verb SHAPE ("I updated ...", "Logged
    the ...") -- a passive or third-person teaching sentence ("dp[i] is updated from the
    previous row of the table", "each insert added log n work") has no such subject and never
    matches;
  - `log` alone is not an artifact cue when it is the complexity idiom (`O(log n)`, `log n`,
    `log(...)`, `log_2`, `log₂`) -- only a bare artifact `log` (a debug log, a ledger) counts;
  - every cue matches on a word boundary, so it cannot fire on part of a longer token.

Never fires on: a blockquote, fenced code, a table row, a question, future/intent phrasing
(will, going to, about to, adding now, next I'll), a negation (not yet, haven't, didn't), the
learner as the sentence's subject ("you added ..."), a bare link/citation with no verb, or
`stop_hook_active`. Stdlib only; never crashes -- any unreadable/malformed input is silence.
"""
import json
import re
import sys
from dataclasses import dataclass, field

# ── Turn-boundary parsing ────────────────────────────────────────────────────────
# Copied from problem_link_reminder.py's `_is_real_user_message` / `last_turn_text` (hooks
# are standalone files; no imports between them), extended to also collect the turn's
# tool_use block names and each input.command string.


def _message_of(entry: dict) -> dict:
    """`entry["message"]`, or {} for anything that isn't itself a dict.

    A malformed/foreign transcript line can carry `"message": "some string"` or
    `"message": null` -- a truthy non-dict still passes `or {}` unchanged, and the next
    `.get(...)` then raises AttributeError. Guarding the TYPE, not just truthiness, is
    what keeps this hook from crashing on input it doesn't recognize.
    """
    message = entry.get("message")
    return message if isinstance(message, dict) else {}


def _is_real_user_message(entry: dict) -> bool:
    """True for a human turn, False for a `tool_result` carrier (typed 'user', mid-turn)."""
    if not isinstance(entry, dict) or entry.get("type") != "user":
        return False
    content = _message_of(entry).get("content")
    if isinstance(content, str):
        return True
    if not isinstance(content, list):
        return False
    return not any(
        isinstance(block, dict) and block.get("type") == "tool_result"
        for block in content
    )


def _entries(transcript_path: object) -> "list[dict]":
    """Every JSON line of the transcript, skipping (not crashing on) a bad one.

    `transcript_path` is typed `object`, not `str`: the payload is untrusted input, and a
    non-string value (missing, null, a number) must be silence here too, not a TypeError
    from `open()`.
    """
    if not isinstance(transcript_path, str) or not transcript_path:
        return []
    try:
        with open(transcript_path, encoding="utf-8") as fh:
            raw_lines = fh.readlines()
    except (OSError, ValueError):
        # OSError: missing/unreadable path. ValueError: UnicodeDecodeError IS a ValueError
        # (a binary file, e.g. a stray non-.jsonl path, decodes as neither UTF-8 text).
        return []
    entries: "list[dict]" = []
    for line in raw_lines:
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except (json.JSONDecodeError, ValueError):
            continue  # one bad line is not this hook's problem
    return entries


@dataclass(frozen=True)
class Turn:
    """One assistant turn: its text, the tool_use names it carried, and their commands."""

    text: str
    tool_names: "frozenset[str]" = field(default_factory=frozenset)
    commands: "tuple[str, ...]" = field(default_factory=tuple)


def last_turn(transcript_path: object) -> Turn:
    """All assistant `text`/`tool_use` emitted since the last real user message.

    One turn spans MANY assistant entries -- `thinking`, `text` and `tool_use` are each their
    own record -- so this walks back to the last human message, skipping interleaved
    `tool_result` carriers and any sidechain (subagent) output, same as its siblings.
    """
    entries = _entries(transcript_path)
    text_chunks: "list[str]" = []
    tool_names: "set[str]" = set()
    commands: "list[str]" = []

    for entry in reversed(entries):
        if _is_real_user_message(entry):
            break
        if not isinstance(entry, dict) or entry.get("type") != "assistant" or entry.get("isSidechain"):
            continue
        content = _message_of(entry).get("content") or []
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            block_type = block.get("type")
            if block_type == "text":
                # `block.get("text", "")` still returns None for `{"text": null}` -- the
                # DEFAULT never fires because the key IS present, just with a null value.
                # `"\n".join(...)` on a None entry raises TypeError, so the type is checked
                # explicitly rather than trusted from the default alone.
                text = block.get("text")
                if isinstance(text, str):
                    text_chunks.append(text)
            elif block_type == "tool_use":
                name = block.get("name")
                if isinstance(name, str):
                    tool_names.add(name)
                tool_input = block.get("input")
                if isinstance(tool_input, dict):
                    command = tool_input.get("command")
                    if isinstance(command, str):
                        commands.append(command)

    return Turn(
        text="\n".join(reversed(text_chunks)),
        tool_names=frozenset(tool_names),
        commands=tuple(commands),
    )


# ── Claim detection ──────────────────────────────────────────────────────────────

VERBS = (
    "updated", "added", "appended", "logged", "wrote", "written", "edited", "scaffolded",
    "created", "moved", "deleted", "removed", "re-slotted", "restored", "regenerated",
    "marked", "struck", "recorded", "staged", "committed", "pushed",
)
_VERB_PATTERN = "|".join(re.escape(v) for v in sorted(VERBS, key=len, reverse=True))

# A real apostrophe, straight or curly -- required (never optional) wherever a contraction
# must NOT collide with an ordinary word: `we'll`/`i'll` with an optional apostrophe also
# matches "well"/"ill", two words that appear in ordinary coaching prose.
_APOS = "['’]"

# Either "I"/"I've"/"I have"/"We've"/"We have" + the verb, or the verb as the sentence's own
# first word (bare imperative-report shape, e.g. "Logged the entry ..."). The subject prefix
# is optional in the SAME group, so one pattern covers both required shapes.
CLAIM_SHAPE = re.compile(
    rf"^(?:(?:i|we)(?:{_APOS}ve|\s+have)?\s+)?(?P<verb>{_VERB_PATTERN})\b",
    re.IGNORECASE,
)

# Artifact cues, word-boundary matched. `log` is handled separately (see _has_cue) because
# `O(log n)` / `O(E log V)` / `O(n log k)` is the single most common false-positive source in
# a DSA (data structures & algorithms) coaching repo.
CUE_WORDS = re.compile(
    r"\b(?:file|note|tracker|schedule|row|stash|ledger|table|commit|branch)\b",
    re.IGNORECASE,
)
CUE_EXTENSION = re.compile(r"\.(?:md|py|ya?ml|json)\b", re.IGNORECASE)
CUE_LOG = re.compile(r"\blog\b", re.IGNORECASE)

# A whole Big-O expression, whatever else it contains ("O(E log V)", "O(n log k)"). Scrubbed
# out before the cue scan below, so a `log` INSIDE one never counts -- not just a `log`
# sitting directly next to the literal "O(".
BIG_O_SPAN = re.compile(r"\bO\([^)]*\)", re.IGNORECASE)

# A `log` OUTSIDE any O(...) span still doesn't count when it is the complexity idiom on its
# own: followed by " n", "(", a subscript-2 (₂ or _2), or preceded by "O(" with no
# matching close paren caught above. Checked around each remaining `\blog\b` hit.
_LOG_AFTER = re.compile(r"^\s*(?:n\b|\(|₂|_2)")
_LOG_BEFORE = re.compile(r"O\(\s*$", re.IGNORECASE)


def _is_complexity_log(sentence: str, match: "re.Match[str]") -> bool:
    before, after = sentence[: match.start()], sentence[match.end() :]
    return bool(_LOG_BEFORE.search(before) or _LOG_AFTER.match(after))


def _has_cue(sentence: str) -> bool:
    scrubbed = BIG_O_SPAN.sub(" ", sentence)
    if CUE_WORDS.search(scrubbed) or CUE_EXTENSION.search(scrubbed):
        return True
    return any(
        not _is_complexity_log(scrubbed, m) for m in CUE_LOG.finditer(scrubbed)
    )


# ── Sentence splitting ───────────────────────────────────────────────────────────
# A boundary is a sentence-ending mark followed by whitespace and then an uppercase letter,
# digit, checkmark or bullet -- NOT every period, so a filename like `743.py.` never splits
# mid-token (the failure a naive `[.!?]` split invites).
_SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[A-Z✅\d\-*])")
_BULLET_START = re.compile(r"^\s*(?:[-*•]|✅)\s*")
_LEADING_FILLER = re.compile(r"^(?:also|just)[,:]?\s+", re.IGNORECASE)

MD_LINK = re.compile(r"\[[^\]]*\]\([^)]*\)")
WIKI_LINK = re.compile(r"\[\[[^\]]*\]\]")
NEGATION = re.compile(
    rf"\b(?:not\s+yet|haven{_APOS}?t|has{_APOS}?n{_APOS}?t|have\s+not|did{_APOS}?n{_APOS}?t|did\s+not)\b",
    re.IGNORECASE,
)
# The apostrophe is MANDATORY on "i'll"/"we'll" (not "i'?ll") -- optional would also match the
# ordinary words "ill" and "well" ("Updated the tracker as well." is not a future tense).
INTENT = re.compile(
    rf"\b(?:will|going\s+to|about\s+to|adding\s+now|next\s+i{_APOS}ll|i{_APOS}ll|we{_APOS}ll|i\s+will|we\s+will)\b",
    re.IGNORECASE,
)


def _filtered_lines(text: str) -> "list[str]":
    """`text`'s lines with fenced code, blockquotes and table rows dropped."""
    kept: "list[str]" = []
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if stripped.startswith(">") or stripped.startswith("|"):
            continue
        kept.append(line)
    return kept


def _paragraph_units(lines: "list[str]") -> "list[str]":
    """Lines regrouped into prose paragraphs, with each bullet/checkmark line its own unit.

    A bullet list is a set of INDEPENDENT claims, not one run-on sentence -- joining
    "- Wrote a.py" and "- Logged b.md" with a bare space would blur two separate lines
    into one, so each bullet line stays its own unit while ordinary prose lines still
    wrap into a paragraph.
    """
    units: "list[str]" = []
    buffer: "list[str]" = []

    def _flush() -> None:
        if buffer:
            units.append(" ".join(buffer))
            buffer.clear()

    for line in lines:
        stripped = line.strip()
        if not stripped:
            _flush()
        elif _BULLET_START.match(stripped):
            _flush()
            units.append(stripped)
        else:
            buffer.append(stripped)
    _flush()
    return units


def _split_sentences(unit: str) -> "list[str]":
    return [s.strip() for s in _SENTENCE_BOUNDARY.split(unit) if s.strip()]


def _clean_sentence_start(sentence: str) -> str:
    """Strip a leading bullet/checkmark marker, then a leading "Also,"/"Just" filler."""
    cleaned = _BULLET_START.sub("", sentence, count=1)
    cleaned = _LEADING_FILLER.sub("", cleaned, count=1)
    return cleaned


def _is_link_only(sentence: str) -> bool:
    """True when `sentence` is nothing but a link/citation -- no verb, no prose."""
    stripped = WIKI_LINK.sub("", MD_LINK.sub("", sentence))
    stripped = re.sub(r"[\s.:;,\-*✅]", "", stripped)
    return not stripped


@dataclass(frozen=True)
class Claim:
    sentence: str
    verb: str


def find_claims(text: str) -> "list[Claim]":
    """Every claim-shaped, artifact-cued sentence in `text` (evidence not yet checked)."""
    claims: "list[Claim]" = []
    for unit in _paragraph_units(_filtered_lines(text)):
        for sentence in _split_sentences(unit):
            if sentence.rstrip().endswith("?"):
                continue  # a question, never a claim
            if NEGATION.search(sentence) or INTENT.search(sentence):
                continue  # "haven't ..." / "will ..." -- not yet done
            if _is_link_only(sentence):
                continue  # a bare citation, no verb of its own
            cleaned = _clean_sentence_start(sentence)
            if cleaned[:4].lower() in ("you ", "your"):
                continue  # the learner as subject, not the agent
            match = CLAIM_SHAPE.match(cleaned)
            if not match:
                continue
            verb = match.group("verb").lower()
            if not _has_required_cue(verb, sentence):
                continue
            claims.append(Claim(sentence=sentence.rstrip(), verb=verb))
    return claims


# ── Evidence ──────────────────────────────────────────────────────────────────────
# Write/Edit/MultiEdit/NotebookEdit and an Agent/Task delegation (a subagent's own report
# is the tool result the claim rests on) are evidence outright. `committed`/`pushed` are
# the exception -- a delegation never substitutes for the actual git command, so they are
# checked separately below and never credited by this set alone.
DIRECT_EVIDENCE_TOOLS = frozenset({"Write", "Edit", "MultiEdit", "NotebookEdit", "Agent", "Task"})
GIT_COMMIT = re.compile(r"\bgit\s+commit\b")
GIT_PUSH = re.compile(r"\bgit\s+push\b")

# ── Read-only Bash/PowerShell detection ──────────────────────────────────────────
# A Bash/PowerShell call is evidence only when it is NOT read-only -- a `grep`/`cat`/
# `git status` read didn't DO anything the claim could rest on. Conservative in the same
# direction as the rest of this hook: an unrecognized command shape counts AS evidence
# (fails toward silence), and only a command matching a known read-only shape, with no
# writing redirect/`tee`/heredoc anywhere in it, is treated as contributing nothing.

# Splits a compound command into its pieces. `\|\|` before `\|` so `||` is never read as
# two single pipes.
_SEGMENT_SPLIT = re.compile(r"&&|\|\||;|\r?\n|\|")

# A bare directory change is neutral -- it does not itself read or write anything, so it
# is dropped before the "every segment is read-only" test rather than required to match
# one of the whitelisted shapes below.
_CD_SEGMENT = re.compile(r"^(?:cd|Set-Location|pushd)\b", re.IGNORECASE)

# One or more leading `NAME=value ` environment-variable assignments, stripped before the
# whitelist match (`PYTHONIOENCODING=utf-8 python scripts/session_date.py` is the same
# read as the bare script).
_ENV_PREFIX = re.compile(r"^(?:[A-Za-z_][A-Za-z0-9_]*=\S*\s+)+")

_READ_ONLY_WORD = re.compile(
    r"^(?:grep|rg|cat|head|tail|ls|find|wc|diff|cmp|stat|file|echo|printf|awk|sort|uniq"
    r"|cut|tr|test|true)\b"
)
_READ_ONLY_SED = re.compile(r"^sed\s+-n\b")
_READ_ONLY_GIT = re.compile(
    r"^git\s+(?:status|diff|log|show|ls-files|ls-remote|branch|remote|rev-parse|blame)\b"
)
_READ_ONLY_PY_SCRIPT = re.compile(
    r"^(?:python3?|py)\s+scripts/(?:links|remaining|effort_budget|check_[a-z_]+"
    r"|meta_review_digest|session_date|promote_report)\.py\b"
)
_READ_ONLY_RECONCILE = re.compile(r"^(?:python3?|py)\s+scripts/reconcile\.py\b")
_READ_ONLY_TECHNIQUE_COVERAGE = re.compile(
    r"^(?:python3?|py)\s+scripts/technique_coverage\.py\s+--check\b"
)
_READ_ONLY_POWERSHELL = re.compile(
    r"^(?:Get-Content|Select-String|Get-ChildItem|Test-Path|Get-Item|Write-Output)\b",
    re.IGNORECASE,
)

# A redirect target that does NOT write anywhere real: discarding output, or duplicating
# one stream onto another (`2>&1`).
_SAFE_REDIRECT_TARGET = re.compile(r"^(?:/dev/null|\$null|&[12])$", re.IGNORECASE)
_REDIRECT = re.compile(r">>?\s*(\S+)")


def _segment_is_read_only(segment: str) -> bool:
    seg = _ENV_PREFIX.sub("", segment.strip())
    if not seg:
        return True
    if seg.startswith("["):
        return True  # the `[` test command
    if _READ_ONLY_WORD.match(seg):
        return True
    if _READ_ONLY_SED.match(seg):
        return True
    if _READ_ONLY_GIT.match(seg):
        return True
    if _READ_ONLY_PY_SCRIPT.match(seg):
        return True
    if _READ_ONLY_RECONCILE.match(seg):
        return "--file" not in seg and "--all" not in seg
    if _READ_ONLY_TECHNIQUE_COVERAGE.match(seg):
        return True
    if _READ_ONLY_POWERSHELL.match(seg):
        return True
    return False


def _has_writing_redirect_or_heredoc(command: str) -> bool:
    if "<<" in command:
        return True
    if re.search(r"\btee\b", command):
        return True
    return any(
        not _SAFE_REDIRECT_TARGET.match(m.group(1)) for m in _REDIRECT.finditer(command)
    )


def _is_read_only_command(command: str) -> bool:
    """True iff EVERY segment of `command` is a recognized read-only shape and the whole
    command carries no writing redirect, `tee`, or heredoc. Anything not recognized, or
    any segment that fails the whitelist, makes the whole command count as evidence --
    the fail-toward-silence direction, so an unknown shape never wrongly suppresses a
    real report."""
    if _has_writing_redirect_or_heredoc(command):
        return False
    for raw in _SEGMENT_SPLIT.split(command):
        seg = raw.strip()
        if not seg or _CD_SEGMENT.match(seg):
            continue  # empty split artifact, or a neutral directory change
        if not _segment_is_read_only(seg):
            return False
    return True


# "committed to <word>" reads as an algorithmic/decision commitment ("committed to the
# greedy choice"), not a repo action -- UNLESS <word> is itself a git-remote cue
# ("Committed to main." stays a real claim). A bare "Committed ..." with no "to X" keeps
# the cue-free repo-action reading unconditionally.
GIT_REMOTE_WORDS = frozenset({"origin", "remote", "upstream", "main", "master", "github"})
GIT_REMOTE_CUE = re.compile(r"\b(?:" + "|".join(GIT_REMOTE_WORDS) + r")\b", re.IGNORECASE)
COMMITTED_TO = re.compile(r"\bcommitted\s+to\s+(\S+)", re.IGNORECASE)


def _committed_reads_as_decision(sentence: str) -> bool:
    match = COMMITTED_TO.search(sentence)
    if not match:
        return False
    word = match.group(1).strip(".,!?;:'\"").lower()
    return word not in GIT_REMOTE_WORDS


def _has_required_cue(verb: str, sentence: str) -> bool:
    """Whether `sentence` carries the cue `verb` needs to count as a claim at all.

    `committed` names a repo action by itself and needs no cue -- except the
    "committed to <decision>" shape, which reads as ordinary algorithmic prose and falls
    back to an ordinary cue requirement (`_committed_reads_as_decision`). `pushed` is
    common DSA (data structures & algorithms) trace vocabulary ("pushed 3 onto the
    stack") and needs either an ordinary cue or a git-remote word (`origin`, `main`, ...);
    it is deliberately never cue-free. Every other verb keeps the ordinary cue rule.
    """
    if verb == "committed":
        return _has_cue(sentence) if _committed_reads_as_decision(sentence) else True
    if verb == "pushed":
        return _has_cue(sentence) or bool(GIT_REMOTE_CUE.search(sentence))
    return _has_cue(sentence)


def _has_evidence(claim: Claim, turn: Turn) -> bool:
    if claim.verb == "committed":
        return any(GIT_COMMIT.search(cmd) for cmd in turn.commands)
    if claim.verb == "pushed":
        return any(GIT_PUSH.search(cmd) for cmd in turn.commands)
    if turn.tool_names & DIRECT_EVIDENCE_TOOLS:
        return True
    return any(not _is_read_only_command(cmd) for cmd in turn.commands)


# How many offending sentences the block message quotes verbatim. One block already covers
# the whole turn (stop_hook_active guards the loop); a long list would just make a re-read
# of the block message itself the next thing to skim past.
MAX_QUOTED_SENTENCES = 3

MESSAGE = (
    "GROUNDED CLAIMS -- this turn states as already done, with no write, edit, commit, "
    "push, or delegation behind it: {sentences}.\n"
    '"If you cannot point to the tool result, it did not happen" -- a claim with none is a '
    "plan, and a plan must be phrased as one. Lapsed Aug 3, 2026 (\"added to your note\" said "
    "before the write) and Aug 21, 2026 twice [P1] (an edit reported but never made; a "
    "schedule failure reported from a partial read).\n"
    "Either make the edit now and re-send with the tool call in THIS turn, or restate the "
    "sentence(s) as a plan (\"I will ...\", \"Next I'll ...\") -- never as something already "
    "done.\n"
    "Rule: .claude/memory/feedback_output_quality.md"
)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return  # malformed input is not this hook's problem -- stay silent
    if not isinstance(payload, dict) or payload.get("stop_hook_active"):
        return  # never block twice -- the re-send passes

    transcript_path = payload.get("transcript_path")
    if not isinstance(transcript_path, str) or not transcript_path:
        return  # missing/null/wrong-typed path (e.g. a bare int) -- nothing to read

    turn = last_turn(transcript_path)
    if not turn.text:
        return

    unevidenced = [c for c in find_claims(turn.text) if not _has_evidence(c, turn)]
    if not unevidenced:
        return

    quoted = "; ".join(f'"{c.sentence}"' for c in unevidenced[:MAX_QUOTED_SENTENCES])
    json.dump({"decision": "block", "reason": MESSAGE.format(sentences=quoted)}, sys.stdout)


# ── Self-test ─────────────────────────────────────────────────────────────────
# python .claude/hooks/grounded_claims.py --selftest
# python .claude/hooks/grounded_claims.py --selftest <real .jsonl>
CASES = [
    # (name, text, should_detect_a_claim)
    # -- block: the spec's own two worked examples --
    ("bare past-tense, sentence-initial", "Logged the entry in the tracker.", True),
    ("first-person contraction", "I've updated the schedule row.", True),
    # -- block: more verbs / more cues --
    ("created + note", "Created a new note for this rep.", True),
    ("restored + tracker", "Restored the tracker from backup.", True),
    ("marked + row/table", "Marked the row as done in the table.", True),
    ("staged + extension", "Staged the changes in schedule.yml.", True),
    ("committed + cue word", "Committed the schedule changes.", True),
    ("pushed + cue word", "Pushed the commit to origin.", True),
    # "well"/"ill" must not be swallowed by an apostrophe-optional we'll/i'll match.
    ("as well, not a future tense", "Updated the tracker as well.", True),
    # -- silent: each of the nine spec exclusions (stop_hook_active is main()'s job) --
    ("blockquote", "> Logged the entry in the tracker.", False),
    ("fenced code", "```\nLogged the entry in the tracker.\n```", False),
    ("table row", "| Logged the entry | tracker.md |", False),
    ("question", "Updated the tracker row, right?", False),
    ("future/intent phrasing",
     "I've updated the file, and I'm going to push it next.", False),
    ("negation", "Updated the tracker row, but I haven't committed it yet.", False),
    ("learner as subject", "You updated the tracker row.", False),
    ("link-only mention", "Rule: .claude/memory/feedback_output_quality.md", False),
    # -- silent: the three teaching-vocabulary collisions --
    ("O(log n) complexity idiom", "Wrote O(log n) as the final bound.", False),
    ("O(E log V) -- log beside another variable, not just 'n'",
     "Added a heap, so the bound is O(E log V).", False),
    ("DP (dynamic programming) table row, passive/third-person",
     "dp[i] is updated from the previous row of the table.", False),
    ("backtracking branch, third-person", "Each branch added one element to the path.", False),
    ("log n work, third-person (spec's own example)", "Each insert added log n work.", False),
    # -- silent: `pushed` is common DSA (data structures & algorithms) trace vocabulary and
    # must NOT fire without an artifact cue or a git-remote word (origin/remote/upstream/
    # main/master/GitHub) -- see _has_required_cue.
    ("pushed, ordinary stack trace, no cue", "Pushed 3 onto the stack.", False),
    ("pushed, ordinary queue trace, no cue", "Pushed the node onto the queue.", False),
    # -- silent: `committed` in its algorithmic/decision sense ("committed to a choice"),
    # not a repo action -- falls back to an ordinary cue requirement, and neither sentence
    # carries one (see _committed_reads_as_decision).
    ("committed, decision sense, no cue",
     "Committed to the greedy choice at each step.", False),
]

# Known, ACCEPTED residual false-positive surface (reported to the lead, not fixed): a
# decision-sense "committed to X" still needs an ordinary cue, but `branch` is ALSO a
# pre-existing artifact cue (git branch) that collides with backtracking vocabulary --
# same class as the O(log n)/DP-row collisions above, just not closeable by a cue check
# alone, since the collision is the cue word itself, not the verb. This fires TRUE (a
# claim), same as it already did before this round's `committed`/`pushed` changes.
KNOWN_RESIDUAL_CASES = [
    ("committed, decision sense, but 'branch' is also a git cue (pre-existing, accepted)",
     "We committed to the left branch.", True),
]

# `pushed`'s bare git-remote-word cue is intentionally broad (per the tech lead's brief) --
# "main" alone anywhere in the sentence counts, so a trace sentence that happens to mention
# "main" (a function, a branch, an ordinary word) can also fire. Reported, not silently
# patched beyond the brief -- see the deviation note in the report.
REPORTED_COLLISION_CASES = [
    ("pushed + bare 'main', ordinary trace (reported collision, not fixed)",
     "Pushed the node, then returned to main.", True),
]


# Evidence cases: (name, claim_text, tool_names, commands, should_block).
# Each entry first asserts `find_claims(claim_text)` is non-empty -- otherwise a case
# would read as "silent" without ever exercising `_is_read_only_command`/evidence at all.
EVIDENCE_CASES = [
    ("Aug 21 case -- grep-only Bash does not evidence a claim",
     "Updated the tracker row.", frozenset({"Bash"}), ("grep -rn TODO tracker.md",), True),
    ("sed -i is a write, not read-only",
     "Updated the tracker row.", frozenset({"Bash"}), ("sed -i 's/a/b/' tracker.md",), False),
    ("an unrecognized script is not on the read-only whitelist",
     "Scaffolded the file.", frozenset({"Bash"}),
     ("python scripts/new_problem.py --number 1 --title X --pattern y --method z",), False),
    ("git status is not git commit",
     "Committed the day's work.", frozenset({"Bash"}), ("git status",), True),
    ("cd prefix stripped, remaining segment still read-only",
     "Updated the tracker row.", frozenset({"Bash"}),
     ("cd repo && grep -n foo file.md",), True),
    ("one non-read-only segment is enough to evidence the whole command",
     "Updated the tracker row.", frozenset({"Bash"}),
     ("grep foo file && python scripts/update_review_dates.py",), False),
    ("Agent delegation evidences a file/record claim",
     "Updated the schedule file.", frozenset({"Agent"}), (), False),
    ("Agent delegation does NOT evidence a pushed claim",
     "Pushed to origin.", frozenset({"Agent"}), (), True),
    ("PowerShell Get-Content is read-only",
     "Updated the tracker row.", frozenset({"PowerShell"}), ("Get-Content x.md",), True),
    ("python -c is an unrecognized shape, not read-only",
     "Updated the tracker row.", frozenset({"Bash"}), ('python -c "print(1)"',), False),
]


def _selftest(transcript: "str | None" = None) -> int:
    failures = 0
    for name, text, expected in CASES:
        got = bool(find_claims(text))
        if got != expected:
            failures += 1
            print(f"FAIL  {name}: detected={got}, expected {expected} -> {find_claims(text)}")
    print(f"claims: {len(CASES) - failures}/{len(CASES)} passed")

    # Documented, accepted behavior -- these run as an ordinary assertion (expected=True in
    # both lists) so a change in outcome is caught, but they are not a "should fix" list.
    collision_cases = KNOWN_RESIDUAL_CASES + REPORTED_COLLISION_CASES
    collision_failures = 0
    for name, text, expected in collision_cases:
        got = bool(find_claims(text))
        if got != expected:
            collision_failures += 1
            print(f"FAIL  {name}: detected={got}, expected {expected} (documented behavior changed)")
    failures += collision_failures
    print(
        f"known/reported collisions: "
        f"{len(collision_cases) - collision_failures}/{len(collision_cases)} confirmed as documented"
    )

    ev_failures = 0
    for name, text, tool_names, commands, should_block in EVIDENCE_CASES:
        claims = find_claims(text)
        if not claims:
            ev_failures += 1
            print(f"FAIL  {name}: find_claims found nothing -- this case tests no evidence path")
            continue
        turn = Turn(text=text, tool_names=tool_names, commands=commands)
        got_block = any(not _has_evidence(c, turn) for c in claims)
        if got_block != should_block:
            ev_failures += 1
            print(f"FAIL  {name}: block={got_block}, expected {should_block}")
    failures += ev_failures
    print(f"evidence: {len(EVIDENCE_CASES) - ev_failures}/{len(EVIDENCE_CASES)} passed")

    if transcript:
        turn = last_turn(transcript)
        if not turn.text.strip():
            failures += 1
            print("FAIL  last_turn recovered no text from a real transcript")
        else:
            print(
                f"transcript: recovered {len(turn.text)} chars of assistant text; "
                f"tool_names={sorted(turn.tool_names)}; commands={len(turn.commands)}"
            )
            claims = find_claims(turn.text)
            unevidenced = [c for c in claims if not _has_evidence(c, turn)]
            print(f"transcript: {len(claims)} claim(s) found, {len(unevidenced)} unevidenced")
            for c in claims:
                print(f"  - [{'UNEVIDENCED' if c in unevidenced else 'evidenced'}] {c.sentence!r}")
    else:
        print("transcript: SKIPPED -- pass a real .jsonl path to exercise the shape")

    return 1 if failures else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        args = [a for a in sys.argv[1:] if a != "--selftest"]
        sys.exit(_selftest(args[0] if args else None))
    main()
