"""Week 4 demo: tracing and cost. Wrap every model call, log one JSON line per call, print a per-run summary.

    python week4/tracing_cost.py                    # live (needs ANTHROPIC_API_KEY)
    DEMO_OFFLINE=1 python week4/tracing_cost.py     # scripted answers and token counts, no key
    python week4/tracing_cost.py --per-day 2000     # project the cost of 2000 requests a day

Each trace line has: call number, task, model, latency, tokens (input / output / cache write / cache read),
estimated cost in USD. Lines go to stdout and to a file (DEMO_TRACE_FILE, default: week4-traces.jsonl in the temp folder). The summary table is the
"cost per request" number every capstone shows on demo day.
"""
import json
import os
import sys
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace as NS

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # the demos folder, for offline.py
from offline import approx_tokens, get_client, reply, text  # noqa: E402

MODEL = os.environ.get("DEMO_MODEL", "claude-opus-5-5")

# Example prices, USD per million tokens. NOT real quotes: VERIFY against the current pricing page before you
# show a cost to anyone. Cache write = 1.25x input and cache read = 0.1x input is the usual pattern; VERIFY that too.
PRICE_INPUT = 5.00        # example price, VERIFY
PRICE_OUTPUT = 25.00      # example price, VERIFY
PRICE_CACHE_WRITE = 6.25  # example price, VERIFY
PRICE_CACHE_READ = 0.50   # example price, VERIFY

TRACE_FILE = Path(os.environ.get("DEMO_TRACE_FILE", Path(tempfile.gettempdir()) / "week4-traces.jsonl"))
SYSTEM = "You are a support triage assistant. Reply with a category and a one-line summary."
TASKS = {
    "refund": "Customer says the monitor arrived cracked and wants a refund. Order ORD-1002.",
    "shipping": "Where is order ORD-1003? Tracking has not changed for two days.",
    "how-to": "How do I reset my password? I do not get the email.",
    "long-ticket": "Hello team. " + "The app logs me out every hour and I lose my work. " * 40 + "Please fix.",
}
ANSWERS = {
    "refund": "Category: refund. Damaged item, within 30 days, photo needed.",
    "shipping": "Category: shipping. Tracking stalled; check the carrier.",
    "how-to": "Category: account. Password reset email not arriving.",
    "long-ticket": "Category: bug. Session expires hourly and loses unsaved work.",
}


def estimate_cost(u):
    """USD from a usage object. Missing fields count as 0."""
    g = lambda name: getattr(u, name, 0) or 0  # noqa: E731
    return (g("input_tokens") * PRICE_INPUT + g("output_tokens") * PRICE_OUTPUT
            + g("cache_creation_input_tokens") * PRICE_CACHE_WRITE
            + g("cache_read_input_tokens") * PRICE_CACHE_READ) / 1_000_000


class Tracer:
    """Wraps client.messages.create. Records a trace line per call, even when the call fails."""

    def __init__(self, client, path=TRACE_FILE):
        self.client, self.path, self.rows = client, path, []
        self.path.write_text("")

    def call(self, task, **kw):
        t0 = time.perf_counter()
        row = {"call": len(self.rows) + 1, "task": task, "model": kw.get("model")}
        try:
            r = self.client.messages.create(**kw)
        except Exception as e:  # trace failures too: an error is a data point
            row.update(latency_ms=round((time.perf_counter() - t0) * 1000), error=type(e).__name__, cost_usd=0.0)
            self._log(row)
            raise
        u = r.usage
        row.update(latency_ms=round((time.perf_counter() - t0) * 1000),
                   input_tokens=u.input_tokens, output_tokens=u.output_tokens,
                   cache_write=getattr(u, "cache_creation_input_tokens", 0) or 0,
                   cache_read=getattr(u, "cache_read_input_tokens", 0) or 0,
                   stop_reason=r.stop_reason, cost_usd=round(estimate_cost(u), 6))
        self._log(row)
        return r

    def _log(self, row):
        self.rows.append(row)
        line = json.dumps(row)
        print("TRACE", line)
        with self.path.open("a") as f:
            f.write(line + "\n")

    def summary(self, per_day=None):
        n = len(self.rows)
        lat = sorted(r["latency_ms"] for r in self.rows)
        cost = sum(r["cost_usd"] for r in self.rows)
        print("\n call  task          in_tok  out_tok  latency_ms   cost_usd")
        for r in self.rows:
            print(f" {r['call']:>4}  {r['task']:<12} {r.get('input_tokens', 0):>7} {r.get('output_tokens', 0):>8} "
                  f"{r['latency_ms']:>11}   {r['cost_usd']:>8.5f}")
        print(f" total {n} calls, cost ${cost:.5f}, per request ${cost / n:.5f}, "
              f"median latency {lat[n // 2]} ms, max {lat[-1]} ms")
        if per_day:
            print(f" at {per_day} requests/day: ${cost / n * per_day:,.2f}/day, ${cost / n * per_day * 30:,.2f}/30 days "
                  "(example prices, VERIFY)")


def responder(kw, n):
    time.sleep(0.05 * n)  # offline only: pretend the model takes longer on later calls
    task = next((k for k, v in TASKS.items() if v == kw["messages"][0]["content"]), "refund")
    return reply(text(ANSWERS[task]))


if __name__ == "__main__":
    per_day = int(sys.argv[sys.argv.index("--per-day") + 1]) if "--per-day" in sys.argv else None
    tracer = Tracer(get_client(responder))
    for name, prompt in TASKS.items():
        tracer.call(name, model=MODEL, max_tokens=200, system=SYSTEM,
                    messages=[{"role": "user", "content": prompt}])
    tracer.summary(per_day)
    print(f"\ntrace file: {TRACE_FILE}")
