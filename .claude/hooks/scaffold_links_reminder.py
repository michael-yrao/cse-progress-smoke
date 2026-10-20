"""PostToolUse hook: remind the agent to emit problem links after scaffolding.

Fires on every Bash call whose command mentions `new_problem.py`, and injects a
reminder back into the model's context.

Why this exists: the "link every scaffolded problem" rule lapsed five times
(Jul 20/21/23/30/31, 2026) while it lived only as prose in
`.claude/memory/feedback_lineup_links_only.md`. Rules anchored to an *artifact*
(the kickoff table) stop applying the moment the output format changes; a rule
anchored to a *tool invocation* cannot. See the Jul 31 entry in
`.claude/memory/self_eval_log.md`.

Costs no context tokens until it fires.
"""
import json
import re
import sys

# An *invocation*, not a mention. A bare "new_problem.py" substring also matches
# `grep -n ... scripts/new_problem.py` and `python -c "...new_problem.py..."`, which
# fired the reminder twice on 2026-08-02 during read-only work on the script itself.
# That is not harmless: a hook that cries wolf trains the agent to skim past it, which
# costs exactly the reliability that makes a hook stronger than a written rule.
# `--number` is required by the script's own argparse, so every real scaffold has it
# and no read-only command does.
TRIGGER = re.compile(r"new_problem\.py.*--number", re.DOTALL)

# A recognition probe is scaffolded blind (new_problem.py --probe → dsa/probes/). Its
# link rule is the INVERSE of a normal scaffold: the local file link YES (the learner
# opens it to do the rep), the LC/NC link NO (the problem page's tags/editorial name the
# technique — the one thing the probe measures). Asking for "both links" here would make
# the agent hand over the spoiler. See feedback_lineup_links_only.md + dsa/probes/README.md.
# Forward only: a real invocation is always `new_problem.py --probe` (script then flag).
# A `--probe.*new_problem.py` alternation added nothing real and false-matched a compound
# command that merely echoed "--probe" in a label before an unrelated scaffold.
PROBE = re.compile(r"new_problem\.py.*--probe", re.DOTALL)

REMINDER = (
    "Scaffold complete. Before continuing, reply with BOTH links for EVERY problem "
    "just scaffolded: the repo-relative .py path AND its LeetCode URL (NeetCode "
    "mirror if premium). Unprompted, in this turn — do not defer to a later table. "
    "Rule: .claude/memory/feedback_lineup_links_only.md"
)

PROBE_REMINDER = (
    "Probe scaffolded. Reply with the probe's LOCAL FILE LINK ONLY — "
    "[<n> <title>](dsa/probes/<file>.py) — and NO LC/NC link: a recognition probe is "
    "blind, so the problem page's tags/editorial would spoil the technique call. "
    "Unprompted, in this turn. Rule: .claude/memory/feedback_lineup_links_only.md"
)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return  # Malformed input is not this hook's problem — stay silent.

    command = (payload.get("tool_input") or {}).get("command", "")
    if not TRIGGER.search(command):
        return

    reminder = PROBE_REMINDER if PROBE.search(command) else REMINDER
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": reminder,
            }
        },
        sys.stdout,
    )


if __name__ == "__main__":
    main()
