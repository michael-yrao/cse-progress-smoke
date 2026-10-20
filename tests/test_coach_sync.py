"""Tests for the engine sync three-way rule.

Runnable two ways:
    python tests/test_coach_sync.py      # plain asserts, no pytest needed
    pytest tests/test_coach_sync.py

The property that matters most is negative and is asserted directly in
`test_learner_data_is_invisible`: **no learner-owned path may ever appear in a
plan.** Every other guarantee here is a refinement of that one.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from coach_sync import (  # noqa: E402
    ADVISORY_PATHS,
    ENGINE_PATHS,
    WRITING,
    Decision,
    FileVerdict,
    classify_one,
    hash_bytes,
    is_newer,
    iter_tracked,
    matches,
    plan,
)

FAILURES: list[str] = []


def check(label: str, got, want) -> None:
    if got != want:
        FAILURES.append(f"{label}: got {got!r}, want {want!r}")


# --- the three-way table -----------------------------------------------------


def test_classify_table() -> None:
    """Each row of the decision table, by hash triple (local, upstream, baseline)."""
    cases = [
        ("in step", "a", "a", "a", Decision.UNCHANGED),
        ("in step despite stale baseline", "b", "b", "a", Decision.UNCHANGED),
        ("untouched, upstream moved", "a", "b", "a", Decision.UPDATE),
        ("upstream added it", None, "b", None, Decision.NEW),
        ("you edited, upstream still", "b", "a", "a", Decision.KEEP_LOCAL),
        ("both moved", "b", "c", "a", Decision.CONFLICT),
        ("upstream dropped it", "a", None, "a", Decision.REMOVED_UPSTREAM),
    ]
    for label, local, upstream, baseline, want in cases:
        got = classify_one("f.py", local, upstream, baseline).decision
        check(f"classify {label}", got, want)


def test_no_baseline_never_clobbers() -> None:
    """First sync (no manifest): a differing file is a CONFLICT, never an UPDATE.

    This is the guarantee that makes the script safe to run on a repo that was
    created from the template before manifests existed.
    """
    got = classify_one("f.py", "yours", "theirs", None).decision
    check("no baseline -> conflict", got, Decision.CONFLICT)


def test_advisory_is_never_written() -> None:
    """An advisory path that moved upstream reports, and is not a write."""
    v = classify_one("CLAUDE.md", "yours", "theirs", "yours", advisory=True)
    check("advisory decision", v.decision, Decision.ADVISORY)
    check("advisory is not a write", v.is_write, False)
    check("advisory needs attention", v.needs_attention, True)


def test_only_update_and_new_write() -> None:
    """Exactly two decisions may write. Anything else must be read-only."""
    check("writing set", WRITING, {Decision.UPDATE, Decision.NEW})
    for decision in Decision:
        v = FileVerdict("f.py", decision, "a", "b", "a")
        check(f"{decision.value} is_write", v.is_write, decision in WRITING)


# --- path matching -----------------------------------------------------------


def test_glob_matching() -> None:
    cases = [
        ("scripts/new_problem.py", ENGINE_PATHS, True),
        ("curriculum/dsa/milestone.yml", ENGINE_PATHS, True),
        (".claude/skills/cse-coach/SKILL.md", ENGINE_PATHS, True),
        (".claude/memory/feedback_spine_first.md", ENGINE_PATHS, True),
        ("docs/foundations/dsa/patterns/techniques/two_pointer.md", ENGINE_PATHS, True),
        ("scripts/fixtures/cheat-sheets.seed.json", ENGINE_PATHS, True),
        (".claude/skills/cse-coach/evals/evals.json", ENGINE_PATHS, True),
        (".claude/hooks/tests/test_grounded_claims.py", ENGINE_PATHS, True),
        (".github/workflows/fold-attempts.yml", ENGINE_PATHS, True),
        (".github/actions/commit-push/action.yml", ENGINE_PATHS, True),
        # a fixture path that climbs OUT of evals/files/ via `..` must never match, even
        # though it still ends in something evals/files/* would otherwise accept
        (".claude/skills/cse-coach/evals/files/../../../cse.config.yml", ENGINE_PATHS, False),
        # learner data - must never match
        ("docs/foundations/dsa/mastery/dsa_progress.md", ENGINE_PATHS, False),
        ("docs/foundations/schedules/20260727_schedule.md", ENGINE_PATHS, False),
        ("dsa/leetcode/graphs/269_alien_dictionary.py", ENGINE_PATHS, False),
        ("cse.config.yml", ENGINE_PATHS, False),
        (".claude/memory/self_eval_log.md", ENGINE_PATHS, False),
        (".claude/memory/project_whatever.md", ENGINE_PATHS, False),
        # learner-owned vocabulary file; its schema is hand-synced, not the file itself
        ("docs/foundations/dsa/mastery/techniques.yml", ENGINE_PATHS, False),
        ("CLAUDE.md", ADVISORY_PATHS, True),
    ]
    for rel, patterns, want in cases:
        check(f"matches {rel}", matches(rel, patterns), want)


def test_line_endings_do_not_create_phantom_conflicts() -> None:
    """CRLF vs LF is the same content. Git rewrites these on checkout, so if the
    hash were byte-exact, every text file in a Windows repo would look modified."""
    check("crlf == lf", hash_bytes(b"a\r\nb\r\n"), hash_bytes(b"a\nb\n"))
    check("cr == lf", hash_bytes(b"a\rb"), hash_bytes(b"a\nb"))
    check("real difference still differs", hash_bytes(b"a\n") != hash_bytes(b"b\n"), True)
    # binary is hashed verbatim - normalizing would corrupt the comparison
    check("binary untouched", hash_bytes(b"\x00\r\n") != hash_bytes(b"\x00\n"), True)


def test_version_comparison() -> None:
    """Release tags drive the update check, so this is the whole notice mechanism."""
    cases = [
        ("v0.2.0", "0.1.0", True),
        ("0.2.0", "0.1.0", True),
        ("v0.1.0", "0.1.0", False),
        ("v0.1.0", "0.2.0", False),
        ("v0.10.0", "0.9.0", True),  # not a string compare
        ("v1.0", "0.9.9", True),
        # unparseable on either side is never evidence of an update - a notice that
        # can never be cleared is a notice the learner learns to ignore
        ("nightly", "0.1.0", False),
        ("v0.2.0", "unknown", False),
    ]
    for candidate, current, want in cases:
        check(f"is_newer({candidate}, {current})", is_newer(candidate, current), want)


def test_double_star_matches_zero_segments() -> None:
    """`a/**/*.md` must match `a/b.md`, not just `a/x/b.md`."""
    check("zero segments", matches("curriculum/x.yml", ("curriculum/**/*.yml",)), True)
    check("one segment", matches("curriculum/dsa/x.yml", ("curriculum/**/*.yml",)), True)


# --- end to end over real trees ----------------------------------------------


def _tree(root: Path, files: dict[str, str]) -> None:
    for rel, body in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")


def test_learner_data_is_invisible(tmp: Path) -> None:
    """The load-bearing negative test: learner paths never enter a plan at all."""
    local, upstream = tmp / "local", tmp / "upstream"
    learner_files = {
        "docs/foundations/dsa/mastery/dsa_progress.md": "108 rows of my real data",
        "docs/foundations/schedules/20260727_schedule.md": "my week",
        "dsa/leetcode/graphs/269_alien_dictionary.py": "my solution",
        "cse.config.yml": "my config",
        ".claude/memory/self_eval_log.md": "my log",
    }
    _tree(local, {**learner_files, "scripts/a.py": "old"})
    _tree(upstream, {"scripts/a.py": "new"})
    # upstream even ships a file at a learner path - still must be ignored
    _tree(upstream, {"docs/foundations/dsa/mastery/dsa_progress.md": "BLANK SEED"})

    verdicts = plan(local, upstream, {"scripts/a.py": "?"})
    planned = {v.path for v in verdicts}

    for rel in learner_files:
        check(f"{rel} absent from plan", rel in planned, False)
    check("engine file present", "scripts/a.py" in planned, True)

    # and the seed did not overwrite the real tracker
    tracker = local / "docs/foundations/dsa/mastery/dsa_progress.md"
    check("tracker untouched", tracker.read_text(encoding="utf-8"), "108 rows of my real data")


def test_plan_end_to_end(tmp: Path) -> None:
    local, upstream = tmp / "local", tmp / "upstream"
    _tree(
        local,
        {
            "scripts/untouched.py": "v1",
            "scripts/mine.py": "I changed this",
            "scripts/both.py": "I changed this too",
            "scripts/gone.py": "upstream deleted this",
        },
    )
    _tree(
        upstream,
        {
            "scripts/untouched.py": "v2",
            "scripts/mine.py": "v1",
            "scripts/both.py": "upstream changed it",
            "scripts/added.py": "brand new",
        },
    )
    baseline = {
        "scripts/untouched.py": _h("v1"),
        "scripts/mine.py": _h("v1"),
        "scripts/both.py": _h("v1"),
        "scripts/gone.py": _h("upstream deleted this"),
    }
    got = {v.path: v.decision for v in plan(local, upstream, baseline)}

    check("untouched -> UPDATE", got["scripts/untouched.py"], Decision.UPDATE)
    check("mine -> KEEP_LOCAL", got["scripts/mine.py"], Decision.KEEP_LOCAL)
    check("both -> CONFLICT", got["scripts/both.py"], Decision.CONFLICT)
    check("added -> NEW", got["scripts/added.py"], Decision.NEW)
    check("gone -> REMOVED_UPSTREAM", got["scripts/gone.py"], Decision.REMOVED_UPSTREAM)


def test_noise_dirs_skipped(tmp: Path) -> None:
    root = tmp / "noisy"
    _tree(root, {"scripts/__pycache__/x.py": "junk", "scripts/real.py": "ok"})
    found = iter_tracked(root, ENGINE_PATHS)
    check("pycache skipped", "scripts/__pycache__/x.py" in found, False)
    check("real kept", "scripts/real.py" in found, True)


def _h(text: str) -> str:
    """Baseline hash for the fixtures - same function the real manifest uses."""
    return hash_bytes(text.encode())


def main() -> int:
    import tempfile

    test_classify_table()
    test_no_baseline_never_clobbers()
    test_advisory_is_never_written()
    test_only_update_and_new_write()
    test_line_endings_do_not_create_phantom_conflicts()
    test_glob_matching()
    test_version_comparison()
    test_double_star_matches_zero_segments()

    with tempfile.TemporaryDirectory() as td:
        test_learner_data_is_invisible(Path(td) / "a")
    with tempfile.TemporaryDirectory() as td:
        test_plan_end_to_end(Path(td) / "b")
    with tempfile.TemporaryDirectory() as td:
        test_noise_dirs_skipped(Path(td) / "c")

    if FAILURES:
        print(f"FAILED ({len(FAILURES)}):")
        for f in FAILURES:
            print("  -", f)
        return 1
    print("all coach-sync tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
