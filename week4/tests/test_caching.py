"""Criterion: Operate it. Stable prefix first, cache_control set, nothing that changes every call before the cache."""
from ops import tracing
from ops.caching import build_request, cache_hit_rate, find_volatile

STABLE = "You answer staff questions from the handbook. " + "Rule text. " * 400


def test_request_has_cache_control_and_the_stable_prefix_as_system():
    req = build_request(STABLE, "How many leave days?", model="m")
    assert req["cache_control"] == {"type": "ephemeral"}
    assert req["system"] == STABLE
    assert req["model"] == "m" and req["max_tokens"] > 0
    assert req["messages"][0]["role"] == "user" and "How many leave days?" in req["messages"][0]["content"]


def test_changing_data_goes_after_the_stable_part_not_into_it():
    a = build_request(STABLE, "q1", dynamic="Today is 2026-12-01 10:00. Request id 7f3a.")
    b = build_request(STABLE, "q2", dynamic="Today is 2026-12-02 11:30. Request id 9c21.")
    assert a["system"] == b["system"]                       # the cached part is byte-identical
    assert "2026-12-01" not in a["system"]
    assert "2026-12-01" in a["messages"][0]["content"]      # the dynamic text is still sent, at the end
    assert a["messages"][0]["content"].startswith("q1")


def test_extra_arguments_pass_through():
    tools = [{"name": "t", "description": "d", "input_schema": {"type": "object", "properties": {}}}]
    assert build_request(STABLE, "q", tools=tools)["tools"] == tools


def test_second_call_reads_from_the_cache(tmp_path, make_client):
    tr = tracing.Tracer(make_client(), path=tmp_path / "t.jsonl")
    for q in ("q1", "q2", "q3"):
        tr.call("ask", **build_request(STABLE, q, dynamic="now: 2026-12-01T10:00:00"))
    assert tr.rows[0]["cache_write"] > 0
    assert tr.rows[1]["cache_read"] > 0 and tr.rows[2]["cache_read"] > 0
    assert cache_hit_rate(tr.rows) > 0.5


def test_a_timestamp_in_the_prefix_breaks_the_cache(tmp_path, make_client):
    tr = tracing.Tracer(make_client(), path=tmp_path / "t.jsonl")
    for i in range(3):
        tr.call("ask", **build_request(STABLE + f"\nNow: 2026-12-01T10:00:0{i}", "q"))
    assert all(r["cache_read"] == 0 for r in tr.rows)
    assert cache_hit_rate(tr.rows) == 0


def test_find_volatile_spots_dates_times_and_ids():
    text = ("Policy v2. Generated 2026-12-01T10:00:00. Session 123e4567-e89b-12d3-a456-426614174000. "
            "Updated at 14:35.")
    found = find_volatile(text)
    assert any("2026-12-01" in f for f in found)
    assert any("123e4567" in f for f in found)
    assert any("14:35" in f for f in found)


def test_find_volatile_is_quiet_on_stable_text():
    assert find_volatile(STABLE) == []


def test_hit_rate_edges():
    assert cache_hit_rate([]) == 0
    assert cache_hit_rate([{"input_tokens": 0, "cache_read": 0, "cache_write": 0}]) == 0
    assert cache_hit_rate([{"input_tokens": 10, "cache_read": 90, "cache_write": 0}]) == 0.9
