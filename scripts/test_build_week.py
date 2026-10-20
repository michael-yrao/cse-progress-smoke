"""Tests for build_week.py. Run with: py -m pytest scripts/test_build_week.py -q"""
from __future__ import annotations

import datetime as dt
import json
import urllib.error

import pytest

import build_week as bw

D = dt.date
NOW = dt.datetime


def _no_network(url: str, timeout: float) -> bytes:
    raise urllib.error.URLError("offline")


# (now, existing mondays, start monday, lead hours, early) -> (monday, skip prefix)
TARGET_CASES = [
    pytest.param(NOW(2026, 10, 21, 12), set(), None, 0, False, D(2026, 10, 19), None,
                 id="current-missing-builds-this-monday"),
    pytest.param(NOW(2026, 10, 21, 12), set(), D(2026, 11, 2), 0, False, D(2026, 11, 2), None,
                 id="future-start-builds-start-monday"),
    pytest.param(NOW(2026, 10, 25, 13), {D(2026, 10, 19)}, None, 10, False, None, "boundary",
                 id="before-boundary-minus-lead"),
    pytest.param(NOW(2026, 10, 25, 14), {D(2026, 10, 19)}, None, 10, False, D(2026, 10, 26), None,
                 id="at-boundary"),
    pytest.param(NOW(2026, 10, 25, 14), {D(2026, 10, 19), D(2026, 10, 26)}, None, 10, False,
                 None, "20261026_schedule.md exists", id="next-exists"),
    pytest.param(NOW(2026, 10, 21, 12), {D(2026, 10, 19)}, None, 0, True, D(2026, 10, 26), None,
                 id="early-builds-next"),
]


@pytest.mark.parametrize(("now", "existing", "start", "lead", "early", "monday", "skip"),
                         TARGET_CASES)
def test_target_week(now, existing, start, lead, early, monday, skip):
    target = bw.target_week(now, frozenset(existing), start, dt.timedelta(hours=lead), early)
    assert target.monday == monday
    assert (target.skip is None) if skip is None else target.skip.startswith(skip)


FULL_BLOCK = {"weekly_build": True, "build_lead_hours": 0, "practice_index_url": "u",
              "prefer_practice_spec": True}


def test_load_automation():
    assert bw.load_automation({}).is_enabled is False
    assert bw.load_automation({"automation": FULL_BLOCK}).is_enabled is True
    incomplete = {"automation": {"weekly_build": True, "build_lead_hours": 0}}
    with pytest.raises(bw.BuildRefused, match="automation.practice_index_url"):
        bw.load_automation(incomplete)


CATALOG = tuple({"number": n, "title": f"P{n}", "difficulty": "Easy", "folder": "f"}
                for n in (1, 2, 3, 4, 5))

# (rows' numbers, site numbers, per week, paused) -> picked numbers
INTAKE_CASES = [
    pytest.param([], None, 2, True, [], id="paused"),
    pytest.param([], None, 3, False, [1, 2, 3], id="index-unavailable-curriculum-order"),
    pytest.param([], frozenset({4, 5}), 2, False, [4, 5], id="index-preferred"),
    pytest.param(["1", "2"], None, 5, False, [3, 4, 5], id="dated-row-excluded"),
    pytest.param(["99"], None, 1, False, [1], id="cap"),
]


@pytest.mark.parametrize(("tracked", "site", "per_week", "paused", "expected"), INTAKE_CASES)
def test_intake_candidates(tracked, site, per_week, paused, expected):
    rows = [{"num": n} for n in tracked]
    picked = bw.intake_candidates(CATALOG, rows, site, per_week, paused)
    assert [entry["number"] for entry in picked] == expected


MONDAY = D(2026, 10, 26)


def _item(number: int, due_offset: int = 0, cost: float = 1.0, is_priority: bool = False):
    due = MONDAY + dt.timedelta(days=due_offset)
    return bw.SeatItem(str(number), f"[{number}]", "🟢", "", due, cost, is_priority, (number,))


def _plan(items, first_offset=0, ceiling=8.0, max_rows=8):
    ctx = bw.PlanContext(MONDAY, MONDAY + dt.timedelta(days=first_offset), ceiling, max_rows,
                         tuple(items))
    plan = bw.plan_week(ctx)
    seated = {f"{d.day:%a}": [i.number for i in d.items] for d in plan.days if d.items}
    return seated, [i.number for i in plan.carried], plan.notes, [d.day.weekday() for d in plan.days]


def test_plan_week():
    at_cap, _, _, _ = _plan([_item(1), _item(2)], max_rows=2)
    assert at_cap == {"Mon": ["1", "2"]}
    over_cap, _, _, _ = _plan([_item(1), _item(2), _item(3)], max_rows=2)
    assert over_cap == {"Mon": ["1", "2"], "Tue": ["3"]}

    at_ceiling, _, _, _ = _plan([_item(1, cost=4.0), _item(2, cost=4.0)])
    assert at_ceiling == {"Mon": ["1", "2"]}
    past_ceiling, _, _, _ = _plan([_item(1, cost=4.0), _item(2, cost=4.0), _item(3, cost=0.5)])
    assert past_ceiling == {"Mon": ["1", "2"], "Tue": ["3"]}

    saturday = 5
    forced, carried, notes, _ = _plan([_item(n, saturday, is_priority=True) for n in (1, 2, 3)],
                                      max_rows=1)
    assert forced == {"Sat": ["1", "3"], "Sun": ["2"]}
    assert carried == [] and notes == ("forced over cap: Sat",)

    _, overflow, notes, _ = _plan([_item(n, saturday) for n in (1, 2, 3)], max_rows=1)
    assert overflow == ["3"] and notes == ()

    wednesday = 2
    late_start, _, _, weekdays = _plan([_item(1)], first_offset=wednesday)
    assert weekdays == [2, 3, 4, 5, 6] and late_start == {"Wed": ["1"]}

    thursday = 3
    not_early, _, _, _ = _plan([_item(1, thursday)])
    assert not_early == {"Thu": ["1"]}


@pytest.mark.parametrize(("opener", "expected"), [
    pytest.param(_no_network, None, id="network-error"),
    pytest.param(lambda url, timeout: b"not json", None, id="bad-json"),
    pytest.param(lambda url, timeout: json.dumps({"schemaVersion": 1, "numbers": [3, 1]}).encode(),
                 frozenset({1, 3}), id="ok"),
])
def test_fetch_site_numbers(opener, expected):
    assert bw.fetch_site_numbers("https://example.test/index.json", opener) == expected


def _config(tmp_path, weekly_build: bool) -> None:
    (tmp_path / "cse.config.yml").write_text(
        "timezone: UTC\nautomation:\n"
        f"  weekly_build: {'true' if weekly_build else 'false'}\n"
        "  build_lead_hours: 0\n  practice_index_url: https://example.test/i.json\n"
        "  prefer_practice_spec: true\n", encoding="utf-8")


def _files(root):
    return sorted(str(p.relative_to(root)) for p in root.rglob("*"))


def _main(tmp_path, *argv):
    return bw.main(list(argv), repo=tmp_path, opener=_no_network)


def test_main_no_config(tmp_path, capsys):
    assert _main(tmp_path, "--now", "2026-10-21T10:00") == 2
    assert "refused: no cse.config.yml — onboard first" in capsys.readouterr().out


def test_main_off_writes_nothing(tmp_path, capsys):
    _config(tmp_path, weekly_build=False)
    before = _files(tmp_path)
    assert _main(tmp_path, "--now", "2026-10-21T10:00") == 0
    assert "skipped: weekly build is off" in capsys.readouterr().out
    assert _files(tmp_path) == before


def test_main_file_exists(tmp_path, capsys):
    _config(tmp_path, weekly_build=True)
    live = tmp_path / bw.LIVE_DIR
    live.mkdir(parents=True)
    for stamp in ("20261019", "20261026"):
        (live / f"{stamp}_schedule.md").write_text("x", encoding="utf-8")
    before = _files(tmp_path)
    assert _main(tmp_path, "--now", "2026-10-25T23:30") == 0
    assert "skipped: 20261026_schedule.md exists" in capsys.readouterr().out
    assert _files(tmp_path) == before


def test_main_dry_run_writes_nothing(tmp_path, capsys):
    _config(tmp_path, weekly_build=False)
    before = _files(tmp_path)
    assert _main(tmp_path, "--dry-run", "--now", "2026-10-26T00:30") == 0
    assert "dry-run: 2026-10-26" in capsys.readouterr().out
    assert _files(tmp_path) == before


def test_main_week_bypasses_off_gate(tmp_path, capsys):
    _config(tmp_path, weekly_build=False)
    assert _main(tmp_path, "--week", "2026-10-26", "--now", "2026-10-21T10:00") == 0
    assert "built: 2026-10-26" in capsys.readouterr().out
    assert (tmp_path / bw.LIVE_DIR / "20261026_schedule.md").is_file()


def test_main_non_monday_week(tmp_path, capsys):
    _config(tmp_path, weekly_build=True)
    assert _main(tmp_path, "--week", "2026-10-21", "--now", "2026-10-21T10:00") == 2
    assert "is not a Monday" in capsys.readouterr().out
