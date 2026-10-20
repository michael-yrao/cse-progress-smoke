"""Round-trip tests for the .history stash (new_problem.py + restore_history.py).

Runnable two ways:
    python tests/test_history_stash.py   # plain asserts, no pytest needed
    pytest tests/test_history_stash.py

Covers the retry lifecycle:
  1. A retry moves the prior attempt OUT of the file into <root>/.history/<n>_<name>.txt,
     leaving a blank stub on top and a pointer at the bottom (the spoiler is gone from disk).
  2. restore_history.py KEEPS the stash out while today's stub is still un-attempted
     (`pass`) — pasting it back would expose the old solution before the rep.
  3. Once today's attempt has a real body, restore pastes the history back and clears
     the stash, reconstructing the single file with full dated history.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
TEMPLATE = (
    Path(__file__).resolve().parents[1]
    / "docs/foundations/dsa/templates/solution_template.py"
)
STAMP = datetime.now().strftime("%Y%m%d")
SOLUTION = "dsa/leetcode/arrays_and_hash/1_two_sum.py"
STASH = "dsa/leetcode/.history/1_two_sum.txt"


def _repo(tmp_path: Path) -> Path:
    """A minimal repo laid out the way the scripts expect (template + source root)."""
    repo = tmp_path / "repo"
    (repo / "docs/foundations/dsa/templates").mkdir(parents=True)
    (repo / "dsa/leetcode").mkdir(parents=True)
    shutil.copy(TEMPLATE, repo / "docs/foundations/dsa/templates/solution_template.py")
    return repo


def _run(script: str, repo: Path, *args: str) -> subprocess.CompletedProcess:
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"{script} failed:\n{result.stderr}"
    return result


def _new(repo: Path, *extra: str) -> None:
    _run(
        "new_problem.py", repo,
        "--number", "1", "--title", "Two Sum", "--pattern", "arrays_and_hash",
        "--method", "twoSum", *extra,
    )


def _write_body_under_today(repo: Path) -> None:
    """Replace the `pass` in today's dated stub with a real return (simulate the rep)."""
    f = repo / SOLUTION
    lines = f.read_text(encoding="utf-8").splitlines()
    start = next(i for i, ln in enumerate(lines) if f"twoSum_{STAMP}" in ln)
    body = next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "pass")
    lines[body] = "        return [0, 1]  # today's attempt"
    f.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_retry_extracts_prior_to_stash(tmp_path: Path):
    repo = _repo(tmp_path)
    _new(repo, "--signature", "nums: List[int], target: int -> List[int]")
    # A real prior attempt worth hiding.
    f = repo / SOLUTION
    f.write_text(f.read_text(encoding="utf-8") + "\n        seen = {}\n        return []\n",
                 encoding="utf-8")

    _new(repo)  # retry

    text = (repo / SOLUTION).read_text(encoding="utf-8")
    assert (repo / STASH).exists(), "prior attempt should be stashed"
    assert f"twoSum_{STAMP}" in text, "today's dated stub goes on top"
    assert "prior attempts stashed" in text, "pointer breadcrumb left behind"
    # The spoiler is physically gone from the working file.
    assert "seen = {}" not in text, "prior body must not remain in the file"
    assert "seen = {}" in (repo / STASH).read_text(encoding="utf-8")


def test_restore_keeps_unattempted_stash_out(tmp_path: Path):
    repo = _repo(tmp_path)
    _new(repo, "--signature", "nums: List[int], target: int -> List[int]")
    f = repo / SOLUTION
    f.write_text(f.read_text(encoding="utf-8") + "\n        seen = {}\n        return []\n",
                 encoding="utf-8")
    _new(repo)  # retry — today's stub is still `pass`

    _run("restore_history.py", repo)  # session end, but the rep was never written

    assert (repo / STASH).exists(), "un-attempted retry must keep its stash out"
    assert "seen = {}" not in (repo / SOLUTION).read_text(encoding="utf-8")


def test_restore_reunites_history_after_real_attempt(tmp_path: Path):
    repo = _repo(tmp_path)
    _new(repo, "--signature", "nums: List[int], target: int -> List[int]")
    f = repo / SOLUTION
    f.write_text(f.read_text(encoding="utf-8") + "\n        seen = {}\n        return []\n",
                 encoding="utf-8")
    _new(repo)  # retry
    _write_body_under_today(repo)  # the rep gets written

    _run("restore_history.py", repo)

    text = (repo / SOLUTION).read_text(encoding="utf-8")
    assert not (repo / STASH).exists(), "stash is consumed on restore"
    assert "return [0, 1]" in text, "today's attempt stays"
    assert "seen = {}" in text, "prior history is pasted back"
    assert "prior attempts stashed" not in text, "pointer is stripped"


def _run_all() -> None:
    import tempfile

    for test in (
        test_retry_extracts_prior_to_stash,
        test_restore_keeps_unattempted_stash_out,
        test_restore_reunites_history_after_real_attempt,
    ):
        with tempfile.TemporaryDirectory() as d:
            test(Path(d))
    print("All history-stash tests passed.")


if __name__ == "__main__":
    _run_all()
