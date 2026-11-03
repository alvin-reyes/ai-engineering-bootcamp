"""Your own deliverable, checked against the build brief. Skipped unless you ask for it:

    CHECK_FINAL=1 pytest tests/test_final_checklist.py

It reads YOUR docs/ and evalset/eval_set.jsonl (not the test fixtures).
"""
import os
from pathlib import Path

import pytest

from docsqa.evalrun import load_eval_set
from docsqa.ingest import load_documents

ROOT = Path(__file__).resolve().parent.parent
pytestmark = pytest.mark.skipif(os.environ.get("CHECK_FINAL") != "1", reason="set CHECK_FINAL=1 for the final check")


def test_at_least_five_documents():
    assert len(load_documents(ROOT / "docs")) >= 5


def test_thirty_cases_five_unanswerable():
    cases = load_eval_set(ROOT / "evalset" / "eval_set.jsonl")
    assert len(cases) >= 30
    assert sum(not c.answerable for c in cases) >= 5
