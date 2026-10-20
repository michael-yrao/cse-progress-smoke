"""Every committed dashboard/*.json that has a schema validates against it.

Runnable two ways:
    python tests/test_dashboard_contract.py      # plain asserts, no pytest needed
    pytest tests/test_dashboard_contract.py

A payload `dashboard/<stem>.json` is checked against `dashboard/<stem>.schema.json`; a payload
with no such schema (progress-summary.json, schedule-history.json) is not covered here. The
schemas' cross-contract `$ref`s resolve from disk through `contract_schema`.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard"
sys.path.insert(0, str(ROOT / "scripts"))

import contract_schema  # noqa: E402

PAYLOAD_GLOB = "*.json"
SCHEMA_SUFFIX = ".schema.json"


def payloads_with_schema() -> list[tuple[Path, Path]]:
    """(payload, schema) for every dashboard/*.json whose `<stem>.schema.json` exists."""
    pairs = []
    for payload in sorted(DASHBOARD.glob(PAYLOAD_GLOB)):
        if payload.name.endswith(SCHEMA_SUFFIX):
            continue
        schema = DASHBOARD / f"{payload.stem}{SCHEMA_SUFFIX}"
        if schema.exists():
            pairs.append((payload, schema))
    return pairs


def violations(payload: Path, schema: Path) -> list[str]:
    """Schema violations of one payload, each prefixed with the payload's file name."""
    try:
        data = json.loads(payload.read_text(encoding="utf-8"))
        errors = contract_schema.validate(data, schema)
    except SystemExit as exc:  # jsonschema missing: fail with the install hint, never skip
        raise AssertionError(str(exc)) from None
    return [f"{payload.name}: {error}" for error in errors]


def test_every_dashboard_payload_matches_its_schema():
    failures = []
    for payload, schema in payloads_with_schema():
        failures.extend(violations(payload, schema))
    assert not failures, "dashboard contract violations:\n" + "\n".join(failures)


if __name__ == "__main__":
    test_every_dashboard_payload_matches_its_schema()
    print("All dashboard contract tests passed.")
