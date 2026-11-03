"""Week 2 demo: the same job as a fixed workflow and as an agent loop. When is the workflow better?

    python agent_vs_workflow.py
    DEMO_OFFLINE=1 python agent_vs_workflow.py     # no key: canned responses, mechanics only

The job: answer four support tickets from the help docs. Three are plain policy questions (the steps are known:
classify, look up the doc, draft). The fourth needs an order lookup first (the steps depend on what it finds).
Counts of model calls and tokens are printed for each. Offline the token counts are rough estimates and the
agent's extra steps are scripted; live, the agent's step count varies from run to run (run it twice).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # the demos/ folder
from offline import get_client, reply, text, tool  # noqa: E402

import support_agent as sa  # noqa: E402  (reuses its tools, SYSTEM prompt and agent loop)

MODEL = os.environ.get("DEMO_MODEL", "claude-opus-5-5")
TICKETS = [
    "How long does standard shipping take?",
    "Can I return an unused keyboard?",
    "What is your refund policy for damaged items?",
    "Where is ORD-1003, and is it late?",
]
CATEGORIES = ["shipping", "returns", "refunds", "order"]


class Counting:
    """Wraps a client and counts model calls and tokens (works for the real client and the offline one)."""

    def __init__(self, client):
        self._client, self.calls, self.tokens = client, 0, 0
        self.messages = self

    def create(self, **kw):
        resp = self._client.messages.create(**kw)
        self.calls += 1
        self.tokens += resp.usage.input_tokens + resp.usage.output_tokens
        return resp


def first_text(resp):
    return next((b.text for b in resp.content if b.type == "text"), "").strip()


# ---- A: the workflow. Your code owns the steps; the model fills in two of them. -----------------------------
def workflow_responder(kwargs, call_no):
    raw = kwargs["messages"][0]["content"]
    q = raw.lower()
    if kwargs["system"].startswith("Classify"):
        for word, cat in (("shipping", "shipping"), ("return", "returns"), ("refund", "refunds"), ("ord-", "order")):
            if word in q:
                return reply(text(cat))
        return reply(text("order"))
    article = raw.split("Help article:")[-1].strip()
    return reply(text(f"Hi! {article} Anything else I can help with?"))


def run_workflow(client, ticket):
    cat = first_text(client.messages.create(            # step 1: model classifies
        model=MODEL, max_tokens=10, system=f"Classify the ticket. Reply with one word from {CATEGORIES}.",
        messages=[{"role": "user", "content": ticket}])).lower()
    doc = sa.HELP_DOCS.get(cat)                          # step 2: plain code, no model, no surprises
    if doc is None:
        return cat, None                                 # the workflow has no step for this: hand it on
    draft = first_text(client.messages.create(          # step 3: model drafts, grounded in the doc
        model=MODEL, max_tokens=300, system="Draft a short, friendly reply using only the help article.",
        messages=[{"role": "user", "content": f"Ticket: {ticket}\n\nHelp article: {doc}"}]))
    return cat, draft


# ---- B: the agent. The model picks the steps. -------------------------------------------------------------
def agent_responder(kwargs, call_no):
    messages = kwargs["messages"]
    q = messages[0]["content"]
    step = (len(messages) - 1) // 2
    if "ORD-1003" in q:
        if step == 0:
            return reply(tool("get_order", {"order_id": "ORD-1003"}))
        return reply(text("ORD-1003 (Keyboard) is in transit with an ETA of 2026-11-04. Delivery is 3-5 business "
                          "days from dispatch, so it is not late yet."))
    topic = "returns" if "return" in q else "refund" if "refund" in q else "shipping"
    if step == 0:
        return reply(tool("search_help", {"query": topic}))
    if topic == "returns" and step == 1:               # scripted: an agent may double-check, and that costs a call
        return reply(tool("search_help", {"query": "shipping"}))
    answers = {"shipping": "Standard shipping takes 3-5 business days.",
               "returns": "Unused items can be returned within 14 days; you pay the return shipping.",
               "refund": "Damaged items can be refunded within 30 days of delivery, with a photo."}
    return reply(text(answers[topic]))


def run_agent_for(client, ticket):
    return sa.run_agent(ticket, client=client, approve=lambda p: "n")


def main():
    print("== A. Workflow: classify -> look up doc (code) -> draft ==")
    wf = Counting(get_client(workflow_responder))
    escalated = []
    for t in TICKETS:
        cat, draft = run_workflow(wf, t)
        if draft is None:
            escalated.append(t)
            print(f"  [{cat}] {t}\n      -> no fixed step for this: send to the agent (or a human)")
        else:
            print(f"  [{cat}] {t}\n      -> {draft}")
    print(f"  model calls: {wf.calls}   tokens: {wf.tokens}   (3 tickets x 2 calls + 1 classify; same every run)")

    print("\n== B. Agent: the model decides the steps (all four tickets) ==")
    ag = Counting(get_client(agent_responder))
    for t in TICKETS:
        before = ag.calls
        answer = run_agent_for(ag, t)
        print(f"  {t}\n      -> {answer}\n      ({ag.calls - before} model calls)")
    print(f"  model calls: {ag.calls}   tokens: {ag.tokens}   (varies run to run)")

    print("\n== Verdict ==")
    print("  Known steps (tickets 1-3): the workflow is cheaper, faster, and the same every run.")
    print(f"  Steps depend on what it finds ({len(escalated)} ticket): only the agent can do it. Use both: workflow first,")
    print("  agent for what the workflow cannot route.")


if __name__ == "__main__":
    main()
