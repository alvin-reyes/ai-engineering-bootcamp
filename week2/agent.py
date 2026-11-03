"""Week 2 build: a support agent with three tools. STARTER: fill in every `# TODO:`.

    python agent.py "Where is ORD-1002? It arrived broken, can I get a refund?"   # needs ANTHROPIC_API_KEY
    python agent.py --yes "..."     # answers the approval prompt "y" for you
    python agent.py --no  "..."     # answers it "n"
    pytest                          # no key needed: a scripted fake model plays the model

The data is fake and local. The point is the loop, the schemas and the guardrails, not the integrations.
You may change the shop, the tool names and the data to your own idea, but then update the tests' expectations in
a copy; the grader's tests use the names below. Explain every line you keep.

The contract the tests rely on (keep these names):
    TOOLS         list of tool definitions (what the model sees)
    HANDLERS      {tool name: function(**args) -> (content, is_error)}; run_tool must look a handler up in this
                  dict at call time, not keep its own copy
    WRITE_TOOLS   names of tools that change something; they need a human "yes" first
    MODEL, MAX_STEPS
    validate_input(name, args) -> None or an error message
    run_tool(block, approve, log) -> one tool_result dict
    run_agent(question, client, approve, max_steps, log) -> the final answer text
"""
import json
import os
import sys
import time

MODEL = os.environ.get("AGENT_MODEL", "claude-opus-5-5")  # VERIFY: use the model id your cohort was given
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
SYSTEM = ("You are a support agent for an electronics shop. Use the tools to answer; never guess order details "
          "or policy. If a refund looks justified, draft it with draft_refund; a human approves it.")

# ---------------------------------------------------------------------------------------------------------------
# 1. Tool definitions: exactly three, with strict schemas.
# ---------------------------------------------------------------------------------------------------------------

# TODO: define three tools: get_order(order_id), search_help(query), draft_refund(order_id, reason).
# Each one is a dict shaped like this (see readings/week2/02-tool-design.md for the six rules):
#     {
#         "name": "get_order",
#         "description": "<when to use it, what it returns, what it is NOT for>",
#         "input_schema": {"type": "object",
#                          "properties": {"order_id": {"type": "string"}},
#                          "required": ["order_id"],
#                          "additionalProperties": False},     # strict: no extra fields
#         "strict": True,
#     }
# The refund tool's description must say it only DRAFTS and that a human approves.
TOOLS: list = []

WRITE_TOOLS = ()  # TODO: the names of the tools that change something (they need a human yes)


# ---------------------------------------------------------------------------------------------------------------
# 2. The tools themselves. Each returns (content, is_error). Errors are written for the MODEL to act on.
# ---------------------------------------------------------------------------------------------------------------

def get_order(order_id):
    """Look up one order. Return (json string, False) or (an error that shows what a valid id looks like, True)."""
    # TODO: look the id up in ORDERS (ignore case and spaces). Unknown id -> error mentioning ORD-1001 as an example.
    raise NotImplementedError("TODO: get_order")


def search_help(query):
    """Find help articles whose topic appears in the query. Return (json list of articles, False) or (hint, True)."""
    # TODO: match the query against HELP_DOCS topics; no match -> an error that lists the topics to try.
    raise NotImplementedError("TODO: search_help")


def draft_refund(order_id, reason):
    """Record a refund DRAFT for a delivered order. It never moves money. Runs only after a human said yes."""
    # TODO: unknown order -> error. Otherwise return a message saying the request is queued for processing.
    raise NotImplementedError("TODO: draft_refund")


HANDLERS = {
    # TODO: map each tool name to its function.
}


# ---------------------------------------------------------------------------------------------------------------
# 3. Guardrails: validate the input, gate the write tool, log every call.
# ---------------------------------------------------------------------------------------------------------------

def validate_input(name, args):
    """Check a tool call BEFORE running anything. Return None if fine, else an error message for the model.

    Catch: unknown tool name; args that are not a dict; a missing required field; a field that is not a
    non-empty string; any field the schema does not list. Say which field is wrong and what is expected.
    """
    # TODO
    raise NotImplementedError("TODO: validate_input")


def ask_human(approve, name, args):
    """Show the human exactly what they would approve, and return True only for a yes ("y" or "yes")."""
    # TODO: build a prompt with the tool name and its arguments; call approve(prompt); anything else is a no.
    raise NotImplementedError("TODO: ask_human")


def run_tool(block, approve=input, log=None):
    """Validate, gate, run and wrap ONE tool call (block has .id, .name, .input) as a tool_result dict.

    Order of work: validate -> (write tools only) ask the human -> run the handler -> log -> return.
    Never let an exception escape: a crashing tool becomes an is_error result the model can read.
    Declined by the human -> is_error result containing the word "declined".
    Log one dict per call to `log` (a list; use a module-level list if None):
        {"tool": ..., "input": ..., "result": ..., "is_error": ..., "seconds": ...}
    Result shape: {"type": "tool_result", "tool_use_id": block.id, "content": str, "is_error": bool}
    """
    # TODO
    raise NotImplementedError("TODO: run_tool")


# ---------------------------------------------------------------------------------------------------------------
# 4. The agent loop.
# ---------------------------------------------------------------------------------------------------------------

CALL_LOG: list = []


def run_agent(question, client, approve=input, max_steps=MAX_STEPS, log=None):
    """Ask the model, run the tools it asks for, send the results back, repeat. Return the final text.

    - messages starts as [{"role": "user", "content": question}]
    - each turn: client.messages.create(model=MODEL, max_tokens=4096, system=SYSTEM, tools=TOOLS, messages=messages)
    - append the assistant reply to messages (never edit earlier messages)
    - if resp.stop_reason != "tool_use": return the text of the first text block ("" if none)
    - otherwise run EVERY tool_use block and send all the tool_results back in ONE user message
    - after max_steps turns without an answer, return a string that says it stopped, e.g. "[stopped after 3 steps]"
    """
    # TODO
    raise NotImplementedError("TODO: run_agent")


if __name__ == "__main__":
    args = sys.argv[1:]
    approve = input
    for flag, answer in (("--yes", "y"), ("--no", "n")):
        if flag in args:
            args.remove(flag)
            approve = (lambda a: lambda prompt: (print(f"{prompt}{a}   (scripted)"), a)[1])(answer)
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("No ANTHROPIC_API_KEY set. Run `pytest` to test your agent with the scripted fake model.")
    import anthropic
    print(run_agent(" ".join(args) or "Where is ORD-1003?", anthropic.Anthropic(), approve=approve))
