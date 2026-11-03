"""Criterion: Ship it. The service answers /health and /ask, takes secrets only from the environment, fails safely.

Runs in-process: either by calling handle_ask directly, or on a free localhost port. No key, no network.
"""
import json
import threading
import urllib.error
import urllib.request
from types import SimpleNamespace as NS

import pytest

from deploy import app


@pytest.fixture
def server():
    srv = app.make_server(port=0)           # port 0 = the OS picks a free port
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()
    srv.server_close()


def call(url, data=None, headers=None, method=None):
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", **(headers or {})},
                                 method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def go_live(monkeypatch, client, token="t0ken"):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    if token:
        monkeypatch.setenv("ASK_TOKEN", token)
    app.set_client(client)


@pytest.fixture(autouse=True)
def reset_client():
    yield
    app.set_client(None)


def test_health_is_cheap_and_reports_the_version(server, monkeypatch, make_client):
    monkeypatch.setenv("APP_VERSION", "v7")
    client = make_client()
    app.set_client(client)
    status, body = call(server + "/health")
    assert status == 200 and body["status"] == "ok" and body["version"] == "v7" and body["mode"] == "offline"
    assert client.calls == []               # /health never calls the model


def test_ask_offline_needs_no_key(server):
    status, body = call(server + "/ask", {"question": "What is a health check?"})
    assert status == 200 and body["mode"] == "offline" and body["answer"]


def test_ask_get_form_works_too(server):
    status, body = call(server + "/ask?q=hello")
    assert status == 200 and body["answer"]


def test_bad_questions_are_rejected(server):
    assert call(server + "/ask", {"question": ""})[0] == 400
    assert call(server + "/ask", {"question": "   "})[0] == 400
    assert call(server + "/ask", {"question": 42})[0] == 400
    assert call(server + "/ask", {"nope": 1})[0] == 400
    assert call(server + "/ask", {"question": "x" * (app.MAX_QUESTION_CHARS + 1)})[0] == 413


def test_unknown_paths_are_404(server):
    assert call(server + "/admin")[0] == 404
    assert call(server + "/admin", {"a": 1})[0] == 404


def test_live_mode_refuses_without_a_token(monkeypatch, make_client):
    go_live(monkeypatch, make_client(), token=None)
    status, body = app.handle_ask("hello", None)
    assert status == 503 and "ASK_TOKEN" in body["error"]


def test_live_mode_checks_the_bearer_token(monkeypatch, make_client):
    client = make_client()
    go_live(monkeypatch, client)
    assert app.handle_ask("hello", None)[0] == 401
    assert app.handle_ask("hello", "Bearer wrong")[0] == 401
    assert client.calls == []               # a refused caller costs nothing
    status, body = app.handle_ask("hello", "Bearer t0ken")
    assert status == 200 and body["mode"] == "live"


def test_live_answer_comes_from_the_model_and_reports_usage(monkeypatch, make_client, blocks):
    client = make_client(replies=[[blocks.text("Forty-two.")]])
    go_live(monkeypatch, client)
    status, body = app.handle_ask("What is the answer?", "Bearer t0ken")
    assert status == 200 and body["answer"] == "Forty-two."
    assert body["usage"]["input_tokens"] > 0 and body["usage"]["output_tokens"] == 20
    call_kwargs = client.calls[0]
    assert call_kwargs["max_tokens"] == app.MAX_TOKENS and call_kwargs["system"]
    assert call_kwargs["messages"] == [{"role": "user", "content": "What is the answer?"}]


def test_model_failure_is_a_502_that_leaks_nothing(monkeypatch, make_client):
    go_live(monkeypatch, make_client(fail=RuntimeError("sk-ant-SECRET upstream said no")))
    status, body = app.handle_ask("hello", "Bearer t0ken")
    assert status == 502
    assert "sk-ant" not in json.dumps(body) and "upstream" not in json.dumps(body)


def test_token_works_over_http_and_the_key_is_never_echoed(server, monkeypatch, make_client):
    go_live(monkeypatch, make_client())
    assert call(server + "/ask", {"question": "hi"})[0] == 401
    status, body = call(server + "/ask", {"question": "hi"}, headers={"Authorization": "Bearer t0ken"})
    assert status == 200
    assert "test-key-not-real" not in json.dumps(body) and "t0ken" not in json.dumps(body)


def test_one_json_log_line_per_request_and_no_question_text(server, capsys):
    call(server + "/ask", {"question": "PRIVATE-QUESTION-TEXT"})
    call(server + "/health")
    out = capsys.readouterr().out
    lines = [json.loads(ln) for ln in out.splitlines() if ln.startswith("{")]
    reqs = [ln for ln in lines if ln.get("path") in ("/ask", "/health")]
    assert len(reqs) == 2 and all({"status", "ms", "path"} <= set(r) for r in reqs)
    assert "PRIVATE-QUESTION-TEXT" not in out
