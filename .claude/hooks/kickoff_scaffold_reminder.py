"""UserPromptSubmit hook: remind the agent that a kickoff greeting must scaffold the board.

Fires when the learner's prompt reads as a session KICKOFF ("let's do our sunday
session", "start saturday session", "/start-day", "what's up today") and injects a
reminder to scaffold the whole day's board BEFORE presenting it.

Why this exists
---------------
"A real kickoff scaffolds every problem on today's schedule before presenting the board"
used to live inline in the always-injected CLAUDE.md and fired every session. The
multi-skill migration demoted it into `references/scaffolding.md` — an opt-in read whose
open-trigger already presumes the decision to scaffold — so at a session-start greeting
the rule was never reached. It lapsed on "start saturday session" (Sep 12, 2026) and
again on "let's do our sunday session" (Sep 13). The Sep 12 fix was a note in that same
cold reference; it lasted one day.

This binds the rule to a MOMENT (the prompt) in a hot tier, the way
`scaffold_links_reminder.py` binds the links rule to a tool invocation. See the
2026-09-13 entry in `.claude/memory/self_eval_log.md` and `decisions.yml`
`kickoff-scaffold-gate`.

Warn-only: it injects context and never blocks. Costs no context tokens until it fires,
and stays silent on a named problem ("let's do 235"), a non-kickoff question ("what's
the bug in my code"), or a CLOSE-OUT ("close monday session", "wrap up and commit") —
a hook that cries wolf trains the agent to skim past it. The close-out guard was added
Sep 14, 2026 after "close monday session" tripped the `<weekday> session` pattern.

Second trigger, the SCOPED START: "doing 332 from tomorrow" took four messages to land as
a pull + scaffold. The coach overrode the script's announced session date with the
wall-clock date (small hours), read the pull as a move to another day, and did not
scaffold on "doing 332" / "I am doing 332 right now". A prompt that is neither a
close-out nor a kickoff but names a problem number next to a do-verb now injects a short
reminder carrying the session date from `scripts/session_date.py`.
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

_DAY = r"(?:mon|tues?|wednes?|thurs?|fri|satur?|sun)(?:day)?"

# Kickoff phrasings. Each requires the *day/session* framing — a bare "start" or a named
# problem must NOT match (that is a scoped scaffold, not a batch). Anchored loosely so
# leading filler ("ok, ", "alright ") still trips it.
KICKOFF_PATTERNS = [
    # "start /let's do/start our sunday session", "start the session", "start today's session"
    r"\b(?:start|do|begin)\b.{0,20}?\b(?:session)\b",
    # "start today", "start the day", "start our day"
    r"\bstart(?:ing)?\b.{0,12}?\b(?:the |our |today'?s )?day\b",
    # "what's up today", "what's on today", "what do we have today"
    r"\bwhat'?s\b.{0,20}?\btoday\b",
    # explicit weekday session, any verb
    rf"\b{_DAY}\b.{{0,8}}?\bsession\b",
    # the slash command
    r"/start-day\b",
]
KICKOFF = re.compile("|".join(KICKOFF_PATTERNS), re.IGNORECASE | re.DOTALL)

# A CLOSE-OUT is the opposite of a kickoff, but "close monday session" / "close out the
# session" match the `<weekday> session` / `do…session` kickoff patterns above and used to
# inject the "scaffold the whole board" reminder at the end of a day (verified Sep 14, 2026
# on "close monday session"). Close-outs use close/wrap/commit/push framing that a kickoff
# never does, so a leading close-out verb suppresses the kickoff reminder. This is also the
# phrase family that carries commit+push authorization (CLAUDE.md gate 8 / decisions.yml
# `close-out-commit-authorization`), so the two must not be confused.
CLOSEOUT = re.compile(
    r"\b(?:clos(?:e|ing)|wrap(?:ping)?(?:\s*up)?|commit|push|"
    r"call it (?:a )?(?:night|day)|done for (?:the )?(?:day|night))\b",
    re.IGNORECASE,
)

# If the prompt names a specific LeetCode problem number, it is a scoped request, not a
# batch kickoff — scaffold only that. A 1-4 digit run guards against matching dates/years.
NAMES_A_PROBLEM = re.compile(r"\b\d{1,4}\b")

REMINDER = (
    "This prompt reads as a session KICKOFF. Per the always-on kickoff gate (CLAUDE.md) "
    "and references/scaffolding.md, a kickoff scaffolds the WHOLE day's board BEFORE the "
    "board is presented: run new_problem.py for EVERY problem on today's schedule "
    "(active block AND both warmup slots, red/yellow/green alike), fill each statement, "
    "THEN present name+links only. Caveat: if the learner named a specific problem "
    "(\"let's do 235\") this is NOT a batch kickoff — scaffold only that one and ask "
    "before batching. Do not commit a scaffold that is never attempted (phantom tracker "
    "rows). Rule: references/scaffolding.md scope section."
)


# Scoped start: a do-verb directly before a 1-4 digit number, or "<number> now|next".
# The number sits right next to the verb (only a problem-ish filler between), is followed
# by end/punctuation/a continuation word, and a month name before it ("Mar 12") disqualifies
# the "<number> now|next" form. A line break or dash ends the clause, and "next" before a
# time noun ("8 next week") is not a start.
_VERB = (
    r"(?:do|doing|start(?:ing)?|pull(?:ing)?|try(?:ing)?|attempt(?:ing)?|work(?:ing)? on|"
    r"let'?s do|i'?ll do|on to|next up)"
)
_FILLER = r"(?:\s+(?:problem|prob|lc|leetcode|number|num|no\.?))?\s*#?\s*"
_MONTH = (
    r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|"
    r"sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\.?\s+"
)
_CONTINUATION = r"(?:now|next|and|&|from|right|today|tonight|first|then|again|please)"
SCOPED_START = re.compile(
    rf"\b{_VERB}\b{_FILLER}(?P<after_verb>\d{{1,4}})\b"
    rf"(?=[ \t]*(?:[.,;:!?)\r\n\-–—]|$)|\s+{_CONTINUATION}\b)"
    rf"|(?P<month>\b{_MONTH})?\b(?P<before_now>\d{{1,4}})\b\s+(?:right\s+)?(?:now|next"
    rf"(?!\s+(?:week|month|year|time|session|day)\b))\b",
    re.IGNORECASE,
)


def scoped_number(prompt: str) -> "str | None":
    """The problem number of the first scoped start in `prompt`, or None."""
    for match in SCOPED_START.finditer(prompt):
        if match.group("month"):
            continue  # a calendar date ("Mar 12 next"), not a problem number
        return match.group("after_verb") or match.group("before_now")
    return None


# A prompt that opens with one of these is a relayed agent report or a system notice, never the learner.
RELAYED_PREFIXES = (
    "Another Claude session sent a message",
    "<agent-message",
    "[Subagent hand-back]",
    "<task-notification",
    "[SYSTEM NOTIFICATION",
)


def is_relayed_message(prompt: str) -> bool:
    """True when `prompt` is a relayed agent message or system notification."""
    return prompt.lstrip().startswith(RELAYED_PREFIXES)


SCOPED_REMINDER = (
    "Learner is starting problem {number} now. {date_sentence}"
    "In THIS turn: (1) if {number} is not on that day's board it is a PULL: reseat it onto "
    "the session date (effort-units: pin the planned figure, the row prices here). A day "
    "named with \"from\" (\"from tomorrow\", \"from Sat\") is the day it is pulled FROM, "
    "never a target; a bare day with no \"from\" is a reseat, not a pull. (2) Scaffold "
    "{number} with new_problem.py before replying, unless its file already carries a stub "
    "dated today (a re-run would stash the attempt in progress). (3) One message. Rule: "
    "references/scaffolding.md scope section."
)


def _date_sentence() -> str:
    """'Session date is YYYY-MM-DD (Weekday) ...' or '' if the date cannot be resolved."""
    try:
        import session_date  # type: ignore

        session, _reason = session_date.detect_session_date(datetime.now())
        return (
            f"Session date is {session.strftime('%Y-%m-%d (%A)')} per scripts/session_date.py "
            "— the script's date, not the clock's. "
        )
    except Exception:  # noqa: BLE001 — a hook that dies silences itself; omit the sentence
        return ""


def _scoped_reminder(number: str) -> str:
    return SCOPED_REMINDER.format(number=number, date_sentence=_date_sentence())


def _emit(context: str) -> None:
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context,
            }
        },
        sys.stdout,
    )


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return  # Malformed input is not this hook's problem — stay silent.

    prompt = payload.get("prompt", "") or ""
    if is_relayed_message(prompt):
        return  # an agent's relayed report or a system notice — never the learner starting a problem
    if CLOSEOUT.search(prompt):
        return  # "close monday session", "wrap up and commit" — a close-out, never a kickoff
    if KICKOFF.search(prompt):
        # A kickoff phrase that also names a problem number is ambiguous; the reminder already
        # carries the "named problem is not a batch" caveat, so still fire.
        _emit(REMINDER)
        return
    number = scoped_number(prompt)
    if number:
        _emit(_scoped_reminder(number))


if __name__ == "__main__":
    main()
