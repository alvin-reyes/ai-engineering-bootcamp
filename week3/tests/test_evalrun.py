"""Acceptance: an eval set file; recall@k and answer accuracy are reported."""
import json

import pytest

from conftest import FakeClient
from docsqa.evalrun import EvalCase, load_eval_set, recall_at_k, run_eval
from docsqa.retrieve import Retriever


def test_load_eval_set(eval_path):
    cases = load_eval_set(eval_path)
    assert len(cases) >= 8
    assert all(isinstance(c, EvalCase) for c in cases)
    unanswerable = [c for c in cases if not c.answerable]
    assert len(unanswerable) >= 2
    assert all(c.source is None and c.must_contain is None for c in unanswerable)
    first = cases[0]
    assert first.answerable and first.source == "returns.md" and first.must_contain == "30 days"


def test_load_skips_blank_lines(tmp_path):
    p = tmp_path / "e.jsonl"
    p.write_text(json.dumps({"id": "a", "question": "q?", "answerable": False}) + "\n\n")
    cases = load_eval_set(p)
    assert len(cases) == 1 and cases[0].source is None


def test_recall_at_k_counts_only_answerable(retriever, eval_path):
    cases = load_eval_set(eval_path)
    assert recall_at_k(cases, retriever, 5) == 1.0
    assert 0.0 < recall_at_k(cases, retriever, 1) <= 1.0


def test_recall_is_a_fraction(chunks):
    r = Retriever(chunks)
    cases = [
        EvalCase("a", "How many days to return an unused bike?", True, "returns.md", "30 days"),
        EvalCase("b", "How many days to return an unused bike?", True, "warranty.md", "x"),  # wrong source on purpose
        EvalCase("c", "anything?", False, None, None),  # ignored
    ]
    assert recall_at_k(cases, r, 1) == 0.5


def test_run_eval_reports_accuracy_and_failures(retriever, eval_path, fake_client):
    cases = load_eval_set(eval_path)
    result = run_eval(cases, retriever, fake_client, k=5)
    assert result["n"] == len(cases)
    assert result["recall_at_k"] == 1.0
    assert result["accuracy"] >= 0.8
    assert isinstance(result["failures"], list)


def test_unanswerable_case_is_wrong_if_the_system_answers(retriever):
    always_cites = FakeClient(lambda prompt: "Sure. " + "[" + prompt.split('<chunk id="')[1].split('"')[0] + "]")
    cases = [EvalCase("u", "What is the CEO's salary and bike?", False, None, None)]
    result = run_eval(cases, retriever, always_cites, k=5)
    assert result["accuracy"] == 0.0 and result["failures"] == ["u"]


def test_answerable_case_needs_phrase_and_right_source(retriever, fake_client):
    good = EvalCase("g", "How many days do customers have to return an unused bike?", True, "returns.md", "30 days")
    wrong_phrase = EvalCase("p", "How many days do customers have to return an unused bike?", True, "returns.md", "99 days")
    wrong_source = EvalCase("s", "How many days do customers have to return an unused bike?", True, "warranty.md", "30 days")
    result = run_eval([good, wrong_phrase, wrong_source], retriever, fake_client, k=5)
    assert result["accuracy"] == pytest.approx(1 / 3)
    assert result["failures"] == ["p", "s"]
