"""Week 2 demo: a support agent with three tools, the agent loop, and guardrails.

    python support_agent.py "Where is my order ORD-1002, and can I get a refund? It arrived broken."
    python support_agent.py --yes "..."    # answer the approval prompt "y" for you (scripted runs, tests)
    python support_agent.py --no  "..."    # answer it "n" (shows the "a human declined" path)
    DEMO_OFFLINE=1 python support_agent.py "..."   # no key needed: a scripted model walks the same loop

Tools run on fake local data. draft_refund never refunds anything: it drafts a request and asks YOU to approve it.
With no ANTHROPIC_API_KEY (or DEMO_OFFLINE=1) a canned responder plays the model: it shows the mechanics (loop,
tool results, the approval gate), not real model behaviour. See ../offline.py.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # the demos/ folder
from offline import get_client, reply, text, tool  # noqa: E402

MODEL = os.environ.get("DEMO_MODEL", "claude-opus-5-5")
MAX_STEPS = 8

ORDERS = {
    "ORD-1001": {"status": "delivered", "item": "USB-C dock", "delivered_on": "2026-10-28"},
    "ORD-1002": {"status": "delivered", "item": "27-inch monitor", "delivered_on": "2026-10-30"},
    "ORD-1003": {"status": "in transit", "item": "Keyboard", "eta": "2026-11-04"},
}
HELP_DOCS = {
    "refunds": "Damaged items can be refunded within 30 days of delivery. A photo of the damage is required.",
    "shipping": "Standard shipping takes 3-5 business days. Tracking updates once a day.",
    "returns": "Unused items can be returned within 14 days. The customer pays return shipping.",
}

TOOLS = [
    {
        "name": "get_order",
        "description": "Look up one order by id. Use for any question about an order's status or contents. "
                       "Order ids look like ORD-1234.",
        "input_schema": {"type": "object", "properties": {"order_id": {"type": "string"}},
                         "required": ["order_id"], "additionalProperties": False},
        "strict": True,
    },
    {
        "name": "search_help",
        "description": "Search the help center for policy questions (refunds, shipping, returns). "
                       "Not for questions about a specific order.",
        "input_schema": {"type": "object", "properties": {"query": {"type": "string"}},
                         "required": ["query"], "additionalProperties": False},
        "strict": True,
    },
    {
        "name": "draft_refund",
        "description": "Draft a refund request for a human to approve. Only after checking the order and the "
                       "refund policy. Does not refund anything by itself.",
        "input_schema": {"type": "object",
                         "properties": {"order_id": {"type": "string"}, "reason": {"type": "string"}},
                         "required": ["order_id", "reason"], "additionalProperties": False},
        "strict": True,
    },
]
SYSTEM = ("You are a support agent for an electronics shop. Use the tools to answer; never guess order details "
          "or policy. If a refund looks justified, draft it with draft_refund; a human approves it.")


def get_order(order_id):
    order = ORDERS.get(order_id.strip().upper())
    if order is None:
        return f"No order {order_id!r}. Order ids look like ORD-1001.", True
    return json.dumps({"order_id": order_id, **order}), False


def search_help(query):
    hits = [text for topic, text in HELP_DOCS.items() if topic.rstrip("s") in query.lower()]
    return (json.dumps(hits), False) if hits else ("No help article matched. Try: refunds, shipping, returns.", True)


def draft_refund(order_id, reason, approve=input):
    print(f"\n  [APPROVAL NEEDED] refund request for {order_id}: {reason}")
    if approve("  approve? (y/n) ").strip().lower() != "y":
        return "A human declined this refund request. Tell the customer it needs review.", True
    return f"Refund request for {order_id} approved by a human and queued.", False


HANDLERS = {"get_order": get_order, "search_help": search_help, "draft_refund": draft_refund}


def run_tool(block, approve=input):
    """Validate, run, and wrap one tool call as a tool_result."""
    schema = next(t["input_schema"] for t in TOOLS if t["name"] == block.name)
    args = block.input
    missing = [k for k in schema["required"] if not isinstance(args.get(k), str) or not args[k].strip()]
    extra = [k for k in args if k not in schema["properties"]]
    if missing or extra:
        content, is_error = f"Invalid input: missing {missing}, unexpected {extra}.", True
    elif block.name == "draft_refund":
        content, is_error = draft_refund(**args, approve=approve)
    else:
        content, is_error = HANDLERS[block.name](**args)
    print(f"  [tool] {block.name}({json.dumps(args)}) -> {'ERROR ' if is_error else ''}{content[:80]}")
    return {"type": "tool_result", "tool_use_id": block.id, "content": content, "is_error": is_error}


def scripted_responder(kwargs, call_no):
    """Offline stand-in for the model: get_order -> search_help -> draft_refund -> final answer."""
    messages = kwargs["messages"]
    question = messages[0]["content"]
    found = re.search(r"ORD-\d+", question.upper())
    order_id = found.group(0) if found else None
    wants_refund = "refund" in question.lower()
    step = (len(messages) - 1) // 2          # how many tool rounds are already in the history
    last = messages[-1]["content"]
    last_result = last[0] if isinstance(last, list) else None
    if step == 0:
        if order_id is None:
            return reply(text("I need an order id (like ORD-1002) to look that up. What is it?"))
        return reply(text(f"I will look up {order_id} first."), tool("get_order", {"order_id": order_id}))
    if step == 1:
        if last_result["is_error"]:
            return reply(text(f"I could not find that order. {last_result['content']} Could you check the id?"))
        if not wants_refund:
            o = json.loads(last_result["content"])
            when = o.get("delivered_on") or o.get("eta")
            return reply(text(f"{order_id} ({o['item']}) is {o['status']} ({when})."))
        return reply(text("The order is delivered. Now the refund policy."),
                     tool("search_help", {"query": "refund policy for damaged items"}))
    if step == 2:
        return reply(text("Damaged items are refundable within 30 days of delivery. Drafting the request."),
                     tool("draft_refund", {"order_id": order_id, "reason": "Arrived damaged, within the 30-day refund window"}))
    if last_result["is_error"]:
        return reply(text(f"I have not refunded {order_id}: a human reviewer declined the request, so it needs "
                          "review. I will let the team follow up with you."))
    return reply(text(f"Your order {order_id} was delivered and the item arrived damaged. That is inside the "
                      "30-day window, so I drafted a refund request, a human approved it and it is queued. "
                      "Please send a photo of the damage."))


def run_agent(question, client=None, approve=input):
    client = client or get_client(scripted_responder)
    messages = [{"role": "user", "content": question}]
    for _ in range(MAX_STEPS):
        resp = client.messages.create(model=MODEL, max_tokens=4096, system=SYSTEM, tools=TOOLS, messages=messages)
        messages.append({"role": "assistant", "content": resp.content})  # append, never edit
        if resp.stop_reason != "tool_use":
            return next((b.text for b in resp.content if b.type == "text"), "")
        results = [run_tool(b, approve) for b in resp.content if b.type == "tool_use"]
        messages.append({"role": "user", "content": results})  # all results, one message
    return f"[stopped after {MAX_STEPS} steps]"


def scripted_approve(answer):
    """An approve() that prints the prompt and answers for you, so a demo or test needs no keyboard."""
    def approve(prompt):
        print(f"{prompt}{answer}   (scripted)")
        return answer
    return approve


if __name__ == "__main__":
    args = sys.argv[1:]
    approve = input
    for flag, answer in (("--yes", "y"), ("--no", "n")):
        if flag in args:
            args.remove(flag)
            approve = scripted_approve(answer)
    print(run_agent(" ".join(args) or "Where is ORD-1003?", approve=approve))
