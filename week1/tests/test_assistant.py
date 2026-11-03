"""Acceptance tests for the Week 1 build. They run with no API key (see conftest.py).

These are the contract: when they all pass, your build meets the criteria. The build also asks for three tests of
your own, including a failure case: add them in tests/test_mine.py.
"""
import json
import pathlib

import pytest

from assistant import (Assistant, AssistantError, SUMMARY_SCHEMA, describe_error, get_api_key, text_of,
                       validate_summary)
from assistant.cli import handle
from conftest import api_error

GOOD = {"topic": "tokens", "key_points": ["a token is a piece of a word"], "open_questions": []}


def sent_roles(call):
    return [m["role"] for m in call["messages"]]


# ---- criterion 1: streams replies token by token ----
def test_streams_chunk_by_chunk(fake, make_assistant, chunks):
    fake.say("A token is a small piece of text.")
    reply = make_assistant().ask("What is a token?")
    assert fake.calls[0]["method"] == "stream"
    assert len(chunks) > 1                       # more than one chunk reached the screen
    assert "".join(chunks).strip() == "A token is a small piece of text."
    assert reply.text.strip() == "A token is a small piece of text."
    assert reply.stop_reason == "end_turn" and reply.truncated is False


# ---- criterion 2: keeps multi-turn history ----
def test_history_is_resent_every_turn(fake, make_assistant):
    fake.say("First answer.").say("Second answer.").say("Your first question was about tokens.")
    a = make_assistant()
    a.ask("question one about tokens")
    a.ask("question two")
    a.ask("What was my first question?")
    third = fake.calls[2]
    assert sent_roles(third) == ["user", "assistant", "user", "assistant", "user"]
    assert third["messages"][0]["content"] == "question one about tokens"
    assert text_of(third["messages"][1]["content"]).strip() == "First answer."
    assert len(a.history) == 6                   # three user turns and three assistant turns
    assert third["system"] and third["model"] and third["max_tokens"]


# ---- criterion 3: /summary is JSON valid against the schema ----
def test_summary_returns_valid_json_and_asks_for_the_schema(fake, make_assistant):
    fake.say("Tokens are pieces of words.").say(json.dumps(GOOD))
    a = make_assistant()
    a.ask("What is a token?")
    assert a.summary() == GOOD
    call = fake.calls[1]
    assert call["method"] == "create"
    assert call["output_config"] == {"format": {"type": "json_schema", "schema": SUMMARY_SCHEMA}}
    assert sent_roles(call) == ["user", "assistant", "user"]   # history plus the summary request


def test_summary_does_not_pollute_history(fake, make_assistant):
    fake.say("Hello.").say(json.dumps(GOOD))
    a = make_assistant()
    a.ask("hi")
    before = list(a.history)
    a.summary()
    assert a.history == before


def test_summary_with_no_conversation_is_a_clean_error(make_assistant):
    with pytest.raises(AssistantError):
        make_assistant().summary()


def test_validate_summary():
    assert validate_summary(GOOD) == []
    assert validate_summary({"topic": "x", "key_points": []})                              # missing key
    assert validate_summary({**GOOD, "key_points": "not a list"})                          # wrong type
    assert validate_summary({**GOOD, "key_points": [1, 2]})                                # wrong item type
    assert validate_summary({**GOOD, "extra": True})                                       # extra key
    assert validate_summary("not an object")


def test_summary_that_breaks_the_schema_is_an_error(fake, make_assistant):
    fake.say("Hi.").say(json.dumps({"topic": "only a topic"}))
    a = make_assistant()
    a.ask("hi")
    with pytest.raises(AssistantError):
        a.summary()


def test_summary_that_is_not_json_is_an_error(fake, make_assistant):
    fake.say("Hi.").say("Sure! Here is a summary: ...")
    a = make_assistant()
    a.ask("hi")
    with pytest.raises(AssistantError):
        a.summary()


# ---- criterion 4: a cut-off reply and API errors are handled cleanly ----
def test_cut_off_reply_is_flagged(fake, make_assistant, chunks):
    fake.say("The context window is everything the", stop="max_tokens")
    reply = make_assistant().ask("Explain the context window.", max_tokens=25)
    assert fake.calls[0]["max_tokens"] == 25
    assert reply.truncated is True and reply.stop_reason == "max_tokens"
    assert "cut off" in "".join(chunks)


def test_cut_off_summary_is_reported_not_parsed(fake, make_assistant):
    """The failure case: the summary hits max_tokens, so the JSON is half an object. Say so; do not crash."""
    fake.say("Hi.").say('{"topic": "tok', stop="max_tokens")
    a = make_assistant()
    a.ask("hi")
    with pytest.raises(AssistantError, match="cut off"):
        a.summary()


@pytest.mark.parametrize("kind, words", [("rate_limit", "rate limit"), ("bad_request", "400"), ("connection", "reach")])
def test_api_errors_become_one_clean_message(fake, make_assistant, kind, words):
    fake.fail(api_error(kind))
    a = make_assistant()
    with pytest.raises(AssistantError) as info:
        a.ask("hello")
    assert words in str(info.value).lower()
    assert a.history == []                       # the failed turn is not left in the history


def test_summary_api_error_is_clean(fake, make_assistant):
    fake.say("Hi.").fail(api_error("rate_limit"))
    a = make_assistant()
    a.ask("hi")
    with pytest.raises(AssistantError):
        a.summary()


def test_describe_error_tells_retry_from_fix():
    assert "rate limit" in describe_error(api_error("rate_limit")).lower()
    assert "400" in describe_error(api_error("bad_request"))
    assert describe_error(ValueError("x"))       # any other error still gets a sentence


# ---- criterion 5: the key comes from the environment, never from the repo ----
def test_key_from_environment():
    assert get_api_key({"ANTHROPIC_API_KEY": "from-env"}) == "from-env"


@pytest.mark.parametrize("env", [{}, {"ANTHROPIC_API_KEY": ""}])
def test_missing_key_names_the_variable(env):
    with pytest.raises(AssistantError, match="ANTHROPIC_API_KEY"):
        get_api_key(env)


def test_no_key_in_the_repo():
    root = pathlib.Path(__file__).resolve().parent.parent
    for path in list(root.rglob("*.py")) + list(root.rglob("*.md")) + list(root.rglob("*.txt")):
        if ".venv" in path.parts or path.name == "test_assistant.py":
            continue
        assert "sk-ant-" not in path.read_text(errors="ignore"), f"possible API key in {path.name}"
    assert not (root / ".env").exists() or ".env" in (root / ".gitignore").read_text()


# ---- the terminal loop ----
def test_handle_quit_and_blank(make_assistant):
    a = make_assistant()
    assert handle(a, "/quit") is False
    assert handle(a, "") is True


def test_handle_chat_line_asks_and_keeps_going(fake, make_assistant):
    fake.say("Hi there.")
    a = make_assistant()
    assert handle(a, "hello", out=lambda s: None) is True
    assert a.history[0] == {"role": "user", "content": "hello"}


def test_handle_summary_prints_json(fake, make_assistant):
    fake.say("Hi.").say(json.dumps(GOOD))
    a = make_assistant()
    a.ask("hi")
    printed = []
    assert handle(a, "/summary", out=printed.append) is True
    assert json.loads("".join(printed)) == GOOD


def test_handle_short_uses_a_tiny_max_tokens(fake, make_assistant):
    fake.say("The context", stop="max_tokens")
    a = make_assistant()
    handle(a, "/short Explain the context window.", out=lambda s: None)
    assert fake.calls[0]["max_tokens"] == 25
    assert a.history[0]["content"] == "Explain the context window."


def test_handle_never_crashes_on_an_api_error(fake, make_assistant):
    fake.fail(api_error("connection"))
    printed = []
    assert handle(make_assistant(), "hello", out=printed.append) is True
    assert "[error:" in "".join(printed)
