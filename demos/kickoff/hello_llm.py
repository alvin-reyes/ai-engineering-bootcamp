"""Kickoff · Builder track · "Hello, LLM": stream one reply from Claude.

    pip install -r ../requirements.txt
    export ANTHROPIC_API_KEY=...          # never commit it
    python hello_llm.py "Explain tokens in one line."
    DEMO_OFFLINE=1 python hello_llm.py        no key or no Wi-Fi: a canned reply (says so)
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # the demos/ folder, for offline.py
from offline import get_client, reply, text  # noqa: E402

MODEL = os.environ.get("DEMO_MODEL", "claude-opus-5-5")

CANNED = ("Tokens are the small chunks of text (often a word or part of a word) that a model reads and writes, "
          "and they are what you pay for.")
client = get_client(lambda kw, n: reply(text(CANNED)))  # live: reads ANTHROPIC_API_KEY from the environment
prompt = " ".join(sys.argv[1:]) or "Explain tokens in one line."

with client.messages.stream(
    model=MODEL,
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    final = stream.get_final_message()

print(f"\n\n[stop_reason={final.stop_reason}  input_tokens={final.usage.input_tokens}  "
      f"output_tokens={final.usage.output_tokens}]")
