"""Week 4 demo: prompt caching. Run the same long, stable prefix twice and watch the cache.

    python week4/caching_demo.py              # call 1 writes the cache, calls 2 and 3 read it
    python week4/caching_demo.py --break      # adds a timestamp to the system prompt: the cache never hits
    DEMO_OFFLINE=1 python week4/caching_demo.py   # no key needed: scripted token counts (mechanics only)

The prefix must be long enough to cache (the minimum depends on the model; VERIFY on the pricing/caching docs),
so this repeats the week 3 handbook 40 times (about 9k tokens). Live, the first call may show a cache write and
later calls reads; the exact numbers come from the API, not from this file.
"""
import datetime
import os
import sys
from pathlib import Path
from types import SimpleNamespace as NS

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # the demos folder, for offline.py
from offline import approx_tokens, get_client, reply, text  # noqa: E402

MODEL = os.environ.get("DEMO_MODEL", "claude-opus-5-5")
HANDBOOK = (Path(__file__).parent.parent / "week3/docs/handbook.md").read_text()
STABLE = "You answer staff questions from this handbook. Be brief.\n\n" + "\n\n".join([HANDBOOK] * 40)
QUESTIONS = ["How many leave days do I get?", "What is the meal allowance?", "When must I report a lost laptop?"]
ANSWERS = ["25 days of annual leave for full-time staff.", "Up to 50 EUR per day when travelling.", "Within 24 hours."]


def responder(kw, n):
    return reply(text(ANSWERS[(n - 1) % len(ANSWERS)]))


_seen = set()


def usage(kw, n, inp, spec):
    """Offline stand-in for the API's cache accounting: a system prompt seen before is a cache read."""
    system = kw["system"]
    prefix = approx_tokens(system)
    rest = max(1, inp - prefix)
    hit = system in _seen
    _seen.add(system)
    return NS(input_tokens=rest, output_tokens=approx_tokens(spec["content"]),
              cache_creation_input_tokens=0 if hit else prefix, cache_read_input_tokens=prefix if hit else 0)


client = get_client(responder, usage)
for i, question in enumerate(QUESTIONS, 1):
    system = STABLE + (f"\n\nNow: {datetime.datetime.now().isoformat()}" if "--break" in sys.argv else "")
    response = client.messages.create(
        model=MODEL,
        max_tokens=512,
        cache_control={"type": "ephemeral"},
        system=system,
        messages=[{"role": "user", "content": question}],
    )
    u = response.usage
    print(f"call {i}: cache_write={u.cache_creation_input_tokens}  cache_read={u.cache_read_input_tokens}  "
          f"uncached_input={u.input_tokens}")
