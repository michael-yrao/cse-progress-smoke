"""Test for promote_report.read_declined.

Runnable two ways:
    python tests/test_promote_report.py
    pytest tests/test_promote_report.py
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from promote_report import DECLINED_PATH, read_declined  # noqa: E402

# (bullet line, path expected in the declined set or None)
CASES = (
    ("- `scripts/foo.py` — reason", "scripts/foo.py"),
    ("- `.githooks/pre-commit` — reason", ".githooks/pre-commit"),
    ("- docs/bar.md — reason", "docs/bar.md"),
    ("- `wedding-lite-oct18` — decision id", None),
    ("- `wedding_lite:` config block", None),
    ("see scripts/prose.py for details", None),
)


def test_read_declined_matches_paths_only() -> None:
    for line, expected in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            declined_file = root / DECLINED_PATH
            declined_file.parent.mkdir(parents=True)
            declined_file.write_text(line + "\n", encoding="utf-8")
            expected_set = {expected} if expected else set()
            assert read_declined(root) == expected_set, line


if __name__ == "__main__":
    test_read_declined_matches_paths_only()
    print("ok")
