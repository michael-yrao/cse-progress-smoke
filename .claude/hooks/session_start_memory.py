"""SessionStart hook: load the agent memory index into context, unprompted.

Fires at session startup/resume/clear/compact and injects `.claude/memory/MEMORY.md`
plus the small set of gates that must fire without being asked for.

Why this exists
---------------
CLAUDE.md already says "read MEMORY.md at the start of each session", but that is a
rule about starting a session, and a session that opens with a direct technical
question ("whats the issue with my code here") does not feel like a start. On
2026-08-02 the memory index was never loaded at all until the learner asked about it
nine turns in — so `feedback_ask_complexity` and `feedback_self_evaluation` were not
merely ignored, they were absent, and both failed in the same session.

The structural fact this encodes: **CLAUDE.md is always injected; `.claude/memory/*.md`
are opt-in reads.** A rule that must fire unprompted cannot live only in memory.
This hook removes the choice — the index arrives whether or not the session looks
like a start.

Note the header below is not decoration. Dumping the index alone would reproduce the
failure it is meant to fix: on 2026-08-02 the index line for the complexity gate
existed and was correct, and the gate still did not fire, because what was missing was
never the *content* — it was the binding to a *moment*. So the gates are restated as
if/then triggers, not as topics.

See the 2026-08-02 entry in `.claude/memory/self_eval_log.md`.
"""
import datetime as _dt
import json
import os
import re
import sys
from pathlib import Path

MEMORY_INDEX = Path("memory") / "MEMORY.md"
SELF_EVAL_LOG = Path("memory") / "self_eval_log.md"

# Cadence thresholds for the meta-review overdue check. These live in cse.config.yml under
# `self_eval:`; the literals here are an ANNOUNCED-in-comment fallback for when the config or a
# YAML parser is unavailable (this hook must never depend on PyYAML — it runs at session start
# and a hard dependency here recreates the no-rules-loaded failure). A regex read keeps it
# dependency-free. These are an operational cadence, not an engine-tuned value, so they are not
# in check_single_source's tracked set.
_META_REVIEW_DAYS_FALLBACK = 14
_OPEN_THRESHOLD_FALLBACK = 8

# The recurring DSA mock interview (the mock slot). Cadence lives in cse.config.yml
# under `dsa_mock:` (`every_days`, `first_due`); like the meta-review thresholds, a regex
# read keeps this hook dependency-free. There is NO `first_due` fallback: with the key
# absent and no mock logged yet, the banner stays silent rather than invent an anchor.
_DSA_MOCK_BLOCK = "dsa_mock"
_DSA_MOCK_EVERY_DAYS_FALLBACK = 28
# The banner opens this many days before the due date.
_DSA_MOCK_WINDOW_DAYS = 7
# A schedule file is named for its MONDAY; its Sunday is this many days later.
_MONDAY_TO_SUNDAY_DAYS = 6
_DSA_MOCK_LOG = Path("docs") / "foundations" / "dsa" / "mocks" / "README.md"
_SCHEDULES_DIR = Path("docs") / "foundations" / "schedules"
_MOCK_GLYPH = "🎤"
# A Log-table row: `| 3 | 2026-11-08 | ...` -- the first date cell after the number.
_MOCK_LOG_ROW = re.compile(r"(?m)^\|\s*\d+\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|")
# A schedule table row whose Start (S, second) cell carries the mock glyph.
_MOCK_SEATED_ROW = re.compile(rf"(?m)^\|[^|\n]*\|[^|\n]*{_MOCK_GLYPH}[^|\n]*\|")

# Gates that must fire without being asked for.
#
# **Keep this list short and keep it earned.** It is injected every single session, so
# every line costs tokens forever. Entry criteria: (a) it must fire unprompted, (b) it has
# actually lapsed before, (c) no source fix or other hook already covers it — a rule the
# tooling now enforces belongs in the script, not here. Scaffold links left on criterion
# (c) when new_problem.py started printing them; the past-midnight dating gate left on
# 2026-08-16 for the same reason, once session_date.py had source-fixed it and the gate's
# own text ("new_problem.py has no --date flag") had gone stale and wrong.
#
# Keep this text free of emoji and arrow glyphs — see the note in emit().
ALWAYS_ON = """\
ALWAYS-ON GATES — each is bound to a MOMENT, not a topic. Check the trigger, not the mood of the session.

1. About to propose a comfort rating (green/yellow/red)? -> The COMPLEXITY GATE is already overdue.
   Time AND space, each with an itemized why-clause, from the learner, BEFORE the rating. It fires on
   the rep, not the ritual: "what's wrong with my code" with no scaffold and no kickoff is still a rep.
   Step 1 of CLAUDE.md's LeetCode Review Workflow. (Skipped entirely 2026-08-02.) The RATING ignores
   Big-O (2026-09-23): a miss never lowers or caps it, only feeds the end-of-week cleanup.
2. Something you did just got corrected — by the learner OR by you, unprompted? -> Append a dated entry
   to .claude/memory/self_eval_log.md IN THE SAME TURN. A sentence in chat is not a fix; it dies with
   the context window. (Caught-then-not-logged 2026-08-02.)
3. Fixing a recurring miss? -> Climb the intervention ladder: source fix > hook > skill reference /
   CLAUDE.md step > memory file. A coaching-moment rule belongs in a skill reference (it loads at that
   moment); an unprompted one in CLAUDE.md. A rule that lapsed twice as prose won't be fixed by better prose.
4. Asked to close out / commit / push / archive? -> Verify it against the visible state of the work
   first, and ASK if they disagree. If any part of a turn contains fabricated tool output, none of that
   turn is evidence. (2 occurrences in one day.)
5. Handing over a retry? -> Problem number and links only. No prior rating, no prior failure category,
   no "where the rep lives" — that is stuck_log content and it pre-localizes the rep. (2 occurrences.)
6. Last session of the week? -> Archive this week's schedule AND generate next week's, before the
   commit. Both, or neither counts. Step 7 of CLAUDE.md's LeetCode Review Workflow. (Missed 2026-08-02.)
7. Learner asks to start the day / a session (a kickoff)? -> Scaffold the WHOLE day's board (every
   problem on today's schedule, active block AND both warmups) BEFORE presenting it. A message naming
   a specific problem is NOT a kickoff -- scaffold only that. (Presented-not-scaffolded Sep 12 AND 13,
   2026; the reference-tier fix lapsed in a day. Gate 9 of CLAUDE.md; kickoff_scaffold_reminder.py.)
8. About to send a message? -> ONE message after the last tool call -- no progress narration,
   no partial results. Every repo-state claim names its tool result; a claim with none is a
   plan, not a report. See grounded_claims.py. (Aug 3, Aug 21 x2, 2026.)

Load the individual memory file before acting on any rule you are unsure about. Index follows.
"""


def project_root() -> Path:
    """Resolve the .claude directory, preferring the harness-provided project dir."""
    env_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_dir:
        candidate = Path(env_dir) / ".claude"
        if candidate.is_dir():
            return candidate
    # Fall back to this script's own location (.claude/hooks/ -> .claude/), which is
    # correct regardless of the working directory the hook is invoked from.
    return Path(__file__).resolve().parent.parent


def _block_scope(text: str, block: str) -> "str | None":
    """The body of one top-level `block:` mapping in cse.config.yml, or None if absent."""
    match = re.search(rf"(?ms)^{re.escape(block)}:\s*$(.*?)^\S", text + "\n\\Z")
    return match.group(1) if match else None


def _config_int(claude_dir: Path, key: str, fallback: int, block: str = "self_eval") -> int:
    """Read one `<block>.<key>` int from cse.config.yml via regex (no PyYAML dep)."""
    try:
        text = (claude_dir.parent / "cse.config.yml").read_text(encoding="utf-8")
        scope = _block_scope(text, block)
        if scope is None:
            scope = text
        m = re.search(rf"^\s+{re.escape(key)}:\s*(\d+)", scope, re.M)
        return int(m.group(1)) if m else fallback
    except Exception:
        return fallback


def _config_date(claude_dir: Path, key: str, block: str) -> "_dt.date | None":
    """Read one `<block>.<key>` ISO date from cse.config.yml, or None if absent."""
    text = (claude_dir.parent / "cse.config.yml").read_text(encoding="utf-8")
    scope = _block_scope(text, block)
    if scope is None:
        return None
    m = re.search(rf"^\s+{re.escape(key)}:\s*(\d{{4}}-\d{{2}}-\d{{2}})", scope, re.M)
    return _dt.date.fromisoformat(m.group(1)) if m else None


def meta_review_banner(claude_dir: Path) -> str:
    """Return a loud one-line banner if the self-eval meta-review is overdue, else ''.

    Fail-soft: any parsing problem returns '' — a broken check must never block session start.
    The meta-review used to be an unfired paragraph ('weekly, or ~8 open'); this computes the
    trigger so it actually fires. Robust signal is the DAYS-since-last-meta-review (a date can't
    be miscounted); the open count is a secondary, approximate nudge.
    """
    try:
        log = (claude_dir / SELF_EVAL_LOG).read_text(encoding="utf-8")
    except OSError:
        return ""
    try:
        review_dates = re.findall(r"(?im)^#+.*META-REVIEW\D*(\d{4}-\d{2}-\d{2})", log)
        last = max(review_dates) if review_dates else None
        # A real entry starts a line and carries a [P1]/[P2] priority tag after its date
        # (## 2026-09-04 [P2] — … or - **2026-08-06 [P1]** …). Requiring the tag excludes the
        # many dated *references* inside prose/cross-refs — the over-count the earlier audit warned
        # about. Count only OPEN entries dated AFTER the last meta-review: legitimately-open one-offs
        # are meant to stay open, so counting the total would keep firing forever after a clean review.
        # The count resets at each review and climbs only as NEW opens accrue.
        open_count = 0
        for m in re.finditer(r"(?im)^(?:#+|-)\s+\**(\d{4}-\d{2}-\d{2})\s*\**\s*\[P\d\].*$", log):
            if "consolidated" in m.group(0).lower():
                continue
            if last is not None and m.group(1) <= last:
                continue
            open_count += 1
        days_thr = _config_int(claude_dir, "meta_review_days", _META_REVIEW_DAYS_FALLBACK)
        open_thr = _config_int(claude_dir, "open_threshold", _OPEN_THRESHOLD_FALLBACK)

        overdue_days = None
        if last:
            try:
                delta = (_dt.date.today() - _dt.date.fromisoformat(last)).days
                overdue_days = delta if delta >= days_thr else None
            except ValueError:
                overdue_days = None
        if overdue_days is None and open_count < open_thr:
            return ""
        why = []
        if overdue_days is not None:
            why.append(f"{overdue_days}d since last ({last})")
        if open_count >= open_thr:
            why.append(f"~{open_count} open entries")
        return (
            "!! SELF-EVAL META-REVIEW OVERDUE (" + "; ".join(why) + "). Before other work, cluster the "
            "open entries in .claude/memory/self_eval_log.md by root cause and promote any 2+ recurrence "
            "up the ladder (source fix > hook > skill reference / CLAUDE.md step > memory file); then "
            "archive consolidated entries. See feedback_self_evaluation.md.\n\n"
        )
    except Exception:
        return ""


# Today is not a missed day until it is over, so the trailing misses compute_streak
# (scripts/gamify.py) counts are `(today - last).days - 1`; kept as a named constant here
# rather than copied inline (see check_single_source.py).
_TODAY_NOT_OVER_DAYS = 1


def _trailing_misses(streak: dict, today: _dt.date) -> int:
    """Missed days since `lastStudyDay`, today excluded. Raises on missing/bad fields."""
    last_study_day = _dt.date.fromisoformat(streak["lastStudyDay"])
    return max(0, (today - last_study_day).days - _TODAY_NOT_OVER_DAYS)


def _streak_is_live(streak: dict, today: _dt.date) -> "bool | None":
    """Mirror compute_streak's liveness check (scripts/gamify.py) without importing it.

    A streak is live iff the freezes banked right after the last study day (`freezes`)
    cover the days missed since — the same test compute_streak uses to decide whether
    `current` resets to 0 at the NEXT regeneration. Reading `current` alone is
    generation-time only: it can still show a positive number days after it went stale,
    because nothing regenerates progress.json between sessions.

    Returns None (rather than raising) when `lastStudyDay`/`freezes` is missing or
    unparseable, so the caller can fail-soft to the pre-existing behaviour.
    """
    try:
        misses = _trailing_misses(streak, today)
        banked = int(streak["freezes"])
    except (KeyError, TypeError, ValueError):
        return None
    return misses <= banked


def dsa_mock_due(today: _dt.date, last_logged: "_dt.date | None",
                 first_due: "_dt.date | None", every_days: int,
                 seated: "list[_dt.date]") -> "str | None":
    """The DSA-mock-due banner, or None when it should stay silent. Pure.

    Due date = last logged mock + every_days, else the configured first_due (None when
    neither exists). Fires once the due date is within the window (or overdue) AND no
    mock row is seated on a Sunday inside the due week: `seated` holds the Sundays whose
    live schedule carries a mock row, and any Sunday >= due - 6 days counts as seating it.
    """
    due = last_logged + _dt.timedelta(days=every_days) if last_logged else first_due
    if due is None:
        return None
    if (due - today).days > _DSA_MOCK_WINDOW_DAYS:
        return None
    due_week_start = due - _dt.timedelta(days=_MONDAY_TO_SUNDAY_DAYS)
    if any(sunday >= due_week_start for sunday in seated):
        return None
    since = (f" ({(today - last_logged).days}d since last {last_logged})"
             if last_logged else "")
    return (
        f"!! DSA MOCK DUE {due}{since} -- seat a mock row on that week's Sunday and skip "
        "the recognition probe that week. See references/dsa-mock.md.\n\n"
    )


def _logged_mock_dates(root: Path) -> "list[_dt.date]":
    """Every date in the mock log's table rows; [] when the README is absent."""
    try:
        text = (root / _DSA_MOCK_LOG).read_text(encoding="utf-8")
    except OSError:
        return []
    return [_dt.date.fromisoformat(d) for d in _MOCK_LOG_ROW.findall(text)]


def _seated_mock_sundays(root: Path) -> "list[_dt.date]":
    """The Sunday of every LIVE (non-archive) schedule week that has a mock row seated."""
    sundays = []
    for path in sorted((root / _SCHEDULES_DIR).glob("[0-9]" * 8 + "_schedule.md")):
        monday = _dt.datetime.strptime(path.name[:8], "%Y%m%d").date()
        if _MOCK_SEATED_ROW.search(path.read_text(encoding="utf-8")):
            sundays.append(monday + _dt.timedelta(days=_MONDAY_TO_SUNDAY_DAYS))
    return sundays


def dsa_mock_banner(claude_dir: Path, today: "_dt.date | None" = None) -> str:
    """Return the DSA-mock-due banner for this repo, else ''.

    Fail-soft like meta_review_banner: any parsing problem returns '' -- a broken check
    must never block session start. A fresh template checkout (no cse.config.yml, no
    mock log, no schedules) lands in the except branch and returns ''.
    """
    try:
        root = claude_dir.parent
        logged = _logged_mock_dates(root)
        return dsa_mock_due(
            today or _dt.date.today(),
            max(logged) if logged else None,
            _config_date(claude_dir, "first_due", _DSA_MOCK_BLOCK),
            _config_int(claude_dir, "every_days", _DSA_MOCK_EVERY_DAYS_FALLBACK,
                        _DSA_MOCK_BLOCK),
            _seated_mock_sundays(root),
        ) or ""
    except Exception:
        return ""


def progress_banner(claude_dir: Path) -> str:
    """Return one honest progress line from progress.json, or '' if unavailable.

    Reads the generated contract directly (no subprocess, no import) so a coaching
    session opens with the streak in view — the Duolingo "here's your streak" moment.
    Fail-soft to the bone: any problem returns '', because a motivational line must
    never be the reason a session starts with no rules loaded. The file is regenerated
    by the pre-commit hook, so it is normally fresh; a stale or missing file just means
    no banner — including a fresh template checkout, which has no dashboard/ yet at
    all. Emoji survive emit()'s json.dump escaping (see emit's docstring).
    """
    try:
        data = json.loads((claude_dir.parent / "dashboard" / "progress.json")
                          .read_text(encoding="utf-8"))
        streak = data["streak"]["current"]
        pl = data["pipeline"]
        reps = data["totals"]["reps"]
        # `current` is only as fresh as the last regeneration; re-check liveness against
        # "today" rather than trusting a number that can be days stale (see
        # _streak_is_live). live=None (fields missing/unparseable) falls back to the
        # pre-existing streak-truthiness check, never a crash.
        today = _dt.date.today()
        live = _streak_is_live(data["streak"], today)
        if streak and live is not False:
            flame = f"🔥 {streak}-day study streak"
            if live:
                left = int(data["streak"]["freezes"]) - _trailing_misses(data["streak"], today)
                flame += f" · 🧊 {left}/{data['streak']['freezeMax']} freezes"
        else:
            flame = "streak lapsed — a rep today restarts it"
        return (f"PROGRESS: {flame} · {pl['graduated']}🎓 + {pl['retired']}🏆 mastered · "
                f"{reps} reps. Full dashboard: progressiveoverflow.com/progress\n\n")
    except Exception:  # noqa: BLE001 — a missing/partial file is normal, never fatal
        return ""


_PS_RESULTS_DIR = "pattern_sense_results"
_PS_DECK_START = re.compile(r"^\s*-\s*week:\s*['\"]?(\d{4}-\d{2}-\d{2})", re.MULTILINE)
_PS_RESULTS_KEY = re.compile(r"^\s+results:", re.MULTILINE)


def _ps_ingested_weeks(decks_text: str) -> set[str]:
    """Weeks whose deck block in pattern_sense.yml carries a `results:` key (text scan, no yaml)."""
    starts = list(_PS_DECK_START.finditer(decks_text))
    ends = [m.start() for m in starts[1:]] + [len(decks_text)]
    return {m.group(1) for m, end in zip(starts, ends)
            if _PS_RESULTS_KEY.search(decks_text, m.end(), end)}


def pattern_sense_banner(claude_dir: Path) -> str:
    """One line when a site-saved Pattern Sense results file is waiting, else ''.

    A directory glob plus one yml read; no network, no subprocess. Silent when the folder or
    the yml is missing, or on any error: a nudge must never block a session start.
    """
    try:
        dashboard = claude_dir.parent / "dashboard"
        files = sorted((dashboard / _PS_RESULTS_DIR).glob("*.json"))
        if not files:
            return ""
        ingested = _ps_ingested_weeks(
            (dashboard / "pattern_sense.yml").read_text(encoding="utf-8"))
        for path in files:
            week = f"{path.stem[:4]}-{path.stem[4:6]}-{path.stem[6:]}"
            if week not in ingested:
                return (f"PATTERN SENSE: results waiting for week {week} — run "
                        f"python scripts/pattern_sense.py ingest --pending\n\n")
        return ""
    except Exception:  # noqa: BLE001 — a missing/partial file is normal, never fatal
        return ""


_ATTEMPT_PREFIX = "# po-attempt: "
_ATTEMPT_NAME = re.compile(r"^(\d+)_[a-z0-9_]+\.py$")


def _attempt_is_complete(path: Path) -> bool:
    try:
        with path.open(encoding="utf-8") as handle:
            first = handle.readline().rstrip("\n")
        return first.startswith(_ATTEMPT_PREFIX) and \
            json.loads(first[len(_ATTEMPT_PREFIX):]).get("complete") is True
    except (OSError, ValueError, AttributeError):  # one bad file must not hide the others
        return False


def practice_banner(claude_dir: Path) -> str:
    """One line when a completed site rep waits in dsa/attempts/, else ''.

    Counts problems whose NEWEST file (by date folder) is complete. A glob plus one first-line
    read per problem; no network, no subprocess. Silent on any error, like its neighbours.
    """
    try:
        newest: dict[str, Path] = {}
        for path in sorted((claude_dir.parent / "dsa" / "attempts").glob("*/*.py")):
            match = _ATTEMPT_NAME.match(path.name)
            if match:
                newest[match.group(1)] = path  # sorted by date folder: the last one wins
        waiting = sum(1 for path in newest.values() if _attempt_is_complete(path))
        if not waiting:
            return ""
        return (f"PRACTICE: {waiting} completed rep(s) waiting — run "
                f"python scripts/fold_attempt.py --pending\n\n")
    except Exception:  # noqa: BLE001 — a missing/partial file is normal, never fatal
        return ""


def emit(context: str) -> None:
    """Write the hook envelope to stdout.

    ⚠️ Do NOT add `ensure_ascii=False` here, and keep emoji out of ALWAYS_ON. The memory
    index carries emoji (the Comfort scale is literally emoji) and this runs on Windows,
    where stdout defaults to cp1252 — encoding them raw raises UnicodeEncodeError and the
    session starts with no rules loaded, the exact failure this hook exists to prevent.
    `json.dump` escapes them to \\uXXXX by default, so the wire bytes stay pure ASCII and
    the emoji survive the round trip. Same class of bug as the 2026-07-04 / 2026-07-08
    entries in self_eval_log.md.
    """
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context,
            }
        },
        sys.stdout,
    )


def main() -> None:
    claude_dir = project_root()
    index_path = claude_dir / MEMORY_INDEX
    try:
        index = index_path.read_text(encoding="utf-8")
    except OSError as exc:
        # Surface the failure rather than starting a session that silently has no
        # rules loaded — a quiet no-op here recreates the exact bug this hook fixes.
        emit(
            f"⚠️ SessionStart hook could not read the memory index at {index_path} "
            f"({exc.__class__.__name__}: {exc}). Agent memory is NOT loaded — read "
            f".claude/memory/MEMORY.md manually before relying on any standing rule."
        )
        return

    emit(f"{meta_review_banner(claude_dir)}{dsa_mock_banner(claude_dir)}{progress_banner(claude_dir)}{pattern_sense_banner(claude_dir)}{practice_banner(claude_dir)}{ALWAYS_ON}\n{index}")


if __name__ == "__main__":
    main()
