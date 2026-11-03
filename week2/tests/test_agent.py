"""Acceptance criteria for the Week 2 build, as tests. They run with no API key (see conftest.py).

Each test names the criterion it checks. Read a failing test top to bottom: it says what is expected.
"""
import pytest

from conftest import reply, text, tool, tool_results

NAMES = {"get_order", "search_help", "draft_refund"}


# --- Criterion: three tools with strict schemas ----------------------------------------------------------------

def test_three_tools_with_the_expected_names(agent):
    assert {t["name"] for t in agent.TOOLS} == NAMES


@pytest.mark.parametrize("name", sorted(NAMES))
def test_each_schema_is_strict(agent, name):
    t = next(t for t in agent.TOOLS if t["name"] == name)
    schema = t["input_schema"]
    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False, "no extra fields allowed"
    assert schema["required"], "list the required fields"
    assert set(schema["required"]) <= set(schema["properties"]), "every required field must be a property"
    assert all(p.get("type") == "string" for p in schema["properties"].values())
    assert len(t["description"]) >= 40, "a description says when to use the tool, what it returns, what it is not for"


def test_every_tool_has_a_handler(agent):
    assert NAMES <= set(agent.HANDLERS)


def test_only_the_refund_is_a_write_tool(agent):
    assert set(agent.WRITE_TOOLS) == {"draft_refund"}


# --- Criterion: inputs validated in your code before any tool runs ---------------------------------------------

@pytest.mark.parametrize("bad_input, mentions", [
    ({}, "order_id"),                                          # missing
    ({"order_id": ""}, "order_id"),                            # empty
    ({"order_id": 1002}, "order_id"),                          # wrong type
    ({"order_id": "ORD-1002", "colour": "red"}, "colour"),     # extra field
])
def test_bad_input_is_rejected_before_the_handler_runs(agent, spies, yes, bad_input, mentions):
    block = tool("get_order", bad_input)
    from conftest import _block
    result = agent.run_tool(_block(block), approve=yes)
    assert result["type"] == "tool_result" and result["is_error"] is True
    assert mentions in result["content"], "the error must name the field the model got wrong"
    assert "get_order" not in spies, "the handler must not run on invalid input"


def test_validate_input_accepts_good_input_and_flags_unknown_tools(agent):
    assert agent.validate_input("get_order", {"order_id": "ORD-1002"}) is None
    assert "Unknown tool" in agent.validate_input("delete_everything", {})


def test_write_tool_input_is_validated_before_the_human_is_asked(agent, spies, yes):
    from conftest import _block
    result = agent.run_tool(_block(tool("draft_refund", {"order_id": "ORD-1002"})), approve=yes)  # no reason
    assert result["is_error"] is True and "reason" in result["content"]
    assert yes.prompts == [], "do not ask a human to approve a request that is not even valid"


# --- Criterion: a refund waits for a human "yes" ---------------------------------------------------------------

def _refund_call():
    from conftest import _block
    return _block(tool("draft_refund", {"order_id": "ORD-1002", "reason": "Arrived damaged"}))


def test_refund_asks_the_human_and_runs_only_after_yes(agent, spies, yes):
    result = agent.run_tool(_refund_call(), approve=yes)
    assert len(yes.prompts) == 1
    assert "ORD-1002" in yes.prompts[0] and "Arrived damaged" in yes.prompts[0], "show the human what they approve"
    assert result["is_error"] is False
    assert len(spies["draft_refund"]) == 1


@pytest.mark.parametrize("answer", ["n", "no", "", "maybe", "later"])
def test_anything_but_yes_declines(agent, spies, answer):
    from conftest import Approver
    result = agent.run_tool(_refund_call(), approve=Approver(answer))
    assert result["is_error"] is True and "declined" in result["content"].lower()
    assert "draft_refund" not in spies, "the write tool must not run without a yes"


@pytest.mark.parametrize("answer", ["y", "Y", "yes", " YES "])
def test_yes_in_any_common_spelling_approves(agent, spies, answer):
    from conftest import Approver
    assert agent.run_tool(_refund_call(), approve=Approver(answer))["is_error"] is False


def test_read_tools_never_ask_the_human(agent, yes):
    from conftest import _block
    agent.run_tool(_block(tool("get_order", {"order_id": "ORD-1002"})), approve=yes)
    agent.run_tool(_block(tool("search_help", {"query": "shipping times"})), approve=yes)
    assert yes.prompts == []


# --- Criterion: a step limit, and every tool call logged -------------------------------------------------------

def test_step_limit_stops_a_model_that_never_finishes(agent, make_client, yes):
    client = make_client(lambda kw, n: reply(text("again"), tool("get_order", {"order_id": "ORD-1001"})))
    out = agent.run_agent("Where is ORD-1001?", client=client, approve=yes, max_steps=3)
    assert len(client.calls) == 3
    assert "stopped" in out.lower() and "3" in out


def test_default_step_limit_is_a_small_number(agent):
    assert 1 <= agent.MAX_STEPS <= 15


def test_every_call_is_logged_with_input_result_and_time(agent, make_client, yes):
    log = []
    client = make_client([
        reply(tool("get_order", {"order_id": "ORD-1002"})),
        reply(tool("get_order", {"order_id": ""})),                    # invalid calls are logged too
        reply(text("done")),
    ])
    agent.run_agent("Status of ORD-1002?", client=client, approve=yes, log=log)
    assert [e["tool"] for e in log] == ["get_order", "get_order"]
    first, second = log
    assert first["input"] == {"order_id": "ORD-1002"} and "monitor" in first["result"]
    assert first["is_error"] is False and first["seconds"] >= 0
    assert second["is_error"] is True


# --- Criterion: bad tool input returns a useful error the model can act on --------------------------------------

def test_unknown_order_error_says_what_a_valid_id_looks_like(agent):
    content, is_error = agent.HANDLERS["get_order"](order_id="ORD-9999")
    assert is_error is True and "ORD-9999" in content and "ORD-1001" in content


def test_a_crashing_tool_becomes_an_error_result_not_a_crash(agent, monkeypatch, yes):
    from conftest import _block

    def boom(**kwargs):
        raise RuntimeError("database is down")
    monkeypatch.setitem(agent.HANDLERS, "get_order", boom)
    result = agent.run_tool(_block(tool("get_order", {"order_id": "ORD-1002"})), approve=yes)
    assert result["is_error"] is True and "database is down" in result["content"]


# --- Criterion: five scripted test conversations (incl. human says no, and a tool fails) -----------------------

def test_conversation_1_order_status(agent, make_client, yes):
    client = make_client([
        reply(text("Looking it up."), tool("get_order", {"order_id": "ORD-1003"})),
        reply(text("ORD-1003 is a keyboard, in transit, due 2026-11-04.")),
    ])
    out = agent.run_agent("Where is ORD-1003?", client=client, approve=yes)
    assert "in transit" in out
    (res,) = tool_results(client.calls[1])
    assert res["type"] == "tool_result" and "Keyboard" in res["content"]
    assert yes.prompts == []


def test_conversation_2_refund_approved(agent, make_client, yes):
    client = make_client([
        reply(tool("get_order", {"order_id": "ORD-1002"})),
        reply(tool("search_help", {"query": "refund policy"})),
        reply(tool("draft_refund", {"order_id": "ORD-1002", "reason": "Arrived damaged"})),
        reply(text("Your refund request was approved and queued.")),
    ])
    out = agent.run_agent("ORD-1002 arrived broken, refund please", client=client, approve=yes)
    assert "queued" in out
    assert len(yes.prompts) == 1
    (res,) = tool_results(client.calls[3])
    assert res["is_error"] is False and "queued" in res["content"]


def test_conversation_3_human_says_no(agent, make_client, no, spies):
    client = make_client([
        reply(tool("draft_refund", {"order_id": "ORD-1002", "reason": "Arrived damaged"})),
        reply(text("A human declined, so it needs review.")),
    ])
    out = agent.run_agent("Refund ORD-1002", client=client, approve=no)
    (res,) = tool_results(client.calls[1])
    assert res["is_error"] is True and "declined" in res["content"].lower()
    assert "draft_refund" not in spies
    assert "declined" in out


def test_conversation_4_a_tool_fails_and_the_model_recovers(agent, make_client, yes):
    client = make_client([
        reply(tool("get_order", {"order_id": "ORD-9999"})),
        reply(text("I could not find that order. Could you check the id?")),
    ])
    out = agent.run_agent("Where is ORD-9999?", client=client, approve=yes)
    (res,) = tool_results(client.calls[1])
    assert res["is_error"] is True and "ORD-9999" in res["content"]
    assert "check the id" in out


def test_conversation_5_invalid_input_then_a_corrected_retry(agent, make_client, yes):
    client = make_client([
        reply(tool("get_order", {"id": "ORD-1001"})),                 # wrong field name
        reply(tool("get_order", {"order_id": "ORD-1001"})),           # the model reads the error and fixes it
        reply(text("ORD-1001 is delivered.")),
    ])
    out = agent.run_agent("ORD-1001?", client=client, approve=yes)
    (first,) = tool_results(client.calls[1])
    (second,) = tool_results(client.calls[2])
    assert first["is_error"] is True and "order_id" in first["content"]
    assert second["is_error"] is False
    assert "delivered" in out


# --- The loop's message shapes (so a real model accepts the history) ---------------------------------------------

def test_two_tool_calls_in_one_turn_go_back_in_one_message(agent, make_client, yes):
    client = make_client([
        reply(tool("get_order", {"order_id": "ORD-1001"}), tool("search_help", {"query": "shipping"})),
        reply(text("ok")),
    ])
    agent.run_agent("two things", client=client, approve=yes)
    results = tool_results(client.calls[1])
    assistant = client.calls[1]["messages"][-2]
    assert assistant["role"] == "assistant"
    ids = [b.id for b in assistant["content"] if b.type == "tool_use"]
    assert [r["tool_use_id"] for r in results] == ids and len(ids) == 2


def test_the_model_sees_the_tools_and_a_system_prompt(agent, make_client, yes):
    client = make_client([reply(text("hi"))])
    assert agent.run_agent("hello", client=client, approve=yes) == "hi"
    call = client.calls[0]
    assert call["tools"] == agent.TOOLS and call["model"] == agent.MODEL
    assert call["system"] and call["max_tokens"] > 0
    assert call["messages"][0] == {"role": "user", "content": "hello"}
