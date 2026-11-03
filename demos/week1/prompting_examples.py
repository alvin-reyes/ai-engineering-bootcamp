"""Week 1 demo (deck slide 04): one task, five prompts, compared side by side.

    python week1/prompting_examples.py
    DEMO_OFFLINE=1 python week1/prompting_examples.py     no key: canned replies show the shape, not a real model

Task: turn a support ticket into something a team can act on.
Passes: 1 weak, 2 goal + context + format, 3 a system prompt, 4 examples (few-shot), 5 structured JSON (schema).
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # the demos/ folder, for offline.py
from offline import get_client, reply, text  # noqa: E402

MODEL = os.environ.get("DEMO_MODEL", "claude-opus-5-5")
TICKET = ("Hi team, since Tuesday's update our nightly export to the finance sheet fails with 'timeout after 30s'. "
          "Finance needs the file by 8am for payroll. We tried twice. Please help asap.")
SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "priority": {"type": "string", "enum": ["P1", "P2", "P3"]},
        "next_action": {"type": "string"},
        "needs_human": {"type": "boolean"},
    },
    "required": ["summary", "priority", "next_action", "needs_human"],
    "additionalProperties": False,
}
SYSTEM = "You are a support triage assistant for an IT team. Be factual. Never promise a fix time."
STRONG = ("Summarize this support ticket for the on-call engineer in two sentences. "
          "Say what broke, since when, and the deadline. Do not guess a cause.\n\n<ticket>\n" + TICKET + "\n</ticket>")
EXAMPLES = ("Classify the ticket's priority as P1 (blocks payroll or customers), P2 (a team is slowed) or P3 (a nuisance). "
            "Answer with the label and one reason.\n\n"
            "<example>Ticket: The office printer is out of toner.\nAnswer: P3. No work is blocked.</example>\n"
            "<example>Ticket: Checkout page returns errors for all customers.\nAnswer: P1. Customers cannot pay.</example>\n\n"
            "<ticket>\n" + TICKET + "\n</ticket>")

PASSES = [  # (label, create() arguments)
    ("1 Weak prompt", dict(messages=[{"role": "user", "content": "summarize this ticket: " + TICKET}])),
    ("2 Goal + context + format", dict(messages=[{"role": "user", "content": STRONG}])),
    ("3 Plus a system prompt", dict(system=SYSTEM, messages=[{"role": "user", "content": STRONG}])),
    ("4 Examples (few-shot)", dict(system=SYSTEM, messages=[{"role": "user", "content": EXAMPLES}])),
    ("5 Structured output (JSON schema)", dict(system=SYSTEM, messages=[{"role": "user", "content": STRONG}],
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}})),
]
CANNED = [  # offline only, in pass order
    "This ticket is about an export problem. The user is having trouble and wants help soon. It seems important and "
    "there are a few details about timing. Let me know if you need more information about what they said.",
    "The nightly export to the finance sheet has failed with 'timeout after 30s' since Tuesday's update, twice so far. "
    "Finance needs the file by 8am for payroll.",
    "The nightly finance export has timed out ('timeout after 30s') since Tuesday's update and was retried twice. "
    "The 8am payroll deadline is at risk. Cause not known.",
    "P1. The failing export blocks payroll, which is due at 8am.",
    json.dumps({"summary": "Nightly finance export times out after Tuesday's update; payroll file due 8am.",
                "priority": "P1", "next_action": "Check export job logs and the 30s timeout setting since Tuesday's release.",
                "needs_human": True}),
]
client = get_client(lambda kw, n: reply(text(CANNED[n - 1])))


def main():
    for label, args in PASSES:
        r = client.messages.create(model=MODEL, max_tokens=1024, **args)
        body = next(b.text for b in r.content if b.type == "text")
        print(f"\n=== {label}   [in={r.usage.input_tokens} out={r.usage.output_tokens}]")
        print("prompt:", args["messages"][0]["content"].split("\n")[0][:90])
        if "output_config" in args:
            data = json.loads(body)  # valid JSON by construction, but check what your code relies on
            missing = [k for k in SCHEMA["required"] if k not in data]
            print(json.dumps(data, indent=2))
            print("required keys present:", not missing, "| priority in P1/P2/P3:", data["priority"] in ("P1", "P2", "P3"))
        else:
            print(body)


if __name__ == "__main__":
    main()
