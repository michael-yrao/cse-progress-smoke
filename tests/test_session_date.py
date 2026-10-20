"""Tests for session-date detection and the restore-merge collision check.

Runnable two ways:
    python tests/test_session_date.py    # plain asserts, no pytest needed
    pytest tests/test_session_date.py

Both behaviors under test are silent-failure guards, which is exactly the kind that
rots without a test: a wrong session date produces a plausible-looking tracker row, and
a shadowed helper class produces code that runs and is wrong.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import restore_history  # noqa: E402
import session_date  # noqa: E402


def _at(hour: int, minute: int = 0, day: int = 15) -> datetime:
    return datetime(2026, 8, day, hour, minute)


def _stub_git(monkey: dict, *, dirty: bool, last_commit: datetime | None) -> None:
    """Replace the two git probes so detection is tested without a real repo."""
    monkey["dirty"] = session_date.has_uncommitted_changes
    monkey["commit"] = session_date.last_commit_time
    session_date.has_uncommitted_changes = lambda: dirty
    session_date.last_commit_time = lambda: last_commit


def _restore_git(monkey: dict) -> None:
    session_date.has_uncommitted_changes = monkey["dirty"]
    session_date.last_commit_time = monkey["commit"]


def test_daytime_uses_wall_clock() -> None:
    """After the small-hours cutoff nothing is inferred — the clock is the answer."""
    monkey: dict = {}
    _stub_git(monkey, dirty=True, last_commit=_at(9, 55))
    try:
        when, reason = session_date.detect_session_date(_at(10))
        assert when.date() == _at(10).date(), when
        assert reason is None, reason
    finally:
        _restore_git(monkey)


def test_small_hours_dirty_tree_rolls_back() -> None:
    """A dirty tree at 00:40 means a session in progress — it started yesterday."""
    monkey: dict = {}
    _stub_git(monkey, dirty=True, last_commit=None)
    try:
        when, reason = session_date.detect_session_date(_at(0, 40))
        assert when.date() == _at(0, 40, day=14).date(), when
        assert reason and "dirty" in reason, reason
    finally:
        _restore_git(monkey)


def test_small_hours_recent_commit_rolls_back() -> None:
    """Clean tree but a commit minutes ago is still a live session, not a new day."""
    monkey: dict = {}
    _stub_git(monkey, dirty=False, last_commit=_at(0, 10))
    try:
        when, reason = session_date.detect_session_date(_at(0, 40))
        assert when.date() == _at(0, 40, day=14).date(), when
        assert reason and "live session" in reason, reason
    finally:
        _restore_git(monkey)


def test_small_hours_cold_repo_uses_wall_clock() -> None:
    """Clean tree, no recent commit: nothing suggests work in progress — don't guess."""
    monkey: dict = {}
    _stub_git(monkey, dirty=False, last_commit=datetime(2026, 8, 10, 21, 0))
    try:
        when, reason = session_date.detect_session_date(_at(2))
        assert when.date() == _at(2).date(), when
        assert reason is None, reason
    finally:
        _restore_git(monkey)


def test_explicit_date_always_wins() -> None:
    assert session_date.resolve("2026-07-04") == "2026-07-04"
    assert session_date.resolve("20260704") == "2026-07-04"
    assert session_date.resolve("2026-07-04", fmt="%Y%m%d") == "20260704"


def test_bad_explicit_date_is_fatal() -> None:
    """A typo'd --date must not silently fall through to the clock."""
    try:
        session_date.resolve("July 4")
    except SystemExit:
        return
    raise AssertionError("expected SystemExit on an unparseable --date")


def test_duplicate_top_level_names_flags_shadowed_helper() -> None:
    """The merge case that motivated the check: two same-named helper classes."""
    merged = (
        "class TrieNode:\n    pass\n\n"
        "class Solution:\n    def f_20260802(self):\n        return 1\n\n"
        "class TrieNode:\n    pass\n"
    )
    dupes = dict(restore_history.duplicate_top_level_names(merged))
    assert "TrieNode" in dupes, dupes
    assert len(dupes["TrieNode"]) == 2, dupes
    assert "Solution" not in dupes, dupes

    warnings = restore_history.collision_warnings(Path("x.py"), merged)
    assert len(warnings) == 1 and "TrieNode" in warnings[0], warnings


def test_dated_helpers_do_not_collide() -> None:
    """The scaffold banner's advice — dating the helper — must clear the warning."""
    merged = (
        "class TrieNode_20260802:\n    pass\n\n"
        "class TrieNode_20260721:\n    pass\n"
    )
    assert restore_history.duplicate_top_level_names(merged) == []


def test_unparseable_file_is_not_this_checks_problem() -> None:
    assert restore_history.duplicate_top_level_names("class :::\n") == []


def _run_all() -> None:
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
    print("All session-date tests passed.")


if __name__ == "__main__":
    _run_all()
