"""Week 1 demo: a streaming terminal chat with memory, stop_reason checks and a structured summary.

    python week1/stream_chat.py              chat by hand (works from demos/ or demos/week1/)
    python week1/stream_chat.py --script     replay a fixed list of turns, nothing to type
    DEMO_OFFLINE=1 python week1/stream_chat.py --script    no key, no Wi-Fi: canned replies

    you> ...            chat; the whole history is sent each turn (the API is stateless)
    you> /short <text>  ask with max_tokens=25 so the reply is cut off (see the stop_reason check)
    you> /summary       the conversation as JSON that matches SUMMARY_SCHEMA
    you> /tokens        how many input tokens the history costs now
    you> /quit
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # the demos/ folder, for offline.py
import anthropic  # noqa: E402
from offline import get_client, reply, text  # noqa: E402

MODEL = os.environ.get("DEMO_MODEL", "claude-opus-5-5")
SYSTEM = "You are a concise assistant for an AI engineering bootcamp. Answer in at most five sentences."
SUMMARY_SCHEMA = {
    "type": "object",
    "properties": {
        "topic": {"type": "string"},
        "key_points": {"type": "array", "items": {"type": "string"}},
        "open_questions": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["topic", "key_points", "open_questions"],
    "additionalProperties": False,
}
# What --script feeds in: memory (turn 3), cost (/tokens), a cut-off reply (/short), a structured summary.
SCRIPT = [
    "What is a token, in one sentence?",
    "Why does my bill depend on tokens and not words?",
    "What was my first question?",
    "/tokens",
    "/short Explain the context window in detail.",
    "/summary",
]


# ---- offline only: canned replies that still use the history, so memory is visible ----
def _plain(content):
    if isinstance(content, str):
        return content
    return " ".join(getattr(b, "text", None) or b.get("text", "") for b in content)


def responder(kw, call_no):
    msgs = kw["messages"]
    users = [_plain(m["content"]) for m in msgs if m["role"] == "user"]
    last = users[-1]
    if "output_config" in kw:  # the /summary call
        asked = [u for u in users if not u.startswith("Summarize")]
        data = {
            "topic": "Tokens, cost and context in LLM apps",
            "key_points": ["A token is a piece of a word; cost is counted in tokens",
                           "The API is stateless: the whole history is sent every turn",
                           f"The user asked {len(asked)} questions so far"],
            "open_questions": ["How do I choose max_tokens for long answers?"],
        }
        return reply(text(json.dumps(data)))
    low = last.lower()
    if "first question" in low:
        out = f'Your first question was: "{users[0]}". I can see it because the app sent the whole history again.'
    elif "just ask" in low or "last question" in low:
        out = f'You just asked: "{users[-2]}" ' if len(users) > 1 else "This is your first message."
    elif "stateless" in low or "remember" in low:
        out = ("The API keeps nothing between calls: the model only sees what you send. So your app stores "
               "the conversation and sends all of it again every turn. That is also why long chats cost more.")
    elif "context window" in low:
        out = ("The context window is everything the model can see in one call: the system prompt, the whole "
               "conversation so far, any tools and documents, and the reply it is writing. It is measured in "
               "tokens, and anything outside it does not exist for the model.")
    elif "bill" in low or "cost" in low:
        out = ("Providers price by tokens because tokens are what the model actually processes: input tokens "
               "(everything you send) and output tokens (what it writes) are billed separately. Words vary "
               "in length, so tokens are the fairer unit.")
    elif "token" in low:
        out = "A token is a small piece of text, often part of a word, that the model reads and writes as its unit."
    else:
        out = "Good question. Ask me about tokens, the context window or stop_reason and I will answer briefly."
    if kw["max_tokens"] < 60:  # simulate being cut off
        return reply(text(" ".join(out.split()[:12])), stop="max_tokens")
    return reply(text(out))


client = get_client(responder)
history = []


def ask(user_text, max_tokens=2048):
    history.append({"role": "user", "content": user_text})
    with client.messages.stream(model=MODEL, max_tokens=max_tokens, system=SYSTEM, messages=history) as stream:
        for chunk in stream.text_stream:
            print(chunk, end="", flush=True)
        final = stream.get_final_message()
    history.append({"role": "assistant", "content": final.content})
    if final.stop_reason == "max_tokens":
        print("\n[cut off at max_tokens: raise max_tokens or ask for less]")
    print(f"\n[stop_reason={final.stop_reason}  in={final.usage.input_tokens}  out={final.usage.output_tokens}]")


def summary():
    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=SYSTEM,
        messages=history + [{"role": "user", "content": "Summarize our conversation so far."}],
        output_config={"format": {"type": "json_schema", "schema": SUMMARY_SCHEMA}},
    )
    body = next(b.text for b in response.content if b.type == "text")
    print(json.dumps(json.loads(body), indent=2))


def handle(line):
    """Run one line. Returns False to stop."""
    if line == "/quit":
        return False
    if line == "/summary":
        summary() if history else print("Say something first.")
    elif line == "/tokens":
        count = client.messages.count_tokens(model=MODEL, system=SYSTEM,
                                             messages=history or [{"role": "user", "content": "hi"}])
        print(f"{count.input_tokens} input tokens")
    elif line:
        short = line.startswith("/short ")
        try:
            ask(line[7:] if short else line, max_tokens=25 if short else 2048)
        except anthropic.RateLimitError:
            history.pop()
            print("[rate limited: wait and retry; the SDK already retried twice]")
        except anthropic.APIStatusError as exc:
            history.pop()
            print(f"[API error {exc.status_code}: fix the request, don't just retry]")
    return True


def main():
    if "--script" in sys.argv:
        for line in SCRIPT:
            print(f"\nyou> {line}")
            handle(line)
        return
    while True:
        try:
            line = input("\nyou> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not handle(line):
            break


if __name__ == "__main__":
    main()
