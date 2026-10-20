"""Behavior + config tests for update_review_dates.py.

Runnable two ways:
    python tests/test_engine.py          # plain asserts, no pytest needed
    pytest tests/test_engine.py

Covers: (1) intervals reproduce cse-review's defaults, (2) config overrides are
read, (3) the source-file regex is language-agnostic, (4) an end-to-end run
reorders the tracker by latest date and recomputes next-review dates.
"""
from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "update_review_dates.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("ur", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_intervals_match_defaults():
    m = _load_module()
    base = datetime(2026, 1, 1)
    days = lambda d: (d - base).days
    assert days(m.compute_next_review_date(m.COMFORT_CLEAN, base, 1)) == 30
    assert days(m.compute_next_review_date(m.COMFORT_CLEAN, base, 2)) == 60
    assert days(m.compute_next_review_date(m.COMFORT_CLEAN, base, 3)) == 180
    # 🎓 Graduated is the streak-3 recurring tier (renamed from 🏆 on Jul 26, 2026 —
    # you graduate, THEN you retire; 🏆 is now the terminal tier and has no rows).
    assert days(m.compute_next_review_date(m.COMFORT_GRADUATED, base, 3)) == 180
    # A legacy 🏆 row must still parse and behave as 🎓 rather than being dropped.
    assert days(m.compute_next_review_date(m.COMFORT_RETIRED, base, 3)) == 180
    assert days(m.compute_next_review_date(m.COMFORT_SHAKY, base, 0)) == 10
    assert days(m.compute_next_review_date(m.COMFORT_BLANK, base, 0)) == 2
    assert m.compute_next_review_date(m.COMFORT_CLEAN, None, 1) is None


def test_load_config_overrides(tmp_path: Path):
    m = _load_module()
    cfg_file = tmp_path / "cse.config.yml"
    cfg_file.write_text(
        "intervals:\n"
        "  clean:  { streak1: 45, streak2: 90, retired: 200 }\n"
        "  shaky:  7\n"
        "  blank:  1\n"
        "retire_at_streak: 4\n"
        "solutions:\n"
        '  roots: ["problems/lc"]\n'
        '  globs: ["*.java", "*.py"]\n',
        encoding="utf-8",
    )
    cfg = m.load_config(cfg_file)
    assert cfg["clean_streak1"] == 45
    assert cfg["clean_streak2"] == 90
    assert cfg["shaky"] == 7
    assert cfg["blank"] == 1
    # This config uses the PRE-Jul-26-2026 key names (`retired`, `retire_at_streak`).
    # They must still be honoured, mapped onto the current internal names — an existing
    # cse.config.yml must not silently fall back to defaults after the rename.
    assert cfg["graduated"] == 200
    assert cfg["graduate_at_streak"] == 4
    assert cfg["source_root"] == "problems/lc"
    assert cfg["source_globs"] == ["*.java", "*.py"]


def test_load_config_accepts_current_key_names(tmp_path: Path):
    m = _load_module()
    cfg_file = tmp_path / "cse.config.yml"
    cfg_file.write_text(
        "intervals:\n"
        "  clean:  { streak1: 45, streak2: 90, graduated: 210 }\n"
        "graduate_at_streak: 5\n",
        encoding="utf-8",
    )
    cfg = m.load_config(cfg_file)
    assert cfg["graduated"] == 210
    assert cfg["graduate_at_streak"] == 5


def test_load_config_ignores_lookalike_keys_in_other_blocks(tmp_path: Path):
    """A nested block reusing the words shaky/blank/graduated must NOT set intervals.

    Regression for a live incident (Aug 7, 2026): an `effort_budget` block holding
    effort WEIGHTS was added to a learner's config —

        comfort_base: {blank: 3.0, shaky: 2.0, clean: 1.0, graduated: 0.5}

    — and load_config, which then scraped the raw text with a flat regex, read those
    weights as REVIEW INTERVALS. Shaky went 10 days -> 2 and Graduated 180 -> 0, the
    pre-commit hook rewrote three rows' review dates, and the commit succeeded with no
    error. A flat regex over a nested document cannot tell "the interval named shaky"
    from "any mapping containing the word shaky", so the config was a landmine for any
    future block reusing a common word.
    """
    m = _load_module()
    cfg_file = tmp_path / "cse.config.yml"
    cfg_file.write_text(
        "intervals:\n"
        "  clean:  { streak1: 30, streak2: 60, graduated: 180 }\n"
        "  shaky:  10\n"
        "  blank:  2\n"
        "effort_budget:\n"
        "  comfort_base: {blank: 3.0, shaky: 2.0, clean: 1.0, graduated: 0.5}\n"
        "  ceiling: 9.0\n",
        encoding="utf-8",
    )
    cfg = m.load_config(cfg_file)
    assert cfg["shaky"] == 10, f"effort weight leaked into the Shaky interval: {cfg['shaky']}"
    assert cfg["blank"] == 2, f"effort weight leaked into the Blank interval: {cfg['blank']}"
    assert cfg["graduated"] == 180, f"effort weight leaked into Graduated: {cfg['graduated']}"
    assert cfg["clean_streak1"] == 30
    assert cfg["clean_streak2"] == 60


def test_count_retired_entries_only_counts_the_terminal_section():
    m = _load_module()
    doc = "\n".join([
        "## 🎓 Graduated",
        "- 999. Decoy — must NOT count, this is the recurring tier",
        "## 🏆 Retired",
        "- 704. Binary Search (loopSearch) — retired 2028-01-20",
        "- 217. Contains Duplicate (hashset) — retired 2028-02-01",
        "prose inside the section is not an entry",
        "## Something Else",
        "- 111. Not in the retired section",
    ]).splitlines()
    # Retired problems have LEFT the review table, so they can't be counted from rows —
    # the summary's Retired column comes from this bullet list instead.
    assert m.count_retired_entries(doc) == 2


def test_source_regex_language_agnostic():
    m = _load_module()
    assert m.SOURCE_FILE_RE.match("1_two_sum.py")
    # default config is python-only, so .java should not match
    assert not m.SOURCE_FILE_RE.match("1_two_sum.java")


TRACKER = "docs/foundations/dsa/mastery/dsa_progress.md"

FIXTURE = """# DSA Progress

| Difficulty | Problem | Comfort | Streak | Next Review Date | Latest Attempt Date | Attempt Dates |
|---|---|---|---|---|---|---|
| Easy | [1. Two Sum](https://leetcode.com/problems/two-sum/) | \U0001f7e2 | 1 | | 2026-01-10 | 2026-01-10 |
| Medium | [15. 3Sum](https://leetcode.com/problems/3sum/) | \U0001f534 | 0 | | 2026-02-01 | 2026-02-01 |
"""


def test_end_to_end_reorder_and_recompute(tmp_path: Path):
    repo = tmp_path / "repo"
    (repo / "docs/foundations/dsa/mastery").mkdir(parents=True)
    (repo / "dsa/leetcode").mkdir(parents=True)
    (repo / TRACKER).write_text(FIXTURE, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT)], cwd=repo, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr

    out = (repo / TRACKER).read_text(encoding="utf-8")
    # The fixture uses the pre-rename "Attempt" header on purpose: this asserts BOTH that the old
    # spelling still parses and that it is upgraded to the current one on write.
    assert "| Latest Rep Date | Rep Dates |" in out
    assert "Latest Attempt Date" not in out
    rows = [ln for ln in out.splitlines() if ln.startswith("| ") and "leetcode.com" in ln]
    # Sorted by latest attempt date descending → 3Sum (Feb) before Two Sum (Jan)
    assert "3Sum" in rows[0] and "Two Sum" in rows[1]
    # Clean streak-1 Two Sum: +30 from 2026-01-10 = 2026-02-09
    assert "2026-02-09" in rows[1]
    # Blank 3Sum: +2 from 2026-02-01 = 2026-02-03
    assert "2026-02-03" in rows[0]


SD_FIXTURE = """# System Design Progress

| Difficulty | Problem | Comfort | Streak | Next Review Date | Latest Attempt Date | Attempt Dates |
|---|---|---|---|---|---|---|
| Tier 1 | [URL Shortener](../case_studies/url_shortener.md) | \U0001f7e2 | 1 | | 2026-01-10 | 2026-01-10 |
| Tier 1 | [Rate Limiter](../components/rate_limiter.md) | \U0001f534 | 0 | | 2026-02-01 | 2026-02-01 |
"""


def test_recompute_simple_no_discovery(tmp_path: Path):
    m = _load_module()
    tracker = tmp_path / "design_progress.md"
    tracker.write_text(SD_FIXTURE, encoding="utf-8")
    m.recompute_simple(tracker)
    out = tracker.read_text(encoding="utf-8")
    rows = [ln for ln in out.splitlines() if ln.startswith("| ") and "](" in ln and "Comfort" not in ln]
    # Sorted by latest date desc → Rate Limiter (Feb) before URL Shortener (Jan)
    assert "Rate Limiter" in rows[0] and "URL Shortener" in rows[1]
    assert "2026-02-09" in rows[1]  # Clean streak-1 URL Shortener: +30
    assert "2026-02-03" in rows[0]  # Blank Rate Limiter: +2
    # No source discovery: exactly the two systems, nothing injected
    assert len(rows) == 2


REP_ERA_FIXTURE = """# DSA Progress

| Difficulty | Problem | Comfort | Streak | Next Review Date | Latest Rep Date | Rep Dates |
|---|---|---|---|---|---|---|
| Easy | [1. Two Sum](https://leetcode.com/problems/two-sum/) | \U0001f7e2 | 1 | | 2026-01-10 | 2026-01-10 |
| Medium | [15. 3Sum](https://leetcode.com/problems/3sum/) | \U0001f534 | 0 | | 2026-02-01 | 2026-02-01 |
"""


def test_current_rep_header_parses(tmp_path: Path):
    """The renamed header is the one the engine writes, so it must also be one it reads.

    Without this, only the backward-compat path was covered and a regression in the current
    spelling would look like a passing suite.
    """
    repo = tmp_path / "repo"
    (repo / "docs/foundations/dsa/mastery").mkdir(parents=True)
    (repo / "dsa/leetcode").mkdir(parents=True)
    (repo / TRACKER).write_text(REP_ERA_FIXTURE, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT)], cwd=repo, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr

    out = (repo / TRACKER).read_text(encoding="utf-8")
    rows = [ln for ln in out.splitlines() if ln.startswith("| ") and "leetcode.com" in ln]
    assert len(rows) == 2, "table went invisible — the current header did not match"
    assert "3Sum" in rows[0] and "Two Sum" in rows[1]
    assert "2026-02-09" in rows[1]
    assert "2026-02-03" in rows[0]
    assert "reps" in out and "attempts" not in out


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
REPO = Path(__file__).resolve().parents[1]
WEEK_DAYS = 7
NAME_LIMIT = 80


def _load_bootstrap():
    """bootstrap.py imports its sibling `_console`, so scripts/ must be importable first."""
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location("bootstrap_under_test", SCRIPTS / "bootstrap.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _intake_text(**overrides) -> str:
    fields = {"name": "Alex", "target": "faang_interview", "timezone": "America/New_York",
              "start_date": "2026-10-14"}
    fields.update(overrides)
    return "".join(f"{k}: {v}\n" for k, v in fields.items() if v is not None)


def test_parse_intake():
    mod = _load_bootstrap()

    valid = [
        _intake_text(start_date="2026-10-14"),     # yaml.safe_load gives a datetime.date
        _intake_text(start_date='"2026-10-14"'),   # quoted: a str
    ]
    for text in valid:
        got = mod.parse_intake(text)
        assert got["start"] == "2026-10-14"
        assert got["timezone"] == "America/New_York"
        assert got["target"] == "faang_interview"
        assert (got["language"], got["lead"], got["sd_cadence"]) == ("python", "dsa", "paused")
        assert got["weekly_build"] is True and got["reach_beyond"] == 1 and got["daily_cap"] == 5

    invalid = [
        ("bad timezone", _intake_text(timezone="Mars/Olympus"), "timezone"),
        ("bad date", _intake_text(start_date='"2026-13-45"'), "start_date"),
        ("unknown target", _intake_text(target="whatever"), "target"),
        ("extra key", _intake_text() + "extra: 1\n", "extra"),
        ("missing key", _intake_text(timezone=None), "timezone"),
        ("name empty after strip", _intake_text(name='"   "'), "name"),
        ("name too long", _intake_text(name="a" * (NAME_LIMIT + 1)), "name"),
        ("name with newline", _intake_text(name='"Al\\nex"'), "name"),
    ]
    for label, text, key in invalid:
        try:
            mod.parse_intake(text)
        except mod.IntakeError as e:
            assert key in str(e), f"{label}: message does not name {key}: {e}"
        else:
            raise AssertionError(f"{label}: expected IntakeError")

    assert mod.parse_intake(_intake_text(name="a" * NAME_LIMIT))["name"] == "a" * NAME_LIMIT


def test_write_config(tmp_path: Path, monkeypatch):
    mod = _load_bootstrap()
    monkeypatch.setattr(mod, "CONFIG", tmp_path / "cse.config.yml")
    base = {"name": "Alex", "start": "2026-10-13", "target": "competitive", "daily_cap": 5,
            "language": "python", "lead": "dsa", "reach_beyond": 1, "sd_cadence": "paused"}
    cases = [
        ("clone", False, {"timezone": "UTC", "weekly_build": False}),
        ("intake", True, {"timezone": "America/New_York", "weekly_build": True}),
    ]
    for label, is_intake, extra in cases:
        mod.write_config({**base, **extra}, fill_placeholder_dates=is_intake)
        lines = mod.CONFIG.read_text(encoding="utf-8").splitlines()
        starts = [ln for ln in lines if ln.strip().startswith("starts:")]
        first_due = [ln for ln in lines if ln.strip().startswith("first_due:")]
        assert f"timezone: {extra['timezone']}" in [ln.split("#")[0].rstrip() for ln in lines], label
        wb = str(extra["weekly_build"]).lower()
        assert f"  weekly_build: {wb}" in [ln.split("#")[0].rstrip() for ln in lines], label
        assert len(starts) == 1 and len(first_due) == 1, label
        if is_intake:
            # 2026-10-13 is a Tuesday: the Monday on or after is 2026-10-19; +28 days is 2026-11-10.
            assert starts[0].strip() == "starts: 2026-10-19", label
            assert first_due[0].strip() == "first_due: 2026-11-10", label
        else:
            assert "PLACEHOLDER" in starts[0] and "PLACEHOLDER" in first_due[0], label

    awkward_name = 'Al "the" \\ Ex'
    mod.write_config({**base, "name": awkward_name, "timezone": "UTC", "weekly_build": False})
    written = mod.yaml.safe_load(mod.CONFIG.read_text(encoding="utf-8"))
    assert written["learner"] == awkward_name


def test_strip_placeholder_rows():
    mod = _load_bootstrap()
    summary = ("| | 🏆 Retired | 🎓 Graduated | 🟢 Clean | 🟡 Shaky | 🔴 Blank |\n"
               "|:---|:---:|:---:|:---:|:---:|:---:|\n"
               "| **Solutions** | 0 | 0 | 0 | 0 | 0 |\n")
    header = ("| Difficulty | Problem | Comfort | Streak | Next Review Date | Latest Rep Date | Rep Dates |\n"
              "|---|---|---|---|---|---|---|\n")
    undated = "| Easy | [1. Two Sum](https://leetcode.com/problems/two-sum/) | 🔴 | 0 |  |  |  |\n"
    dated = "| Easy | [217. Contains Duplicate](https://leetcode.com/problems/x/) | 🟢 | 1 | 2026-11-01 | 2026-10-02 | 2026-10-02 |\n"
    cases = [
        ("undated row dropped", summary + "\n" + header + undated, summary + "\n" + header),
        ("dated row kept", summary + "\n" + header + dated, summary + "\n" + header + dated),
        ("summary table untouched", summary, summary),
    ]
    for label, text, want in cases:
        assert mod.strip_placeholder_rows(text) == want, label


def test_intake_builds_week(tmp_path: Path):
    for part in ("scripts", "curriculum", "docs"):
        shutil.copytree(REPO / part, tmp_path / part, ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy(REPO / "cse.config.example.yml", tmp_path / "cse.config.example.yml")
    (tmp_path / "intake.yml").write_text(
        _intake_text(timezone="UTC", start_date="2026-10-12"), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(tmp_path / "scripts" / "bootstrap.py"), "--intake",
         str(tmp_path / "intake.yml"), "--non-interactive"],
        cwd=tmp_path, capture_output=True, text=True, encoding="utf-8",
    )
    assert result.returncode == 0, result.stderr

    weeks = list((tmp_path / "docs/foundations/schedules").glob("*_schedule.md"))
    assert len(weeks) == 1 and "20261012" in weeks[0].name.replace("-", "")
    module_name = "fold_schedule_under_test"
    spec = importlib.util.spec_from_file_location(
        module_name, tmp_path / "scripts" / "fold_schedule.py")
    fold_schedule = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = fold_schedule  # a @dataclass under `from __future__ import annotations` needs it
    try:
        spec.loader.exec_module(fold_schedule)
    finally:
        del sys.modules[module_name]
    headers = fold_schedule.day_headers(
        weeks[0].read_text(encoding="utf-8").splitlines(), datetime(2026, 10, 12).date())
    assert len(headers) == WEEK_DAYS


def _run_all():
    # test_parse_intake / test_write_config / test_strip_placeholder_rows / test_intake_builds_week
    # use pytest features (monkeypatch, skipif); they run under pytest only.
    import tempfile

    test_intervals_match_defaults()
    test_source_regex_language_agnostic()
    # Was defined but never registered here — it only ran under pytest, so `python tests/test_engine.py`
    # reported success without it.
    test_count_retired_entries_only_counts_the_terminal_section()
    with tempfile.TemporaryDirectory() as d:
        test_load_config_overrides(Path(d))
    with tempfile.TemporaryDirectory() as d:
        test_load_config_accepts_current_key_names(Path(d))
    with tempfile.TemporaryDirectory() as d:
        test_load_config_ignores_lookalike_keys_in_other_blocks(Path(d))
    with tempfile.TemporaryDirectory() as d:
        test_end_to_end_reorder_and_recompute(Path(d))
    with tempfile.TemporaryDirectory() as d:
        test_recompute_simple_no_discovery(Path(d))
    with tempfile.TemporaryDirectory() as d:
        test_current_rep_header_parses(Path(d))
    print("All engine tests passed.")


if __name__ == "__main__":
    _run_all()
