"""pytest fixtures for tests written to also run as plain scripts (see test_coach_sync.py)."""
from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def tmp(tmp_path: Path) -> Path:
    """A not-yet-created scratch directory, as test_coach_sync.main() passes
    (`Path(tempdir) / "a"`): each test makes whatever it needs beneath it."""
    return tmp_path / "scratch"
