"""Week 2 demo: tool design. Same question, vague tools vs precise tools; then errors the model can act on.

    python tool_design.py            # part 1: which tool and arguments does the model pick?
    python tool_design.py --errors   # part 2: bad input comes back as is_error tool_results; the model recovers
    python tool_design.py --errors --terse   # part 2 again, but the error messages are useless ("Error.")
    DEMO_OFFLINE=1 python tool_design.py     # no key: canned responses show the mechanics only

Live, run part 1 a few times: the point is how often each version picks the right tool. Offline, the vague
version is scripted to go wrong so you can see what "wrong" looks like; that is not a measurement.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # the demos/ folder
from offline import get_client, reply, text, tool  # noqa: E402

MODEL = os.environ.get("DEMO_MODEL", "claude-opus-5-5")
ORDERS = {"ORD-1002": {"status": "delivered", "item": "27-inch monitor"},
          "ORD-1003": {"status": "in transit", "item": "Keyboard", "eta": "2026-11-04"}}
HELP = {"refunds": "Damaged items can be refunded within 30 days of delivery.",
        "shipping": "Standard shipping takes 3-5 business days.",
        "returns": "Unused items can be returned within 14 days."}

# BAD: vague names, vague descriptions, one free-text field each. The model has to guess.
VAGUE = [
    {"name": "search", "description": "Search for things.",
     "input_schema": {"type": "object", "properties": {"input": {"type": "string"}}}},
    {"name": "get", "description": "Get something.",
     "input_schema": {"type": "object", "properties": {"input": {"type": "string"}}}},
]
# GOOD: one job each, says when to use it and when not to, closed schema, enum for the topic.
PRECISE = [
    {"name": "get_order",
     "description": "Look up ONE order by id. Use for any question about a specific order's status or contents. "
                    "Order ids look like ORD-1234. Returns status, item and delivery date or ETA.",
     "input_schema": {"type": "object", "properties": {"order_id": {"type": "string"}},
                      "required": ["order_id"], "additionalProperties": False}},
    {"name": "search_help",
     "description": "Look up a help-center policy. Use for general policy questions. Not for questions about a "
                    "specific order.",
     "input_schema": {"type": "object",
                      "properties": {"topic": {"type": "string", "enum": ["refunds", "shipping", "returns"]}},
                      "required": ["topic"], "additionalProperties": False}},
]
# (question, right tool in the PRECISE set, right tool in the VAGUE set)
QUESTIONS = [("Where is ORD-1003?", "get_order", "get"),
             ("How long do I have to return an unused item?", "search_help", "search"),
             ("Is ORD-1002 delivered yet?", "get_order", "get")]


def part1_responder(kwargs, call_no):
    """Offline: the vague tool set goes wrong (it always picks `search`); the precise set goes right."""
    q = kwargs["messages"][0]["content"]
    names = [t["name"] for t in kwargs["tools"]]
    if "search" in names:
        return reply(tool("search", {"input": q}))
    found = re.search(r"ORD-\d+", q)
    if found:
        return reply(tool("get_order", {"order_id": found.group(0)}))
    return reply(tool("search_help", {"topic": "returns"}))


def part1(client):
    right = {"vague": 0, "precise": 0}
    for q, good_precise, good_vague in QUESTIONS:
        print(f"\nQ: {q}")
        for label, tools, good in (("vague", VAGUE, good_vague), ("precise", PRECISE, good_precise)):
            resp = client.messages.create(model=MODEL, max_tokens=300, tools=tools,
                                          messages=[{"role": "user", "content": q}])
            call = next((b for b in resp.content if b.type == "tool_use"), None)
            if call is None:
                print(f"  {label:8} -> no tool call (answered from nothing)")
                continue
            ok = call.name == good
            right[label] += ok
            print(f"  {label:8} -> {call.name}({json.dumps(call.input)})  {'right tool' if ok else 'WRONG/unclear'}")
    print(f"\nRight tool: vague {right['vague']}/{len(QUESTIONS)}, precise {right['precise']}/{len(QUESTIONS)}")


# ---- Part 2: errors the model can act on -------------------------------------------------------------------
# These tools are NOT strict on purpose, so bad input can reach our validation. (With strict tools the API
# keeps inputs schema-valid; wrong-but-valid values such as a missing order id still reach your code.)
SLOPPY = [dict(PRECISE[0], description="Look up one order by id (ORD-1234).")]


def run_get_order(args, terse):
    """Validate, then run. Returns (content, is_error). Good messages say what was wrong AND what is right."""
    if not isinstance(args.get("order_id"), str):
        keys = sorted(args)
        return ("Error." if terse else
                f"Invalid input: this tool needs 'order_id' (string like ORD-1234), got keys {keys}."), True
    oid = args["order_id"].strip().upper()
    if oid not in ORDERS:
        return ("Error." if terse else
                f"No order {args['order_id']!r}. Order ids look like ORD-1001 (prefix ORD-, then 4 digits)."), True
    return json.dumps({"order_id": oid, **ORDERS[oid]}), False


def part2_responder(kwargs, call_no):
    """Offline: wrong key -> wrong id format -> right call -> answer. With terse errors it gives up."""
    messages = kwargs["messages"]
    step = (len(messages) - 1) // 2
    if step == 0:
        return reply(text("Looking up the order."), tool("get_order", {"order": "1003"}))
    last = messages[-1]["content"][0]
    if last["is_error"] and last["content"] == "Error.":
        if step == 1:
            return reply(text("That failed. Trying again."), tool("get_order", {"order": "1003"}))
        return reply(text("I could not look up the order and I do not know why, so I cannot say where it is."))
    if step == 1:
        return reply(text("It wants order_id. Retrying with that key."), tool("get_order", {"order_id": "1003"}))
    if step == 2:
        return reply(text("Ids start with ORD-. Retrying."), tool("get_order", {"order_id": "ORD-1003"}))
    return reply(text("ORD-1003 (Keyboard) is in transit and should arrive on 2026-11-04."))


def part2(client, terse):
    messages = [{"role": "user", "content": "Where is order 1003?"}]
    for step in range(1, 6):
        resp = client.messages.create(model=MODEL, max_tokens=500, tools=SLOPPY, messages=messages)
        messages.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason != "tool_use":
            print(f"\nFinal: {next((b.text for b in resp.content if b.type == 'text'), '')}")
            return
        results = []
        for b in resp.content:
            if b.type != "tool_use":
                continue
            content, is_error = run_get_order(b.input, terse)
            print(f"step {step}: get_order({json.dumps(b.input)}) -> {'is_error=True ' if is_error else ''}{content}")
            results.append({"type": "tool_result", "tool_use_id": b.id, "content": content, "is_error": is_error})
        messages.append({"role": "user", "content": results})
    print("\n[stopped: step limit]")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--errors" in args:
        terse = "--terse" in args
        part2(get_client(part2_responder), terse)
    else:
        part1(get_client(part1_responder))
