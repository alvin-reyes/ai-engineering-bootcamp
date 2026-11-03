"""Criterion: Operate it. One JSON line per model call; cost per request and median latency can be read from it."""
import json
from types import SimpleNamespace as NS

import pytest

from ops import tracing
from ops.summary import format_summary, read_traces, summarize

KEYS = {"call", "task", "model", "latency_ms", "input_tokens", "output_tokens", "cache_write", "cache_read",
        "stop_reason", "cost_usd"}


def usage(i=0, o=0, w=0, r=0):
    return NS(input_tokens=i, output_tokens=o, cache_creation_input_tokens=w, cache_read_input_tokens=r)


def test_prices_are_labelled_as_examples():
    src = open(tracing.__file__).read()
    for name in ("PRICE_INPUT", "PRICE_OUTPUT", "PRICE_CACHE_WRITE", "PRICE_CACHE_READ"):
        line = next(ln for ln in src.splitlines() if ln.startswith(name))
        assert "VERIFY" in line, f"{name} must be labelled VERIFY (example price)"


def test_estimate_cost_uses_the_four_prices():
    u = usage(1_000_000, 1_000_000, 1_000_000, 1_000_000)
    want = tracing.PRICE_INPUT + tracing.PRICE_OUTPUT + tracing.PRICE_CACHE_WRITE + tracing.PRICE_CACHE_READ
    assert tracing.estimate_cost(u) == pytest.approx(want)


def test_estimate_cost_missing_fields_count_as_zero():
    assert tracing.estimate_cost(NS(input_tokens=1000, output_tokens=None)) == pytest.approx(
        1000 * tracing.PRICE_INPUT / 1_000_000)


def test_one_json_line_per_call(tmp_path, make_client, capsys):
    path = tmp_path / "t.jsonl"
    tr = tracing.Tracer(make_client(delay=0.02), path=path)
    for i in range(3):
        tr.call(f"task{i}", model="m", max_tokens=10, messages=[{"role": "user", "content": "hi"}])
    lines = path.read_text().splitlines()
    assert len(lines) == 3
    row = json.loads(lines[0])
    assert KEYS <= set(row)
    assert row["call"] == 1 and row["task"] == "task0" and row["model"] == "m"
    assert row["latency_ms"] >= 15
    assert row["output_tokens"] == 20 and row["stop_reason"] == "end_turn"
    assert row["cost_usd"] > 0
    assert len(tr.rows) == 3


def test_trace_line_has_no_prompt_text(tmp_path, make_client):
    path = tmp_path / "t.jsonl"
    tracing.Tracer(make_client(), path=path).call(
        "t", model="m", max_tokens=10, messages=[{"role": "user", "content": "PRIVATE-QUESTION-TEXT"}])
    assert "PRIVATE-QUESTION-TEXT" not in path.read_text()


def test_a_failed_call_is_traced_and_reraised(tmp_path, make_client):
    path = tmp_path / "t.jsonl"
    tr = tracing.Tracer(make_client(fail=TimeoutError("boom")), path=path)
    with pytest.raises(TimeoutError):
        tr.call("t", model="m", max_tokens=10, messages=[])
    row = json.loads(path.read_text().splitlines()[0])
    assert row["error"] == "TimeoutError" and row["cost_usd"] == 0.0 and row["latency_ms"] >= 0
    assert "boom" not in path.read_text()


def test_cache_numbers_appear_on_repeat_calls(tmp_path, make_client):
    tr = tracing.Tracer(make_client(), path=tmp_path / "t.jsonl")
    kw = dict(model="m", max_tokens=10, cache_control={"type": "ephemeral"}, system="S" * 4000,
              messages=[{"role": "user", "content": "q"}])
    tr.call("a", **kw)
    tr.call("b", **kw)
    assert tr.rows[0]["cache_write"] > 0 and tr.rows[0]["cache_read"] == 0
    assert tr.rows[1]["cache_read"] > 0 and tr.rows[1]["cache_write"] == 0


def test_tracer_returns_the_response(tmp_path, make_client, blocks):
    tr = tracing.Tracer(make_client(replies=[[blocks.text("hello")]]), path=tmp_path / "t.jsonl")
    r = tr.call("t", model="m", max_tokens=10, messages=[])
    assert r.content[0].text == "hello"


def rows(*specs):
    return [{"call": i, "task": t, "latency_ms": ms, "cost_usd": c, **extra}
            for i, (t, ms, c, extra) in enumerate(specs, 1)]


def test_summary_cost_per_request_and_median():
    s = summarize(rows(("a", 100, 0.01, {}), ("b", 300, 0.03, {}), ("c", 200, 0.02, {})))
    assert s["calls"] == 3 and s["requests"] == 3
    assert s["cost_total"] == pytest.approx(0.06)
    assert s["cost_per_request"] == pytest.approx(0.02)
    assert s["median_latency_ms"] == 200 and s["max_latency_ms"] == 300 and s["slowest_task"] == "b"


def test_summary_median_of_an_even_count():
    s = summarize(rows(("a", 100, 0, {}), ("b", 200, 0, {}), ("c", 300, 0, {}), ("d", 400, 0, {})))
    assert s["median_latency_ms"] == 250


def test_summary_groups_calls_into_requests():
    s = summarize(rows(("plan", 100, 0.01, {"request_id": "r1"}), ("answer", 200, 0.02, {"request_id": "r1"}),
                       ("plan", 50, 0.01, {"request_id": "r2"})))
    assert s["calls"] == 3 and s["requests"] == 2
    assert s["cost_per_request"] == pytest.approx(0.02)
    assert s["max_latency_ms"] == 300 and s["median_latency_ms"] == pytest.approx(175)


def test_summary_projection_and_errors():
    s = summarize(rows(("a", 100, 0.01, {}), ("b", 100, 0.0, {"error": "TimeoutError"})), per_day=1000)
    assert s["errors"] == 1
    assert s["projected_per_day"] == pytest.approx(5.0)
    assert s["projected_30_days"] == pytest.approx(150.0)


def test_summary_of_nothing_does_not_crash():
    s = summarize([])
    assert s["calls"] == 0 and s["cost_per_request"] == 0 and s["median_latency_ms"] == 0


def test_summary_reads_a_trace_file_and_prints(tmp_path, make_client):
    path = tmp_path / "t.jsonl"
    tr = tracing.Tracer(make_client(), path=path)
    tr.call("t", model="m", max_tokens=10, messages=[{"role": "user", "content": "hi"}])
    s = summarize(read_traces(path))
    assert s["calls"] == 1
    out = format_summary(s)
    assert "per request" in out and "median" in out
    assert "example" in format_summary(summarize(read_traces(path), per_day=10)).lower()
    assert tr.summary()["calls"] == 1
